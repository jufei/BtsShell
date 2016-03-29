import re
import os
import time
import serial
from threading import *

 
class MyThread(Thread):
    def __init__(self, ser_port, baudrate, file_path):
        Thread.__init__(self)
        self.port = ser_port
        self.baudrate = baudrate
        self.file_path = file_path
        
    def run (self):

        self.buffer = ""
        self.ifdo = True;
        self.serial_ins = None
        port = self.port
        baudrate = self.baudrate
        
        self.serial_ins = serial.Serial(port=port,
                                   baudrate=baudrate,
                                   bytesize=8,
                                   parity='N',
                                   stopbits=1,
                                   timeout=10 )  
        while self.ifdo:
            #print 'I am reading...'
            cmd_ret = self.serial_ins.read(1024).lower()
            self.buffer += cmd_ret            
            time.sleep(2)
 
    def stop (self):
        file_path = self.file_path
        print 'I am stopping it...'
        self.ifdo = False;
        file(file_path, 'w').write(self.buffer )
        if self.serial_ins:
            self.serial_ins.close()
            
def start_read_serial(ser_port, baudrate, file_path):
    """This keyword start to capture serial content at background.
    | Input Parameters | Man. | Description                |
    | ser_port         | Yes  | '1' or 'COM1'              |
    | baudrate         | Yes  | 115200 or 9600             |
    | file_path        | Yes  | abs path for save log path |
    Example
    | start_read_serial | COM1 | 9600 | d:\\123.txt | 
    """

    global tr
    tr = MyThread(ser_port, baudrate,  file_path)
    tr.setDaemon(True)
    tr.start()

def stop_read_serial():
    """This keyword stop to capture serial and save content.

    Example
    | stop_read_serial | 
    """    
    global tr
    tr.stop()
    tr.join()
    
if __name__ == '__main__':     
    start = time.clock()
    start_read_serial('COM6', '115200', "d:\\123.txt")
    time.sleep(20)
    stop_read_serial()
    print time.clock() - start