#!/usr/bin/python
# -*- coding: cp936 -*-

#==============================================================
#       Function:       FileOper.py
#       Author:         Pan Lei , Chen Yali
#       Time:           22/07/2011
#*	*********************************
#*	* 1. Script description:
#*	*********************************
#*	* File operation.
#*	*********************************
#==============================================================
from __future__ import with_statement
import sys, os, time, string, glob, re, shutil, math, copy, datetime
from xlutils.copy import copy
from numpy import *

global CELL_ID_LIST, FILE_TEMPLATE

CELL_ID_LIST = ["12", "13", "14"]

FILE_TEMPLATE = "\
,Antenna Port,Port 1,Port 2,Port 3,Port 4,Port 5,Port 6,Port 7\n\
,,,,,,,,\n\
Cell 1,Rx_Max_ampRatio,11_Rx_Max_ampRatio,12_Rx_Max_ampRatio,13_Rx_Max_ampRatio,14_Rx_Max_ampRatio,15_Rx_Max_ampRatio,16_Rx_Max_ampRatio,17_Rx_Max_ampRatio\n\
,Rx_Min_ampRatio,11_Rx_Min_ampRatio,12_Rx_Min_ampRatio,13_Rx_Min_ampRatio,14_Rx_Min_ampRatio,15_Rx_Min_ampRatio,16_Rx_Min_ampRatio,17_Rx_Min_ampRatio\n\
,Rx_Var_Degree,11_Rx_Var_Degree,12_Rx_Var_Degree,13_Rx_Var_Degree,14_Rx_Var_Degree,15_Rx_Var_Degree,16_Rx_Var_Degree,17_Rx_Var_Degree\n\
,Tx_Max_ampRatio,11_Tx_Max_ampRatio,12_Tx_Max_ampRatio,13_Tx_Max_ampRatio,14_Tx_Max_ampRatio,15_Tx_Max_ampRatio,16_Tx_Max_ampRatio,17_Tx_Max_ampRatio\n\
,Tx_Min_ampRatio,11_Tx_Min_ampRatio,12_Tx_Min_ampRatio,13_Tx_Min_ampRatio,14_Tx_Min_ampRatio,15_Tx_Min_ampRatio,16_Tx_Min_ampRatio,17_Tx_Min_ampRatio\n\
,Tx_Var_Degree,11_Tx_Var_Degree,12_Tx_Var_Degree,13_Tx_Var_Degree,14_Tx_Var_Degree,15_Tx_Var_Degree,16_Tx_Var_Degree,17_Tx_Var_Degree\n\
,,,,,,,,\n\
Cell 2,Rx_Max_ampRatio,21_Rx_Max_ampRatio,22_Rx_Max_ampRatio,23_Rx_Max_ampRatio,24_Rx_Max_ampRatio,25_Rx_Max_ampRatio,26_Rx_Max_ampRatio,27_Rx_Max_ampRatio\n\
,Rx_Min_ampRatio,21_Rx_Min_ampRatio,22_Rx_Min_ampRatio,23_Rx_Min_ampRatio,24_Rx_Min_ampRatio,25_Rx_Min_ampRatio,26_Rx_Min_ampRatio,27_Rx_Min_ampRatio\n\
,Rx_Var_Degree,21_Rx_Var_Degree,22_Rx_Var_Degree,23_Rx_Var_Degree,24_Rx_Var_Degree,25_Rx_Var_Degree,26_Rx_Var_Degree,27_Rx_Var_Degree\n\
,Tx_Max_ampRatio,21_Tx_Max_ampRatio,22_Tx_Max_ampRatio,23_Tx_Max_ampRatio,24_Tx_Max_ampRatio,25_Tx_Max_ampRatio,26_Tx_Max_ampRatio,27_Tx_Max_ampRatio\n\
,Tx_Min_ampRatio,21_Tx_Min_ampRatio,22_Tx_Min_ampRatio,23_Tx_Min_ampRatio,24_Tx_Min_ampRatio,25_Tx_Min_ampRatio,26_Tx_Min_ampRatio,27_Tx_Min_ampRatio\n\
,Tx_Var_Degree,21_Tx_Var_Degree,22_Tx_Var_Degree,23_Tx_Var_Degree,24_Tx_Var_Degree,25_Tx_Var_Degree,26_Tx_Var_Degree,27_Tx_Var_Degree\n\
,,,,,,,,\n\
Cell 3,Rx_Max_ampRatio,31_Rx_Max_ampRatio,32_Rx_Max_ampRatio,33_Rx_Max_ampRatio,34_Rx_Max_ampRatio,35_Rx_Max_ampRatio,36_Rx_Max_ampRatio,37_Rx_Max_ampRatio\n\
,Rx_Min_ampRatio,31_Rx_Min_ampRatio,32_Rx_Min_ampRatio,33_Rx_Min_ampRatio,34_Rx_Min_ampRatio,35_Rx_Min_ampRatio,36_Rx_Min_ampRatio,37_Rx_Min_ampRatio\n\
,Rx_Var_Degree,31_Rx_Var_Degree,32_Rx_Var_Degree,33_Rx_Var_Degree,34_Rx_Var_Degree,35_Rx_Var_Degree,36_Rx_Var_Degree,37_Rx_Var_Degree\n\
,Tx_Max_ampRatio,31_Tx_Max_ampRatio,32_Tx_Max_ampRatio,33_Tx_Max_ampRatio,34_Tx_Max_ampRatio,35_Tx_Max_ampRatio,36_Tx_Max_ampRatio,37_Tx_Max_ampRatio\n\
,Tx_Min_ampRatio,31_Tx_Min_ampRatio,32_Tx_Min_ampRatio,33_Tx_Min_ampRatio,34_Tx_Min_ampRatio,35_Tx_Min_ampRatio,36_Tx_Min_ampRatio,37_Tx_Min_ampRatio\n\
,Tx_Var_Degree,31_Tx_Var_Degree,32_Tx_Var_Degree,33_Tx_Var_Degree,34_Tx_Var_Degree,35_Tx_Var_Degree,36_Tx_Var_Degree,37_Tx_Var_Degree\n"

