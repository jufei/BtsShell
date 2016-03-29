import os
from BtsShell import connections
from BtsShell.common_lib.get_path import *

def calibration_check(path_of_log, bandwidth = "20"):
    """This keyword is used for analyzing UDPlog calibration information
    | Input Parameters | Man. |  Description |
    | path_of_log      | Yes  |  Path of log |
    | bandwidth        | Yes  |  10 or 20    |

    Example
    | Calibration Check | "C:\\SYSLOG_270.LOG" | "20" |
    """

    toolPath = os.path.join(get_tools_path(), "Calibration.exe")
    command  = toolPath + " " + '"' + path_of_log + '"' + " " + bandwidth
    connections.execute_shell_command(command)
    ret = os.system(command)
    if 1 == ret:
        raise Exception, "Calibration check fail!"

if __name__ == '__main__':
    print calibration_check("C:\\SYSLOG_270.LOG", "20")
    pass
