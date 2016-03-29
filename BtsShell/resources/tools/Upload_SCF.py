from BtsShell.application_lib.sftp import sftp_download,sftp_upload
from BtsShell.file_lib.common_operation import Change_xml_file
from BtsShell.file_lib.BTS_file_control import check_scf_version
import os, time, glob, sys


def get_time_stamp():
    return time.strftime("%y%m%d%H%M%S")

def _convert_list(src_list):
    items = []
    temp = ''
    for item in src_list:
        flag = True
        if item.find("u\'") > 0:
            temp = item
            flag = False
        else:
            temp += " " + item
        if flag:
            items.append(temp)
    items = [item.strip() for item in items[-1].split(",")]
    items[0] = items[0].lstrip('[')
    items[-1] = items[-1].rstrip(']')
    for item in items:
        index = items.index(item)
        if item.endswith("\'"):
            items[index] = item.rstrip("\'")
    for item in items:
        index = items.index(item)
        if item.startswith("u\'"):
            items[index] = item.lstrip("u\'")
    return items

    
def main(timestamp, scf_file_name, src_file, parameter_list):
    
    print "*INFO*", 'Input:', parameter_list
    para_list = _convert_list(parameter_list)  
    print "*INFO*", 'Processed:', para_list

    tmp_scf_path = "C:\\%s_SCF.xml" % timestamp
    tmp_fidtdir_path = "C:\\%s_FileDirectory.xml" % timestamp
    
    if os.path.exists(tmp_fidtdir_path):
        print "*INFO* FileDirectory exsit: %s" % tmp_fidtdir_path
        scf_name = check_scf_version(tmp_fidtdir_path, scf_file_name)
        print "*INFO* Get SCF_NAME success: %s" % scf_name
    else:
        print "*WARN* %s does not exist! Give SCF_NAME a default value: %s_1" % tmp_fidtdir_path, scf_file_name
        scf_name = "%s_1" %scf_file_name
        
    Change_xml_file(src_file, tmp_scf_path, para_list)
    if os.path.exists(tmp_scf_path):
        print "*INFO* SCF modify successed: %s" % tmp_scf_path
    else:
        print "*ERROR* SCF modify failed."
        raise Exception, "Modify SCF failed, not generated a new scf file!"
    
    #del temp filedirectory and scf file.
##    try:
##        os.remove(tmp_fidtdir_path)
##        os.remove(tmp_scf_path)
##    finally:
##        pass
    print "*INFO* The effective SCF name is: %s" % scf_name
    print "*INFO* Upload SCF file successed !"
    
main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])

