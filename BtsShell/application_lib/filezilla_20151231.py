import os
import re
import time
from optparse import OptionParser
from BtsShell import connections
from BtsShell.file_lib.xml_control import ParseXML


file_zilla_exe_path = "C:\\Program Files\\FileZilla Server\\FileZilla server.exe"
file_zilla_xml_path = "C:\\Program Files\\FileZilla Server\\FileZilla server.xml"
def filezilla_server_restart(connection='local', path=file_zilla_exe_path):
    """This keyword restart filezilla server.
    | Input Parameters | Man. | Description |
    | connection  | Yes  | ${TM500_CONTROL_PC} |

    Example
    | filezilla_restart | ${TM500_CONTROL_PC} |
    | filezilla_restart |  |
    """

    if 'local' == connection:
        if not os.path.exists(path):
            raise Exception, "'%s' is not exist."%path
        if 0 != os.system('\"%s\" /stop' % path):
            raise Exception, "FileZilla Server stop failed"
        time.sleep(5)
        if 0 != os.system('\"%s\" /start' % path):
            raise Exception, "FileZilla Server start failed"
        print "FileZillar restart OK!"
    else:
        connections.switch_host_connection(connection)
        ret = connections.execute_shell_command_without_check('\"%s\" /stop' % path)
        time.sleep(5)
        ret = connections.execute_shell_command_without_check('\"%s\" /start' % path)

def filezilla_server_check_user(targe_folder_path, src_file=file_zilla_xml_path):
    """This keyword check 'TA_LOG' user exist in 'FileZilla Server.xml', if not add one.
    | Input Parameters  | Man.  | Description |
    | targe_folder_path | Yes   | add folder path |
    | tar_file          | Yes   | modified 'FileZilla Server new.xml' full path  |
    | src_file          | Yes   | 'FileZilla Server.xml' full path  |

    Example
    | ${restart_fz_flag} | filezilla_server_check_user | "C:\\TM500_log\\" | 'C:\\FileZilla Server.xml' |
    """
    ftp_dir = os.path.splitdrive(targe_folder_path)[0].upper()
    add_user = """<User Name="TA_LOG">
    <Option Name="Pass"></Option>
    <Option Name="Group"></Option>
    <Option Name="Bypass server userlimit">0</Option>
    <Option Name="User Limit">0</Option>
    <Option Name="IP Limit">0</Option>
    <Option Name="Enabled">1</Option>
    <Option Name="Comments"></Option>
    <Option Name="ForceSsl">0</Option>
    <IpFilter>
        <Disallowed />
        <Allowed />
    </IpFilter>
    <Permissions>
        <Permission Dir="%s">
            <Option Name="FileRead">1</Option>
            <Option Name="FileWrite">1</Option>
            <Option Name="FileDelete">1</Option>
            <Option Name="FileAppend">1</Option>
            <Option Name="DirCreate">1</Option>
            <Option Name="DirDelete">1</Option>
            <Option Name="DirList">1</Option>
            <Option Name="DirSubdirs">1</Option>
            <Option Name="IsHome">1</Option>
            <Option Name="AutoCreate">0</Option>
        </Permission>
    </Permissions>
    <SpeedLimits DlType="0" DlLimit="10" ServerDlLimitBypass="0" UlType="0" UlLimit="10" ServerUlLimitBypass="0">
        <Download />
        <Upload />
    </SpeedLimits>
</User>\n""" % ftp_dir

    user_flag = 0
    permission_flag = 0

    xml = ParseXML(src_file)
    users = xml.get_element("User")
    for user in users:
        if "TA_LOG" == xml.get_ele_attr(user, "Name"):
            print "'filezilla serve.xml' find user name as 'TA_LOG'"
            user_flag = 1
            permissions = xml.get_element("Permission")
            for permission in permissions:
                if ftp_dir == xml.get_ele_attr(permission, "Dir").upper():
                    print "'filezilla serve.xml' find permission dir as '%s'."%ftp_dir
                    permission_flag = 1
                    return False
            if 1==user_flag and 0==permission_flag:
                print "'filezilla serve.xml' modify permission dir as '%s'."%ftp_dir
                xml.set_ele_attr(permissions[0], "Dir", ftp_dir)
                xml.write_xml_file(src_file)
                print "filezilla serve need to restart"
                return True

    if 0 == user_flag and 0 == permission_flag:
        add = xml.string_to_element(add_user)
        xml.insert_ele(users, add)
        xml.write_xml_file(src_file)
