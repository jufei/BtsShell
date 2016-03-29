"""This file is used to control CPE by send AT command after TELNET successfully,
These keywords can be use in Robot framework.
Every methods should try to return a value first, not raise exception.
"""
import re
import time
import telnetlib
from BtsShell.connections.telnet import BtsTelnet

DEBUGDIC = {} # {cpe_ip, ERRCODE}just for debug.
ERRCODE = "0000000000000000"
#POSITION: 0123456789012345

def changestatus(strings, position):
    tmp = ''
    li = list(strings)
    li[position] = 1
    for it in li:
        tmp += str(it)
    return tmp

class AltairCpe_control:
    def __init__(self):
        pass
    def execute_cpe_command(self, host, cmd):
        tel = telnetlib.Telnet(host)
        ret = tel.read_until('# ')
        print ret
        time.sleep(1)
        cmd = cmd +"\n"
        print "will execute command: %s" %(cmd)
        tel.write(cmd+'\n')
        time.sleep(0.2)
        tel.write('\n')
        tel.close()

    def check_telnet(self,host):
        flag = False
        count = 0
        while not flag:
            time.sleep(5)
            if count <=10:
                try:
                    telnetlib.Telnet(host)
                    flag = True
                    print "telnet success..."
                except Exception,e:
                    flag = False
                    count = count+1
            else:
                return False
                break
        return True

