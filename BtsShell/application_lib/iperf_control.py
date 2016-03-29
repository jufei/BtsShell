#################################################################################
#Author: Chen Jin Emily(61368521)
#Date: 2010-3-18
#Moudle use: Iperf serve/client start/stop control, and iperf log analyse
##################################################################################


from BtsShell import connections
#from BtsShell import file_lib
import os, time, re, sys
from BtsShell.file_lib.common_operation import file_read
from BtsShell.common_lib.get_path import *
iperfPath = os.path.join(get_tools_path(), "iperf.exe")
miperfPath = os.path.join(get_tools_path(), "miperf.exe")
psexecPath = os.path.join(get_tools_path(), "psexec.exe")
iperfMgrPath = os.path.join(get_tools_path(), "IperfMgr.exe")

def iperf_server_start_ssh(Port, LogFile, ProtocolType = 'UDP', packet_size='1024'):
    """This keyword will start Iperf Server in linux.
       In robot script, you should swith the ssh connect to the specific server first.

    | Input Parameters | Man. | Description |
    | Port             | Yes  | Specifical port |
    | LogFile          | Yes  | Iperf serve log file path and name |
    | ProtocolType     | No   | Protocal type, can be UDP, Dual UDP, FTP, and Dual TCP |
    | packet_size      | No   | The package size of UDP type |
    
    | return | pid |
    Example
    | ${client_pid} | Iperf Serve Start ssh | 50866 | /var/iperfDL.txt |
    """    
    if 'UDP' == ProtocolType or 'Dual UDP' == ProtocolType:
        cmd = 'iperf -s -u -P 0 -i 1 -p %s -w 41.0K -l %s.0B -f k >> "%s" &'\
          %(Port, packet_size, LogFile)
    elif 'FTP' == ProtocolType or 'Dual TCP' == ProtocolType:
        cmd = 'iperf -s -P 0 -i 1 -p %s -f k >> "%s" &'\
          %(Port, LogFile)
    else:
        raise Exception, "Please check the protocol type!!"
    
    ret = connections.execute_ssh_command_without_check("rm -f %s"%LogFile)
    ret = connections.execute_ssh_command_without_check(cmd)
    
    pid_tmp = re.search('\]\s*(\d+)', ret,re.M)
    if pid_tmp:
        pid = pid_tmp.group(1)
    else:
        pid = None
    
    return pid    

def iperf_server_stop_ssh(Port):
    """This keyword will stop Iperf server.

    | Input Parameters | Man. | Description |
    | Port             | Yes  | port running iperf server |

    Example
    | Iperf Server Stop Ssh | 5086 |
    """

    try:
        pcmd = "lsof -i:%s" %Port
        ret = connections.execute_ssh_command_without_check(pcmd)
        pattern = 'iperf\s+(\d+)\s+'
        match = re.search(pattern, ret)
        if match:
            connections.execute_ssh_command_without_check('kill -9 %s' %match.group(1))
    except Exception,e:
        print e

