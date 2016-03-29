from __future__ import with_statement
from ftplib import FTP
from optparse import OptionParser
import sys
import StringIO
import os
import re

class FTP_Client():
    def __init__(self, host, port, username, password):

        self.ftp = FTP()
        self.port = int(port)
        try:
            self.ftp.connect(host,port)
        except Exception, e:
            print e
            raise Exception,"Open ftp failed ip='%s' port='%s' " % (host,port)

        try:
            self.ftp.login(username, password)
        except Exception, e:
            print e
            raise Exception," Login serve failed username='%s' password='%s' " % (username,password)

        print self.ftp.getwelcome()

    def ftp_upload_single_file(self, local_file_dir, host_file_name, host_dir):
        try:
            self.ftp.cwd(host_dir)
        except Exception, e:
            print e
            raise Exception," No '%s' dir in ftp serve  " % (host_dir)

        bufsize = 10240

        try:
            file_handler = open(local_file_dir,'rb')
        except Exception, e:
            print e
            raise Exception,"Open file '%s' failed " % (local_file_dir)

        ftp_cmd ='STOR ' + host_file_name
        try:
            self.ftp.storbinary(ftp_cmd, file_handler, bufsize)
        except Exception, e:
            print e
            raise Exception,"Run ftp command '%s' failed" % (ftp_cmd)

        file_handler.close()

    def ftp_download_single_file(self, local_file_dir, host_file_name, host_dir):
        try:
            self.ftp.cwd(host_dir)
        except Exception, e:
            print e
            raise Exception," No '%s' dir in ftp serve  " % (host_dir)

        bufsize = 10240

        try:
            file_handler = open(local_file_dir, 'wb').write
        except Exception, e:
            print e
            raise Exception,"Open file '%s' failed " % (local_file_dir)

        ftp_cmd ='RETR ' + host_file_name
        try:
            self.ftp.retrbinary(ftp_cmd, file_handler, bufsize)
        except Exception, e:
            print e
            raise Exception,"Run ftp command '%s' failed" % (ftp_cmd)


    def get_dirs_files(self):
        dir_res = []
        self.ftp.dir('.' , dir_res.append)
        files = [f.split(None, 8)[-1] for f in dir_res if f.startswith('-')]
        dirs = [f.split(None, 8)[-1] for f in dir_res if f.startswith('d')]
        return files, dirs

    def walk(self, next_dir, filter_flag, walk_flag):
        print 'Walking to', next_dir
        try:
            self.ftp.cwd(next_dir)
        except Exception, e:
            print e
            raise Exception," No '%s' dir in ftp serve  " % (host_dir)
        ftp_curr_dir = self.ftp.pwd()
        
        files, dirs = self.get_dirs_files()
        if (0 < len(files)) and (0 < walk_flag):
            try:
                os.mkdir(next_dir.strip('/'))
            except OSError:
                pass
            os.chdir(next_dir.strip('/'))        
        local_curr_dir = os.getcwd()

        new_files = []
        if "ALL" == filter_flag:
            pass
        else:
            for f in files:
                if re.search(filter_flag, f):
                    new_files.append(f)
            files = new_files

        for f in files:
            print next_dir, ':', f
            outf = open(f, 'wb')
            try:
                self.ftp.retrbinary('RETR %s' % f, outf.write)
            finally:
                outf.close()
        walk_flag += 1
        for d in dirs:
            os.chdir(local_curr_dir)
            self.ftp.cwd(ftp_curr_dir)
            self.walk(d, filter_flag, walk_flag)

    def ftp_download_all_file(self, local_file_dir, host_file_name, host_dir):

        if os.path.isdir(local_file_dir):
            print "Dir %s has existed" % (local_file_dir)
        else:
            try:
                os.makedirs(local_file_dir)
            except Exception, e:
                print e
                raise Exception,"Create directory '%s' failed!" % (local_file_dir)

        os.chdir(local_file_dir) #set current folder as local_file_dir
        walk_flag  = 0
        self.walk(host_dir, host_file_name, walk_flag)


    def ftp_quit(self):
        self.ftp.quit()


def ftp_upload(host, port, username, password, local_file_dir, host_file_name, host_dir):
    """This keyword use ftp download upload file to host PC.

    | Input Parameters | Man. | Description |
    | host             | Yes  | host ip address |
    | port             | Yes  | ftp port |
    | username         | Yes  | ftp login username |
    | password         | Yes  | ftp login password |
    | local_file_dir   | Yes  | upload source file full path |
    | host_file_name   | Yes  | host file name  |
    | host_dir         | Yes  | ftp host file dir |

    Example
    | FTP Upload | 192.168.255.1 | 21 | test | test | d:\\test.dat | test.dat | temp |
    """
    cftp = FTP_Client(host, port, username, password)
    try:
        cftp.ftp_upload_single_file(local_file_dir, host_file_name, host_dir)
    finally:
        cftp.ftp_quit()


def ftp_download(host, port, username, password, local_file_dir, host_file_name, host_dir):
    """This keyword use ftp download upload file to host PC.

    | Input Parameters | Man. | Description |
    | host             | Yes  | host ip address |
    | port             | Yes  | ftp port |
    | username         | Yes  | ftp login username |
    | password         | Yes  | ftp login password |
    | local_file_dir   | Yes  | local file or folder full path |
    | host_file_name   | Yes  | download file name or "ALL"  |
    | host_dir         | Yes  | ftp host file dir |

    Example
    | FTP Download | 192.168.255.1 | 21 | test | test | d:\\test.dat | test.dat | temp |
    | FTP Download | 192.168.255.1 | 21 | test | test | d:\\test | "ALL" | temp |
    | FTP Download | 192.168.254.129 | 21 | root | None | d:\\test | "F01.*" | /ram |

    """
    cftp = FTP_Client(host, port, username, password)
    try:
        if ("ALL" == host_file_name) or (0 <= host_file_name.find('*')):
            cftp.ftp_download_all_file(local_file_dir, host_file_name, host_dir)
        else:
            cftp.ftp_download_single_file(local_file_dir, host_file_name, host_dir)
    finally:
        cftp.ftp_quit()




if __name__ == '__main__':

    description = "ftp_client for TDLTE I&V testing.       \
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
        ftp_download(host, port, username, password, local_file_dir, host_file_name, host_dir)
    elif "ul" == dire:
        ftp_upload(host, port, username, password, local_file_dir, host_file_name, host_dir)
    else:
        raise Exception, "please give the option '-d ul' for upload or download!"

##    pass
