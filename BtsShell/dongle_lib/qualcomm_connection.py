
"""In order to totally control Altair dongle, please input these parameters:
   ${path}${os.sep}altair_control.py, com_port, frequency"""
import re
from BtsShell import connections
from BtsShell.common_lib.get_path import *

class Qualcomm_control():
    def __init__(self, args):
        if not 'PATH' in args.keys():
            args['PATH'] = os.path.join(get_btsshell_path(), "dongle_lib", "Qualcomm_control.py")
        else:
            pass
        self.var_dict = args

    def __send_command(self, cmd):
        old_timeout = connections.set_shell_timeout('300')
        try:
            ret = connections.execute_shell_command_without_check(cmd)
            return ret
        finally:
            connections.set_shell_timeout(old_timeout)

    def dongle_attach(self):
        """This keyword used for sending attach AT command to UE through COM port.

        Example
        | Dongle Attach |
        """
        cmd = "python \"%s\" -o attach --port=%s --freq=%s" % (\
              self.var_dict['PATH'], self.var_dict['PORT'], self.var_dict['FREQUENCY'])
        if self.var_dict.has_key('IMSI'):
            cmd = cmd + " --imsi=%s" % (self.var_dict['IMSI'])
        ret = self.__send_command(cmd)
        if ret.find("Return value is: 0") >0:
            #process pass, if 1, attach success
            return 0
        else:
            return 1

    def dongle_detach(self):
        """This keyword used for sending detach AT command to UE through COM port.

        Example
        | Dongle Detach |
        """
        cmd = "python \"%s\" -o detach --port=%s" % (self.var_dict['PATH'], self.var_dict['PORT'])
        ret = self.__send_command(cmd)
        if ret.find("Return value is: 0") >0:
            #process pass, if 1, detach success
            return 0
        else:
            return 1

    def dongle_reboot(self):
        """This keyword used for sending reset AT command to UE through COM port.

        Example
        | Dongle Detach |
        """
        cmd = "python \"%s\" -o reset --port=%s" % (self.var_dict['PATH'], self.var_dict['PORT'])
        ret = self.__send_command(cmd)
        if ret.find("Return value is: 0") >0:
            #process pass, if 1, detach success
            return 0
        else:
            return 1
        
    def get_dongle_ip_address(self):
        """This keyword used for sending get ip AT command to UE through COM port.

        Example
        | Get Dongle IP Address |
        """
        ip_pattern = "Aquired IP is: ([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\
\.([01]?\d\d?|2[0-4]\d|25[0-5])\.(2[0-4]\d|25[0-5]|[01]?\d\d?)"
        old_timeout = connections.set_shell_timeout('300')
        try:
            cmd = "python \"%s\" -o getip --port=%s" % (self.var_dict['PATH'], self.var_dict['PORT'])
            ret = connections.execute_shell_command_without_check(cmd)
            match = re.search(ip_pattern, ret)
            if match:
                ue_ip = match.group(0)
                if re.search("\"", ue_ip):
                    ue_ip = re.sub("\"", "", ue_ip)
                if re.search("\n", ue_ip):
                    ue_ip = re.sub("\n", "", ue_ip)
                if re.search("\r", ue_ip):
                    ue_ip = re.sub("\r", "", ue_ip)
                return ue_ip.replace('Aquired IP is: ','', 1)
            else:
                print "The information returned do not contain any correct ip address"
                return None                
        finally:
            connections.set_shell_timeout(old_timeout)

    def get_attached_btscell_id(self):
        """This keyword used get cellid.

        Example
        | Get attached btscell id |
        """
        old_timeout = connections.set_shell_timeout('300')
        try:
            cmd = "python \"%s\" -o getcell --port=%s" % (self.var_dict['PATH'], self.var_dict['PORT'])
            ret = connections.execute_shell_command_without_check(cmd)
            match = re.search("Aquired cellid is: (.*)\.", ret)
            if match:
                return match.group(1)
            else:
                print "The information returned do not contain any correct cellid"
                return None                
        finally:
            connections.set_shell_timeout(old_timeout)

    def check_dongle_attach_status(self):
        """This keyword used for sending detach AT command to UE through COM port.

        Example
        | Dongle Detach |
        """
        cmd = "python \"%s\" -o getstatus --port=%s" % (self.var_dict['PATH'], self.var_dict['PORT'])
        ret = self.__send_command(cmd)
        if ret.find("Return value is: 0") >0:
            #process pass, if 1, detach success
            return 0
        else:
            return 1
        
    def execute_at_command(self, atcmd):
        """This keyword used execute at cmd to dongle.

        Example
        | execute_at_command | AT%VER |
        """
        old_timeout = connections.set_shell_timeout('300')
        try:
            cmd = "python \"%s\" -o command -c %s --port=%s" % (self.var_dict['PATH'], atcmd, self.var_dict['PORT'])
            ret = connections.execute_shell_command_without_check(cmd)
            errcode = connections.execute_shell_command_without_check("echo %ERRORLEVEL%")
            errcode = int(errcode.split('%')[-1].split()[0])
            if errcode == 0:
                return ret
            else:
                raise Exception, "execute at command failed!"
        finally:
            connections.set_shell_timeout(old_timeout)


if __name__ == "__main__":
    connections.connect_to_host('10.69.64.112', 23, 'tdlte-tester', '1')
    obj = Qualcomm_control({'PORT':'COM5', 'FREQUENCY':'38000'})
    obj.execute_at_command(r'at%tstlte=\"rrc\",\"idle\",\"0\"')
##    import time
##    time.sleep(15)
##    ip = obj.get_attached_btscell_id()
##    print "+++", ip, "+++"
##    obj.dongle_detach()
##    connections.disconnect_from_host()
