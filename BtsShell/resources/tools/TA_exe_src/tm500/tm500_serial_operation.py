import re
import os
import time
import serial
from optparse import OptionParser
from serial_common import SerialCommon
FAIL_INFO = "tm500 reboot failed"

def serial_operation(tm500_sw_version, operate='reboot', timeout="240"):
    
    timeout_sec = int(timeout)
    tm500_sw_ver_tuple = __formalize_sw_version(tm500_sw_version)
    tm500_serial_ins = __init_serial_inst(tm500_sw_ver_tuple)
    
    all_start = time.clock()
    if not tm500_serial_ins:
        print('Failed to connect to TM500 by serial port!')
        print(FAIL_INFO)
        return
    print "open serial ok"
    #tm500_serial_ins.open_connection()
    try:
        #if operate == 'reboot':
        #    tm500_serial_ins.write("reboot\n")
        #    print("Send -> TM500 serial 'reboot' command.")
        if not __wait_until_soft_reboot_ready(tm500_serial_ins, timeout_sec, 
                                            tm500_sw_ver_tuple):
            print("TM500 failed to be ready after serial check in '%s's!" % timeout)
            print(FAIL_INFO)
        else:
            print('TM500 serial check ready sucessfully.')
            
    except Exception, error:
        print error
        raise Exception(FAIL_INFO)
    finally:
        print "check over start to close serial"
        tm500_serial_ins.close()
        print "use time: %s" % (time.clock()-all_start)
    
    
def __formalize_sw_version(tm500_sw_version):
    pattern = r'([KSL])(\d{1,2})\.(\d{1,2})\.(\d{1,2}).*?REV(\d{2})'
    match = re.search(pattern, tm500_sw_version, re.I)
    if not match:
        raise Exception('Input string "%s" does NOT contain ' 
                        % tm500_sw_version + 
                        'valid TM500 software version info! ' + 
                        'Valid info should be like [K/S/L].1.2.3.REV00')
    else:
        return match.groups()

def __wait_until_soft_reboot_ready(tm500_serial_ins, 
                             timeout, tm500_sw_ver_tuple):
    """
    @param tm500_serial_ins: SerialCommon instance which is connected to TM500.
    @param timeout: timeout for waiting, float, seconds.
    @param tm500_sw_ver_tuple: format like ('K', '4', '6', '3', '01')
    @return: True/False
    """
    # change format to K_04_06_02_REV11
    sw_ver_items = [tm500_sw_ver_tuple[0].upper()]
    sw_ver_items.extend(['%02d' %int(item) for item in tm500_sw_ver_tuple[1:4]])
    sw_ver_items.append('REV%02d' %int(tm500_sw_ver_tuple[4]))
    tm500_sw_version = '_'.join(sw_ver_items)
    

    start_time = time.clock()
    data_ret_by_tm500 = ''
    ret_val = False
    while True:
        data_ret = tm500_serial_ins.read(512)
        print('Data received from TM500\'s serial port:\n%s' % data_ret)
        data_ret_by_tm500 += data_ret
        if 'Router Initialised' in data_ret_by_tm500:
            if tm500_sw_version in data_ret_by_tm500:
                print('TM500 reboot done, is ready for use.')
                ret_val = True
            else:
                # receive serial data once again, then judge
                time.sleep(3)
                data_ret = tm500_serial_ins.read(512)
                print('Data received from TM500\'s serial port:\n%s' 
                         %data_ret)
                data_ret_by_tm500 += data_ret
                if tm500_sw_version in data_ret_by_tm500:
                    print('TM500 reboot done, is ready for use.')
                    ret_val = True
                else:
                    print('TM500 reports "Router Initialised", ' +
                             'but expected software version is NOT met! ' +
                             'SW version expected: "%s"' %tm500_sw_version)
                    ret_val = False
            break
        elif time.clock() - start_time > timeout:
            print("TM500 reboot is NOT done within %d seconds!" %timeout)
            ret_val = False
            break
        else:
            time.sleep(3)
    
    return ret_val
    
