"""
This library supports keywords to
   - log in to a remote Linux or Microsoft Windows host via telnet
   - execute any command supported by the underlying operting system

"""
from types import MethodType
import sys
import os
import re
import time

from robot.errors import ExecutionFailed
from BtsComm import TelnetConnection

try:
    mod = __import__("version", globals())
    __version__ = mod.version
except:
    __version__ = "0.0.0"


class BtsTelnet:

    def __init__(self):
        self._telnet_connections = {}
        self._current = None
        self._loglevel = "INFO"

    def connect_to_host(self, host, port = 23, user = "public", passwd = "public", prompt = "", timeout = "120sec"):
        """This keyword opens a telnet connection to a remote host and logs in.

        | Input Parameters | Man. | Description |
        | host      | Yes | Identifies to host |
        | port      | No  | Allows to change the default telnet port |
        | user      | No  | Authentication information. Default is 'public' |
        | passwd    | No  | Authentication information. Default is 'public' |
        | prompt    | No  | prompt as list of regular expressions. Default is: |
        |           |     | "%s@.*\$ " % user for Linux |
        |           |     | "\w:.*>" for Microsoft Windows |
        |           |     | "#" for Cisco Router |
        | timeout   | No  | Timeout for commands issued on this connection. Default is 120 sec |

        | Return value | connection identifier to be used with 'Switch Host Connection' |

        Example
        | Open Test | Connect to Host | zeppo |

        Note
        When log in some device, it don't need input user name, for example ESA,
        you must input uesr by '' to replace it.
        """
        if prompt == None or prompt == "":
           # myprompt = [ "%s@.*\$ " % user, "\w:.*>", "Cisco.*>", "Cisco.*#" ]
           myprompt = [ "%s@.*[$>#]\s{0,1}" % user, "root@.*>$", "\w:.*>", ".*#"]
        else:
           myprompt = prompt

        if user != "":
            conn = TelnetConnection(host, port, myprompt, timeout, "CR")
        else:
            conn = TelnetConnection(host, port, "", timeout, "CR")

        conn.set_loglevel(self._loglevel)
        if user != "":
            ret = conn.login(user, passwd, [ "login: ", "Username: ", "ENTER USERNAME <", '>'], [ "password: ", "Password:\s{0,1}", "Password for .*: " , "ENTER PASSWORD <"])
        else:
            ret = conn.login(user, passwd, [""], [ "password:", "Password:", "Password for .*: " ])

        if ret.find("Microsoft") >= 0:
            self._telnet_connections[conn] = "Windows"
            if prompt == None or prompt == "":
                conn.set_prompt([ "^[a-zA-Z]:.*>", "^.*\(y/n\)\s*", "^.*\(y/n.*\)\s*"])
        elif ret.find("[%s@" % user) >= 0: #linux
            self._telnet_connections[conn] = "Linux"
            if prompt == None or prompt == "":
                conn.set_prompt([ "%s@.*\$|\# " % user, ])
        elif ret.find("openSUSE") >= 0:
            self._telnet_connections[conn] = "Linux"
            if prompt == None or prompt == "":
                conn.set_prompt([".*#"])
        elif ret.find("Flexi Transport Module") >= 0:
            self._telnet_connections[conn] = "Linux"
            if prompt == None or prompt == "":
                conn.set_prompt([".*#"])
        else:
            self._telnet_connections[conn] = "Device"
            if prompt == None or prompt == "":
                conn.set_prompt([ ".*>", ".*#", "Password: " ])

        self._current = conn
        return conn

    def connect_to_mme(self, host, port = 23, user = "SYSTEM", passwd = "SYSTEM", prompt = "", timeout = "120sec"):
        """This keyword opens a telnet connection to a remote host and logs in.

        | Input Parameters | Man. | Description |
        | host      | Yes | Identifies to host |
        | port      | No  | Allows to change the default telnet port |
        | user      | No  | Authentication information. Default is 'public' |
        | passwd    | No  | Authentication information. Default is 'public' |
        | prompt    | No  | prompt as list of regular expressions. Default is: |
        | timeout   | No  | Timeout for commands issued on this connection. Default is 120 sec |
        | Return value | connection identifier to be used with 'Switch Host Connection' |

        Example
        | Open Test | connect to mme | mme_ip |
        """
        if prompt == None or prompt == "":
           myprompt = [ "^<"]
        else:
           myprompt = prompt

        if user != "":
            conn = TelnetConnection(host, port, myprompt, timeout, "CR")
        else:
            conn = TelnetConnection(host, port, "", timeout, "CR")

        conn.set_loglevel(self._loglevel)
        if user != "":
            ret = conn.login(user, passwd, [ "ENTER USERNAME <"], [ "ENTER PASSWORD <"])
        else:
            ret = conn.login(user, passwd, [""], [ "password:", "Password:", "Password for .*: " ])

        self._telnet_connections[conn] = "MME"
        if prompt == None or prompt == "":
            conn.set_prompt([ "^<" ])

        self._current = conn
        return conn

    def get_current_connection_type(self):
        return self._telnet_connections[self._current]

    def connect_to_bts(self, host, port = 23, user = "public", passwd = "public", prompt = "", timeout = "10sec"):
        if prompt == None or prompt == "":
           # myprompt = [ "%s@.*\$ " % user, "\w:.*>", "Cisco.*>", "Cisco.*#" ]
          myprompt = [ "root@.*\$", "root@.*>$", ".*>\r\n.*>", ".*#" ]
        else:
           myprompt = prompt

        if user != "":
            conn = TelnetConnection(host, port, myprompt, timeout, "CR")
        else:
            conn = TelnetConnection(host, port, "", timeout, "CR")

        conn.set_loglevel(self._loglevel)
        if user != "":
            ret = conn.login(user, passwd, [ "login: ", "Username: " ], ["password: ", "Password: ", "Password for .*: "])
        else:
            ret = conn.login(user, passwd, [""], [ "password:", "Password:", "Password for .*: " ])

        self._telnet_connections[conn] = "FlexiBTS"
        if prompt == None or prompt == "":
            conn.set_prompt([ ".*>", ".*#", "Password: " ])

        self._current = conn
        return conn

    def send_command_to_fcmd_from_bts_control_pc(self, host, user, passwd, command):
        try:
            old_prompt = self.set_host_prompt('legislation.')
            ret = self.execute_shell_command_without_check('ssh %s@%s'%(user,host))
            #self.get_recv_content(1000)
            self.set_host_prompt('root@FCTB:~ >')
            self.execute_shell_command_without_check(passwd)
            if isinstance(command,list):
                for i in range(len(command)):
                    ret = self.execute_shell_command_without_check(command[i])
            else:
                ret = self.execute_shell_command_without_check(command)
        finally:
            self.set_host_prompt(old_prompt)
            self.execute_shell_command_without_check('exit')





    def connect_to_aashell(self, host, port, user = "", passwd = "", prompt = "", timeout = "10sec"):
        if prompt == None or prompt == "":
            myprompt = [ "root@.*\$", "root@.*>$", ".*>\r\n.*>", ".*#" ]
        else:
            myprompt = prompt

        if user != "":
            conn = TelnetConnection(host, port, myprompt, timeout, "CR")
        else:
            conn = TelnetConnection(host, port, "", timeout, "CR")

        conn.set_loglevel(self._loglevel)

        self._telnet_connections[conn] = "FlexiBTS"
        if prompt == None or prompt == "":
            conn.set_prompt([ ".*>", ".*#", "Password: " ])

        self._current = conn
        return conn

    def connect_to_ipsec_server(self, host, port = 23, user = "public", passwd = "public", prompt = "", timeout = "10sec"):
        if prompt == None or prompt == "":
            myprompt = [ "root@.*\$", "root@.*>$", ".*>\r\n.*>", ".*#" ]
        else:
            myprompt = prompt

        if user != "":
            conn = TelnetConnection(host, port, myprompt, timeout, "LF")
        else:
            conn = TelnetConnection(host, port, "", timeout, "LF")

        conn.set_loglevel(self._loglevel)
        if user != "":
            ret = conn.login(user, passwd, [ "login: ", "Username: " ], ["password: ", "Password: ", "Password for .*: "])
        else:
            ret = conn.login(user, passwd, [""], [ "password:", "Password:", "Password for .*: " ])

        self._telnet_connections[conn] = "IPSecServer"
        if prompt == None or prompt == "":
            conn.set_prompt([ ".*>", ".*#", "Password: " ])

        self._current = conn
        return conn


    def connect_to_converter(self, host, port=1110, user="public", passwd="public", input_board="3", baudrate="5", prompt="", timeout="10sec"):
        if prompt == None or prompt == "":
            myprompt = [ "root@.*\$", "root@.*>$", ".*->", ".*-> "]
        else:
            myprompt = prompt

        if user != "":
            conn = TelnetConnection(host, port, myprompt, timeout, "LF")
        else:
            conn = TelnetConnection(host, port, "", timeout, "LF")

        conn.set_loglevel(self._loglevel)
        if user != "":
            ret = conn.login_converter(user, passwd, input_board, baudrate,["Username:"], ["Password:"], ["Input Board ID.*:"], [" Enter BaudRate Number:"])
        else:
            ret = conn.login_converter(user, passwd, [""], [ "password:", "Password:", "Password for .*: " ])

        self._telnet_connections[conn] = "Converter"
        if prompt == None or prompt == "":
            conn.set_prompt([ ".*>", ".*#", "Password: ", ".*-> ", ".*->"])

        self._current = conn
        return conn

    def connect_to_LMT_BBP(self, host, port=6000, user="admin", passwd="admin", cmd_prompt = "RETCODE = 0  Operation succeeded.", prompt=""):

        myprompt = prompt
        conn = TelnetConnection(host, port, myprompt)

        conn.set_loglevel(self._loglevel)
        ret = conn.login_LMT_BBP(user, passwd, cmd_prompt)

        self._telnet_connections[conn] = "LMT"
        self._current = conn
        return conn

    def execute_cmd_LMT_BBP(self, cmd, cmd_prompt = "RETCODE = 0  Operation succeeded."):

        print cmd
        self._current.write(cmd)
        time.sleep(1)
        ret = self._current.read(None)

        if cmd_prompt in ret:
          print "execute command in LMT BBP successfully!"
        else:
          print "execute command in LMT BBP error!"

        return ret

    def disconnect_from_LMT_BBP(self, cmd_prompt="RETCODE = 0  Operation succeeded."):

        ret = self._current.disconnect_LMT_BBP(cmd_prompt)
        print ret


    def connect_to_rru(self, host, port=23, user="", passwd="", prompt="", timeout="30sec"):
        if prompt == None or prompt == "":
            myprompt = ["root@.*\$", "root@.*>$", ".*->", ".*->.*", ".*", "\$\s*"]#
        else:
            myprompt = prompt

        if user != "":
            conn = TelnetConnection(host, port, myprompt, timeout, "LF")
        else:
            conn = TelnetConnection(host, port, "", timeout, "LF")

        conn.set_loglevel(self._loglevel)
        if user != "":
            ret = conn.login_converter(user, passwd)
            converter_required = True
        else:
            converter_required = False

        self._telnet_connections[conn] = "RRU"
        if prompt == None or prompt == "":
            if converter_required:
                conn.set_prompt([""])
            else:
                conn.set_prompt(["\$\s*"])

        try:
            conn.get_recv(100)
        except Exception, e:
            print e
            pass

        self._current = conn
        return conn


    def connect_to_tm500(self, host, port = 5003, prompt = "", timeout = "30sec"):
        if prompt == None or prompt == "":
          myprompt = [ "" ]
        else:
           myprompt = prompt
        port = int(port)
        try:
            conn = TelnetConnection(host, port, myprompt, timeout, "CR")
        except:
            try:
                conn = TelnetConnection(host, port+1, myprompt, timeout, "CR")
            except:
                conn = TelnetConnection(host, port+2, myprompt, timeout, "CR")

        conn.set_loglevel(self._loglevel)

        self._telnet_connections[conn] = "TM500"
        if prompt == None or prompt == "":
            conn.set_prompt([ "" ])

        self._current = conn
        return conn

    def connect_to_cpe(self, host, port=23, prompt="", timeout="30sec"):
        """This keyword opens a telnet connection to remote CPE.

        | Input Parameters | Man. | Description |
        | host      | Yes | Identifies to host |
        | port      | No  | Allows to change the default telnet port |
        | prompt    | No  | prompt as list of regular expressions. Default is: |
        | timeout   | No  | Timeout for commands issued on this connection. Default is 120 sec |

        Example
        | Connect To CPE | 192.168.15.1 |
        """
        if prompt == None or prompt == "":
          myprompt = ["root@.*\$", ".*#", ".*>"]
        else:
           myprompt = prompt

        conn = TelnetConnection(host, port, myprompt, timeout, "CR")
        ret = conn.get_recv(512)
        conn.set_loglevel(self._loglevel)

        self._telnet_connections[conn] = "CPE"
        if prompt == None or prompt == "":
            conn.set_prompt([".*#", ".*>"])

        self._current = conn
        return conn

    def connect_to_catapult(self, host="10.68.152.157", port=23, user="catapult", passwd="catapult", prompt="", timeout="30sec"):
        """This keyword opens a telnet connection to remote CPE.

        | Input Parameters | Man. | Description |
        |       host       |  No  | Default is "10.206.25.151" |
        |       port       |  No  | Allows to change the default telnet port |
        |      prompt      |  No  | prompt as list of regular expressions. Default is: |
        |      timeout     |  No  | Timeout for commands issued on this connection. Default is 30 sec |

        Example
        | Connect To Catapult | 10.206.25.151 |
        """
        if prompt == None or prompt == "":
          myprompt = ["root@.*\$", "root@.*>$", ".*]:", ".*]: "]
        else:
           myprompt = prompt

        if user != "":
            conn = TelnetConnection(host, port, myprompt, timeout, "CR")
        else:
            conn = TelnetConnection(host, port, "", timeout, "CR")

        conn.set_loglevel(self._loglevel)
        if user != "":
            ret = conn.login_catapult(user, passwd, [".*login: ", ".*login:"], ["Password:", "Password: "])
        else:
            ret = conn.login_catapult(user, passwd, [".*login: ", ".*login:"], ["Password:", "Password: "])

        self._telnet_connections[conn] = "ixiaCatapult"
        if prompt == None or prompt == "":
            conn.set_prompt([ ".*]:", ".*]: "])

        self._current = conn
        return conn


    def set_host_prompt(self, new_prompt):
        """This keyword sets the connection prompt to new prompt other than default one.
        """
        old_prompt = self._current._prompt
        self._current.set_prompt(new_prompt)
        return old_prompt

    def disconnect_all_hosts(self):
        """Closes all existing telnet connections to remote hosts.
        """
        for conn in self._telnet_connections:
            conn.close_connection()
        self._telnet_connections = {}
        self._current = None

    def disconnect_from_host(self):
        """Closes the telnet connections to the currently active remote host.
        """
        self._telnet_connections.pop(self._current)
        self._current.close_connection()
        if len(self._telnet_connections) == 0:
            self._current = None
        else:
            self._current = self._telnet_connections.keys()[0]

    def switch_host_connection(self, conn):
        """Switch to the connection identified by 'conn'.

        The value of the parameter 'conn' was obtained from keyword 'Connect to Host'
        """
        if conn in self._telnet_connections:
            self._current = conn
            print "Switch to '%s' now."%conn.host
        else:
            raise RuntimeError("Unknow connection Switch Host Connection")

    def current_host_connection(self):
        """
        get current host connection.
        """
        return self._current

    def set_shell_loglevel(self, loglevel):
        """Sets the loglevel of the current host connection.

        The log level of the current connection is set. If no connection exists yet, this loglevel is used as default
        for connections created in the future. In both cases the old log level is returned, either the log level of the
        current connection or the previous default loglevel.

        | Input Paramaters | Man. | Description |
        | loglevel         | Yes  | new loglevel, e.g. "WARN", "INFO", "DEBUG", "TRACE" |

        | Return Value | Previous log level as string |
        """
        if self._current == None:
            old = self._loglevel
            self._loglevel = loglevel
            return old
        return self._current.set_loglevel(loglevel)

    def set_shell_timeout(self, timeout = "30sec"):
        """Allows to set a different timeout for long lasting commands.

        | Input Paramaters | Man. | Description |
        | timeout | No | Desired timeout. If this parameter is omitted, the timeout is reset to 30.0 seconds. |

        Example
        | Reset Timeout Test | Set MML Timeout |
        """
        return self._current.set_timeout(timeout)

    def set_pause_time(self, pause = "3"):
        """Allows to set a different timeout for long lasting commands.

        | Input Paramaters | Man. | Description |
        | timeout | No | Desired timeout. If this parameter is omitted, the timeout is reset to 30.0 seconds. |

        Example
        | Reset Pause Time Test | Set pause Timeout |
        """
        return self._current.set_pause(pause)

    def get_recv_content(self, length = 2048):
        """Allows to set a different receive length.

        | Input Paramaters | Man. | Description |
        | timeout | No | Desired timeout. If this parameter is omitted, the length is reset to 2048. |

        Example
        | get recv content | content length |
        """
        length = int(length)
        return self._current.get_recv(length)

    def execute_shell_command(self, command, password="", username="root",timeout="0"):
        """Execute a command on the remote system. Depending on the system type some checks concerning the command success are performed.

        | Input Parameters  | Man. | Description |
        | command           | Yes  | command to be executed on the remote system |
        | password          | No   | password for user on the remote system (Linux only) |
        |                   |      | default is "", execute command as current user. |
        | username          | No   | username for execute command on the remote system (Linux only) |
        |                   |      | default is "root". |

        | Return value | command output (String) |

        Example
        | Execute shell command | ${command} |                  | # execute command as current user. |
        | Execute shell command | ${command} | ${root password} | # execute command as root. |
        """
        result = self.execute_shell_command_without_check(command,timeout,password,username)
        current_env =  self._telnet_connections[self._current]
        if "Cisco" == current_env:
            if (result.lower().find("unknown command") >= 0 or
               result.lower().find("incomplete command") >= 0 or
               result.lower().find("invalid input") >= 0 or
               result.lower().find("command rejected") >= 0):
                raise ExecutionFailed, "Execute failed !"
        elif "Linux" == current_env:
            raw_return_code = self.execute_shell_command_without_check('echo $?')
            return_lines = raw_return_code.splitlines()
            try:
                return_code = int(return_lines[0])
            except ValueError:
                return_code = int(return_lines[1])
            if return_code != 0:
                raise ExecutionFailed, "Execute failed with return code: %d" % return_code
        elif "Windows" == current_env or "MS" == current_env:
            raw_return_code = self.execute_shell_command_without_check('echo %ERRORLEVEL%')
            return_lines = raw_return_code.splitlines()
            try:
                return_code = int(return_lines[1])
            except ValueError:
                return_code = int(return_lines[0])
            if return_code != 0:
                raise ExecutionFailed, "Execute failed with return code: %d" % return_code
        else:
            pass
        return result


    def execute_shell_command_without_check(self, command, timeout="0",password="", username="root"):
        """Execute a command on the remote system without checking the result.

        | Input Parameters  | Man. | Description |
        | command           | Yes  | command to be executed on the remote system |
        | timeout           | No   |  sleep time if need to set command timeout |
        | password          | No   | password for user on the remote system (Linux only) |
        |                   |      | default is "", execute command as current user. |
        | username          | No   | username for execute command on the remote system (Linux only) |
        |                   |      | default is "root". |

        | Return value | command output (String) |

        Example
        | Execute shell command | ${command} |                  | # execute command as current user. |
        | Execute shell command | ${command} | ${root password} | # execute command as root. |
        """
        if self._telnet_connections[self._current] == "Linux" and password != "" and username != "root":
            # use "su" to change user for command
            self._current.write("su " + username)
            origprompt = self._current.set_prompt("Password:")
            self._current.read_until_prompt(None)
            self._current.write(password)
            origprompt.append("%s@.*[\$|\#] " % username)
            self._current.set_prompt(origprompt)
            self._current.read_until_prompt()
            self._current.write('echo $?')
            return_lines = self._current.read_until_prompt().splitlines()
            try:
                return_code = int(return_lines[0])
            except ValueError:
                return_code = int(return_lines[1])
            if return_code != 0:
                raise ExecutionFailed, 'CANNOT to change user %s with password:%s.' % (username,password)

        self._current.write(command)
        try:
            ret = self._current.read_until_prompt()
            time.sleep(0.25)
            tmp = self._current.read()
            return ret + tmp
        except AssertionError, e:
            print e
            time.sleep(float(timeout))
            self._current.write('\x13')
        self._current.write('\x03')
        time.sleep(0.25)
        self._current.write('\x03')
        raise Exception, "command '%s' execution failed:'%s'" %(command, e)

    def execute_shell_command_bare(self, command):
        return self._current.write_bare(command)


    def execute_tm500_command_without_check(self, command, length = '2048', delay_timer = '0', exp_prompt='', newtimeout = 600, ignore_output = 'N'):
        # read the socket queue before any command execution
        import time
        timeout = newtimeout
        rs = time.time()
        try:
            old_pause_time = self.set_pause_time("0")
            latency = self._current.read_eager()
        except:
            pass
        finally:
            self.set_pause_time(old_pause_time)

        # with open('/home/work/tarun/a.txt', 'a') as f:
        #     f.write(time.ctime() + '  Execute Command: '+ command +  '\n')

        self._current.write(command)
        ret = ''
        st = time.time()
        ret += self._current.read_eager()
        str1 = 'C: %s' %(command.split(' ')[0]).upper()
        str2 = 'C: %s' %(command.split(' ')[0].replace('#$$','')).upper()

        while (True):
            ret += self._current.read_very_eager()
            if 'OK' in ret.upper():
                break
            if 'FAILURE' in ret.upper():
                break
            if str1 in ret.upper():
                break
            if str2 in ret.upper():
                break
            if time.time() - st > timeout:
                # self._current._log("AAAAAAA Command Timeout! " , self._loglevel)
                ret += 'TMA NO RESPONSE, timeout'
                break
            time.sleep(0.01)

        delay_timeout = float(delay_timer)
        if delay_timeout > 0 or exp_prompt:
            st = time.time()
            while (True):
                ret += self._current.read_very_eager()
                if exp_prompt.strip():
                    if exp_prompt in ret:
                        self._current._log("Found Prompt: " + exp_prompt, self._loglevel)
                        break
                if delay_timeout > 0 and time.time() - st > delay_timeout:
                    # self._current._log("BBBBB Command Timeout! " , self._loglevel)
                    break
                time.sleep(0.05)
        if ignore_output <> 'Y':
            self._current._log("Get Response: " + latency + ret, self._loglevel)
        return ret.upper()

    def execute_cpe_command_without_check(self, command, length='512'):
        # Just copied from "execute_tm500_command_without_check" for execute cpe
        # AT command
        try:
            old_pause_time = self.set_pause_time("0")
            self._current.read_lazy()
        except:
            pass
        finally:
            self.set_pause_time(old_pause_time)

        self._current.write(command)
        ret = self._current.get_recv(int(length))

        return ret


    def execute_tm500_command(self, command, length = '2048', delay_timer = '0', exp_prompt=''):
        ret = self.execute_tm500_command_without_check(command, length, delay_timer, exp_prompt)
        if ret.find('OK') < 0:
            raise ExecutionFailed, "command '%s' execution failed" % command
        return ret

    def execute_tm500_file_without_check(self, file_dir, pause_time = None, last_command_pause_time = None):
        try:
            file_handle = file('%s' % file_dir, 'r')
        except:
            raise ExecutionFailed, "open file '%s' failed" % file_dir
        lines = file_handle.readlines()
        #linesLen = len(lines)
        #i = 0
        # set the pause time for every TM500 commands except for last one
        my_pause_time = pause_time == None and '2' or pause_time
        old_PauseTime = self.set_pause_time(my_pause_time)

        lines = [line for line in lines if not re.match('(^(\r|\n|\s+)$)|(^$)|^#', line)] # remove all the unnecessary lines including comment
        #last_command = lines[-1]
        last_command_index = len(lines) - 1

        try:
            ret = ''
            index = 0
            for command in lines:
                if index == last_command_index:
                    my_last_pause_time = last_command_pause_time == None and '30' or last_command_pause_time
                    self.set_pause_time(my_last_pause_time)
                    ret = self.execute_tm500_command_without_check(command, '15000', '3')
                    if ret.upper().find('OK') < 0:
                        print "command '%s' execution failed" % command
                else:
                    if not re.match('(^(\r|\n|\s+)$)|(^$)', command):
                        ret = self.execute_tm500_command_without_check(command)
                        if ret.upper().find('OK') < 0:
                            print "command '%s' execution failed" % command
                index += 1
            return ret
        finally:
            self.set_pause_time(old_PauseTime)

    def execute_f8_command_without_check(self, command, length = '2048'):
        self._current.write_for_F8(command)
        ret = self._current.get_recv(int(length))
        return ret.upper()

    def execute_f8_command(self, command, length = '2048'):
        ret = self.execute_f8_command_without_check(command, length)
        if ret.find('OK') < 0:
            raise ExecutionFailed, "command '%s' execution failed" % command

    def execute_bash_command(self, command, expected_return_code="0"):
        """ Execute a command on the remote system and check the return code.
        Check the return code ($?) of the command to be the expected return code

        | Input Parameters     | Man. | Description |
        | command              | Yes  | command to be executed on the remote system |
        | expected_return_code | No   | expected return code of the command |
        |                      |      | (default is 0) |

        | Return value | command output (String) |
        """

        return_value = self.execute_shell_command_without_check(command)
        raw_return_code =  self.execute_shell_command_without_check('echo $?')
        return_lines = raw_return_code.splitlines()
        try:
            return_code = int(return_lines[0])
        except ValueError:
            return_code = int(return_lines[1])
        if return_code != int(expected_return_code):
            raise RuntimeError("Command '%s' returned '%s' but '%s' was expected"%(command, return_code,expected_return_code))
        return return_value

    def execute_shell_command_file(self, filename, ignore_errors = "NO"):
        """Executes all commands in the file identified by 'filename'

        Each line in the file is passed to 'execute_mml' or 'execute_mml_without_check'
        when this keyword is used with 'ignore_errors' set to 'YES'. Leading and trailing whitespaces are
        removed. '#' at the beginning of a line marks a comment.
        When a line starts with 'NC', the following command (seperated by a space) is executed without result checking.
        The file is first searched for in the current directory and then in the python path.

        | Input Paramaters | Man. | Description |
        | filnname         | Yes  | filenname of the file which contains the single commands |
        | ignore_errors    | No   | steers the behaviour in case of erros. Default is to check for errors |
        """
        pathlist = sys.path[:]
        pathlist.insert(0, '.')
        for path in pathlist:
#            print path
#            print dir (self)
            name = os.path.join(path, filename)
            if os.path.isfile(name):
                break
            name = None
        if name == None:
            raise RuntimeError("File '%s' not available in python path" % filename)
        file = open(name, mode="rb")
        res = file.read()
        file.close()
        lines = res.splitlines()
        res = ""
        for line in lines:
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                continue
            try:
                if line.startswith("NC "):
                    res += self.execute_shell_command_without_check(line[3:])
                else:
                    res += self.execute_shell_command(line)
            except Exception, e:
                if ignore_errors == "NO" or ignore_errors == "" or ignore_errors == None:
                    raise
                else:
                    print "*WARN* %s" % e.message
        return res

    def ping_system(self, host_or_ip, count="1", packet_size="32", intervall = "1", fromip = ""):
        """'Ping System' allows to send 'count' ICMP ECHO REQUEST of size 'packet_size'
        to the host identified by 'host_or_ip'.
        OS Cisco:Ping
        OS MS:ping
        OS Linux:ping
        | Input Parameters  | Man. | Description |
        | host_or_ip        | Yes  | Name or ip address of the host which shall be pinged |
        | count             | No   | Number of echo requests. Default is 1 |
        | packet_size       | No   | Size of the echo requests. Default is 32 |
        | intervall         | No   | Time between two echo requests. Default is 1 sec. Intervals smaller than 0.2 sec are currently not supported. |
        | fromip            | No   | Ip address from where shall be pinged (-I) |

        | Return value      | Number of received ICMP ECHO RESPONSEs ("1" or "0") |

        Example
        | Ping Test | ${recv_pkg}=      | Ping System | 10.50.16.11   |
        |           | Fail unless equal | 5           | ${recv_pkg}   |
        """
        if not count or count.lower() == 'none':   count = "1"
        if not packet_size or count.lower() == 'none':  packet_size = "32"
        if not intervall or intervall.lower() == 'none':  intervall = "1"

        if self._telnet_connections[self._current] == "MS":
            res = self.execute_shell_command_without_check("ping -n %s -l %s %s" % (count, packet_size, host_or_ip))
        elif self._telnet_connections[self._current] == "Cisco":
            command = "ping ip %s repeat %s size %s timeout %s" % (host_or_ip, count, packet_size, intervall)
            if fromip:
                command += " source %s" % (fromip)
            res = self.execute_shell_command_without_check(command)
        else:
            if fromip == "":
                res = self.execute_shell_command_without_check("ping -c %s -s %s -i %s %s" % (count, packet_size, intervall, host_or_ip))
            else:
                res = self.execute_shell_command_without_check("ping -c %s -s %s -i %s -I %s %s" % (count, packet_size, intervall, fromip, host_or_ip))

        if self._telnet_connections[self._current] == "Cisco":
            for line in res.splitlines():
                if line.find("Success") >= 0:
                    print line
                    res = line.split()[5]
                    print res
                    return res.split('/')[0][1:]
        else:
            for line in res.splitlines():
                if line.find("Packets:") >= 0:
                    return line.split()[6]
                if line.find("packets") >= 0:
                    return line.split()[3]
        return "0"


    def Check_Axis_power(self,RF_Mode,RF_Count = 1,RF1_ip = '192.168.254.129',RF2_ip = '192.168.254.137',RF3_ip = '192.168.254.145',username = 'root',password = 'axis',port = 23):
        try:
            Local_Conn1 = self.connect_to_host(RF_ip1,port,username,password)
            if RF_Count > 1 and RF_Count < 4:
                Local_Conn2 = self.connect_to_host(RF_ip2,port,username,password)
            if RF_Count == 3:
                Local_Conn3 = self.connect_to_host(RF_ip3,port,username,password)
            if RF_Count not in range(4):
                raise Exception, 'The RF count number is wrong,it is between 1 and 3'
        except:
            raise Exception, 'can not connect to RF'
        try:
            if RF_Count == 1 :
                exec_command_on_axis_and_check_power(Local_Conn1)
            if RF_Count == 2 :
                exec_command_on_axis_and_check_power(Local_Conn1)
                exec_command_on_axis_and_check_power(Local_Conn2)
            if RF_Count == 3 :
                exec_command_on_axis_and_check_power(Local_Conn1)
                exec_command_on_axis_and_check_power(Local_Conn2)
                exec_command_on_axis_and_check_power(Local_Conn3)
        except:
            raise Exception, 'The steps have some problem,please check!'


    def exec_command_on_axis_and_check_power(self,Local_Conn):
        try:
            self.switch_host_connection(Local_Conn)
            self.execute_shell_command_without_check('c2-cmd set tx all on')
            self.execute_shell_command_without_check('fwr 0x41110 0x3')
            self.execute_shell_command_without_check('fwr 0x41110 0x0')
            self.execute_shell_command_without_check('fwr 0x41120 0x3')
            self.execute_shell_command_without_check('fwr 0x41120 0x0')
            time.sleep(4)
            ret = self.execute_shell_command_without_check('dstat')
            power1_value = None
            power2_value = None

            lines = ret.splitlines()
            for line in lines:
                if line.find('Power') >= 0:
                    (power1, power2) = line.split('|')
                    power1_value = float(power1.split()[2])
                    power2_value = float(power2.split()[2])
                    break
            if power1_value == None or power2_value == None:
                raise Exception, 'can not find the specified power value from output (%s)' % ret
            if (RF_Mode == '20M_SISO' or RF_Mode == '10M_SISO') and power1_value <= 10:
                raise Exception, 'power1 value less than zero, it is %f' % power1_value
            if (RF_Mode == '20M_MIMO' or RF_Mode == '10M_MIMO') and (power1_value <= 10 or power2_value <= 10):
                raise Exception, 'power1/power2 value less than zero, it is %f and %f respectively' % (power1_value, power2_value)
        finally:
            self.disconnect_all_hosts()




if __name__ == '__main__':
##    tl = BtsTelnet()
##    tl.connect_to_catapult()
##    vncserver_ret = tl.execute_shell_command_without_check('vncserver')
##    print vncserver_ret
##    cd_ret = tl.execute_shell_command_without_check('cd /home/catapult/NSN_EPC/launchers')
##    print cd_ret
##    dir_ret = tl.execute_shell_command_without_check('dir')
##    print dir_ret
    # tl = BtsTelnet()
    # tl.connect_to_host('10.69.70.75','23','root', 'btstest', '#')
    # tl.execute_shell_command_without_check('cd ..')
    # cmd = 'echo "C:\Documents and Settings>"'
    # tl.execute_shell_command_without_check(cmd)
    # tl.execute_shell_command_without_check("pwd")
    # tl.disconnect_from_host()
    pass
