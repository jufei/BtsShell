from __future__ import with_statement
import os, zipfile, time
import types
import shutil
from robot.utils import asserts
import re
import string
import mmap
from BtsShell import connections

from xml.dom import minidom
import codecs
from BtsShell.common_lib.get_path import *

pscpPath = os.path.join(get_tools_path(), "pscp.exe")

IP_PATTERN = "(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)"

Key_List_1 = []
Value_List_1 = []

Key_List = []
Value_List = []
Class_List = []
Cvalue_List = []
Find_List = []

New_Value_List = []
New_Class_List = []
New_Cvalue_List = []
New_Find_List = []

CONDITION_NAME = []
CONDITION_VALUE = []
MODIFY_NAME = []

Excep_list = []


def _get_string_msg(str1, str2, msg, delim):
    _msg = "'%s' %s '%s'" % (str1, delim, str2)
    if msg is None:
        msg = _msg
    return msg


def _copy_list(list):
    temp_list = []
    for item in list:
        temp_list.append(item)
    return temp_list


def _print_file_link(file_path, tag_name):
    """This keyword will display the file name to be hyperlink.

    | Input Paramaters | Man. | Description |
    | file_path        | Yes  | the file hyperlink to |
    | tag_name         | Yes  | name hyperlink displays |

    Example
    | Print File Link | C:\Temp\BTSLogs\udp.log | display name |
    """

    return '*HTML*<a href = "%s">%s</a>' % (file_path, tag_name)



def Folder_All_File_Remove(srcFilename='C:\Temp\BTSLogs'):
    """BTSLogs's folder copy and clear.

    | Input Paramaters | Man. | Description |
    | srcFilename      | No   | Absolute path of folder that you want to clear |

    Example
    | Folder All File Remove | C:\Temp\BTSLogs |
    """

    #check if the backup path is exist
    desFilename = 'C:\Temp\BTSLogsbackup'
    if not os.path.exists(desFilename):
        os.mkdir(desFilename)
    from BtsShell.application_lib.process import kill_process
    kill_process('BTSLog.exe')

    #copy old log file in backup path
    Copy_command = "copy %s %s" % (srcFilename, desFilename)
    os.system(Copy_command)

    #clear the
    for root, dirs, files in os.walk(srcFilename):#top, topdown=False):
        if(0 < len(files)):
            for name in files:
                os.remove(os.path.join(root, name))#delete all file




def file_match_all(file_path, regexp, read_mode='r+'):
    """This keyword match all

    | Input Parameters | Man. | Description |
    | file_path        | Yes  | Source file path |
    | regexp           | Yes  | match regexp |
    | read_mode        | No   | Read mode, default is 'r+' |

    | Output Parameters| Man. | Description |
    | match_content     | Yes  | file match content list, [] if match nothing. |

    Example
    | file_read | D:\\1.txt | #\s*(\d+) | 'r+' |
    """
    if not os.path.isfile(file_path):
        raise Exception, "File %s does not exists" % (file_path)
    try:
        with open(file_path, read_mode) as file_obj:
            data = mmap.mmap(file_obj.fileno(), 0)
            result = re.findall(regexp, data)
            return result
    except IOError:
        raise Exception, "Open %s failed!" % (file_path)



def file_read(file_path, output_format="list", read_mode = 'r'):
    """This keyword read file with special mode, return file content as list or string

    | Input Parameters | Man. | Description |
    | file_path        | Yes  | Source file path |
    | output_format    | No  | output format default as list |
    | read_mode        | No   | Read mode, default is 'r' |


    | Output Parameters| Man. | Description |
    | file_content     | Yes  | file line content list, [] if error happens or empty file. |

    Example
    | file_read | D:\\1.txt | 'rb' |
    | file_read | D:\\1.txt |
    """
    if not os.path.isfile(file_path):
        raise Exception, "File %s does not exists" % (file_path)
    try:
        with open(file_path, read_mode) as file_obj:
            if "string" == output_format:
                return file_obj.read()
            else:
                return file_obj.readlines()
    except IOError:
        raise Exception, "Open %s failed!" % (file_path)

def file_write(file_path, file_content, write_mode = 'w'):
    """This keyword Write content to File

    | Input Parameters | Man. | Description |
    | file_path        | Yes  | Destination file path |
    | file_content     | Yes  | file content need to write |
    | write_mode       | No   | Write mode, default is 'w', e.g 'w', 'a' for normal use, 'wb'/'ab' for bin file, 'wu'/'au' for Unix file |


    | Output Parameters| Man. | Description |
    | True/False     | Yes  | True - success, False for any issue. |

    Example
    | file_write | D:\\Desktop\\1.txt | "12345" |
    """
    #Check input argv

    dir_name = os.path.dirname(file_path)

    if not (isinstance(file_content, (list, str, unicode))):
        raise Exception, "Fail to write file: %s, file content: %s must be list or string", \
                            (file_path, file_content)

    if os.path.isfile(file_path):
        print "File: %s has existed, may be overwrited"%file_path
    elif os.path.isdir(dir_name):
        print "Parent dir: %s is exist"%dir_name
    else:
        print "Parent dir: %s is not exist, try to create it"% dir_name
        os.makedirs(dir_name)

    try:
        with open(file_path, write_mode) as file_obj:
            file_obj.writelines(file_content)
    except Exception, err_info:
        raise Exception, "Write file '%s' falied: %s" % (file_path, err_info)


    print "Write file '%s' success" % file_path

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
        print "Creat directory %s fail"% (p_DirFullName)
        return False
    print "Creat directory %s OK"% (p_DirFullName)
    return True

def dir_remove(DirFullName):
    """Remove a directory

    Input:[1] DirFullName: full path name of directory forced
    Notes: If directory not existed, return 1 directly.
    """
    p_DirFullName = DirFullName
    if not os.path.isdir(p_DirFullName):
        print "Dir %s is not exist, needn't remove." % p_DirFullName
        return True
    try:
        shutil.rmtree(p_DirFullName)
        print "Remove directory %s easily" % p_DirFullName
    except Exception, p_ErrorInfo:
        print "Remove directory %s easily failed because of '%s'" % (p_DirFullName, p_ErrorInfo)

        try:
            for p_Loop in os.listdir(p_DirFullName):
                p_ReadOnlyFile = os.path.join(p_DirFullName, p_Loop)
                os.chmod(p_ReadOnlyFile, stat.S_IRWXU)
                if os.path.isdir(p_ReadOnlyFile):
                    DirRemove(p_ReadOnlyFile)
                elif os.path.isfile(p_ReadOnlyFile):
                    FileRemove(p_ReadOnlyFile)
            shutil.rmtree(p_DirFullName)
        except Exception, p_ErrorInfo:
            print "Remove directory %s hardly failed because of '%s'" % (p_DirFullName, p_ErrorInfo)
            return False
        print "Remove directory %s hardly" % p_DirFullName
    return True

