"""This file is used to control CPE by send AT command
These keywords can be use in Robot framework.
"""
import re
import time
import socket
import os

class DMCPE_Control:
    def __init__(self, args):
        key_list = args.keys()
        if 'IP' not in key_list:
            raise Exception, "Please input CPE ip address first"
        self.ip = args['IP']
        self.freq = None
        if args.has_key("FREQUENCY"):
            self.freq = args["FREQUENCY"]
        self.retry_time = 3
        self.timeout = 30
        self.pausetime = 1
        self.RebootRetry = 2
        self.Reboot = False
        print "DeMing CPE started:", self.ip

        self.connect_to_cpe()

    def __del__(self):
        if self.Reboot:
            return
        if self.con:
            try:
                #self.__send_cmd("ATBEGIN=2")
                self.con.close()
            except:
                print "*WARN* close connection and lte interface failed!"
        
    def connect_to_cpe(self):
        try:
            self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.con.settimeout(self.timeout)
            self.con.connect((self.ip, 9001))
            print "socket connect succeed!"
        except Exception, e:
            print "Error: ", e
            raise Exception, "Connect to cpe %s failed ! " %(self.ip)
        finally:
            pass

    def __send_cmd(self, cmd):
        s = ''
        self.retry_time = 3
        while self.retry_time:
            if not self.con:
                raise Exception, "socket is not exists!"         
            self.con.sendall(cmd)
            print "command(%ss): %s" % ((4-self.retry_time), cmd)
            time.sleep(self.pausetime)
            try:
                s = self.con.recv(1024)
            except Exception, e:
                print "*WARN* ", e
                self.retry_time -= 1
                continue #make sure if s is None continue next loop.
            print "response(%ss): %s" %((4-self.retry_time), s)
            if "ERROR" in s:
                self.retry_time -= 1
                continue
            else:
                return s
        return s
    
    def execute_at_command(self, at_cmd):
        try:
            ret = self.__send_cmd("ATBEGIN=1")
            if 'OK' in ret:
                pass
            else:
                raise Exception, "Enter lte interface failed!"
            return self.__send_cmd(at_cmd)
        except Exception, e:
            print "*WARN* Exec AT cmd \"%s\" failed with error: %s" % (at_cmd, e)
        finally:
            pass
        
    def __execute_at_command(self, at_cmd):
        #time.sleep(self.pausetime)
        try:
            ret = self.__send_cmd("ATBEGIN=1")
            if 'OK' in ret:
                pass
            else:
                raise Exception, "Enter lte interface failed!"
            
            ret = self.__send_cmd(at_cmd)
            if "OK" in ret:
                return 0
            else:
                return 1
        except Exception, e:
            print "*WARN* Exec AT cmd \"%s\" failed with error: %s" % (at_cmd, e)
        finally:
            pass

    def dongle_reboot(self, at_cmd="ATREBOOT"): 
        self.Reboot = True
        if self.RebootRetry == 0:
            return 1
        Flag = False
        self.con.settimeout(2)     
        self.con.sendall(at_cmd)
        self.con.sendall(os.linesep)
        print "command(1s): %s" % (at_cmd)
        time.sleep(5)
        curtime = time.time()
        while time.time() - curtime < 10 :
            ret = os.system('ping %s -n 1' %self.ip)
            if ret == 0:
                continue
            else:
                curtime_tmp = time.time()
                while time.time() - curtime_tmp < 180:
                    ret = os.system('ping %s -n 1' %self.ip)
                    if ret == 0:
                        print 'cpe_reboot succeed!'
                        Flag = True
                        break
                    else:
                        continue
                if Flag == True:
                    break
        self.RebootRetry -= 1
        if Flag == True:
            time.sleep(10)
            return 0
        else:
            self.dongle_reboot()
    
    def dongle_attach(self, at_cmd="AT+CGATT=1"):
        if self.freq is not None:
            try:
                self.__execute_at_command("AT%%EARFCN=%s" %(self.freq))
            except:
                pass
        try:
            self.__execute_at_command('AT+CFUN=1')
        except:
            pass
        ret = self.__execute_at_command(at_cmd)
        if ret == 0:
            print "cpe_attach succeed!"
            return ret
        elif ret == 1:
            if self.dongle_reboot() == 0:
                self.connect_to_cpe()
                try:
                    self.__execute_at_command('AT+CFUN=1')
                except:
                    pass
                ret = self.__execute_at_command(at_cmd)
                if ret == 0:
                    print "cpe_attach succeed!"
                    return ret
                else:
                    print "*WARN* cpe_attach failed!"
                    return 1
        
    def dongle_detach(self, at_cmd="AT+CGATT=0"):
        ret = self.__execute_at_command(at_cmd)
        if ret == 0:
            print "cpe_detach succeed!"
        elif ret == 1:
            print "*WARN* cpe_detach failed!"
        return ret
        
    def check_dongle_attach_status(self, at_cmd="AT+CGATT?"):
        """This keyword used for execute attach AT command to UE by Telnet.

        Example
        | Check Dongle Attach Status |
        """
        ret = self.execute_at_command(at_cmd)
        if re.search(".*CGATT: 1.*", ret):
            return 0
        else:
            return 1

    def get_dongle_ip_address(self, at_cmd="AT+CGPADDR"):
        """This keyword used for execute attach AT command to UE by Telnet.

        Example
        | Get Dongle IP address |
        """
        """
'\n\n+CGPADDR: 1,"10.68.191.153"\n\n\n\nOK\n\n'
        """
        ip_addr = None
        try:
            for i in range(self.retry_time):
                ret = self.execute_at_command(at_cmd)
                if ret == None:
                    print "None info retruned"
                    break
                if "+CGPADDR" in ret:
                    break
                else:
                    time.sleep(3)
            ip_pattern = "((25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?))"
            #ip_pattern = "(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])).*"
            res_search = re.search(ip_pattern, ret)
            if res_search:
                ## return PDN ip address, such as "10.68.190.xx"
                ip_addr = res_search.group(1)
                return ip_addr
        except Exception, e:
            print "Try to get CPE IP address failed"
            print e
        finally:
            return ip_addr

        
    def get_attached_btscell_id(self,at_cmd="AT%PCONI"):
        """
'duplexing mode: TDD\n\nTransmission mode: Open loop MIMO\n\nBandwidth: 3\n\nEARFCN: 38000\n\nGlobal Cell ID: 00002E01\n\nPhysical Cell ID: 11\n\nOK\n\n'
"""
        cell_id = None
        try:
            for i in range(self.retry_time):
                ret = self.execute_at_command(at_cmd)
                if ret == None:
                    break
                if "Global Cell ID" in ret:
                    break
                else:
                    time.sleep(3)
            result = re.search('Global Cell ID:\s(.*)\n',ret)
            if result:
                global_cellid = int(result.group(1),16)
                btsid = global_cellid/256
                cellid = global_cellid%256
                cell_id = "%d/%d" %(btsid, cellid)
                print "UE have connect to BTS/CELL \"%s\"" % cell_id
        except Exception,e:
            print "Try to get attached bts and cell id failed"
            print e
        finally:
            return cell_id

    def get_dongle_bandwidth(self, at_cmd="AT%GETCFG=\"BAND\""):
        """
'\n\nBands:  38\n\n\n\nOK\n\n'"""
        result = None
        try:
            for i in range(self.retry_time):
                ret = self.execute_at_command(at_cmd)
                if ret:
                    break
            res_result = re.search(".*Bands:\s+(\d+).*", ret, re.I)
            if res_result:
                result = res_result.group(1)
        except Exception,e:
            print "Try to set dongle bandwidth failed"
            print e
        finally:
            return result
        
    def set_dongle_bandwidth(self, band=38):
        result = 1
        try:
            at_cmd = "AT%SETCFG=\"BAND\",\"%s\"" %band
            for i in range(self.retry_time):
                ret = self.execute_at_command(at_cmd)
                if ret:
                    result = 0#0 means set success
                    break
        except Exception,e:
            print "Try to set dongle bandwidth failed"
            print e
        finally:
            return result

    def set_cqi_ri(self, cqi, ri, pmi):
        # Override CQI command ""
        at_cmd = ""
        ret = self.execute_at_command(at_cmd)

        return -1

    def catch_cpe_logs(self, path_saved=""):
        return -1

