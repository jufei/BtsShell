"""This file is used to control CPE by send AT command
These keywords can be use in Robot framework.
"""
import re
import time
import os
import telnetlib


class LCCPE_Connection:
    def __init__(self, ip):
        self.timeout = 20
        self.pausetime = 2
        self.ip = ip
        self.retpat = re.compile("(?ms).*send message.*type:\d+\s(.*)-1\.exit.*")
        self.retrytime = 2
        #self.connect_to_cpe()
         
    def connect_to_cpe(self):
        for i in range(self.retrytime):
            try:
                self.conn = telnetlib.Telnet(self.ip)
                loginret = self.conn.read_until("ogin:", self.timeout)
                print loginret,
                self.conn.write("root" + os.linesep)
                passwdret = self.conn.read_until("assword:", self.timeout)
                print passwdret
                self.conn.write("5up" + os.linesep)
                ret = self.conn.read_until("~ #", self.timeout)
                print ret,
                self.conn.write("mmtest" + os.linesep)
                time.sleep(self.pausetime)
                print self.conn.read_until("modem file at", self.timeout)
                print "*INFO* connect to longcheer CPE %s success !" % self.ip
                break
            except Exception, e:
                print e
                print "*WARN* connect to longcheer CPE %s failed(%d) !" % (self.ip, i+1)
                try:
                    self.conn.close()
                except:
                    pass
        else:
            raise Exception, "connect to longcheer CPE %s failed !" % self.ip

        
    def execute_at_command(self, cmd):
        for i in range(self.retrytime):
            print self.conn.read_very_lazy()
            self.conn.write('14' + os.linesep)
            time.sleep(self.pausetime)
            inputret = self.conn.read_until("please input at:", self.timeout)
            print inputret,
            self.conn.write(cmd + os.linesep)
            time.sleep(self.pausetime)
            atret = self.conn.read_until("modem file at", self.timeout)
            print atret
            res = self.retpat.search(atret)
            if res:
                atret = res.groups()[0]
                if "OK" in atret:
                    print "*INFO* Command: %s execute successed!" % cmd
                    return atret
                else:
                    print "*WARN* Command: %s execute failed(%d)!" % (cmd, i+1)
        raise Exception, "Command: %s execute failed!" % (cmd)
            
    def reboot(self):
        result = 1
        try:
            for i in range(self.retrytime):
                self.close()
                self.conn = telnetlib.Telnet(self.ip)
                loginret = self.conn.read_until("ogin:", self.timeout)
                print loginret,
                self.conn.write("root" + os.linesep)
                passwdret = self.conn.read_until("assword:", self.timeout)
                print passwdret
                self.conn.write("5up" + os.linesep)
                ret = self.conn.read_until("~ #", self.timeout)
                print ret,
                self.conn.write("reboot" + os.linesep)
                print "reboot"
                flag = False
                sst = time.time()
                while time.time() - sst < 30:
                    if os.system("ping %s -n 1" % self.ip) != 0:
                        print "*INFO* cpe %s is shutdown ..." % self.ip
                        break
                ust = time.time() 
                while time.time() - ust < 180:
                    if os.system("ping %s -n 1" % self.ip) == 0:
                        print "*INFO* cpe %s is up ..." % self.ip
                        flag = True
                        break       
                if flag:
                    print "*INFO* cpe %s reboot success !!" % self.ip
                    result = 0
                    break
                else:
                    print "*WARN* cpe %s reboot failed(%d) !!" % (self.ip, i+1)
        finally:
            return result

    def __del__(self):
        self.close()
        
    def close(self):
        try:
            self.conn.close()
        except:
            pass

class LCCPE_Control:
    def __init__(self, args):
        key_list = args.keys()
        if 'IP' not in key_list:
            raise Exception, "Please input CPE ip address first"
        self.ip = args['IP']
        print "LongCheer CPE started:", self.ip

        self.con = LCCPE_Connection(self.ip)
        self.connect_to_cpe()

    def __del__(self):
        if self.con:
            try:
                #self.__send_cmd("ATBEGIN=2")
                self.con.close()
            except:
                print "*WARN* close connection and lte interface failed!"
        
    def connect_to_cpe(self):
        return self.con.connect_to_cpe()


    def execute_at_command(self, at_cmd):
        try:
            return self.con.execute_at_command(at_cmd)
        except Exception, e:
            print "*WARN* Exec AT cmd \"%s\" failed with error: %s" % (at_cmd, e)
        finally:
            pass

    def dongle_reboot(self): 
        return self.con.reboot()
    
    def dongle_attach(self, at_cmd="AT+CGATT=1"):
        try:
            self.execute_at_command('AT+CFUN=1')
        except:
            pass
        ret = self.execute_at_command(at_cmd)
        if ret:
            print "cpe_attach succeed!"
            return 0
        else:
            if self.dongle_reboot() == 0:
                self.connect_to_cpe()
                try:
                    self.execute_at_command('AT+CFUN=1')
                except:
                    pass
                ret = self.execute_at_command(at_cmd)
                if ret:
                    print "*INFO* cpe_attach succeed!"
                    return 0
                else:
                    print "*WARN* cpe_attach failed!"
                    return 1
        
    def dongle_detach(self, at_cmd="AT+CGATT=0"):
        ret = self.execute_at_command(at_cmd)
        if ret:
            print "*INFO* cpe_detach succeed!"
            return 0
        else:
            print "*WARN* cpe_detach failed!"
            return 1
        
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
    con = LCCPE_Control({'name': 'LONGCHEER_CPE','IP':'192.168.1.1'})
    ret = con.execute_at_command("AT+CGMR")
    con.dongle_attach("AT+CGATT=1")
    
    print '====',ret

    raise "here"
    pass


