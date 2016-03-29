from __future__ import with_statement
import serial
import time
import socket
import os
import re
import sys
import select

base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]

CRC8Table = [
  0, 94, 188, 226, 97, 63, 221, 131, 194, 156, 126, 32, 163, 253, 31, 65,
  157, 195, 33, 127, 252, 162, 64, 30, 95, 1, 227, 189, 62, 96, 130, 220,
  35, 125, 159, 193, 66, 28, 254, 160, 225, 191, 93, 3, 128, 222, 60, 98,
  190, 224, 2, 92, 223, 129, 99, 61, 124, 34, 192, 158, 29, 67, 161, 255,
  70, 24, 250, 164, 39, 121, 155, 197, 132, 218, 56, 102, 229, 187, 89, 7,
  219, 133, 103, 57, 186, 228, 6, 88, 25, 71, 165, 251, 120, 38, 196, 154,
  101, 59, 217, 135, 4, 90, 184, 230, 167, 249, 27, 69, 198, 152, 122, 36,
  248, 166, 68, 26, 153, 199, 37, 123, 58, 100, 134, 216, 91, 5, 231, 185,
  140, 210, 48, 110, 237, 179, 81, 15, 78, 16, 242, 172, 47, 113, 147, 205,
  17, 79, 173, 243, 112, 46, 204, 146, 211, 141, 111, 49, 178, 236, 14, 80,
  175, 241, 19, 77, 206, 144, 114, 44, 109, 51, 209, 143, 12, 82, 176, 238,
  50, 108, 142, 208, 83, 13, 239, 177, 240, 174, 76, 18, 145, 207, 45, 115,
  202, 148, 118, 40, 171, 245, 23, 73, 8, 86, 180, 234, 105, 55, 213, 139,
  87, 9, 235, 181, 54, 104, 138, 212, 149, 203, 41, 119, 244, 170, 72, 22,
  233, 183, 85, 11, 136, 214, 52, 106, 43, 117, 151, 201, 74, 20, 246, 168,
  116, 42, 200, 150, 21, 75, 169, 247, 182, 232, 10, 84, 215, 137, 107, 53
]


def _dec2hex(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 16)
        mid.append(base[rem])
    return ''.join([str(x) for x in mid[::-1]])

def _CRC8(Temp, str):
    for i in range(1, len(str)+1):
        Temp = CRC8Table[Temp ^ ord(str[i-1:i])]
    CRC = hex(Temp)
    return CRC

def _set_HX_channel_command(channel_value):
    if(0 > channel_value or 127 < channel_value):
        #print
        raise Exception, "Attenuation Value is out of range!"

    check_sum = 0x10 + channel_value
    set_value  = '%c' * 5 % (0x7e, 0x7e, 0x10, channel_value, check_sum)
    return set_value

def _read_HX_channel_command():
    set_value  = '%c' * 5 % (0x7e, 0x7e, 0x30, 0x00, 0x30)
    return set_value

def _serial_open(com_port)  :
    ser = serial.Serial(com_port,\
                        baudrate = 9600, \
                        bytesize = 8,\
                        parity = 'N',\
                        stopbits = 1,\
                        timeout = 0)

    if ser is not None:
        print "%s open ok" % com_port
        return ser
    else:
        #print
        raise Exception, "%s open fail" % com_port

def _socket_open(conn):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    host, port = conn.split(",")
    sock.connect((host, int(port)))
    return sock

def _serial_write_and_read_HX(serial, value, read_len):
    retValue = [0 for x in range(read_len)]
    serial.write(value)

    time.sleep(0.2)
    for iIndex in range(read_len):
        tmp = serial.read(1)

        retValue[iIndex] = hex(ord(tmp))

    return retValue

def _serial_write_and_read_HJ(serial, msg):
    serial.write(msg)
    time.sleep(0.25)
    return serial.readline()

def _socket_write_and_read_HJ(sock, msg):
    try:
        time.sleep(0.05)
        sock.sendall(msg)
        print "command send ok !"
        ret = ""
        while select.select([sock.fileno()], [], [], 3) != ([], [], []):
            break
        ret = sock.recv(len(msg))
        #print "get response ok !"
        return ret

    except Exception, error:
        print error
        time.sleep(0.25)
        sock.sendall(msg)
        print "command send ok !"
        ret = ""
        while select.select([sock.fileno()], [], [], 3) != ([], [], []):
            break
        ret = sock.recv(len(msg))
        #print "get response ok !"
        return ret


