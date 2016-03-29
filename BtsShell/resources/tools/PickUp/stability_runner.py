"""
This script just to:
1.run cases in BTS contol PC which cases in SuiteMapping.csv
2.anaylse testcases' info,the info contain:cases name,test_starttime,test_endtime,test_elspedtime
  and detail info from output.xml
3.insert the above info into SQLserver.
****************************************************************************************************
The using in CMD window,eg:
python stability_runner.py -r d:\Project\script_for_QT\Cases -p d:\Project\script_for_QT\SuiteMapping.csv -b d:\ford.py -d "d:\project"
-r for gettting cases' root path
-p for getting SuiteMapping.csv file,which contain cases' extend paths,case number and run times
-b for getting robot variable file
-d for setting which path to save output.xml,log.html,report.html files and logs.
Get Current Active SW Version must be testcase setup or teardown
BTW:Before run this script,make sure robot and pyodbc models are installed.
"""
import os
import time
import re
import commands
import mmap
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


import shutil
from optparse import OptionParser
##import pyodbc
import subprocess, sys, glob


SET_TABLE = {'test_set': 'Test Set',
             'test_suite': 'Test Suite',
             'run': 'Run',
             'pass_rate': 'Pass Rate(%)',
            'timeout': 'Timeout(min)',
            'case_tag': 'Case Tag',
            'Max_run': 'Max Run'
             }



def parse_suite_mapping():
    """It will analyse PICK_FILE_PATH, then write case information into a list which
    contains case path, case name, case tag """
    try:
        file_handle = file(PICK_FILE_PATH)
    except:
        raise Exception, "Open file %s failed" % (PICK_FILE_PATH)

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
                pass_rate_position = items.index(SET_TABLE['pass_rate'])
                max_run_position = items.index(SET_TABLE['Max_run'])
                sets = ['' for index in range(suite_position + 6)]
                continue
            if suite_position == None or run_position == None or case_tag_position == None:
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
                sets[-5] = items[run_position]
                if items_length > case_tag_position:
                    sets[-1] = items[case_tag_position]
                if items_length > timeout_position:
                    sets[-2] = items[timeout_position]
                if items_length > pass_rate_position:
                    sets[-3] = items[pass_rate_position]
                if items_length > max_run_position:
                    sets[-4] = items[max_run_position]  
                file_path = ROOT_PATH
                for set_ in sets[1:-6]:
                    file_path = os.path.join(file_path, set_)
                suite_name = re.sub(".html$", "", sets[-6])
                file_path = os.path.join(file_path, suite_name)
                case_dict[sets[-6]] = [sets[-5],sets[-4],sets[-3], sets[-2], sets[-1]]
                case_info_list.append(case_dict)
                case_dir_dict[file_path] = case_info_list
                case_list.append(case_dir_dict)
                sets[-5] = ''
                sets[-4] = ''
                sets[-3] = ''
                sets[-2] = ''
                sets[-1] = ''        
        return case_list

    except Exception, p_Err:
        print p_Err


def make_new_folder():
    # create a new folder to store cases needed to be tested
    time_string = time.strftime("%Y%m%d%H%M%S")
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
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
                    output_path = ""
                    
                    #special_flag for case need to stop once case failed, in suitmapping Max_run should be as '10s'
                    special_flag = False
                    max_run_num = name_run_tag_dict[case][-4]
                    if max_run_num.endswith('s'):
                        max_run_num = int(max_run_num[:-1])
                        special_flag = True
                    timeout = name_run_tag_dict[case][-2]
                    pass_rate = name_run_tag_dict[case][-3]
                    must_run_num = name_run_tag_dict[case][-5]
                    pass_num = 0
                    fail_num = 0
                    print "\nCase '%s' exec %s" %(case, name_run_tag_dict[case])
                    
                    try:
                        if pass_rate == '':
                            pass_rate = 1
                        else:
                            pass_rate = int(pass_rate)
                    except Exception, e:
                        print e
                        pass_rate = 1
                   
                    if not re.search("[0-9]+", name_run_tag_dict[case][0]):
                        name_run_tag_dict[case][0] = '1'
                    last_result = 0
                    for i in range(int(max_run_num)):
                        #if special case and case failed just stop, no loop again
                        if special_flag==True and last_result==1:
                            break  
                           
                        tag_diff_list.append("#" + str(i))
                        print tag_diff_list
                        tag_not_run = False
                        
                        if name_run_tag_dict[case_tmp][-1]:
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
                            # step1::run case: one by one from case list
                            output_path, last_result = run_case(case, tag_info, case_run_dir, case_backup_dir, robot_case_path,timeout)
                            

                        except Exception,e:
                            print " Error: %s" %e

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

        common_cmd = " -V \"%s\" -l None -r None %s -o \"%s\" -d \"%s\" " \
