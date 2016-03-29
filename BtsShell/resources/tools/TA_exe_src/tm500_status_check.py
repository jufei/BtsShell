import time
import serial
import re
ser = None
try:
    ser = serial.Serial(port='COM1',\
                      baudrate=9600,\
                      bytesize=8,\
                      parity='N',\
                      stopbits=1,\
                      timeout=10)
    print "check:serial open ok"
    start_time = time.clock()
    output = ""

    print "check:send check ok"
    time.sleep(10)
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
            break

    print "check:reboot done"
finally:
    if None == ser:
        pass
    else:
        ser.close()




