from __future__ import with_statement

import os
import sys
import re
import glob
import zipfile
import ConfigParser
import csv
import time
import getopt
import subprocess


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

def record_local_time():
    """ record_local_time
    """
    ret = ''
    for value in time.localtime()[3:6]:
        temp = str(value)
        ret = ret + ":" + temp
    local_time = "local" + ret
    
    return local_time
'''
def read_output_and_analyze(output_file_path):

    Result = {}
    flag = 0
    try:
        output_content = file_read(output_file_path)
        print "read content from output.txt successfully!"
    except:
        raise Exception, "read content from output.txt failed!"
    for line in output_content:
        if 'command :uptime   return is ->' in line and 'load average:' in line and 'failed' not in line:
            Result[str(line.split(':')[0])] = str(line.split('up')[-1].split('load average:')[0]).replace(",", " ").replace(' ', '')
            if flag == 0:
                Result['bbuip'] = str(line.split('up')[-2].split('return is ->')[-1]).replace(' ', '')
                flag = 1
                
                
        if 'failed!' in line:
            Result[str(line.split(':')[0])] = 'failed'
            
    if flag == 0:
        Result['bbuip'] = record_local_time()
   
    return Result
    '''
    
def dir_create(DirFullName):
    """Creat a directory, makes all intermediate-level directories contain the leaf directory.

    Input:[1] p_DirFullName: full path name of directory
    Notes: If directory existed, return 1 directly.
    """
    p_DirFullName = DirFullName
    if os.path.isdir(p_DirFullName):
        print "Dir %s has existed" % (p_DirFullName)
        return False
    try:
        os.makedirs(p_DirFullName)
    except:
        print "Creat directory %s fail" % (p_DirFullName)
        return False
    print "Creat directory %s OK" % (p_DirFullName)
    return True

    
def normalize_content(content):
    
    returnlist = []
   
    for i in range(len(content)):
        ip = content[i].split("\n")[0].strip()
        if(len(ip) >=7):
            returnlist.append(ip)

    return returnlist

def create_csv_file(csv_file_path, kw_list):
    
    try:
        with open(csv_file_path, 'wb') as csvfile:
            sp = csv.writer(csvfile, dialect = 'excel')
        #    kw_list.insert(0, 'bbuip')
            sp.writerow(kw_list)
            print "create new techlogs.csv file successfully!"
    except Exception, s:
        print s
        raise Exception,"Create new techlogs.csv file error!try again!"
   

def read_write_techlogs_csv(ip_value, csv_file_path, kw_dict):

    try:
        with open(csv_file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile, dialect = 'excel')
            line_list = [ln for ln in reader]
    except Exception, s:
        print s
        raise Exception,"Read content from techlogs.csv file error!try again!"
    
    row = len(line_list)
    first_list = line_list[0]
    column = len(first_list)
    last_line = []
    for i in range(column):
        last_line.append('')

    for kw in kw_dict.keys():
        if kw in first_list:
            index = first_list.index(kw)
            last_line[index] = kw_dict[kw]
        else:
            first_list.append(kw)
            last_line.append(kw_dict[kw])
            
    last_line[0] = ip_value
    line_list.append(last_line)

    try:
        with open(csv_file_path, 'wb') as csvfile:
            sp = csv.writer(csvfile, dialect = 'excel')
            for con in line_list:
                sp.writerow(con)
            print "Write content to techlogs.csv successfully!"
            
    except Exception, s:
        print s
        raise Exception,"Write content to techlogs.csv file error!try again!"
    
