import os
import paramiko
from optparse import OptionParser
class Sftp():
    def __init__(self, host, port, username, password):
        try:        
            self.transport = paramiko.Transport((host, int(port)))
            print "transport is ok, host:'%s', port:'%s'"%(host, port)
        except Exception,e:
            print e
            raise Exception, "transport is failed, host:'%s', port:'%s'"%\
                          (host,port)
        try:
            self.transport.connect(username=username, password=password)
            #'str' object has no attribute 'get_name' if use username, password directly
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            print "sftp connect to '%s', username:'%s', password:'%s' is ok"%\
                      (host,username,password)            
        except Exception,e:            
            raise Exception, "sftp connect to '%s', username:'%s', password:'%s' is failed, reason:'%s'."%\
                          (host, username, password, e)
        
    def sftp_upload_file(self, local_file, host_file_name, host_dir):
        try:
            self.sftp.put(local_file, host_dir+'/'+host_file_name)
            print "sftp upload from '%s' to '%s' is ok."%\
                  (local_file, host_dir+'/'+host_file_name) 
        except Exception,e:
            raise Exception, "sftp upload from '%s' to '%s' is failed, reason:'%s'."%\
                  (local_file, host_dir+'/'+host_file_name, e) 
        
    def sftp_download_file(self, local_file, host_file_name, host_dir):
        try:
            self.sftp.get(host_dir+'/'+host_file_name, local_file)
            print "sftp download from '%s' to '%s' is ok."%\
                  (host_dir+'/'+host_file_name, local_file)
        except Exception,e:            
            raise Exception, "sftp download from '%s' to '%s' is failed, reason:'%s'."%\
                  (host_dir+'/'+host_file_name, local_file, e)
        
    def sftp_close(self):
        try:
            self.sftp.close()
            self.transport.close()
            print "sftp close is ok"
        except Exception,e:            
            raise Exception, "sftp close is failed for '%s'"%e
        


def sftp_download(host, port, username, password, local_file, host_file_name, host_dir):
    """This keyword use sftp download file to local PC.

    | Input Parameters | Man. | Description |
    | host             | Yes  | host ip address |
    | port             | Yes  | ftp port |
    | username         | Yes  | ftp login username |
    | password         | Yes  | ftp login password |
    | local_file_dir   | Yes  | local file full path |
    | host_file_name   | Yes  | download file name |
    | host_dir         | Yes  | ftp host file dir |

    Example
    | SFTP Download | 192.168.255.1 | 21 | test | test | d:\\test.dat | test.dat | temp |

    """
    sf = Sftp(host, port, username, password) 
    try:                    
        sf.sftp_download_file(local_file, host_file_name, host_dir) 
    finally:
        sf.sftp_close() 

def sftp_upload(host,port,username,password,local_file, host_file_name, host_dir):
    """This keyword use sftp upload file to host PC.

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
        sf.sftp_upload_file(local_file, host_file_name, host_dir)   
    finally:
        sf.sftp_close()     

    
if __name__ == '__main__':
    description = "sftp_client for TDLTE I&V testing.       \
                   Author: Chen Jin(61368521)                  \
                   Email: jin_emily.chen@nsn.com                         \
                   Data: 2012-5-4                                                                         \
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

    
