import os
import re
import time
import random
import inspect
import platform
import glob
##import win32api, win32pdhutil, win32con
##import win32pdh, string

from lxml import etree

import socket
import subprocess
import shutil
from BtsShell.application_lib.sftp import *
import traceback
from BtsShell import connections
from BtsShell.common_lib.get_path import *
from BtsShell.application_lib.process import kill_process
try:
    import win32com.client
    from _winreg import (CloseKey, OpenKey, SetValueEx,
                         HKEY_CURRENT_USER, KEY_ALL_ACCESS, REG_EXPAND_SZ)
except Exception, error:
    print error

TP_LICENSE_ERROR = 'Unable to create the TestPartner object'
IP_LIST = ["10.68.160.99","10.68.160.98","10.135.60.203"]

def write_parameters_to_file_for_tp(parameters, file_path="parameters_tp.txt"):
    """This keyword will remove the specify file if it exist, and write parameters
    information into "C:\\parameters_tp.txt" in order to be read by testpartner.

    | Input Parameters  | Man. | Description |
    | parameters        | Yes  | parameters information, format is list or string  |

    Example
    | ${parameters_list} | create list | EEA0=1  | EEA1=2 |
    | Write Parameters To File For TP  | ${parameters_list} |
    | Write Parameters To File For TP  | EEA0=1 |
     """

##    systemversion = platform.platform()
##    if 'XP' in systemversion:
##        file_folder = 'c:\\'
##    else:
##        file_folder = 'c:\\gui_para'
    file_folder = 'c:\\gui_para'
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    file_path = os.path.join(file_folder,file_path)
    if os.path.exists(file_path):
        os.remove(file_path)

    file_handle = open(file_path, "a")
    try:
        if isinstance(parameters, list):
            for parameter in parameters:
                tmp = parameter.split('=')
                name = tmp[0]
                value = tmp[1]
                len_tmp = len(tmp)
                if 2 < len_tmp:
                    for i in xrange(len_tmp-2):
                        value = value + "=" +tmp[i+2]
                if re.search(' ', name):
                    name = name.replace(' ', '_')
                parameter = '='.join([name, value])
                print parameter + "\n"
                file_handle.write(parameter + "\n")
        elif parameters:
            tmp = parameters.split('=')
            name = tmp[0]
            value = tmp[1]
            len_tmp = len(tmp)
            if 2 < len_tmp:
                for i in xrange(len_tmp-2):
                    value = value + "=" +tmp[i+2]
            if re.search(' ', name):
                name = name.replace(' ', '_')
            parameters = '='.join([name, value])
            print parameters + "\n"
            file_handle.write(parameters)
        else:
            print "Please input parameter information, either in list or string"
    finally:
        file_handle.close()


def run_testpartner(script_name, TEST_LOG_DIRECTORY, sw_release="rl15"):
    """ DEPRECATED Use "Run TestPartner Command" instead.
    This keyword runs TestPartner script in command line interface and
    check the response

    | Input Parameters | Man. | Description |
    |     script_name  | Yes  | Identify test script name |
    |     sw_release   |  No  | Software Release version, default is "RL15" |

    Example
    | Run TestPartner Command |
    """
    try:
        ret = _run_testpartner_once(script_name, TEST_LOG_DIRECTORY, sw_release)
    except TP_LICENSE_ERROR:
        time.sleep(random.randint(60, 180))
        ret = _run_testpartner_once(script_name, TEST_LOG_DIRECTORY, sw_release)
    return ret