def read_write_csv(csv_file_path, content, option):

    if option == 'uptime':
        try:
      #      judge_csv_exist(csv_file_path)      # judge if csv file is existed
            with open(csv_file_path, 'rb') as csvfile:
                reader = csv.reader(csvfile, dialect = 'excel')
                line_list = [ln for ln in reader]
        except Exception, s:
            print s
            raise Exception,"Read content from uptime.csv file error!try again!"
        
        row = len(line_list)
        first_list = line_list[0]
        column = len(first_list)
        last_line = []
        for i in range(column):
            last_line.append('')

        for ip in content.keys():
            if ip in first_list:
                index = first_list.index(ip)
                last_line[index] = content[ip]
            else:
                first_list.append(ip)
                last_line.append(content[ip])
                
      #  update_time = str(time.strftime('%Y_%m_%d %H:%m:%S'))
        last_line[0] = content['bbuip']
        line_list.append(last_line)

        try:
            with open(csv_file_path, 'wb') as csvfile:
                sp = csv.writer(csvfile, dialect = 'excel')
                for con in line_list:
                    sp.writerow(con)
                print "Write content to uptime.csv successfully!"
                
        except Exception, s:
            print s
            raise Exception,"Write content to uptime.csv file error!try again!"
    elif option == 'search':
        te = []
        te.append('bbuip')
        try:
            config_file_name = read_config("search", "file_name")
            file_name = config_file_name.strip("\"")
            file_name_list = file_name.split(",")
        except Exception,e:
            result = "read file name and path from config.ini error,please check!"
            print e
            raise Exception,result
        head_list = te + file_name_list
        try:
            with open(csv_file_path, 'wb') as csvfile:
                sp = csv.writer(csvfile, dialect = 'excel')
                sp.writerow(head_list)
                for ip in content.keys():
                    temp = []
                    write_content = []
                    temp.append(ip)
                    write_content = temp + content[ip]
                    sp.writerow(write_content)
                print "Write content to search.csv successfully!"
                
        except Exception, s:
            print s
            raise Exception,"Write content to search.csv file error!try again!"
    elif option == 'sysinfo':
        
        head_list = ['bbuip', 'SFP', 'Vendor_PN', 'Vendor_name', 'Wavelength', 'Vendor_SN']
        try:
            with open(csv_file_path, 'wb') as csvfile:
                sp = csv.writer(csvfile, dialect = 'excel')
                sp.writerow(head_list)
                for ip in content.keys():
                    temp = []
                    for i in range(0, len(content[ip]), 5):
                        temp.append(content[ip][i:i+5])
                    for j in range(len(temp)):
                        temp[j].insert(0, ip)
                        sp.writerow(temp[j])
                print "Write content to sysinfo_SFP.csv successfully!"
                
        except Exception, s:
            print s
            raise Exception,"Write content to sysinfo_SFP.csv file error!try again!"

def read_output_and_analyze(output_file_path, option):
    
    Result = {}
    try:
        output_content = file_read(output_file_path)
        print "read content from output.txt successfully!"
    except:
        raise Exception, "read content from output.txt failed!"

    if option == 'uptime':
        
        flag = 0
        for line in output_content:
            if 'command :uptime   return is ->' in line and 'load average:' in line and 'failed' not in line:
                Result[str(line.split(':')[0])] = str(line.split('up')[-1].split('load average:')[0]).replace(",", " ").replace(' ', '')
                if flag == 0:
                    Result['bbuip'] = str(line.split('up')[-2].split('return is ->')[-1]).replace(' ', '')
                    flag = 1
                    
                    
            if 'failed!' in line:
                Result[str(line.split(':')[0])] = 'failed'
                
        if flag == 0:
            Result['bbuip'] = record_local_time()
    elif option == 'search':
        try:
            config_file_name = read_config("search", "file_name")
            file_name = config_file_name.strip("\"")
            file_name_list = file_name.split(",")
        except Exception,e:
            result = "read file name and path from config.ini error,please check!"
            print e
            raise Exception,result
        value_list = ['failed'] * len(file_name_list)
        ip_name = ''
        for line in output_content:
            if 'action information as below:' not in line:
                if ip_name == '':
                    ip_name = str(line.split(':')[0].strip(" "))
                if 'failed' not in line and str(line.split(':')[-1].split('=')[0].strip(" ")) in file_name_list:
                    value_list[file_name_list.index(str(line.split(':')[-1].split('=')[0].strip(" ")))] = str(line.split('=')[-1].strip(" ").strip("\n"))

                Result[ip_name] = value_list
            else:
                value_list = ['failed'] * len(file_name_list)
                ip_name = ''
                
    return Result