if __name__ == '__main__':
    #cpe_conn = BtsTelnet()
    #cpe_conn.connect_to_cpe('192.168.255.201')
    con = DMCPE_Control({'name': 'DEMING_CPE','IP':'192.168.15.1'})
    con.execute_at_command("AT+CSQ")
##    print "+++", con.check_dongle_attach_status()
##    print "+++", con.dongle_detach()
##    print "+++", con.set_dongle_bandwidth()
##    print "+++", con.get_dongle_bandwidth()
##    print "+++", con.dongle_attach()
##    print "+++", con.get_attached_btscell_id()
##    print "+++", con.check_dongle_attach_status()
##    print "+++", con.get_dongle_ip_address()
##    print "+++", con.dongle_detach()

##    #Get signal strength Test
##    ret = con._DMCPE_Controlexecute_at_command('AT%CSQ')
#'\n\n%CSQ: 22,99,24\n\n\n\nOK\n\n'
##    #get RSRP
##    ret = con._DMCPE_Controlexecute_at_command('AT%MEAS=\"0\"')
#'\n\nRSRP: Reported = -48, Rx0Tx0 = -49, Rx0Tx1 = -67, Rx1Tx0 = -45, Rx1Tx1 = -68\n\nOK\n\n'
##    #get RSRQ
##    ret = con._DMCPE_Controlexecute_at_command('AT%MEAS=\"1\"')
#'\n\nRSRQ: Reported = -7, Rx0Tx0 = -4, Rx0Tx1 = N/S, Rx1Tx0 = -4, Rx1Tx1 = N/S\n\nOK\n\n'
##    #get SNR
##    ret = con._DMCPE_Controlexecute_at_command('AT%MEAS=\"2\"')
#'\n\nSINR: Reported = 23, Rx0Tx0 = 24, Rx0Tx1 = 11, Rx1Tx0 = 29, Rx1Tx1 = 9\n\nOK\n\n'
##    #get throughput
##    ret = con._DMCPE_Controlexecute_at_command('AT%COUNT=\"PDM\"')
#'\n\nPDM Stats:\n\nRX total number of bytes: 0\n\nTX total number of bytes: 0\n\nRX Throughput: 0\n\nTX Throughput: 0\n\nRX total number of bytes(64b): 0\n\nTX total number of bytes(64b): 0\n\nOK\n\n'
##    #detach
##    ret = con._DMCPE_Controlexecute_at_command('AT+CGATT=0')
##    #attach
##    ret = con._DMCPE_Controlexecute_at_command('AT+CGATT=1')
    pass


