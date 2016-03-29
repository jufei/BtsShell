from __future__ import with_statement
import os
import re
import time
import string
import sys
import subprocess
import getopt
import threading
import ConfigParser 
import shutil
import paramiko

from SSHLibrary import SSHLibrary

Result = {}

version_content = "RemoteAction is used to support action you want to do via S1 port\n\
Current version is 1.5.0 (support FileCollectorTool to fetch logs)"
help_content = '\n Please input the right parameter in command\
line: currently we can support\n -d:vendor for donwload vendor -u:vendor for\
 upload vendor -c:vswr for enable vswr -r for update vendor\n================\
=================================\n'


class ThreadIP(threading.Thread):
    def __init__(self, ip, save_dir, upload_dir, command_content, value):
        threading.Thread.__init__(self)
        self.ip = ip
        self.save_dir = save_dir
        self.upload_dir = upload_dir
        self.command_content = command_content
        self.value = value
        Result[self.ip] = []
        lenth = len(self.command_content)
        if len(self.save_dir) > 0:
            Result[self.ip].append("@1@\n")
        if len(self.upload_dir) > 0:
            Result[self.ip].append("@1@\n")
        if lenth > 0:
            for inition in range(lenth):
                Result[self.ip].append("@1@\n")
            
    def run(self):
       
        enable_ssh(self.ip)
        lenth = len(self.command_content)
        if len(self.save_dir) > 0 and len(self.upload_dir) == 0 and lenth == 0:
            information = download_action(self.ip, os.path.join(self.save_dir, self.ip), self.value)   # download vendor
            Result[self.ip][0] = information + "\n"
        elif len(self.save_dir) == 0 and len(self.upload_dir) > 0 and lenth == 0:
            ret = upload_action(self.ip, self.upload_dir,self.value)   # upload vendor
            Result[self.ip][0] = ret + "\n"
        elif len(self.save_dir) == 0 and len(self.upload_dir) == 0 and lenth > 0:
            if 'vswr' == self.value:
                infor = Send_command_from_BBU_to_RRU(self.ip, "enable_vswr")
                Result[self.ip][0] = infor + "\n"
            elif 'opt' == self.value:
                infor = Send_command_from_BBU_to_RRU(self.ip, "enable_opt")
                Result[self.ip][0] = infor + "\n"
            elif 'uptime' == self.value:
                infor = excute_command(self.ip, self.command_content[0])
                command_ret = self.ip + ": command :" + self.command_content[0] + "   return is ->" + infor
                Result[self.ip][0] = command_ret + "\n"
            elif 'search' == self.value:
                index = 0
                for command in self.command_content:
                    infor = excute_command(self.ip, command)
                    check_point = command.split(" ")[-1]
               #     print "check point is %s" % (check_point)
                    if check_point in infor:
                        Result[self.ip][index] = self.ip + " : " + check_point + " = 1\n"
                    else:
                        Result[self.ip][index] = self.ip + " : " + check_point + " = 0\n"
                    index = index + 1
            else:
                index = 0   # record for command number
                for command in self.command_content:
                    infor = excute_command(self.ip, command)
                    '''
                    if 'vswr' == self.value and 1 == index:
                     #   log_result = analyse_vswrlog(infor)
                        log_result = analyse_vswrlog(infor, "written succesfully", 6)
                        command_ret = self.ip + ": command :" + command + "   analyse vswr is ->" + log_result
                        Result[self.ip][index] = command_ret + "\n"
                    elif 'opt' == self.value and 1 == index:
                    #    log_result = analyse_vswrlog(infor)
                        log_result = analyse_vswrlog(infor, "written succesfully", 3)
                        command_ret = self.ip + ": command :" + command + "   analyse opt is ->" + log_result
                        Result[self.ip][index] = command_ret + "\n"
                    else:    
                        command_ret = self.ip + ": command :" + command + "   return is ->" + infor
                        Result[self.ip][index] = command_ret + "\n"
                        index = index + 1
                        '''
                    command_ret = self.ip + ": command :" + command + "   return is ->" + infor
                    Result[self.ip][index] = command_ret + "\n"
                    index = index + 1

def analyse_vswrlog(initial_infor, check, times):
    reinfor = ''
    if "129@done@" in initial_infor and "137@done@" in initial_infor and "141@done@" in initial_infor:
        if int(times) == initial_infor.count(check):
            reinfor = "pass:" + initial_infor
            return reinfor
        else:
            reinfor = "fail:" + initial_infor
            return reinfor
        
    else:
        if "129@done@" not in initial_infor:
            reinfor = reinfor + "fail:error in 129 \n"
        if "137@done@" not in initial_infor:
            reinfor = reinfor + "fail:error in 137 \n"
        if "141@done@" not in initial_infor:
            reinfor = reinfor + "fail:error in 141 \n"
    
        reinfor = reinfor + initial_infor
        return reinfor
    
def excutessh_comm(host, comm):
    username = "toor4nsn"
    password = "oZPS0POrRieRtu"
    
    plink_path = "echo y|plink.exe"
    cmd = plink_path + " -pw " + password + " -ssh " + username + "@" + host + " " + comm
    print cmd
    
    try:
        ret = ''
        ret = os.popen(cmd).read()
        
        if '' == ret:
            ret = "command return content is blank,please double check,command:%s" % (comm)
            print ret
        else:
            print ret
            
            
    except:
        ret = "execute popen to run command failed!,command:%s" % (comm)
        raise ret
    
    return ret

def execute_remote_sshcmd(conn, cmd, except_ret):
    try:
        ret = conn.SendCmd(cmd)
        if except_ret in ret:
            return True
        else:
            print "execute command %s failed!" % (cmd)
            return False
    except:
        raise "execute command %s failed!" % (cmd)
            
def normalize_content(content, flag = 'ip'):
    
    returnlist = []
    if 'ip' == flag:
        for i in range(len(content)):
            ip = content[i].split("\n")[0].strip()
            if(len(ip) >1):
                returnlist.append(ip)

    elif 'command' == flag:
        for i in range(len(content)):
            command = content[i].split("\n")[0]
            if(len(command) >0):
                returnlist.append(command)
    return returnlist

