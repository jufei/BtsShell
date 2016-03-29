from __future__ import with_statement
import os
import re
import sys
import subprocess
import getopt
import threading
import shutil

Result = {}

class ThreadIP(threading.Thread):
    def __init__(self, ip, value):
        threading.Thread.__init__(self)
        self.ip = ip
        self.value = value
        Result[self.ip] = []
        Result[self.ip].append("@1@")
            
    def run(self):
        if 'ssh' == self.value:
            information = enable_ssh(self.ip)
            Result[self.ip][0] = information + "\n"
        elif 'rdport' == self.value:
            information = enable_rdport(self.ip)
            Result[self.ip][0] = information + "\n"
        elif 'all' == self.value:
            information_ssh = enable_ssh(self.ip)
            information_rdport = enable_rdport(self.ip)
            Result[self.ip][0] = information_ssh + "\n" + information_rdport + "\n"
            
            
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
        raise "execute subprocess failed:", e
        
    
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
        print "Fail:ping is fail,ip:%s" % (ip)
        return "Fail:ping is fail,ip:%s" % (ip)
    
    # enable ssh
    
    current_dir = os.path.abspath(os.curdir)
   
    enablessh_cmd = current_dir + "\\\\" + "wget --user=Nemuadmin --password=nemuuser \
        --no-check-certificate https://" + ip + "/protected/enableSsh.cgi --tries=1 --timeout=10 -O- -q"

    ret = execute_subprocess(enablessh_cmd)
    if 0 == pingret:
        print "enable ssh is ok,ip:%s" % (ip)
        return "Pass:enable ssh is ok,ip:%s" % (ip)
    else:
        print 'Enable SSH fail,command :%s' % (enablessh_cmd)
        return 'Fail:Enable SSH fail,command :%s' % (enablessh_cmd)

def enable_rdport(ip):
    """ execute command to enable rdport

    Input:[1] ip: the eNB in which you want to enable rdport
   
    """
    #  ping testing
    ping_cmd = "ping " + ip + " -n 2 -w 500"
    pingret = execute_subprocess(ping_cmd)

    if 0 == pingret:
        print "ping is ok,ip:%s" % (ip)
    else:
        print "ping is fail,ip:%s" % (ip)
        return "Fail:ping is fail,ip:%s" % (ip)
    
    # enable rdport
    current_dir = os.path.abspath(os.curdir)
   
    enablerdport_cmd = current_dir + "\\\\" + "wget --user=Nemuadmin --password=nemuuser \
        --no-check-certificate https://" + ip + "/protected/enableRndPorts.cgi --tries=1 --timeout=10 -O- -q"

    ret = execute_subprocess(enablerdport_cmd)
    if 0 == pingret:
        print "enable rdport is ok,ip:%s" % (ip)
        return "Pass:enable rdport is ok,ip:%s" % (ip)
    else:
        print 'Enable rdport failed,command :%s' % (enablerdport_cmd)
        return 'Fail:Enable rdport failed,command :%s' % (enablerdport_cmd)



def cycle(head, info, option):
    group = []
    current = info[head:head+50]
  
    group = normalize_content(current, 'ip')
    
    if len(group) > 0:
        threads = []
        for ipindex in group:
            thread = ThreadIP(ipindex, option)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
   
    if head+50 <= len(info):
        head = head + 50
        cycle(head, info, option)
def prepare():
    
    li = ['','']
    current_dir = os.path.abspath(os.curdir)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "he:")
        for op, value in opts:
            if '-e' == op:
                if ':ssh' == value:
                    print "enable ssh only"
                    li[0] = 'ssh'
                elif ':rdport' == value:
                    print "enable rdport only"
                    li[0] = 'rdport'
                elif ':all' == value:
                    print "enable ssh and rdport all"
                    li[0] = 'all'
                
    except getopt.GetoptError, e:
        print e
        print "%s" % (help_content)
        raise "input parameter error!"

    #bbuip.txt information
    bbuip_path = os.path.join(current_dir, "bbuip.txt")
    if not os.path.isfile(bbuip_path):
        file_write(bbuip_path,'')
        raise "system create bbuip.txt auto and please fill in your bbuip and separate by enter!"
    
    li[1] = bbuip_path
    
    return li
    
def output_file_operation(option):

    #output.txt information
    current_dir = os.path.abspath(os.curdir)
    output_path = os.path.join(current_dir,"output.txt")
    file_write(output_path,'')
    
    num = 0    # record for ip number
    for ipvalue in Result.keys():
        num = num +1
        index = 0   # record for action number
        file_write(output_path, "NO.%s action information as below: ============================================\n" % num, 'a')
        if 'ssh' == option:
            if '@1@' == Result[ipvalue]:
                con = ipvalue + ": enable " + option + " executed failed! please check detail!\n" 
                file_write(output_path, con, 'a')
                file_write(output_path, Result[ipvalue], 'a')
            else:
                file_write(output_path, Result[ipvalue], 'a')
        elif 'rdport' == option:
            if '@1@' == Result[ipvalue]:
                con = ipvalue + ": enable " + option + " executed failed! please check detail!\n" 
                file_write(output_path, con, 'a')
                file_write(output_path, Result[ipvalue], 'a')
            else:
                file_write(output_path, Result[ipvalue], 'a')
        elif 'all' == option:
            if '@1@' == Result[ipvalue]:
                con = ipvalue + ": enable ssh and rdport executed failed! please check detail!\n" 
                file_write(output_path, con, 'a')
                file_write(output_path, Result[ipvalue], 'a')
            else:
                file_write(output_path, Result[ipvalue], 'a')

if __name__ == '__main__':

    ret = prepare()
  #  print ret
    bbuip_content = file_read(ret[1])

    start = 0   
    cycle(start, bbuip_content, ret[0])

    output_file_operation(ret[0])

    print "@action done@"

    sys.exit()
