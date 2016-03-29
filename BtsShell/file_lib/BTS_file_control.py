import os
import re
import sys
import time
import types
import shutil
import codecs
from common_operation import *
from xml.dom import minidom
from lxml import etree
from xml_control import ParseXML
from BtsShell import connections
from BtsShell.application_lib.sftp import *
from BtsShell.file_lib import *

def change_ipsec_file(src_ipsec_file, tar_ipsec_file, modify_list):
    """Change ipsec file if the script changed and copy modified file with new name to target.

    | Input Paramaters   | Man. | Description |
    | src_ipsec_file     | yes  | Absolute path of ipsec file you want to modify |
    | tar_ipsec_file     | yes  | new ipsec file name |
    | modify_list        | no   | new list you want to modify |

    Example
    | ${list}= | Create List | keyexchange=ikev1 | esp=aes128-sha1,3des-sha1! |
    | Change Ipsec File  | ipsec.conf | ipsec1.conf | ${list} |
    """

    if type(modify_list) is not types.ListType:
        if modify_list == '':
            shutil.copyfile(src_ipsec_file, tar_ipsec_file)
            return
        else:
            print 'ERROR:The input must be a empty string or a LIST!'
            raise TypeError

    key_list = []
    value_list = []
    try:
        for item in modify_list:
             tmp = item.split('=')
             key_list.append(tmp[0])
             value_list.append(tmp[1])
        if modify_list is []:
             shutil.copyfile(src_ipsec_file, tar_ipsec_file)
             return
    except:
        print ''''ERROR:The input parameter must be one '=' involved!'''
        raise TypeError

    src_handle = file(src_ipsec_file,'rb')
    tar_handle = open(tar_ipsec_file,'wb')
    try:
        for src_line in src_handle.readlines():
            tar_line = src_line
            for i in range(0,len(key_list)):
                #search_pattern = "^  %s=" % (key_list[i])
                search_pattern = "\s+%s=" % (key_list[i])
                if re.search(search_pattern, src_line):
                    src_tmp = src_line.split('=')
                    tar_line = src_tmp[0] + "=" + value_list[i] + "\n"
            tar_handle.write(tar_line)
    finally:
        #shutil.copyfile(src_ipsec_file, tar_ipsec_file)
        src_handle.close()
        tar_handle.close()


