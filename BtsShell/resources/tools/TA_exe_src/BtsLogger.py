import socket
import os, sys, time
from datetime import datetime


def GetTimeStamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

class Redstdout:
    def __init__(self, logfile):
        self.f = logfile
        try:
            self.file_handle = open(self.f, 'w')
        except Exception, e:
            print e
            print "Log file create failed!"
    def write(self, s):
        self.file_handle.write(s)
    def __del__(self):
        self.file_handle.close()
        
class BtsLogger:
    def __init__(self, logpath='.'):
        self.btsState = "OffAir"
        self.loggerState = "notStarted"
        self.logpath = logpath
        self.udplogfile = "SYSLOG_%s.LOG" %( GetTimeStamp() )
    
        self.udplogfile = os.path.join(os.path.abspath(self.logpath), self.udplogfile)
    
    def CatchUDPLog(self):
        sys.__stderr__.write("\n BtsLog scanning started")
        UDP_IP="0.0.0.0"
        UDP_PORT1=51000
        clearudpport(UDP_PORT1)
        
        sock1 = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
        sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except AttributeError:
            pass # Some systems don't support SO_REUSEPORT
        sock1.bind( ('',UDP_PORT1) )
    
        sys.__stderr__.write("\n Will catch log to log file '%s'" %self.udplogfile)
        
        sys.__stderr__.write("\n Listening for messages on UDP port %d" % UDP_PORT1)
    
        oldstdout = sys.stdout
        sys.stdout = Redstdout(self.udplogfile)
        try:
            while True:
              data1, addr = sock1.recvfrom( 250000 )
              print data1
        except KeyboardInterrupt:
            sys.stdout = oldstdout
            sys.__stderr__.write("\n Catch log to file '%s' stoped." %self.udplogfile)

def main(logpath):
    b = BtsLogger(logpath)
    b.CatchUDPLog()

def clearudpport(port):
    try:
        lines = os.popen("netstat -ano|grep %s" % port).readlines()
        for ln in lines:
            if 'UDP' in ln:
                s = ln
                break
        cmd = "taskkill /f /t /pid %s" %(s.split()[-1])
        print cmd
        os.system(cmd)
    except:
        pass

def printUsage():
    print """
----------------------------------------------------------------------
This tool is used for collect UDP log to specfied path.
    usage:
        python %s LOGPATH
----------------------------------------------------------------------
""" % os.path.basename(sys.argv[0])
    

if __name__ == "__main__":
    args = sys.argv
    for arg in args:
        if 'HELP' in arg.upper() or "?" in arg.upper():
            printUsage()
            sys.exit(1)
    if len(args) == 1:
        logpath = os.path.curdir
    elif len(args) == 2:
        logpath = args[-1]
    else:
        printUsage()
        sys.exit(1)
    main(logpath)