class JieXi:
    def __init__(self, conn = "192.168.0.254,80"):
        """
        conn should be : host, port
        """
        self.host, self.port = conn.split(",")

    def clean_scoket(self):
        try:
            for line in os.popen("netstat -ano").readlines():
##                if line.find("PID") > 0:
##                    P_index = line.split("  ").index("PID")
##                    print line
##                    continue
                if line.find("%s:%s" %(self.host, self.port)) >0 :
                    os.system("taskkill /F /PID %s" %(line.split()[-1]))
                    break
                continue
            print "Clean socket success!"
        except Exception, e:
            print "Error happend on clean_socket: ", e

    def socket_open(self):
        #self.clean_scoket()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(3)
        self.sock.connect((self.host, int(self.port)))
        print "Have open socket ip: %s, port: %s" % (self.host , self.port)

    def socket_close(self):
        self.sock.close()
        print "Have close the socket ip: %s, port: %s" % (self.host , self.port)

    def __enter__(self):
        self.socket_open()
        self.socket_write("*SETREMOTE")
        return self

    def socket_write(self, msg):
        print ">>> ", msg
        if self.port == '80':
            self.sock.sendall("%s\0" %(msg))
        elif self.port == '1000':
            self.sock.sendall("%s\r\n" %(msg))
        else:
            raise Exception, "Wrong port input, 8pipe is 80, 16pipe is 1000."
        time.sleep(0.5)

    def socket_write_and_read(self, msg):
        print ">>> ", msg
        if self.port == '80':
            self.sock.sendall("%s\0" %(msg))
        elif self.port == '1000':
            self.sock.sendall("%s\r\n" %(msg))
        else:
            raise Exception, "Wrong port input, 8pipe is 80, 16pipe is 1000."
        time.sleep(0.5)
        ret = self.sock.recv(1024)
        print "<<< ", ret
        return ret

    def __exit__(self, type, value, traceback):
        self.socket_close()
        return False

def set_attenuation_fix_value(vendor_channel_info, channel_value):
    """This keyword can change attenuation value once, with different kind of PA equipment

    | Input Parameters       | Man. | Description |
    | vendor_channel_info    | Yes  | vendor, connection type, and channels |
    | channel_value          | Yes  | the attenuation value you want to set, scope is 0~127 |

    Example
    For HuaXiang PA(serial port)
    | Set Attenuation Fix Value | HX:Com2 | 3 |
    For HuaXiang PA(Eth port)
    | Set Attenuation Fix Value | HX:192.168.1.18:2 | 3 |
    For HaoJing PA(Eth port)
    | Set Attenuation Fix Value | HJ:192.168.1.18,10001:2 | 3 |
    For HaoJing PA(serial port)
    | Set Attenuation Fix Value | HJ:COM2:2 | 3 |
    For JieXi PA (socket)
    | Set Attenuation Fix Value | JX:192.168.1.18,80:2 | 3 |
    """
    if vendor_channel_info == "":
        print "*INFO* There is no attenuator on you test bed, Return!"
        return
    channel_value = int(channel_value)

    tmp = vendor_channel_info.split(':')
    vendor = tmp[0]
    conn_type = tmp[1]

    if vendor == "HX" and not re.match('^\d+.\d+.\d+.\d+$', conn_type):
        serial = _serial_open(conn_type)
        try:
            if serial:
                set_value = _set_HX_channel_command(channel_value)
                ReadBackValue = _serial_write_and_read_HX(serial, set_value, 6)
                if hex(channel_value) == ReadBackValue[3] and \
                              hex(32) == ReadBackValue[2]:
                    print "Set channel_value %d Ok" % channel_value
                else:
                    raise Exception, "set_value Fail"
        finally:
            serial.close()

    elif vendor == 'HX' and re.match('^\d+.\d+.\d+.\d+$', conn_type):
        if channel_value < 0 or channel_value > 126:
            raise Exception, "Channel value most be in 0dB to 126dB, '%d' is invalid !" % channel_value
        ip = conn_type
        channel = int(tmp[2])
        value = channel_value * 2
        num = _dec2hex(channel)
        if value == 0:
            val = '0'
        else:
            val = _dec2hex(value)
        if channel < 16 and value < 16:
            inf = ['$HX,C,','0',num,'0',val,'*']
            cmd = ''
            cmd = ''.join(inf)
        if channel < 16 and value >= 16:
            inf = ['$HX,C,''0',num,val,'*']
            cmd = ''
            cmd = ''.join(inf)
        if channel >= 16 and value < 16:
            inf = ['$HX,C,',num,'0',val,'*']
            cmd = ''
            cmd = ''.join(inf)
        if channel >= 16 and value >= 16:
            inf = ['$HX,C,',num,val,'*']
            cmd = ''
            cmd = ''.join(inf)
        crc = _CRC8(0, cmd)
        crc = crc[2:4].upper()
        if len(crc) == 1:
            crc = '0' + crc
        cmd = cmd + crc
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, 4001))
            sock.send(cmd)
            print "Cmd: ", cmd
            res=sock.recv(1024)
            print ">>>" , res
        finally:
            sock.close()

    elif vendor == 'HJ':
        channel = tmp[2]
        if conn_type.startswith('COM'):
            serial = _serial_open(conn_type)
            try:
                if serial:
                    read_back_msg = _serial_write_and_read_HJ(serial, \
                                     "ATT %s %d\r\n" % (channel, channel_value))
                    print read_back_msg
            finally:
                serial.close()
        else:
            sock = _socket_open(conn_type)
            try:
                if sock:
                    read_back_msg = _socket_write_and_read_HJ(sock, \
                                    "ATT %s %d\r\n" % (channel, channel_value))
                    print read_back_msg
            finally:
                sock.close()
    elif vendor.upper().strip() == "JX":
        port = conn_type.split(',')[1]
        if port == '80':
            with JieXi(conn_type) as s:
                s.socket_write("BO%s %s" %(tmp[2], channel_value))
        elif port == '1000':
            with JieXi(conn_type) as s:
                s.socket_write("SET:%s:%s" %(tmp[2], channel_value))
        else:
            raise Exception, "Wrong port input, 8pipe is 80, 16pipe is 1000."
        time.sleep(1)
    else:
        raise Exception, "Please check the argument1, sample as: \
                              HX:COM2 or HJ:COM1:2 or HJ:192.168.1.18,10001:3"

