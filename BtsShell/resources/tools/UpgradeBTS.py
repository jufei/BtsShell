# -*- coding: utf-8 -*-
##from os.path import join,getsize
import os
import sys
import types
import traceback
import re
import time
import random
import string
import win32com.client

from BtsShell import connections
#from BtsShell.file_lib.common_operation import *
from BtsShell.application_lib.process import kill_process
from BtsShell.application_lib.testpartner_qtp import *
from BtsShell.file_lib.BTS_file_control import get_active_sw_version
from BtsShell.application_lib.sftp import *
from BtsShell.common_lib.get_path import *
import subprocess
import shutil

QTP_LICENSE_ERROR = "QTP run failed for special reason!"
COMM_PATH = os.path.join(os.path.dirname(get_btsshell_path()),"QTP", "RL35", "QTPScripts95_TDD_Prod","SiteMan")
logindir = os.path.join(COMM_PATH, 'Login')
btsdir = os.path.join(COMM_PATH, 'SiteMan_MenuOperation')
sitemandir = os.path.join(COMM_PATH, 'InstallSeMApplication')
resetbtsdir = os.path.join(COMM_PATH, 'ResetSite')
checkbtsdir = os.path.join(COMM_PATH, 'WaitFor_FinalState_BTS')

def _parse_qtp_last_error(src_file):
    try:
        tree = etree.parse(open(src_file, "rb"))
    except:
        raise Exception, "Open '%s' file failed!" % src_file
    step_id = None
    record_step_id = []
    troot = tree.getroot()
    for root in troot:
        for son in root.iter():
            if ("Summary" == son.tag):
                last1_step = son.getprevious()
                last2_step = last1_step.getprevious()
                last3_step = last2_step.getprevious()
                last3_step_info = etree.tostring(last3_step)
                last2_step_info = etree.tostring(last2_step)
                last1_step_info = etree.tostring(last1_step)
                break

    #both "Stop action replay" or "Stop Run" detail include "Run stopped by user"
    if 0 <= last1_step_info.find("stopped by user") :
        last2_fail_info = re.findall("<Details.*>(.*)</Details>", last2_step_info)
        last3_fail_info = re.findall("<Details.*>(.*)</Details>", last3_step_info)
        last2_fail_info2 = re.findall("<Details.*>(.*)", last2_step_info)
        last3_fail_info2 = re.findall("<Details.*>(.*)", last3_step_info)
        tmp = ""
        if last3_fail_info :
            tmp +=  last3_fail_info[-1]+"\n"
        elif last3_fail_info2:
            tmp +=  last3_fail_info2[-1]+"\n"

        if last2_fail_info:
            tmp +=  last2_fail_info[-1]
        elif last2_fail_info2:
            tmp +=  last2_fail_info2[-1]


        status = re.search(".*NodeArgs.*status=(.*)>", last2_step_info)
        if status:
            sta = status.groups()[0].strip("\"")
            if "Failed" == sta:
                #raise Exception, "QTP run failed! "
                raise Exception, tmp
    else:
        status = re.search(".*NodeArgs.*status=(.*)>", last1_step_info)
        if status:
            sta = status.groups()[0].strip("\"")
            if "Failed" == sta:
                raise Exception, "QTP step run failed!"