def _run_testpartner_once(script_name, TEST_LOG_DIRECTORY, sw_release="rl15"):
    script_name = script_name.lower()
    if re.search("\s", script_name):
        script_name = re.sub("\s+", "_", script_name)
    tp_app_path_xp = 'c:\\Program Files\\Micro Focus\\TestPartner\\TP.exe'
    tp_app_path_win7 = 'C:\\Program Files (x86)\\Micro Focus\\TestPartner\\TP.exe'
    ret = ''
    if os.path.exists(tp_app_path_xp):
        testpartner_cmd = "\"%s\" -d testpartner_lib_%s -u Admin -v -p admin \
-r common -s %s" % (tp_app_path_xp,sw_release.lower(), script_name)

        capture_screen_cmd = "\"%s\" -d testpartner_lib_%s -u Admin -v -p admin \
-r  common -s capture_screen" %(tp_app_path_xp,sw_release.lower())
    elif os.path.exists(tp_app_path_win7):
        testpartner_cmd = "\"%s\" -d testpartner_lib_%s -u Admin -v -p admin \
-r common -s %s" % (tp_app_path_win7,sw_release.lower(), script_name)

        capture_screen_cmd = "\"%s\" -d testpartner_lib_%s -u Admin -v -p admin \
-r common -s capture_screen" %(tp_app_path_win7,sw_release.lower())
    else:
        print 'Cannot find Testpartner App'
        ret = 'ERROR'
   # cmd = testpartner_cmd + script_name
    if not ret == 'ERROR':
        ret = os.popen(testpartner_cmd).read()
        print ret
    if ('Failed' in ret) or ('ERROR' in ret) or ('error' in ret):
        print "Save screenshot to %s" %TEST_LOG_DIRECTORY
        write_parameters_to_file_for_tp("PathName=%s"%TEST_LOG_DIRECTORY)
        screen_ret = os.popen(capture_screen_cmd).read()
        print screen_ret
        if ('Failed' in screen_ret) or ('ERROR' in screen_ret) or ('error' in screen_ret):
            bts_shell_parent_path = os.path.dirname(get_btsshell_path())
            test_dir = os.path.join(bts_shell_parent_path,"QTP",sw_release.lower(),"QTPScripts95_TDD_Prod","SiteMan","CaptureImage")
            mod_para_list = []
            mod_para_list.append("LogPath=%s\\"%TEST_LOG_DIRECTORY)
            run_qtp(test_dir, TEST_LOG_DIRECTORY, mod_para_list, "N", "300")
            os.system("TASKKILL /F /IM mspaint.exe")
        raise Exception, "Testpartner script '%s' run failed"%script_name
    elif TP_LICENSE_ERROR in ret:
        raise TP_LICENSE_ERROR
    else:
        return True

##def GetProcessID( name ):
##    try:
##        object = "Process"
##        items, instances = win32pdh.EnumObjectItems(None,None,object, win32pdh.PERF_DETAIL_WIZARD)
##        val = None
##        if name in instances :
##            hq = win32pdh.OpenQuery()
##            hcs = []
##            item = "ID Process"
##            path = win32pdh.MakeCounterPath( (None,object,name, None, 0, item) )
##            hcs.append(win32pdh.AddCounter(hq, path))
##            win32pdh.CollectQueryData(hq)
##            time.sleep(0.01)
##            win32pdh.CollectQueryData(hq)
##            for hc in hcs:
##                type, val = win32pdh.GetFormattedCounterValue(hc, win32pdh.PDH_FMT_LONG)
##                win32pdh.RemoveCounter(hc)
##                win32pdh.CloseQuery(hq)
##                return val
##    except:
##        return None

##def Kill_Process_pid(pid) :
##    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pid) #get process handle
##    win32api.TerminateProcess(handle,0) #kill by handle
##    win32api.CloseHandle(handle) #close api
##
##def kill_qtp_process():
##    print "----------Process list before delete------------"
##    plist = os.system("tasklist")
##    print plist
##
##    processlist = ['QTAutomationAgent','QTPro','DW20','dwwin']
##    print "Start to kill QTP process.%s"%processlist
##
##    for pname in processlist:
##        for i in range(1,5):
##            pid = GetProcessID (pname)
##            if pid == None:
##                pid2 ="None"
##            if pid <> None:
##                Kill_Process_pid(pid)
##            else:
##                print " Process "+pname+"is not existense"
##                break
##            time.sleep(1)
##
##            pid = GetProcessID (pname)
##            if pid == None:
##                print "process %s kill sucessuflly"%pname
##                break
##
##    print "Finshed to kill QTP process."
##
##    print "----------Process list after delete------------"
##    plist = os.system("tasklist")
##    print plist