def iperf_client_start_ssh(IperfServeIp, Port, Bandwidth, Delay, ProtocolType = 'UDP', packet_size='1024', bindIp='192.168.255.126', parallel='1'):
    """This keyword will start Iperf Client in linux.
       In robot script, you should swith the ssh connect to the specific PC first.

    | Input Parameters | Man. | Description |
    | IperfServeIp     | Yes  | Iperf Serve PC IP |
    | Port             | Yes  | Same with Serve Port |
    | Bandwidth        | Yes  | The bandwidth of client send package, unit: M , use in 'UDP' and 'DUAL UDP' |
    | Delay            | Yes  | Time of client send package, unit:second |
    | ProtocolType     | No   | Default as 'UDP', also could be 'FTP','DUAL TCP', 'DUAL UDP' |
    | packet_size      | No   | Default as '1024' use in 'UDP' protocol|
    | bindIp           | No   | Default as '192.168.255.126' use in 'TCP' protocol |
    | parallel         | No   | Default as '1' use in 'Ftp' protocol |
    
    | return | pid |
    Example
    | ${client_pid} | Iperf client Start ssh | '1.1.1.1' | 50866 | 10 | 1000 |
    
    """    
    iperfPath = "iperf"
    dualport = 58899
    if 'UDP' == ProtocolType:
        if Delay.upper().endswith("B") or Delay.upper().endswith("K") or Delay.upper().endswith("M")\
            or Delay.upper().endswith("G"):
            cmd1 = '%s -c %s -u -P 1 -i 1 -p %s -w 41.0K -l %s.0B -f k -b %sM -n %s -T 1 >> iperf_client.txt &'\
                  %(iperfPath, IperfServeIp, Port, packet_size, Bandwidth, Delay)
        else:
            cmd1 = '%s -c %s -u -P 1 -i 1 -p %s -w 41.0K -l %s.0B -f k -b %sM -t %s -T 1 >> iperf_client.txt &'\
                  %(iperfPath, IperfServeIp, Port, packet_size, Bandwidth, Delay)

    elif 'FTP' == ProtocolType:
        if Delay.upper().endswith("B") or Delay.upper().endswith("K") or Delay.upper().endswith("M")\
            or Delay.upper().endswith("G"):
            cmd1 = '%s -c %s -P %s -i 1 -p %s -f k -n %s -T 1 >> iperf_client.txt &'\
            %(iperfPath, IperfServeIp, parallel, Port, Delay)
        else:
            cmd1 = '%s -c %s -P %s -i 1 -p %s -f k -t %s -T 1 >> iperf_client.txt &'\
            %(iperfPath, IperfServeIp, parallel, Port, Delay)

    elif 'Dual UDP' == ProtocolType:
        if Delay.upper().endswith("B") or Delay.upper().endswith("K") or Delay.upper().endswith("M")\
            or Delay.upper().endswith("G"):
            cmd1 = '%s -c %s -u -P 1 -i 1 -p %s -w 41.0K -l 1024.0B -f k -b %sM -n %s -d -L %s -T 1 >> iperf_client.txt &'\
                    %(iperfPath, IperfServeIp, Port, Bandwidth, Delay,dualport)
        else:
            cmd1 = '%s -i -d %s -c %s -u -P 1 -i 1 -p %s -w 41.0K -l 1024.0B -f k -b %sM -t %s -d -L %s -T 1 >> iperf_client.txt &'\
                    %(iperfPath, IperfServeIp, Port, Bandwidth, Delay,dualport)

    elif 'Dual TCP' == ProtocolType:
        if Delay.upper().endswith("B") or Delay.upper().endswith("K") or Delay.upper().endswith("M")\
            or Delay.upper().endswith("G"):
            cmd1 = '%s -c %s -P %s -i 1 -p %s -f k -n %s -d -L %s -T 1 -B %s >> iperf_client.txt &'\
                   %(iperfPath, IperfServeIp, parallel, Port, Delay, dualport, bindIp)
        else:
            cmd1 = '%s -c %s -P %s -i 1 -p %s -f k -t %s -d -L %s -T 1 -B %s >> iperf_client.txt &'\
                   %(iperfPath, IperfServeIp, parallel, Port, Delay, dualport, bindIp)
    else:
        raise Exception, "Please check the protocol type!!"
    connections.execute_ssh_command_without_check("rm -f iperf_client.txt")
    ret = connections.execute_ssh_command_without_check(cmd1)
    pid_tmp = re.search('\]\s*(\d+)', ret,re.M)
    if pid_tmp:
        pid = pid_tmp.group(1)
    else:
        pid = None
    
    return pid    