class AltairCPEControl:
    def __init__(self, args):
        key_list = args.keys()
        if 'IP' not in key_list:
            raise Exception, "Please input CPE ip address first"
        self.ip = args['IP']
        self.ReTryTime = 5
        print "AltairCPE started:", self.ip

        if 'username' in key_list:
            self.username = args['username']
        else:
            self.username = 'admin'

        if 'password' in key_list:
            self.password = args['password']
        else:
            self.password = 'admin'

    def execute_at_command(self, command):
        command = command.strip()
        if 'AT' in command.upper() and command.upper().startswith("AT"):
            command = "input " + command
        try:
            cpe_conn = BtsTelnet()
            cpe_conn.connect_to_cpe(self.ip)
            cpe_conn.set_pause_time(3)
            # AT command just works under debug mode
            for i in range(self.ReTryTime):
                time.sleep(3)
                dbg_ret = cpe_conn.execute_cpe_command_without_check('dbgCli')
                if dbg_ret.find('This is dbgcli start') > 0:
                    print "*INFO* Enter dbgCli mode success!"
                    break
                else:
                    print "*WARN* Try to enter dbgCli mode for another time."
                    continue
            # execute AT command
            for i in range(self.ReTryTime):
                time.sleep(5)
                ret = cpe_conn.execute_cpe_command_without_check(command)
                ret = ret.lstrip('%s' %(command)).rstrip("dbgcli>").strip()
                print "*INFO* Processed response: %s" % ret
                if ret == "" or ret.find("Unrecognized command.") > 0 or ret.find("<XXXXX>") >0 \
                   or ret.find("+CME ERROR:") >0:
                    print "*WARN* Command: %s execute failed, retry." % command
                else:
                    print "*INFO* Command: %s execute success!" % command
                    break
            return ret
        except Exception, e:
            print e
            raise Exception, "Execute command \"%s\" failed" % (command)
        finally:
            try:
                cpe_conn.disconnect_from_host()
            except Exception, e:
                print e

    def dongle_reboot(self, cmd_line="reboot"):
        #ret = self.execute_at_command("input AT+CRSM=176,28539,0,0,12")
        #print ret
        #ret = self.execute_at_command('input AT+CRSM=214,28539,0,0,12,"FFFFFFFFFFFFFFF"')
        #print ret
        result = 1
        try:
            cpe_col = AltairCpe_control()
            cpe_col.execute_cpe_command(self.ip,cmd_line)
            cpe_col.check_telnet(self.ip)
            time.sleep(20)
            result = 0
        except Exception, e:
            print e
        finally:
            return result

    def dongle_attach(self, at_cmd="enableLte"):
        """This keyword used for execute attach AT command to UE by Telnet.

        Example
        | Dongle Attach |
        """
        self.enable_lte_funcation()
        time.sleep(10)
        ue_status = self.execute_at_command('getUeStatus')
        if re.search("UE Connected", ue_status):
            print "UE Connected after command \"%s\"" % (at_cmd)
            return 0
        else:
            self.dongle_reboot()
            for i in range(5):
                time.sleep(5)
                ue_status = self.execute_at_command('getUeStatus')
                if re.search("UE Connected", ue_status):
                    print "UE Connected after command \"%s\"" % (at_cmd)
                    return 0
        return 1
        #raise Exception, "CPE attach failed, ip: '%s'." % (self.ip)

    def disable_lte_funcation(self, at_cmd="disableLte"):
        """This keyword is for disable lte funcation of CPE
        Example
        | disable lte funcation |
        """
        detach_ret = self.execute_at_command(at_cmd)
        if re.search("LTE interface is disabled", detach_ret):
            print "execute AT command \"%s\" successfully" % (at_cmd)
            return 0
        else:
            print "execute AT command \"%s\" failed" % (at_cmd)
            return 1

    def enable_lte_funcation(self, at_cmd="enableLte"):
        """This keyword is for enable lte funcation of CPE
        Example
        | enable lte funcation |
        """
        detach_ret = self.execute_at_command(at_cmd)
        if re.search("LTE interface is enabled", detach_ret):
            print "execute AT command \"%s\" successfully" % (at_cmd)
            return 0
        else:
            print "execute AT command \"%s\" failed" % (at_cmd)
            return 1
    def dongle_detach(self):
        try:
            for i in range(self.ReTryTime):
                ret = self.disable_lte_funcation()
                if ret == 0:
                    break
                else:
                    time.sleep(3)
                    print "*INFO* Detach failed, retry!"
            return ret
        except Exception,e:
            print "Detach failed."
            print e

    def check_dongle_attach_status(self, at_cmd="input AT+CGATT@"):
        """This keyword used for execute attach AT command to UE by Telnet.

        Example
        | Check Dongle Attach Status |
        """
        for i in range(self.ReTryTime):
            ret = self.execute_at_command(at_cmd)
            if "CGATT" in ret:
                break
            else:
                time.sleep(3)
        if re.search(".*CGATT: 1.*", ret):
            return 0
        else:
            return 1
        return 1 # "Detached"

    def get_dongle_ip_address(self, at_cmd="input AT+CGPADDR"):
        """This keyword used for execute attach AT command to UE by Telnet.

        Example
        | Get Dongle IP address |
        """
        # AT command "AT+CGPADDR" to get CPE attached IP address
        ip_addr = None
        try:
            for i in range(self.ReTryTime):
                ret = self.execute_at_command(at_cmd)
                if "+CGPADDR" in ret:
                    break
                else:
                    time.sleep(3)                
            if ret == None:
                raise Exception, "Do not get any response after sending AT command"
            else:
                ip_pattern = "((25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?))"
                #ip_pattern = "(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])).*"
                res_search = re.search(ip_pattern, ret)
                if res_search:
                    ## return PDN ip address, such as "10.68.190.xx"
                    ip_addr = res_search.group(1)
                    return ip_addr
        except Exception,e:
            print "Try to get CPE IP address failed"
            print e
        finally:
            return ip_addr

    def get_attached_btscell_id(self,at_cmd="input AT%PCONI"):
        cell_id = None
        try:
            for i in range(self.ReTryTime):
                ret = self.execute_at_command(at_cmd)
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
        except Exception,e:
            print "Try to get attached bts and cell id failed"
            print e
        finally:
            return cell_id

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
    con = CpeControl({'name': 'CPE','IP':'192.168.15.1'})
    print "+++", con.dongle_attach()
    print "+++", con.get_attached_btscell_id()
    print "+++", con.check_dongle_attach_status()
    print "+++", con.get_dongle_ip_address()
    print "+++", con.dongle_detach()
    pass