def solve_time_period_udplog(udp_log, period):
    """This keyword reads udp log to get period value,then contrast with design data.

    | Input Parameters  | Man. | Description |
    | udp_log           | Yes  | Configuration file directory |
    | period            | Yes  | srs's period we design |

    | Return value | is the different is right for peroid you design |

    Example
    | solve_time_period_udplog | C:\\SYSLOG_212.LOG | 10ms |
    """

    try:
        file_handle = file('%s' % (udp_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % udp_log
    lines = file_handle.readlines()
    time_list = []
    d = []
    flag = 1
    try:
        for line in lines:
            if re.match('.*HandleSrsCellMeasResp,.*', line):
                m=re.match('.*\<\d.*\d+:\d+:\d+\.(\d{3}).*\>.*', line)
                time_list.append(int(m.group(1)))
                flag=0
        for i in range(0,len(time_list)-1):
            diff=time_list[i+1]-time_list[i]
            if diff<0:
                diff=1000+time_list[i+1]-time_list[i]
            if  str(diff)+'ms' != period:
                print time_list[i+1],time_list[i],i
                flag=1
    finally:
        file_handle.close()
        if flag == 0:
            return True
        else:
            return False
        
def print_log_console(logs):
    print logs
    sys.__stdout__.write(logs)

def _get_active_sw_version(downloaddir='/flash', username='toor4nsn', passwd='oZPS0POrRieRtu'):
    """This keyword get software version of BTS

    | Input Parameters  | Man. | Description |
    |    downloaddir    |  No  | Default value is /flash  |
    |    username       |  No  | Default value is 'toor4nsn' for BTS  |
    |     passwd        |  No  | Default value is 'oZPS0POrRieRtu' for BTS  |

    Example
    |  get_active_sw_version  |
    """
    #step 1 make new dir in the current dir
    curdir = os.getcwd()
    desDirname = curdir + '\log\\'
    filename = 'FileDirectory.xml'
    if not os.path.exists(desDirname):
        os.mkdir(desDirname)
    desPath = desDirname + filename

    print 'desDirname=%s, downloaddir=%s ,filename=%s' %(desPath, downloaddir, filename)
    #step 2 retr xml from the server to the dir made before
    try:
        sftp_download('192.168.255.1', 22, username, passwd, desPath, filename,downloaddir)
    except:
        try:
            sftp_download('192.168.255.129', 22, 'root', '', desPath, filename, '/ffs/fs1')
        except:
            try:
                sftp_download('192.168.255.129', 22, 'root', '', desPath, filename, downloaddir)
            except:
                print 'activeBuildVersion=UNKNOWN'
                raise Exception, 'get file %s from FCM failed' % (filename)

    #step 3 Parse the xml file ,and get the Version Value
    version_info = __ParseVersion(desPath)

    sys.__stderr__.write("\n****Current BTS version is '%s' *****\n"%version_info)
    return version_info

def __ParseVersion(filename):
    VersionValue=""
    local_Tag="fileDirectory"
    local_keyName="activeBuildVersion"
    try:
        #xmldoc = minidom.parse(filename)
        xml = ParseXML(filename)
    except:
        print 'activeBuildVersion=UNKNOWN'
        return VersionValue

    fd_ele = xml.get_element(local_Tag)
    VersionValue = xml.get_ele_attr(fd_ele, local_keyName)
    if len(VersionValue) < 3:
        VersionValue = xml.get_ele_attr(fd_ele, "activeBuildName")

    if VersionValue=="":
        print 'activeBuildVersion=UNKNOWN'
    else:
        print "activeBuildVersion=%s" %(VersionValue)

    return VersionValue


def modify_swconfig(source_file, dest_file, modify_list = []):
    """This keyword modify BTS's swconfig file

    | Input Parameters  | Man. | Description |
    | source_file       | Yes  | source swconfig's full path |
    | dest_file         | Yes  | target swconfig's full path |
    | modify_list       | No   | new  [key:value] list you want to modify |


    Example
    | source file | target file |
    | #0x16000F=1 | 0x16000F=3  |
    | 0x160010=1  | 0x160010=5  |
    | 0x160011=1  | #0x160011=1 |

    | ${modify_list}= | Create List | 0x16000F=3 | 0x160010=5 | \#0x160011=1 |
    |  modify_swconfig  |  c:\\swconfig.txt | c:\\swconfig_new.txt | ${modify_list} |
    """

    file_src = file(source_file, 'r')
    file_dst = file(dest_file, 'w')
    try:
        for line in file_src.readlines():
            for para in modify_list:
                (key, value) = para.split("=")
                if key.startswith("#"):
                    if key[1:] in line:
                        (key, value) = line.split("=")                        
                        line = "#%s = %s\n"%(key, value.strip())                    
                elif re.search("^#?%s\s=" % (key), line):
                    line = "%s = %s\n" % (key, value)
                elif re.search("^#?%s=" % (key), line):
                    line = "%s = %s\n" % (key, value)

            file_dst.write(line)
    finally:
        file_src.close()
        file_dst.close()

def read_swconfig(source_file, read_list = []):
    if read_list == []:
        return
    result_list = []
    file_content = file_read(source_file)
    for read in read_list:
        read_flag = 0
        for f in file_content:            
            tmp = re.search('^\s*%s\s*=\s*(\d)'%read, f)
            if tmp:
                result_list.append(tmp.groups()[0])
            else:
                read_flag += 1
        
        if read_flag == len(file_content):            
            result_list.append(None)
    return result_list            
    
    
    
def OMSearchInFolder(keyword, FoldName, printFlag = 0):
    """Search keyword in the specifical folder.

    | Input Paramaters | Man. | Description |
    | keyword          | Yes  | the string you want to search, you can use '.*' to match any character |
    | FoldName         | Yes  | the destination folder |
    | printFlag        | No   | if you want to print the detail, the value is 1 |

    Example
    | OMSearchInFolder | SPMAG: FSPB.*PLL Locked | C:\Temp\BTSLogs | 0 |
    | OMSearchInFolder | RNW parameters validated in RROM  | C:\Temp\BTSLogs | 1 |
    """

    findFlag = 0

    if('' == keyword or 4 > len(keyword)):
        print "keyword is null"
        raise Exception
    if not os.path.exists(FoldName):
        print "Folder <%s> is not exist!" % FoldName
        raise Exception

    MultiTupple = os.walk(FoldName)

    CurrentDate = time.strftime('%Y%m%d%H%M')

    resultFolder = '%s%slog' % (os.getcwd(), os.sep)

    if not os.path.exists(resultFolder): # not 'log' dir exist in CWD
        os.mkdir(resultFolder)

    logname = resultFolder + '\\' + CurrentDate + '_OM_Search_result.txt'
    logfile = file(logname, 'a')

    for Path, Folder, FilenameList in MultiTupple:
        if (0 < len(FilenameList)):
            for Filename in FilenameList:
                if '.LOG' in Filename:
                    FilePath = Path + '\\' + Filename
                    if 0 == _OMSearchInFile(keyword, FilePath, logfile, printFlag):
                        findFlag = 1
                        print >> logfile, "Search \"%s\" in \"%s\"\n\n" % (keyword,Filename)
    logfile.close()
    if not findFlag:
        print "Can't find \"%s\" in \"%s\"" %(keyword, FoldName)
        raise Exception


def _OMSearchInFile(keyword, FilePath, logfile, printFlag = 0):
    FileFindFlag = 0
    fIndex = file(FilePath)
    fContent = fIndex.readlines()

    for i in xrange(len(fContent)):
        if re.search(keyword, fContent[i]):
            FileFindFlag += 1
            print >> logfile, fContent[i]
            if '1' == printFlag:
                print fContent[i]

    fIndex.close()

    if FileFindFlag > 0:
        print "Find keyword <%s> times in \"%s\"\n"%(FileFindFlag, FilePath)
        print >> logfile, "Find keyword <%s> times in \"%s\"\n"%(FileFindFlag, FilePath)
        return 0

def get_time_from_udplog(log_path, info, time_index=0):
    """This keyword read UDP log to get time information based on the given info.

    | Input Parameters  | Man. | Description |
    | log_path          | Yes  | Configuration file directory |
    | info              | Yes  | srs's period we design |

    | Return value | time information with pattern hh:mm:ss |

    Example
    | Get Time From UDPLog | C:\\UDPLog_Tue_Nov_23_14_01_48_2010.log | BTS status is now OnAir |
    """

    try:
        file_handle = file('%s' % (log_path), 'r')
    except:
        raise Exception, "UDP log '%s' open failed" % log_path

    lines = file_handle.readlines()
    file_handle.close()
    pattern = ".*%s.*" % (info)
    
    time_list = []
    find_flag = 0
    for line in lines:
        if re.search(pattern, line):
            search_result = re.search('^.*\\s(\\d+:\\d+:\\d+).\\d+\\s', line)
            if search_result:
                find_flag += 1
                print "Find msg '%s' with condition '%s'"%(line, pattern)
                time_list.append( search_result.group(1).strip())
                
            else:
                raise Exception, "This line '%s' contain '%s' but not include time stamp"%(line, pattern)
    if 0 == find_flag:
        raise Exception, "UDP log '%s' do not contain '%s'"%(log_path, info)       
    else:
        time_index = int(time_index)
        return time_list[time_index]   

def check_scf_version(firedirectory_dir, scf_file_name):
    print "SCFC file name is %s"%scf_file_name
    try:
        xmldoc = minidom.parse(firedirectory_dir)
        root = xmldoc.documentElement
    except:
        raise Exception, "'%s' open failed" % firedirectory_dir

    file_Directory_element = xmldoc.getElementsByTagName('fileDirectory')
    activeBuildVersion = file_Directory_element[0].attributes['activeBuildVersion'].value
    version = activeBuildVersion.split('_')[0]

    all_file_Element = xmldoc.getElementsByTagName('fileElement')
    for i in range(len(all_file_Element)):
        name = all_file_Element[i].attributes['name'].value
        version = all_file_Element[i].attributes['version'].value
        activeFlag = all_file_Element[i].attributes['activeFlag'].value
        if (scf_file_name == name) and ('TRUE' == activeFlag):
            return scf_file_name + version
    raise Exception, "Can't find actived SCF version"


def get_fspb_id_for_memdump(log_path):
    """This keyword read UDP log to get fsp and faraday number if there is "FATAL KERNEL ERROR" in log.
    | Input Parameters  | Man. | Description                 |
    | log_path          | Yes  | UDP log directory           |
    | Return value      | fsp and faraday number             |

    Example
    | get fspb id for memdump | C:\\UDPLog_Tue_Nov_23_14_01_48_2010.log |
    """

    fspList = []
    fspListIdleProcess = []
    try:
        file_handle = file('%s' % (log_path), 'r')
    except:
        raise Exception, "UDP log '%s' open failed" % log_path

    pattern = "FATAL KERNEL ERROR"
    try:
        for line in file_handle.readlines():
            if re.search(pattern, line):
                if re.search(".*proc=0 \(IdleProcess\).*ecode=0x00000024.*", line):
                    search_result = re.search('.*Nid:(0x\d{4}).*', line)
                    if search_result:
                        if search_result.groups()[0] not in fspListIdleProcess:
                            fspListIdleProcess.append(search_result.groups()[0])
                    else:
                        raise Exception, "This UDP log do not contain fspb number when proc=0!"
                else:
                    search_result = re.search('.*Nid:(0x\d{4}).*', line)
                    if search_result:
                        if search_result.groups()[0] not in fspList:
                            fspList.append(search_result.groups()[0])
                    else:
                        raise Exception, "This UDP log do not contain fspb number"

    finally:
        file_handle.close()
        if 0 == len(fspList):
            return fspListIdleProcess
        else:
            return fspList

#xq and ghs 2010-8-3
def change_configuration_file(src_File_Dir, target_File_Dir, Need_to_Modify='',link_display_name = 'SCF_1.xml'):
    """scf xml change and copy modified file with new name to both target dir and local log dir.

    | Input Paramaters | Man. | Description |
    | src_File_Dir     | yes  | Absolute path of scf xml file you want to modify |
    | target_File_Dir  | yes  | new scf xml file name(No path informatino,share absolute path with src_File_Dir) |
    | Need_to_Modify   | no   | new  key:value list you want to modify |
    |link_display_name | no   | display link_name for log |

    Example
    | ${list}= | drbAmMxRtxTh:100 | eia0:1 |
    | Change Configuration File | C:\Temp\SCF_1.xml | C:\Temp\SCF_new_file.xml | ${list} |

    Note:
    if Need_to_Modify is string type but not empty string,the function will raise ValueError exception,
    if Need_to_Modify is neither string type nor list type,the function will raise TypeError exception.
    """
    if 0 < len(Key_List):
        for i in range(len(Key_List)):
            del Key_List[0]
            del Value_List[0]

    #step 1: if the Need_to_Modify is empty string,the function just do copy job
    if type(Need_to_Modify)is types.StringType:
        if '' == Need_to_Modify:
            shutil.copyfile(src_File_Dir, target_File_Dir)  #copy file
            #file_copy_and_display_link(target_File_Dir, link_display_name)
            return
        else:
            raise Exception, 'ERROR:The input string(3rd parameter) is not empty!'

    #step 2: if the type of Need_to_Modify is not list type,rasie exception
    if not type(Need_to_Modify) is  types.ListType:
        raise Exception, 'ERROR:The input parameter type(3rd parameter) is not ListType!'

    elif 0 == len(Need_to_Modify):
        shutil.copyfile(src_File_Dir, target_File_Dir)  #copy file
        #file_copy_and_display_link(target_File_Dir, link_display_name)
        return

    #step 3: modify the file
    for target in Need_to_Modify:
        (key, value) = target.split(':')
        Key_List.append(key)
        Value_List.append(value)

    xmldoc = minidom.parse(src_File_Dir)
    _Analyse_xml_File(xmldoc, xmldoc)

    file_Object = file(target_File_Dir, 'w')
    writer = codecs.lookup('utf-8')[3](file_Object)
    xmldoc.writexml(writer, encoding = 'utf-8')
    writer.close()
    #shutil.copyfile(src_File_Dir, target_File_Dir)  #copy file
    #file_copy_and_display_link(target_File_Dir, link_display_name)


def _Analyse_xml_File(node, _xmldoc):
    for childnode in node.childNodes:
        if childnode.nodeType == node.ELEMENT_NODE:
            _Analyse_xml_File(childnode,_xmldoc)
        if childnode.nodeType == node.TEXT_NODE:
            for i in range(0,len(Key_List)):
                if cmp(node.getAttribute('name'),Key_List[i]) == 0:#match
                    if len(node.childNodes)==1:  #suggest only one child node
                        node.replaceChild(_xmldoc.createTextNode(Value_List[i]),childnode)#replace



def read_FTM_counter_file(file_dir, key):
    """Read key value from counter xml file.

    | Input Paramaters   | Man. | Description |
    | file_dir           | yes  | counter xml file abs path |
    | key                | yes  | key name |

    Example
    | Read Configuration File | D:\counter.xml | M8000C6 |
    """
    try:
        file_handle = file(file_dir, 'r')
    except:
        raise Exception, "Counter file '%s' open failed" % file_dir

    search_pattern = "%s>([0-9]{1,10})</%s" % (key, key)
    value_list = []
    try:
        lines = file_handle.readlines()
        for line in lines:
            search_result = re.search(search_pattern, line)
            if search_result:
                value = search_result.group(1)
                value_list.append(value)
    finally:
        file_handle.close()

    return value_list[-1]


from xml_control import ParseXML
def read_counter_file(file_dir, key, index=-1):
    """This keyword reads BTS counter file.

    | Input Parameters  | Man. | Description |
    | file_dir          | Yes  | counter file directory |
    | key               | Yes  | Key for search |

    | Return value | The value for search key or None when key is not found |

    Example
    | Read Configuration File | D:\\counter.xml | M8000C6 |
    """
    '''
    try:
        file_handle = file(file_dir, 'r')
    except:
        raise Exception, "Counter file '%s' open failed" % file_dir

    search_pattern = '%s>([0-9]+)</%s' % (key, key)
    value_list = []
    try:
        lines = file_handle.readlines()
        for line in lines:
            tags = line.split("><")
            for tag in tags:
                search_result = re.search(search_pattern, tag)
                if search_result:
                    value = search_result.group(1)
                    value_list.append(value)
    finally:
        file_handle.close()
    print value_list

    return value_list[-1]
    '''

    value_list = []
    xml = ParseXML(file_dir)
    if ':' not in key:
        key_list = xml.get_element(key, 'ALL', True)
        
        for key in key_list:
            value_list.append(xml.get_ele_text(key))
        if value_list:
            return value_list[index]    
        else:
            raise Exception("Not find the tag as '%s'" % key)
    elif 1 == key.count(':'):
        cell, tag = key.split(':')
        match_mo_list = []
        all_local_mo = xml.get_element('localMoid', 'ALL', True)
        
        for local_mo in all_local_mo:
            text = xml.get_ele_text(local_mo)
            if cell in text:
                match_mo_list.append(local_mo)
        
        for local_mo in match_mo_list:
            father = xml.get_ele_parent(local_mo, 2)
            try:
                match_tag = xml.get_element(tag, father)
                value_list.append(xml.get_ele_text(match_tag))
            except:
                pass
        if value_list:
            return value_list[index]
        else:
            raise Exception("Not find the element by '%s'" % key)  
    else:
        raise Exception("Please check condition as 'M8000C6' or 'LNCEL-3312:M8001C18'") 
        
def Read_MaxValue_In_Counter_File(file_dir, key):
    """This keyword reads BTS counter file, and return the max value of one counter

    | Input Parameters  | Man. | Description |
    | file_dir          | Yes  | counter file directory |
    | key               | Yes  | Key for search |

    | Return value | The value for search key or None when key is not found |

    Example
    | Read Configuration File | D:\\counter.xml | 'M8000C6' |
    """
    try:
        file_handle = file(file_dir, 'r')
    except:
        raise Exception, "Counter file '%s' open failed" % file_dir

    search_pattern = '%s>([0-9]+)</%s' % (key, key)
    value_list = []
    try:
        lines = file_handle.readlines()
        for line in lines:
            tags = line.split("><")
            for tag in tags:
                search_result = re.search(search_pattern, tag)
                if search_result:
                    value = search_result.group(1)
                    value_list.append(value)
    finally:
        file_handle.close()
    print value_list
    return max(value_list)



def get_value_in_siteem_file(src_File_Dir):
    """This keyword get major, minor and build value from SiteEM.xml.
    | Input Paramaters  | Man. | Description |
    | src_File_Dir      | yes  | Absolute path of SiteEM.xml file |

    Example
    | get_value_in_siteem_file | 'D:\\SiteEM.xml' |
    """
    try:
        file_src = file(src_File_Dir, 'r')
    except:
        raise Exception, "'%s' open failed" % src_File_Dir

    value_list = []

    try:
        lines = file_src.readlines()

        search_result = re.search('(\d+)\n', lines[14])
        if search_result:
            major = search_result.groups()[0]
            value_list.append(major)

        search_result = re.search('(\d+)\n', lines[17])
        if search_result:
            minor = search_result.groups()[0]
            value_list.append(minor)

        search_result = re.search('(\d+)\n', lines[20])
        if search_result:
            build = search_result.groups()[0]
            value_list.append(build)

    finally:
        file_src.close()

    if len(value_list) != 0:
        return value_list
    else:
        raise Exception, "Don't get value!"

def change_siteem_file(src_File_Dir, target_File_Dir, Need_to_Modify):
    """This keyword modify SiteEM.xml.

    | Input Paramaters  | Man. | Description |
    | src_File_Dir      | yes  | Absolute path of SiteEM.xml file you want to modify                      |
    | target_File_Dir   | yes  | new file name(No path information,share absolute path with src_File_Dir) |
    | Need_to_Modify    | yes  | list you want to modify                                                  |

    Example
    | change_siteem_file | 'D:\\SiteEM.xml' | 'new.xml' | ['1', '10', '383'] |

    Note:
    if Need_to_Modify is not list or list but empty, the function will raise ValueError exception
    """

    path = os.path.dirname(src_File_Dir)

    target_name_temp = target_File_Dir
    if path == '':
        target_File_Dir = '.\\' + target_File_Dir
    else:
        target_File_Dir = path + '\\' + target_File_Dir

    #step 1: if the type of Need_to_Modify is not list type,rasie exception
    if not type(Need_to_Modify) is  types.ListType:
        raise Exception, 'ERROR:The input parameter type is not ListType!'

    if 3 == len(Need_to_Modify):
        major = Need_to_Modify[0]
        minor = Need_to_Modify[1]
        build = Need_to_Modify[2]
    else:
        raise Exception, 'ERROR:The input string is wrong!'

    #step 2: modify the file
    try:
        file_src = file(src_File_Dir, 'r')
        file_object = file(target_File_Dir, 'w')
    except:
        raise Exception, "'%s' open failed" % target_File_Dir

    try:
        lines = file_src.readlines()

        lines[14] = '    %s\n' % major
        lines[17] = '    %s\n' % minor
        lines[20] = '    %s\n' % build

        for line in lines:
            file_object.write(line)

    finally:
        file_src.close()
        file_object.close()

def _parse_alarm_file(file_path):
    file_content = file_read(file_path, "string")
    alarm_list = file_content.split("\n*****")
    alarm_dict_list = []
    for alarm in  alarm_list:
        if "***" in alarm and "row" in alarm:
            alarm_dict = {}            
            item_list = alarm.splitlines()
            for item in item_list:
                if "***" in item:
                    ret = re.search('.*\s+(\\d+).*row', item)
                    if ret:
                        index = ret.groups()[0]
                        alarm_dict['index'] = index
                elif ":" in item:
                    key, value = item.split(':',1)
                    key = key.strip()
                    value = value.strip()
                    alarm_dict[key] = value
                else:
                    pass
            alarm_dict_list.append(alarm_dict)        
            
    #for alarm_dict in alarm_dict_list:
    #    print alarm_dict['index']   
    return alarm_dict_list

def check_alarm_file(file_path, check_list):
    """ This keyword return match alarm msg dict from alarm file

    | Input Parameters | Man. | Description |
    | file_path  | Yes  | alarm file path |
    | check_list | Yes  | check condition |
    | Return | match condition alarm dict |

    Example
    | ${condition} | create list | AlarmId: 105953 | Cleared: 0 |
    | ${match_dict_list} | check_alarm_file | d:\\alarm.txt | ${condition} |
    | ${time} | run keyword if | ${a} != ${False} | Get From Dictionary | ${match_dict_list[0]} | LOCAL_AlarmTime |
    """ 
    find_flag = 0
    result_dict_list = []
    alm_dict_list = _parse_alarm_file(file_path)
    for alm_dict in alm_dict_list:
        all_pass_flag = 0
        for check in check_list:
            key,value = check.split(':',1)
            key = key.strip()
            value = value.strip()
            if  key in alm_dict.keys() and alm_dict[key] == value:
                all_pass_flag += 1         
        if all_pass_flag == len(check_list):
            print "Find alarm in row '%s'"%alm_dict['index']
            result_dict_list.append( alm_dict)
            find_flag += 1
            
    if find_flag > 0:
        return result_dict_list
    else:
        return False
    
if __name__ == '__main__':

    #print read_swconfig("D:\\SVN\\TACT_UT_trunk\\file_lib\\swconfig_575.txt", ['575', '0x16000F', '0x160010'])
    #print check_scf_version("d:\\20130806145124_TARGET_FileDirectory.xml", 'SCFC')
    condition = [ 'MOId: moid=NE-MRBTS-889/NE-LNBTS-889',
                 'SpecificProblem: 7650' ,
                 'Cleared: 0',
                  'PerceivedSeverity: 2' ,
                  'AlarmText: BASE STATION FAULTY',
                  'LOCAL_AlarmTime: 2013-08-30 10:29:24' ]
    condition2 = [ 'SpecificProblem: 7657',
                    #'AlarmText: BASE STATION CONNECTIVITY DEGRADEd',
                    'LOCAL_AlarmTime: 2013-09-18 13:38:32']
    print check_alarm_file('d:\\AllAlarm_OMS.txt',condition2)