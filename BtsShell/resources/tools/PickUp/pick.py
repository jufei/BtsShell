"""This tool use to run CT with CSV file which stored cases need to be run
informaiton.

1, Parse the SuiteMapping.csv to get case infomarion and store cases need to be run in a list
2, Copy one backup case to current Dir such as "pick_file_name_timestamp"
3, Run case in its primary path and output to "pick_file_name_timestamp"
4, Generate output log and report for all *.xml both in "pick_file_name_timestamp" and log_dir if given

Usage:
    python pick.py --rootpath=root_path --pickup=pick_file_path --btsfile=bts_file_path --logdir=log_dir --loglevel=log_level

Example:
test    python pick.py -r "D:\Script\TestCase\trunk\RL25" -p pick.csv -b lexus.py -d "D:\TestResult\RL25"
"""

import os
import re
import time
import shutil
from optparse import OptionParser
from fix_xml import fix_xml

from robot import version
ROBOT_VERSION = version.get_version()
if ROBOT_VERSION > '2.7':
    from robot.api import ExecutionResult
    class TestSuite:
        def __init__(self, outputpath):
            self._er = ExecutionResult(outputpath)
            self.status = self._er.suite.status
else:
    from robot.output import TestSuite
    

import subprocess, sys, glob


global ROOT_PATH
global PICK_FILE_PATH
global BTS_FILE
global TARGET_BTS_FILE
global LOG_PATH
global LOG_LEVEL

global RERUN_FLAG
global RERUN_FAILRATIO

SET_TABLE = {'test_set': 'Test Set',
             'test_suite': 'Test Suite',
             'run': 'Run',
             'case_tag': 'Case Tag',
            'timeout': 'Timeout(min)'}



def parse_suite_mapping_new():
    """It will analyse PICK_FILE_PATH, then write case information into a list which
    contains case path, case name, case tag """
    try:
        file_handle = file(PICK_FILE_PATH)
    except:
        raise Exception, "Open file %s failed" % (PICK_FILE_PATH)


    # case "get_active_sw_version.html" will be the 1st one to be executed
    case_list = []

    try:
        suite_pos   = None
        run_pos     = None
        timeout_pos = None
        lines = file_handle.readlines()
        for line in lines:
            case_dict = {}
            case_info_list = []
            case_dir_dict = {}
            line = re.sub("\n", "", line)
            line = re.sub("\"", "", line)
            #print line
            items = line.split(',')
            items_length = len(items)
            if items[0] == SET_TABLE['test_suite']:
                suite_pos   = items.index(SET_TABLE['test_suite'])
                run_pos     = items.index(SET_TABLE['run'])
                timeout_pos = items.index(SET_TABLE['timeout'])
                sets = ['' for index in range(suite_pos + 4)]
                continue

            if suite_pos == None or run_pos == None or timeout_pos == None:
                continue

            if items_length < suite_pos + 1:  # In order to get the dir path
                continue

            for index in range(items_length):
                if index < suite_pos + 1:
                    try:
                        if items[index] != '':
                            sets[index] = items[index]
                        if items[index] == '' and index > 0 and items[index - 1] != '':
                            sets[index] = items[index]
                    except:
                        pass
            if items[run_pos] and items[run_pos] != "0":

                file_name = os.path.basename(sets[-4])
                file_path = os.path.dirname(sets[-4]).replace("/", "\\")
                file_path = os.path.join(ROOT_PATH, file_path)

                sets[-3] = items[run_pos]
                if items_length > timeout_pos:
                    sets[-1] = items[timeout_pos]
                sets[-2] = ''
                case_dict[file_name] = [sets[-3], sets[-2],sets[-1]]
                case_info_list.append(case_dict)
                case_dir_dict[file_path] = case_info_list
                case_list.append(case_dir_dict)
                sets[-3] = ''
                sets[-2] = ''
                sets[-1] = ''
        return case_list

    except Exception, p_Err:
        print line
        print p_Err