def change_attenuation_value_period(vendor_channel_info, min_value, max_value, step, delay = '1'):
    """This keyword can change attenuation value period, with different kind of PA equipment

    | Input Parameters      | Man. | Description |
    | vendor_channel_info   | Yes  | vendor, connection type, and channels |
    | min_value              | Yes  | the min value you want to set(0~127) |
    | max_value              | Yes  | the max value you want to set(0~127) |
    | step                  | Yes  | att. value change step, if step > zero |
    |                       |      | the value change from low to high, |
    |                       |      | otherwise change from high to low |
    | delay                 | No   | attenuation value change delay time, unit: s |

    Example
    For HuaXiang PA(serial port)
    | Change Attenuation Value Period | HX:Com116 | 3 | 20 | 3 | 2 |
    For HuaXiang PA(Eth port)
    | Change Attenuation Value Period | HX:192.168.1.18:2 | 3 | 20 | 3 | 2 |
    For HaoJing PA(Eth port)
    | Change Attenuation Value Period | HJ:192.168.1.18,10001:2 | 3 | 33  | 2 | 2 |
    For HaoJing PA(serial port)
    | Change Attenuation Value Period | HJ:COM1:2 | 3 | 33  | -2  | 1 |
    For JieXi PA (socket)
    | Change Attenuation Value Period | JX:192.168.0.80,10001:2 | 3 | 33  | 2 | 2 |

    """
    if vendor_channel_info == "":
        print "*INFO* There is no attenuator on you test bed, Return!"
        return
    step = int(step)
    min_value = int(min_value)
    max_value = int(max_value)
    delay = int(delay)

    if 0 == step:
        raise Exception, "The step should be non-zero, pls modify it!"

    if min_value > max_value:
        raise Exception, "Pls exchange value of min_value and max_value"

    if 0 < step:
        i = min_value
    else:
        i = max_value

    tmp = vendor_channel_info.split(':')
    vendor = tmp[0]
    conn_type = tmp[1]

    if vendor == "HX" and not re.match('^\d+.\d+.\d+.\d+$', conn_type):
        serial = _serial_open(conn_type)
        try:
            if serial:
                while(min_value <= i and  max_value >= i):
                    set_value = _set_HX_channel_command(i)
                    read_value = _serial_write_and_read_HX(serial, set_value, 6)

                    if  hex(i) == read_value[3] and hex(32) == read_value[2]:
                        print "Attenuation set value %d Ok" % i
                    else:
                        raise Exception, "Attenuation set value Failed!"
                    i += step
                    time.sleep(delay - 0.2)

        finally:
            serial.close()

    elif vendor == "HX" and re.match('^\d+.\d+.\d+.\d+$', conn_type):
        if min_value < 0 or max_value > 126:
            raise Exception, "Channel value most be in 0dB to 126dB !"
        ip = conn_type
        channel = int(tmp[2])
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, 4001))
            while(min_value <= i and  max_value >= i):
                value = i * 2
                num = _dec2hex(channel)
                if value == 0:
                    val = '0'
                else:
                    val = _dec2hex(value)
                if channel < 16 and value < 16:
                    inf = ['$HX,C,','0',num,'0',val,'*']
                    cmd = ''
                    cmd = ''.join(inf)
                if channel < 16 and value >= 16:
                    inf = ['$HX,C,''0',num,val,'*']
                    cmd = ''
                    cmd = ''.join(inf)
                if channel >= 16 and value < 16:
                    inf = ['$HX,C,',num,'0',val,'*']
                    cmd = ''
                    cmd = ''.join(inf)
                if channel >= 16 and value >= 16:
                    inf = ['$HX,C,',num,val,'*']
                    cmd = ''
                    cmd = ''.join(inf)
                crc = _CRC8(0, cmd)
                crc = crc[2:4].upper()
                if len(crc) == 1:
                    crc = '0' + crc
                cmd = cmd + crc
                sock.send(cmd)
                res=sock.recv(1024)
                i += step
                time.sleep(delay - 0.2)
        finally:
            sock.close()

    elif vendor == 'HJ':
        channel = tmp[2]
        if conn_type.startswith('COM'):
            serial = _serial_open(conn_type)
            try:
                if serial:
                    while(min_value <= i and  max_value >= i):
                        read_back_msg = _serial_write_and_read_HJ(serial, \
                                               "ATT %s %d\r\n" % (channel, i))
                        print read_back_msg
                        i += step
                        time.sleep(delay - 0.2)
            finally:
                serial.close()
        else:
            sock = _socket_open(conn_type)
            try:
                if sock:
                    while(min_value <= i and  max_value >= i):
                        read_back_msg = _socket_write_and_read_HJ(sock, \
                                               "ATT %s %d\r\n" % (channel, i))
                        print read_back_msg
                        i += step
                        time.sleep(delay - 0.2)
            finally:
                sock.close()
    elif vendor.upper().strip() == "JX":
        port = conn_type.split(',')[1]
        with JieXi(conn_type) as s:
            while (min_value <= i and  max_value >= i):
                if port == '80':
                    cmd = "BO%s %s" %(tmp[2], i)
                elif port == '1000':
                    cmd = "SET:%s:%s" %(tmp[2], i)
                else:
                    raise Exception, "Wrong port input, 8pipe is 80, 16pipe is 1000."
                s.socket_write(cmd)
                i += step
                time.sleep(delay - 0.2)

    else:
        raise Exception, "Please check the argument1, sample as: \
                             HX:COM2 or HJ:COM1:2 or HJ:192.168.1.18,10001:3"


