import os
import re
import time
from BtsShell import connections
from BtsShell.common_lib.get_path import *
psexecPath = os.path.join(get_tools_path(), "psexec.exe")

def start_program_without_psexec(program_Path):
    """This keyword opens application without GUI.

    | Input Parameters | Man. | Description |
    | program_Path     | Yes  | "C:\\Program Files\\BTSlog\\BTSlog.exe" |

    Example
    | start_program_without_psexec | "C:\\Program Files\\BTSlog\\BTSlog.exe" |
    """

##    if True == os.path.isfile(program_Path):
    return connections.execute_shell_command_without_check(program_Path)
##    else:
##        print program_Path + ' is not exist!'
##        raise Exception


def start_program_with_psexec(program_Path):
    """This keyword opens application with GUI.

    | Input Parameters | Man. | Description |
    | psexe_Path       | Yes  | "C:\\psexec.exe" |
    | program_Path     | Yes  | "C:\\Program Files\\BTSlog\\BTSlog.exe" |

    Example
    | Start Program With Psexec | C:\\psexec.exe | C:\\Program Files\\BTSlog\\BTSlog.exe |
    """
    """
    if False == os.path.isfile(psexe_Path):
        print psexe_Path + ' is not exist!'
        raise Exception

    if False == os.path.isfile(program_Path):
        print program_Path + ' is not exist!'
        raise Exception
    """

    cmd1 = 'psexec.exe -i -d ' + program_Path
    cmd2 = psexecPath + ' -i -d ' + program_Path

    ret = connections.execute_shell_command_without_check(cmd1)
    if ret.find('process ID') < 0:
        ret = connections.execute_shell_command_without_check(cmd2)
        if ret.find('process ID') < 0:
            raise Exception, "application '%s' start failed" % program_Path

def kill_process(processes):
    """This keyword kill Process.

    | Input Parameters | Man. | Description |
    |     processes    | Yes  | Process name/id, or List |

    Example
    | ${process_list}= | Create List | 1003 | 5043 |
    | kill Process | ${process_list} |
    | kill Process | BTSlog.exe |
    """

    if isinstance(processes, list) or isinstance(processes, set):
        for process in processes:
            cmd = "TASKKILL /F /IM " + process
            ret = connections.execute_shell_command_without_check(cmd)
    else:
        cmd = "TASKKILL /F /IM " + processes
        ret = connections.execute_shell_command_without_check(cmd)
    return ret

def kill_process_by_sockets(ip, port):
    """This keyword is used to kill processes by specfied sockets

    | Input Parameters | Man. | Description |
    |     ip           | Yes  | This socket's ip |
    |     port         | Yes  | This socket's port |

    Example
    | kill_process_by_sockets | 192.168.255.1 | 15003 |
    """
    socket_kill = str(ip).strip() + ":" + str(port).strip()
    ret = connections.execute_shell_command_without_check("netstat -ano")
    for ln in ret.splitlines():
        if socket_kill in ln:
            pid = ln.split()[-1]
            if pid != "0":
                connections.execute_shell_command("TASKKILL /F /T /PID %s" % pid)
                break

def _get_and_kill_sitemanager_process():
    """This keyword get and kill sitemanager Process without telnet connection.
        no use now coulde be resolved by change jekins name.

    Example
    | get_and_kill_sitemanager_process |

    """
    cmd = os.path.join(get_tools_path(), "handle.exe")
    all_java_process = connections.execute_shell_command_without_check(cmd+" \"Site Manager\"")
    pattern = re.compile("pid: (\\d+)")
    java_ps_list = all_java_process.split("\n")

    sm_ps_list = []
    for java_ps in java_ps_list:
        tmp = re.search(pattern, java_ps)
        if tmp:
            sm_ps_list.append(tmp.groups()[0])
    sm =  set(sm_ps_list)

    kill_process(sm)

def _tma_port_match(tma_port_list):
    ret = connections.execute_shell_command("netstat -ano|grep 0.0.0.0")
    lines = ret.splitlines()
    pids = []
    for tma_port in tma_port_list:
        for line in lines:
            tmp = re.match('^.*%s.*LISTENING\s+(\d+)'%tma_port, line)
            if tmp:
                print line
                pids.append(tmp.groups()[0])
    return pids

def _wait_until_port_exist(tma_ports):
    start_time = time.clock()
    duration = 0
    check_flag = False
    #check_port = "0.0.0.0:5003"
    check_command = "netstat -ano|grep 0.0.0.0"
    ret = connections.execute_shell_command(check_command)
    for tma_port in tma_ports:
        if tma_port in ret:
            check_flag = True
    while (False == check_flag) and (duration < 60):
        time.sleep(10)
        ret = connections.execute_shell_command( check_command)
        duration = time.clock() - start_time
        for tma_port in tma_ports:
            if tma_port in ret:
                check_flag = True
    if check_flag == False:
        raise Exception, "5003 port open failed in 60 second"


def restart_tma(tma_version, connection):
    """This keyword get and kill sitemanager Process without telnet connection.
        no use now coulde be resolved by change jekins name.

    Example
    | get_and_kill_sitemanager_process |

    """
    connections.switch_host_connection(connection)
    kill_process("TmaApplication.exe")

    tma_ports = []#'0.0.0.0:5003', '0.0.0.0:5004', '0.0.0.0:5005']

    for port in range(5003, 5099):
        tma_ports.append('0.0.0.0:%s' % port)

    pids = _tma_port_match(tma_ports)
    for pid in pids:
        print pid
        connections.execute_shell_command("ntsd -c q -p %s"%pid)

    pids = _tma_port_match(tma_ports)
    if 0 < len(pids):
        print "TMA port pid as %s kill failed" %pids
    client = os.path.join(get_tools_path(), "Server_Client", "client.exe")
    tma_version = re.sub('TMA.exe', 'TMAApplication.exe', tma_version)
    cmd  = '"%s" localhost "%s" /u \\"Default User\\" /c y /p 5003 /a n\r\n' %(client, tma_version)
    connections.execute_shell_command_bare(cmd)
    time.sleep(3)
    connections.execute_shell_command_without_check('\x03')  # ctrl+c
    _wait_until_port_exist(tma_ports)

if __name__ == '__main__':
    restart_tma("a","b")
    pass