def parse_suite_mapping():
    """It will analyse PICK_FILE_PATH, then write case information into a list which
    contains case path, case name, case tag """
    try:
        file_handle = file(PICK_FILE_PATH)
    except:
        raise Exception, "Open file %s failed" % (PICK_FILE_PATH)

    #case_get_sw_ver_path = __get_sw_version_case_path()
    # case "get_active_sw_version.html" will be the 1st one to be executed
    case_list = []

    try:
        suite_position = None
        run_position = None
        case_tag_position = None
        lines = file_handle.readlines()
        for line in lines:
            case_dict = {}
            case_info_list = []
            case_dir_dict = {}
            if re.search("\n", line):
                line = re.sub("\n", "", line)
            if re.search("\"", line):
                line = re.sub("\"", "", line)
            items = line.split(',')
            items_length = len(items)
            if items[0] == SET_TABLE['test_set']:
                suite_position = items.index(SET_TABLE['test_suite'])
                run_position = items.index(SET_TABLE['run'])
                case_tag_position = items.index(SET_TABLE['case_tag'])
                timeout_position = items.index(SET_TABLE['timeout'])
                sets = ['' for index in range(suite_position + 4)]
                continue
            if suite_position == None or run_position == None or case_tag_position == None or timeout_position == None:
                continue
            if items_length < suite_position + 1:  # In order to get the dir path
                continue
            for index in range(items_length):
                if index < suite_position + 1:
                    try:
                        if items[index] != '':
                            sets[index] = items[index]
                        if items[index] == '' and index > 0 and items[index - 1] != '':
                            sets[index] = items[index]
                    except:
                        pass
            if items_length < run_position + 1:
                continue
            if items[run_position] and items[run_position] != "0":
                sets[-3] = items[run_position]
                if items_length > timeout_position:
                    sets[-1] = items[timeout_position]
                if items_length > case_tag_position:
                    sets[-2] = items[case_tag_position]
                file_path = ROOT_PATH
                for set_ in sets[1:-4]:
                    file_path = os.path.join(file_path, set_)
                suite_name = re.sub(".html$", "", sets[-4])
                file_path = os.path.join(file_path, suite_name)
                case_dict[sets[-4]] = [sets[-3], sets[-2],sets[-1]]
                case_info_list.append(case_dict)
                case_dir_dict[file_path] = case_info_list
                case_list.append(case_dir_dict)
                sets[-3] = ''
                sets[-2] = ''
                sets[-1] = ''
        return case_list

    except Exception, p_Err:
        print line
        print p_Err


def make_new_folder():
    # create a new folder to store cases needed to be tested
    time_string = time.strftime("%Y%m%d%H%M%S")
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
    case_log_dir = os.path.join(LOG_PATH, 'TestLog_%s' % time_string)
    if not os.path.exists(case_log_dir):
        os.mkdir(case_log_dir)
    case_backup_dir = os.path.join(case_log_dir, "Cases_Picked_Backup")
    if not os.path.exists(case_backup_dir):
        os.mkdir(case_backup_dir)

    return case_log_dir, case_backup_dir


