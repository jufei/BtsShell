import time
import serial
import os
import subprocess
import sys
import types
import struct
import socket
import logging
import binascii
import string
import random
from optparse import OptionParser
import telnetlib
import traceback

DEBUG_LEVEL_NONE = 0

CYCLERUSER = "login: "
CYCLERPASS = "assword: "


POWER_ON_PORT = ["01050000FF008C3A", "01050001FF00DDFA", "01050002FF002DFA", "01050003FF007C3A", "01050004FF00CDFB", "01050005FF009C3B"]

POWER_OFF_PORT = ["010500000000CDCA", "0105000100009C0A", "0105000200006C0A", "0105000300003DCA", "0105000400008C0B", "010500050000DDCB"]

CHECK_PORT = ["010200000001B9CA", "010200010001E80A", "010200020001180A", "01020003000149CA", "010200040001F80B", "010200050001A9CB"]

DC_ON     = (0x40,0x30,0x30,0x57,0x52,0x30,0x30,0x31,0x30,0x30,0x30,0x30,0x32,0x34,0x36,0x2a,0x0d)
AC_ON     = (0x40,0x30,0x30,0x57,0x52,0x30,0x30,0x31,0x30,0x30,0x30,0x30,0x31,0x34,0x35,0x2A,0x0D)
POWER_OFF = (0x40,0x30,0x30,0x57,0x52,0x30,0x30,0x31,0x30,0x30,0x30,0x30,0x30,0x34,0x34,0x2a,0x0d)
POWER_ON  = (0x40,0x30,0x30,0x57,0x52,0x30,0x30,0x31,0x30,0x30,0x30,0x30,0x33,0x34,0x37,0x2a,0x0d)
#APC
USERPROMPT = "ame :"
PASSWORDPROMPT = "assword  :"


def Reboot_Facom(Host):
    """Reboot Facom Power breaker"""
    try:
        Flag = False
        Prompt = "Key in your selection:"
        cmd1 = "s"
        cmd2 = "y"
        tn = telnetlib.Telnet(Host)
        con1 = tn.read_until(Prompt, 10)
        print con1
        tn.write(cmd1 + "\r\n")
        con2 = tn.read_until(Prompt, 10)
        print con2
        tn.write(cmd2 + "\r\n")
        stime = time.time()
        time.sleep(3)
        while time.time() - stime < 30:
            if os.system("ping %s -n 1" % Host) == 0:
                Flag = True
                break
            time.sleep(1)
        if Flag:
            print "Reboot Facom PB successfully"
        else:
            print "Reboot Facom PB failed in 30 sec!"
        return Flag
    except Exception, e:
        print e
        exit(-1)
    finally:
        tn.close()


