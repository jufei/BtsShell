import os
import sys
import re
import glob
import types
from BtsShell import connections
from BtsShell.file_lib import *
from BtsShell.common_lib.get_path import *
from robot.libraries.BuiltIn import _Variables as Variables

def cpla_parse(UDPlog_path, Check_component='', Check_level='', Check_version=''):
    """This keyword used for using CPLA.exe to analyze UDPlog and generate CPLAN html log
    |  Input Parameters | Man. | Description |
    |     UDPlog_path   | Yes  | the UPDlog path you want to analyze  |
    |  Check_component  | Yes  | cplane components <all:rrom:uec> you want to check  |
    |    Check_level    | Yes  | cplane level <all:cell:ue>you want to check |
    |  Check_version    | Yes  | eNB SW version <25:35> you want to check  |


    Example
    |    cpla_parse    | "c:\\UDP.LOG" |
    |    cpla_parse    | ${TEST LOG DIRECTORY}${/}L3_CALL*      |
    |    cpla_parse    | "c:\\UDP.LOG" | "rrom" | "cell" |
    |    cpla_parse    | "c:\\UDP.LOG" | "all"  |  "ue"  | "25" |
    """
    re_output_dir = ''
    #input udplog path checking
    
    udp_path = glob.glob(UDPlog_path)
    if len(udp_path) == 1:
        print "INF/: UDPlog path is right!"
    else:
        raise Exception, "ERR/: UDPlog path is wrong or udp log isn't only one!"
    
    # checking if input udp path is flag or full path
    log_dir = os.path.dirname(udp_path[0])
    H = UDPlog_path.split("\\")[-1]
    flag = ''
    if "*" in H:
        if "." in H:
            flag = H.split(".")[0].strip("*")
        else:
            flag = H.strip("*")
        print "parsing udp log with flag!"
    else:
        print "parsing udp log with full path!"

    #generate command
    
    cmd = os.path.join(get_tools_path(), "CPLA", "cpla.exe") + ' '

    if Check_component:
        cmd = cmd + '/s ' + Check_component.lower() + ' '
    if Check_level:
        cmd = cmd + '/l ' + Check_level.lower() + ' '
    if Check_version:
        cmd = cmd + '/v ' + Check_version.lower() + ' '

    cmd = cmd + "\"" + str(udp_path[0]) + "\""

    #execute command
    try:
        old_timeout = connections.set_shell_timeout(900)
        ret = connections.execute_shell_command_without_check(cmd)
        errcode = connections.execute_shell_command_without_check('echo %ERRORLEVEL%')
        errcode = int(errcode.split('%')[-1].split()[0])
    except Exception, e:
        print e
        print "current command is '%s'"%(cmd)
        raise Exception, "Execute command failed"
    finally:
        connections.set_shell_timeout(old_timeout)

    f = 0
    content = ret.split("\n")
    for line in content:
        if re.search("^Parse end...", line):
            f = f + 1
            
    if (int(f) == 1) and (errcode == 0) :
        print "INF/: Parse UDPlog successfully!"
    else:
        print ret
        raise Exception, "ERR/: Parse UDPlog failed"
    
    # rename output folder
    output = glob.glob(os.path.join(log_dir, "CPLAOutput"))
    if len(output) == 1:
        print "INF/: output path is right!"
        if flag == '':
            flag_name = "Default_CPLAOutput"
        else:
            flag_name = flag + "_CPLAOutput"
        try:
            os.rename(os.path.join(log_dir, "CPLAOutput"), os.path.join(log_dir, flag_name))
            re_output_dir = os.path.join(log_dir, flag_name)
            print "output folder name is %s" % (flag_name)
        except Exception, e:
            print e
            raise Exception, "Rename output folder failed!"
        
    else:
        raise Exception, "ERR/: output path is wrong or output isn't only one!"

        
    return re_output_dir

if __name__=='__main__':

    
    pass