def _run_qtp_once_python(test_dir,log_save_dir,mod_para_list,keep_qtp_open,timeout):
    image_log = "LogPath=%s\\" % log_save_dir
    mod = []
    mod.append(image_log)
    if None == mod_para_list:
        modify = mod
    elif isinstance(mod_para_list, list):
        modify = mod + mod_para_list
    else:
        raise Exception, "3rd parameter is not 'None' or 'list'"

    write_parameters_to_file_for_tp(modify, "c:\\qtp_para.txt")
    log_save_dir = log_save_dir + "\qtp_log" + time.strftime("%Y%m%d%H%M%S")

    #Check script existence
    if not os.path.isdir(test_dir):
        raise Exception, "<QTP> Test script %s does not exists" % (test_dir)
    else:
        print '<QTP> Test %s is existence.'%(test_dir)
    try:
        qApp = win32com.client.DispatchEx("QuickTest.Application")              #As QuickTest.Application ' Declare the Application object variable
        if qApp == None:
            raise Exception, "<QTP> instanciation was Failed"
        else:
            print "<QTP> instanciation was SUCCESSFUL!"
        qApp.Open(test_dir)  #open QTP script
        qtest = qApp.Test
        if qtest == None:
            raise Exception, " <QTP> automated test case open was Failed!."
        else:
            print "<QTP> automated test case open was SUCCESSFUL!"
        qApp.Launch()  #Start QuickTest
        qApp.Visible = True  #Make the QuickTest application visible
        qdefcoll = qApp.Test.ParameterDefinitions  #As QuickTest.ParameterDefinitions ' Declare a Parameter Definitions collection
        rtparas = qdefcoll.GetParameters()  #As QuickTest.Parameters ' Declare a Parameters collection
     	try:
            print '<QTP> Parameter as below:'
            for para in modify:
                tmp = para.split("=")
                print tmp[0].strip()+":"+tmp[1].strip()
                rtpara = rtparas.Item(tmp[0].strip())  #Retrieve a specific parameter.
                rtpara.Value = tmp[1].strip()  #Change the parameter value.
        except Exception,e:
            print e
            #traceback.print_exc()
            raise Exception, "<QTP> Set Parameter value error"
        result_dir = log_save_dir

        qoptions = win32com.client.DispatchEx("QuickTest.RunResultsOptions")    #As QuickTest.RunResultsOptions ' Declare a Run Results Options object variable
        qoptions.ResultsLocation = result_dir
        #runresult = qtest.Run(qoptions,True,rtparas)

        print '<QTP> Save log to %s'%(os.path.join(result_dir, "Report"))
        try:
            runresult = qtest.Run(qoptions,True,rtparas)
        except Exception, e:
            print e
            #traceback.print_exc()
            raise Exception, "<QTP> Run QTP Test error"

        result = qtest.LastRunResults.Status
        if str(result).lower() == 'failed':
            error_info = ""
            error_info = _parse_qtp_last_error(os.path.join(result_dir, "Report", "Results.xml"))
            raise Exception," Test failed %s"%(error_info)
    #except:
    #    traceback.print_exc()
    finally:
        if keep_qtp_open == "N":
            if qApp <> None:
                qApp.Quit()
                qApp = None


def run_qtp_python(test_dir, log_save_dir="c:\\tmp", mod_para_list=None, keep_qtp_open="N", timeout="300"):
    """This keyword used for run qtp script, if you use in robot please select run_qtp_script

    | Input Parameters  | Man. | Description |
    | test_dir      | Yes  | Path of qtp test case  |
    | log_save_dir   | No  | Save directory for qtp log |
    | mod_para_list    | No   | Parameters need to modified, need be a list or None |

    Example

    | run_qtp  |  config.xml  |
     """
    try:
        _run_qtp_once_python(test_dir, log_save_dir, mod_para_list, keep_qtp_open, timeout)
    except QTP_LICENSE_ERROR:
        kill_qtp_process()
        time.sleep(random.randint(60, 120))
        _run_qtp_once_python(test_dir, log_save_dir, mod_para_list, keep_qtp_open, timeout)
    except Exception, e:
        print e
        #traceback.print_exc()
        raise "run_qtp_python error"


def auto_upgrade_sw(btssw_dir,smsw_dir,log_save_dir):
     """This keyword used for upgrade BTS and BTS Site Manager software version

    | Input Parameters  | Man. | Description |
    | btssw_dir         | Yes  | Path of BTS software version file  |
    | smsw_dir          | Yes  | Path of BTS Site Manager software version install file |
    | log_save_dir      | No   | Save directory for qtp log |


    Example

    | @{btssw_dir} | d:\\rl35\\LNT3.0_ENB_1210_016_00\\LNT3.0_ENB_1210_016_00_release_BTSSM_downloadable_wo_images.zip |
    | @{smsw_dir} | d:\\rl35\\BTSSiteEM-TD-LTE30-1210_004_00.exe |
    | @{log_save_dir} | d:\\test\\log |
    | auto upgrade sw  | ${btssw_dir} | ${smsw_dir} | ${log_save_dir} |
     """

     print '--------------------------- Start Login BTS Site Manager ----------------------------------'
     
     loginpara = ['IPAddress=Local','UserName=Nemuadmin','Password=nemuuser']
     run_qtp_python(logindir,log_save_dir,loginpara)
     print '--------------------------- Login BTS Site Manager Pass ----------------------------------'
