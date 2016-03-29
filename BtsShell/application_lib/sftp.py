from __future__ import with_statement
import os
import re
import paramiko
from optparse import OptionParser
from BtsShell import connections
from BtsShell.common_lib.get_path import *
from BtsShell.file_lib.common_operation import *

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
            print "sftp connect to '%s', username:'%s', password:'%s' is ok" % (host,username,password)
        except Exception,e:
            raise Exception, "sftp connect to '%s', username:'%s', password:'%s' is failed, reason:'%s'." % (host, username, password, e)

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

    def download_file_once(self, local_file, target_file):
        self.get_size(target_file)
        self.sftp.get(target_file, local_file)
        local_file_size = os.path.getsize(local_file)
        if int(local_file_size) == 0:
            self.sftp.get(target_file, local_file)
            print "local file size is zero, try again"

        print "sftp download from '%s' to '%s' is ok. local file size is %sk"%\
                  (target_file, local_file, int(local_file_size)/1000)
                  
    def download_file(self, local_file, target_file):
        try:
            self.download_file_once(local_file, target_file)
        except Exception,e:
            print "download failed for:"
            print e
            ret = os.popen("ping %s"%self.host).read()
            print ret
            try:
                self.download_file_once(local_file, target_file)
            except Exception,e:
                print e
                raise Exception, "sftp download from '%s' to '%s' is failed."%\
                  (target_file, local_file)
                


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

    def __search_advanced(self, target_dir, local_dir, file_filter = "", if_deep_walk = True):
        """
        search all files with filter into local dir, no dir tree will keep
        Input Parameters:
        [1] target_dir: dir on ssh server
        [2] local_dir: local dir where will store searched files
        [3] file_filter: regular expression about file name, such as ".*.xml", "\d+_\d+.log"
        [4] if_deep_walk: if search in sub directory

        Output Parameters:
        [1] result
        """
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
                print "%s is a dir" % item_path
                if if_deep_walk:
                    self.__search_advanced(item_path, local_dir, file_filter, if_deep_walk)
                else:
                    print "No deep mode, jump sub dir %s" % item_path

            else:
                print "Error happens when check %s!" % item_path

        return True

    def __download_advanced(self, target_dir, local_dir, if_deep_walk = True, file_filter = ""):
        """

        """

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
                print "%s is a dir" % item_path
                if if_deep_walk:
                    local_sub_dir = os.path.join(local_dir, item)
                    self.__download_advanced(item_path, local_sub_dir, if_deep_walk, file_filter)
                else:
                    print "No deep mode, jump sub dir %s" % item_path
            else:
                print "Error happens when check %s!" % item_path

        return True


    def download_dir(self, target_dir, local_dir, file_filter = ""):
        return self.__download_advanced(target_dir, local_dir, False, file_filter)

    def download_dir_deep(self, target_dir, local_dir, file_filter = ""):
        return self.__download_advanced(target_dir, local_dir, True, file_filter)

    def search_dir(self, target_dir, local_dir, file_filter):
        return self.__search_advanced(target_dir, local_dir, file_filter, False)

    def search_dir_deep(self, target_dir, local_dir, file_filter):
        return self.__search_advanced(target_dir, local_dir, file_filter, True)

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
    try:
        _sftp_download_once(host, port, username, password, local_file_dir, host_file_name, host_dir)
    except Exception,e:        
        print "sftp download failed for '%s'\nTry to sftp download again!"%e
        _sftp_download_once(host, port, username, password, local_file_dir, host_file_name, host_dir)
        
    
    
def _sftp_download_once(host, port, username, password, local_file_dir, host_file_name, host_dir):    
    sf = Sftp(host, port, username, password)
    try:
        if '.*' in host_file_name:
            sf.download_dir(host_dir, local_file_dir, host_file_name)
        else:
            sf.download_file(local_file_dir, '%s/%s' % (host_dir, host_file_name))
    finally:
        sf.close()

