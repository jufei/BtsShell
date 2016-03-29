import time, re
from BtsShell.high_shell_lib.run import _run_keyword as kw
from robot.libraries.BuiltIn import BuiltIn
from BtsShell.common_lib.get_path import *
from BtsShell import connections

def start_robot_remote_library(library=None, host=None, port=None, allow_stop=None):
    tools_path = get_tools_path_with_command()
    remoteserver = os.path.join(tools_path, "robotremoteserver.py")
    psexecPath = os.path.join(tools_path, "psexec.exe")

    cmd = 'python "%s" ' % remoteserver

    if library:cmd += " -l " + library
    if host:cmd += " -i " + host
    if port:cmd += " -p " + port
    if allow_stop:cmd += " -s " + allow_stop


    cmd = '"%s" -i -d ' % psexecPath + cmd
    ret = connections.execute_shell_command_without_check(cmd)
    if "with process ID" in ret:
        return
        return re.match("with process ID (\d+)\.", ret, re.I|re.M).groups()[0]


def _kill_if_port_exist(port):
    #check 5003 port in use or not, if yes kill 5003 port
    ret = kw("execute_shell_command_without_check", "netstat -ano|grep %s"%port)
    tmp = ret.split('\n')
    full_port = "0.0.0.0:%s"%port
    for i in range(len(tmp)):
        if full_port in tmp[i]:
            port = tmp[i].split()[-1]
            kw("execute_shell_command", "ntsd -c q -p %s"%port)

def _tm500_status_check(tm500_pc_conn, tma_version):
    #"\"C:\\Program Files\\Aeroflex\\TM500\\LTE - K3.2.6.REV50\\Test Mobile Application\\TMA.exe\""
    tmp = re.search('.*\s(\w+\d.\d.\d.\w+\d+).*', tma_version)
    if tmp:
        simple_version = tmp.groups()[0]
    else:
        raise Exception("Get simple version failed from %s" % tma_version)
    # simple_version = [x for x in tma_version.split('\\') if 'LTE - ' in x][0]
    kw("switch_host_connection", tm500_pc_conn)
    kw("kill_process", "tm500_serial_check.exe")
    # status_check_path = os.path.join(get_tools_path(), "tm500_serial_check.exe")
    status_check_path = r'C:\Python27\lib\site-packages\BtsShell\resources\tools\tm500\tm500_serial_operation.exe'
    try:
        old_timeout = kw("set_shell_timeout", 300)
        ret = kw("execute_shell_command_without_check",
                "%s -v \"%s\" -p only_check" % (status_check_path,simple_version))
        if "tm500 reboot failed" in ret.lower():
            raise Exception, "TM500 reboot failed!"
    finally:
        kw("set_shell_timeout", old_timeout)

def _wait_until_port_exist(tm500_pc_conn):
    kw("switch_host_connection", tm500_pc_conn)
    start_time = time.clock()
    duration = 0
    #check_port = "0.0.0.0:5003"
    check_command = "netstat -ano|grep 0.0.0.0"
    ret = kw("execute_shell_command_without_check", check_command)
    while (not re.search("0.0.0.0:50\d\d", ret)) and (duration < 60):
        time.sleep(10)
        ret = kw("execute_shell_command_without_check", check_command)
        duration = time.clock() - start_time
    if not re.search("0.0.0.0:50\d\d", ret):
        raise Exception, "50xx port open failed in 60 second"

def tm500_hardware_restart(tma_version, bts_pc_conn, tm500_pc_conn):
    """recommend keyword used for hardware restart TM500 and start TMA wait until 5003 port open ok.
    | Input Parameters          | Man. | Description |
    | tma_version   |  Yes | the dir of script  |
    | bts_pc_conn   |  Yes | object of bts control pc connection  |
    | tm500_pc_conn |  Yes | object of tm500 control pc connection  |

    Example
    | tm500_hardware_restart | ${TM500_APPLICATION_S_VERSION_DIR} | ${BTS_CONTROL_PC_CONNECTION} | ${TM500_CONTROL_PC_CONNECTION} |
    """
    kw("switch_host_connection",tm500_pc_conn)
    pro_list = ['hypertrm.exe', 'TmaApplication.exe', 'PUTTY.exe']
    kw("kill_process", pro_list)
    _kill_if_port_exist("5003")

    TM500_PB_PORT = _GetRuntimeVar("TM500_POWERBREAK_PORT")
    #restart tm500 by powerbreak
    kw("switch_host_connection", bts_pc_conn)
    kw("tm500_power_off", TM500_PB_PORT)
    time.sleep(10)
    kw("tm500_power_on", TM500_PB_PORT)

    #check tm500 restart status
    try:
        _tm500_status_check(tm500_pc_conn, tma_version)
    finally:
        pass
    #time.sleep(180)

    #start TMA UI and wait until port open ok
    kw("switch_host_connection", tm500_pc_conn)
    #Jufei
    # client = os.path.join(get_tools_path(), "Server_Client", "client.exe")
    client = r'C:\Python27\lib\site-packages\BtsShell\resources\tools\Server_Client\client.exe'
    tma_version = re.sub('TMA.exe', 'TMAApplication.exe', tma_version)
    if tma_version.startswith('\"'):
        cmd  = '"%s" localhost %s /u \\"Default User\\" /c y /p 5003 /a n\r\n' %(client, tma_version)
    else:
        cmd  = '"%s" localhost "%s" /u \\"Default User\\" /c y /p 5003 /a n\r\n' %(client, tma_version)
    cmd  = '"C:\Python27\lib\site-packages\BtsShell\resources\tools\Server_Client\client.exe" localhost "C:\Program Files\Aeroflex\TM500\LTE - LMC2.3.0.REV51\" /u \"Default User\" /c y /p 5003 /a n'
    kw("execute_shell_command_bare", cmd)
    time.sleep(5)
    kw("execute_shell_command_without_check", '\x03')  # ctrl+c
    _wait_until_port_exist(tm500_pc_conn)

def _GetRuntimeVar(varname):
    try:
        if not varname.startswith("${"):
            varname = "${%s}" % varname
        return BuiltIn().replace_variables(varname)
    except:
        print "Not run with robot..."
        return

def get_active_sw_version(downloaddir='/flash', username='toor4nsn', passwd='oZPS0POrRieRtu'):
    """This keyword get software version of BTS

    | Input Parameters  | Man. | Description |
    |    downloaddir    |  No  | Default value is /flash  |
    |    username       |  No  | Default value is 'toor4nsn' for BTS  |
    |     passwd        |  No  | Default value is 'oZPS0POrRieRtu' for BTS  |

    Example
    |  get_active_sw_version  |
    """
    fcmd_usr = _GetRuntimeVar("FCMD_USERNAME")
    fcmd_psw = _GetRuntimeVar("FCMD_PASSWORD")
    fcmd_pmt = _GetRuntimeVar("FCMD_PROMPT")
    fcmd_ip = _GetRuntimeVar("BTS_FCM")
    fcmd_port = _GetRuntimeVar("SSH_PORT")

    connections.connect_to_ssh_host(fcmd_ip, int(fcmd_port), fcmd_usr, fcmd_psw, fcmd_pmt)
    ret = connections.execute_ssh_command_without_check("ls %s" % downloaddir)
    connections.disconnect_from_ssh()

    tmp = re.search("TargetBD_(.*).xml", ret, re.M)
    if tmp:
        build_version = tmp.groups()[0]
        print "get build version is %s" % build_version
        return build_version

if __name__ == '__main__':
    TM500_hardware_restart_xxxx(1,2,3)
    pass
