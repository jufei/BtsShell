import re
import os
import types
import shutil
import sys
import time
import string
import glob
from BtsShell import connections
from BtsShell.common_lib.get_path import *
from BtsShell.application_lib.sftp import *
toolPath = os.path.join(get_tools_path(), "TTITrace")

def _get_mac_ttitrace_once(dsp_id_DL, dsp_id_UL, ttiTrace_DL_path, ttiTrace_UL_path, tool_Type = 'SICFTP'):
    """This keyword start sicftp, generate mac TTI Trace file
    | Input Parameters  | Man. |  Description                |
    | dsp_id_DL         | Yes  |  FSP and Faraday id in DL   |
    | dsp_id_UL         | Yes  |  FSP and Faraday id in UL   |
    | ttiTrace_DL_path  | Yes  |  DL Trace log path          |
    | ttiTrace_UL_path  | Yes  |  UL Trace log path          |

    Example
    | get mac ttitrace | '1243' | '1262' | 'd:\\ttiTraceDL_20111201203759.dat' | 'd:\\ttiTraceUL_20111201203759.dat' |
    """
    SevenUpexe = os.path.join(get_tools_path(), "7UP", "7up.exe")
    sicftp = os.path.join(get_tools_path(), "TTITrace", "sicftp.exe")

    def clean_dat_file(file_pattern):
        for old_dat_file in glob.glob(file_pattern):
            print "Remove old dat file: %s!" % old_dat_file
            os.remove(old_dat_file)

    try:
        if str(tool_Type).strip().upper() == '7UP':
            CurDir = os.getcwd()
            ttiTrace_DL_pattern = os.path.join(CurDir, "ttitrace*%s.dat" % dsp_id_DL)
            ttiTrace_UL_pattern = os.path.join(CurDir, "ttitrace*%s.dat" % dsp_id_UL)

            command_DL_7up = SevenUpexe + " --fsm r3:1 --fsp 1 --syscom tcptunnel -T 0x" + dsp_id_DL
            command_UL_7up = SevenUpexe + " --fsm r3:1 --fsp 1 --syscom tcptunnel -T 0x" + dsp_id_UL

            clean_dat_file(ttiTrace_DL_pattern)
            clean_dat_file(ttiTrace_UL_pattern)

            # download dl dat
            os.system(command_DL_7up)
            ttiTrace_DL_list = glob.glob(ttiTrace_DL_pattern)
            if len(ttiTrace_DL_list) == 1:
                shutil.move(ttiTrace_DL_list[0], ttiTrace_DL_path)
            else:
                raise Exception, "[ERR]7up download DL ttiTrace fail!"

            # download ul dat
            os.system(command_UL_7up)
            ttiTrace_UL_list = glob.glob(ttiTrace_UL_pattern)
            if len(ttiTrace_UL_list) == 1:
                shutil.move(ttiTrace_UL_list[0], ttiTrace_UL_path)
            else:
                raise Exception, "[ERR]7up download UL ttiTrace fail!"

        elif str(tool_Type).strip().upper() == 'SICFTP':
            command_DL_SicFtp = "%s -g -c %s -o \"%s\"" % (sicftp, dsp_id_DL, ttiTrace_DL_path)
            os.system(command_DL_SicFtp)
            command_UL_SicFtp = "%s -g -c %s -o \"%s\"" % (sicftp, dsp_id_UL, ttiTrace_UL_path)
            os.system(command_UL_SicFtp)

        else:
            raise Exception, "[ERR]TtiTrace tool %s doesn't recognize!" % tool_Type

        # check dl dat
        if os.path.getsize(ttiTrace_UL_path) != 0:
            print "[INF]Download UL_TtiTrace from %s success! -> %s" % (dsp_id_DL, ttiTrace_DL_path)
        else:
            raise Exception, "[ERR]Download UL ttiTrace success but dat size = 0!"

        # check ul dat
        if os.path.getsize(ttiTrace_DL_path) != 0:
            print "[INF]Download DL_TtiTrace from %s success! -> %s" % (dsp_id_DL, ttiTrace_DL_path)
        else:
            raise Exception, "[ERR]Download DL ttiTrace success but dat size = 0!"

    except Exception, p_Err:
        raise Exception, "[ERR]Download ttiTrace fail because of %s!" % p_Err