TOP = "\n\
====================================================================\n\
**               Calibration Tool version 3.6.0                   **\n\
**              Author: Pan Lei <lei.pan@nsn.com>                 **\n\
===================================================================="

TEMPLATE = "\
====================================================================\n\
                     BTS: [BTS_IP]\n\
====================================================================\n\
antennaPort |      1       2       3       4       5       6       7\n\
------------+-------------------------------------------------------\n\
Cell 1      |     11      12      13      14      15      16      17\n\
Cell 2      |     21      22      23      24      25      26      27\n\
Cell 3      |     31      32      33      34      35      36      37\n\
===================================================================="

def FileRead(FileFullPath, ReadMode = 'r'):
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

def FileWrite(FileFullPath, FileContent, WriteMode = 'w'):
    """Write content to File

    Input:
        [1]: FileContent: a sequence of strings to write the file
        [2]: FileFullPath: file to wirte
        [3]: WriteMode: e.g 'w', 'a' for normal use, 'wb'/'ab' for bin file, 'wu'/'au' for Unix file
    Output:
        [1]: EReturnSuccess: write sucessfully
              Other: write fail
    """
    #Check input argv
    p_FileName = FileFullPath
    p_DirName = os.path.dirname(p_FileName)
    
    if not (isinstance(FileContent, list) or isinstance(FileContent, str)):
        print "Fail to write file: %s, file content: %s must be list or string" % (p_FileName, FileContent)
        return False
    if os.path.isfile(p_FileName):
        #print "File: %s has existed, may be overwrited" % (p_FileName)
        pass
    elif os.path.isdir(p_DirName):
        #print "Parent dir: %s is exist" % (p_DirName)
        pass
    else:
        #print "Parent dir: %s is not exist, try to create it" % (p_DirName)
        DirCreate(p_DirName)        
    try:
        with open(p_FileName, WriteMode) as p_FileObj:
            p_FileObj.writelines(FileContent)
    except:
        print "Write file %s failed!" % (FileFullPath)
        return False
    #print "Succeed to write file: %s"% (p_FileName)
    return True