def CheckPort(ipaddr, port):
    """Check port statu and release port if it is obtained

        Input parameters:
            [1] ipaddr
            [2] port
        Output parameters:
            True if success
            False if failed.
    """
    PortInfo = str(ipaddr)+ ':' + str(port)
    print "Try to release port %s..." % (PortInfo)
    try:
        arglist = ["netstat.exe", '-ano']
        sp = subprocess.Popen(
                args = arglist,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
        netlist = sp.stdout.read()
        pid = None

        if PortInfo in netlist:

            pid = str(netlist).split()[str(netlist).split().index(PortInfo) + 2]
            if not str(pid).isdigit():
                print "Port %s is obtained but decode PID failure" % (PortInfo)
                return False
            print "Port %s is obtained by PID %s" % (PortInfo, pid)
            if int(pid) == 0:
                print "Process 0 is not valid! Skip it!"
                return True
            ret = os.system("ntsd -c q -p " + str(pid))
            if ret == 0:
                print "Kill PID %s and release %s successful!" % (pid, PortInfo)
                return True
            else:
                print "Kill PID %s and release %s failed!" % (pid, PortInfo)
                return False
        else:
            print "Port %s is free!" % (PortInfo)
            return True
    except:
        print "Unknown error occur when check port %s!" % (PortInfo)
        return False


class XCYCLERTelnet:
    def __init__(self, host, port, prompt, user, passwd, timeout):
        self.host = host
        self.port = port
        self.prompt = prompt
        self.user = user
        self.passwd = passwd
        try:
            self.timeout = float(timeout)
        except:
            print "*INFO* Timeout is not float type!"
            self.timeout = 3
        self.tn = None
        if self.Connect():
            print "*INFO* Telnet socket setup success!"
        else:
            print "*WARN* Telnet socket setup failure!"

        if self.tn:
            print "*INFO* CTelnet object initialize success!"
        else:
            print "*WARN* CTelnet object initialize failed!"

    def Connect(self):
        tn = None
        try:
            tn = telnetlib.Telnet(self.host, self.port)
        except Exception,e:
            print e
            print "*INFO* Open telnet connection error because of IP wrong or Port is accopied!"
            return False

        if not tn:
            print "*WARN* Open telnet connection failure!"
            return False

        try:
            tn.write("\r\n")
            # Input User Name
            p_UserPrompt = tn.read_until(CYCLERUSER, self.timeout)
            #print p_UserPrompt,
            if CYCLERUSER not in p_UserPrompt:
                print "\n*WARN*: User name prompt keyword '%s' is not in content!" % (CYCLERUSER)
                return False
            tn.write( self.user + "\r\n" )

            # Input Password
            p_PasswordPrompt = tn.read_until(CYCLERPASS, self.timeout)
            print p_PasswordPrompt
            if CYCLERPASS not in p_PasswordPrompt:
                print "*WARN* Password prompt keyword '%s' is not in content!" % (CYCLERPASS)
                return False
            tn.write( self.passwd + "\r\n" )

            # Check if logined
            p_LoginPrompt = tn.read_until(self.prompt, self.timeout)
            print p_LoginPrompt
            if self.prompt in p_LoginPrompt:
                self.tn = tn
                return True
            else:
                return False

        except Exception, e:
            print e
            print "*INFO* Telnet authentication failure!"
            return False

    def Disconnect(self):
        if self.tn:
            print self.prompt + " quit"
            self.tn.write('quit'+'\r\n')
            print self.tn.read_until('Bye!')
            print "*INFO* Socket is exit!"
            return self.tn.close()
        else:
            return True

    def __CheckConnectStatus(self):
        if not self.tn:
            print "*WARN* Connection is down!"
            return False
        else:
            print "*INFO* Connection is alive!"
            return True

    def __CheckResult(self, result, keyword = ""):
        if not result:
            print "*WARN* No output present!"
            return False
        else:
            try:
                result = str(result)
            except:
                print "*WARN* Output result is no string type!"
                return False
        if (keyword in result) and ("ERROR" not in result.upper()):
            print "*INFO* Output check ok!"
            return True
        else:
            print "*WARN* Output check failed!"
            return False

    def get_xcycler_powermeter(self):
        if not self.__CheckConnectStatus():
            print "*WARN* Non telnet connection!"
            return False

        print self.prompt,
        command = "show powermeters" + "\r\n"
        #print command
        outlet_keys = []
        powermeter = {}
        try:
            self.tn.write(command)
            p_Output = self.tn.read_until(self.prompt, self.timeout)
            print p_Output
            if self.__CheckResult(p_Output):
                for ln in p_Output.splitlines():
                    if 'n  |Rated(A)' in ln:
                        outlet_keys = [item.strip() for item in ln.split("|")]
                        continue
                    if ln.count(".") >= 5:
                        items = [item.strip() for item in ln.split()]
                        powermeter[items[0]] = dict(zip(outlet_keys, items))
            return powermeter
        except Exception, e:
            print "\n*WARN* Write command failure: ", e
            return False

    def get_xcycler_sensor_info(self):
        if not self.__CheckConnectStatus():
            print "*WARN* Non telnet connection!"
            return False

        print self.prompt,
        command = "show environment" + "\r\n"
        #print command
        sensor_info = {}
        try:
            self.tn.write(command)
            p_Output = self.tn.read_until(self.prompt, self.timeout)
            print p_Output
            if self.__CheckResult(p_Output):
                for ln in p_Output.splitlines():
                    if 'env_temperature' in ln:
                        sensor_info['env_temperature'] = ln.split(":")[-1].strip()
                        continue
                    if 'env_humidity' in ln:
                        sensor_info['env_humidity'] = ln.split(":")[-1].strip()
                        break
            return sensor_info
        except Exception, e:
            print "\n*WARN* Write command failure: ", e
            return False

    def SendCmd(self, command, RetKeyword = None):
        if not self.__CheckConnectStatus():
            print "*WARN* Non telnet connection!"
            return False

        if command == None or command == False:
            print "*WARN* No valid command to run."
            return True
        else:
            print self.prompt,
            command = str(command) + "\r\n"
        try:
            self.tn.write(command)
            p_Output = self.tn.read_until(self.prompt, self.timeout)
            print p_Output
            if RetKeyword:
                return self.__CheckResult(p_Output, RetKeyword)
            else:
                return self.__CheckResult(p_Output)
        except Exception, e:
            print "\n*WARN* Write command failure: ", e
            return False

def operate_xcycler(host, cmd, outlet):
    RETRYTIME  = 1
    try:
        PowerBreaker = XCYCLERTelnet(host, '23', "ycler>", "admin", "admin", '3')
        if not PowerBreaker.tn:
            for i in xrange(RETRYTIME):
                p_BackupStep = random.randint(1, 5)
                print "*WARN* The socket is conjested, waiting for another %s sec to retry for %s time!" % (p_BackupStep, i + 1)
                time.sleep(p_BackupStep)
                PowerBreaker.Connect()
                if PowerBreaker.tn:
                    break
                if i == RETRYTIME - 1:
                    print "*WARN* Max connect time reached!"
                    return 1
        if isinstance(outlet, list):
            if len(set(outlet)) == 8:
                command = "outlet all %s" % cmd
            else:
                command = ["outlet %s %s" %(o, cmd) for o in outlet]
        else:
            command = "outlet %s %s" % (outlet, cmd)

        if isinstance(command, list):
            for cmd in command:
                PowerBreaker.SendCmd(cmd)
        elif not PowerBreaker.SendCmd(command):
            print "*WARN* Send command failure! Retry process start..."
            for i in xrange(RETRYTIME):
                time.sleep(1)
                if PowerBreaker.SendCmd(command):
                    break
                if i == RETRYTIME - 1:
                    print "*WARN* Max operate time reached!"
                    return 2
        time.sleep(1)
        PowerBreaker.SendCmd("show outlet")
        return 0
    finally:
        PowerBreaker.Disconnect()

class CSocketClient:

    def __init__(self, ServerIp = '127.0.0.1', ServerPort = 15004, ClientIp = "127.0.0.1", ClientPort = 12005, ConnectType = 'TCP', TimeOut = 5.0):

        self.DebugLevel = DEBUG_LEVEL_NONE
        self.IfConneted = False
        self.TimeOut = TimeOut
        self.ServerIp = ServerIp
        self.ServerPort = ServerPort
        self.ClientIp = ClientIp
        self.ClientPort = ClientPort
        self.ConnectType = ConnectType
        self.Socket = None
        print "Current bind socket is:", ClientIp, ClientPort
        os.system("netstat -ano|grep 4001")

    def open(self):
        # close previous connection
        if self.IfConneted == True:
            self.close()
        try:
            # check port status
            if not CheckPort(self.ServerIp, self.ServerPort):
                print "Check port %s:%s failed!" % (self.ServerIp, self.ServerPort)

            if self.ConnectType == 'TCP':
                self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            elif self.ConnectType == 'UDP':
                self.Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                print "Socket type '%s' is invalid!" % self.ConnectType
                self.Socket = None
                self.IfConneted = False
                return False

            self.Socket.settimeout(self.TimeOut)
            self.Socket.bind((self.ClientIp, self.ClientPort))
            self.Socket.connect((self.ServerIp, self.ServerPort))
            self.IfConneted = True
            print "'%s' socket '%s:%s' is established!" % (self.ConnectType, self.ServerIp, self.ServerPort)
            return True

        except Exception, p_ErrInfo:
            print p_ErrInfo
            return False

    def close(self):
        if self.IfConneted == True:
            self.Socket.close()
            self.IfConneted = False
        print "'%s' socket '%s:%s' is closed!" % (self.ConnectType, self.ServerIp, self.ServerPort)
        return True

    def send(self, SendMsg = ''):
        p_marshalled = ""

        if self.IfConneted == False:
            self.__Log.error("'%s' socket '%s:%s' is closed, send failure!" %\
                             (self.ConnectType, self.ServerIp, self.ServerPort))
            return False

        for p in SendMsg:
            if isinstance(p, types.StringTypes) == False:
                p_marshalled += struct.pack("l", socket.htonl(p))
            else:
                p_marshalled += p

        try:
            self.Socket.send(p_marshalled)
            print "Send message over '%s' socket '%s:%s' is success!" %\
                  (self.ConnectType, self.ServerIp, self.ServerPort)
        except Exception, p_Err:
            print p_Err
            print "Send message over '%s' socket '%s:%s' is failed!" %\
                  (self.ConnectType, self.ServerIp, self.ServerPort)
        return True

    def receive(self, maxMsgSize=4096, recTimeout=10.0):

        marshalled = []
        msg = ""

        if self.TimeOut != recTimeout:
            self.TimeOut = recTimeout

        try:
            if self.TimeOut == 0xFFFFFFFF:
                # infinite timeout
                self.TimeOut = None
            elif self.TimeOut > 0x7FFFFFFF:
                # to avoid errors
                self.TimeOut = 0x7FFFFFFF

            self.Socket.settimeout(self.TimeOut)
            (msg, address) = self.Socket.recvfrom(maxMsgSize)

        except Exception, p_Error:
            print p_Error
            print "No response received during the timeout '%s'." % recTimeout
            msg = None

        return msg

class CTelnet:
    def __init__(self, host, port, prompt, user, passwd, timeout):
        self.host = host
        self.port = port
        self.prompt = prompt
        self.user = user
        self.passwd = passwd
        self.Reconnect = 0
        try:
            self.timeout = float(timeout)
        except:
            print "Timeout is not float type!"
            self.timeout = 10
        self.tn = None
        if self.Connect():
            print "Telnet socket setup success!"
        else:
            print "Telnet socket setup failure!"

        if self.tn:
            print "CTelnet object initialize success!"
        else:
            print "CTelnet object initialize failed!"

    def Connect(self):
        if self.Reconnect == 1:
            return self.tn

        tn = None
        os.system("TSKILL /A telnet")
        time.sleep(2)
        try:
            tn = telnetlib.Telnet(self.host, self.port)
        except Exception,e:
            print e
            print "Open telnet connection error because of IP wrong or Port is accopied!"
            return False

        if not tn:
            print "Open telnet connection failure!"
            return False

        try:
            # Input User Name
            p_UserPrompt = tn.read_until(USERPROMPT, self.timeout)
            print p_UserPrompt
            if USERPROMPT not in p_UserPrompt:
                print "ERR: User name prompt keyword '%s' is not in content!" % (USERPROMPT)
                return False
            tn.write( self.user + "\r\n" )

            # Input Password
            p_PasswordPrompt = tn.read_until(PASSWORDPROMPT, self.timeout)
            print p_PasswordPrompt
            if PASSWORDPROMPT not in p_PasswordPrompt:
                print "ERR: Password prompt keyword '%s' is not in content!" % (PASSWORDPROMPT)
                return False
            tn.write( self.passwd + "\r\n" )

            # Check if logined
            p_LoginPrompt = tn.read_until(self.prompt, self.timeout)
            print p_LoginPrompt
            if "1:" in p_LoginPrompt and "8:" in p_LoginPrompt :
                print "APC status is OK!"
                if self.prompt not in p_LoginPrompt:
                    print "ERR: Login prompt keyword '%s' is not in content!" % (self.prompt)
                    return False
                self.tn = tn
                return True
            else:
                print "APC status is NOK!"
                tn.write("exit" + "\r\n")
                tn.close()
                if self.connect_with_apc():
                    return self.Connect()
                else:
                    return False

            #print tn.get_socket()

        except Exception, e:
            print e
            print "Telnet authentication failure!"
            return False

    def connect_with_apc(self):
        self.Reconnect += 1
        tn = None
        os.system("TSKILL /A telnet")
        time.sleep(2)
        print "connect with password \"apc\", reslove APC abnormal problem."
        try:
            tn = telnetlib.Telnet(self.host, self.port)
        except Exception,e:
            print e
            print "Open telnet connection error ~~!"
            return False

        if not tn:
            print "Open telnet connection failure!"
            return False

        try:
            # Input User Name
            p_UserPrompt = tn.read_until(USERPROMPT, self.timeout)
            print p_UserPrompt
            if USERPROMPT not in p_UserPrompt:
                print "ERR: User name prompt keyword '%s' is not in content!" % (USERPROMPT)
                return False
            tn.write( self.user + "\r\n" )

            # Input Password
            p_PasswordPrompt = tn.read_until(PASSWORDPROMPT, self.timeout)
            print p_PasswordPrompt
            if PASSWORDPROMPT not in p_PasswordPrompt:
                print "ERR: Password prompt keyword '%s' is not in content!" % (PASSWORDPROMPT)
                return False
            tn.write( "apc" + "\r\n" )

            # Check if logined
            time.sleep(0.5)
            p_LoginPrompt = tn.read_very_eager()
            print p_LoginPrompt
            if "4- Logout" in p_LoginPrompt :
                tn.write( "4" + "\r\n" )
                tn.close()
                return True
            else:
                raise Exception, "Login with password failed!"

        except Exception, e:
            print e
            print "Telnet authentication with password 'apc' failure!"
            return False

    def Disconnect(self):
        if self.tn:
            return self.tn.close()
        else:
            return True

    def __CheckConnectStatus(self):
        if not self.tn:
            print "Connection is down!"
            return False
        else:
            print "Connection is alive!"
            return True

    def __CheckResult(self, result, keyword = "OK"):
        if not result:
            print "No output present!"
            return False
        else:
            try:
                result = str(result)
            except:
                print "Output result is no string type!"
                return False
        if (keyword in result) and ("OK" in result) and ("E100" not in result) and ("E101" not in result) and \
               ("E102" not in result) and ("E103" not in result) and ("E104" not in result) and ("E200" not in result):
            print "Output check ok!"
            return True
        else:
            print "Output check failed!"
            return False

    def SendCmd(self, command, RetKeyword = None):
        if not self.__CheckConnectStatus():
            print "Non telnet connection!"
            return False

        if command == None or command == False:
            print "No valid command to run."
            return True
        else:
            command = str(command) + "\r\n"
            print self.prompt + command

        try:
            self.tn.write(command)
            p_Output = self.tn.read_until(self.prompt, self.timeout)
            print p_Output
            if RetKeyword:
                return self.__CheckResult(p_Output, RetKeyword)
            else:
                return self.__CheckResult(p_Output)
        except:
            print "Write command failure"
            return False

def _operate_apc(host,port,prompt,user,passwd,timeout,cmd, outlet):
    RETRYTIME  = 5
    try:
        PowerBreaker = CTelnet(host, port, prompt, user, passwd, timeout)
        if not PowerBreaker.tn:
            p_BackupStep = random.randint(5, 30)
            print "The socket is conjested, waiting for another %s sec to retry for %s time!" % (p_BackupStep, i + 1)
            time.sleep(p_BackupStep)
            PowerBreaker.Connect()
            PowerBreaker.Reconnect = 0
            if i == RETRYTIME - 1:
                print "Max connect time reached!"
                return 1
        command = "%s %s" % (cmd, outlet)

        if not PowerBreaker.SendCmd(command):
            print "Send command failure! Retry process start..."
            for i in xrange(RETRYTIME):
                time.sleep(10)
                if PowerBreaker.SendCmd(command):
                    break
                if i == RETRYTIME - 1:
                    print "Max operate time reached!"
                    return 2
        for i in xrange(10):
            if PowerBreaker.SendCmd("status"):
                print "Outlet %s is %s now!" % (outlet, cmd)
                break
            if i == 9:
                print "waiting for outlet %s comming up timeout!" % outlet
                return 3
            time.sleep(3)
        return 0
    finally:
        PowerBreaker.Disconnect()


def power_dc_on(port='COM1'):
    try:
        ser=serial.Serial(port,baudrate=9600,bytesize=7,parity='E',xonxoff=1,stopbits=2,timeout=0)
    except:
        raise Exception,"Open Serial failed port='%s' " %port

    DC_ON_CMD= '%c'* len(DC_ON) % DC_ON
    try:
        ser.write(DC_ON_CMD)
        print "DC_ON"
    finally:
        ser.close()

def power_ac_on(port='COM1'):
    try:
        ser=serial.Serial(port,baudrate=9600,bytesize=7,parity='E',xonxoff=1,stopbits=2,timeout=0)
    except:
        raise Exception,"Open Serial failed port='%s' " %port

    AC_ON_CMD = '%c'* len(AC_ON) % AC_ON
    try:
        ser.write(AC_ON_CMD)
        print "AC ON"
    finally:
        ser.close()

def power_on(vendor_info="COM1"):
    Flag = False
    retry_time = 2
    tmp = vendor_info.split(":")
    __power_on(vendor_info)

def _get_unuse_bind_port():
    selected_port = random.randint(10240, 102400)
    arglist = ["netstat.exe", '-ano']
    sp = subprocess.Popen(
            args = arglist,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
    netlist = sp.stdout.read()
    if str(selected_port) not in netlist:
        Flag = True
        return selected_port
    else:
        return _get_unuse_bind_port()

def __power_on(vendor_info='COM1'):
    """
    Example
    | Power On ||
    | Power On | ${POWER_BREAK_IP}:${POWER_BREAK_OUTPUT}:${BTS_CONTROL_PC_LAB} |
    """

    tmp = vendor_info.split(':')
    vendor_info = vendor_info.upper()
    if vendor_info.startswith('XCYCLER'):
        PowerBreaker_Ip   = tmp[1]
        PowerBreaker_Port = tmp[2]
        operate_xcycler(PowerBreaker_Ip, "on", PowerBreaker_Port)
        return
    # Facom
    if 3 == len(tmp) and tmp[0].upper() != "XCYCLER":
        PowerBreaker_Ip   = tmp[0]
        PowerBreaker_Port = tmp[1]
        BtsControlPC_ip   = tmp[2]

        if int(PowerBreaker_Port)<1 or int(PowerBreaker_Port)>6:
            raise Exception, "PowerBreaker_Port %s out of range!" % PowerBreaker_Port

        p_Socket = None

        # Open socket
        p_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (PowerBreaker_Ip, 4001)
        p_Socket.connect(server_address)

        # Power on port for 5 retry times
        # power on
        if p_Socket.send(binascii.a2b_hex(POWER_ON_PORT[int(PowerBreaker_Port)-1])):
            print "Send message POWER_ON_PORT_%s %s over socke success!" \
                  % (PowerBreaker_Port, POWER_ON_PORT[int(PowerBreaker_Port)-1])
        else:
            raise Exception, "Send message POWER_ON_PORT_%s %s over socke failed!" \
                  % (PowerBreaker_Port, POWER_ON_PORT[int(PowerBreaker_Port)-1])

        p_Socket.close()

    #APC
    elif 2 == len(tmp):
        print tmp
        PowerBreaker_Ip   = tmp[0]
        PowerBreaker_Port = tmp[1]
        if int(PowerBreaker_Port) > 8 or int(PowerBreaker_Port) <1:
            raise "Your powerbreaker port is out of range, should be from 1 to 8"
        _operate_apc(PowerBreaker_Ip, "23", "APC>", "apc", "apc-c", "10", "on", PowerBreaker_Port)

    # NSN
    else:
        port = vendor_info

        try:
            ser=serial.Serial(port,baudrate=9600,bytesize=7,parity='E',xonxoff=1,stopbits=2,timeout=0)
        except:
            raise Exception,"Open Serial failed port='%s' " %port

        POWER_ON_CMD = '%c'* len(POWER_ON) % POWER_ON
        try:
            ser.write(POWER_ON_CMD)
            print "Power ON"
        finally:
            ser.close()

def power_off(vendor_info="COM1"):
    Flag = False
    tmp = vendor_info.split(':')
    retry_time = 2

    __power_off(vendor_info)

def __power_off(vendor_info='COM1'):
    """
    Example
    | Power Off ||
    | Power Off | ${POWER_BREAK_IP}:${POWER_BREAK_OUTPUT}:${BTS_CONTROL_PC_LAB} |
    """


    tmp = vendor_info.split(':')


    vendor_info = vendor_info.upper()
    if vendor_info.startswith('XCYCLER'):
        PowerBreaker_Ip   = tmp[1]
        PowerBreaker_Port = tmp[2]
        operate_xcycler(PowerBreaker_Ip, "off", PowerBreaker_Port)
        return
    # Facom
    if 3 == len(tmp) and tmp[0].upper() != "XCYCLER":
        PowerBreaker_Ip   = tmp[0]
        PowerBreaker_Port = tmp[1]
        BtsControlPC_ip   = tmp[2]

        if int(PowerBreaker_Port)<1 or int(PowerBreaker_Port)>6:
            raise Exception, "PowerBreaker_Port %s out of range!" % PowerBreaker_Port

        p_Socket = None

        # Open socket
        try:
            p_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (PowerBreaker_Ip, 4001)
            p_Socket.connect(server_address)
            if p_Socket.send(binascii.a2b_hex(POWER_OFF_PORT[int(PowerBreaker_Port)-1])):
                print "Send message POWER_OFF_PORT_%s %s over socke success!" \
                      % (PowerBreaker_Port, POWER_OFF_PORT[int(PowerBreaker_Port)-1])
            else:
                raise Exception, "Send message POWER_OFF_PORT_%s %s over socke failed!" \
                      % (PowerBreaker_Port, POWER_OFF_PORT[int(PowerBreaker_Port)-1])
        finally:
            if p_Socket:
                p_Socket.close()
    #APC
    elif 2 == len(tmp):
        PowerBreaker_Ip   = tmp[0]
        PowerBreaker_Port = tmp[1]
        if int(PowerBreaker_Port) > 8 or int(PowerBreaker_Port) <1:
            raise "Your powerbreaker port is out of range, should be from 1 to 8"
        _operate_apc(PowerBreaker_Ip, "23", "APC>", "apc", "apc-c", "10", "off", PowerBreaker_Port)

    # NSN
    else:
        port = vendor_info

        try:
            ser=serial.Serial(port,baudrate=9600,bytesize=7,parity='E',xonxoff=1,stopbits=2,timeout=0)
        except:
            raise Exception,"Open Serial failed port='%s' " %port

        POWER_OFF_CMD = '%c'* len(POWER_OFF) % POWER_OFF
        try:
            ser.write(POWER_OFF_CMD)
            print "Power off"
        finally:
            ser.close()

def option_parse():
    parser = OptionParser()
    parser.set_usage("\n\tExample: powerbreaker.exe -o AC_ON -p COM1")
    parser.add_option("-o","--operation",
                      action="store",
                      type="string",
                      dest="operation",
                      help="Operation of powerbreaker.\
                      \n  Support DC_ON, AC_ON, POWER_OFF, POWER_ON.\
                      \n Can support HuaXiang and FaChen powerbreaker.\
                      \n  HuaXiang support DC_ON, AC_ON, POWER_OFF, POWER_ON.\
                      \n  FaChen support POWER_OFF and POWER_ON. ")
    parser.add_option("-p","--port",
                      action="store",
                      type="string",
                      dest="port",
                      help="The COM port or address of you powerbreak.\
                      If HuaXiang can type: COM1 \t\t\t\t\
                      If FaChen can type: 192.168.127.254:6:192.168.127.253")
    (options, args) = parser.parse_args()
    addr = options.port.upper()

    if options.operation == None :
        sys.exit("\n  Pls type -o option. Type powerbreaker.exe --help for help.")
    elif options.operation.upper() == "DC_ON" :
        if addr.count('COM') != 1:
            print "\n\tThere is some error with you input.\n"
            print "\tType powerbreaker.exe --help for help.\n"
            sys.exit("\tDC_ON not support FaChen!")
        power_dc_on(addr)
    elif options.operation.upper() == "AC_ON":
        if addr.count('COM') != 1:
            print "\n\tThere is some error with you input.\n"
            print "\tType powerbreaker.exe --help for help.\n"
            sys.exit("\tAC_ON not support FaChen!")
        power_ac_on(addr)
    elif options.operation.upper() == "POWER_OFF":
        power_off(addr)
    elif options.operation.upper() == "POWER_ON":
        power_on(addr)
    else:
        sys.exit("\n The operation you input is not support now: %s" %(options.operation))

if __name__ == "__main__":
##    power_off('192.168.127.254:3:192.168.127.200')
##    time.sleep(5)
##    power_on('192.168.127.254:3:192.168.127.200')
    option_parse()