% (BTS_FILE, log_level, ouput_path, case_run_dir)
        if TARGET_BTS_FILE != "":
            traget_btsfile = " -V \"%s\":target" %(TARGET_BTS_FILE)
            common_cmd = "%s%s" %(traget_btsfile , common_cmd)
        common_cmd = "pybot.bat %s" %(common_cmd)
        pybot_cmd = common_cmd + "\"%s\"" % (robot_case_path)
        if tag_info != "":
            pybot_cmd = common_cmd + "%s\"%s\"" % (tag_info, robot_case_path)
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
            file_tail =  tag + "_output.xml"
            new_output_file =  os.path.join(LOG_PATH,file_tail)
        else:
            new_output_file = output_file
##            os.rename(output_file,new_output_file)

        rebot_cmd = "rebot -N Stability_TA -l %s/log.html -r %s/report.html -o \"%s\" \"%s\"" % (LOG_PATH,\
                                                    LOG_PATH, new_output_file, ouput_path)
        rebot_ret = os.system(rebot_cmd)
        suite_status = GetSuiteStatus(new_output_file.replace('\\', '\\\\'))
        time.sleep(1)
        
    except Exception,e:
        print e
    
    return ouput_path, suite_status


def combine_output_file(dir):
    """It will combine all result file with".xml" into log file and report file"""
    rebot_cmd = "rebot -N QT_TA -l %s/log.html -r %s/report.html -o %s/output.xml %s/*.xml" % (LOG_PATH, LOG_PATH, LOG_PATH, dir)
    rebot_ret = os.system(rebot_cmd)
    time.sleep(1)
    if not os.path.exists("%s/output.xml" % (dir)):
        rebot_pick_cmd = "rebot -N QT_TA -l %s/log.html -r %s/report.html -o %s/output.xml %s/*.xml" % (dir, dir, dir, dir)
        rebot_pick_ret = os.system(rebot_pick_cmd)

           
def parse_parameters():
    parser = OptionParser()
    parser.add_option("-r", "--rootpath", action="store", type="string", dest="rootpath")
    parser.add_option("-p", "--pickup", action="store", type="string", dest="pickup")
    parser.add_option("-b", "--btsfile", action="store", type="string", dest="btsfile")
    parser.add_option("-t", "--targetbtsfile", action="store", type="string", dest="targetbtsfile")
    parser.add_option("-d", "--dir", action="store", type="string", dest="dir")
    parser.add_option("-l", "--loglevel", action="store", type="string", dest="loglevel")
    (options, args) = parser.parse_args()

    if options.rootpath:
        ROOT_PATH = options.rootpath
    else:
        raise Exception, "Please input the root path for these cases"

    if options.pickup:
        PICK_FILE_PATH = options.pickup
    else:
        raise Exception, "Please input pick up file name which ending with .csv"

    if options.btsfile:
        BTS_FILE = options.btsfile
    else:
        raise Exception, "Please input BTS file name which ending with .py"

    if options.targetbtsfile:
        TARGET_BTS_FILE = options.targetbtsfile
    else:
        TARGET_BTS_FILE = ''

    if options.dir:
        LOG_PATH = options.dir
    else:
        raise Exception, "Please input LOG DIR for log.html, report.html and output.xml"

    if options.loglevel:
        LOG_LEVEL = options.loglevel
    else:
        LOG_LEVEL = "INFO"

    return (ROOT_PATH, PICK_FILE_PATH, BTS_FILE, TARGET_BTS_FILE, LOG_PATH, LOG_LEVEL)

def _get_testbed_info():
    try:
        f = open(BTS_FILE, 'r+')
    except:
        raise Exception, "open file '%s' failed" % BTS_FILE
    try:
        lines = f.readlines()
        for  line in lines:
            if "BTS_IP" in line.upper():
                global ENV_IP
                ENV_IP = line.split('\'')[-2]
            if "BTS_NAME" in line.upper():
                global ENV_NAME
                ENV_NAME = line.split('\'')[-2]
    except Exception, e:
        pass
    finally:
        f.close()


if __name__ == "__main__":
    (ROOT_PATH, PICK_FILE_PATH, BTS_FILE, TARGET_BTS_FILE, LOG_PATH, LOG_LEVEL) = parse_parameters()
    _get_testbed_info()
    case_list = parse_suite_mapping()
    print "case_list: %s"  %case_list
    (cases_dir, backup_dir) = make_new_folder()
    try:
        copy_and_run_cases(case_list, cases_dir, backup_dir)
    except Exception, e:
        print "Error: "
        print e
##    finally:
##        combine_output_file(backup_dir)
    pass
