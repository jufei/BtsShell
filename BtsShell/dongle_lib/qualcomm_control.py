import serial, re, os, time
from optparse import OptionParser

IP_PATTERN = "([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5]).*"

class QualcommDongle_Control():

    def __init__(self,port):
        self.port = port
        print "Qualcomm Dongle started:", self.port
        
    def serial_open(self):
        try:
            ser_obj = serial.Serial(port=self.port,baudrate=115200,bytesize=serial.EIGHTBITS,\
                                    parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,\
                                    timeout=None,xonxoff=0,rtscts=0,interCharTimeout=None)
            self.ser_obj = ser_obj
            print "*INFO* Have connected to serial port %s." %(self.port)
            #print ser_obj
        except Exception , e:
            print "*ERROR* Serial open failed with port %s." %(self.port)
            print e
        
    def serial_close(self):
        try:
            self.ser_obj.close()
        except Exception , e:
            print "*ERROR* Serial close failed."
            print e
            
    def serial_write(self,cmd):
        try:
            self.serial_open()
            print "*INFO* Will write command: %s" %(cmd)
            self.ser_obj.write(cmd)
            rsp = self.ser_obj.write('\r')
            ret = self.ser_obj.read(512)
            print "*INFO* Response: %s" %ret
            return ret.replace('\r\n','')
        except Exception , e:
            print "*ERROR* Serial write failed."
            print e
        finally:
            self.serial_close()

    def UE_Attach(self,freq=38000):
        flag = False
        try:
            ret = self.serial_write("AT%%EARFCN=%s" %(freq))
            if 'OK' in ret:
                print "*INFO* set EARFCN successed."
            else:
                print "*ERROR* set EARFCN failed."
            ret = self.serial_write("AT+CFUN=1,0")
            if 'OK' in ret:
                print "*INFO* set capacity successed."
            else:
                print "*ERROR* set capacity failed."
            ret = self.serial_write("AT+CGATT=1")
            if 'OK' in ret:
                flag = True
                print "*INFO* Dongle attach successed."
            else:
                flag = False 
                print "*ERROR* Dongle attach failed."
        except Exception ,e :
            print e
        finally:
            if flag:
                #PASS
                print "Return value is: 0"
            else:
                print "Return value is: 1"
            return flag

    def UE_Detach(self):
        flag = False
        try:
            ret = self.serial_write("AT+CGATT=0")
            if 'OK' in ret:
                flag = True
                print "*INFO* Dongle detach successed."
            else:
                flag = False 
                print "*ERROR* Dongle detach failed."
        finally:
            if flag:
                #PASS
                print "Return value is: 0"
            else:
                print "Return value is: 1"
            return flag

    def UE_reset(self):
        flag = False
        try:
            ret = self.serial_write("AT+CFUN=0")
            if 'OK' in ret:
                pass
            else:
                print "*WARN* AT+CFUN=0 execute failed."
            ret = self.serial_write("AT+CFUN=1,1")
            if 'OK' in ret:
                flag = True
                print "*INFO* Dongle reset successed."
            else:
                flag = False 
                print "*ERROR* Dongle reset failed."
        except Exception ,e :
            print e
        finally:
            if flag:
                #PASS
                print "Return value is: 0"
            else:
                print "Return value is: 1"
            return flag

    def Get_ip_addr(self):
        ip_addr = ""
        try:
            ret = self.serial_write("AT+CGCONTRDP=1")
            result = re.search(IP_PATTERN, ret)
            #print '***', ret,"***"
            if result:
                ip_addr = result.group(0)
                print "*INFO* Get IP successed:%s." %(ip_addr)
            else:
                print "*ERROR* Get IP failed."
        finally:
            ip_addr = '.'.join(ip_addr.split('.')[:4])
            print "Aquired IP is: %s" %ip_addr
            return ip_addr

    def Get_attached_cellid(self):
        cell_id = ""
        try:
            ret = self.serial_write("AT%PCONI")
            result = re.search('Global Cell ID: (.*)Physical',ret, re.M)
            #print '***', ret,"***"
            if result:
                global_cellid = int(result.group(1),16)
                btsid = global_cellid/256
                cellid = global_cellid%256
                cell_id = "%d/%d" %(btsid, cellid)
                print "*INFO* Get cellid successed:%s." %(cell_id)
            else:
                print "*ERROR* Get cellid failed."
        finally:
            print "Aquired cellid is: %s." %cell_id
            return cell_id
        
    def check_dongle_attach_status(self):
        #+CGATT: 1
        flag = False
        cell_id = ""
        try:
            ret = self.serial_write("AT+CGATT?")
            if ": 1" in ret:
                flag = True
            else:
                flag = False
        finally:
            if flag:
                #PASS
                print "Return value is: 0"
            else:
                print "Return value is: 1"
            return cell_id
        