def copy_and_run_cases(case_list, case_run_dir, case_backup_dir):
    """It will make a new directory if not exist, then copy cases to pickup folder
    and run Robot command and generate output.xml file"""
    for case_dict in case_list:
        for case_dir in case_dict.keys():
            for name_run_tag_dict in case_dict[case_dir]:
                print "\tWill Run case, INFO: ", name_run_tag_dict
                for case in name_run_tag_dict.keys():
                    robot_case_path = os.path.join(case_dir, case)
                    if not os.path.exists(robot_case_path):
                        print "\n####################Case Not Exist#######################"
                        print "Case: \"%s\" do not exist" % (robot_case_path)
                        print "\n\n"
                        continue
                    # copy case to new folder
                    tag_info = ""
                    tag_diff_list = []
                    case_tmp = case
                    timeout = name_run_tag_dict[case][2]
                    if not re.search("[0-9]+", name_run_tag_dict[case][0]):
                        name_run_tag_dict[case][0] = '1'
                    tmp_status = []
              
                    case_fail_num = 1
                    for i in range(int(name_run_tag_dict[case][0])):
                    
                        if (0 != case_fail_num) or RERUN_FLAG:
                            tag_diff_list.append("#" + str(i))
                            tag_not_run = False
                            if name_run_tag_dict[case_tmp][1]:
                                tag_info = ""
                                tag_list = name_run_tag_dict[case_tmp][1].split(";")
                                for tag in tag_list:
                                    if not re.search("^#", tag):
                                        tag_info = tag_info + "-i " + tag + " "
                                        tag_diff_list[-1] = tag_diff_list[-1] + "#" + tag
                            if len(tag_diff_list) > 1:
                                case = re.sub("%s.html" % (tag_diff_list[-2]), "%s.html" % (tag_diff_list[-1]), case)
                            else:
                                case = re.sub(".html", "%s.html" % (tag_diff_list[-1]), case)
                            try:
                                case_store_path = os.path.join(case_backup_dir, case)
                                shutil.copy(robot_case_path, case_store_path)
                                # run case one by one
                                print """
    ========================Run case:============================
    case: %s
    tag_info: %s
    case_run_dir: %s
    case_backup_dir: %s
    robot_case_path: %s
    timeout: %s 
    =============================================================
                                """ %(case, tag_info, case_run_dir, case_backup_dir, robot_case_path, timeout)
    
                                status_flag, case_fail_num = run_case(case, tag_info, case_run_dir, case_backup_dir, robot_case_path, timeout)
                                if RERUN_FLAG:
                                    tmp_outputname = re.sub(".html$", ".xml", case)
                                    if os.path.exists("%s/%s" % (case_backup_dir, tmp_outputname)):
                                        
                                        tmp_status.append(GetSuiteStatus("%s/%s" % (case_backup_dir, tmp_outputname)))
                                    else:
                                        if status_flag:
                                            
                                            tmp_status.append(status_flag)
                            except Exception, e:
                                print "Error: "
                                print e

                    try:
                        if RERUN_FLAG:
                            tmp_failratio = float(tmp_status.count(1))/float(len(tmp_status))
                            print "+++++++++++++++++++++", tmp_failratio, RERUN_FAILRATIO
                            if tmp_failratio >= RERUN_FAILRATIO:
                                print """
    ========================Re-Run case:===============================
            case: %s
            FailRatio: %s
    ===================================================================
                                """ %(case, tmp_failratio)
                                run_case(case, tag_info, case_run_dir, case_backup_dir, robot_case_path, timeout, output_tag='_rerun.xml')
                    except Exception, e:
                        print """
    =============================ERROR Re-Run:==========================
        Case: %s
        Exception: %s
    ====================================================================
                        """ % case, e
def GetSuiteStatus(outputfile):
    obj = TestSuite(outputfile)
    if obj.status == 'FAIL':
        return 1
    else:
        return 0