def DirCreate(DirFullName):
    """Creat a directory, makes all intermediate-level directories contain the leaf directory.

    Input:[1] p_DirFullName: full path name of directory
    Notes: If directory existed, return 1 directly.
    """
    p_DirFullName = DirFullName

    if os.path.isdir(p_DirFullName):
        #print "File %s has existed" % (p_DirFullName)
        return False
    try:
        os.makedirs(p_DirFullName)
    except:
        print "Creat directory %s fail"% (p_DirFullName)
        return False
    #print "Creat directory %s OK"% (p_DirFullName)
    return True

def startBtslog():
    os.system("TASKKILL /F /IM btslog.exe")
    btslog_dir = "\"C:\\Program Files\\BTSlog\\btslog.exe\""
    cmd = btslog_dir + " " + "start_udplog"
    os.system(cmd)
    #connections.execute_shell_command_without_check(cmd)

def stop_btslog():
    os.system("TASKKILL /F /IM btslog.exe")

def get_last_modified_file(file_pattern=""):
    """
    | file_pattern | No | File pattern for file filtering, default is for Counter file |
    | Return value | The absolute file path of last modified file |
    """
    BTSLOG_DIR = 'C:\\temp\\BTSlogs\\'
    file_ext   = 'LOG'

    ret = connections.execute_shell_command('dir /A /B /O-D "%s"' % BTSLOG_DIR)
    lines = ret.splitlines()
    match_pattern = file_pattern == '' and '.' or '^.*%s' % file_pattern

    for line in lines:
        try:
            (file_name, file_extention) = line.split('.')
            print file_extention
            if file_extention == file_ext and re.match(match_pattern, line):
                return os.path.join(BTSLOG_DIR, line)
        except ValueError:
            pass

def file_copy(source_file_dir, dest_file_dir):
    """This keyword copies source file to destination directory.
    | File Copy | C:\Master_Configuration.xml | D:\configuration_file |
    """

    try:
        shutil.copy(source_file_dir, dest_file_dir)
    except:
        raise Exception, "File '%s' copied to '%s' failed" % (source_file_dir, dest_file_dir)

def decode_udplog(file_content):
    """
    decode_result = {"192.168.1.1": [(direction, cell, antenna, timeoffset, phase, ampRatio), (direction, cell, antenna, timeoffset, phase, ampRatio), ...],
                    "13.12.12.4": [(direction, cell, antenna, timeoffset, phase, ampRatio), (direction, cell, antenna, timeoffset, phase, ampRatio), ...],
                    ....
                    }
    """
    lines = file_content
    pattern = "FSP.*AntIdx"

    decode_result = {}
    
    try:
        for line in lines:
            if "TC:" in line:
##                tx_search_result = re.search('^(\d+).*FSP-(\d{2})44.*AntIdx\((\d+)\).*TimeOff=.*(\d+).*antPhaseOff=.*(\d+\.\d+).*, AmpRatio=.*(\d+\.\d+).*finalAmpRatio', line)
##                tx_search_result = re.search('^(\d+).*FSP-(\d{2})44.*AntIdx\((\d+)\).*TimeOff=([0-9\-]+).*antPhaseOff=([0-9.\-]+).*maxTxAntAmpRatio=([0-9.\-]+[0-9])', line)
                #tx_search_result = re.search('\[(\d+.\d+.\d+.\d+)\].*FSP-(\d{2}).*\sAntIdx\((\d+)\).*\sTimeOff=([0-9\-]+).*\santPhaseOff=([0-9.\-]+).*\sAmpRatio=([0-9.\-]+),', line)
                tx_search_result = re.search('\[(\d+.\d+.\d+.\d+)\].*FSP-(\d{2}).*,\s*AntIdx\((\d+)\).*:\s*TimeOff=([0-9\-]+).*,\s*antPhaseOff=([0-9.\-]+).*,\s*AmpRatio=([0-9.\-]+)\s*,', line)
                if tx_search_result:
                    direction = 'tx'
                    ip = tx_search_result.groups()[0]
                    cell = tx_search_result.groups()[1]
                    antenna = tx_search_result.groups()[2]
                    timeoffset = round(float(tx_search_result.groups()[3]), 4)
                    phase = round(float(tx_search_result.groups()[4]), 4)
                    ampRatio = abs(round(float(tx_search_result.groups()[5]), 4))

                    if decode_result.has_key(ip):
                        decode_result[ip].append((direction, cell, antenna, timeoffset, phase, ampRatio))
                    else:
                        decode_result[ip] = [(direction, cell, antenna, timeoffset, phase, ampRatio)]
                    
            elif "RC:" in line:
##                rx_search_result = re.search('^(\d+).*FSP-(\d{2})41.*antennaIndex=(\d+).*TimeOffet=.*(\d+).*antPhaseOff=.*(\d+\.\d+).*, antAmpRatio=.*(\d+\.\d+).*finalAntAmpRatio', line)
##                rx_search_result = re.search('^(\d+).*FSP-(\d{2})41.*antennaIndex=(\d+).*TimeOffet=([0-9\-]+).*antPhaseOff=([0-9.\-]+).*maxRxAntAmpRatio=([0-9.\-]+[0-9])', line)
                #rx_search_result = re.search('\[(\d+.\d+.\d+.\d+)\].*FSP-(\d{2}).*\santennaIndex=(\d+).*\sTimeOffet=([0-9\-]+).*\santPhaseOff=([0-9.\-]+).*\santAmpRatio=([0-9.\-]+),', line)
                rx_search_result = re.search('\[(\d+.\d+.\d+.\d+)\].*FSP-(\d{2}).*,\s*antennaIndex=(\d+).*,\s*TimeOffet=([0-9\-]+).*,\s*antPhaseOff=([0-9.\-]+).*,\s*antAmpRatio=([0-9.\-]+)\s*,', line)
                if rx_search_result:
                    direction = 'rx'
                    ip = rx_search_result.groups()[0]
                    cell = rx_search_result.groups()[1]
                    antenna = rx_search_result.groups()[2]
                    timeoffset = round(float(rx_search_result.groups()[3]), 4)
                    phase = round(float(rx_search_result.groups()[4]), 4)
                    ampRatio = abs(round(float(rx_search_result.groups()[5]), 4))

                    if decode_result.has_key(ip):
                        decode_result[ip].append((direction, cell, antenna, timeoffset, phase, ampRatio))
                    else:
                        decode_result[ip] = [(direction, cell, antenna, timeoffset, phase, ampRatio)]
        return decode_result

    except Exception, e:
        print line
        raise Exception,  "Decode udplog fail: %s" % e
        return {}
    