def get_mac_ttitrace(dsp_id_DL, dsp_id_UL, ttiTrace_DL_path, ttiTrace_UL_path, tool_Type = 'SICFTP'):
    """This keyword start sicftp, generate mac TTI Trace file
    | Input Parameters  | Man. |  Description                |
    | dsp_id_DL         | Yes  |  FSP and Faraday id in DL   |
    | dsp_id_UL         | Yes  |  FSP and Faraday id in UL   |
    | ttiTrace_DL_path  | Yes  |  DL Trace log path          |
    | ttiTrace_UL_path  | Yes  |  UL Trace log path          |

    Example
    | get mac ttitrace | '1243' | '1262' | 'd:\\ttiTraceDL_20111201203759.dat' | 'd:\\ttiTraceUL_20111201203759.dat' |
    """
    for retry_time in xrange(3):
        try:
            _get_mac_ttitrace_once(dsp_id_DL, dsp_id_UL, ttiTrace_DL_path, ttiTrace_UL_path, tool_Type)
            return True
        except Exception, p_Err:
            print "[ERR]Get TtiTrace fail for %s time, retry in 3 sec." % (retry_time + 1)
            print p_Err
            time.sleep(3)

    raise Exception, "[ERR]Get TtiTrace fail because retry times exceed threshold!"

def get_trace_level(bin_Tracelog, case_Directory):
    """This keyword check trace log and return it's level
    | Input Parameters | Man. | Description
    | bin_Tracelog     | Yes  | Name of the binary trace file |
    | case_Directory   | Yes  | The absolute path of the case |

    return value:
    level  1:   DL low
    level  2:   DL med
    level  3:   DL high
    level 14:   UL low
    level 15:   UL med
    level 16:   UL high

    Example
    | get trace level | "DLttiTrace.dat" | "D:\\TTITrace\\ta test" |
    """

    traceLevel      = 0
    tempfile        = os.path.join(case_Directory, "trace.level")
    bin_Tracelog    = os.path.join(case_Directory, bin_Tracelog)
    traceParserPath = os.path.join(toolPath, "BinaryFileParser")
    traceParserTool = os.path.join(traceParserPath, "tti_trace_parser.exe")

    if os.path.isfile(bin_Tracelog):
        cmd_GetTraceLevel = traceParserTool + " " + '"' + bin_Tracelog + '"' + " CHECK > " + '"' + tempfile + '"'
        print "*************************************************"
        print cmd_GetTraceLevel
        print "*************************************************"
        os.system("\"" + cmd_GetTraceLevel + "\"")
    else:
        raise Exception, "[ERR]Trace bin log does not exist!"

    try:
        fopen = open(tempfile, 'r')
        content = fopen.readlines()
    except:
        print "[ERR]open trace level log failed!"

    finally:
        fopen.close()
        os.remove(tempfile)

    for line in content:
        if "Trace Level" in line:
            traceLevel = int(string.split(line,' ')[3])
            break

    return traceLevel

def choose_config(bin_Tracelog, case_Directory):
    """This keyword choose configure file according to get_trace_level
    | Input Parameters | Man. | Description                             |
    | bin_Tracelog     | Yes  | Name of the binary trace file           |
    | case_Directory   | Yes  | The absolute path of the case           |

    | return value | if pass, return the absolute path of configure file |

    Example
    | choose config | "DLttiTrace.dat" | "D:\\TTITrace\\ta test" |
    """
 
    configFile      = ""
    tool_ConfigPath = os.path.join(toolPath, "BinaryFileParser")
    traceLevel      = get_trace_level(bin_Tracelog, case_Directory)

    if traceLevel < 0:
        raise Exception, "[ERR]Decode error! traceLevel < 0"

    elif traceLevel == 0:
        raise Exception, "[ERR]Cannot decode trace level! traceLevel == 0"

    elif traceLevel == 1:
        print "[INFO]Trace Level = DL Low!"
        configFile = os.path.join(tool_ConfigPath,"dl_low_config.txt")

    elif traceLevel == 2:
        print "[INFO]Trace Level = DL Medium!"
        configFile = os.path.join(tool_ConfigPath,"dl_medium_config.txt")

    elif traceLevel == 3:
        print "[INFO]Trace Level = DL High!"
        configFile = os.path.join(tool_ConfigPath,"dl_high_config.txt")

    elif traceLevel == 14:
        print "[INFO]Trace Level = UL Low!"
        configFile = os.path.join(tool_ConfigPath,"ul_low_config.txt")

    elif traceLevel == 15:
        print "[INFO]Trace Level = UL Medium!"
        configFile = os.path.join(tool_ConfigPath,"ul_medium_config.txt")

    elif traceLevel == 16:
        print "[INFO]Trace Level = UL High!"
        configFile = os.path.join(tool_ConfigPath,"ul_high_config.txt")

    else:
        raise Exception, "[ERR]Trace level is out of range!"

    if os.path.isfile(configFile):
        return configFile

    else:
        raise Exception, "[ERR]Config file '%s' doesn't exist!" % configFile