def set_attenuation_multi_channel_value(vendor_channel_info, channel_value_pair, interval = '1'):
    """This keyword change attenuation value of HaoJin's attenuator, gradually and periodically

    | Input Parameters    | Man. | Description |
    | vendor_channel_info | Yes  | vendor:ip,port |
    | channel_value_pair  | Yes  | list [channel:start:stop:step, ...] |
    |                     |      | step, can be < 0 or > 0, cannot be = 0 |
    | interval            | No   | attenuation value change time interval, unit: s |

    Example
    | ${value_list} | create list | 1:10:110:9 | 2:10:110:10 | 3:110:10:-10 |
    | set attenuation multi channel value | HJ:10.68.143.121,50000 | ${value_list} | 5 |
    """
    if vendor_channel_info == "":
        print "*INFO* There is no attenuator on you test bed, Return!"
        return
    interval = float(interval)
    print "Arguments as: %s, %s, %s"%(vendor_channel_info, channel_value_pair, interval)
    channel_list = []
    value_group_list = []
    value_group_max_len = 0
    for data in channel_value_pair:
        channel, value_start, value_stop, step = data.split(':')
        channel_list.append(channel)
        value_start = int(value_start)
        value_stop = int(value_stop)
        step = int(step)
        if step == 0:
            step = 1

        if ((value_start>value_stop) and (step>0)) or\
                (value_start<value_stop) and (step<0):
            step = -step

        value_group = range(value_start, value_stop, step)
        value_group.append(value_stop)
        value_group_list.append(value_group)
        if len(value_group) > value_group_max_len:
            value_group_max_len = len(value_group)


    vendor, conn_type = vendor_channel_info.split(':')

    if "HJ"==vendor:
        sock = _socket_open(conn_type)
        try:
            if sock:
                for value_idx in range(value_group_max_len):
                    command_str = "ATT "
                    command_ret = ""
                    for channel_idx in range(len(channel_list)):
                        if value_idx > len(value_group_list[channel_idx]) - 1:
                            # this channel's all att values have been already sent
                            continue
                        else:
                            channel = channel_list[channel_idx]
                            value = value_group_list[channel_idx][value_idx]
                            command_str += "%s %d;" %(channel, value)
                            command_ret += "ATT %s %d;" %(channel, value)
                            #print "ATT %s %d\r\n" %(channel, value)
                            #str_back = _socket_write_and_read_HJ(sock, "ATT %s %d\r\n" %(channel, value))
                            #if str_back == "ATT %s %d\r\n" %(channel, value):
                            #    print "HaoJin Channel%s Set attenuation value %d OK" %(channel, value)
                            #else:
                            #    print "HaoJin Channel%s Set attenuation value %d FAIL!" %(channel, value)
                    command_str = command_str[0:-1] # delete the last ";"
                    print command_str
                    command_str += "\r\n"
                    command_ret = command_ret[0:-1]
                    command_ret += "\r\n"
                    #a = time.clock()
                    str_back = _socket_write_and_read_HJ(sock, command_str)
                    #print time.clock() - a
                    print "Return string:",str_back
                    print "Expection string:", command_ret
                    if str_back == command_ret:
                        print "HaoJin set attenuation value OK"
                    time.sleep(interval)
        finally:
            #pass
            sock.close()
    elif "JX" == vendor:
        port = conn_type.split(',')[1]
        with JieXi(conn_type) as s:
            for value_idx in range(value_group_max_len):
                for channel_idx in range(len(channel_list)):
                    if value_idx > len(value_group_list[channel_idx]) - 1:
                        # this channel's all att values have been already sent
                        continue
                    else:
                        channel = channel_list[channel_idx]
                        value = value_group_list[channel_idx][value_idx]
                        if port == '80':
                            cmd = "BO%s %d" %(channel, value)
                        elif port == '1000':
                            cmd = "SET:%s:%d" %(channel, value)
                        else:
                            raise Exception, "Wrong port input, 8pipe is 80, 16pipe is 1000."
                        s.socket_write(cmd)
                time.sleep(interval)

    elif vendor == "HX" and re.match('^\d+.\d+.\d+.\d+$', conn_type):
        ip = conn_type
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, 4001))
        try:
            if sock:
                for value_idx in range(value_group_max_len):
                    for channel_idx in range(len(channel_list)):
                        if value_idx > len(value_group_list[channel_idx]) - 1:
                            # this channel's all att values have been already sent
                            continue
                        else:
                            channel = channel_list[channel_idx]
                            channel = int(channel)
                            value = value_group_list[channel_idx][value_idx]
                            value = int(value)
                            print "Set channel: %s value: %s" % (channel, value)
                            if value < 0 or value > 126:
                                raise Exception, "Channel value most be in 0dB to 126dB, '%d' is invalid !" % value
                            value = value * 2
                            num = _dec2hex(channel)
                            if value == 0:
                                val = '0'
                            else:
                                val = _dec2hex(value)
                            if channel < 16 and value < 16:
                                inf = ['$HX,C,','0',num,'0',val,'*']
                                cmd = ''
                                cmd = ''.join(inf)
                            if channel < 16 and value >= 16:
                                inf = ['$HX,C,''0',num,val,'*']
                                cmd = ''
                                cmd = ''.join(inf)
                            if channel >= 16 and value < 16:
                                inf = ['$HX,C,',num,'0',val,'*']
                                cmd = ''
                                cmd = ''.join(inf)
                            if channel >= 16 and value >= 16:
                                inf = ['$HX,C,',num,val,'*']
                                cmd = ''
                                cmd = ''.join(inf)    
                            
                            crc = _CRC8(0, cmd)
                            crc = crc[2:4].upper()
                            if len(crc) == 1:
                                crc = '0' + crc
                            cmd = cmd + crc
                            sock.send(cmd)
                            print "Cmd: ", cmd
                            ret = sock.recv(1024)
                            print ">>>",ret
                    time.sleep(interval)
        finally:
            sock.close() 
    else:
        raise Exception, "Type %s not supported now ! More requirement please contact with TA team." % vendor_channel_info