##
##     print '--------------------------- Start Check BTS On air ----------------------------------'
##     
##     checkbtspara = ['TargetOperState=On air','TargetBlockingState=Unblocked']
##     run_qtp_python(checkbtsdir,log_save_dir,checkbtspara)
##     print '--------------------------- Check BTS On air Pass ----------------------------------'

     print '--------------------------- Start Upgrade BTS Version ----------------------------------'
     
     btspara = ['MenuName=Software:Update SW to BTS Site...','OperationName=UpdateSWToBTS','JEditName='+btssw_dir,'JEditValue=']
     run_qtp_python(btsdir,log_save_dir,btspara)
     print '--------------------------- Upgrade BTS Version Pass ----------------------------------'

     print '--------------------------- Start Install new BTS Site Manager Version ----------------------------------'
     
     sitemanpara = ['ApplicationPath='+smsw_dir,'InstallMode=Clean']
     run_qtp_python(sitemandir,log_save_dir,sitemanpara)
     print '--------------------------- Install new BTS Site Manager Version Pass ----------------------------------'

def check_bts_state_before_upgrade(log_save_dir):
    print '--------------------------- Start Login BTS Site Manager ----------------------------------'
    
    loginpara = ['IPAddress=Local','UserName=Nemuadmin','Password=nemuuser']
    run_qtp_python(logindir,log_save_dir,loginpara)
    print '--------------------------- Login BTS Site Manager Pass ----------------------------------\n'

    print '--------------------------- Start Check BTS On air ----------------------------------'
    
    checkbtspara = ['TargetOperState=On air','TargetBlockingState=Unblocked']
    try:
        run_qtp_python(checkbtsdir,log_save_dir,checkbtspara)
        print '--------------------------- Check BTS On air Pass ----------------------------------\n'
    except:
        #traceback.print_exc()
        print '--------------------------- Start Resite BTS ----------------------------------'
        
        resetbtspara = []
        run_qtp_python(resetbtsdir,log_save_dir,resetbtspara)
        print '--------------------------- Resite BTS Pass ----------------------------------\n'
        print '--------------------------- Start Login BTS Site Manager ----------------------------------'
        run_qtp_python(logindir,log_save_dir,loginpara)
        print '--------------------------- Login BTS Site Manager Pass ----------------------------------\n'
        print '--------------------------- Start Check BTS On air Again----------------------------------'
        run_qtp_python(checkbtsdir,log_save_dir,checkbtspara)
        print '--------------------------- Check BTS On air Pass ----------------------------------\n'


def StartUDPLog(logpath):
    try:
        root = os.path.dirname(sys.argv[0])
        BtsLogger = os.path.join(root, "BtsLogger.exe")
        if os.path.exists(BtsLogger):
            cmd = "%s %s" %(BtsLogger, logpath)
        else:
            return "ERROR"
        s = subprocess.Popen(cmd)
        if s.poll() == None:
            return s.pid
        print "cmd \"%s\" run is not startup..." %cmd
        return "ERROR"
    except :
        traceback.print_exc()
        return


def StopUDPLog(pid):
    try:
        if pid != "ERROR":
            os.system("taskkill /f /t /pid %s" %pid)
            os.system("taskkill /f /im BtsLogger.exe")
    except :
        traceback.print_exc()
        pass

RelColPath = "\\\\10.68.160.99\\trunk_rl45"

def GetBtsAndSMSWPath(CurRelName):
    NewRelPath = "%s\\NewRelInfo_TRUNK_RL45.ini" % RelColPath
    print "NewRelPath=%s"%NewRelPath

    try:
        f = open(NewRelPath, 'r')
        CurRels = [item.replace('\r','').replace('\n','').split(" ") for item in f.readlines()]
        print CurRels
    except Exception ,e:
        print "Error with info: \"%s\"" % e
    finally:
        f.close()

    for Rel in CurRels:
        print Rel
        if Rel[0] == CurRelName:
            CurSMName = Rel[1]

    if CurSMName:
        CurRelPath = "%s\\%s\\%s_release_BTSSM_downloadable_wo_images.zip" %(RelColPath, CurRelName, CurRelName)
        CurSMPath =  "%s\\%s" %(RelColPath, CurSMName)

    return (CurRelPath, CurSMPath)

def CopySW2Local(swpath):
    tarpath = "C:\\BTSSW"
    if not os.path.exists(tarpath):
        os.mkdir(tarpath)
    try:
        shutil.copy(swpath, tarpath)
        tarswpath = os.path.join(tarpath, os.path.basename(swpath))
        if os.path.exists(tarswpath):
            return tarswpath
    except:
        traceback.print_exc()
        return swpath