def iperf_serve_start(Port, LogFile, ProtocolType = 'UDP', packet_size='1024', mulserver=True):
    """This keyword will start Iperf Serve.
       In robot script, you should swith the telnet connect to the specific PC first.

    | Input Parameters | Man. | Description |
    | Port             | Yes  | Specifical port |
    | LogFile          | Yes  | Iperf serve log file path and name |
    | ProtocolType     | No   | Protocal type, can be UDP, Dual UDP, FTP, and Dual TCP |
    | packet_size      | No   | The package size of UDP type |
    | mulserver        | No   | The flag of launch multi iperf server, can launch multi server only if this flag is open. |

    Example
    | Iperf Serve Start | 5086 | C:\\log\\iperfDL.txt |
    """
    if mulserver:
        print "*INFO* Mult-iperf flag opened!"
    try:
        pcmd = "netstat -ano|grep %s" %Port
        ret = connections.execute_shell_command_without_check(pcmd)
        pid = ret.splitlines()[1].split()[-1]
        if 0 != int(pid):
            kcmd = "taskkill /F /T /PID %s" % pid
            connections.execute_shell_command_without_check(kcmd)

    except Exception,e:
        print e

    if 'UDP' == ProtocolType or 'Dual UDP' == ProtocolType:
        cmd1 = '%s -s -u -P 0 -i 1 -p %s -w 41.0K -l %s.0B -f k -o "%s"'\
          %(iperfPath, Port, packet_size, LogFile)
        cmd2 = 'iperf.exe -s -u -P 0 -i 1 -p %s -w 41.0K -l %s.0B -f k -o "%s"'\
          %(Port, packet_size, LogFile)
    elif 'FTP' == ProtocolType or 'Dual TCP' == ProtocolType:
        cmd1 = '%s -s -P 0 -i 1 -p %s -f k -o "%s"'\
          %(iperfPath, Port, LogFile)
        cmd2 = 'iperf.exe -s -P 0 -i 1 -p %s -f k -o "%s"'\
          %(Port, LogFile)
    else:
        raise Exception, "Please check the protocol type!!"

    if mulserver:
        cmd2 = "psexec.exe -i -d %s %s" %(iperfMgrPath, cmd2)
        cmd1 = "%s -i -d %s %s" %(psexecPath, iperfMgrPath, cmd1)
    else:
        cmd2 = cmd2 + " -D"
        cmd1 = cmd1 + " -D"
    ret = connections.execute_shell_command_without_check(cmd2)

    if mulserver:
        if "process ID" in ret:
            pass
        else:
            ret = connections.execute_shell_command_without_check(cmd1)
            if not "process ID" in ret:
                raise Exception, "IPerf Service started on %s failed" % Port
    else:
        if ret.find('IPerf Service started') < 0:
            ret = connections.execute_shell_command_without_check(cmd1)
            if ret.find('IPerf Service started') < 0:
                raise Exception, "IPerf Service started on %s failed" % Port

def iperf_serve_stop(Port, ProtocolType = 'UDP', mulserver=True):
    """This keyword will stop Iperf serve.

    | Input Parameters | Man. | Description |
    | Port             | Yes  | port running iperf server |
    | ProtocolType     | No   | Default is UDP |

    Example
    | Iperf Serve Stop | 5086 |
    """

    if 'UDP' == ProtocolType or 'Dual UDP' == ProtocolType:
        cmd = 'iperf.exe -s -u -p %s -R' % Port
    elif 'FTP' == ProtocolType or 'Dual TCP' == ProtocolType:
        cmd = 'iperf.exe -s -p %s -R' % Port
    else:
        raise Exception, "Please check the protocol type!!"
    if mulserver:
        try:
            pcmd = "netstat -ano|grep '0.0.0.0:%s '" % Port
            ret = connections.execute_shell_command_without_check(pcmd)
            pid = ret.splitlines()[1].split()[-1]
            kcmd = "taskkill /F /T /PID %s" % pid
            connections.execute_shell_command_without_check(kcmd)
        except Exception,e:
            print e
    else:
        connections.execute_shell_command_without_check(cmd)