def run_case(case_name, tag_info, case_run_dir, case_backup_dir, robot_case_path, timeout, output_tag='.xml'):
    suite_status = 1
    """ run case one by obe by pybot command """
    try:
        output_name = re.sub(".html$", ".xml", case_name)
        output_name = output_name.replace(" ","_")
        output_file = os.path.join(LOG_PATH,'output.xml')
        ouput_path = os.path.join(case_backup_dir, output_name)
        log_level = "-L %s" % (LOG_LEVEL)
        
        if not os.path.exists(robot_case_path):
            raise Exception("NO case file '%s'!" % robot_case_path)
        file_content = file(robot_case_path).read()
        cmd_option = " "
        if "RobotWS.html" in file_content:
            if new_btsfile == "":
                raise Exception("Please add '--new_btsfile' option to use newlib's btsname.py")
            cmd_option += "-V \"%s\" " % new_btsfile
            if new_target != "":
                cmd_option += " -V \"%s\":TGT1" %(new_target)
        elif "BtsShell.html" in file_content:
            cmd_option += "-V \"%s\" " % BTS_FILE
            if TARGET_BTS_FILE != "":
                cmd_option += " -V \"%s\":target" %(TARGET_BTS_FILE)
        
        if VAR_STR:
            cmd_option += " -v %s " % ( VAR_STR)
       
        cmd_option += " -l None -r None %s -o \"%s\" -d \"%s\" " \
                    % ( log_level, ouput_path, case_run_dir)
        
        pybot_cmd = "pybot.bat %s \"%s\"" %(cmd_option, robot_case_path)
        print pybot_cmd
        if tag_info != "":
            pybot_cmd = cmd_option + "%s\"%s\"" % (tag_info, robot_case_path)
        start_time = time.time()
        p = subprocess.Popen(pybot_cmd, stdout=sys.stdout, shell=True)
        if timeout:
            while p.poll() == None and (time.time() - start_time) < float(timeout)*60:
                time.sleep(3)
            if p.poll() != None:
                pass
            else:
                print """
     ======================Timeout=========================
        Timeout!!! teminate this case:
        Case: %s
        output: %s
    =====================================================""" % (case_name, ouput_path)
                os.system("TASKKILL /F /T /PID %s" % (p.pid))
                p.__del__()
                time.sleep(2)
                try:
                    if os.path.exists(ouput_path):
                        file_size = os.path.getsize(ouput_path)
                        if file_size > 0:
                            print "start fix xml--------\n%s"%ouput_path
                            fix_xml(ouput_path, ouput_path, int(timeout))
                            print "stop fix xml--------"
                        else:                       
                            print 'File size is zero!'
                except Exception,e:
                    print e
                finally:                    
                    pass
##                try:
##                    if os.path.exists(ouput_path):
##                        print 'Rename output file: %s' %os.path.abspath(ouput_path)
##                        os.system("mv -f %s %s.timeoutbak" %(os.path.abspath(ouput_path), os.path.abspath(ouput_path)))
##                        if os.path.exists(ouput_path):
##                            os.renames(ouput_path, "%s.timeoutbak" %(os.path.abspath(ouput_path)))
##                except Exception,e:
##                    print e
##                finally:
##                    return 1, suite_status
        else:            
            p.wait()

        time.sleep(2)
        if os.path.exists(output_file):
            tag = time.strftime("%m%d%H%M%S")
            file_tail =  tag  + "_output.xml"
            new_output_file =  os.path.join(LOG_PATH,file_tail)
        else:
            new_output_file = output_file
#            os.rename(output_file,new_output_file)
        if ROBOT_VERSION < '2.5.7':
            rebot_cmd = "rebot -l \"%s\"/log.html -r \"%s\"/report.html -o \"%s\" \"%s\"" % (LOG_PATH,\
                                                    LOG_PATH, new_output_file, ouput_path)        
        else:
            rebot_cmd = "rebot -L INFO -l \"%s\"/log.html -r \"%s\"/report.html -o \"%s\" \"%s\"" % (LOG_PATH,\
                                                    LOG_PATH, new_output_file, ouput_path)
        rebot_ret = os.system(rebot_cmd)
        suite_status = GetSuiteStatus(new_output_file.replace('\\', '\\\\'))
        time.sleep(1)
        
    except Exception,e:
        print e
    
    return ouput_path, suite_status

def combine_output_file(dir_,cases='*',output_name='output.xml'):
    """It will combine all result file with".xml" into log file and report file"""
    log_name = time.strftime("%m%d%H%M%S") + '_log.html'
    if ROBOT_VERSION < '2.5.7':
        rebot_cmd = "rebot -N TA -l %s/%s -r %s/report.html  %s/%s.xml" % (LOG_PATH, log_name, LOG_PATH, dir_, cases)
    else:
        rebot_cmd = "rebot -L INFO -N TA -l %s/%s -r %s/report.html  %s/%s.xml" % (LOG_PATH, log_name, LOG_PATH, dir_, cases)
        
    rebot_ret = os.system(rebot_cmd)
    time.sleep(1)
    if not os.path.exists("%s/%s" % (dir_,output_name)):
        rebot_pick_cmd = "rebot -L INFO -N TA -l %s/log.html -r %s/report.html -o %s/%s %s/%s.xml" % (dir_, dir_, dir_, output_name, dir_, cases)
        rebot_pick_ret = os.system(rebot_pick_cmd)

