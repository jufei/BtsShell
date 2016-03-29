import re
from process import *
from BtsShell import connections

def start_btslog(btslog_dir, log_type):
    """This keyword starts collecting BTS logs using BTSLog tool.
    
    | Input Parameters | Man. | Description |
    | btslog_dir       | Yes  | Application btslog.exe directory |
    | log_type         | Yes  | Log type for collecting, 'UDP' or 'TRACING' or 'BOTH' |
    
    Example
    | Start BTSLog | C:\\BTSLog\\btslog.exe | UDP |
    | Start BTSLog | C:\\BTSLog\\btslog.exe | TRACING |
    """
    
    log_type = log_type.upper()
    if "BTSlog2" in btslog_dir:
        if log_type == 'UDP':
            argument = 'start_udplog'
        elif log_type == 'TRACING':
            argument = 'start_tracing'
        elif log_type == 'BOTH':
            argument = 'start_both'
        else:
            raise Exception, "log_type '%s' is not supported" % log_type
        start_program_with_psexec('\"%s\" -nogui -%s' % (btslog_dir, argument))

    else:
        if log_type == 'UDP':
            argument = 'start_udplog'
        elif log_type == 'TRACING':
            argument = 'start_bssigrec'
        elif log_type == 'BOTH':
            argument = 'start_both'
        else:
            raise Exception, "log_type '%s' is not supported" % log_type
        ret = connections.execute_shell_command_without_check('\"%s\" %s' % (btslog_dir, argument))
        if ret.find('is not recognized') > 0: # probably given path is not avaialbe
            raise Exception, 'start %s log failed' % log_type
    
def stop_btslog():
    """This keyword stops btslog.exe process.

    | Input Parameters | Man. | Description |

    Example
    | Stop BTSLog |
    """
    kill_process(['btslog.exe', 'BTSlog2.exe'])

