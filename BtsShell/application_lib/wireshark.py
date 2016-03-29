import re, os
from BtsShell import connections
from BtsShell.application_lib.protocols import *

def _wireshark_capture(file_name, interface= '3', timeout = '600'):
    """This keyword get the FTM network interface package by wireshark,and save
       the pcap  file in dir "C:"

    | Input Parameters  | Man. | Description |
    | file_name         | Yes  | Name of save pcap file |
    | interface         | No   | index of network interface,default is 3,baseon TM500 controlPC |
    | timeout           | No   | set time for capture,and default is 600 sec |

    Example
    | Wireshark Capture | C:\\test.pcap |
    """

    cmd = '"c:\\Program Files\\Wireshark\\wireshark.exe"  -i %d -a duration:%d -k  -Q  -w  C:\\%s.pcap'  %(int(interface),int(timeout),file_name)
    ret = connections.execute_shell_command_without_check(cmd)


def _start_tshark_on_linux(pcap_file, interface = "eth0"):
    """This keyword start wireshark capture on Linux system, and save the file as pcap file

    | Input Parameters  | Man. | Description |
    | pcap_file         | Yes  | Name of save pcap file |
    | interface         | No   | index of network interface, default is eth0 |

    Example
    | Start Tshark On Linux | test.pcap |
    """

    process_id =''
    cmd = "tshark -i %s -w /tmp/%s &" % (interface, pcap_file)
    ret = connections.execute_shell_command_without_check(cmd)
    pattern = '\[\d*\] *(\d+)'
    match =  re.search(pattern, ret)
    if match:
        process_id = match.group(1)
    return process_id

def _stop_tshark_on_linux(process_id = ""):
    """This keyword stop wireshark capture on Linux system by kill the tshark process
    | Input Parameters  | Man. | Description |
    | process_id | No | Choose the process id to kill,If omitted, it will kill all
    Example
    | Stop Tshark On Linux |

    """
    if "" != process_id:
        cmd = "kill -9 %s" %( process_id )
        ret_kill = connections.execute_shell_command_without_check(cmd)
    else:
        ret = connections.execute_shell_command_without_check("ps -ef | grep tshark")
        lines = ret.split("\n")
        for line in lines:
            pattern = "^root[\s]+([\d]+)\s.*tshark"
            match_obj = re.search(pattern, line)
            if match_obj:
                cmd = "kill -9 %s"  %(int(match_obj.group(1)))
                ret = connections.execute_shell_command_without_check(cmd)

def stop_tshark(login_type = 'telnet', process_id = ""):
    """This keyword stop wireshark capture
    | Input Parameters  | Man. | Description |
    | login_type  | No | Login method |
    | process_id | No | Choose the process id to kill,If omitted, it will kill all
    Example
    | Stop tshark |
    """
    
    if 'telnet' == login_type:

        connection_type = connections.get_current_connection_type()
        if connection_type == 'Windows':
            if "" != process_id:
                cmd = 'taskkill /F /PID %s' %( process_id )
            else:    
                cmd = 'taskkill /F /IM tshark.exe'
            connections.execute_shell_command_without_check(cmd)
        elif connection_type == 'Linux' or connection_type == 'Device':
            if "" != process_id:
                cmd = "kill -9 %s" %( process_id )
                ret_kill = connections.execute_shell_command_without_check(cmd)
            else:
                ret = connections.execute_shell_command_without_check("ps -ef | grep tshark")
                lines = ret.split("\n")
                for line in lines:
                    pattern = "^root[\s]+([\d]+)\s.*tshark"
                    if re.search(pattern, line):
                        cmd = "kill -9 %s"  %(int(re.search(pattern, line).group(1)))
                        ret_kill = connections.execute_shell_command_without_check(cmd)
        else:
            raise Exception, "Unknow connection type as '%s'"%connection_type
    elif 'ssh' == login_type:

            if "" != process_id:
                cmd = "kill -9 %s" %( process_id )
                ret_kill = connections.execute_ssh_command_without_check(cmd)
            else:
                ret = connections.execute_ssh_command_without_check("ps -ef | grep tshark")
                lines = ret.split("\n")
                for line in lines:
                    pattern = "^root[\s]+([\d]+)\s.*tshark"
                    if re.search(pattern, line):
                        cmd = "kill -9 %s"  %(int(re.search(pattern, line).group(1)))
                        ret_kill = connections.execute_ssh_command_without_check(cmd)