##        users_flag = 0
##        try:
##            file_handle = file(src_file, 'r+')
##        except:
##            raise Exception, "'%s' open failed" % src_file
##        try:
##            lines = file_handle.readlines()
##            lin_num = 0
##            for line in lines:
##                lin_num += 1
##                if "<Users>" in line:
##                    users_flag = 1
##                    break
##        finally:
##            file_handle.close()
##
##        lines.insert(lin_num, add_user)
##        try:
##            tar_file_handle = file(src_file, 'w')
##        except:
##            raise Exception, "'%s' open failed" % tar_file
##        try:
##            lines = tar_file_handle.writelines(lines)
##        finally:
##            tar_file_handle.close()

        print "'filezilla serve.xml' add user name as 'TA_LOG' and dir as '%s' ok"%ftp_dir
        print "filezilla serve need to restart"
        return True

def filezilla_server_check_tma_version(TM500_APP_DIR, src_file):
    """This keyword change TMA version by modify 'FileZilla Server.xml'.
    | Input Parameters  | Man.  | Description |
    | TM500_APP_DIR     | Yes   | target TMA version |
    | tar_file          | Yes   | modified 'FileZilla Server new.xml' full path  |
    | src_file          | Yes   | 'FileZilla Server.xml' full path  |

    Example
    | ${restart_fz_flag} | filezilla_server_check_tma_version | "C:\\Program Files\\Aeroflex\\TM500\\LTE - K3.2.6.REV50\\ppc_pq\\public\\ftp_root" | 'C:\\FileZilla Server.xml' |
    """

    tmp = re.search("^.*(LTE.*REV\d{2,3}).*", TM500_APP_DIR)
    target_version = tmp.group(1)
    xml = ParseXML(src_file)
    aero_permissions = xml.find_ele_by_part_attr("Permission", "Dir", 'Aeroflex')
    modified = False
    for permission in aero_permissions:
        dire = xml.get_ele_attr(permission, "Dir")
        option, is_home_value = xml.get_ele_text_by_attr(permission, "Name", "IsHome")
        newvalue = '1' if target_version in dire else '0'
        if newvalue != is_home_value:
            xml.modify_ele_text(option, newvalue)
            modified = True
    xml.write_xml_file(src_file)
    return modified


if __name__ == '__main__':
    description = "FileZillar.py for TDLTE I&V testing.       \
                   Author: Chen Jin(61368521)                 \
                   Email: jin_emily.chen@nsn.com              \
                   Data: 2012-5-24                            \
                   Version: 1.0.0"
    parser = OptionParser(description = description)

    parser.add_option("-t", "--target_folder",
                              action = "store",
                              dest = "target_folder",
                              type = "string",
                              default = "C:\\",
                              help = "user dir.")
    parser.add_option("-m", "--tma_dir",
                              action = "store",
                              dest = "tma_dir",
                              type = "string",
                              default = "D:\\",
                              help = "TMA version full path.")
    parser.add_option("-x", "--xml_dir",
                              action = "store",
                              dest = "xml_dir",
                              type = "string",
                              default = "\"C:\\Program Files\\FileZilla Server\\FileZilla server.xml\"",
                              help = "FileZillar xml dir.")
    parser.add_option("-e", "--exe_dir",
                              action = "store",
                              dest = "exe_dir",
                              type = "string",
                              default = "\"C:\\Program Files\\FileZilla Server\\FileZilla server.exe\"",
                              help = "FileZillar exe dir.")
    parser.add_option("-c", "--connection",
                              action = "store",
                              dest = "connection",
                              type = "string",
                              default = "local",
                              help = "FileZilla restart at local or under connection.")
    (options, args) = parser.parse_args()
    target_folder = options.target_folder
    tma_dir = "C:\\Program Files\\Aeroflex\\TM500\\LTE - K4.3.2.REV02\\ppc_pq\\public\\ftp_root"#options.tma_dir
    xml_dir = "D:\\chenjinEmily\\xml\\FileZilla Server2.xml"#options.xml_dir
    tar_dir = "D:\\chenjinEmily\\xml\\FileZilla Server3.xml"
    exe_dir = options.exe_dir
    connection = options.connection

    fz_restart1 = filezilla_server_check_user(target_folder, tar_dir, xml_dir)
    fz_restart2 = filezilla_server_check_tma_version(tma_dir, tar_dir, xml_dir)

    if fz_restart1 or fz_restart2:
        print "need to restart"
        pass#filezilla_server_restart(connection, exe_dir)