def trace_parser(bin_Tracelog, ascii_Tracelog, configFile, case_Directory):
    """This keyword parse bin file, result will be stored in ASCII file
    | Input Parameters | Man. | Description                            |
    | bin_Tracelog     | Yes  | Name of the binary trace file          |
    | ascii_Tracelog   | Yes  | Name of resulting ASCII file           |
    | configFile       | Yes  | Name of resulting config file          |
    | case_Directory   | Yes  | The absolute path of the case          |

    Example
    | trace parser | "DLttiTrace.dat" | "tti_results.txt" | return value of choose_config | "D:\\TTITrace\\ta test" |
    """

    bin_Tracelog    = os.path.join(case_Directory, bin_Tracelog)
    tempfile        = os.path.join(case_Directory, "traceParserTemp.log")
    traceParserPath = os.path.join(toolPath, "BinaryFileParser")
    traceParserTool = os.path.join(traceParserPath, "tti_trace_parser.exe")
    cmd_Parser      = traceParserTool + " " + '"' + bin_Tracelog + '"' + " " + \
                      '"' + ascii_Tracelog + '"' + " > " +'"' + tempfile + '"'
    print "==============================================="
    print cmd_Parser
    print "==============================================="
    os.system("\"" + cmd_Parser + "\"")

    if os.path.isfile(tempfile):
        os.remove(tempfile)

    logfile = os.path.join(case_Directory, ascii_Tracelog)
    print "----------------------------------------------"
    print logfile
    print "----------------------------------------------"
    if os.path.isfile(logfile):
        print "[INFO]Parse binary tracelog successfully!"
        return True
    else:
        raise Exception, "[ERR]Parse binary tracelog failure!"

def trace_converter(ascii_Tracelog, OutputCsv, configFile, case_Directory, FilterPath=""):
    """This keyword parse ASCII file, result will be stored in .csv file
    | Input Parameters | Man. | Description                             |
    | ascii_Tracelog   | Yes  | Name of ASCII file                      |
    | OutputCsv        | Yes  | Name of resulting csv file              |
    | configFile       | Yes  | Name of resulting config file           |
    | case_Directory   | Yes  | The absolute path of the case           |
    | FilterPath       | no   | Name of filter file, optional           |

    Example
    | trace converter | "tti_results.txt" | "ttiTrace.csv" | return value of choose_config | "D:\\TTITrace\\ta test" |
    """

    tempfile               = os.path.join(case_Directory, "traceConverterTemp.log")
    TraceConverterPath     = os.path.join(toolPath, "TraceConverter")
    tool_TtiTraceConverter = os.path.join(TraceConverterPath, "TtiTraceConverter.pl")
    ascii_Tracelog         = os.path.join(case_Directory, ascii_Tracelog)
    FilterPath             = os.path.join(case_Directory, FilterPath)

    if os.path.isfile(FilterPath):
        cmd_Converter = "perl " + '"' + tool_TtiTraceConverter + '"' + " " + '"' + ascii_Tracelog + '"' + " " + '"' + configFile \
                        + '"' + " " + '"' + OutputCsv + '"' + " " + '"' + FilterPath + '"' + " > " + '"' + tempfile + '"'

    else:
        cmd_Converter = "perl " + '"' + tool_TtiTraceConverter + '"' + " " + '"' + ascii_Tracelog + '"' + " " \
                        + '"' + configFile + '"' + " " + '"' + OutputCsv + '"' + " > " + '"' + tempfile + '"'
    print "++++++++++++++++++++++++++++++++++++++++++++++++++"
    print cmd_Converter
    print "++++++++++++++++++++++++++++++++++++++++++++++++++"
    os.chdir(TraceConverterPath)
    os.system("\"" + cmd_Converter + "\"")

    if os.path.isfile(tempfile):
       os.remove(tempfile)

    logfile = os.path.join(case_Directory, OutputCsv)
    if os.path.isfile(logfile):
        print "[INFO]Generate CSV file",OutputCsv,"successfully!"
        return True
    else:
        raise Exception, "[ERR]Generate CSV file '%s' failed!" % OutputCsv

