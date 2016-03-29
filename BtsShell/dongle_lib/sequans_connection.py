
"""In order to totally control Sequans dongle, please input these parameters:
   ue_control_script, com_port, frequency"""

from BtsShell import connections
from BtsComm import TelnetConnection
import re

class SequansControl():
    def __init__(self, args):
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
self.var_dict['path'], self.var_dict['port'], self.var_dict['frequency'])
        if self.var_dict['imsi']:
            cmd = cmd + " --imsi=%s" % (self.var_dict['imsi'])
        ret = self.__send_command(cmd)
        return ret

    def dongle_detach(self):
        """This keyword used for sending detach AT command to UE through COM port.

        Example
        | Dongle Detach |
        """
        cmd = "python \"%s\" -o detach --port=%s" % (self.var_dict['path'], self.var_dict['port'])
        ret = self.__send_command(cmd)
        return ret

    def get_dongle_ip_address(self):
        """This keyword used for sending get ip AT command to UE through COM port.

        Example
        | Get Dongle IP Address |
        """
        ip_pattern = "([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\
\.([01]?\d\d?|2[0-4]\d|25[0-5])\.(2[0-4]\d|25[0-5]|[01]?\d\d?)"
        old_timeout = connections.set_shell_timeout('300')
        try:
            cmd = "python \"%s\" -o getip --port=%s" % (self.var_dict['path'], self.var_dict['port'])
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
                return ue_ip
            else:
                raise Exception, "The information returned do not contain any correct ip address"
        finally:
            connections.set_shell_timeout(old_timeout)


    def check_dongle_attach_status(self):
        """This keyword used for sending get status AT command to UE through COM port.

        Example
        | Check Dongle Attach Status |
        """
        cmd = "python \"%s\" -o checkstatus --port=%s" % (self.var_dict['path'], self.var_dict['port'])
        ret = self.__send_command(cmd)
        return ret


    def set_cqi_ri(cqi="15", qi="1"):
        """This keyword used for sending get ip AT command to UE through COM port.

        | Input Parameters  | Man. | Description |
        |         cqi       |  No  | CQI value need to set, default is "15"  |
        |         ri        |  No  | RI value need to set, default is "1"  |

        Example
        | Set CQI RI | 15 | 1 |
        """
        cmd = "python \"%s\" -o setcqiri --port=%s --cqi=%s --ri=%s" % (\
self.var_dict['path'], self.var_dict['port'], cqi, ri)
        ret = self.__send_command(cmd)
        return ret