def iperf_client_start(IperfServeIp, Port, Bandwidth, Delay, ProtocolType = 'UDP', packet_size='1024', bindIp='192.168.255.126', parallel='1'):
    """This keyword will start Iperf Client.
       In robot script, you should swith the telnet connect to the specific PC first.

    | Input Parameters | Man. | Description |
    | IperfServeIp     | Yes  | Iperf Serve PC IP |
    | Port             | Yes  | Same with Serve Port |
    | Bandwidth        | Yes  | The bandwidth of client send package, unit: M , use in 'UDP' and 'DUAL UDP' |
    | Delay            | Yes  | Time of client send package, unit:second |
    | ProtocolType     | No   | Default as 'UDP', also could be 'FTP','DUAL TCP', 'DUAL UDP' |
    | packet_size      | No   | Default as '1024' use in 'UDP' protocol|
    | bindIp           | No   | Default as '192.168.255.126' use in 'TCP' protocol |
    | parallel         | No   | Default as '1' use in 'Ftp' protocol |

    Example
    | Iperf Client Start | 10.68.152.44 | 5086 | 20 | 1 |
    """

    dualport = 58899
    print "*INFO*" ,"The protocolType you select is: ", ProtocolType
    Delay = str(Delay)
    if 'UDP' == ProtocolType:
        if Delay.upper().endswith("B") or Delay.upper().endswith("K") or Delay.upper().endswith("M")\
            or Delay.upper().endswith("G"):
            cmd1 = '%s -i -d %s -c %s -u -P 1 -i 1 -p %s -w 41.0K -l %s.0B -f k -b %sM -n %s -T 1'\
                  %(psexecPath, iperfPath, IperfServeIp, Port, packet_size, Bandwidth, Delay)
            cmd2 = 'psexec.exe -i -d iperf.exe -c %s -u -P 1 -i 1 -p %s -w 41.0K -l %s.0B -f k -b %sM -n %s -T 1'\
                  %(IperfServeIp, Port, packet_size, Bandwidth, Delay)
        else:
            cmd1 = '%s -i -d %s -c %s -u -P 1 -i 1 -p %s -w 41.0K -l %s.0B -f k -b %sM -t %s -T 1'\
                  %(psexecPath, iperfPath, IperfServeIp, Port, packet_size, Bandwidth, Delay)
            cmd2 = 'psexec.exe -i -d iperf.exe -c %s -u -P 1 -i 1 -p %s -w 41.0K -l %s.0B -f k -b %sM -t %s -T 1'\
                  %(IperfServeIp, Port, packet_size, Bandwidth, Delay)

        if bindIp != "192.168.255.126":
            cmd1 = cmd1 + " -B " + bindIp
            cmd2 = cmd2 + " -B " + bindIp

    elif 'FTP' == ProtocolType:
        if Delay.upper().endswith("B") or Delay.upper().endswith("K") or Delay.upper().endswith("M")\
            or Delay.upper().endswith("G"):
            cmd1 = '%s -i -d %s -c %s -P %s -i 1 -p %s -f k -n %s -T 1'\
            %(psexecPath, iperfPath, IperfServeIp, parallel, Port, Delay)
            cmd2 = 'psexec.exe -i -d iperf.exe -c %s -P %s -i 1 -p %s -f k -n %s -T 1'\
            %(IperfServeIp, parallel, Port, Delay)
        else:
            cmd1 = '%s -i -d %s -c %s -P %s -i 1 -p %s -f k -t %s -T 1'\
            %(psexecPath, iperfPath, IperfServeIp, parallel, Port, Delay)
            cmd2 = 'psexec.exe -i -d iperf.exe -c %s -P %s -i 1 -p %s -f k -t %s -T 1'\
            %(IperfServeIp, parallel, Port, Delay)

    elif 'Dual UDP' == ProtocolType:
        if Delay.upper().endswith("B") or Delay.upper().endswith("K") or Delay.upper().endswith("M")\
            or Delay.upper().endswith("G"):
            cmd1 = '%s -i -d %s -c %s -u -P 1 -i 1 -p %s -w 41.0K -l 1024.0B -f k -b %sM -n %s -d -L %s -T 1'\
                    %(psexecPath, iperfPath, IperfServeIp, Port, Bandwidth, Delay,dualport)
            cmd2 = 'psexec.exe -i -d iperf.exe -c %s -u -P 1 -i 1 -p %s -w 41.0K -l 1024.0B -f k -b %sM -n %s -d -L %s -T 1'\
                    %(IperfServeIp, Port, Bandwidth, Delay, dualport)
        else:
            cmd1 = '%s -i -d %s -c %s -u -P 1 -i 1 -p %s -w 41.0K -l 1024.0B -f k -b %sM -t %s -d -L %s -T 1'\
                    %(psexecPath, iperfPath, IperfServeIp, Port, Bandwidth, Delay,dualport)
            cmd2 = 'psexec.exe -i -d iperf.exe -c %s -u -P 1 -i 1 -p %s -w 41.0K -l 1024.0B -f k -b %sM -t %s -d -L %s -T 1'\
                    %(IperfServeIp, Port, Bandwidth, Delay, dualport)

    elif 'Dual TCP' == ProtocolType:
        if Delay.upper().endswith("B") or Delay.upper().endswith("K") or Delay.upper().endswith("M")\
            or Delay.upper().endswith("G"):
            cmd1 = '%s -i -d %s -c %s -P %s -i 1 -p %s -f k -n %s -d -L %s -T 1 -B %s'\
                  %(psexecPath, iperfPath, IperfServeIp, parallel, Port, Delay, dualport, bindIp)
            cmd2 = 'psexec.exe -i -d iperf.exe -c %s -P %s -i 1 -p %s -f k -n %s -d -L %s -T 1 -B %s'\
                  %(IperfServeIp, parallel, Port, Delay, dualport, bindIp)
        else:
            cmd1 = '%s -i -d %s -c %s -P %s -i 1 -p %s -f k -t %s -d -L %s -T 1 -B %s'\
                    %(psexecPath, iperfPath, IperfServeIp, parallel, Port, Delay, dualport, bindIp)
            cmd2 = 'psexec.exe -i -d iperf.exe -c %s -P %s -i 1 -p %s -f k -t %s -d -L %s -T 1 -B %s'\
                    %(IperfServeIp, parallel, Port, Delay, dualport, bindIp)
    else:
        raise Exception, "Please check the protocol type!!"

    ret = connections.execute_shell_command_without_check(cmd2)
    if ret.find('iperf.exe started') < 0:
        ret = connections.execute_shell_command_without_check(cmd1)
    if ret.find('iperf.exe started') < 0:
        raise Exception, "iperf.exe started failed"
    else:
        lines = ret.splitlines()
        for line in lines:
            if 'iperf.exe started' in line:
                tmp = line.split(' ')[-1].strip()
                ProcessId = tmp.split('.')[0]
                return ProcessId

