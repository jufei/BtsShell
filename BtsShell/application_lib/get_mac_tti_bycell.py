"""ttitrace control, include get mac ttitrace, download mac ttitrace tool,
decode mac ttitace functions.
 
@author: zhang yongchao
@contact: sam.c.zhang@nsn.com
"""

import os
import time

from BtsShell.common_lib.get_path import *
tool_path = os.path.join(get_tools_path(), "TTITrace")

_global_ttitrace_tool_path = os.path.join(get_tools_path(), "TTITrace")
"""
# TODO auto get dsp_id, auto_download ttitrace tools
# TODO: env prepare with script, update ttitrace tool.
# TODO: investgate ttitrace tool with SCM package, liwei will put this tool to specifical folder
execute command 'getCellMapping @RROMexe' get follow response:
[telnet_common.py@234] Get Response:  
lcr lnCel chBw noRx secId ULCoMP SwDeployment SPool UEC     CELLC   MACCELL MACULTTI MACDLTTI DL-PHY  UL-PHY 
1   4097  20M  2    -     -      TDD-2-DSP    -     0x120d  0x120d  0x1233  0x1234   0x1231   0x1244  0x1242 
1   4098  20M  2    -     -      TDD-2-DSP    -     0x120d  0x120d  0x1233  0x1233   0x1232   0x1244  0x1242
AaShell>
"""

def _get_mac_tti_address(cell="ALL"):
    macultti = 'MACULTTI'
    macdltti = 'MACDLTTI'
    cell_id = 'lnCel'
    cmd = 'getCellMapping @RROMexe'
    connections.connect_to_host('192.168.255.1', port=15007, timeout=10)
    response = connections.execute_shell_command(cmd)
    if macultti not in response:
        response = connections.execute_shell_command(cmd)
        if macultti not in response:
            raise Exception("execute command '%s' failed!" % cmd) 
    connections.disconnect_from_host()
    lines = response.splitlines()
    value_list = []

    
    useful_index = {}
    for line in  lines:
        tmp = line.split()
        if len(tmp) > 8:
            value_list.append(tmp)

    for value in  value_list:
        if macultti in value and \
             (macdltti in value) and \
                 (cell_id in value):
            useful_index[macultti] = value.index(macultti)            
            useful_index[macdltti] = value.index(macdltti)            
            useful_index[cell_id] = value.index(cell_id)    
            value_list.remove(value)         

    mac_address_dict = {}
    for value in value_list:
        cell_add = value[useful_index[cell_id]]
        mac_ul = value[useful_index[macultti]][2:]
        mac_dl = value[useful_index[macdltti]][2:]     
        mac_address_dict[cell_add] = [mac_dl,mac_ul]

    if cell == 'ALL':  
        all_address = []
        for add in mac_address_dict.keys():
            all_address += mac_address_dict[add]
        return all_address                
    else:
        return mac_address_dict[cell]  
 
def dump_mac_ttitrace(save_log_path, cell_id="ALL", dump_method='SICFTP'):
    """This keyword start sicftp, generate mac TTI Trace file
    | Input Parameters  | Man. |  Description                |
    | save_log_path     | Yes  |  save log path   |


    Example
    | get mac ttitrace | save_log_path | 'd:\\ttiTrace' |
    """


    mac_address = _get_mac_tti_address(cell_id)
    if not os.path.exists(save_log_path):
        os.mkdir(save_log_path)
    _dump_mac_ttitrace(','.join(mac_address), save_log_path, dump_method)

def _dump_mac_ttitrace(dsp_id, save_log_path, dump_method='SICFTP'):
    retry_times = 1
    for retry_time in xrange(retry_times):
        try:
            return _dump_mac_ttitrac_once(dsp_id, 
                                     save_log_path, 
                                     dump_method=dump_method)
        except Exception, err:
            print "Get TtiTrace '%s' fail for %s time, retry in 3 sec. Error:%s"\
                    % (dsp_id, retry_time + 1, repr(err))
            time.sleep(3)
    raise Exception("Get TtiTrace '%s' failed total %d times !" % (dsp_id, retry_times))

def _dump_mac_ttitrac_once(dsp_id_group, save_log_path, dump_method = 'SICFTP'):
    """This keyword start sicftp, generate mac TTI Trace file
    | Input Parameters  | Man. |  Description                |
    | dsp_id            | Yes  | dsp id in FCMD   |
    | save_log_path   | Yes  |  downloaded ttitrace log path  |
    | dump_method        | No   |  the ttitrace log fetch method, default is SICFTP |
   
    Example
    | _dump_mac_ttitrace | '1243' | 'd:\\ttiTraceUL_20111201203759.dat' |
    """
    sicftp_path = os.path.join(tool_path, "sicftp.exe")
    ##sicftp.exe -r -c 1231,1234,1431,1434
    if str(dump_method).strip().upper() == 'SICFTP':
        download_cmd = "%s -r -c %s -o \"%s\\\\\"" % (sicftp_path, 
                                                  dsp_id_group, 
                                                  save_log_path)
        print download_cmd        
        os.popen(download_cmd)
        
        
    else:
        raise Exception("TtiTrace tool %s doesn't recognize!" % dump_method)
    import glob
    dat_list = glob.glob(os.path.join(save_log_path, '*.dat'))
    # check if download success
    if len(dat_list) > 0:
        print "Download TtiTrace from %s success! -> %s" % (dsp_id_group, 
                                                               save_log_path)
    else:
        raise Exception("Download ttiTrace dat size = 0!")
    return save_log_path

def decode_mac_ttitrace(save_log_path):
    """This keyword run trace_parser and trace_converter, get .csv file
    | Input Parameters        | Man. | Description                                |
    | save_log_path           | Yes  | path of log file                 |

    Example
    | ttitrace decoder | D:\\DLttiTrace |
    
    Note:
    Make sure DevC_tti_trace_parser.exe exist in BtsShell\resources\tools\TTITrace
     
    """

    ttitrace_parser_tool = os.path.join(tool_path, "DevC_tti_trace_parser.exe")    

    if not os.path.exists(save_log_path):
        raise Exception("log folder is not exist in %s" % save_log_path)
    
    ascii_trace_log = os.path.join(save_log_path, "ascii_ttitrace.log")
    import glob
    dat_list = glob.glob(os.path.join(save_log_path, '*.dat'))
    for dat_file in dat_list:
        decode_cmd = "%s \"%s\" \"%s\" > %s" % (ttitrace_parser_tool,
                                         dat_file,
                                         dat_file.replace(".dat", ".csv"),
                                         ascii_trace_log)
        print "Execute command: '%s'" % decode_cmd
    
        os.system(decode_cmd)




    
if __name__ == '__main__':
    #dump_mac_ttitrace("d:\\")
    #print _get_mac_tti_address()
    dump_mac_ttitrace("d:\\mac")
    #decode_mac_ttitrace("C:\\Python27\\Lib\site-packages\\BtsShell\\resources\\tools\\TTITrace\\BinaryFileParser\\DevC_tti_trace_parser.exe", "d:\\mac")

    pass