def file_remove(FileFullName):
    """Remove a file

    Input:[1] FileFullName: full path name of file
    Notes: If file not existed, return directly.
    """
    p_FileFullName = FileFullName
    if not os.path.isfile(FileFullName):
        print "File %s is not exist, needn't remove." % p_FileFullName
        return True

    try:
        os.remove(p_FileFullName)
        print "Remove file %s easily", p_FileFullName
    except Exception, p_ErrorInfo:
        print "Remove file %s easily failed because of '%s'" % (p_FileFullName, p_ErrorInfo)

        try:
            os.chmod(p_FileFullName, stat.S_IWRITE)
            os.remove(p_FileFullName)
            print "Remove file %s hardly", p_FileFullName
        except Exception, p_ErrorInfo:
            print "Remove file %s failed because of '%s'" % (p_FileFullName, p_ErrorInfo)
            return False
    return True

def file_should_match(source_file_dir, keyword):
    """This keyword checks whether file match specified keyword.

    | Input Parameters | Man. | Description |
    | source_file_dir  | Yes  | Target file directory |
    | keyword          | Yes  | Keyword or keyword list for search in file |


    Example
    | File Should Match | C:\\test.txt | PBCH | 0 |
    """

    FileFindFlag = 0

    fIndex = file(source_file_dir)
    fContent = fIndex.readlines()

    keywordlist = []
    if types.ListType != type(keyword):
        keywordlist.append(keyword)
    else:
        keywordlist = keyword

    srcList = _copy_list(keywordlist)
    try:
        for k in keywordlist:
            for i in xrange(len(fContent)):
                if re.search('\\b'+k+'\\b', fContent[i]):
                    FileFindFlag += 1

            if 0 == FileFindFlag:
                print "\"Can't find \"%s\" in \"%s\"\n"%(k, source_file_dir)
            else:
                print "Find \"%s\" <%s> times in \"%s\""%(k, FileFindFlag, source_file_dir)
                #print >> logfile, "Find \"%s\" <%s> times in \"%s\"\n"%(k, FileFindFlag, destFilePath)
                FileFindFlag = 0
                srcList.remove(k)

        if 0 != len(srcList):
            log = "Not all keyword find in \"%s\"\n"%(source_file_dir)
            raise Exception, log
    finally:
        fIndex.close()


def file_should_contain(source_file_dir, keywords, dest_file_name='', tag_name='log_file', msg=None):
    """This keyword checks whether file contains specified keyword.
    It will copy the source file to the directory '${CURRENT_WORKING_DIR}/log' which will be
    published with report/log file so user can get the whole file through HTML link

    | Input Parameters | Man. | Description |
    | source_file_dir  | Yes  | Source file directory |
    | keywords         | Yes  | Keywords for search in file |
    | dest_file_name   | No   | Destination file name, default is '' and file name will remain the same |
    | tag_name         | No   | HTML tag name, default is 'log_file' |
    | msg              | No   | Special messages for error case |

    | Return value | list of lines found in file with given keywords |

    Example
    | File Should Contain | C:\\test.txt | PBCH | UDPLog.log | UDP_Log |
    """

##    try:
##        file_handle = file(source_file_dir, 'r')
##        lines = file_handle.readlines()
##    except:
##        raise Exception, "Open file '%s' failed" % (source_file_dir)
##    finally:
##        file_handle.close()
    lines = file_read(source_file_dir)
    not_found_keywords = []
    search_keywords = []
    contain_lines = []

    if type(keywords) != types.ListType:
        not_found_keywords.append(keywords)
    else:
        not_found_keywords = keywords

    for keyword in not_found_keywords:
        search_keywords.append(keyword)

    for line in lines:
        not_found_keywords = _copy_list(search_keywords)
        for keyword in not_found_keywords:
            # in order to support RegExp, instead of "if keyword in line:"
            search_result = re.search(keyword, line)
            if search_result:
          #  if keyword in line:
                print '*DEBUG*keyword (%s) found in line (%s)' % (keyword, line)
                contain_lines.append(line)
                try:
                    search_keywords.remove(keyword)
                except ValueError:
                    pass

    msg = _get_string_msg(source_file_dir, search_keywords, msg, 'does not contain')

    if len(search_keywords) != 0: # not all keywords found
        print '*HTML*<a href = "%s">fail log</a>' % source_file_dir
        asserts.fail(msg)

    return contain_lines


def file_should_not_contain(source_file_dir, keywords):
    """This keyword checks whether file doe not contain specified keyword.
    It will copy the source file to the directory '${CURRENT_WORKING_DIR}/log' which will be
    published with report/log file so user can get the whole file through HTML link

    | Input Parameters | Man. | Description |
    | source_file_dir  | Yes  | Source file directory |
    | keyword          | Yes  | Keyword for search in file |


    Example
    | File Should Not Contain | C:\\test.txt | MIMO | 
    """
##    try:
##        file_handle = file(source_file_dir, 'r')
##        lines = file_handle.readlines()
##    except:
##        raise Exception, "Open file '%s' failed" % source_file_dir
##    finally:
##        file_handle.close()

    lines = file_read(source_file_dir)

    if isinstance(keywords, str) or isinstance(keywords, unicode):
        keywords  = [keywords]
    keywords = [str(kw) for kw in keywords]
    for line in lines:
        for kw in keywords:
            if kw in line: # keyword found but it is not expected
                msg = _get_string_msg(source_file_dir, kw, msg, 'contains')
                asserts.fail(msg)




def file_copy(source_file_dir, dest_file_dir):
    """This keyword copies source file to destination directory.

    | Input Parameters | Man. | Description |
    | source_file_dir  | Yes  | Source file directory |
    | dest_file_dir    | Yes  | Destination file directory or file name |

    Example
    | File Copy | C:\Master_Configuration.xml | D:\configuration_file |
    """

    try:
        shutil.copy(source_file_dir, dest_file_dir)
        print "File '%s' copied to '%s' successfully!" % (source_file_dir, dest_file_dir)
    except:
        raise Exception, "File '%s' copied to '%s' failed" % (source_file_dir, dest_file_dir)


def file_move(source_file_dir, dest_file_dir):
    """This keyword moves source file to destination directory. If new name is given, file will also be renamed

    | Input Parameters | Man. | Description |
    | source_file_dir  | Yes  | Source file directory |
    | dest_file_dir    | Yes  | Destination file directory or file name |

    Example
    | File Move | D:\\Desktop\\1.txt | D:\\Desktop\\2.txt |
    | File Move | D:\\Desktop\\1.txt | D:\\Desktop\\New_directory |
    """

    try:
        shutil.move(source_file_dir, dest_file_dir)
    except:
        raise Exception, "File '%s' moved to '%s' failed" % (source_file_dir, dest_file_dir)


def file_remove(file_dir, file_name=None):
    """This keyword removes source file in specified directory. If file_name is not given, removes all the files in such directory

    | Input Parameters | Man. | Description |
    | file_dir         | Yes  | Source file directory |
    | file_name        | No   | Source file name, if not given default is all files |

    Example
    | File Remove | D:\\Desktop |
    | File Remove | D:\\Desktop | 1.txt |
    """

    if file_name:
        abs_file_dir = '\"%s%s%s\"' % (file_dir, os.sep, file_name)
    else:
        abs_file_dir = '\"%s%s*.*\"' % (file_dir, os.sep)
    connections.execute_shell_command('del /F /Q %s' % abs_file_dir)