def set_attenuation_with_irregular_value(vendor_port_info, channel_value_list, interval="1"):
    """This keyword change attenuation  of HaoJin's attenuator with special value,
    | Input Parameters    | Man. | Description |
    | vendor_channel_info | Yes  | vendor:ip,port |
    | channel_value_list  | Yes  | list [channel:value1,value2,value3,value4, ...] |
    | interval            | No   | attenuation value change time interval, unit: s |

    Example
    | ${value_list} | create list | 2 : 5,7,8,25,30 | 5 : 5,7,8,25,30 | 4 : 20,18,15,7,3 |
    | set attenuation with irregular value | HJ:10.68.143.121,50000 | ${value_list} | 5 |    

    """
    if vendor_port_info == "":
        print "*INFO* There is no attenuator on you test bed, Return!"
        return
    interval = float(interval)
    channel_list = []
    value_list = []
    for mod in channel_value_list:
        channel, all_value =  mod.split(":")
        channel_list.append(channel)
        value_list.append(all_value.split(","))

    value_len = []
    for i in range(len(channel_list)):
        value_len.append(len(value_list[i]))

    for vv in range(max(value_len)):
        for ch in range(len(channel_list)):
            if vv >= len(value_list[ch]):
                # this channel's all att values have been already sent
                continue
            else:
                arg1 = vendor_port_info + ":" + channel_list[ch].strip()
                arg2 = value_list[ch][vv].strip()
                print arg1, arg2
                set_attenuation_fix_value(arg1, arg2)
        time.sleep(interval)
        print

