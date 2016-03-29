from BtsShell import connections
from BtsShell.common_lib.get_path import *
import time
# PB_PATH = os.path.join(get_tools_path(), "powerbreaker.exe")
PB_PATH = r'C:\Python27\lib\site-packages\BtsShell\resources\tools\powerbreaker.exe'


def tm500_power_on(addr):
    """This keyword power on TM500.

    | Input Parameters | Man. | Description |
    | port             | Yes  | com port |

    Example
    | Tm500 Power On | COM1 |

    """
    if addr == "":
        raise "Powerbreak port info is null, please check the configuration"
        return
    cmd = "%s -o power_on -p %s" %(PB_PATH, addr)
    ret= connections.execute_shell_command_without_check(cmd)
    errcode = connections.execute_shell_command_without_check('echo %ERRORLEVEL%')
    errcode = int(errcode.split('%')[-1].split()[0])
    if errcode != 0:
        raise Exception, "tm500_power_on failed, \"%s\"" % addr
    else:
        print "*INFO* %s" % ret


def tm500_power_off(addr):
    """This keyword power off TM500.

    | Input Parameters | Man. | Description |
    | port             | Yes  | com port |

    Example
    | Tm500 Power Off | COM1 |
    """
    if addr == "":
        raise "Powerbreak port info is null, please check the configuration"
        return
    if addr.upper().strip().startswith("COM"):
        cmd = "%s -o dc_on -p %s" %(PB_PATH, addr)
    else:
        cmd = "%s -o power_off -p %s" %(PB_PATH, addr)
    ret= connections.execute_shell_command_without_check(cmd)
    errcode = connections.execute_shell_command_without_check('echo %ERRORLEVEL%')
    errcode = int(errcode.split('%')[-1].split()[0])
    if errcode != 0:
        raise Exception, "tm500_power_off failed, \"%s\"" % addr
    else:
        print "*INFO* %s" % ret

def _power_on_once(addr, ue_type='TM500'):

    if not addr.upper().strip().startswith('COM'):
        cmd = "%s -o power_on -p %s" %(PB_PATH, addr)
    else:
        if ue_type.upper() == 'TM500':
            cmd = "%s -o power_on -p %s" %(PB_PATH, addr)
        elif ue_type.upper() == 'CPE':
            cmd = "%s -o dc_on -p %s" %(PB_PATH, addr)

    ret= connections.execute_shell_command_without_check(cmd)
    errcode = connections.execute_shell_command_without_check('echo %ERRORLEVEL%')
    errcode = int(errcode.split('%')[-1].split()[0])
    if errcode != 0:
        raise Exception, "power_on failed, \"%s\"" % addr
    else:
        print "*INFO* %s" % ret

def _power_off_once(addr, ue_type='TM500'):

    if not addr.upper().strip().startswith('COM'):
        cmd = "%s -o power_off -p %s" %(PB_PATH, addr)
    else:
        if ue_type.upper() == 'TM500':
            cmd = "%s -o ac_on -p %s" %(PB_PATH, addr)
        elif ue_type.upper() == 'CPE':
            cmd = "%s -o power_off -p %s" %(PB_PATH, addr)
    ret= connections.execute_shell_command_without_check(cmd)
    errcode = connections.execute_shell_command_without_check('echo %ERRORLEVEL%')
    errcode = int(errcode.split('%')[-1].split()[0])
    if errcode != 0:
        raise Exception, "power_off failed, \"%s\"" % addr
    else:
        print "*INFO* %s" % ret

def power_on(addr, ue_type='TM500'):
    """This keyword power on BTS , and it can support Facom and HuaXiang PB.
    For HuaXiang PB, it can support "TM500" and "CPE" two kind of connect type.
    For Facom PB, it can operate multiple ports.

    | Input Parameters | Man. | Description |
    | vendor_info      | Yes  | PB COM port or IP  |

    Example
    | Power Off | COM1 |
    | Power Off | ${POWER_BREAK_IP}:${POWER_BREAK_OUTPUT}:${BTS_CONTROL_PC_LAB} |
    | Power Off | ["192.168.127.254:1:192.168.127.200", "192.168.127.254:2:192.168.127.200"] |
    """
    if addr == "":
        raise "Powerbreak port info is null, please check the configuration"
        return
    if isinstance(addr, list):
    #if type(addr) is types.ListType:
        for item in addr:
        #for i in range(len(addr)):
            _power_on_once(item)
            time.sleep(5)
    else:
        _power_on_once(addr, ue_type)

def power_off(addr, ue_type='TM500'):
    """This keyword power off BTS , and it can support Facom and HuaXiang PB.
    For HuaXiang PB, it can support "TM500" and "CPE" two kind of connect type.
    For Facom PB, it can operate multiple ports.

    | Input Parameters | Man. | Description |
    | vendor_info      | Yes  | PB COM port or IP  |

    Example
    | Power Off | COM1 |
    | Power Off | ${POWER_BREAK_IP}:${POWER_BREAK_OUTPUT}:${BTS_CONTROL_PC_LAB} |
    | Power Off | ["192.168.127.254:1:192.168.127.200", "192.168.127.254:2:192.168.127.200"] |
    """
    if addr == "":
        raise "Powerbreak port info is null, please check the configuration"
        return
    if isinstance(addr, list):
    #if type(addr) is types.ListType:
        for item in addr:
        #for i in range(len(addr)):
            _power_off_once(item)
            time.sleep(5)
    else:
        _power_off_once(addr, ue_type)




if __name__ == "__main__":
    #power_on()
    connections.connect_to_host('10.68.152.34',23,'tdlte-tester','btstest')
    power_on("COM1")
    #power_off()
    pass