def directory_empty(dir):
    """This keyword empties directory includes files and subdirectories.

    | Input Parameters | Man. | Description |
    | dir              | Yes  | Source file directory |

    Example
    | Directory Empty | D:\\Desktop |
    """

    # first remove all the files in dir
    file_remove(dir)
    # then remove all
    ret = connections.execute_shell_command('dir /AD %s' % dir)
    lines = ret.splitlines()
    for line in lines:
        if line.find('<DIR>') > 0:
            sub_dir = line.split()[4]
            if sub_dir != '.' and sub_dir != '..':
                directory_remove('%s%s%s' % (dir, os.sep, sub_dir))


def directory_remove(dir, sub_dir=True):
    """This keyword removes directory.

    | Input Parameters | Man. | Description |
    | dir              | Yes  | Source file directory |
    | sub_dir          | No   | Also remove subdirectory? Default is True |

    Example
    | Directory Remove | D:\\Desktop |
    """

    if sub_dir:
        connections.execute_shell_command_without_check('rmdir /S /Q %s' % dir)
    else:
        connections.execute_shell_command_without_check('rmdir /Q %s' % dir)


def get_file_name_in_folder(parent_dir, file_pattern=''):
    """This keyword gets file with given file pattern in given directory.

    | Input Parameters | Man. | Description |
    | parent_dir       | Yes  | Target directory for file searching |
    | file_pattern     | No   | File pattern for file filtering, regular expression supported |

    | Return value | The absolute file path with the given file pattend, for example ".log" |

    Example
    | Get File Name In Folder | C:\\ | log |
    """

    ret = connections.execute_shell_command('dir /A /B /O-D "%s"' % parent_dir)
    lines = ret.splitlines()

    for line in lines:
        try:
            if re.match(file_pattern, line):
                return os.path.join(parent_dir, line)
        except ValueError:
            pass

    raise Exception, 'no any files found with pattern (%s)' % (file_pattern)

def get_last_modified_file(parent_dir, file_ext, file_pattern=""):
    """This keyword gets latest modified file in given directory,
        no matter the OS type is windows or linux.

    | Input Parameters | Man. | Description |
    | parent_dir       | Yes  | Target directory for file searching |
    | file_ext         | Yes  | File extention for file filterring |
    | file_pattern     | No   | File pattern for file filtering, default is for Counter file |

    | Return value | The absolute file path of last modified file |

    Example
    | Get Last Modified File | /root | txt |
    """
    from BtsShell.high_shell_lib.common_operation import _GetRuntimeVar
    connection_type = connections.get_current_connection_type()

    if connection_type == 'Windows':
        if _GetRuntimeVar("BTS_CONTROL_PC_LAB") == connections.BTSTELNET._current.host:
            if not os.path.exists(parent_dir):
                raise Exception, 'Given path "%s" is not exists!' % parent_dir
            mtime = lambda f: os.stat(os.path.join(parent_dir, f)).st_mtime
            match_pattern = file_pattern == '' and '.' or '^.*%s' % file_pattern
            latestFiles = list(sorted([f for f in os.listdir(parent_dir) if (os.path.splitext(f)[-1] \
                                      == file_ext or f.endswith(file_ext)) and  re.match(match_pattern, f)], key=mtime, reverse=True))
            for f in latestFiles:
                print f
            if latestFiles:
                #SYSLOG_008.LOG
                UDPLOG_PAT = "SYSLOG_(\d+)\.LOG"
                if not re.match(UDPLOG_PAT, latestFiles[0].strip(), re.I):
                    latestFile = latestFiles[0]
                else:
                    if len(latestFiles) == 1:
                        latestFile = latestFiles[0]
                    else:
                        firstFileID = re.match(UDPLOG_PAT, latestFiles[0], re.I).group(1)
                        secondFileID = re.match(UDPLOG_PAT, latestFiles[1], re.I).group(1)
                        if mtime(os.path.join(parent_dir,latestFiles[0])) == mtime(os.path.join(parent_dir,latestFiles[1])):
                            if int(secondFileID) - int(firstFileID) == 1:
                                latestFile = latestFiles[1]
                            else:
                                latestFile = latestFiles[0]
                        else:    
                            latestFile = latestFiles[0]
            else:
                raise Exception, 'no any files found with extention (%s) and with pattern (%s)' \
              % (file_ext, file_pattern)        
            return os.path.join(parent_dir, latestFile)
            
                
        else:
            ret = connections.execute_shell_command('dir /A /B /O-D-S "%s"' % parent_dir)
            lines = ret.splitlines()
            match_pattern = file_pattern == '' and '.' or '^.*%s' % file_pattern
    
            for line in lines:
                try:
                    (file_name, file_extention) = line.split('.')
                    print file_extention
                    if file_extention == file_ext and re.match(match_pattern, line):
                        file_full_path = os.path.join(parent_dir, line)
                        connections.execute_shell_command('dir "%s"' % file_full_path)
                        return file_full_path
                except ValueError:
                    pass
    elif connection_type == 'Linux':
        ret = connections.execute_shell_command('ls -tl "%s"|awk \'{print $9}\'' % parent_dir)
        lines = ret.splitlines()
        match_pattern = '.*%s.*\.%s' % (file_pattern, file_ext)

        for line in lines:
            if re.search('\[0\;0m', line):
                line = re.sub('\[0\;0m', '', line)
                line = re.sub('\[0m', '', line)
            try:
                ret = re.match(match_pattern, line)
                if ret:
                    return str2unicode(line)
            except ValueError:
                pass

    raise Exception, 'no any files found with extention (%s) and with pattern (%s)' \
          % (file_ext, file_pattern)
          
def get_last_modified_file_linux(parent_dir, file_ext, file_pattern=""):
    """This keyword gets latest modified file in given directory,
        no matter the OS type is windows or linux.

    | Input Parameters | Man. | Description |
    | parent_dir       | Yes  | Target directory for file searching |
    | file_ext         | Yes  | File extention for file filterring |
    | file_pattern     | No   | File pattern for file filtering, default is for Counter file |

    | Return value | The absolute file path of last modified file |

    Example
    | Get Last Modified File | /root | txt |
    """
    
    ret = connections.execute_ssh_command('ls -tl "%s"|awk \'{print $9}\'' % parent_dir)
    lines = ret.splitlines()
    match_pattern = '.*%s.*\.%s$' % (file_pattern, file_ext)

    for line in lines:
        if re.search('\[0\;0m', line):
            line = re.sub('\[0\;0m', '', line)
            line = re.sub('\[0m', '', line)
        try:
            ret = re.match(match_pattern, line)
            if ret:
                connections.execute_ssh_command_without_check('ls -tl "%s"' % parent_dir)
                return str2unicode(line)
        except ValueError:
            pass

    raise Exception, 'no any files found with extention (%s) and with pattern (%s)' \
          % (file_ext, file_pattern)

