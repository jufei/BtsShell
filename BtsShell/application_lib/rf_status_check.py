import time
import serial
import re
from BtsShell.file_lib.common_operation import *
ser = None

def rf_status_check(com_port, log_file):
    """This keyword unzip /ram/startup.zip, and copy startup.log to local

    | Input Parameters | Man.| Description |
    | com_port         | Yes | com port    |
    | log_file         | Yes | copy startup.log to local, local file's name |
    """
    try:
        ser = serial.Serial(port = com_port,\
                  baudrate = 115200,\
                  bytesize = 8,\
                  parity = 'N',\
                  stopbits = 1,\
                  timeout = 10)

        print "check:serial open ok"
        start_time = time.clock()
        output = ""

        print "check:send check ok"
        time.sleep(10)

        ser.write("unzip startup.zip")
        ser.write("\n")
        print "unzip startup.zip ok!"
        time.sleep(5)
        ser.write("cat startup.log")
        ser.write("\n")
        time.sleep(10)

        try:
            a = ser.read(1048576*2)
            #print str(a)
            output += str(a)

        except:
            pass

        print "RF check done!"
        file_write(log_file, output, "w")
    finally:
        if None == ser:
            pass
        else:
            ser.close()

if __name__ == '__main__':
    rf_status_check("COM1", "D:\\abcd.txt")
    pass






