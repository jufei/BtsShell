import zipfile
import os.path
import os
import time
import re
from BtsShell import connections
from BtsShell.common_lib.get_path import *

zip_exe_path = os.path.join(get_tools_path(), "7z.exe")
class ZFile(object):
    def __init__(self, filename, mode='r', basedir=''):
        self.filename = filename
        self.mode = mode
        if self.mode in ('w', 'a'):
            self.zfile = zipfile.ZipFile(filename, self.mode, compression=zipfile.ZIP_DEFLATED)
        else:
            self.zfile = zipfile.ZipFile(filename, self.mode)
        self.basedir = basedir
        if not self.basedir:
            self.basedir = os.path.dirname(filename)

    def addfile(self, path, arcname=None):
        path = path.replace('//', '/')
        if not arcname:
            if path.startswith(self.basedir):
                arcname = path[len(self.basedir):]
            else:
                arcname = ''
        self.zfile.write(path, arcname)

    def addfiles(self, paths):
        for path in paths:
            if isinstance(path, tuple):
                self.addfile(*path)
            else:
                self.addfile(path)

    def close(self):
        self.zfile.close()

    def extract_to(self, path):
        for p in self.zfile.namelist():
            self.extract(p, path)

    def extract(self, filename, path):
        if not filename.endswith('/'):
            f = os.path.join(path, filename)
            dir = os.path.dirname(f)
            if not os.path.exists(dir):
                os.makedirs(dir)
            file(f, 'wb').write(self.zfile.read(filename))

    def search_file(self, target):
        for f in self.zfile.namelist():
            if re.search(target, f):
                return f
        raise Exception, "Not find '%s'" % (target)

def zip_file_search(zip_file_path, file_name):
    """This keyword search file in zip file, and return the search file full name

    | Input Parameters  | Man. | Description |
    | zip_file_path          | Yes  | full path of zip file |
    | file_name              | Yes  | target search file name, could be part of name |

    | Return value | the full name of search name |

    Example
    | zip_file_search | D:\\tmp.zip | 'abc.txt' |
    """

    zipf = ZFile(zip_file_path)
    file_path = zipf.search_file(file_name )
    zipf.close()
    print "Find '%s' in '%s'"%(file_name, zip_file_path)
    return file_path

def zip_zip_file_search(zip_file_path, condition):
    """This keyword search file in zip file's zip file, and return the search file full name

    | Input Parameters  | Man. | Description |
    | zip_file_path          | Yes  | full path of zip file |
    | condition              | Yes  | zip file name and search file name |

    | Return value | the full name of search name |

    Example
    | zip_zip_file_search | D:\\tmp.zip | 'bcd.zip\\abc.txt' |
    """

    source_dir, name = os.path.split(zip_file_path)
    zip_name, file_name = condition.split("\\")
    zip1_path = zip_file_search(zip_file_path, zip_name)

    if None != zip1_path:

        unzip_folder = os.path.join(source_dir, name.strip(".zip"))
        zip1 = ZFile(zip_file_path)
        zip1.extract_to(unzip_folder)
        zip1.close()

        zip_full_path = os.path.join(unzip_folder, zip1_path.replace("/", "\\"))
        ret = zip_file_search(zip_full_path, file_name)
        return ret

def zip_folder_file(srcFolderName, file_ext,timeout = 30):
    """This keyword zip all the '.LOG' file of specifical folder.

    | Input Paramaters | Man. | Description |
    | srcFilename      | No   | Absolute path of folder that you want to zip |

    Example
    | Zip Folder File | C:\\Temp\\BTSLogs |
    """
    old_timeout = connections.set_shell_timeout(timeout)
    CurrentDate = time.strftime('%Y%m%d%H%M')

    zipFileName = srcFolderName + os.sep + CurrentDate + '.zip'
    srcFileName = srcFolderName + os.sep + '*.' + file_ext
    try:
        cmd = "%s a \"%s\" \"%s\"" %(zip_exe_path, zipFileName, srcFileName)
        ret = connections.execute_shell_command(cmd)
        return zipFileName
    finally:
        connections.set_shell_timeout(old_timeout)


def unzip_file(zip_file_name, target_folder_name):
    """This keyword can zip all the '.LOG' file of specifical folder.

    | Input Paramaters | Man. | Description |
    | srcFilename      | No   | Absolute path of folder that you want to zip |

    Example
    | Unzip File | C:\\counter.zip | C:\\counter |
    """
    try:
        zip_init = None
        zip_init = ZFile(zip_file_name)
        zip_init.extract_to(target_folder_name)
        print "unzip '%s' to '%s' successfully!" % (zip_file_name, target_folder_name)
    except Exception, error:
        print "unzip '%s' to '%s' failed for '%s'!\nTry to use 7z.exe" % (zip_file_name, target_folder_name, error)
        cmd = "%s x \"%s\" -y -o\"%s\"" %(zip_exe_path, zip_file_name, target_folder_name)
        ret = connections.execute_shell_command_without_check(cmd)
        print "unzip '%s' to '%s' with 7z.exe successfully!" % (zip_file_name, target_folder_name)
        
    finally:
        if zip_init:
            zip_init.close()

def zip_file(src_file_name, zip_file_name):
    """This keyword can zip specifical file.

    | Input Paramaters | Man. | Description |
    | src_file_name    | Yes  | Absolute path of file that you want to zip |
    | zip_file_name    | Yes  | Absolute path of zip file                  |

    Example
    | Unzip File | C:\\counter.txt | C:\\counter.zip |
    """

    cmd = "%s a \"%s\" \"%s\"" %(zip_exe_path, zip_file_name, src_file_name)
    connections.execute_shell_command(cmd)
    return zip_file_name

if __name__ == '__main__':
##    zip_file_path = "D:\\RL25\\TACT_UT\\file_lib\\log\\2012-6-11_20_28_8.zip"
##
##    file_name="BTSLogFiles.zip"
##    print zip_file_search(zip_file_path, file_name)
##
##    condition="BTSLogFiles.zip\\BbcConfiguration.txt"
##    print zip_zip_file_search(zip_file_path, condition)
    pass