def get_last_modified_directory(parent_dir):
    """This keyword gets latest modified directory in given parent directory.

    | Input Parameters | Man. | Description |
    | parent_dir       | Yes  | Target directory for directory searching |

    | Return value | The absolute directory path |

    Example
    | Get Last Modified Directory | C:\\ |
    """

    ret = connections.execute_shell_command('dir /AD /B /O-D "%s"' % parent_dir)
    lines = ret.splitlines()

    try:
        if 'SessionHistory' in lines[1]:
            return os.path.join(parent_dir, lines[2]) # return second line of response
        else:
            return os.path.join(parent_dir, lines[1])
    except ValueError:
        raise Exception, 'no any directories found in given path (%s)' % parent_dir


def copyfile2local(remote_host, username, password, remote_file_dir, local_file_dir, trans_type='scp', timeout="600"):
    """This keyword copies the remote file to local host using 'pscp.exe' application.

    | Input Parameters | Man. | Description |
    | remote_host      | Yes  | remote host IP |
    | username         | Yes  | remote host user name  |
    | password         | Yes  | remote host password |
    | remote_file_dir  | Yes  | remote file directory |
    | local_file_dir   | Yes  | local file directory |
    | trans_type       | No   | transport type:scp or sftp  |

    example
    | copyfile2local  | 192.168.255.100 | tdlte-tester | btstest | C:\\tm500_log\\20100302_PORT_LOG.csv | C:\\personal\\mylog.csv |
    | copyfile2local  | 192.168.255.100 | tdlte-tester | btstest | C:\\tm500_log\\20100302_PORT_LOG.csv | C:\\personal\\mylog.csv |
                      | sftp |

    """

    remote_file_dir = remote_file_dir.replace('\\', '\\\\')
    remote_file_dir = remote_file_dir.replace('\\\\ ', '\\ ').replace('(', '\\(').replace(')', '\\)')
    #command_scp = 'pscp -r -q -scp -unsafe -pw %s %s@%s:\"%s\" \"%s\"' % (password, username, remote_host, remote_file_dir, local_file_dir)
    command_scp = '%s -r -q -scp -unsafe -pw %s %s@%s:\"%s\" \"%s\"' \
                  % (pscpPath, password, username, remote_host, remote_file_dir, local_file_dir)
    #command_sftp = 'pscp -r -q -sftp -unsafe -pw %s %s@%s:\"%s\" \"%s\"' % (password, username, remote_host, remote_file_dir, local_file_dir)
    command_sftp = '%s -r -q -sftp -unsafe -pw %s %s@%s:\"%s\" \"%s\"' \
                  % (pscpPath, password, username, remote_host, remote_file_dir, local_file_dir)

    if trans_type == 'scp':
        command = command_scp
    elif trans_type == 'sftp':
        command = command_sftp
    else:
        command = "None"
        raise Exception, "please give right trans type! scp or sftp"

    print '*DEBUG* command = %s' % command

    if timeout:
        old_timeout = connections.set_shell_timeout(timeout)
        try:
            ret = connections.execute_shell_command_without_check(command)
            if ret.find('y/n') >= 0:
                connections.execute_shell_command_without_check('y')
        finally:
            connections.set_shell_timeout(old_timeout)
    else:
        ret = connections.execute_shell_command_without_check(command)
        if ret.find('y/n') >= 0:
            connections.execute_shell_command_without_check('y')

    raw_return_code = connections.execute_shell_command_without_check('echo %ERRORLEVEL%')
    return_lines = raw_return_code.splitlines()
    return_code = int(return_lines[1])
    if return_code != 0:
        raise Exception, "command [%s] execution failed" % command


def copyfile2remote(remote_host, username, password, remote_file_dir, local_file_dir, trans_type='scp', timeout=None):
    """This keyword copies the local file to remote host using 'pscp.exe' application.

    | Input Parameters | Man. | Description |
    | remote_host      | Yes  | remote host IP |
    | username         | Yes  | remote host user name  |
    | password         | Yes  | remote host password |
    | remote_file_dir  | Yes  | remote file directory |
    | local_file_dir   | Yes  | local file directory |
    | trans_type       | No   | trans type:scp or sftp |

    example
    | copyfile2remote  | 192.168.255.100 | tdlte-tester | btstest | C:\\tm500_log\\20100302_PORT_LOG.csv | C:\\personal\\mylog.csv |
                       | sftp |
    """
    remote_file_dir = remote_file_dir.replace('\\', '\\\\')
    remote_file_dir = remote_file_dir.replace('\\\\ ', '\\ ').replace('(', '\\(').replace(')', '\\)')
    if trans_type == 'scp':
        command = '%s -r -q -scp -pw %s \"%s\" %s@%s:\"%s\" ' % \
            (pscpPath, password, local_file_dir, username, remote_host, remote_file_dir)
    elif trans_type == 'sftp':
        command = '%s -r -q -sftp -pw %s \"%s\" %s@%s:\"%s\" ' % \
             (pscpPath, password, local_file_dir, username, remote_host, remote_file_dir)
    else:
        raise Exception, "Error,please enter right trans type,scp or sftp!"

    print command
    print '*DEBUG* command = %s' % command

    if timeout:
        old_timeout = connections.set_shell_timeout(timeout)
        try:
            ret = connections.execute_shell_command_without_check(command)
            if ret.find('y/n') >= 0:
                connections.execute_shell_command_without_check('y')
        finally:
            connections.set_shell_timeout(old_timeout)
    else:
        ret = connections.execute_shell_command_without_check(command)
        if ret.find('y/n') >= 0:
            connections.execute_shell_command_without_check('y')

    raw_return_code = connections.execute_shell_command_without_check('echo %ERRORLEVEL%')
    return_lines = raw_return_code.splitlines()
    return_code = int(return_lines[1])
    if return_code != 0:
        raise Exception, "command [%s] execution failed" % command


def get_unique_value_from_file(filename, keyword, searchtime=10):
    """This keyword reads TM500 log to get a keyword's special value.

    | Input Parameters  | Man. | Description |
    | filename          | Yes  | Configuration file directory |
    | keyword           | Yes  | The unique keyword in this filename  |
    | searchtime        | No   | Avoid file is to large to bring timeout  |

    | Return value | The list contains unique value with reading order |

    Example
    | Get Unique Value From File | C:\\100601_113514_TDLTE-B7HGT2X_PROT_LOG_ALL.csv | ueCapabilityRAT-Container | 100 sec |
    """

    try:
        file_handle = file('%s' % (filename), 'r')
    except:
        raise Exception,  "filename %s open failed" % filename

    lines = file_handle.readlines()
    try:
        for line in lines:
            if keyword in line:
                print "%s" % line
                break
        rule = '^\s*.*\s\'?([0-9A-F]+)\'?[A-Z]?'
        str = re.match(rule,line)
        value = str.group(1)
        return value
    finally:
        file_handle.close()


