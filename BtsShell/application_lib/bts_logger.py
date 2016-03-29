import thread
import socket
import sys, time
import re

class BtsLogger:
  
  def __init__(self, check):
    self.btsState = "zero"
    self.checkpoint = check
    self.loggerState = "notStarted"
    
  def BtsLogProcess(self):

    sys.__stdout__.write("\n BtsLog scanning started")
    UDP_IP="0.0.0.0"
    UDP_PORT1=51000
   
    sock1 = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
    sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print "\n==================="
    
    try:
      sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except AttributeError:
      pass # Some systems don't support SO_REUSEPORT
    sock1.bind( ('',UDP_PORT1) )
  
    sys.__stdout__.write("\n Listening for messages on UDP port %d" % UDP_PORT1)
    while True:
      data1, addr = sock1.recvfrom( 250000 )
      m = re.search(self.checkpoint , data1, re.I)
      if m:
        self.btsState = self.checkpoint
        sys.__stdout__.write("\ncheck information successfully now!")

  def start_log(self):
    if (self.loggerState == "notStarted"):
      thread.start_new_thread(self.BtsLogProcess, ())
      self.loggerState = "Started"
    else:
      pass
    
  def reset_bts_state(self):
    self.btsState = "zero"
  
  def get_bts_state(self):
    return self.btsState
    
  def wait_bts_onair(self, timeoutInSeconds):
    li = []
    timeoutCounter = 0;
    sys.__stdout__.write("\nWaiting for checking bts information...")
    while (self.btsState != self.checkpoint) and (timeoutCounter < int(timeoutInSeconds)):
      time.sleep(1)
      timeoutCounter = timeoutCounter + 1
    if self.btsState != self.checkpoint:
      sys.__stdout__.write("\n*ERROR* checking bts information timeout!")
      li.append("FAIL: checking bts information timeout!")
    else:
      li.append("PASS")

    li.append(timeoutCounter)
    return li

def bts_logger_check(information, timeout):
  
  try:
    SL = BtsLogger(information)
  except:
    raise "try to build BTS Logger object failed!"

  else:
    SL.start_log()
    ret = SL.wait_bts_onair(timeout)
    return ret

  
if __name__ == '__main__':

 # result = bts_logger_check("GPS_Agent forward evGpsSignalLevelResp", 300)
 # print result

  pass

  


      

  

  
  