def read_config(section, item):

    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    value = config.get(section, item)

    return value

def check_filter_in_zip_list(z, ip_path, total_name_list, filter_list):

    ret = []
    result = {}
    for i in filter_list:
        result[i] = 0
    try:
        for f in total_name_list:
            if f.endswith('_pm_1_system.log.zip') or f.endswith('_pm_2_system.log.zip') \
               or f.endswith('_runtime.zip') or f.endswith('_startup.zip'):
                ret.append(f)
                outfile = open(os.path.join(ip_path, "temp.zip"), 'wb')
                outfile.write(z.read(f))
                outfile.close()
                z_temp = zipfile.ZipFile(os.path.join(ip_path, "temp.zip"), mode = 'r')
                try:
                    for real_file in z_temp.namelist():
                        content = z_temp.read(real_file)
                        for kw in filter_list:
                            num = content.count(kw)
                            result[kw] = result[kw] + num
                finally:
                    z_temp.close()
                    os.remove(os.path.join(ip_path, "temp.zip"))
    except Exception, e:
        print e

    print ret
    print len(ret)
    print result
    return result

def check_filter_in_log_list(z, total_name_list, filter_list):

    print filter_list
    ret = []    
    result = {}
    for i in filter_list:
        result[i] = 0
    try:
        for f in total_name_list:
            if f.endswith('61_runtime.log'):
                ret.append(f)
                content = z.read(f)
                for kw in filter_list:
                    num = content.count(kw)
                    result[kw] = result[kw] + num
    except Exception, e:
        print e
        
    print ret
    print len(ret)
    print result
    return result

def writec_csv_output_file(ip_value, index, kw_dict, output_path):
    
    #output.txt information
    try:
        file_write(output_path, "NO.%s action information as below: ============================================\n" % index, 'a')
        buf = ip_value + ": "
        con = ' '
        for value in kw_dict.keys():
            con = con + value + "=" + str(kw_dict[value]) + "  "
        file_write(output_path, buf + con + '\n', 'a')
        
    except Exception, e:
        print e

def make_download_folder(current_dir):
    """ make one download folder with local time stamp
    """
    
    ret = ''
    for value in time.localtime()[0:6]:
        temp = str(value)
        ret = ret + "_" + temp
    file_name = "download_" + ret
    download_path = os.path.join(current_dir, file_name)
    dir_create(download_path)
    
    return download_path

def write_config(section, item, value):
    
    config = ConfigParser.ConfigParser()
    if not os.path.isfile("config.ini"):
        raise "Please put config.ini file in your current dir try again!"
    config.read("config.ini")
    config.set(section, item, value)

    f = open ("config.ini", "r+")
    config.write(f)
    f.close
    
def execute_subprocess(cmd, check_point):

    try:
    #    print cmd
        ret = os.popen(cmd).read()
        print ret
        
        if isinstance(ret, str):
            ret = ''
            flag = 0
            for value in ret.split("\n"):
                if re.search(check_point, value):
                    flag = 1
                    ret = check_point
                    print "Find %s in stout!\n" % check_point
                    break;
            if 0 == flag :
                ret = "Coundn't find %s in stout!\n" % check_point
                print ret
                raise ret
            
        if isinstance(ret, list):
            ret = []
            for p in check_point:
                flag = 0
                for value in ret.split("\n"):
                    if re.search(p, value):
                        flag = 1
                        ret.append(p)
                        print "Find %s in stout!\n" % (p)
                        break
                if flag == 0:
                    print "Coundn't find %s in stout!\n" % p
            if ret == []:
                ret = "Coundn't find any check point in stout!\n"
                print ret
                raise ret
                
            
    except Exception, e:
        print e

    return ret