def get_subframe_from_index(srsindex, sfn , ueperstr = '10ms'):
    """This keyword get subframe number in different ue periodicity.

    | Input Parameters | Man. | Description |
    | srsindex         | Yes  | srs-ConfigIndex from rrc_set_up message |
    | sfn              | Yes  | SFN get from ULSRS log |
    | ueperstr         | No   | ue srs periodicity  |

    example
    | Get Subframe From Index | 3 | 928 | 10ms |
    """

    srsindex = int(srsindex)
    subfr_num = []
    ueper = int(ueperstr[:-2])
    inner_dict = {'5ms':10, '10ms':15, '20ms':25, '40ms':45, '80ms':85, '160ms':165, '320ms':325}
    for ueper_dict in inner_dict.keys():
        if ueper_dict == ueperstr:
            Time_offset = srsindex - inner_dict[ueper_dict]
            if Time_offset < 0 or Time_offset > ueper:
                raise Exception, 'the srsindex is out of range.'
            for K_srs in range(0,10):
                if (10*sfn+K_srs-Time_offset)%ueper==0:
                    if K_srs == 0 or K_srs == 1:
                        subfr_num += [1]
                    elif K_srs == 5 or K_srs == 6:
                        subfr_num += [6]
                    else:
                        subfr_num += [K_srs]
                else:
                    continue
            return subfr_num
        else:
            print "The ueper input is incorrect"


def get_counter_file_remain_time(time_info, period='15'):
    """This keyword get the time message from the given information using RegExp and then
    calculate the remain time in seconds.

    | Input Parameters | Man. | Description |
    |   time_info      | Yes  | information including remain time message |
    |     period       |  No  | point-in-time for counter file refresh   |

    example
    | Get Counter File Remain Time | Thu Dec 23 16:15:37 CST 2010 |
    """

    ret = re.search("\s([0-9]{2}\:[0-9]{2}\:[0-9]{2})\s", time_info)
    if ret:
        time = ret.group(1)
        time_list = time.split(":")
        int_period = int(period)
        return str((int_period-int(time_list[1])%int_period)*60 - int(time_list[2]) + 80)
    else:
        return '900'
        raise Exception, 'The infomation do not include time'

def get_contain_keyword_lines(source_file_dir, keywords, dest_file_name='', tag_name='log_file', msg=None):
    """This keyword checks whether file contains specified keyword.
    It will copy the source file to the directory '${CURRENT_WORKING_DIR}/log' which will be
    published with report/log file so user can get the whole file through HTML link

    | Input Parameters | Man. | Description |
    | source_file_dir  | Yes  | Source file directory |
    | keywords         | Yes  | Keywords for search in file |
    | dest_file_name   | No   | Destination file name, default is '' and file name will remain the same |
    | tag_name         | No   | HTML tag name, default is 'log_file' |
    | msg              | No   | Special messages for error case |

    | Return value | list of lines found in file with given keywords |

    Example
    | get_contain_keyword_lines | C:\\test.txt | PBCH | UDPLog.log | UDP_Log |
    """

    try:
        file_handle = file(source_file_dir, 'r')
    except:
        raise Exception, "Open file '%s%' failed" % source_file_dir

    lines = file_handle.readlines()

    not_found_keywords = []
    search_keywords = []
    contain_lines = []

    for line in lines:
            if keywords in line:
                print '*DEBUG*keyword (%s) found in line (%s)' % (keywords, line)
                contain_lines.append(line)
    msg = _get_string_msg(source_file_dir, search_keywords, msg, 'does not contain')
    file_handle.close()

    if len(search_keywords) != 0: # not all keywords found
        asserts.fail(msg)

    return contain_lines

def get_contain_element_from_list(Source_list, keywords):
    """This keyword checks whether file contains specified keyword.
    It will copy the source file to the directory '${CURRENT_WORKING_DIR}/log' which will be
    published with report/log file so user can get the whole file through HTML link

    | Input Parameters | Man. | Description |
    | Source_list      | Yes  | Source List |
    | keywords         | Yes  | Keywords for search in list |

    | Return value | list of lines found in Source_list  |

    Example
    | get_contain_element_from_list | Source_list |  PBCH  |
    """
    List_contain_list = []
    try:
        for element in Source_list:
            print element
            if keywords in element:
                List_contain_list.append(element)
    finally:
        return List_contain_list

def no_duplicate_list(Source_list):
    """This keyword deleteduplicate value in the source_list

    | Input Parameters | Man. | Description |
    | Source_list      | Yes  | Source List |

    | Return value | list of no duplicate   |

    Example
    | no_duplicate_list | Source_list  |
    """
    no_duplicate_list = []
    if type(Source_list) != type([]):
        ret_list = [Source_list]
        return ret_list
    else:
        for element in Source_list:
            if element not in no_duplicate_list:
                no_duplicate_list.append(element)
        return no_duplicate_list



def get_ue_ip(information):
    ue_ip = []
    info_list = information.split('\n')
    try:
        for item in info_list:
            m = re.search(IP_PATTERN,item)
            if m:
                ue_ip.append(m.group())
        if  len(ue_ip) == 1:
            ue_ip = ue_ip[0]
        return ue_ip
    finally:
        if len(ue_ip) == 0:
            raise Exception, "Do not contain any IP information"


def write_into_bat_for_DL(ip, port, bandwidth, bat_dir):
    bat_info = "@echo off\n"
    command = "start miperf.exe -c "

    try:
        if bat_dir.find('.bat') < 0:
            time_string = time.strftime("%Y%m%d%H%M%S")
            bat_dir = bat_dir + '\\' + 'DL_%s.bat' %time_string
        file_obj = open(bat_dir, 'a+')

        if type(ip) == str or type(ip) == unicode:
            jperf_cmd = command + "%s -u -P 1 -i 1 -p %s -l 1024.0B -f k -b %sM -t 999999 -T 1\n" % (ip, port, bandwidth)
            bat_info += jperf_cmd
        elif type(ip) == list:
            for item in ip:
                jperf_cmd = command + "%s -u -P 1 -i 1 -p %s -l 1024.0B -f k -b %sM -t 999999 -T 1\n" % (item, port, bandwidth)
                bat_info += jperf_cmd
                port = int(port) + 1
        else:
           raise Exception, "Wrong IP type,please check!"
        file_obj.write(bat_info)
        return bat_dir

    finally:
        file_obj.close()

def str2unicode(mesg):
    string = ''
    ascii_list = map(unichr, range(32, 127))
    for i in mesg:
        if i in ascii_list:
            string += i
    return string


def calc_timegap_in_millisecond(t1,t2,basevalue='',tolvalue=''):
    """get the gap of two time and check if it meet the basevalue
     and tolerance value, if the third and four parameters is null, will
     return the interval value, else it will judge the interval value with
     basevalue and tolvalue.
    | Input Parameters  | Man. | Description |
    | t1                | Yes  | first time (should be 'HH:MM:SS:MS')|
    | t2                | Yes  | second time(should be 'HH:MM:SS:MS')|
    | basevalue         | No   | basevalue |
    | tolvalue          | No   | tolerance value millisecond|

    | return            | No   | the two time interval value|

    Example
    | calc_timegap_in_millisecond |'23:59:59:999'|'00:00:10:240'|10240|1|
    |Return value=| calc_timegap_in_millisecond |'23:59:59:999'|'00:00:10:240'|
    """
    time1 = []
    time2 = []
    tmp1 = []
    tmp2 = []

    t1 = t1.split(':')
    t2 = t2.split(':')
    for i in range(len(t1)):
        time1.append(int(t1[i]))
    for i in range(len(t2)):
        time2.append(int(t2[i]))
    if time1[0] == time2[0]:
        pass
    elif time1[0] != time2[0] and time1[0] >20 and time2[0] == 0:
        time2[0] = 24
    elif time1[0] != time2[0] and time1[0] <20 and time2[0] == 0:
        time2[0] = 12
    else:
        pass
    try:
        tmp1 = ((time1[0]*60+time1[1])*60+time1[2])*1000+time1[3]
        tmp2 = ((time2[0]*60+time2[1])*60+time2[2])*1000+time2[3]
        inval = tmp2-tmp1
        if basevalue == '' and tolvalue =='':
            if inval >=0:
                return inval
            else:
                raise Exception,'ERROR:The second time you input is \
                      before the first one'
        else:
            tolvalue=int(tolvalue)
            basevalue=int(basevalue)
            if inval == basevalue or inval+tolvalue == basevalue or\
               inval-tolvalue == basevalue:
                print 'SUCCESS: The two time interval is just your basevalue!'
                pass
            else :
                raise Exception, "The time interval of the two time is not the basevalue"
    finally:
        pass