def printUsage():
    print """
----------------------------------------------------------------------
This script is used for upgrade BTS and sitemanage automatilly.
    usage:
        python %s TrunkRelName WORKSPACE
----------------------------------------------------------------------
""" % os.path.basename(sys.argv[0])


def backup_bts_file_to_local(file_save_dir="c:\\Flash_bak",username="toor4nsn",password="oZPS0POrRieRtu"):
    """ This keyword used for backup BTS file to local
    | Input Parameters  | Man. | Description |
    | file_save_dir     | No   | default value is "c:\\Flash_bak"  |
    | username          | No   | default value is "toor4nsn" for BTS   |
    | password          | No   | default value is "oZPS0POrRieRtu" for BTS |


    Example

    | backup bts file to local  |
    | backup bts file to local  |
    """
    os.system(r"wget.exe --user=Nemuadmin --password=nemuuser --no-check-certificate https://192.168.255.129/protected/enableSsh.cgi -t 1 --timeout=10 -q -O -")
    sw_version = get_active_sw_version()
    Flash_dir = file_save_dir
    if not os.path.exists(Flash_dir):
        os.mkdir(Flash_dir)
    CurVerDir = os.path.join(Flash_dir, sw_version)
    if not os.path.exists(CurVerDir):
        os.mkdir(CurVerDir)
    print "------------------------ Start Backup BTS file to %s ---------------------------------"%CurVerDir
    sftp_download_deep("192.168.255.129", "22", "toor4nsn", "oZPS0POrRieRtu", CurVerDir, ".*", "/flash")
    ##os.system(r"pscp -r -pw oZPS0POrRieRtu -scp toor4nsn@192.168.255.129:/flash %s" % CurVerDir)
    print "------------------------ Backup BTS file successfully -------------------------------- "


##def upgrade_bts(CurRelName,WSPath):
##    print CurRelName
##    print WSPath
##    backup_bts_file_to_local()
##    print """
##==========================CurRelName=================================
##    %s
##=======================================================================
##""" %CurRelName
##    BtsSWPath, SMSWPath = GetBtsAndSMSWPath(CurRelName)
##    SMSWPath = CopySW2Local(SMSWPath)
##    BtsSWPath = CopySW2Local(BtsSWPath)
##    print """
##-------------------------Start to upgrade---------------------------------
##BtsSWPath is: \"%s\"
##SMPath is: \"%s\"
##LogPath is: \"%s\"
##--------------------------------------------------------------------------
##""" %(BtsSWPath, SMSWPath, WSPath)
##
##    check_bts_state_before_upgrade(WSPath)
##    p = StartUDPLog(WSPath)
##    try:
##        auto_upgrade_sw(BtsSWPath,SMSWPath,WSPath)
##    except:
##        traceback.print_exc()
##        raise "Error happened when on \"auto_upgrade_sw\".."
##    StopUDPLog(p)


if __name__ =="__main__":
    try:
        backup_bts_file_to_local()
    except Exception,e:
        print e



    args = sys.argv[1:]
    if len(args) != 2:
        printUsage()
        sys.exit(1)
    CurRelName = args[0].strip()
    WSPath = args[1].strip()
    print """
==========================CurRelName=================================
    %s
=======================================================================
""" %CurRelName
    BtsSWPath, SMSWPath = GetBtsAndSMSWPath(CurRelName)
    SMSWPath = CopySW2Local(SMSWPath)
    BtsSWPath = CopySW2Local(BtsSWPath)
    print """
-------------------------Start to upgrade---------------------------------
BtsSWPath is: \"%s\"
SMPath is: \"%s\"
LogPath is: \"%s\"
--------------------------------------------------------------------------
""" %(BtsSWPath, SMSWPath, WSPath)

##    check_bts_state_before_upgrade(WSPath)
    print "------------------------- start UDP log to %s-------------------------"%WSPath
    p = StartUDPLog(WSPath)
    try:
        auto_upgrade_sw(BtsSWPath,SMSWPath,WSPath)
    except:
        traceback.print_exc()
        raise "Error happened when on \"auto_upgrade_sw\".."
    finally:
        StopUDPLog(p)
        print "------------------------- Stop UDP log sucessfully-------------------------"

    #checkbtsstate(log_save_dir)