def sftp_download_deep(host, port, username, password, local_file_dir, host_file_name, host_dir):
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
    | SFTP Download | 192.168.255.1 | 22 | test | test | d:\\temp | .*.txt | /tmp | download all txt file |
    | SFTP Download | 192.168.255.1 | 22 | test | test | d:\\test.bat | test.bat | /tmp | download test.bat file |
    | SFTP Download | 192.168.255.1 | 22 | test | test | d:\\new.bat | test.bat | /tmp | download test.bat file and change name |


    """
    sf = Sftp(host, port, username, password)
    try:
        sf.download_dir_deep(host_dir, local_file_dir, host_file_name)
    finally:
        sf.close()

def sftp_upload(host,port,username,password,local_file, host_file_name, host_dir):
    """This keyword use sftp upload file from BTS control PC to BTS. telnet connection is not needed.

    | Input Parameters | Man. | Description |
    | host             | Yes  | host ip address |
    | port             | Yes  | sftp port |
    | username         | Yes  | sftp login username |
    | password         | Yes  | sftp login password |
    | local_file_dir   | Yes  | upload source file full path |
    | host_file_name   | Yes  | host file name  |
    | host_dir         | Yes  | sftp host file dir |

    Example
    | SFTP Upload | 192.168.255.1 | 22 | test | test | d:\\test.dat | test.dat | temp |
    """
    sf = Sftp(host, port, username, password)
    try:
        sf.upload_file(local_file, host_dir+'/'+host_file_name)
    finally:
        sf.close()

sftp_exe_path = os.path.join(get_tools_path(),"sftp_client.exe")
def sftp_download_remote(host, port, username, password, local_file, host_file_name, host_dir):
    """This keyword use sftp download file from BTS to BTS control PC. telnet connection is needed.

    | Input Parameters | Man. | Description |
    | host             | Yes  | host ip address |
    | port             | Yes  | ftp port |
    | username         | Yes  | ftp login username |
    | password         | Yes  | ftp login password |
    | local_file_dir   | Yes  | local file full path |
    | host_file_name   | Yes  | download file name |
    | host_dir         | Yes  | ftp host file dir |

    Example
    | SFTP Download remote| 192.168.255.1 | 21 | test | test | d:\\test.dat | test.dat | temp |

    """
    cmd = "%s -d dl -i %s -p %s -u %s -w %s -l \"%s\" -f %s -r \"%s\""%\
              (sftp_exe_path, host, port, username, password, local_file, host_file_name, host_dir)

    return connections.execute_shell_command_without_check(cmd)

def sftp_upload_remote(host,port,username,password,local_file, host_file_name, host_dir):
    """This keyword use sftp upload file from BTS control PC to BTS. telnet connection is needed.

    | Input Parameters | Man. | Description |
    | host             | Yes  | host ip address |
    | port             | Yes  | ftp port |
    | username         | Yes  | ftp login username |
    | password         | Yes  | ftp login password |
    | local_file_dir   | Yes  | upload source file full path |
    | host_file_name   | Yes  | host file name  |
    | host_dir         | Yes  | ftp host file dir |

    Example
    | SFTP Upload remote| 192.168.255.1 | 21 | test | test | d:\\test.dat | test.dat | temp |
    """
    cmd = "%s -d ul -i %s -p %s -u %s -w %s -l \"%s\" -f %s -r \"%s\""%\
              (sftp_exe_path, host, port, username, password, local_file, host_file_name, host_dir)
    return connections.execute_shell_command_without_check(cmd)



if __name__ == '__main__':
    #sftp_download('10.68.143.135', 22, "Nemuadmin", "nemuuser", "d:\\", "WiresharkFile.cap", "/home/test")
    description = "sftp_client for TDLTE I&V testing.       \
                   Author: Chen Jin(61368521)                  \
                   Email: jin_emily.chen@nsn.com                         \
                   Data: 2012-3-30                                                                         \
                   Version: 1.0.0"
    parser = OptionParser(description = description)

    parser.add_option("-d", "--direction",
                              action = "store",
                              dest = "direction",
                              type = "string",
                              default = "dl",
                              help = "upload or download file by ftp.")
    parser.add_option("-i", "--hostip",
                              action = "store",
                              dest = "host",
                              type="string",
                              default = "10.68.152.46",
                              help = "ftp host ip address.")
    parser.add_option("-p", "--port",
                              action = "store",
                              dest = "port",
                              type="string",
                              default = "21",
                              help = "ftp port default as 21.")
    parser.add_option("-u", "--username",
                              action = "store",
                              dest = "username",
                              type="string",
                              default = "ftp",
                              help = "ftp login username.")
    parser.add_option("-w", "--password",
                              action = "store",
                              dest = "password",
                              type="string",
                              default = "ftp",
                              help = "ftp login password.")
    parser.add_option("-l", "--localdir",
                              action = "store",
                              dest = "localdir",
                              type="string",
                              default = "d:/tmp",
                              help = "ftp port default as 21.")
    parser.add_option("-f", "--hostfilename",
                              action = "store",
                              dest = "hostfilename",
                              type="string",
                              default = "ALL",
                              help = "ftp login username.")
    parser.add_option("-r", "--hostdir",
                              action = "store",
                              dest = "hostdir",
                              type="string",
                              default = "new/a",
                              help = "ftp login password.")
    (options, args) = parser.parse_args()
    dire = options.direction
    host = options.host
    port = options.port
    username = options.username
    password = options.password
    local_file_dir = options.localdir
    host_file_name = options.hostfilename
    host_dir = options.hostdir

    if "dl" == dire:
        sftp_download(host, port, username, password, local_file_dir, host_file_name, host_dir)
    elif "ul" == dire:
        sftp_upload(host, port, username, password, local_file_dir, host_file_name, host_dir)
    else:
        raise Exception, "please give the option '-d ul' for upload or download!"
    ## not any debug informatino here, this py will be used directly.