def check_key_in_xml_file(file_dir, key):
    """check key in xml file.

    | Input Paramaters   | Man. | Description |
    | file_dir           | yes  | counter xml file abs path |
    | key                | yes  | key name                  |

    | return value       | True  | the key is in xml file     |
                         | False | the key is not in xml file |
    Example
    | check key in xml file | D:\FlexiBTSProperties.xml | Murkku2 |
    """
    try:
        file_handle = file(file_dir, 'r')
    except:
        raise Exception, "Counter file '%s' open failed" % file_dir

    search_pattern = "<Name>%s</Name>" % (key)
    try:
        lines = file_handle.readlines()
        for line in lines:
            search_result = re.search(search_pattern, line)
            if search_result:
                return True

    finally:
        file_handle.close()
    return False

def get_list_value_appeared_format(src_list):
    temp = src_list[0]
    format = [temp]
    for item in src_list:
        if item != temp:
            temp = item
            format.append(temp)
        else:
            pass
    return format

def get_remote_file_size(file_dir):
    """Get file size for specific file by using command "dir" if OS is Windows
    or "ls -l" if OS is Linux.

    | Input Paramaters | Man. | Description |
    | file_dir         | Yes  | file directory |

    Example
    | Get File Size | "D:\\Script\\TestCase\\trunk\\common_operation.py" |
    | Get File Size | "/opt/scripts/common_operation.py" |
    """
    file_path = os.path.dirname(file_dir)
    file_name = os.path.basename(file_dir)
    connection_type = connections.get_current_connection_type()
    if connection_type == 'Windows':
        cmd = 'dir "%s"' % (file_path)
    elif connection_type == 'Linux':
        cmd = 'ls -l "%s"' % (file_path)

    ret = connections.execute_shell_command_without_check(cmd)
    for line in ret:
        print line
        if re.search("\s%s\n" % (file_name), line):
            ret_search = re.search(".*\s([0-9]+(,[0-9]+)?)\s.*", line)
            if ret_search:
                file_size = ret_search.group(1)
                return file_size

    print "Get file size failed"
    return False

def check_folder_or_file_exist(full_path, connect_type = "telnet"):
    """this keyword simple judge full_path folder or file exist or not in current telent connection.
    | Input Paramaters | Man. | Description |
    | full_path        | Yes  | 'd:\\test' |
    | connect_type     | no  | default as 'telnet' you can change it such as 'ssh' |
    | Return value     | if folder exist return 'True' else return 'False' |
    Example
    | switch host connection | ${TM500_Control_PC} |  |
    | ${result} | check folder or file exist | 'd:\\Lib' |
    | switch host connection | ${BTS_Control_PC} |  |
    | ${result} | check folder or file exist | 'C:\\test.txt' |
    | switch host connection | ${FCTB} |  |
    | ${result} | check folder or file exist | '/ffs/fs1/config/SCFC_1.xml' | ssh |    
    """
    if connect_type == "telnet":        
        ret = connections.execute_shell_command_without_check("ls \"%s\""%full_path)
    else:        
        ret = connections.execute_ssh_command_without_check("ls \"%s\""%full_path)
    if (0 <= ret.find('No such file or directory')) or \
            (0 <= ret.find('not found')):
        return False
    return True


def check_tm500_pc_exe_exist(file_dir, exe_list, bts_pc_conn, tm500_pc_conn):
    """check tm500 control pc psexec.exe and iperf.exe exist. if not copy from bts control pc.

    | Input Paramaters | Man. | Description |
    | file_dir         | Yes  | 'd:\\resources\\tools' |
    | exe_list         | yes  | ['psexec.exe', 'iperf.exe']  |
    | bts_pc_conn      | Yes  | ${BTS_CONTROL_PC_CONNECTION} |
    | tm500_pc_conn    | yes  | ${TM500_CONTROL_PC_CONNECTION}  |

    Example
    | ${check_list} | create list | psexec.exe | iperf.exe |
    | check_tm500_pc_exe_exist | ${tools_dir} | ${check_list} | ${BTS_CONTROL_PC_CONNECTION} | ${TM500_CONTROL_PC_CONNECTION} |

    """
    connections.switch_host_connection(tm500_pc_conn)
    tmp = check_folder_or_file_exist(file_dir)
    if not tmp:
        connections.execute_shell_command_without_check("mkdir %s"%file_dir)

    for exe in exe_list:
        tar_file = "%s.tar" % exe
        exe_path = os.path.join(file_dir, exe)
        tar_path = os.path.join(file_dir, tar_file)
        tmp2 = check_folder_or_file_exist(exe_path)

        if not tmp2:
            connections.switch_host_connection(bts_pc_conn)
            connections.execute_shell_command("cd %s" % file_dir)
            connections.execute_shell_command("tar -cf %s %s" % (tar_file, exe))
            copyfile2remote(tm500_pc_conn.host, tm500_pc_conn.user, \
                            tm500_pc_conn.password, tar_path, tar_path)
            connections.switch_host_connection(tm500_pc_conn)
            connections.execute_shell_command("cd %s" % file_dir)
            connections.execute_shell_command("tar -xf %s -C ." % tar_file)
            connections.execute_shell_command("rm %s.tar" % exe)


def get_appear_times(sequence, *element):
    """
    get the appear time from a sequence, it can be a list, tuple, set, or dictionary.
    | Input Paramaters | Man. | Description |
    | sequence         | Yes  | can be list, tuple, set, dictionary, or generator. if given a dictionary, \
                                it will process it's keys.|
    | element          | No   | The elements of sequence.|

    | Return value     | Yes  | if element given , will return the appear times of this elements, else return \
                                the max/min appear times of element in sequence |
    Example
    | get_appear_times | [1,2,2,1,4,2,1,2] | 2 |
    | get_appear_times | [1,2,2,1,4,2,1,2] |
    | get_appear_times |  xrange(10)       | 1 |

    """

    from itertools import groupby

    lst = list(sequence)
    result = {}
    #generate a dic key is the elements, values is it's appear times
    for k, v in groupby(sorted(lst)):
        result[k] = len(list(v))

    del groupby, lst, sequence, k, v

    if element:
        items = []
        for item in element:
            if item in result.keys():
                print "*INFO* Element: \"%s\" appeared %s times." %(item, result[item])
                items.append(result[item])
            else:
                print "*WARN* The element you input(\"%s\") is not in the sequence!" %item
        return len(items)==1 and items[0] or items
    else:
        tmp = sorted(result, key=lambda x:result[x], reverse=True) #sorted by the value, from big to small.
        print "*INFO* Max: \"%s\" appeared %s times." %(tmp[0], result[tmp[0]])
        print "*INFO* Min: \"%s\" appeared %s times." %(tmp[-1], result[tmp[-1]])
        return tmp[0], tmp[-1]

