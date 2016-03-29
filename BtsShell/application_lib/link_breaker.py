import os
from BtsShell import connections
from BtsShell.common_lib.get_path import *
psexecPath = os.path.join(get_tools_path(), "psexec.exe")


def start_link_breaker_server(com_number):
    """This keyword starts the server command-line program in control PC connected with IUB Break

    | Input Parameters  | Man.  | Description |
    | com_number        | Yes   | specified com port in PC connected with IUB Break,
                                | com 7 usually in BTS control PC |
    Example
    | Start Link Breaker Server | 7 |

    Pay Attention:
    After test, please add "| kill_process | IUB.exe |" in the rear of  *.html script
    in order to stop "link break server"
    """

    command = "%s -i -d IUB.exe -s -cp %s -p 10000" % (psexecPath, com_number)
    os.system(command)

def start_link_breaker_client(server_ip, port_number, opening_time, closing_time,\
                              break_number, burst_number, option, setting=''):
    """This keyword starts the client command-line program in control PC

    | Input Parameters  | Man. |  Description |
    | server_ip         | Yes  |  server ip address, 127.0.0.1 is local ip           |
    | port_number       | Yes  |  specified port number, generally port 1            |
    | opening_time      | Yes  |  on time, 1-65535ms/second/minute/hour/day          |
    | closing_time      | Yes  |  Closing time                                       |
    | break_number      | Yes  |  break numbers                                      |
    | burst_number      | Yes  |  burst numbers                                      |
    | option            | Yes  |  fiber or network                                   |
    | setting           | No   |  start port according to setting when type is fiber |

    Example
    | Start Link Breaker Client | 127.0.0.1 | 1 | 1s | 2s | 1 | 1 | network |
    | start_link_breaker_client | 127.0.0.1 | 1 | 1s | 2s | 1 | 1 | fiber | start |
    | start_link_breaker_client | 127.0.0.1 | 1 | 1s | 2s | 1 | 1 | fiber | stop  |
    | start_link_breaker_client | 127.0.0.1 | 1 | 1s | 2s | 1 | 1 | fiber | NC    |
    | start_link_breaker_client | 127.0.0.1 | 1 | 1s | 2s | 1 | 1 | fiber | NO    |
    """
    if 'fiber' == option:
        connections.execute_shell_command_without_check("IUB.exe -c -ip %s -p 10000 -m SDH -n %s -d both -on %s -off %s -bkn %s -btn %s -%s"\
        %(server_ip, port_number, opening_time, closing_time, break_number, burst_number, setting))
    elif 'network' == option:
        connections.execute_shell_command_without_check("IUB.exe -c -ip %s -p 10000 -m eth -n %s -d both -on %s -off %s -bkn %s -btn %s -start"\
        %(server_ip, port_number, opening_time, closing_time, break_number, burst_number))

def stop_specified_port(server_ip, port_number):
    """This keyword stop the specified port

    | Input Parameters  | Man. | Description |
    | server_ip         | Yes  | server ip address, 127.0.0.1 is local ip |
    | port_number       | Yes  | specified port number, generally port 1  |

    Example
    | Stop Specified Port | 127.0.0.1 | 1 |
    """

    connections.execute_shell_command_without_check(\
    "IUB.exe -c -ip %s -p 10000 -m eth -n %s -stop" % (server_ip, port_number))


if __name__ == '__main__':

    pass