def start_tshark(file_dir, interface = 'eth0', duration = '', filte = None, login_type = 'telnet'):
    """This keyword start wireshark capture and save the file as text file -new

    | Input Parameters  | Man. | Description |
    | file_dir          | Yes  | Directory of output file |
    | interface         | No   | Index of network interface, default is eth0 |
    | duration          | No   | Capture duration, unit is sec |
    | filte             | No   | Filte |

    Example
    | Start TShark | wireshark.txt |
    """

    process_id = ''
    
    if 'telnet' == login_type:

        connection_type = connections.get_current_connection_type()
        if duration == '':
            option = ''
        else:
            option = ' -a duration:%s' % duration

        if filte == None:
            filte = 'ip'
        else:
            pass

        if connection_type == 'Windows':
            command = 'psexec -i -d cmd /c \"tshark -i %s%s  -R \"%s\"  -V > %s\"' % (interface, option,filte, file_dir)
            ret = connections.execute_shell_command_without_check(command)

            cmdlst = ['tasklist', 'pslist tshark']
            for cmd in cmdlst:
                ret = connections.execute_shell_command_without_check(cmd)
                pattern = 'tshark[.ex]* +(\d+)'
                match  =  re.findall(pattern, ret)
                if match :
                    process_id = match[(len(match) - 1)]
                    break
            
        elif connection_type == 'Linux' or connection_type == 'Device':
            
            command =  'nohup tshark -i %s%s -R \"%s\" -V > %s &' % (interface, option, filte, file_dir)
            pattern = '\[\d*\] *(\d+)'
            ret = connections.execute_shell_command_without_check(command)
            match =  re.search(pattern, ret)
            if match:
                process_id = match.group(1)
        else:
            raise Exception, "Unknow connection type as '%s'"%connection_type
    elif 'ssh' == login_type:

        if duration == '':
            option = ''
        else:
            option = ' -a duration:%s' % duration

        if filte == None:
            filte = 'ip'
        else:
            pass

        command =  'nohup tshark -i %s%s -R \"%s\" -V > %s &' % (interface, option, filte, file_dir)
        ret = connections.execute_ssh_command_without_check(command)
        pattern = '\[\d*\] *(\d+)'
        match =  re.search(pattern, ret)
        if match:
            process_id = match.group(1)
                
    return process_id

def tshark_capture_pcap_log(file_dir, interface = 'eth0', filte = '', duration = '', login_type = 'telnet'):
    """This keyword start wireshark capture and save the file as pcap file

    | Input Parameters  | Man. | Description |
    | file_dir          | Yes  | Directory of output file |
    | interface         | No   | Index of network interface, default is eth0 |
    | duration          | No   | Capture exit condition:duration(sec) and filesize(KB), -a duration:20 -a filesiez:400  |
    | filte             | No   | Filte |

    Example
    | start_tshark_pcap | wireshark.txt | eth0 | ip |  30 filesize:50  |
    | start_tshark_pcap | wireshark.txt | eth0 | ip |  30 |
    Edit: add option -F libpcap to capture pcap file use tshark --by GuanXiaobing 2012-05-14
    Edit: add option -a filesize to stop capture,when get duration,search keyword filesize is in it
          or not,which decide to use duration or filesize for -a.--by GuanXiaobing 2012-05-15
    """

    process_id = ''
    if duration == '':
        option = ''
    else:
        ret = re.match('\s*(\d*)\s*filesize:(\d+).*',duration)
        if ret and (len(str(ret.group(1))) == 0):
            option = ' -a filesize:%s' % (ret.group(2))
        elif ret and (len(str(ret.group(1))) != 0):
            option = ' -a  duration:%s -a filesize:%s' % (ret.group(1),ret.group(2))
        else:
            option = ' -a duration:%s' % duration
    if filte == '' :
        option_f = ''
    else:
        option_f = ' -f \"%s\"' %filte
            
    if 'telnet' == login_type:
        connection_type = connections.get_current_connection_type()
        if connection_type == 'Windows':
            command = 'psexec -i -d cmd /c tshark -i %s%s -w  %s -F libpcap -q %s' % (interface, option_f, file_dir,option)
            print command
            ret = connections.execute_shell_command_without_check(command)
            cmdlst = ['tasklist', 'pslist tshark']
            for cmd in cmdlst:
                ret = connections.execute_shell_command_without_check(cmd)
                pattern = 'tshark[.ex]* +(\d+)'
                match  =  re.findall(pattern, ret)
                if match > 0:
                    process_id = match[(len(match) - 1)]
                    break
        elif connection_type == 'Linux' or connection_type == 'Device':
            
            command = 'tshark -i %s%s -w %s -F libpcap -q%s&' % (interface, option_f, file_dir,option)
            print command
            ret = connections.execute_shell_command_without_check(command)
            pattern = '\[\d*\] *(\d+)'
            match =  re.search(pattern, ret)
            if match:
                process_id = match.group(1)
        else:
            raise Exception, "Unknow connection type as '%s'"%connection_type
    elif 'ssh' == login_type:
        command = 'tshark -i %s%s -w %s  -F libpcap -q%s&' % (interface, option_f, file_dir, option)
        print command
        ret = connections.execute_ssh_command_without_check(command)
        pattern = '\[\d*\] *(\d+)'
        match =  re.search(pattern, ret)
        if match:
            process_id = match.group(1)
                
    return process_id

