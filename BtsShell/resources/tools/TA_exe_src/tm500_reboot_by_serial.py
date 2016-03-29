import time
import serial
import sys
import re
ser = serial.Serial(port='COM1',\
                  baudrate=9600,\
                  bytesize=8,\
                  parity='N',\
                  stopbits=1,\
                  timeout=10)
print "serial open ok"
try:
    ser.write("reboot")
    ser.write("\n")
    print "send reboot ok"
    
    time.sleep(10)
    start_time = time.clock()
    
    output = ""
    for i in xrange(90):
        try:
            a = ser.read(512)
            print str(a)
            output += str(a)
        except:
            pass

        if re.search("ROUTER\s*INITIALISED", output.upper()):
            break
        time.sleep(3)
        print "-------" +  str(i) +  "--------"
        duration = time.clock() - start_time
        if 260 < duration :
            print "tm500 reboot failed in 5 minutes!!!"
            sys.exit(-100)

    print "check:reboot done"
    sys.exit(0)
finally:
    ser.close()