RelColPath = "C:\\BTSSW_bak"

def GetBtsAndSMSWPath(CurRelName):
    NewRelPath = "%s\\NewRelInfo.ini" % RelColPath
    try:
        f = open(NewRelPath, 'r')
        CurRels = [item.replace('\r','').replace('\n','').split(" ") for item in f.readlines()]
    except Exception ,e:
        print "Error with info: \"%s\"" % e
    finally:
        f.close()

    for Rel in CurRels:
        if Rel[0] == CurRelName:
            CurSMName = Rel[1]

    if CurSMName:
        CurRelPath = "%s\\%s\\%s_release_BTSSM_downloadable_wo_images.zip" %(RelColPath, CurRelName, CurRelName)
        CurSMPath =  "%s\\%s" %(RelColPath, CurSMName)

    return (CurRelPath, CurSMPath)

##def GetBtsAndSMSWPath(CurRelName,workspace):
##    NewRelPath = "%s\\NewRelInfo_TRUNK_RL45.ini" % workspace
##    try:
##        f = open(NewRelPath, 'r')
##        CurRels = [item.replace('\r','').replace('\n','').split(" ") for item in f.readlines()]
##    except Exception ,e:
##        print "Error with info: \"%s\"" % e
##    finally:
##        f.close()
##
##    for Rel in CurRels:
##        if Rel[0] == CurRelName:
##            CurSMName = Rel[1]
##
##    if CurSMName:
##        CurRelPath = "%s\\%s\\%s_release_BTSSM_downloadable_wo_images.zip" %(workspace, CurRelName, CurRelName)
##        CurSMPath =  "%s\\%s" %(workspace, CurSMName)
##        this_file_path = inspect.getfile(inspect.currentframe())
##        resource_path = os.path.dirname(this_file_path)
##        semfiledir = os.path.join(os.path.dirname(os.path.dirname(resource_path)),'BtsShell','resources','scripts','1866')
##        semfilepath = os.path.join(semfiledir,'SEMversion.txt')
##        if os.path.exists(semfilepath):
##            os.remove(semfilepath)
##    try:
##        if not os.path.exists(semfiledir):
##            os.makedirs(semfiledir)
##        f = open(semfilepath,'w')
##        f.write(CurSMName+"\n")
##        f.write(CurSMPath)
##    except Exception,e:
##        print ""
##    finally:
##        f.close()
##
##    return (CurRelPath, CurSMPath)

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
    from BtsShell.high_shell_lib.common_operation import get_active_sw_version
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


def kill_qtp_process():
    print "Start to kill QTP process."
    os.system("TASKKILL /F /IM QTAutomationAgent.exe")
    os.system("TASKKILL /F /IM QTPro.exe /T")
    os.system("TASKKILL /F /IM DW20.EXE")
    os.system("TASKKILL /F /IM dwwin.exe")
    print "Finshed to kill QTP process."


def kill_testpartner_process():
    print "Start to kill TestPartner process."
    os.system("TASKKILL /F /IM TestPartner.exe")
    os.system("TASKKILL /F /IM TP.exe")
    os.system("TASKKILL /F /IM TESTPA~1.EXE")
    print "Finshed to kill TestPartner process."

def kill_sem_process():
    cmd = """wmic process where "commandline like '%com.nokia.em.poseidon.PoseidonStarter%' or commandline like '%com.nokia.em.sitemgr.SitemgrStarter%' and not commandline like '%wmic%'" delete"""
    result = os.popen(cmd).read()
    print result

    cmd = """wmic process where "commandline like '%alclient.jar%' and not commandline like '%wmic%'" delete"""
    result = os.popen(cmd).read()
    print result