def path_split_driver(full_path):
    driver, rest = os.path.splitdrive(full_path)
    return driver, rest

def get_para_dict_from_file(file_dir, split_tag='='):
    """this keyword get parameters dictionary from file.
    | Input Paramaters | Man. | Description |
    | file_dir         | Yes  | parameters file directory |
    | split_tag        | No   | default as "=" |
    | return | parameters dictionary |

    Example
    | ${para_dict}    | get_para_dict_from_file | "D:\\para.txt" |
    | ${actCiphering} | Get From Dictionary     | ${para_dict}   | actCiphering |

    """

    lines = file_read(file_dir)
    kv_dic = {}
    for line in lines:
        tmp = line.split(split_tag)
        if 2 == len(tmp):
            key = tmp[0].strip()
            value = tmp[1].strip()
            kv_dic[key] = value
            print "Get parameter %s=%s ." % (key,value)
    return kv_dic

def get_info_from_file(file_path,hw_type,target_info):
    """ This keyword is search target_info accoding hw_type in file. return true or false

    | Input Parameters | Man. | Description |
    | file_path        | Yes  | Source file path |
    | hw_type          | Yes  | type of hardware, such as "FZHA1", "FZNC2" |
    | target_info      | Yes  | info user want to find in file, such as "TDL02.01.R99G" |

    Example
    | get_info_from_file | D:\\SiteInformation_BENZ_20130110.txt | FZHA1 | TDL02.01.R99G |
    | get_info_from_file | D:\\SiteInformation_BENZ_20130110.txt | FSMF1 | LNT3.0_ENB_1210_010_00 |

    """
    # check file exist
    lines = file_read(file_path)

    # check file contain the flag
    search_info = 'CORE_'+hw_type[:len(hw_type)-1]+' '+hw_type[len(hw_type)-1]
    for line in lines:
        search_result = re.search(search_info,line)
        if search_result <> None:
            search_result2 = re.search(target_info,line)
            if search_result2 <> None:
                return True
    return False

def date_to_second(time_string):
    """ This keyword calculate delta-T from input time to 1970-1-1

    | Input Parameters | Man. | Description |
    | time_string  | Yes  | format as '2011-02-28 17:44:30' or '2011-02-28-17-44-30' or '20130827122619' |

    Example
    | date_to_second | 2013-02-04 17:34:30 |

    """ 
    if len(time_string)==19:
        time_string = time_string.replace(' ','-').replace(':', '-') 
    elif len(time_string) == 14: 
        t_list = []
        for i in range(0, 14, 2):
            t_list.append(time_string[i:i+2])

        time_string = '-'.join(t_list)  
        time_string = time_string.replace('-','',1)       
    else:
        raise Exception, "Time format is not match, it should be \
'2011-02-28 17:44:30' or '2011-02-28-17-44-30' or '20130827122619'"    
        
    return time.mktime(time.strptime(time_string, "%Y-%m-%d-%H-%M-%S"))

def second_to_date(second, format=1):
    """ This keyword return date format from seconds(delta-T of 1970-1-1)

    | Input Parameters | Man. | Description |
    | second  | Yes  | seconds to 1970-1-1 |
    | format  | No  | default 1 as '2013-02-04 17:34:30', if 2 as '2011-02-28-17-44-30', if 3 as '20130827122619' |

    Example
    | date_to_second | 2013-02-04 17:34:30 |

    """ 
    format_time = ""
    if 1 ==  int(format): 
        format_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(second))
    elif 2 ==  int(format): 
        format_time = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(second))        
    elif 3 ==  int(format): 
        format_time = time.strftime("%Y%m%d%H%M%S",time.localtime(second))  
    else:    
        format_time = time.strftime("%Y%m%d%H%M%S",time.localtime(second))  
    return format_time

def calculate_delta_time(time_string1, time_string2, format="hour"):
    """ This keyword calculate delta-T from input time to 1970-1-1

    | Input Parameters | Man. | Description |
    | time_string1        | Yes  | format as "2011-02-28 17:44:30" |
    | time_string2        | Yes  | format as "2011-02-28 17:44:39" |
    | format              | No   | default as hour, other could be minute or second |

    Example
    | time_to_second | 2013-02-04 17:34:30 | 2013-02-04 14:24:30 | hour |

    """    
    time1 = date_to_second(time_string1)
    time2 = date_to_second(time_string2)
    if "hour" == format:
        delta_time = float(abs(time1 - time2) / 3600)
    elif "minute" == format:
        delta_time = float(abs(time1 - time2) / 60)
    else:
        delta_time = float(abs(time1 - time2))
    return delta_time

def get_file_signature(verify_signature_cmd):
    """This keyword checks p7 file signature with verify command.
    It will return 'good signature', 'bad signature' or 'other'
    other means all the status excepte good and bad signature

    | Input Parameters      | Man. | Description |
    | verify_signature_cmd  | Yes  | craverify file signature command |

    | Return value          | return this file signature status |

    Example
    | get_file_signature    | craverify /ffs/fs1/vendor_HD405400.xml /ffs/fs1/vendor_HD405400.xml.p7|
    """

    signature_status = ''
    ret = connections.execute_ssh_command_without_check(verify_signature_cmd)
    if 'good signature' in ret:
        signature_status = 'good signature'
    elif 'bad signature' in ret:
        signature_status = 'bad signature'
    else:
        signature_status = ''
        ret = connections.execute_ssh_command_without_check(verify_signature_cmd)
        if 'good signature' in ret:
            signature_status = 'good signature'
        elif 'bad signature' in ret:
            signature_status = 'bad signature'
        else:
            signature_status = 'other'

    return signature_status
    
