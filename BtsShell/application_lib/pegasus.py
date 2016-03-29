import os
import re
from BtsShell import connections
#from BtsShell import file_lib

def run_pegasus_script(pegasus_dir, workspace_dir, project_name, test_dir, timeout = '900'):
    """This keyword runs Pegasus script in command line interface.

    | Input Parameters | Man. | Description |
    | pegasus_dir      | Yes  | Identifies to pegasus directory |
    | workspace_dir    | Yes  | Identifies to workspace directory |
    | project_name     | Yes  | Identifies to project name |
    | test_dir         | Yes  | Identifies to test xml file |
    | timeout          | No   | Timeout for Pegasus script execution, default is 900 sec |

    Example
    | Run Pegasus Script | C:\\Pegasus\\PegasusRCPc.exe | C:\\Pegasus\\workspaceTDD | LTE_Inc21 | Tests/LNT/HW_Configuration_FSP.xml |
    """
    old_timeout = connections.set_shell_timeout(timeout)   
    command = '%s -application pegasus.headless -noSplash --launcher.suppressErrors -data %s --project %s --testHierarchy %s --refresh' \
              %(pegasus_dir, workspace_dir, project_name, test_dir)
    try:
        ret = connections.execute_shell_command_without_check(command)
        #pegasus_log_file = file_lib.get_last_modified_file(os.path.join(workspace_dir, 'log'), 'txt', 'root_logger')
        #file_lib.file_should_contain(pegasus_log_file, '', '', 'Pegasus_log') # does not check Pegasus log file but only publish it in log.html
        errcode = connections.execute_shell_command_without_check('echo %ERRORLEVEL%')
        errcode = int(errcode.split('%')[-1].split()[0])
        if re.search('JVM TERMINATED', ret.upper(), re.MULTILINE) or errcode != 0:
            raise Exception, 'command (%s) execution failed' % command
    finally:
        connections.set_shell_timeout(old_timeout)