def miperf_client_start(IperfServeIp, Port, Bandwidth, Delay, ProtocolType = 'UDP', packet_size='1024'):
    """This keyword will start Iperf Client.
       In robot script, you should swith the telnet connect to the specific PC first.

    | Input Parameters | Man. | Description |
    | IperfServeIp     | Yes  | Iperf Serve PC IP |
    | Port             | Yes  | Same with Serve Port |
    | Bandwidth        | Yes  | The bandwidth of client send package, unit: M |
    | Delay            | Yes  | Time of client send package, unit:second |

    Example
    | Iperf Client Start | 10.68.152.44 | 5086 | 20 | 1 |
    """


    cmd = 'start %s -c %s -u -P 1 -i 1 -p %s -l %s.0B -f k -b %sM -t %s -T 1'\
              %(miperfPath, IperfServeIp, Port, packet_size, Bandwidth, Delay)

    ret = connections.execute_shell_command_without_check(cmd)



def iperf_client_stop(process_id):
    """This keyword will stop Iperf client.

    | Input Parameters | Man. | Description |
    | Port             | Yes  | port running iperf client |

    Example
    | Iperf Client Stop | 5086 |
    """
    connections.execute_shell_command_without_check("TASKLIST | grep iperf")
    connections.execute_shell_command_without_check("TASKKILL /F /PID %s" % process_id)

def iperf_get_summarized_value(server_output, value='Kbits'):
    """This keyword returns the summarized value.

    | Input Parameters | Man. | Description |
    | server_output    | Yes  | Iperf Serve output file |
    | value            | No   | the summarized value you want to get from file, defaut is Kbits |

    | Return value     | '' or summarized value - e.g. Kbits or KBytes|

    Example
    | ${result} | iperf get summarized value | C:\\iperf_out.log |
    | ${result} | iperf get summarized value | C:\\iperf_out.log | KBytes |

    Note:
	only get the last summarized line content in iperf file.
    """

    flag = True
    summary_result = ''
    pattern = '\[(\d+)\]\s+([0-9.]+\s*-\s*[0-9.]+)\s+sec\s+[0-9.]+\s+KBytes\s+([0-9.]+)\s+Kbits/sec'
    
    file_content_lines = file_read(server_output)
    
    for i in range(-1, -len(file_content_lines)-1, -1):
        if re.match(pattern, file_content_lines[i]):
            flag = False
            print 'find summarized line:%s' % (file_content_lines[i])
            summary_result = file_content_lines[i].split(str(value))[0].strip().split()[-1]
            break;
    if flag:
        print "can't find summarized line in %s" % (server_output)

    
    return summary_result