def fetch_techlogs(saved_path):

    username = "toor4nsn"
    password = "oZPS0POrRieRtu"
    
    bbuip_path = os.path.join(os.path.dirname(saved_path),"bbuip.txt")
    out_path = os.path.join(os.path.dirname(saved_path),"output.txt")
    
    cmd = 'collectfiles.bat -pw Nemuadmin:nemuuser -ssh ' + username + ':' + password + \
          ' -ipfile ' + bbuip_path + ' -dir -fullCoverage -outDir ' + saved_path + ' -timeout 2400'
    
    bbuip_content = file_read(bbuip_path)
    content = normalize_content(bbuip_content)
    if [] == content:
        raise "your bbuip.txt is empty,please check!"
    
    check_list = []
    for i in content:
        info = 'Successfully got technical logs from ' + i
        check_list.append(info)
    print check_list
    
    try:
        print "start to execute subprocess......"
        ret = execute_subprocess(cmd, check_list)
        print "start to write output log........."
        write_fetch_output(out_path, ret)
    except Exception, e:
        print e
        raise e
                    

def select_action():

    current_dir = os.path.abspath(os.curdir)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:a:")
        for op, value in opts:
            if '-d' == op:
                download_save = make_download_folder(current_dir)
                if ':techlogs' == value:
                    print "download filter log only"
                    write_config("system","download_folder_name", os.path.basename(download_save))
                    print "write download_save folder name to config successfully!"
                    try:
                        fetch_techlogs(download_save)
                        print "@action done@"
                    except Exception, e:
                        print e
                        raise e
            if '-a' == op:
                if ':techlogs' == value:
                    download_folder = read_config("system", "download_folder_name")
                    download_path = os.path.join(current_dir, download_folder)
                    ip_path_list = glob.glob(os.path.join(download_path, "*"))
                    try:
                        analyze_action(ip_path_list)
                        print "@action done@"
                    except Exception, s:
                        print s
                        raise s
                elif ':search' == value:
                    output_file_path = os.path.join(current_dir, "output.txt")
                    csv_file_path = os.path.join(current_dir, "search.csv")
                    try:
                        read_write_csv(csv_file_path, read_output_and_analyze(output_file_path, 'search'), 'search')
                        print "@action done@"
                    except Exception, s:
                        print s
                        raise s
                elif ':sysinfo' == value:
                    download_folder = read_config("system", "download_folder_name")
                    download_path = os.path.join(current_dir, download_folder)
                    ip_path_list = glob.glob(os.path.join(download_path, "*"))
                    try:
                        read_write_file_csv(ip_path_list, 'sysinfo')
                        print "@action done@"
                    except Exception, s:
                        print s
                        raise s
                    
    except getopt.GetoptError, e:
        print e

def write_fetch_output(output_path, content):

    index = 0
    try:
        file_write(output_path, '')
        for index in range(len(content)):
            file_write(output_path, "NO.%s action information as below: ============================================\n" % (index + 1), 'a')
            file_write(output_path, content[index] + '\n', 'a') 
        
    except Exception, e:
        print e 
            