def parse_parameters():

    runtype = ''
    parser = OptionParser()
    parser.add_option("-r", "--rootpath", action="store", type="string", dest="rootpath")
    parser.add_option("-p", "--pickup", action="store", type="string", dest="pickup")
    parser.add_option("-b", "--btsfile", action="store", type="string", dest="btsfile")
    parser.add_option("-t", "--targetbtsfile", action="store", type="string", dest="targetbtsfile")
    parser.add_option("-d", "--dir", action="store", type="string", dest="dir")
    parser.add_option("-l", "--loglevel", action="store", type="string", dest="loglevel")
    parser.add_option("-f", "--rerunflag", action="store", type="string", dest="rerunflag")
    parser.add_option("-v", "--variable", action="store", type="string", dest="variable")
    parser.add_option("-n", "--runtype", action="store", type="string", dest="runtype")
    parser.add_option("--new_btsfile", action="store", type="string", dest="new_btsfile")
    parser.add_option("--new_target", action="store", type="string", dest="new_target")


    (options, args) = parser.parse_args()



    if options.rootpath:
        ROOT_PATH = options.rootpath
    else:
        raise Exception, "Please input the root path for these cases"

    if options.pickup:
        PICK_FILE_PATH = options.pickup
    else:
        raise Exception, "Please input pick up file name which ending with .py"

    if (not options.btsfile) and (not options.new_btsfile):
        raise Exception, "Please input BTS file name which ending with .py"
        
    if options.btsfile:
        BTS_FILE = options.btsfile
    else:
        BTS_FILE = ""        

    if options.targetbtsfile:
        TARGET_BTS_FILE = options.targetbtsfile
    else:
        TARGET_BTS_FILE = ''

    if options.new_btsfile:
        new_btsfile = options.new_btsfile
    else:
        new_btsfile = ""


    if options.new_target:
        new_target = options.new_target
    else:
        new_target = ""


    if options.dir:
        LOG_PATH = options.dir
    else:
        raise Exception, "Please input LOG DIR for log.html, report.html and output.xml"

    if options.loglevel:
        LOG_LEVEL = options.loglevel
    else:
        LOG_LEVEL = "INFO"

    if options.rerunflag:
        RERUN_FLAG = True
        RERUN_FAILRATIO = float(options.rerunflag)
    else:
        RERUN_FLAG = False
        RERUN_FAILRATIO = 0.8
        
    if options.variable:
        VAR_STR = options.variable
    else:
        VAR_STR = ""

    if options.runtype:
        runtype = "1"
    else:
        runtype = "0"



    return (ROOT_PATH, PICK_FILE_PATH, BTS_FILE, 
            TARGET_BTS_FILE, LOG_PATH, LOG_LEVEL, 
            RERUN_FLAG, RERUN_FAILRATIO,VAR_STR, 
            runtype, new_btsfile, new_target)


if __name__ == "__main__":
    runflag = ''
    (ROOT_PATH, PICK_FILE_PATH, BTS_FILE, 
    TARGET_BTS_FILE, LOG_PATH, LOG_LEVEL, 
    RERUN_FLAG, RERUN_FAILRATIO,VAR_STR, 
    runflag, new_btsfile, new_target) = parse_parameters()

    if "1" == runflag:
        case_list =  parse_suite_mapping_new()
    else:
        case_list = parse_suite_mapping()

    (cases_dir, backup_dir) = make_new_folder()
    try:
        copy_and_run_cases(case_list, cases_dir, backup_dir)
    except Exception, e:
        print "Error: "
        print e
    finally:
       combine_output_file(backup_dir)
    pass