def analyze_ethernet_frame(file_dir, *conditions):
    """
    This keyword analyses the wireshark text file which generated by 'tshark'.
    It can have multiple conditions as filters with 'AND' logic.
    It returns the Frames instance which inherited from BtsShell.helper.CommonDict which key is the frame id.
       Following are the possible attributes can be access with hierarchy, such as
       - ethernet.type
       - ethernet.ip.protocol
       - ethernet.ip.icmp.typ
       - ethernet.ip.udp.source_port
       - ethernet.ip.tcp.window_size

       ethernet
           - source_mac
           - destination_mac
           - type

       ethernet.vlan
           - priority
           - cfi
           - id
           - type

       ethernet.ip
           - version
           - header_length
           - tos
           - dscp
           - total_length
           - identification
           - flags
           - fragment_offset
           - ttl
           - protocol
           - checksum
           - source_ip
           - destination_ip

        ethernet.ip.icmp
           - type
           - code
           - checksum
           - identifier
           - sequence_number
           - data

        ethernet.ip.udp
           - source_port
           - destination_port
           - length
           - checksum

        ethernet.ip.udp.gtp
           - flags
           - message_type
           - length
           - teid
           - sequence_number
           - npdu_number
           - data

        ethernet.ip.udp.dhcp
           - operation
           - hw_type
           - hw_length
           - hops
           - transaction_id
           - seconds_elapsed
           - flags
           - client_ip
           - your_ip
           - next_server_ip
           - relay_agent_ip
           - client_mac
           - server_name
           - boot_file_name
           - options (dict)

        ethernet.ip.tcp
           - source_port
           - destination_port
           - sequence_number
           - acknowledgement_number
           - header_length
           - flags
           - window_size
           - checksum
        ethernet.ip.sctp
           - source_port
           - destination_port
           - verification_tag
           - checksum
           - chunk_type
           - chunk_flag
           - chunk_length
           - chunk_parameters (dict with key equals parameter name)
        ethernet.ip.sctp.s1ap

    Be notice that not all the protocols can be parsed and debugging msg will be printed if unsupported protocols met.
    This is the first version for wireshark log analyze which may contains defects,
        please contact TA CORE team if you met any problems

    | Input Parameters  | Man. | Description |
    | file_dir          | Yes  | input wireshark text file |
    | *conditions       | No   | multiple filters and it can be given as 'ethernet.ip.type=ICMP' |

    Example
    | Analyze Ethernet Frame | ${TEMPDIR}\\wireshark.txt |
    | Analyze Ethernet Frame | ${TEMPDIR}\\wireshark.txt | ethernet.ip.type=ICMP |
    | Analyze Ethernet Frame | ${TEMPDIR}\\wireshark.txt | ethernet.ip.udp.source_port=53 | ethernet.ip.flags=10 |
    """
    try:
        file_handle = open(file_dir, 'r')
    except:
        raise Exception, 'file %s open fail' % file_dir

    try:
        lines = file_handle.readlines()
        frame_list = []
        temp_line = ''

        for line in lines:
            if re.match('^Frame\s*\d+', line):
                index_num = lines.index(line)
                break
        try:
            lines = lines[index_num:]
        except:
            pass
        
        for line in lines:
            if re.match('^Frame\s*\d+', line):
                if len(temp_line) != 0:
                    frame_list.append(temp_line)
                temp_line = ''
            temp_line = temp_line + line
        #frame_list.append(temp_line)
        ethernet_frames = Frames(frame_list)
    finally:
        file_handle.close()

    return _filter_ethernet_frames(ethernet_frames, conditions)


def _filter_ethernet_frames(ethernet_frames, conditions):

    match_ethernet_frame = CommonDict()
    condition_list = _parse_condition(conditions)

    for (index, ethernet_frame) in ethernet_frames.items():
        condition_match = True
        for condition in condition_list:
            (attribute, logic, value) = condition
            try:
                if not eval("ethernet_frame.%s%s'%s'" % (attribute, logic, value)):
                    condition_match = False
                    break
            except AttributeError:
                print '*DEBUG* AttributeError, no attribute %s available' % attribute
                condition_match = False
                break
            except:
                pass
        if condition_match:
            match_ethernet_frame[index] = ethernet_frame

    """
    condition_dict = _parse_condition(conditions)
    for (index, ethernet_frame) in ethernet_frames.items():
        condition_match = True
        for (attribute, value) in condition_dict.items():
            try:
                if eval('ethernet_frame.%s' % attribute) != value:
                    condition_match = False
                    break
            except AttributeError:
                print '*DEBUG* AttributeError, no attribute %s available' % attribute
                condition_match = False
                break
        if condition_match:
            match_ethernet_frame[index] = ethernet_frame
    """
    return match_ethernet_frame