def craverify_file(file_input):
    """ This keyword is used to verify file signature in active partition with file(s) you have input

    | Input Parameters | Man. | Description |
    | file_input       | Yes  | file or file list you want to verify signature |

    | Return value     | return two info if verify passed, first is True with index 0, second is good signature file/or file list\
                         return four info if verify failed, first is False with index 0, second is bad signature file/or file list\
                         third is not clear signature file/or file list, fourth is not existed file/or file list|
    

    Example
    | craverify_file | /flash/vendor_HD401700.xml |
    | craverify_file | @{file_list}               |

    """
    bad_signature_list = []
    good_signature_list = []
    other = []
    not_exist = []
    file_lists = []

    if not isinstance(file_input,list):
        file_lists.append(file_input)
    else:
        file_lists = file_input

    for f in file_lists:
        check_exist_cmd = 'find ' + f
        temp = connections.execute_ssh_command_without_check(check_exist_cmd)
        if 'No such file or directory' in temp:
            not_exist.append(f)
        else:
            cmd = 'craverify ' + f + " " + f + '.p7'
            ret = get_file_signature(cmd)
            if ret == 'good signature':
                good_signature_list.append(f)
            elif ret == 'bad signature':
                bad_signature_list.append(f)
            else:
                other.append(f)
        
    for f in bad_signature_list:
        print "*ERR* bad signature for file:%s\n" % f
    for f in other:
        print "Warning: not clear signature status for file:%s\n" % f
    for f in not_exist:
        print "not existed file:%s" % f

    if bad_signature_list == [] and other == [] and not_exist == []:
        return True, good_signature_list
    else:
        return False,bad_signature_list,other,not_exist 


def crasign_file(file_input):
    """ This keyword is used to sign file signature in active partition with file(s) you have input

    | Input Parameters | Man. | Description |
    | file_input       | Yes  | file or file list you want to sign signature |

    | Return value     | return two info if signed passed, first is True with index 0, second is good signature file/or file list\
                         return four info if signed failed, first is False with index 0, second is bad signature file/or file list\
                         third is not clear signature file/or file list, fourth is not existed file/or file list|
    

    Example
    | crasign_file | /flash/vendor_HD401700.xml |
    | crasign_file | @{file_list}               |

    """
    
    bad_signature_list = []
    good_signature_list = []
    other = []
    not_exist = []
    file_lists = []

    if not isinstance(file_input,list):
        file_lists.append(file_input)
    else:
        file_lists = file_input

    for f in file_lists:   # sign signature
        check_exist_cmd = 'find ' + f
        temp = connections.execute_ssh_command_without_check(check_exist_cmd)
        if 'No such file or directory' in temp:
            not_exist.append(f)
        else:
            # remove target p7 file before sign
            cmd = 'rm -rf ' + f + '.p7'
            connections.execute_ssh_command_without_check(cmd)
            # sign target file
            cmd = 'crasign ' + f
            connections.execute_ssh_command_without_check(cmd)
        
    for f in file_lists:     # verify after signed
        if f not in not_exist:
            cmd = 'craverify ' + f + " " + f + '.p7'
            ret = get_file_signature(cmd)
            if ret == 'good signature':
                good_signature_list.append(f)
            elif ret == 'bad signature':
                bad_signature_list.append(f)
            else:
                other.append(f)
    
    for f in bad_signature_list:
        print "*ERR* bad signature for file:%s\n" % f
    for f in other:
        print "Warning: not clear signature status for file:%s\n" % f
    for f in not_exist:
        print "not existed file:%s" % f
        
    if bad_signature_list == [] and other == [] and not_exist == []:
        return True, good_signature_list
    else:
        return False,bad_signature_list,other,not_exist 

def combine_wirshark_hex_info(source_file_path, target_file_path):
    """ This keyword is used to combine wireshark log hex part.
    such as source:
        0000  ac 16 2d a7 8b 78 00 26 88 7b 18 23 08 00 45 00   ..-..x.&.{.#..E.
        0010  00 ae 17 06 00 00 fb 06 3e e5 0a 44 b3 e2 0a 44   ........>..D...D
        0020  a0 f4 cc 2e 1f 42 b6 28 83 3d bf 91 df 5c 80 18   .....B.(.=...\..
        0030  00 66 39 d4 00 00 01 01 08 0a 01 d3 14 78 02 41   .f9..........x.A
        0040  97 90 1a 00 77 30 80 a0 80 80 02 2c 1e 81 02 03   ....w0.....,....
        0050  76 83 02 03 76 00 00 81 05 73 74 61 74 65 82 01   v...v....state..
        0060  00 83 13 4d 52 42 54 53 2d 38 38 36 2f 4c 4e 42   ...MRBTS-886/LNB
        0070  54 53 2d 38 38 36 a4 80 30 80 80 10 4f 70 65 72   TS-886..0...Oper
        0080  61 74 69 6f 6e 61 6c 53 74 61 74 65 81 05 6f 6e   ationalState..on
        0090  41 69 72 82 01 ff 00 00 30 80 80 0a 4c 6f 63 61   Air.....0...Loca
        00a0  6c 53 74 61 74 65 81 09 55 6e 62 6c 6f 63 6b 65   lState..Unblocke
        00b0  64 82 01 ff 00 00 00 00 85 00 00 00               d...........
    target:
        ..-..x.&.{.#..E.........>..D...D.....B.(.=...\...f9..........x.A....w0\
.....,....v...v....state.....MRBTS-886/LNBTS-886..0...OperationalState..onAir..\
...0...LocalState..Unblocked...........
    | Input Parameters | Man. | Description |
    | source_file_path            | Yes | wireshark txt log file path |
    | Return target_file_path     | Yes | combine hex content file path |    

    Example
    | combine_wirshark_hex_info | d:\\test.txt | d:\\test2.txt |

    """
    file_content = file_read(source_file_path) 
    new_content = ""  
    
    frame_line_num = []
    for line in range(len(file_content)):        
        if re.match('^Frame\s*\d+', file_content[line]):
            frame_line_num.append(line)
    
    frame_line_num.append(len(file_content))
    
    for num in range(len(frame_line_num)-1):
        frame_content = file_content[frame_line_num[num]:frame_line_num[num+1]]
        for f in frame_content:                      
            if (f.startswith('0') or f.startswith('1')) and len(f) > 57:
                if f.startswith("0000"):
                    new_content += "\n\n"
                tmp = re.search(r"\s[a-f0-9]{2}\s[a-f0-9]{2}\s{3}(.*)\n", f)
                if tmp:
                    new_content += tmp.groups()[0]       
    new_content = new_content.replace("><", ">\n<")          
    file_write(target_file_path, new_content)

def combine_wirshark_counterid(file_path):
    file_content = file_read(file_path) 
    new_content = ""  
    for line in file_content:
        if 'measurement_id' in line or 'counter_subid' in line:
            new_content += line.strip()
    measure_list = new_content.split('measurement_id:')

    measure_dict = {}
    measure_list = measure_list[1:]
    sub_list = []
    for meas in measure_list:        
        sub_meas = meas.split('counter_subid:')
        meas_id = int(sub_meas[0], 16) 
        counter_list = sub_meas[1:]
        for counter in counter_list:            
            counter_id = int(counter, 16)
            sub_list.append( "M%sC%s" % (meas_id, counter_id))
            
    return set(sub_list)          
 

def generate_random_ip():
    import random
    return "%s.%s.%s.%s" % (random.randint(0,255),
                            random.randint(0,255),
                            random.randint(0,255),
                            random.randint(0,255))    
                      
if __name__ == '__main__':    
    #second = date_to_second('2013-08-27-12-26-19')
    #deta_second = second - 3600*5
    #print second_to_date(deta_second, 3)
    #combine_wirshark_hex_info("d:\\tshark.txt", "d:\\test2.txt")
    combine_wirshark_counterid("D:\\work\\all problems\\fan\\test.txt")
    pass