def ttitrace_decoder(bin_Tracelog, csv_Resultfile, case_Directory):
    """This keyword run trace_parser and trace_converter, get .csv file
    | Input Parameters | Man. | Description                                |
    | bin_Tracelog     | Yes  | Name of the binary trace file              |
    | csv_Resultfile   | Yes  | Name of resulting csv file                 |
    | case_Directory   | Yes  | The absolute path of the case              |
    | FilterPath       | no   | Name of filter file, optional              |

    Example
    | ttitrace decoder | DLttiTrace.dat | ttiTrace.csv | "D:\\TTITrace\\ta test" |
    """

    ascii_Tracelog     = os.path.join(case_Directory, "ascii_Trace.log")
    csv_Resultfile     = os.path.join(case_Directory, csv_Resultfile)
    bin_Tracelog       = os.path.join(case_Directory, bin_Tracelog)

    traceParserPath = os.path.join(toolPath, "BinaryFileParser")
    traceParserTool = os.path.join(traceParserPath, "DevC_tti_trace_parser.exe")

    if os.path.isfile(ascii_Tracelog):
        os.remove(ascii_Tracelog)

    if os.path.isfile(csv_Resultfile):
        os.remove(csv_Resultfile)
        
    decode_cmd = traceParserTool  + ' "' + bin_Tracelog + '" "' +csv_Resultfile + '" > "' + ascii_Tracelog + '"'
    print decode_cmd
    os.system(decode_cmd)

#    configFile = choose_config(bin_Tracelog, case_Directory)
#    if not configFile:
#        raise Exception, "There is no *.dat trace log file!"
#    
#    if not trace_parser(bin_Tracelog, ascii_Tracelog, configFile, case_Directory):
#        raise Exception, "Trace parser failed!"
#
#    if not trace_converter(ascii_Tracelog, csv_Resultfile, configFile, case_Directory, FilterPath):
#        raise Exception, "Trace convert failed!"

    if os.path.isfile(ascii_Tracelog):
        os.remove(ascii_Tracelog)

    if os.path.isfile(os.path.join(case_Directory, "%s.harq" %csv_Resultfile)):
        os.remove(os.path.join(case_Directory, "%s.harq" %csv_Resultfile))


def download_ttitrace_tool_from_svn(MacVersion):
    """This keyword download tti trace tools from svn according to mac version.

    | Input Parameters | Man. | Description |
    | MacVersion       | Yes  | MAC version |

    Example
    | download_ttitrace_tool_from_svn | 'LNT2.0_MAC_0001_026_00' |
    """

    ParseTool     = 'https://svne1.access.nokiasiemensnetworks.com/isource/svnroot/BTS_SC_MAC_PS_TDD/tags/%s/C_Test/SC_MAC/TtiTracer/ExcelTraceAnalyzerTool/BinaryFileParser' %(MacVersion)
    ConverterTool = 'https://svne1.access.nokiasiemensnetworks.com/isource/svnroot/BTS_SC_MAC_PS_TDD/tags/%s/C_Test/SC_MAC/TtiTracer/ExcelTraceAnalyzerTool/TraceConverter' %(MacVersion)
    IniFileDict   = { 'BinaryFileParser_SVN_ADDR': ParseTool,
                      'TraceConverter_SVN_ADDR': ConverterTool }

    # Check out TtiTrace file in resources\tools\TTITrace
    os.chdir(toolPath)
    cmd  = 'svn checkout ' + IniFileDict.get('BinaryFileParser_SVN_ADDR')
    print cmd
    os.system(cmd)

    cmd  = 'svn checkout ' + IniFileDict.get('TraceConverter_SVN_ADDR')
    print cmd
    os.system(cmd)