def run_qtp(test_dir, log_save_dir="c:\\tmp", mod_para_list=None, keep_qtp_open="N", timeout="300"):
    """This keyword used for run qtp script, if you use in robot please select run_qtp_script

    | Input Parameters  | Man. | Description |
    | test_dir      | Yes  | Path of qtp test case  |
    | log_save_dir   | No  | Save directory for qtp log |
    | mod_para_list    | No   | Parameters need to modified, need be a list or None |

    Example

    | run_qtp  |  D:\\QTP\\SiteMan\\BlockBTS  |
     """
    image_log = "LogPath=%s\\" % log_save_dir
    mod = []
    mod.append(image_log)
    if None == mod_para_list:
        modify = mod
    elif isinstance(mod_para_list, list):
        is_found = False
        for avalue in mod_para_list:
            para_array = avalue.split("=",1)
            if para_array[0] == "LogPath":
                is_found = True
                break
        if is_found:
            modify = mod_para_list
        else:
            modify = mod + mod_para_list
    else:
        kill_qtp_process()
        raise Exception, "3rd parameter is not 'None' or 'list'"
    log_save_dir = log_save_dir + "\qtp_log" + time.strftime("%Y%m%d%H%M%S")

    #Check script existence
    if not os.path.isdir(test_dir):
        kill_qtp_process()
        raise Exception, "<QTP> Test script %s does not exists" % (test_dir)
    else:
        print '<QTP> Test %s is existence.'%(test_dir)


    for i in range(0,3):
        qApp = connect_to_server()
        if qApp <> None:
            break
        print "<QTP> Create QTP Application Failed for the " + str(i+1) + " time" + "\n"
        time.sleep(120)

    #qApp = connect_to_server()
    if qApp == None:
        print "<QTP> instanciation was Failed"
        raise Exception
    else:
        print "<QTP> instanciation was SUCCESSFUL!"


    #Load AddIn
    try:
        blnNeedChangeAddins = False
        Addins = qApp.GetAssociatedAddinsForTest(test_dir)
        for testAddin in Addins:
            if testAddin == "Java":
                print "<QTP> find java addin"
                if qApp.Addins(testAddin).Status <> "Active":
                    print "<QTP> java addin isn't active"
                    blnNeedChangeAddins = True
                    break

        if qApp.Launched and blnNeedChangeAddins:
            qApp.Quit()

        if blnNeedChangeAddins:
            errorDescription = ""
            print "<QTP> start to set addins to active"
            blnActivateOK = qApp.SetActiveAddins(Addins, errorDescription)
            if not blnActivateOK:
                print "<QTP load >" + testAddin + "failed.\n"
                print errorDescription
                kill_qtp_process()
                raise Exception
            print "<QTP> set addins to active successfully"
    except Exception,e:
        print e
        print "<QTP> Load AddIn Failed."
        


    try:
        print "<QTP> start to open test %s again"%test_dir
        try:
            qApp.Open(test_dir)  #open QTP script
        except Exception,e:
            print "<QTP> 2nd to open test failed.open test at 3rd time"
            qApp.Open(test_dir)
        print "<QTP> open test successfully at 3rd time"
        qtest = qApp.Test
        print "<QTP> automated test case open was SUCCESSFUL!"

        print "<QTP> launch QTP App,it's default is visibled"
        if not qApp.Launched:
            qApp.Launch()  #Start QuickTest
        qApp.Visible = False  #Make the QuickTest application visible
        #Set folder to research
        #bts_shell_parent_path = os.path.dirname(get_btsshell_path())
        print "<QTP> start to move current release lib path to active"
        pattern = re.compile(r".*\\QTP\\RL.*\\QTPScripts95_TDD_Prod\\.*\\.*")
        match = pattern.match(test_dir)
        if match:
            pathstr = os.path.dirname(os.path.dirname(test_dir))
            fnum = qApp.Folders.Find(pathstr)
            if fnum == -1:
                qApp.Folders.Add(pathstr, 1)
            else:
                qApp.Folders.MoveToPos(fnum, 1)

        # Set Parameters
        qdefcoll = qApp.Test.ParameterDefinitions  #As QuickTest.ParameterDefinitions ' Declare a Parameter Definitions collection
        rtparas = qdefcoll.GetParameters()  #As QuickTest.Parameters ' Declare a Parameters collection
        cnt = qdefcoll.Count
        print '<QTP> Parameter as below:'
        try:
            for para in modify:
                tmp = para.split("=",1)
                for i in range(cnt):
                    anitem = qdefcoll.Item(i+1).Name
                    if tmp[0] == anitem:
                        print tmp[0].strip() + "=\"" + tmp[1].strip() + "\""
                        rtpara = rtparas.Item(tmp[0].strip())  #Retrieve a specific parameter.
                        rtpara.Value = tmp[1].strip()  #Change the parameter value.
                        break
        except:
            print "<QTP> Set Parameter value error."
            kill_qtp_process()
            raise Exception

        result_dir = log_save_dir

        qoptions = win32com.client.DispatchEx("QuickTest.RunResultsOptions")    #As QuickTest.RunResultsOptions ' Declare a Run Results Options object variable
        qoptions.ResultsLocation = result_dir
        #runresult = qtest.Run(qoptions,True,rtparas)

        print '<QTP> Save log to %s'%(os.path.join(result_dir, "Report"))

        runresult = qtest.Run(qoptions,True,rtparas)

        result = qtest.LastRunResults.Status
        if str(result).lower() == 'failed':
            error_info = ""
            error_info = _parse_qtp_last_error(os.path.join(result_dir, "Report", "Results.xml"))
            if error_info.lower() <> "passed":
                kill_qtp_process()
                raise Exception, "QTP result is failed! "
    except Exception,e:
        print e
        print "<QTP> run Failed."
        kill_qtp_process()
        raise Exception
    finally:
        if keep_qtp_open == "N":
            if qApp <> None:
                qApp.Quit()
                qApp = None



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
            #if "Failed" == sta:
            if 0 == sta.find("Failed"):
                #raise Exception, "QTP run failed! "
                raise Exception, tmp
            else:
                return tmp
    else:
        status = re.search(".*NodeArgs.*status=(.*)>", last1_step_info)
        if status:
            sta = status.groups()[0].strip("\"")
            #if "Failed" == sta:
            if 0 == sta.find("Failed"):
                raise Exception, "QTP step run failed!"
            else:
                return sta