class SshConnection:
    def __init__(self):
        self._ssh_connections = {}
        self._current = None
        self._loglevel = "INFO"

    def connect_to_ssh_host(self, host, port = 22, user = "omc", passwd = "omc", prompt = "", timeout = "60sec"):
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
        | Open Test | Connect To SSH Host | OMS |

        Note
        When log in some device, it don't need input user name, for example ESA,
        you must input uesr by '' to replace it.
        """
        if prompt == None or prompt == "":
           myprompt = '#'
        else:
           myprompt = prompt

        conn = SSHLibrary(timeout, "CR", myprompt)
        conn.open_connection(host)
        conn.login(user, passwd)

        self._ssh_connections[conn] = 'Linux'
        self._current = conn
        self._current._prompt = myprompt
        return conn
    
    def set_ssh_prompt(self, new_prompt):
        """This keyword sets the SSH connection prompt to new prompt other than default one.
        """
        old_prompt = self._current._prompt
        self._current.set_prompt(new_prompt)
        return old_prompt

    def disconnect_from_ssh(self):
        """Closes the SSH connections to the currently active remote host.
        """
        self._ssh_connections.pop(self._current)
        self._current.close_connection()
        if len(self._ssh_connections) == 0:
            self._current = None
        else:
            self._current = self._ssh_connections.keys()[0]
            
    def judge_folder_exist(self, folder_dir, folder_name):
        
        cmd = 'll -F ' + folder_dir + ' |grep ' + folder_name
        self._current.write(cmd)
        time.sleep(0.5)
        temp = self._current.read()
        flag = 0
        if re.search(folder_name, temp):
            flag = 1
        return flag
         
    def capture_rrulog(self, rru_ip, username, password, prompt):

        folder_name = 'RRULog' + rru_ip[-3:]
        
        file_list = ['F01_fault_history_log.txt','F01_pm_collect.log','F01_pm_1_system.log','F01_pm_2_system.log','F01_startup.zip',\
                  'F01_runtime.zip','fdrules.xml','swconfig.txt','dapdcalibs','tempFile','dapdconfigs','FileDirectory.xml']
        try:
            
            if 1 == self.judge_folder_exist("/tmp", folder_name):
                print "folder: %s is existed!" % (folder_name)
                cmd = 'rm -rf /tmp/' + folder_name + '/*'
                self._current.write(cmd)
                self._current.read_until_regexp(prompt)
            else:
                print "folder: %s is not existed!creating a new one!" % (folder_name)
                cmd = 'mkdir /tmp/' + folder_name
                self._current.write(cmd)
                self._current.read_until_regexp(prompt)
                
            ini_prompt = self.set_ssh_prompt('$ ')
            self._current.write('ping -c 2 -i 0.1 %s' %(rru_ip))
            time.sleep(0.5)
            temp = self._current.read()
         #   print temp
            if not re.search('2 received', temp.splitlines()[-3]):
                information = "Fail: ping RRU %s failed" % (rru_ip)
                raise Exception,information
            else:
                self._current.write('telnet %s 2323' %(rru_ip))
                time.sleep(0.5)
                self._current.read_until_regexp('Welcome to OSE Shell ose5.3.')
                print "telnet rru:%s ok......"%(rru_ip)
                self._current.write('log -a')
                self._current.read_until_regexp('Successfully collected node 0xF01 logs.')
                self._current.write('ls')
                time.sleep(0.5)
              #  self._current.read_until_regexp('F01_frozenFrame.log')
                self._current.write('ftp 192.168.255.1')
                self._current.read_until_regexp('Name:')
                self._current.write(username)
                self._current.read_until_regexp('Password:')
                self._current.write(password)
                self._current.read_until_regexp('ftp> ')
                try:
                    for file_name in file_list:
                        cmd = 'put /ram/' + file_name + ' /tmp/' + folder_name + '/' + file_name
                        self._current.write(cmd)
                        self._current.read_until_regexp('ftp> ')
                except:
                    raise Exception, "ftp put file from RRU:%s to BBU error!" % (rru_ip)
                finally:
                    self._current.write('bye')
                    self._current.read_until_regexp('221 Goodbye.')

                    self._current.write('exit')
                    self._current.read_until_regexp(prompt)
        except:
            self.set_ssh_prompt(ini_prompt)
            self._current.write('\n')
            self._current.read_until_regexp(prompt)
            raise Exception, "ping %s failed" % (rru_ip)
            

        
    def send_command_to_rru_from_bbu(self, host, flag):
      
        enable_opt_command = 'rad -pw 0xED 1'
        enable_vswr_mimor = 'rad -nspw VSWR_Minor_Alarm_OFF 0'
        enable_vswr_major = 'rad -nspw VSWR_Major_Alarm_OFF 0'
        information = ''
        try:
            ini_prompt = self.set_ssh_prompt('$ ')
            self._current.write('ping -c 2 -i 0.1 %s' %(host))
            time.sleep(0.5)
            temp = self._current.read()
            print temp
            if not re.search('2 received', temp.splitlines()[-3]):
                information = "Fail: ping RRU %s failed" % (host)
                raise Exception,information
            else:
                self._current.write('telnet %s 2323' %(host))
                time.sleep(0.5)
                self._current.read_until_regexp('Welcome to OSE Shell ose5.3.')
                print "telnet rru:%s ok......"%(host)
                if "enable_opt" == flag:
                    try:
                        self._current.write(enable_opt_command)
                        time.sleep(0.5)
                        self._current.read_until_regexp('written succesfully')
                        print "enable opt succesfully!"
                    except:
                        print "execute command %s failed!" % (enable_opt_command)
                    finally:
                        self.set_ssh_prompt(ini_prompt)
                        self._current.write('exit')
                        self._current.read_until_regexp('root@FCTB:~ >')
                elif "enable_vswr" == flag:
                    try:
                        self._current.write(enable_vswr_mimor)
                        time.sleep(0.5)
                        self._current.read_until_regexp('written succesfully')
                        print "enable enable vswr mimor succesfully!"

                        self._current.write(enable_vswr_major)
                        time.sleep(0.5)
                        self._current.read_until_regexp('written succesfully')
                        print "enable enable vswr major succesfully!"
                    except:
                        print "execute command %s failed!" % (enable_vswr_major)
                    finally:
                        self.set_ssh_prompt(ini_prompt)
                        self._current.write('exit')
                        self._current.read_until_regexp('root@FCTB:~ >')

        except:
            self.set_ssh_prompt(ini_prompt)
            self._current.write('\n')
            self._current.read_until_regexp('root@FCTB:~ >')
            raise Exception, "ping %s failed" % (host)
            
def Send_command_from_BBU_to_RRU(host, operation):
    
    username = "toor4nsn"
    password = "oZPS0POrRieRtu"
    port = 22
    RRU_1 = "192.168.254.129"
    RRU_2 = "192.168.254.137"
    RRU_3 = "192.168.254.141"
    
    resultall = result_1 = result_2 = result_3 = ''
    
    try:
        SSHCONNECTION = SshConnection()
        conn = SSHCONNECTION.connect_to_ssh_host(host, port, username, password, "~ >")
    except:
        resultall = "Fail:connect to %s with ssh failed!" % (host)
        raise "connect to %s with ssh failed!" % (host)
    
    try:
        SSHCONNECTION.send_command_to_rru_from_bbu(RRU_1, operation)
        result_1 = "%s:PASS:send command from bbu to rru:%s pass,operation:%s\n" % (host, RRU_1, operation)
    except:
        result_1 = "%s:Fail:send command from bbu to rru:%s failed,operation:%s\n" % (host, RRU_1, operation)
        print "%s:Fail:send command from bbu to rru:%s failed,operation:%s" % (host, RRU_1, operation)
    try:
        SSHCONNECTION.send_command_to_rru_from_bbu(RRU_2, operation)
        result_2 = "%s:PASS:send command from bbu to rru:%s pass,operation:%s\n" % (host, RRU_2, operation)
    except:
        result_2 = "%s:Fail:send command from bbu to rru:%s failed,operation:%s\n" % (host, RRU_2, operation)
        print "%s:Fail:send command from bbu to rru:%s failed,operation:%s" % (host, RRU_2, operation)
    try:
        SSHCONNECTION.send_command_to_rru_from_bbu(RRU_3, operation)
        result_3 = "%s:PASS:send command from bbu to rru:%s pass,operation:%s\n" % (host, RRU_3, operation)
    except:
        result_3 = "%s:Fail:send command from bbu to rru:%s failed,operation:%s\n" % (host, RRU_3, operation)
        print "%s:Fail:send command from bbu to rru:%s failed,operation:%s" % (host, RRU_3, operation)
    
    SSHCONNECTION.disconnect_from_ssh() 

    resultall = result_1 + result_2 + result_3
    return resultall
def Capture_RRULog_to_BBU(ip, port, username, password, prompt, RRU):

    flag = 0
    SSHCONNECTION = SshConnection()
    conn = SSHCONNECTION.connect_to_ssh_host(ip, port, username, password, prompt)
    try:
        SSHCONNECTION.capture_rrulog(RRU, username, password, prompt)
        flag = 1
        print "%s:PASS:capture log from rru:%s to bbu successfully!\n" % (ip, RRU)
    except:
        flag =0
        print "%s:Fail:capture log from rru:%s to bbu failed!\n" % (ip, RRU)
    finally:
        SSHCONNECTION.disconnect_from_ssh()
    return flag
                
class Sftp():
    def __init__(self, host, port, username, password):
        self.host=host
        self.port=port
        self.username=username
        self.password=password

        try:
            self.transport = paramiko.Transport((host, int(port)))
            print "transport is ok, host:'%s', port:'%s'"%(host, port)
        except Exception,e:
            print e
            raise Exception, "transport is failed, host:'%s', port:'%s'" % (host,port)
        try:
            self.transport.connect(username=username, password=password)
            #'str' object has no attribute 'get_name' if use username, password directly
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
           # print "sftp connect to '%s', username:'%s', password:'%s' is ok" % (host,username,password)
            print "sftp connect to '%s', username:'%s' is ok" % (host, username) 
        except Exception,e:
            raise Exception, "sftp connect to '%s', username:'%s', is failed, reason:'%s'." % (host, username, e)

    def get_size(self, host_file_path):
        if self.is_file(host_file_path):
            size = self.sftp.lstat(host_file_path).st_size/1000
            print "sftp get file size '%s' is %sKB" % (host_file_path, size)
            return size
        else:
            print "sftp get file size '%s' is wrong: not a file or not exist" % (host_file_path)
            return None



    def upload_file(self, local_file, target_file):
        try:
            self.sftp.put(local_file, target_file)
            print "sftp upload from '%s' to '%s' is ok."%\
                  (local_file, target_file)
            self.get_size(target_file)

        except Exception,e:
            raise Exception, "sftp upload from '%s' to '%s' is failed, reason:'%s'."%\
                  (local_file, target_file, e)

    def download_file(self, local_file, target_file):
        try:
            self.get_size(target_file)
            self.sftp.get(target_file, local_file)
            print "sftp download from '%s' to '%s' is ok."%\
                  (target_file, local_file)
        except Exception,e:
            raise Exception, "sftp download from '%s' to '%s' is failed, reason:'%s'."%\
                  (target_file, local_file, e)


    def close(self):
        try:
            self.sftp.close()
            self.transport.close()
            print "sftp close is ok"
        except Exception,e:
            raise Exception, "sftp close is failed for '%s'"%e



    def listdir(self, path = '.'):
        return self.sftp.listdir(path)

    def is_file(self, path = '.'):
        print path
        ret = self.sftp.lstat(path)
        if str(ret.__str__()).startswith('-'):
            return True
        else:
            return False

    def is_dir(self, path = '.'):
        print path
        ret = self.sftp.lstat(path)
        if str(ret.__str__()).startswith('d'):
            return True
        else:
            return False

    def rename(self, old_path, new_path):
        return self.sftp.rename(old_path, new_path)

    def remove(self, path):
        return self.sftp.remove(path)

    def __download_advanced(self, target_dir, local_dir, if_deep_walk = True, file_filter = ""):

        # change to target dir
        try:
            self.sftp.chdir(target_dir)
            print 'sftp walking to %s' % (target_dir)
        except Exception, e:
            print e
            raise Exception,"sftp cd to dir '%s' failed." % (target_dir)
        sftp_curr_dir = self.sftp.getcwd()
        
        # make local dir
        if not os.path.isdir(local_dir):
            dir_create(local_dir)
            

        # walk process
        list_folder = self.listdir(sftp_curr_dir)

        for item in list_folder:
            item_path = '%s/%s' % (sftp_curr_dir, item)
            if self.is_file(item_path):
                print "%s is a flie" % item_path
                local_path = os.path.join(local_dir, item)
                if file_filter != "":
                    if re.search(file_filter, item):
                        self.download_file(local_path, item_path)
                else:
                    self.download_file(local_path, item_path)

            elif self.is_dir(item_path):
          #      print "%s is a dir" % item_path
                if if_deep_walk:
                    local_sub_dir = os.path.join(local_dir, item)
                    self.__download_advanced(item_path, local_sub_dir, if_deep_walk, file_filter)
         #       else:
          #          print "No deep mode, jump sub dir %s" % item_path
            else:
                print "Error happens when check %s!" % item_path

        return True


    def download_dir(self, target_dir, local_dir, file_filter = ""):
        return self.__download_advanced(target_dir, local_dir, False, file_filter)


def sftp_download(host, port, username, password, local_file_dir, host_file_name, host_dir):
    """This keyword use sftp download file from BTS to BTS control PC. telnet connection is not needed.

    | Input Parameters | Man. | Description |
    | host             | Yes  | host ip address |
    | port             | Yes  | sftp port |
    | username         | Yes  | sftp login username |
    | password         | Yes  | sftp login password |
    | local_file_dir   | Yes  | local file full path |
    | host_file_name   | Yes  | download file name | if you want to download whole dir,set this parameter "ALL" |
    | host_dir         | Yes  | sftp host file dir |

    Example
    | SFTP Download | 192.168.255.1 | 22 | test | test | d:\\temp | .* | /tmp | download whole tmp dir |
    | SFTP Download | 192.168.255.1 | 22 | test | test | d:\\temp | .*.txt | /tmp | download all .txt file |
    | SFTP Download | 192.168.255.1 | 22 | test | test | d:\\test.bat | test.bat | /tmp | download test.bat file |
    | SFTP Download | 192.168.255.1 | 22 | test | test | d:\\new.bat | test.bat | /tmp | download test.bat file and change name |


    """
    sf = Sftp(host, port, username, password)
    try:
        if '.*' in host_file_name:
            sf.download_dir(host_dir, local_file_dir, host_file_name)
        else:
            sf.download_file(local_file_dir, '%s/%s' % (host_dir, host_file_name))
    finally:
        sf.close()


def sftp_upload(host,port,username,password,local_file, host_file_name, host_dir):
    """This keyword use sftp upload file from BTS control PC to BTS. telnet connection is not needed.

    | Input Parameters | Man. | Description |
    | host             | Yes  | host ip address |
    | port             | Yes  | ftp port |
    | username         | Yes  | ftp login username |
    | password         | Yes  | ftp login password |
    | local_file_dir   | Yes  | upload source file full path |
    | host_file_name   | Yes  | host file name  |
    | host_dir         | Yes  | ftp host file dir |

    Example
    | SFTP Upload | 192.168.255.1 | 21 | test | test | d:\\test.dat | test.dat | temp |
    """
    sf = Sftp(host, port, username, password)
    try:
        sf.upload_file(local_file, host_dir+'/'+host_file_name)
    finally:
        sf.close()



class CSsh():
    """
    This is a simple class of ssh
    """
    def __init__(self, host, port = 22, user = 'toor4nsn', passwd = 'oZPS0POrRieRtu'):
        self.host = host
        self.port = int(port)
        self.user = user
        self.passwd = passwd
        self.ssh = None
        
        self.Connect()


    def Connect(self):
        """Setup telnet connection
            Input parameters:
                n/a
            Output parameters:
                1. True if success.
                    False if failed.

        """
##        if os.system("ping %s -n 1 -w 3" % self.host) != 0:
##            raise Exception, "Ping host ip failed, please check the connection ok!"
##
        try:
            ssh = paramiko.SSHClient()
##            os.system("TSKILL /A ssh.exe")
##            time.sleep(2)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host, self.port, self.user, self.passwd)
            self.ssh = ssh

        except Exception, p_Err:
            print p_Err
            raise "Open ssh connection error because of authentication failure or port is accopied!"



    def Disconnect(self):
        if self.ssh:
            return self.ssh.close()
        else:
            return True


    def SendCmd(self, command, RetKeyword = None):
        """Send command in ssh socket connection
            Input:
                1. Command
            Output:
                True if execute success.
                False if execute failure.
        """
        if not self.ssh:
            print "Non ssh connection, reconnect again!"
            self.connect()

        if command == None or command == False:
            print "No valid command to run."
            return True
        else:
            command = str(command)
            print "->Send: %s" % command

        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            p_Ret = stdout.read()
            """
            p_Output = stdout.readlines()
            p_Ret = string.join(p_Output)
            """
            print "<-Receive: %s" % p_Ret
            return p_Ret
        except:
            print "Write command failure"
            return False

def execute_sshcommand(host, port, username, password, command):
    
    sshconn = CSsh(host, port, username, password)
    """
    try:
        sshconn.Conect()
    except:
        print "ssh connection failed before executing ssh command"
        """
    try:
        ret = sshconn.SendCmd(command)
    except:
        print"execute ssh command failed,command:%s" % (command)
    finally:
        sshconn.Disconnect()

    return ret

def write_config(section, item, value):
    
    config = ConfigParser.ConfigParser()
    if not os.path.isfile("config.ini"):
        raise "Please put config.ini file in your current dir try again!"
    config.read("config.ini")
    config.set(section, item, value)

    f = open ("config.ini", "r+")
    config.write(f)
    f.close
    
def read_config(section, item):
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    value = config.get(section, item)
    return value
    

def file_write(FileFullPath, FileContent, WriteMode = 'w'):
    """Write content to File

    Input:
        [1]: FileFullPath: file to wirte
        [2]: FileContent: a sequence of strings to write the file
        [3]: WriteMode: e.g 'w', 'a' for normal use, 'wb'/'ab' for bin file, 'wu'/'au' for Unix file
    Output:
        [1]: EReturnSuccess: write sucessfully
              Other: write fail
    """
    #Check input argv
    p_FileName = FileFullPath    
    try:
        with open(p_FileName, WriteMode) as p_FileObj:
            p_FileObj.writelines(FileContent)
    except Exception, e:
        print "Write file %s failed! with ErrInfo: \"%s\"" % (FileFullPath, e)
        return False

    return True

def file_read(FileFullPath, ReadMode = 'r'):
    """Read File content

    Input:
        [1]: File Name
    Output:
        [1]: File content in list
                [] - if file is empty or read error
    """
    if not os.path.isfile(FileFullPath):
        print "File %s does not exists" % (FileFullPath)
        return []
    try:
        with open(FileFullPath, ReadMode) as p_FileObj:
            return p_FileObj.readlines()
    except IOError:
        print "Open %s failed!" % (FileFullPath)
        return []
    

def dir_create(DirFullName):
    """Creat a directory, makes all intermediate-level directories contain the leaf directory.

    Input:[1] p_DirFullName: full path name of directory
    Notes: If directory existed, return 1 directly.
    """
    p_DirFullName = DirFullName
    if os.path.isdir(p_DirFullName):
        print "Dir %s has existed" % (p_DirFullName)
        return False
    try:
        os.makedirs(p_DirFullName)
    except:
        print "Creat directory %s fail" % (p_DirFullName)
        return False
    print "Creat directory %s OK" % (p_DirFullName)
    return True
   

def local_vendor_name(DirFullName):
    """get vendor file name from vendor dir

    Input:[1] p_DirFullName: full path name of directory
   
    """
    for root, dirs, files in os.walk(DirFullName):
        if(0 == len(files)):
            print "there is no file under this folder:%s" % (DirFullName)
            raise "there is no file under this folder:%s" % (DirFullName)
        elif(1 < len(files)):
            print "there are more than one files under this folder:%s" % (DirFullName)
            raise "there are more than one files under this folder:%s" % (DirFullName)
        else:
            print "there is only one file under %s" % (DirFullName)
            return files[0]

def make_download_folder(current_dir):
    """ make one download folder with local time stamp
    """
    
    ret = ''
    for value in time.localtime()[0:6]:
        temp = str(value)
        ret = ret + "_" + temp
    file_name = "download_" + ret
    download_path = os.path.join(current_dir, file_name)
    dir_create(download_path)
    
    return download_path
        

def execute_subprocess(cmd):
    """ create one subprocess to execute cmd
    Input:[1] cmd: the command you want subprocess to execute
    """

   
    try:
        returncode = subprocess.call(cmd, shell = False)
        if returncode < 0:
            print "subprocess was terminated by signal"
        elif returncode == 0:
            print "execute subprocess successfully"
        else:
            print "subprocess returned with code:%s" % (returncode)
    except OSError, e:
        print "execute subprocess failed:", e
        
    
    return returncode

def enable_ssh(ip):
    """ execute command to enable ssh

    Input:[1] ip: the eNB in which you want to enable ssh
   
    """
    #  ping testing
    ping_cmd = "ping " + ip + " -n 2 -w 500"
   
    pingret = execute_subprocess(ping_cmd)

    if 0 == pingret:
        print "ping is ok,ip:%s" % (ip)
    else:
        raise "ping is fail,ip:%s" % (ip)
    
    # enable ssh
    
    current_dir = os.path.abspath(os.curdir)
   
    enablessh_cmd = current_dir + "\\\\" + "wget --user=Nemuadmin --password=nemuuser --no-check-certificate https://" + ip + "/protected/enableSsh.cgi --tries=1 --timeout=10 -O- -q"

    ret = execute_subprocess(enablessh_cmd)
    if 0 == pingret:
        print "enable ssh is ok,ip:%s" % (ip)
    else:
        raise 'Enable SSH fail,command :%s' % (cmd)
        
        

def download_action(ip, file_save_dir, option):
    """ download vendor 

    Input:[1] connection: the connection with eNB from which you want to download vendor
    Input:[1] file_save_dir: the dir you want to save download vendor
   
    """
    username = "toor4nsn"
    password = "oZPS0POrRieRtu"
    port = 22
    file_content = file_vendor = file_scfc = file_config = file_swconfig = file_sysinfo = file_hwf = file_selfdefi =''

    if 'all' == option:
        if "1" == read_config("item", "vendor"):  # download vendor
            host_dir = "/rom"
            host_file_name = "^(vendor_).*(.xml)$"
            try:
                sftp_download(ip, port, username, password, file_save_dir, host_file_name, host_dir)
                file_vendor = '%s: download vendor file successfully!\n' % (ip)
            except:
                file_vendor = '%s: download vendor file failed!\n' % (ip)
        if "1" == read_config("item", "scfc"):  # download scfc
            host_dir = "/rom/config"
            host_file_name = "^(SCF).*(.xml)$"
            try:
                sftp_download(ip, port, username, password, file_save_dir, host_file_name, host_dir)
                file_scfc = '%s: download scf file successfully!\n' % (ip)
            except:
                file_scfc = '%s: download scf file failed!\n' % (ip)
        if "1" == read_config("item", "config"):  # download trs config
            #generate trs config.xml file
            command = '/opt/trs/bin/objcli generate_scf'
            try:
                infor = excute_command(ip, command)
                print infor
            except:
                file_content = '%s: generate trs config.xml file failed!' % (ip)
                
            # download config
            host_dir = "/tmp/ftp"
            host_file_name = "config.xml"
            save_file = os.path.join(file_save_dir, host_file_name)
            try:
                sftp_download(ip, port, username, password, save_file, host_file_name, host_dir)
                file_config = '%s: download trs config.xml file successfully!\n' % (ip)
            except:
                file_config = '%s: download trs config.xml file failed!\n' % (ip)
        if "1" == read_config("item", "swconfig"):  # download swconfig
            host_dir = "/rom"
            host_file_name = "swconfig.txt"
            # make local dir
            if not os.path.isdir(file_save_dir):
                dir_create(file_save_dir)
                print file_save_dir
            local_file = os.path.join(file_save_dir, host_file_name);
            try:
                sftp_download(ip, port, username, password, local_file, host_file_name, host_dir)
                file_swconfig = '%s: download swconfig file successfully!\n' % (ip)
            except:
                file_swconfig = '%s: download swconfig file failed!\n' % (ip)
        if "1" == read_config("item", "hwf"):  # download swconfig
            host_dir = "/rom/config"
            host_file_name = "HWF.xml"
            # make local dir
            if not os.path.isdir(file_save_dir):
                dir_create(file_save_dir)
                print file_save_dir
            local_file = os.path.join(file_save_dir, host_file_name);
            try:
                sftp_download(ip, port, username, password, local_file, host_file_name, host_dir)
                file_hwf = '%s: download HWF.xml file successfully!\n' % (ip)
            except:
                file_hwf = '%s: download HWF.xml file failed!\n' % (ip)
        if "1" == read_config("item", "sysinfo"):  # download sysinfo
            host_dir = "/var/log"
            if judge_remote_file_exist(ip, "/var/log/sysinfo.txt"):
                host_file_name = "sysinfo.txt"
            elif judge_remote_file_exist(ip, "/var/log/sysinfo"):
                host_file_name = "sysinfo"
            else:
                host_file_name = ""
                print "there is no sysinfo.txt or sysinfo file!please check!"
            # make local dir
            if not os.path.isdir(file_save_dir):
                dir_create(file_save_dir)
            local_file = os.path.join(file_save_dir, host_file_name);
            try:
                sftp_download(ip, port, username, password, local_file, host_file_name, host_dir)
                file_sysinfo = '%s: download sysinfo file successfully!\n' % (ip)
            except:
                file_sysinfo = '%s: download sysinfo file failed!\n' % (ip)
                
        if "1" == read_config("item", "selfdefi"):  # download sysinfo
            host_dir_list, host_file_name_list = get_filepath_filename_list()
            pass_list = []
            fail_list = []
            pass_info = ''
            fail_info = ''
            for i in range(len(host_dir_list)):
                host_dir = host_dir_list[i]
                host_file_name = host_file_name_list[i]
    
                # make local dir
                if not os.path.isdir(file_save_dir):
                    dir_create(file_save_dir)
                    print file_save_dir
                local_file = os.path.join(file_save_dir, host_file_name);
                try:
                    sftp_download(ip, port, username, password, local_file, host_file_name, host_dir)
                    pass_list.append(host_file_name)
                except:
                    fail_list.append(host_file_name)
            if len(pass_list) != 0 and len(fail_list) != 0:
                pass_info = '%s: download %s file successfully!\n' % (ip, string.join(pass_list))
                fail_info = '%s: download %s file failed!\n' % (ip, string.join(fail_list))
                file_selfdefi = pass_info + fail_info
            if len(pass_list) != 0 and len(fail_list) == 0:
                file_selfdefi = '%s: download %s file successfully!\n' % (ip, string.join(pass_list))
            if len(pass_list) == 0 and len(fail_list) != 0:
                file_selfdefi = '%s: download %s file failed!\n' % (ip, string.join(fail_list))
            
        file_content = file_vendor + file_scfc + file_config + file_swconfig + file_sysinfo + file_hwf + file_selfdefi
        
    if 'rrulog' == option:
        
        RRU_list = ["192.168.254.129","192.168.254.137","192.168.254.141"]
        prompt = 'root@FCTB:~ >'
    #    capture_result1 = capture_result2 = capture_result3 = 0
        result_1 = result_2 = result_3 = ''
        
        capture_result1 = Capture_RRULog_to_BBU(ip, port, username, password, prompt, RRU_list[0])
        capture_result2 = Capture_RRULog_to_BBU(ip, port, username, password, prompt, RRU_list[1])
        capture_result3 = Capture_RRULog_to_BBU(ip, port, username, password, prompt, RRU_list[2])
                                                                                        
        print "capture log finished,download log starting...."

        if 1 == capture_result1:
            try:
                host_dir = "/tmp/RRULog" + RRU_list[0][-3:]
                name = "RRULog" + RRU_list[0][-3:]
                RRULog_dir = os.path.join(file_save_dir, name);
                host_file_name = '.*'  
                sftp_download(ip, port, username, password, RRULog_dir, host_file_name, host_dir)            
                result_1 = '%s: download RRU:%s Log successfully!\n' % (ip, RRU_list[0])
            except:
                result_1 = '%s: download RRU:%s Log failed!\n' % (ip, RRU_list[0])
        else:
            result_1 = "%s:Fail:capture log from rru:%s to bbu failed!\n" % (ip, RRU_list[0])
                                                
        if 1 == capture_result2:                   
            try:
                host_dir = "/tmp/RRULog" + RRU_list[1][-3:]
                name = "RRULog" + RRU_list[1][-3:]
                RRULog_dir = os.path.join(file_save_dir, name);
                host_file_name = '.*'  
                sftp_download(ip, port, username, password, RRULog_dir, host_file_name, host_dir)            
                result_2 = '%s: download RRU:%s Log successfully!\n' % (ip, RRU_list[1])
            except:
                result_2 = '%s: download RRU:%s Log failed!\n' % (ip, RRU_list[1])
        else:
            result_2 = "%s:Fail:capture log from rru:%s to bbu failed!\n" % (ip, RRU_list[1])
                                                
        if 1 == capture_result3:
            try:
                host_dir = "/tmp/RRULog" + RRU_list[2][-3:]
                name = "RRULog" + RRU_list[2][-3:]
                RRULog_dir = os.path.join(file_save_dir, name);
                host_file_name = '.*'  
                sftp_download(ip, port, username, password, RRULog_dir, host_file_name, host_dir)            
                result_3 = '%s: download RRU:%s Log successfully!\n' % (ip, RRU_list[2])
            except:
                result_3 = '%s: download RRU:%s Log failed!\n' % (ip, RRU_list[2])
        else:
            result_3 = "%s:Fail:capture log from rru:%s to bbu failed!\n" % (ip, RRU_list[2])
                                                
                
        file_content = result_1 + result_2 + result_3

    if 'vendor' == option:
        host_dir = "/rom"
        host_file_name = "^(vendor_).*(.xml)$"
        try:
            sftp_download(ip, port, username, password, file_save_dir, host_file_name, host_dir)
            file_content = '%s: download vendor file successfully!' % (ip)
        except:
            file_content = '%s: download vendor file failed!' % (ip)
    if 'filter' == option:

        saved = os.path.dirname(file_save_dir)            
        bat_path = os.path.join(os.path.join(os.path.dirname(saved), "FileCollectorTool"),"collectfiles.bat")
        
        if "1" == read_config("filter", "techlogs"):  # download filter -fullCoverage
            cmd = 'collectfiles.bat -pw Nemuadmin:nemuuser -ssh ' + username + ':' + password + ' -ne ' + \
                  ip + ' -fullCoverage ' + '-outDir ' + file_save_dir + ' -timeout 1800'
         #   print cmd
           
            ret = execute_subprocess(cmd)
            if 0 == ret:
                file_content = '%s: execute FileCollectorTool to capture techlogs successfully!\n' % (ip)
            else:
                file_content = '%s: execute FileCollectorTool to capture techlogs failed!\n' % (ip)

    return file_content
    
def upload_action(ip, localdir, option):

    username = "toor4nsn"
    password = "oZPS0POrRieRtu"
    port = 22
    file_content = file_vendor = file_scfc = file_config = file_swconfig = file_hwf = file_sysinfo = file_selfdefi = ''
 #   vendor_name = local_vendor_name(localdir)
 #   local_path = os.path.join(localdir, vendor_name)

    
    if 'vendor' == option:
        vendor_name = local_vendor_name(localdir)
        local_path = os.path.join(localdir, vendor_name)
        host_dir = "/rom"
        try:
            sftp_upload(ip, port, username, password, local_path, vendor_name, host_dir)
            file_content = '%s: upload vendor file successfully!' % (ip)
        except:
            file_content = '%s: upload vendor file failed!' % (ip)
    elif 'swconfig' == option:
        vendor_name = local_vendor_name(localdir)
        local_path = os.path.join(localdir, vendor_name)
        host_dir = "/rom"
        try:
            sftp_upload(ip, port, username, password, local_path, vendor_name, host_dir)
            file_content = '%s: upload swconfig file successfully!' % (ip)
        except:
            file_content = '%s: upload swconfig file failed!' % (ip)
    elif 'scf' == option:
        vendor_name = local_vendor_name(localdir)
        local_path = os.path.join(localdir, vendor_name)
        host_dir = "/rom/config"
        try:
            sftp_upload(ip, port, username, password, local_path, vendor_name, host_dir)
            file_content = '%s: upload scf file successfully!' % (ip)
        except:
            file_content = '%s: upload scf file failed!' % (ip)
    elif 'hwf' == option:
        vendor_name = local_vendor_name(localdir)
        local_path = os.path.join(localdir, vendor_name)
        host_dir = "/rom/config"
        try:
            sftp_upload(ip, port, username, password, local_path, vendor_name, host_dir)
            file_content = '%s: upload HWF.xml file successfully!' % (ip)
        except:
            file_content = '%s: upload HWF.xml file failed!' % (ip)
    elif 'update' == option:
        host_dir = "/rom"
        update_vendor_name = read_config("system", "update_vendor_name")
        name = update_vendor_name.strip("\"")
        download_folder_name = read_config("system", "download_folder_name")

        update_dir = os.path.join(os.path.join(localdir,download_folder_name),ip)
        vendor_name = local_vendor_name(update_dir)
        local_path = os.path.join(update_dir, vendor_name)
        try:
            sftp_upload(ip, port, username, password, local_path, name, host_dir)
            file_content = '%s: upload vendor in update process successfully!' % (ip)
        except:
            file_content = '%s: upload vendor in update process failed!' % (ip)
    elif 'vswr' == option:
        host_dir = "/tmp"
        vendor_name = "enablevswr.sh"
        local_path = os.path.join(localdir, vendor_name)
        try:
            sftp_upload(ip, port, username, password, local_path, vendor_name, host_dir)
            file_content = '%s: upload vswr script in update process successfully!' % (ip)
        except:
            file_content = '%s: upload vswr script in update process failed!' % (ip)
    elif 'opt' == option:
        host_dir = "/tmp"
        vendor_name = "enableopt.sh"
        local_path = os.path.join(localdir, vendor_name)
        try:
            sftp_upload(ip, port, username, password, local_path, vendor_name, host_dir)
            file_content = '%s: upload opt script in update process successfully!' % (ip)
        except:
            file_content = '%s: upload opt script in update process failed!' % (ip)
    elif 'config' == option:
        vendor_name = local_vendor_name(localdir)
        local_path = os.path.join(localdir, vendor_name)

    #    remove_remote_files(ip, '/rom/trs_data/db/*')
    #    remove_remote_files(ip, '/rom/trs_data/active/*')
        print 'delete db and bak files in trs_data/db ok'
        host_dir = "/rom/trs_data/db"

        try:
            sftp_upload(ip, port, username, password, local_path, vendor_name, host_dir)
            file_content = '%s: upload trs config file successfully!' % (ip)
        except:
            file_content = '%s: upload trs config file successfully!' % (ip)
        
    elif 'allupdate' == option:
        download_folder_name = read_config("system", "download_folder_name")
        update_dir = os.path.join(os.path.join(localdir,download_folder_name),ip)
        self_path = read_config("item", "selfpath")
        defi_path = self_path.strip("\"")
        self_file = read_config("item", "selffile")
        defi_file = self_path.strip("\"")

        for root, dirs, files in os.walk(update_dir):
            for f in files:
                if f.startswith('vendor_') and f.endswith('.xml') and "1" == read_config("item", "vendor"):   # upload vendor file
                    print '%s is vendor file!' % (f)
                    host_dir = "/rom"
                    local_path = os.path.join(update_dir, f)
                    try:
                        sftp_upload(ip, port, username, password, local_path, f, host_dir)
                        vendor_content = '%s: upload vendor file successfully!\n' % (ip)
                    except:
                        file_content = '%s: upload vendor file failed!\n' % (ip)
                        
                if f.startswith('SCF') and f.endswith('.xml') and "1" == read_config("item", "scfc"):   # upload scfc file
                    print '%s is scf file!' % (f)
                    host_dir = "/rom/config"
                    local_path = os.path.join(update_dir, f)
                    try:
                        sftp_upload(ip, port, username, password, local_path, f, host_dir)
                        file_scfc = '%s: upload scf file successfully!\n' % (ip)
                    except:
                        file_scfc = '%s: upload scf file failed!\n' % (ip)
                        
                if f == 'config.xml' and "1" == read_config("item", "config"): # upload trs config.xml file
                    print '%s is trs config file!' % (f)
                #    remove_remote_files(ip, '/rom/trs_data/db/*')
                #    remove_remote_files(ip, '/rom/trs_data/active/*')
                    print 'delete all files in trs_data/db and trs_data/active ok'
                    host_dir = "/rom/trs_data/db"
                    local_path = os.path.join(update_dir, f)
                    try:
                        sftp_upload(ip, port, username, password, local_path, f, host_dir)
                        file_config = '%s: upload trs config file successfully!\n' % (ip)
                    except:
                        file_config = '%s: upload trs config file failed!\n' % (ip)
                        
                if f == 'swconfig.xml' and "1" == read_config("item", "swconfig"):   # upload swconfig file
                    print '%s is swconfig file!' % (f)
                    host_dir = "/rom"
                    local_path = os.path.join(update_dir, f)
                    try:
                        sftp_upload(ip, port, username, password, local_path, f, host_dir)
                        file_swconfig = '%s: upload swconfig file successfully!\n' % (ip)
                    except:
                        file_swconfig = '%s: upload swconfig file failed!\n' % (ip)

                if f == 'HWF.xml' and "1" == read_config("item", "hwf"):   # upload hwf file
                    print '%s is HWF file!' % (f)
                    host_dir = "/rom/config"
                    local_path = os.path.join(update_dir, f)
                    try:
                        sftp_upload(ip, port, username, password, local_path, f, host_dir)
                        file_hwf = '%s: upload HWF file successfully!\n' % (ip)
                    except:
                        file_hwf = '%s: upload HWF file failed!\n' % (ip)

                if f == 'sysinfo' and "1" == read_config("item", "sysinfo"):   # upload sysinfo file
                    print '%s is sysinfo file!' % (f)
                    host_dir = "/var/log"
                    local_path = os.path.join(update_dir, f)
                    try:
                        sftp_upload(ip, port, username, password, local_path, f, host_dir)
                        file_sysinfo = '%s: upload sysinfo file successfully!\n' % (ip)
                    except:
                        file_sysinfo = '%s: upload sysinfo file failed!\n' % (ip)
                        
                if f == defi_file and "1" == read_config("item", "selfdefi"):   # upload selfdefine file
                    print '%s is self-defined file!' % (f)
                    host_dir = defi_path
                    local_path = os.path.join(update_dir, f)
                    try:
                        sftp_upload(ip, port, username, password, local_path, f, host_dir)
                        file_selfdefi = '%s: upload %s file successfully!\n' % (ip, f)
                    except:
                        file_selfdefi = '%s: upload %s file failed!\n' % (ip, f)
                       
        file_content = file_vendor + file_scfc + file_config + file_swconfig + file_hwf + file_sysinfo + file_selfdefi
    elif 'all' == option:
        for root, dirs, files in os.walk(localdir):
            for f in files:
                print f
                local_path = os.path.join(localdir, f)
                if f.startswith('vendor_') and f.endswith('.xml') and "1" == read_config("item", "vendor"):   # upload vendor file
                    print '%s is vendor file!' % (f)
                    host_dir = "/rom"
                  #  local_path = os.path.join(update_dir, f)
                    try:
                        sftp_upload(ip, port, username, password, local_path, f, host_dir)
                        vendor_content = '%s: upload vendor file successfully!\n' % (ip)
                    except:
                        file_content = '%s: upload vendor file failed!\n' % (ip)
                        
                if f.startswith('SCF') and f.endswith('.xml') and "1" == read_config("item", "scfc"):   # upload scfc file
                    print '%s is scf file!' % (f)
                    host_dir = "/rom/config"
                  #  local_path = os.path.join(update_dir, f)
                    try:
                        sftp_upload(ip, port, username, password, local_path, f, host_dir)
                        file_scfc = '%s: upload scf file successfully!\n' % (ip)
                    except:
                        file_scfc = '%s: upload scf file failed!\n' % (ip)
                        
                if f == 'config.xml' and "1" == read_config("item", "config"): # upload trs config.xml file
                    print '%s is trs config file!' % (f)
                #    remove_remote_files(ip, '/rom/trs_data/db/*')
                #    remove_remote_files(ip, '/rom/trs_data/active/*')
                    print 'delete all files in trs_data/db and trs_data/active ok'
                    host_dir = "/rom/trs_data/db"
                 #   local_path = os.path.join(update_dir, f)
                    try:
                        sftp_upload(ip, port, username, password, local_path, f, host_dir)
                        file_config = '%s: upload trs config file successfully!\n' % (ip)
                    except:
                        file_config = '%s: upload trs config file failed!\n' % (ip)
                        
                if f == 'swconfig.xml' and "1" == read_config("item", "swconfig"):   # upload swconfig file
                    print '%s is swconfig file!' % (f)
                    host_dir = "/rom"
                 #   local_path = os.path.join(update_dir, f)
                    try:
                        sftp_upload(ip, port, username, password, local_path, f, host_dir)
                        file_swconfig = '%s: upload swconfig file successfully!\n' % (ip)
                    except:
                        file_swconfig = '%s: upload swconfig file failed!\n' % (ip)

                if f == 'HWF.xml' and "1" == read_config("item", "hwf"):   # upload hwf file
                    print '%s is HWF file!' % (f)
                    host_dir = "/rom/config"
                  #  local_path = os.path.join(update_dir, f)
                    try:
                        sftp_upload(ip, port, username, password, local_path, f, host_dir)
                        file_hwf = '%s: upload HWF file successfully!\n' % (ip)
                    except:
                        file_hwf = '%s: upload HWF file failed!\n' % (ip)

        file_content = file_vendor + file_scfc + file_config + file_swconfig + file_hwf
            
    return file_content


def excute_command(ip, command):
    port = 22
    username = "toor4nsn"
    password = "oZPS0POrRieRtu"

    try:
        ret = execute_sshcommand(ip, port, username, password, command)
        file_content = ret
    except:
        file_content = '%s: excute ssh command failed! command:%s' % (ip, command)
    return file_content
def get_filepath_filename_list():

    path_name_list = []
    file_name_list = []
    if "1" == read_config("search", "search"):  # check if self-define is enabled
        try:
            config_path_name = read_config("item", "selfpath")
            config_file_name = read_config("item", "selffile")
        except Exception,e:
            result = "read file selfpath and selffile from config.ini error,please check!"
            print e
            raise Exception,result
        path_name = config_path_name.strip("\"")
        file_name = config_file_name.strip("\"")
        path_name_list = path_name.split(",")
        file_name_list = file_name.split(",")
            
        if len(path_name_list) != len(file_name_list):
            result = "file name number isn't equal to path number,please check!"
            print result
            raise Exception,result
        else:
            print len(path_name_list)
            print "file name number is equal to path number!"
            
    return path_name_list,file_name_list
        

def get_search_command():

    return_list = []
    if "1" == read_config("search", "search"):  # check if search is enabled
        print "search file is enabled!"
        try:
            config_file_name = read_config("search", "file_name")
            config_file_path = read_config("search", "file_path")
        except Exception,e:
            result = "read file name and path from config.ini error,please check!"
            print e
            raise Exception,result
        print "read file name and path from config file ok!"
        file_name = config_file_name.strip("\"")
        file_path = config_file_path.strip("\"")
        file_name_list = file_name.split(",")
        file_path_list = file_path.split(",")
        lenth_name = len(file_name_list)
        print lenth_name
        lenth_path = len(file_path_list)
        if lenth_name != lenth_path:
            result = "file name number isn't equal to file path number,please check!"
            print result
            raise Exception,result
        else:
            print "file name number is equal to file path number!"
            for i in range(lenth_name):
                cmd = 'ls ' + file_path_list[i] + '|grep ' + file_name_list[i]
                return_list.append(cmd)

        print len(return_list)
    
    return return_list
    
def remove_remote_files(ip, host_file):
    port = 22
    username = "toor4nsn"
    password = "oZPS0POrRieRtu"

    ret = ''
    sshconn = CSsh(ip, port, username, password)
    try:
        command = 'rm -rf ' + host_file
        ret = sshconn.SendCmd(command)
    except:
        print"execute ssh command failed,command:%s" % (command)
    finally:
        sshconn.Disconnect()

    return ret

def judge_remote_file_exist(ip, remote_file_path):
    port = 22
    username = "toor4nsn"
    password = "oZPS0POrRieRtu"

    sshconn = CSsh(ip, port, username, password)
    flag = 0
    try:
        cmd = 'ls ' + remote_file_path
        ret = sshconn.SendCmd(cmd)
        time.sleep(0.5)
        if re.search(remote_file_path, ret):
            flag = 1
            print "%s is existed!" % (remote_file_path)
        else:
            print "%s isn't existed!" % (remote_file_path)
    except:
        print"execute ssh command failed,command:%s" % (cmd)
    finally:
        sshconn.Disconnect()

    return flag

def cycle(head, info, downloadsave, uploaddir, command, option):
    
    group = []
#    current = info[head:head+50]
    
    if option == 'filter':
        current = info[head:head+10]
    else:
        current = info[head:head+48]
        
    
    group = normalize_content(current, 'ip')
    
    if len(group) > 0:
        threads = []
        for ipindex in group:
            thread = ThreadIP(ipindex, downloadsave, uploaddir, command, option)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
            '''
    if head + 50 <= len(info):
            head = head + 50
            cycle(head, info, downloadsave, uploaddir, command, option)
            '''
    
    if option == 'filter':
        if head + 10 <= len(info):
            head = head + 10
            cycle(head, info, downloadsave, uploaddir, command, option)
    else:
        if head + 48 <= len(info):
            head = head + 48
            cycle(head, info, downloadsave, uploaddir, command, option)
            
def prepare():
    
    li = ['','','','','']
    current_dir = os.path.abspath(os.curdir)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:u:c:")
        for op, value in opts:
            if '-d' == op:
                #download save dir information   # build folder with timestamp infor
                download_save = make_download_folder(current_dir)
                li[0] = download_save
                if ':all' == value:
                    print "download all files with your selection!"
                    li[3] = 'all'
                    write_config("system","download_folder_name", os.path.basename(download_save))
                elif ':rrulog' == value:
                    print "download rru log only"
                    li[3] = 'rrulog'
                    write_config("system","download_folder_name", os.path.basename(download_save))
                elif ':vendor' == value:
                    print "download vendor only"
                    li[3] = 'vendor'
                    write_config("system","download_folder_name", os.path.basename(download_save))
                elif ':filter' == value:
                    print "download filter log only"
                    li[3] = 'filter'
                    write_config("system","download_folder_name", os.path.basename(download_save))
                
            elif '-u' == op:
                if ':vendor' == value:
                    uploaddir = current_dir + "\\upload"
                    li[1] = uploaddir
                    print "upload vendor only"
                    li[3] = 'vendor'
                    if not os.path.isdir(uploaddir):
                        os.mkdir(uploaddir)
                        raise "Please put your vendor file in upload folder and try again!"
                elif ':scf' == value:
                    uploaddir = current_dir + "\\upload"
                    li[1] = uploaddir
                    print "upload scf only"
                    li[3] = 'scf'
                    if not os.path.isdir(uploaddir):
                        os.mkdir(uploaddir)
                        raise "Please put your scfc file in upload folder and try again!"
                elif ':hwf' == value:
                    uploaddir = current_dir + "\\upload"
                    li[1] = uploaddir
                    print "upload HWF only"
                    li[3] = 'hwf'
                    if not os.path.isdir(uploaddir):
                        os.mkdir(uploaddir)
                        raise "Please put your HWF.xml file in upload folder and try again!"
                elif ':swconfig' == value:
                    uploaddir = current_dir + "\\upload"
                    li[1] = uploaddir
                    print "upload swconfig only"
                    li[3] = 'swconfig'
                    if not os.path.isdir(uploaddir):
                        os.mkdir(uploaddir)
                        raise "Please put your swconfig file in upload folder and try again!"
                elif ':update' == value:
                    uploaddir = current_dir
                    li[1] = uploaddir
                    print "update vendor process"
                    li[3] = 'update'
                elif ':vswr' == value:
                    uploaddir = current_dir
                    li[1] = uploaddir
                    print "update enable vswr shell script process"
                    li[3] = 'vswr'
                elif ':opt' == value:
                    uploaddir = current_dir
                    li[1] = uploaddir
                    print "update enable opt shell script process"
                    li[3] = 'opt'
                elif ':config' == value:
                    uploaddir = current_dir + "\\upload"
                    li[1] = uploaddir
                    print "upload config only"
                    li[3] = 'config'
                    if not os.path.isdir(uploaddir):
                        os.mkdir(uploaddir)
                        raise "Please put your config.xml file in upload folder and try again!"
                elif ':all' == value:
                    uploaddir = current_dir + "\\upload"
                    li[1] = uploaddir
                    print "upload all files with your selection!"
                    li[3] = 'all'
                elif ':allupdate' == value:
                    uploaddir = current_dir
                    li[1] = uploaddir
                    print "updateput all files with your selection!"
                    li[3] = 'allupdate'
                    
            elif '-c' == op:
                if ':vswr' == value:
                    print "enable vswr command only"
                    commandlines = []
                    commandlines.append("enable_vswr")
                    li[2] = commandlines
                    li[3] = 'vswr'
                elif ':uptime' == value:
                    print "execute uptime command only"
                    commandlines = []
                    commandlines.append("uptime")
                    li[2] = commandlines
                    li[3] = 'uptime'
                elif ':opt' == value:
                    print "enable opt command only"
                    commandlines = []
                    commandlines.append("enable_opt")
                    li[2] = commandlines
                    li[3] = 'opt'
                elif ':search' == value:
                    print "search file and check exist only"
                    commandlines = []
                    commandlines = get_search_command()
                    li[2] = commandlines
                    li[3] = 'search'
                elif ':normal' == value:
                    print "command only"
                    #comand.txt information
                    command_file_path = os.path.join(current_dir, "command.txt")
                    if not os.path.isfile(command_file_path):
                        file_write(command_file_path,'')
                        raise "system create command.txt auto and please fill in your command and separate by enter!"
                    else:
                        command_content = file_read(command_file_path)
                        commandlines = normalize_content(command_content, 'command')
                        li[2] = commandlines
                        li[3] = 'normal'
                
    except getopt.GetoptError, e:
        print e
        print "%s" % (help_content)
        raise "input parameter error!"

    #bbuip.txt information
    bbuip_path = os.path.join(current_dir, "bbuip.txt")
    if not os.path.isfile(bbuip_path):
        file_write(bbuip_path,'')
        raise "system create bbuip.txt auto and please fill in your bbuip and separate by enter!"
    
    li[4] = bbuip_path
    
    return li
    
def output_file_operation(download, upload, command, option):

    #output.txt information
    current_dir = os.path.abspath(os.curdir)
    output_path = os.path.join(current_dir,"output.txt")
    file_write(output_path,'')
    
    num = 0    # record for ip number
    for ipvalue in Result.keys():
        num = num +1
        index = 0   # record for action number
        file_write(output_path, "NO.%s action information as below: ============================================\n" % num, 'a')
        if len(download) > 0 and len(upload) == 0 and len(command) == 0:
            if '@1@\n' == Result[ipvalue]:
                con = ipvalue + ": Download " + option + " executed failed! please check detail!\n" 
                file_write(output_path, con, 'a')
            else:
                file_write(output_path, Result[ipvalue], 'a')
        elif len(download) == 0 and len(upload) > 0 and len(command) == 0:
            if '@1@\n' == Result[ipvalue]:
                con = ipvalue + ": Upload " + option + " executed failed! please check detail!\n" 
                file_write(output_path, con, 'a')
            else:
                file_write(output_path, Result[ipvalue], 'a')
        elif len(download) == 0 and len(upload) == 0 and len(command) > 0:
            for value in Result[ipvalue]:
                index = index + 1
                if '@1@\n' == value:
                    con = ipvalue + ": " + option + " command Action num:" + str(index) + " executed failed! please check detail!\n" 
                    file_write(output_path, con, 'a')
                else:
                    file_write(output_path, value, 'a')
                

if __name__ == '__main__':

    print version_content
    ret = prepare()
 #   print ret
    
    bbuip_content = file_read(ret[4])
    content = normalize_content(bbuip_content, 'ip')
    if [] == content:
        raise "your bbuip.txt is empty,please check!"
    else:
        start = 0
        cycle(start, bbuip_content, ret[0], ret[1], ret[2], ret[3])
        output_file_operation(ret[0], ret[1], ret[2], ret[3])
        

    print version_content
    print "@action done@"

    sys.exit()

    pass