def check_phase_amp(decode_list, cell, antenna):
    global FILE_TEMPLATE

    Rx_Max_ampRatio = None
    Rx_Min_ampRatio = None
    Rx_Var_Degree = None
    Tx_Max_ampRatio = None
    Tx_Min_ampRatio = None
    Tx_Var_Degree = None
    
    phase_Rx = []
    ampRatio_Rx = []
    timeoffset_Rx = []
    
    phase_Tx = []
    ampRatio_Tx = []
    timeoffset_Tx = []

    try:
        for decode_info in decode_list:
            (direction, cell_id, antenna_id, timeoffset, phase, ampRatio) = decode_info
            if (cell_id == CELL_ID_LIST[int(cell) - 1]) and (antenna_id == antenna): # cell + antenna
                if direction == 'rx': # receive
                    phase_Rx.append(phase)
                    ampRatio_Rx.append(ampRatio)
                    timeoffset_Rx.append(timeoffset)

                elif direction == 'tx': # transmit
                    phase_Tx.append(phase)
                    ampRatio_Tx.append(ampRatio)
                    timeoffset_Tx.append(timeoffset)

    except Exception, e:
        raise Exception,  "Analyze udplog fail: %s" % e

    def _calc_degree(a, b):
        delta = a - b
        if delta > 180:
            delta = delta - 360
        elif delta < -180:
            delta = delta + 360
        return delta
   
    if len(phase_Rx) > 0:
        Rx_Max_ampRatio = max(ampRatio_Rx)
        Rx_Min_ampRatio = min(ampRatio_Rx)

        Delta_timeoffset_Rx = [timeoffset_Rx[i + 1] - timeoffset_Rx[i] for i in xrange(len(timeoffset_Rx) - 1)]
        Delta_phase_Rx = [_calc_degree(phase_Rx[i + 1], phase_Rx[i])  for i in xrange(len(phase_Rx) - 1)]
        
        Rx_Var_TimeOffset = var(array(Delta_timeoffset_Rx))
        Rx_Var_phase = var(array(Delta_phase_Rx))
        Rx_Var_Degree = round(math.sqrt(COEFF * Rx_Var_TimeOffset + Rx_Var_phase), 2)
        
        FILE_TEMPLATE = FILE_TEMPLATE.replace("%s%s_Rx_Max_ampRatio" % (cell, antenna), str(Rx_Max_ampRatio))
        FILE_TEMPLATE = FILE_TEMPLATE.replace("%s%s_Rx_Min_ampRatio" % (cell, antenna), str(Rx_Min_ampRatio))
        FILE_TEMPLATE = FILE_TEMPLATE.replace("%s%s_Rx_Var_Degree" % (cell, antenna), str(Rx_Var_Degree))
        
        print "      Range of Rx_ampRatio is [%s, %s]!" % (Rx_Min_ampRatio, Rx_Max_ampRatio)
        print "      Rx_Var_Degree: y = %s" % Rx_Var_Degree
        
    else:

        FILE_TEMPLATE = FILE_TEMPLATE.replace("%s%s_Rx_Max_ampRatio" % (cell, antenna), "--")
        FILE_TEMPLATE = FILE_TEMPLATE.replace("%s%s_Rx_Min_ampRatio" % (cell, antenna), "--")
        FILE_TEMPLATE = FILE_TEMPLATE.replace("%s%s_Rx_Var_Degree" % (cell, antenna), "--")
        
        print "      No Rx signal"

  
    if len(phase_Tx) > 0:

        Tx_Max_ampRatio = max(ampRatio_Tx)
        Tx_Min_ampRatio = min(ampRatio_Tx)
        
        Delta_timeoffset_Tx = [timeoffset_Tx[i + 1] - timeoffset_Tx[i] for i in xrange(len(timeoffset_Tx) - 1)]
        Delta_phase_Tx = [_calc_degree(phase_Tx[i + 1], phase_Tx[i]) for i in xrange(len(phase_Tx) - 1)]
        
        Tx_Var_TimeOffset = var(array(Delta_timeoffset_Tx))
        Tx_Var_phase = var(array(Delta_phase_Tx))
        Tx_Var_Degree = round(math.sqrt(COEFF * Tx_Var_TimeOffset + Tx_Var_phase), 2)
        
        FILE_TEMPLATE = FILE_TEMPLATE.replace("%s%s_Tx_Max_ampRatio" % (cell, antenna), str(Tx_Max_ampRatio))
        FILE_TEMPLATE = FILE_TEMPLATE.replace("%s%s_Tx_Min_ampRatio" % (cell, antenna), str(Tx_Min_ampRatio))
        FILE_TEMPLATE = FILE_TEMPLATE.replace("%s%s_Tx_Var_Degree" % (cell, antenna), str(Tx_Var_Degree))
        
        print "      Range of Tx_ampRatio is [%s, %s]!" % (Tx_Min_ampRatio, Tx_Max_ampRatio)
        print "      Tx_Var_Degree: y = %s" % Tx_Var_Degree
        
    else:

        FILE_TEMPLATE = FILE_TEMPLATE.replace("%s%s_Tx_Max_ampRatio" % (cell, antenna), "--")
        FILE_TEMPLATE = FILE_TEMPLATE.replace("%s%s_Tx_Min_ampRatio" % (cell, antenna), "--")
        FILE_TEMPLATE = FILE_TEMPLATE.replace("%s%s_Tx_Var_Degree" % (cell, antenna), "--")
        
        print "      No Tx signal"
        
    
    if None not in [Rx_Max_ampRatio, Rx_Max_ampRatio, Rx_Var_Degree, Tx_Max_ampRatio, Tx_Max_ampRatio, Tx_Var_Degree]:
        
        if Tx_Var_Degree > 5.7:
            raise Exception,  "Variance of Calibration degree of Cell %s antenna %s tranmit: %s > 5.7 !" \
                              %(cell, antenna, Tx_Var_Degree)

        
        if (Tx_Max_ampRatio > 1.404) or (Tx_Min_ampRatio < 0.7079):
            raise Exception,  "Cell %s antenna %s transmit: AmpRatio range [%s, %s] beyonds limitaion [0.7079, 1.404] !" \
                              %(cell, antenna, Tx_Min_ampRatio, Tx_Max_ampRatio)
        
        if Rx_Var_Degree > 5.7:
            raise Exception,  "Variance of Calibration degree of Cell %s antenna %s receive: %s > 5.7 !" \
                              %(cell, antenna, Rx_Var_Degree)

        if (Rx_Max_ampRatio > 1.404) or (Rx_Min_ampRatio < 0.7079):
            raise Exception,  "Cell %s antenna %s receive: AmpRatio range [%s, %s] beyonds limitaion [0.7079, 1.404] !" \
                              %(cell, antenna, Rx_Min_ampRatio, Rx_Max_ampRatio)
            
        return "OK"

    else:

        return "--"