def connect_to_server():
    qApp = None

    for aip in IP_LIST:
        connect_fail = False
        try:
            a = win32com.client.DispatchEx("QuickTest.Application")
        except:
            try:
                cmdstr1 = "TASKKILL /F /IM QTAutomationAgent.exe"
                cmdstr2 = "TASKKILL /F /IM QTPro.exe"
                os.system(cmdstr1)
                os.system(cmdstr2)
                time.sleep(60)
                a = win32com.client.DispatchEx("QuickTest.Application")
            except:
                connect_fail = True

        if not connect_fail:
            qApp = a
            break

        print "Change IP to: " + aip + "\n"

        key = OpenKey(HKEY_CURRENT_USER, 'Environment', 0, KEY_ALL_ACCESS)
        SetValueEx(key, "LSHOST", 0, REG_EXPAND_SZ, aip)
        CloseKey(key)

    if qApp == None:
        try:
            monitor_license()
        finally:
            pass

    return qApp


def get_sm_version():
    #file_dir = os.path.joing(log_path,"SWVersions.txt")
    file_dir = "c:\\gui_para\\SWVersions.txt"
    if not os.path.exists(file_dir):
        raise Exception, "SWVersions not exists!"

    try:
        smver_file_obj = open(file_dir,"r")
        text = smver_file_obj.readline()
        sm_ver = text.strip("\n")
    except:
        raise Exception, "Read File Failed"
    finally:
        smver_file_obj.close()

    #sm_ver = "Version LNT3.0 (1303_001_00)"
    #LNT3.0_BTSSM_1304_001_00

    sm_ver_list = sm_ver.split(" ")

    ver_num = sm_ver_list[2].lstrip("(").rstrip(")")

    sm_version = sm_ver_list[1] + "_BTSSM_" + ver_num
    #print sm_version

    return sm_version


