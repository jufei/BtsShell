import os
import sys
import time
import re
from BtsShell import connections
from BtsShell.common_lib.get_path import *

psexecPath = os.path.join(get_tools_path(), "psexec.exe")

def SevenUp_Start(Logfile, logDirectory, faraday_core, TraceSwitch = "true", UdpSwitch = "false"):
    """This keyword run 7up.exe, get IDA log.
    | Input Parameters | Man. | Description                   |
    | Logfile          | Yes  | Trace log's name              |
    | logDirectory     | Yes  | The path of log               |
    | faraday_core     | Yes  | Faraday Core                  |
    | TraceSwitch      | Yes  | Default is true, trace log on |
    | sleep_time       | Yes  | 7up.exe running time          |
    | UdpSwitch        | no   | true: udp log on              |
                              | false: udp log off            |
                              | default is false              |

    Example
    | SevenUp_Start | 'tracelog.log' | ${CURDIR} | '1431:210b' | 'true' |
    """

    #default params
    SevenUpexe = os.path.join(get_tools_path(), "7UP", "7up.exe")
    configfile = os.path.join(get_tools_path(), "7UP", "Config_UDP_Off", "7up.ini")
    Logfile    = os.path.join(logDirectory, Logfile)

    #UDPlog on or off
    if UdpSwitch == "false":
        pass
    elif UdpSwitch == "true":
        configfile = os.path.join(get_tools_path(), "7UP", "Config_UDP_On", "7up.ini")
    else:
        raise Exception, "ERR/: the second cmd line param %s is error" % UdpSwitch

    #Tracelog on or off and generate command
    if TraceSwitch == "false":
        command = '%s -C %s -U "%s"' %(SevenUpexe, configfile, Logfile)
    elif TraceSwitch == "true":
        command = '%s -C %s -U "%s" -I %s' %(SevenUpexe, configfile, Logfile, faraday_core)
    else:
        raise Exception, "ERR/: the third cmd line param %s is error" % TraceSwitch

    #execute command
    command = psexecPath + " -i -d " + command
    connections.execute_shell_command_without_check(command)

def Fled_Start(Logfile, logDirectory, sackfile_BigEndian, sackfile_LowEndian):
    """This keyword run fled.exe, decode Ida log.
    | Input Parameters   | Man. | Description           |
    | Logfile            | Yes  | Trace log's name      |
    | logDirectory       | Yes  | The path of log       |
    | sackfile_BigEndian | Yes  | Big endian sack file  |
    | sackfile_LowEndian | Yes  | Low endian sack file  |

    Example
    | Fled_Start | ${Log_name} | ${TARGET LOG DIRECTORY} | ${BigEndian_Sack} | ${LowEndian_Sack} |
    """

    #default params
    fledexe  = os.path.join(get_tools_path(), "7UP", "fled.exe")
    Logfile  = os.path.join(logDirectory, Logfile)

    #log file exist or not and generate command
    if os.path.isfile(Logfile) and os.path.getsize(Logfile) > 0:
        # Pre-process 7up log
        KeyWord = ['TUP','MAC','PHY']
        LogFileObj1 = open(Logfile, 'r')
        Content = LogFileObj1.readlines()
        Post_Content = Content[0:-10]
        Post_Content_Temp = Post_Content[:]
        for line in Post_Content_Temp:
            if all([kw not in line for kw in KeyWord]):
                Post_Content.remove(line)
            else:
                pass
        LogFileObj1.close()
        LogFileObj2 = open(Logfile, 'w')
        LogFileObj2.writelines(Post_Content)
        LogFileObj2.close()

        #generate command
        command = fledexe + " -f native_le32" + " -S " + \
                  sackfile_BigEndian + ":" + sackfile_LowEndian + " -U " + '"' + Logfile + '"'

        #execute command
        print command
        os.chdir(logDirectory)
        statue = os.system(command)
        print "INF/: the statue is %s" % str(statue)
        if int(statue) == 0:
            print "INF/: execute %s OK" % command
        else:
            raise Exception, "ERR/: execute %s fail" % command
    else:
        raise Exception, "ERR/: there is no valid logfile %s, 7up fail to get tracelog" % Logfile


if __name__ == '__main__':
    #print SevenUp_Start('tracelog.log', 'E:\\7up_FSM2', '1431:210b')
    pass