def _parse_condition(conditions):
    SUPPORTED_LOGIC = ['>=', '<=', '<', '>', '!=', '=']
    condition_list = []

    for condition in conditions:
        for logic in SUPPORTED_LOGIC:
            if condition.find(logic) > 0:
                (attribute, value) = condition.split(logic)
                if logic == '=':
                    logic = '=='
                condition_list.append((attribute, logic, value))
                break
    return condition_list

"""
def _parse_condition(conditions):
    condition_dict = {}
    for condition in conditions:
        (attribute, value) = condition.split('=')
        condition_dict[attribute] = value
    return condition_dict
"""

def get_AP_value_from_ethernet_frame(file_dir,protocol_type,message_type,location,*ie_info):
    """This keyword get value base on  analyze_ethernet_frame

    | Input Parameters  | Man. | Description |
    | file_dir          | Yes  | input wireshark text file |
    | protocol_type     | Yes  | protocol type which want to get,can be 's1ap' or 'x2ap'  |
    | message_type      | Yes  | type of s1ap message  |
    | location          | Yes  | location of value  |
    | ie_info           | Yes  | item_name and ie name,like Cause.radioNetwork,Cause.Cause,TargetCell-ID.pLMN-Identity   |

    Example1(get some ie values in the same frame,but one or more items),return all values at different frames:
    | get_AP_value_from_ethernet_frame  | d:\\X2ap.txt  | x2ap |  0  |  all | Cause.radioNetwork   |  Cause.Cause  | TargetCell-ID.pLMN-Identity |
    Example2 return the value only default at location :
    | get_AP_value_from_ethernet_frame  | d:\\X2ap.txt  | x2ap |  0  |   1  | Cause.radioNetwork = radioNetwork |  TargetCell-ID.pLMN-Identity |
    """

    value_dict = {}
    keys_list = []
    match_frame_list = []
    value_list = []
    result_list  = []
    ie_num = len(ie_info)
    if location == 'all':
        Flag = 'Yes'
    else:
        location = int(location)
        Flag = 'No'



    protocol_type = 'ethernet.ip.sctp.' + protocol_type
    ret = analyze_ethernet_frame(file_dir,protocol_type)


    #sort the frame by frame number
    for key in ret.keys():
        keys_list.append(int(key))
    keys_list.sort()

    for key in keys_list:
        match_frame_list.append(ret.get(str(key)))
    print keys_list


    #get the line or lines contain IE_name
    for item in match_frame_list:
        try:
            if eval("item.%s.ProcedureCode_id"  %protocol_type) == message_type:
                item_dict = eval("item.%s.items"  %protocol_type)
                list_index = match_frame_list.index(item)
                list_index = keys_list[list_index]
                for info in ie_info:
                    item_name,ie_name = info.split('.')
                    for (key,value) in item_dict.items():
                        if '(' and ')' in ie_name:
                            ie_name = ie_name.replace('(','\(')
                            ie_name = ie_name.replace(')','\)')
                        if key == item_name :
                            lines = value.splitlines()
                            for line in lines:
                                pa = re.search('%s:\s(\w*.*)' %ie_name,line)
                                if pa:
                                    ie_value = pa.group(1)
                                    print ie_value
                                    value_list.append(info + ' = ' + ie_value)
                            #value_dict[str(keys_list[list_index]) + '.' + info] = value_list
                if (list_index,value_list) not in result_list and  len(value_list) >= ie_num:
                    result_list.append((list_index,value_list))
                value_list = []

        except AttributeError:
            pass
    if Flag == "Yes" and len(result_list) > 0:
        print result_list
        return result_list
    elif Flag == 'No' and len(result_list) >= location:
        ret_value = result_list[location]
        print ret_value
        return ret_value
    elif Flag == 'No' and len(result_list) < location:
        raise Exception, 'Location out of result_list,please check!'
    else:
        raise Exception, 'Protocol type,procdurecode-id,Item name or IE name is error,please check!'


def get_value_baseon_value_string(ie_value_string):
    value = re.match('.*\w+.*\s=\s(\w*.*)', ie_value_string).group(1)
    if value.endswith(')'):
        pa = '(.*\w*.*)\s\((\w+.*)\)'
        ret = re.match(pa,value).groups()
        return ret
    else:
        return value




if __name__ == '__main__':
    pass
"""
    ret = analyze_ethernet_frame('D:\\liepixie\\Desktop\\2.txt')
    print ret[0].ethernet.ip.udp.dhcp
    print ret[1].ethernet.ip.udp.dhcp
"""