def get_tp_output():
    file_dir = "d:\\tp_output.txt"
    if not os.path.exists(file_dir):
        raise Exception, "Output file not exists!"

    try:
        fileobj = open(file_dir,"r")
        text = fileobj.read()
    except:
        raise Exception, "Read File Failed!"
    finally:
        fileobj.close()

    print text


def monitor_license():
    #Create fine in D: with IP__Time format
    now_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    try:
        myname = socket.getfqdn(socket.gethostname(  ))
        myaddr = socket.gethostbyname(myname)
        addr_list = socket.gethostbyname_ex(myname)
        ip_list = addr_list[2]
        for anip in ip_list:
            if anip <> "192.168.255.126":
                myaddr = anip
                break
    except Exception, e:
        myaddr = "Unknown"
        addr_list = "Get address list failed."
     #   print e
    finally:
        pass

    file_folder = 'c:\\gui_para\\monitor_license'
    if not os.path.exists('c:\\gui_para'):
        os.makedirs('c:\\gui_para')
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    pure_name = str(myaddr) + "_" + now_time
    local_file_name = pure_name + ".txt"
    local_file_name =  os.path.join(file_folder,local_file_name)

    f = None
    try:
        f = open(local_file_name,"w")
        f.write(str(addr_list))
    finally:
        if f <> None:
            f.close()

    # Upload the file to 59
    sf = Sftp("10.69.68.59", "22", "tdlte-tester", "btstest")
    remote_file_name = "d:\\GUI_License_Monitor\\" + pure_name + ".txt"
    try:
        sf.sftp.put(local_file_name, remote_file_name)
    #except Exception,e:
     #   print e
    finally:
        sf.close()

    try:
        os.remove(local_file_name)
    finally:
        pass


def modify_sem_maxpermsize():
    """This keyword is used to change MaxPermSize to 128m in the file cl_tdlte.xml
    """
    cl_file = glob.glob('C:\\Program Files*\\NSN\\Managers\\BTS Site\\BTS Site Manager\\NodeManagers\\*_BTSSM_*\\cl_tdlte.xml')
    file_handle = open(cl_file[0], "r")
    try:
        n = 0
        updated_line = ""
        text = file_handle.readlines()
        line_length = len(text)
        for i in range(0,line_length):
            if re.search('MaxPermSize=\d*m',text[i]):
                n = i
                updated_line = re.sub("MaxPermSize=\d*m","MaxPermSize=128m",text[i])
                print "Updated MaxPermSize to 128m."
                break
        #print updated_line
        text[n] = updated_line
        file_handle_2 = open(cl_file[0], "w")
        file_handle_2.writelines(text)

    finally:
        file_handle.close()
        file_handle_2.close()








if __name__ == '__main__':
##    kill_sem_process()
##    _run_testpartner_once("qertd", "c:\\sss", sw_release="rl15")
##    CurRelName = 'LNT0.0_ENB_94140102_8545'
##    workspace = 'C:\Temp'
##    btspath,sempath = GetBtsAndSMSWPath(CurRelName,workspace)
    pass
##    run_testpartner("sm_logon", "d:\\svn", "rl45")
##    parameters=['a=b','c=d']
##    write_parameters_to_file_for_tp(parameters)

    """log_save_dir = "D:\\Test\\log"
    test_dir = "C:\Python25\Lib\site-packages\QTP\RL45\QTPScripts95_TDD_Prod\SiteMan\Login"
    mod_para_list=[]
    mod_para_list.append("IPAddress=Local")
    mod_para_list.append("UserName=Nemuadmin")
    mod_para_list.append("Password=nemuuser")
    mod_para_list.append("LogPath=D:\\Test\\log")
    run_qtp(test_dir,log_save_dir,mod_para_list,"N","300")"""
    #get_sm_version("D:\\")
    #get_tp_output()
##    a = connect_to_server()
##    print a
    #res_file="D:\\Test\\Results1.xml"
    #_parse_qtp_last_error(res_file)



