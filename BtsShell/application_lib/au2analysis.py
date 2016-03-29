import os
import sys
import re
import types
from BtsShell import connections
from BtsShell.file_lib import *
from robot.libraries.BuiltIn import BuiltIn

def Au2Analysis(A2APath, Inifile, A2ALogFile, Switch=""):
    """This keyword used for calling Au2Analysis.exe to analysis the logs together,
    such as UDP log, Trace log, TM500 log and TtiTrace log. Switch example:
    u for UDP log
    t for Trace log
    m for TM500 log
    i for TtiTrace log
    p for TM500 Protocol log
    w for Wireshark log

    |  Input Parameters   | Man. | Description |
    |       A2APath       | Yes  | Path of "Au2Analysis.exe" |
    |       Inifile       | Yes  | ini path used by "Au2Analysis.exe"  |
    |     A2ALogFile      | Yes  | log path to store logs for "Au2Analysis.exe"  |
    |       Switch        | Yes  | should be "u t m i p w"  |

    Example
    |     Au2Analysis     | "c:\\A2A\\Au2Analysis.exe" | "c:\\A2A\\A2A.ini" |
    |                     | "c:\\A2A\\A2ALog.log" | utmipw |
    """

    if Switch == "":
        raise Exception, "ERR/: No command line option give.."

    switch_list = []
    ret = [switch_list.append(item.upper()) for item in Switch]

    # Get command line option
    Option = ''
    if "U" in switch_list:
        Option = Option + ' -u '
    if "T" in switch_list:
        Option = Option + ' -t '
    if "M" in switch_list:
        Option = Option + ' -m '
    if "I" in switch_list:
        Option = Option + ' -i '
    if "P" in switch_list:
        Option = Option + ' -p '
    if "W" in switch_list:
        Option = Option + ' -w '
    if "A" in switch_list:
        Option = Option + ' -a '
        
    if not Option:
        raise Exception, "ERR/: No command line option give.: %s" % switch_list
        return 2
    
    new_ini_file = a2a_file_variable_replace(Inifile)
    
    cmd = "%s -c \"%s\" %s -F -L \"%s\"" % (A2APath, new_ini_file, Option, A2ALogFile)
    print cmd
    #execute command
    """
    try:
        old_timeout = connections.set_shell_timeout("900")
        ret = connections.execute_shell_command_without_check(cmd)
        errcode = connections.execute_shell_command_without_check('echo %ERRORLEVEL%')
        errcode = int(errcode.split('%')[-1].split()[0])
    except Exception, e:
        print e
        raise Exception, "Execute command failed"
        return False
    finally:
        connections.set_shell_timeout(old_timeout)
    """
    ret = os.popen(cmd).read()
    print ret
    ErrNo = 0
    content = ret.split("\n")
    for p_Log in content:
        if re.search("(?i).*ERROR:.*", p_Log):
            ErrNo += 1
        elif re.search("(?i).*CRITICAL:.*", p_Log):
            ErrNo += 1
        elif re.search("(?i).*is not recognized as.*", p_Log):
            raise Exception, "%s" % str(ret)
            return False
        elif re.search("(?i).*The system cannot find the path specified.*", p_Log):
            raise Exception, "%s" % str(ret)
            return False
        elif re.search("(?i).*could not be found.*", p_Log):
            raise Exception, "%s" % str(ret)
            return False
    if (int(ErrNo) == 0)  :
        print "INF/: Check log successfully"
        return True
    else:
        raise Exception, "ERR/: Check log failed, %d errors found" % int(ErrNo)
        return False