def analyze_action(ip_path_list):

    kw_dict = {}
    print read_config("filter", "filter").strip("\"")
    kw_list = read_config("filter", "filter").strip("\"").split(",")
    for kw in kw_list:
        if kw == '' or kw == ' ' or kw == '  ':
            kw_list.remove(kw)
            
    kw_list.insert(0, 'bbuip')      
    print kw_list
    print "starting..............................."
    
    current_dir = os.path.abspath(os.curdir)
    output_path = os.path.join(current_dir, "output.txt")
    techlogs_csv_path = os.path.join(current_dir, "techlogs.csv")
    file_write(output_path, '')

    try:
        create_csv_file(techlogs_csv_path, kw_list)
    except Exception, e:
        print e

    try:
        ip_index = 0
        for ip_path in ip_path_list:
            for kw in kw_list:
                kw_dict[kw] = 0
            
            print "***************************************************"
            print kw_dict
            print "do action in ip folder: %s ............" % (ip_path)
            zip_path = glob.glob(os.path.join(ip_path, "*TSLogFiles.zip"))
            print zip_path
            if 1 == len(zip_path):
                print zip_path[0]
                try:
                    z = zipfile.ZipFile(zip_path[0],mode = 'r')
                    try:
                        print "check in log......................"
                        kw_dict_log = check_filter_in_log_list(z, z.namelist(), kw_dict.keys())
                        print "check in zip......................"
                        kw_dict_zip = check_filter_in_zip_list(z, ip_path, z.namelist(), kw_dict.keys())
                        print "========================="
                    finally:
                        z.close()
                    for i in kw_dict.keys():
                        kw_dict[i] = kw_dict_log[i] + kw_dict_zip[i]
                    print kw_dict
                    ip_index = ip_index + 1
                    writec_csv_output_file(os.path.basename(ip_path), ip_index, kw_dict, output_path)
                    read_write_techlogs_csv(os.path.basename(ip_path), techlogs_csv_path, kw_dict)
                except Exception, e:
                    print e
            else:
                print "zip_path is error!"
    except Exception, e:
        print e

def read_write_file_csv(ip_path_list, selection):

    Result = {}
    if selection == 'sysinfo':
        try:
            for ip_path in ip_path_list:
                file_list = glob.glob(os.path.join(ip_path, "*"))
                if file_list == []:
                     print "There is no file in %s !" % (ip_path) 
                else:
                    info_list = get_info(ip_path, selection)
                    Result[os.path.basename(ip_path)] = info_list
                    
            read_write_csv(os.path.join(os.path.abspath(os.curdir), "sysinfo_SFP.csv"), Result, selection)
            
        except Exception, e:
            print e

def get_info(ip_path, selection):

    if selection == 'sysinfo':
        try:
            if os.path.exists(os.path.join(ip_path, "sysinfo.txt")):
                print "support RL25 sysinfo.txt analyze!"
                file_lines = file_read(os.path.join(ip_path, "sysinfo.txt"))
            elif os.path.exists(os.path.join(ip_path, "sysinfo")):
                print "support RL35 sysinfo analyze!"
                file_lines = file_read(os.path.join(ip_path, "sysinfo"))
            else:
                print "No sysinfo or sysinfo.txt found!"
                file_lines = ''
        except Exception, e:
            print e
        value_list = []
        for line in file_lines:
            if line.startswith('SFP_MODULES_') and '/sys/class/sfp/sfp_' in line:
                value = line.split('/sys/class/sfp/')[-1].split(":")[0].strip(" ")
                value_list.append(value)
            if line.startswith('SFP_MODULES_') and 'base_id/Vendor_PN' in line:
                value = line.split('base_id/Vendor_PN')[-1].split("'")[0].strip(" ")
                value_list.append(value)
            if line.startswith('SFP_MODULES_') and 'base_id/Vendor_name' in line:
                value = line.split('base_id/Vendor_name')[-1].split("'")[0].strip(" ")
                value_list.append(value)
            if line.startswith('SFP_MODULES_') and 'base_id/Wavelength' in line:
                value = line.split('base_id/Wavelength')[-1].split("'")[0].strip(" ")
                value_list.append(value)
            if line.startswith('SFP_MODULES_') and 'extended_id/Vendor_SN' in line:
                value = line.split('extended_id/Vendor_SN')[-1].split("'")[0].strip(" ")
                value_list.append(value)
    return value_list
    

if __name__ == '__main__':

    try:
        select_action()
    except Exception, e:
        raise e
        
    pass