def iperf_get_throughput(server_output, allvalue=False):
    """This keyword returns the average throughput.

    | Input Parameters | Man. | Description |
    | server_output    | Yes  | Iperf Serve output file |
    | allvalue         | No   | if False return average value, if True return max/min/avg value |

    | Return value     | 0 or real througput value or max/min/avg value |

    Example
    | ${result} | Iperf Get Throughput | C:\\iperf_out.log |
    | Run Keyword If | 0==${result} | Fail | value is zero |

    Note:
	First 10% and last 5% throughput lines (by timestamp) in input file will NOT be calculated into output.
    """

    lines = file_read(server_output, "string")

    max_throughput = 0
    min_throughput = 0
    average_throughput = 0
    result_throughput_list = []
    pattern = '\[\s*(\d+)\]\s+([0-9.]+\s*-\s*[0-9.]+)\s+sec\s+[0-9.]+\s+KBytes\s+([0-9.]+)\s+Kbits/sec'

    p_single = re.compile(pattern, re.M)

    ret_single = p_single.findall(lines)
    raw_throughput_list = []
    print '*INFO* total throughput lines in file %s : %d' %(server_output, len(ret_single))
    for match in ret_single:
        second_space = [float(item.strip()) for item in match[1].split('-')]
        if second_space[1] - second_space[0] != 1.0:
            continue
        else:
            raw_throughput_list.append((match[0], second_space[0], float(match[2]))) # thread indexer, time from(sec), throughput
    del ret_single
    throughput_dict = {}
    thread_dict = {}
    
    for a_throughput_match in raw_throughput_list:
        if a_throughput_match[1] not in throughput_dict.keys():
            throughput_dict[a_throughput_match[1]] = a_throughput_match[2]
            thread_dict[a_throughput_match[1]] = [a_throughput_match[0]]
        
        elif (a_throughput_match[1] in throughput_dict.keys()) and \
             (a_throughput_match[0] not in thread_dict[a_throughput_match[1]]):
            throughput_dict[a_throughput_match[1]] += a_throughput_match[2]
            thread_dict[a_throughput_match[1]].append(a_throughput_match[0])
        
        elif (a_throughput_match[1] in throughput_dict.keys()) and \
             (a_throughput_match[0] in thread_dict[a_throughput_match[1]]):
            throughput_dict[a_throughput_match[1]] = a_throughput_match[2]
            thread_dict[a_throughput_match[1]] = [a_throughput_match[0]]
    
    tmp_keys = throughput_dict.keys()    
    tmp_keys.sort()    
    sum_value = len(tmp_keys)
    for idx in range(sum_value):        
        if idx+1 < sum_value*0.1 or idx+1 > sum_value*0.95:
            continue
        else:
            if throughput_dict[tmp_keys[idx]] == 0:
                print tmp_keys[idx], throughput_dict[tmp_keys[idx]]
            result_throughput_list.append(throughput_dict[tmp_keys[idx]])

    if 0 < len(result_throughput_list):
        max_throughput = '%.2f' %max(result_throughput_list)
        min_throughput = '%.2f' %min(result_throughput_list)
        average_throughput = '%.2f' %float(sum(result_throughput_list) / len(result_throughput_list))
    '''
    # add to print summary result in output file  by zhaolibo
    file_content_lines = file_read(server_output)
    for i in range(-1, -len(file_content_lines)-1, -1):
        if re.match(pattern, file_content_lines[i]):
            print file_content_lines[i]
            summary_result = file_content_lines[i].split('Kbits')[0].strip().split()[-1]
            break;
    '''
    
    print '*DEBUG*AVERAGE_THROUGHPUT = %s' %average_throughput
    print '*DEBUG*MAXIMUM_THROUGHPUT = %s' %max_throughput
    print '*DEBUG*MINIMUM_THROUGHPUT = %s' %min_throughput
    return average_throughput if (not allvalue) else [max_throughput, min_throughput, average_throughput]

if __name__ == '__main__':
    #A_Not_Less_Than_B('2.1', '5')
    #connections.connect_to_host('10.68.152.86', 23, 'tdlte-tester', 'btstest')
    #iperf_client_start('10.68.152.86', '5003', '10','10', 'Dual TCP','1024', '192.168.255.199')
    #iperf_serve_stop('5011', 'UDP')
    #iperf_get_throughput("e:\zhanghongming\\cacrt\\logs\\1035-C TM3 20M 17\\1035-C_TM3_20M 1_7_20130107165239\DLIperflog_20130107165240.txt")
    '''
    print iperf_get_throughput("D:\\temp\\iperf.txt",'true')
    print "================"
    print iperf_get_throughput("D:\\temp\\iperf.txt")
    print "@@@@@@@@@@@@@@@@@@@@@@@@"
    print iperf_get_summarized_value("D:\\temp\\iperf.txt")
    print "============================="
    print iperf_get_summarized_value("D:\\temp\\iperf.txt", "KBytes")
    '''


    pass