def get_macttitrace_with_command(dat_file_path, core_input, times, gap, prompt = 'Ok'):
    """This keyword is used to get macttitrace with command in aashell then sftp download to local pc

    | Input Parameters    | Man. | Description |
    | dat_file_path       | Yes  | the directory where you want to store dat file |
    | core_input          | Yes  | core or core list you want to get macttitrace  |
    | times               | Yes  | how many times you want to get macttitrace     |
    | gap                 | Yes  | time sleep among each times to get macttitrace |
    | prompt              | Yes  | the prompt when send get macttitrace comand finished,default is 'Ok'|

    Example
    | get_macttitrace_with_command | 'd:\\logs' | '1231' | '2' | '5' |
    ${core_list} = Creat List | '1231' | '1234' | '1331' | '1334' |
    | get_macttitrace_with_command | 'd:\\logs' | core_list | '3' | '3' |
    """

    ip = "192.168.255.1"
    port = 22
    username = "toor4nsn"
    passwd = "oZPS0POrRieRtu"
    logname_list = []
    core_list = []
    flag = False
    
    # capture macttitrace log to /ram
    if not isinstance(core_input, list):
        core_list.append(core_input)
    else:
        core_list = core_input

    for core in core_list:
        for i in range(0, int(times)): # remove dat file before get it
            remove_file = 'rm -rf /ram/' + str(core) + 'macttitrace_aashell' + str(i) + '.dat'
            connections.execute_ssh_command_without_check(remove_file)
            print "remove file: %s ok" % (remove_file.split("rm -rf /ram/")[-1])
        
    try:
        if connections.login_aashell():
            try:
                for core in core_list:
                    for i in range(0, int(times)):
                        log_name = ''
                        cmd = 'file -g 0x' + str(core) + ' /ram/ttiTraceHb.dat /ram/' + str(core) + 'macttitrace_aashell' + str(i) + '.dat'
                        log_name = str(core) + 'macttitrace_aashell' + str(i) + '.dat'
                        connections.execute_aashell_command(cmd, prompt)
                        time.sleep(int(gap))
                        logname_list.append(log_name)
                print "PASS:capture macttitrace from aashell successfully!\n"
            finally:
                connections.exit_aashell('root@FCTB:~ >')
        else:
            print "login aashell failed!"

    except:
        print "Fail:capture macttitrace from aashell failed!\n"
    finally:
        if len(logname_list) == int(times)*len(core_list):
            print 'all macttitrace gethered ok!'

    # download macttitrace to local pc

    if len(logname_list)>0:
        print "Gether log from aashell is over,get log from eNB to local starting...."
        if not os.path.isdir(dat_file_path):
            print "%s is not existed!" % (dat_file_path)
        else: 
            for i in logname_list: 
                host_dir = '/ram'
                host_file_name = i
                local_file = os.path.join(dat_file_path, i);
                sftp_download(ip, port, username, passwd, local_file, host_file_name, host_dir)
            print "get macttitrace is finished,please check!"
            flag = True
    else:
        print 'there is no ttitrace gethered in eNB,pls check and try again!\n'

    return flag, logname_list

if __name__=='__main__':
##    get_mac_ttitrace('1231', '1234', \
##                           'DLttiTrace.dat', \
##                           'ULttiTrace.dat')
    #print get_trace_level('20M_1_7_dl.dat', 'D:\\TTITrace\\tatest')
    #print choose_config('20M_1_7_dl.dat', 'D:\\TTITrace\\tatest')
    print ttitrace_decoder('DLttiTrace.dat', 'dlttiTrace.csv', 'E:\\')
    print ttitrace_decoder('ULttiTrace.dat', 'ulttiTrace.csv', 'E:\\')
    #download_ttitrace_tool_from_svn('LNT1.0_MAC_1010_013_00')
    pass