def __init_serial_inst(tm500_sw_ver_tuple):
    """
    @param tm500_sw_ver_tuple: format like ('K', '4', '6', '3', '01')
    """
    #os.system("TASKKILL /F /T /IM hypertrm.exe")
    tm500_pc_serial_port_info = SerialCommon.get_os_serial_port_info()
    tm500_baudrate = __get_corrent_tm500_serial_baudrate(tm500_sw_ver_tuple)
    print tm500_pc_serial_port_info, tm500_baudrate
    #return

    for serial_port_name in tm500_pc_serial_port_info:
        
        serial_ins = serial.Serial(port=serial_port_name, 
                                  baudrate=tm500_baudrate,
                                  bytesize=8,
                                  parity='N',
                                  stopbits=1,
                                  timeout=10
                                  )
        try:
            print("Try to open '%s'" % serial_port_name)
            
            #serial_ins.open_connection()
            '''
            ret = serial_ins.write('COMMAND_NOT_EXIST\n')
            print "Send -> 'COMMAND_NOT_EXIST' return '%s'" % ret
            if not ret:
                serial_ins.close()
                continue
            cmd_ret = serial_ins.read(25).lower()
            print "Receive <- '%s'" % cmd_ret
            
            # judge if this serial port connects to TM500, by cmd return value
            EXPECT_STRING = 'unknown symbol name'
            if EXPECT_STRING not in cmd_ret:
                print "The device is not tm500 for in receive the '%s' is not exist" % EXPECT_STRING
                serial_ins.close()
                continue
            '''
        except Exception, err_info:
            print(err_info)
            serial_ins.close()
            continue
        else:
            # found the right serial port, please be noted that
            # this port will be closed in "finally" clause
            return serial_ins
        finally:
            # close_connection for every tried serial_ins
            #serial_ins.close_connection() # not close
            pass
    print('No serial port connects to TM500!')
    return 

def __get_corrent_tm500_serial_baudrate(tm500_sw_ver_tuple):
    """
    @param tm500_sw_ver_tuple: format like ('K', '4', '6', '3', '01')
    """
    baudrate = 0
    if tm500_sw_ver_tuple[0].upper() == 'K':
        if int(tm500_sw_ver_tuple[1]) >= 7:
            baudrate = 115200
        else:
            baudrate = 9600
    elif tm500_sw_ver_tuple[0].upper() == 'S':
        if int(tm500_sw_ver_tuple[1]) >= 5:
            baudrate = 115200
        else:
            baudrate = 9600
    elif tm500_sw_ver_tuple[0].upper() == 'L':
        if int(tm500_sw_ver_tuple[1]) >= 3:
            baudrate = 115200
        else:
            baudrate = 9600
    else:
        pass  # no chance to be here
    print("Auto parse baudrate is '%s' by version '%s'" % (baudrate, '_'.join(tm500_sw_ver_tuple)))
    return baudrate  

def parse_parameters():

    runtype = ''
    parser = OptionParser()
    parser.add_option("-p", "--operate", action="store", type="string", dest="operate")
    parser.add_option("-v", "--version", action="store", type="string", dest="version")
    parser.add_option("-t", "--timeout", action="store", type="string", dest="timeout")

    (options, args) = parser.parse_args()

    if options.operate:
        OPERATE = options.operate
    else:
        OPERATE = ''

    if options.timeout:
        TIMEOUT = options.timeout
    else:
        TIMEOUT = '240'

    VERSION = options.version


    return OPERATE, VERSION, TIMEOUT
        

if __name__ == "__main__":
    #"S5.0.0 REV51"
    OPERATE, VERSION, TIMEOUT = parse_parameters()
    if OPERATE == '':
        serial_operation(VERSION)
    else:
        serial_operation(VERSION, 'check')

    