if __name__=='__main__':
    
    #startBtslog()
    #time.sleep(60) #
    #stop_btslog()
    #path = get_last_modified_file()
    #file_copy(path, 'D:\\udplog\\udp.log')
    import copy

    ret_value = 0
    
    
    try:
        try:
            logpath = sys.argv[1]
        except:
            raise Exception, "Missing 1st parameter: <UDP log path>."

        if logpath in ['-h', '--help']:
            print "Usage:"
            print "    [Calibration.exe] <Full path of log> <bandwidth:10/20>"
            print "           e.g.  C:\Calibration.exe C:\udp_1.log 20"   
            sys.exit(3)
        try:
            bandwidth = int(sys.argv[2])
        except:
            raise Exception, "Missing 2nd parameter: <Bandwidth>."
        
        if bandwidth == 20:
            COEFF = 0.0042
        elif bandwidth == 10:
            COEFF = 0.00105
        else:
            raise Exception, "Wrong Bandwidth, should be 10 or 20."
    except Exception, e:
        print e
        print "Error CLI command format! The command format should be:"
        print "    [Calibration.exe] <Full path of log> <bandwidth:10/20>"
        print "           e.g.  C:\Calibration.exe C:\udp_1.log 20"
        sys.exit(2)
        
    file_handle = None
    
    try:
        file_handle = file(logpath, 'rb')
        file_content = file_handle.readlines()
    except:
        raise Exception, "Open file '%s' failed" % (logpath)
    finally:
        if file_handle:
            file_handle.close()
    decode_result = decode_udplog(file_content)
    #print decode_result

    print TOP

    origin_FILE_TEMPLATE = copy.deepcopy(FILE_TEMPLATE)
    
    for bts_ip in decode_result.keys():
        print "\n------------------Start to check BTS %s------------------" % bts_ip
        temp_TEMPLATE = copy.deepcopy(TEMPLATE)
        FILE_TEMPLATE = copy.deepcopy(origin_FILE_TEMPLATE)
        for cell_id in [1, 2, 3]:
            for ant_idx in ['1', '2', '3', '4', '5', '6', '7']:
                try:
                    print "[INFO] BTS: %s, Start to check Cell %s antenna %s..."  % (bts_ip, cell_id, ant_idx)
                    result = check_phase_amp(decode_result[bts_ip], cell_id, ant_idx)
                    temp_TEMPLATE = temp_TEMPLATE.replace("%s%s" % (cell_id, ant_idx), result)
                    
                    print "      -> Cell %s antenna %s Calibration check result: %s!"   % (cell_id, ant_idx, result)
                except Exception,e:
                    temp_TEMPLATE = temp_TEMPLATE.replace("%s%s" % (cell_id, ant_idx), 'NO')
                    print "      %s" % e
                    print "      -> Cell %s antenna %s Calibration check failed!"   % (cell_id, ant_idx)


        print temp_TEMPLATE.replace('[BTS_IP]', bts_ip)
        # write calibration result file
        FileWrite(os.path.join(os.path.dirname(logpath), "calibration_summary.log"), "\n\nLogging time: %s\n" % datetime.datetime.now(), 'a')
        FileWrite(os.path.join(os.path.dirname(logpath), "calibration_summary.log"), temp_TEMPLATE.replace('[BTS_IP]', bts_ip), 'a')
        
        print "%s records per cell*antenna were found!" % (len(decode_result[bts_ip])/(21 - temp_TEMPLATE.count(" -- ")))
        # generate record file
        print "Summary csv located:"
        print "-> %s" % os.path.join(os.path.dirname(logpath), "result_%s.csv" % bts_ip)
        print "Source analyzed data located:"
        print "-> %s" % os.path.join(os.path.dirname(logpath), "sourceData_%s.csv" % bts_ip)
        #write result.csv
        FileWrite(os.path.join(os.path.dirname(logpath), "result_%s.csv" % bts_ip), FILE_TEMPLATE)
        
        # write sourceData.csv
        log_content = ["direction, cell_id, antenna_id, timeoffset, phase, ampRatio\n"]
        for decode_info in decode_result[bts_ip]:
            (direction, cell_id, antenna_id, timeoffset, phase, ampRatio) = decode_info
            log_content.append(string.join([direction, cell_id, antenna_id, str(timeoffset), str(phase), str(ampRatio)], ',') + '\n')

        FileWrite(os.path.join(os.path.dirname(logpath), "sourceData_%s.csv" % bts_ip), log_content)

        if ('NO' in temp_TEMPLATE) or not ('OK' in temp_TEMPLATE):
            ret_value += 1



    print "\
====================================================================\n\
**                    Algorithm of Calibration                    **\n\
====================================================================\n\
  0.7079 < |AmpRatio| < 1.404\n\
  if 10MHz:\n\
sqrt((2*0.0009*18)^2*Var(Delta_TimeOff)+Var(Delta_antPhaseOff))<5.7\n\
  if 20MHz:\n\
sqrt((2*0.0018*18)^2*Var(Delta_TimeOff)+Var(Delta_antPhaseOff))<5.7\n\
  ----\n\
  Delta_TimeOff = TimeOff(n) - TimeOff(n - 1)\n\
  Delta_antPhaseOff = Degree_Delta (antPhaseOff(n), antPhaseOff(n-1))\n\
===================================================================="

    # return
    sys.exit(ret_value)



                