def _open_schedule_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((host, int(port)))
    return sock
    
def send_req_and_wait_receive_ok(host, port, msg, max_wait_time):
    src_time = max_wait_time
    start_time = time.clock()
    success_flag = False
    duration = 0
    max_wait_time = float(max_wait_time)
    max_wait_time *= 60
    while duration < max_wait_time:
        try:
            sock = _open_schedule_socket(host, port)
            sock.settimeout(20)
            sock.sendall(msg + "\n")
            time.sleep(2)
            received = sock.recv(500)
            timestmp = time.strftime("%Y%m%d%H%M%S", time.localtime())
            log = "\n%s\nsend -> %s\nreceive <- %s\n" % (timestmp, msg, received)
            sys.__stdout__.write(log)
            print log
            if "Welcome" in received:
                success_flag = True
                print "Successful get tm500 resource!"
                break        
            duration = time.clock() - start_time
            time.sleep(10)
            sock.close()
        except Exception, error:
            print "Error '%s', just remind" % (error)
    if not success_flag:   
        raise Exception, "Couldn't get tm500 resource in %s mins" % src_time
    return success_flag, received


def send_release_to_tm500_server(host, port):
    try:
        sock = _open_schedule_socket(host, port)
        sock.settimeout(20)
        sock.sendall("release\n")
        time.sleep(2)
        received = sock.recv(500)
        timestmp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        log = "\n%s\nsend -> release\nreceive <- %s\n" % (timestmp, received)
        sys.__stdout__.write(log)
        print log
        sock.close()
    except Exception, error:
        print "Error '%s', just remind" % (error)


if __name__ == '__main__':
    #JX and HJ
    #set_attenuation_fix_value('JX:10.69.3.251,1000:2', '88')
    #set_attenuation_fix_value('JX:10.69.3.251,1000:12', '88')
    #set_attenuation_fix_value('JX:10.69.3.251,1000:16', '89')
    a = time.clock()
    #set_attenuation_multi_channel_value("JX:10.69.65.168,80", ['2:110:110:1', '3:110:110:1'])
    set_attenuation_multi_channel_value("HJ:10.69.65.162,50000", ['2:110:110:1', '3:110:110:1'])
    print time.clock() - a
    pass