def modify_a2a_ini_file(src_file, parameters, dst_file=""):
    """This keyword will modify the Au2Analysis ini file based on the given parameters.

    |  Input Parameters   | Man. | Description |
    |      src_file       | Yes  | Au2Analysis ini file path |
    |     parameters      | Yes  | parameters need to be chaneged, format will be string or list  |
    |      dst_file       |  NO  | default will be same as src_file  |

    Example
    | Modify A2A INI File | "c:\\A2A\\a2a.ini" | ["LOGDIR: D:\\A2A", "UDPLOG_TAG_1: UDPlog*.log"] |
    """
    ini_dict = {}
    # check change list format
    if None == parameters:
        print "No changes needed!"
        return
    elif isinstance(parameters, str) or type(parameters) == types.UnicodeType:
        tmp = parameters.split(":", 1)
        ini_dict[tmp[0]] = parameters
    elif isinstance(parameters, list):
        for content in parameters:
            tmp = content.split(":", 1)
            ini_dict[tmp[0]] = content
    else:
        raise Exception, "Please input such as \"LOGDIR: D:\Au2Analysis\""

    # read ini file
    lines = file_read(src_file)


    # modify ini file content
    for key in ini_dict.keys():
        Tag_IfChanged = False
        for index in range(len(lines)):
            if re.search("^%s:" % (key), lines[index]):
                lines[index] = ini_dict[key]+"\n"
                Tag_IfChanged = True

        if Tag_IfChanged:
            print "Change '%s' success!" % (ini_dict[key])
        else:
            print "change '%s' not found! Bypassed!" % (ini_dict[key])

    # write ini file
    if dst_file == "":
        dst_file = src_file
    file_write(dst_file, lines)

def a2a_file_variable_replace(ini_file):
    """This keyword will replace a2a ini or pdm file varible.
        if there are the varialbe type as robot ${xxx}, it will replace it from robot varible.

    |  Input Parameters   | Man. | Description |
    |  ini_file       | Yes  | Au2Analysis ini file path |
    |  return value   |  modified_ini_file_path  |

    Example
    | a2a_file_variable_replace | "c:\\A2A\\a2a.ini" |
    """
    if not os.path.exists(ini_file):
        raise Exception, "Can't find '%s', please check!"%ini_file
    f_path, f_name = os.path.split(ini_file)

    #ini file variable replace
    modify_ini = _template_file_variable_replace(ini_file)

    ini_file_new = os.path.join(f_path, modify_ini)
    print

    #parse pdm file name and variable replace all pdm file
    pmds = _parse_pdm_file_name(ini_file)
    src_pdm = []
    tar_pdm = []
    for pdm in pmds:
        src_pdm.append(pdm)
        tar_pdm.append(_template_file_variable_replace(os.path.join(f_path, pdm)))
    #print src_pdm, tar_pdm
    print

    #pdm file name change in ini file
    ini_content = file_read(ini_file_new, "string", 'rb')

    for i in range(len(src_pdm)):
        p = re.compile(src_pdm[i])
        ini_content, count = p.subn(tar_pdm[i], ini_content)
        print "Replace '%s' as '%s' %s times in '%s'"%(src_pdm[i], tar_pdm[i], count, ini_file_new)

    file_write(ini_file_new, str(ini_content), 'w')
    return ini_file_new

def _template_file_variable_replace(src_file):
    f_path, f_name = os.path.split(src_file)
    tar_f_name = "modify_" + f_name
    tar_file = os.path.join(f_path, tar_f_name)

    #file_copy(src_file, tar_file)

    f_content = file_read(src_file, "string", 'rb')

    f_content = string.replace( f_content, "\\", "\\\\")

    f_content_new = BuiltIn().replace_variables(f_content)

    #f_content_new
    file_write(tar_file, f_content_new, 'wb')
    print "Replace variable from '%s' to '%s' OK."%(src_file, tar_file)

    return tar_f_name

def _parse_pdm_file_name(src_file):
    pmd_start_list = ['.\\', '$pwd\\', '$PWD\\']
    pdm_file_list = []


    comment_pdms = file_match_all(src_file, "#\s*PARADIGM:(.*)", "r+")
    for i in range(len(comment_pdms)):
        comment_pdms[i] = comment_pdms[i].strip()

    pdms = file_match_all(src_file, "PARADIGM:(.*)", "r+")
    for i in range(len(pdms)):
        pdms[i] = pdms[i].strip()

    for p in comment_pdms:
        pdms.remove(p)

    for pdm in pdms:
        for pmd_start in pmd_start_list:
            if pdm.startswith(pmd_start):
                pdm_file_list.append(pdm.strip(pmd_start))

    pdm_file_list = set(pdm_file_list)
    return pdm_file_list

if __name__=='__main__':
    a2a_file_variable_replace("D:\\SVN\\TACT_UT\\file_lib\\log\\LTE41.ini")
    #_parse_pdm_file_name("d:\\j4chen\\My Documents\\wang sesha\\A2A.ini")
    pass


