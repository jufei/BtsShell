from BtsShell import connections
from BtsShell.common_lib.get_path import *
import re

PSCLIPATH = os.path.join(get_tools_path(), "pscli")


def set_mac_rd_parameter(core, value):
    """This keyword used to set MAC R&D parameter use pscli.exe

    | Input Paramaters      | Man. | Description |
    | core                  | yes  | Target core in BTS |
    | value                 | yes  | parameter value |
    Example
    | switch host connection    | ${connections} |
    | set_rd_parameter_by_pscli | 1231      | ERadSwDomainLteMac_TRdPdcchOllaUsed=0x1234 |
    | set_rd_parameter_by_pscli | 1231,1234 | ERadSwDomainLteMac_TRdPdcchOllaUsed=0x1234 |
    """
    connections.execute_shell_command("cd %s" %PSCLIPATH)
    
    cmd = 'pscli.exe --setrd -T %s %s' %(core, value)
    ret = connections.execute_shell_command(cmd)
    if 'Set Rad Parameters succeed' in ret:
        print "Set R&D parameters succeed!"
        return True
    else:
        raise Exception, "Set MAC R&D parameters failed!"
    
    
def get_mac_rd_parameter(core, value):
    """This keyword used to get MAC R&D parameter use pscli.exe

    | Input Paramaters      | Man. | Description |
    | core                  | yes  | Target core in BTS |
    | value                 | yes  | parameter value |
    Example
    | switch host connection    | ${connections} |
    | get_rad_parameter | 1231      | ERadSwDomainLteMac_TRdPdcchOllaUsed |
    | get_rad_parameter | 1231,1234 | ERadSwDomainLteMac_TRdPdcchOllaUsed |
    """
    connections.execute_shell_command("cd %s" %PSCLIPATH)
    
    cmd = 'pscli.exe --queryrd -T %s %s' %(core, value)
    
    cores = core.split(',')
    try:
        cores.remove('')
    except:
        pass
    result = []
    
    ret = connections.execute_shell_command(cmd)
    lns = ret.splitlines()
    for ln in lns:
        for c in cores:
            res = re.match("^%s:.*\((.*)\)$" %c, ln)
            if res:
                result.append(res.groups()[0])
                cores.remove(c)
    return result[0] if len(result)==1 else result

def set_mac_log_level(core, value):
    """This keyword used to set MAC R&D parameter use pscli.exe

    | Input Paramaters      | Man. | Description |
    | core                  | yes  | Target core in BTS |
    | value                 | yes  | parameter value |
    Example
    | switch host connection    | ${connections} |
    | set_rd_parameter_by_pscli | 1231      | ERadSwDomainLteMac_TRdPdcchOllaUsed=0x1234 |
    | set_rd_parameter_by_pscli | 1231,1234 | ERadSwDomainLteMac_TRdPdcchOllaUsed=0x1234 |
    """
    #pscli.exe --setlog -T 1231,1234 FID_PDSCH_LA=WARNING
    connections.execute_shell_command("cd %s" %PSCLIPATH)
    
    cmd = 'pscli.exe --setlog -T %s %s' %(core, value)
    ret = connections.execute_shell_command(cmd)
    if 'succeed' in ret:
        print "Set MAC LOG LEVEL succeed!"
        return True
    else:
        raise Exception, "Set MAC LOG LEVEL failed!"

if __name__ == '__main__':
    connections.connect_to_host('10.69.71.113', 23, 'tdlte-tester', 'btstest')
    a = get_mac_rd_parameter('1231,1234', 'ERadSwDomainLteMac_TRdPdcchOllaUsed')
    print '++++a is:', a
    print set_mac_rd_parameter('1231', 'ERadSwDomainLteMac_TRdPdcchOllaUsed=%s' %a[0])
    a = get_mac_rd_parameter('1231,1234', 'ERadSwDomainLteMac_TRdPdcchOllaUsed')   
     