def main():
    """This keyword used for parsing arguments input.
    Example
    | python qualcomm_control.py --port COM4 -o attach --freq 38000 |
    """
    parser = OptionParser()
    parser.set_usage("\n\tExample: \n\t\tpython -o attach -p COM4 -f 38000 altair_control.py")	
    parser.add_option("-o", "--operation", action="store", type="string", \
                      dest="operation",help="--Available operation of this dongle: \t\t1.attach\t2.detach\t3.getip\t4.command\t5.getstatus\6.reset")
    parser.add_option("--port","-p", action="store", type="string", dest="port",\
                      help="--The COM port of your Dongle.")
    parser.add_option("--atcmd","-c", action="store", type="string", dest="atcmd",\
                      help="--The atcmd you want send.")
    parser.add_option("--freq", "-f",action="store", type="string", dest="frequency",\
                      help="--The frequency of your eNB.Pls input this value according your eNB's earfcn value.")
    (options, args) = parser.parse_args()

    if options.port:
        Qualcomm_control = QualcommDongle_Control(options.port)
    else:
        raise Exception, "Please input correct com port"

    if options.operation == "attach":
        Qualcomm_control.UE_Attach(options.frequency)
    elif options.operation == 'detach':
        Qualcomm_control.UE_Detach()
    elif options.operation == 'getip':
        Qualcomm_control.Get_ip_addr()
    elif options.operation == 'getcell':
        Qualcomm_control.Get_attached_cellid()
    elif options.operation == 'getstatus':
        Qualcomm_control.check_dongle_attach_status()
    elif options.operation == 'command':
        Qualcomm_control.serial_write(options.atcmd)
    elif options.operation == 'reset':
        Qualcomm_control.UE_reset()
    else:
        raise Exception, "The operation \"%s\" do not support now" % (options.operation)
#main()

        
if __name__ == "__main__":
    
    

    obj = QualcommDongle_Control("COM5")
    print "detach:",obj.UE_Detach()   
    print "attach:",obj.UE_Attach("37900")
    import time
    time.sleep(5)
    print "<0>get_ip:"
    ip = obj.Get_ip_addr()
    print "**", ip
    cellid = obj.Get_attached_cellid()
    print "**--", cellid
                                                                      
##    print "<1>Get signal strength Test:",obj.serial_write("AT%CSQ")
##    print "<2>Get available PLMN list Test:",obj.serial_write("AT+COPS=?")
##    print "<3>Check PLMN Connection Status Test:",obj.serial_write("AT+CGATT?")
##    print "<4>Get EARFCN (E-UTRA Absolute Radio Frequency Channel Number) Test:"\
##          ,obj.serial_write("AT%EARFCN?")
##    print "<5>Get CREG parameters Test:",obj.serial_write("AT+CREG?")
##    print "<6>Read APN (Access Point Name) Test:",obj.serial_write("AT+CGDCONT?")
##    print "<7>Get USIM status Test:",obj.serial_write('AT%STATUS="USIM"')
##    print "<8>Get USIM status Test:",obj.serial_write('AT%GETCFG="USIM_SIMULATOR"')    
##    print "<9>Get USIM status Test:",obj.serial_write('AT%GETCFG="BAND"')
##    print "<10>Get USIM status Test:",obj.serial_write('AT%PCONI')
##
##    print "Following is AT command for testing UE initiated dedicated bearer :"
##    
##    
##    print "detach:",obj.UE_Detach()


    
