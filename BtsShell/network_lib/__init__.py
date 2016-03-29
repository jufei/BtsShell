from BtsShell import connections
import re, os
import time

# try:
#     from network_config import *
# except Exception, e:
#     print 'import network_config failed: %s' % e
#     pass

#from TcpIp import TcpIps

from Pinger import BackgroundPinger
BgPing = BackgroundPinger()

def Bg_ping_start(host, options):
    """This keyword is for backgroud ping
    | Input Parameters          | Man. | Description |
    | host                      | Yes  | Host IP address |
    | options                   | No   | Options for ping command such as "-n 10 -l 1024" |
    Example
    | switch host connection    | ${TM500 CONTROL PC CONNECTION} |          |
    | Bg_ping_start             | 10.68.152.34                   | -n 10    |
    | Do other things           | arg1                           | arg2     |
    | Bg_ping_stop              |                                |
    | ${result}                 | Bg_get_ping_result             |
    """
    BgPing.start_traffic(host, options)

def Bg_ping_stop():
    """This keyword is used with "Bg ping start", it just stop ping process .
     see Bg_ping_start for example.
    """
    BgPing.stop_traffic()

def Bg_get_ping_result():
    """This keyword is used with "Bg ping start" and "Bg ping stop", it is used for get the ping result.
     see Bg_ping_start for example.
    | return value                                               |
    | ([sends, recvs, losts], [max_delay, min_delay, avg_delay]) |
    """
    return BgPing.analyse_result()

def ping_remote_system(host, options="", ignore=""):
    """This keyword test the reachability of remote system.

    | Input Parameters          | Man. | Description |
    | host                      | Yes  | Host IP address |
    | options                   | No   | Options for ping command such as "-n 10 -l 1024" |
    | ping delay statistics     | No   | default or sample as ":1" or "5:" or "5:10" |

    | Return Value 1 | a list contains three values which indicate sent/received/lost packagets |
    | ${package_summary[0]}   | send package count |
    | ${package_summary[1]}   | receive package count |
    | ${package_summary[2]}   | lost package count |
    | Return Value 2 | a list contains three values which indicate max/min/average ping delay |
    | ${ping_delay[0]}   | max ping delay |
    | ${ping_delay[1]}   | min ping delay |
    | ${ping_delay[2]}   | average ping delay |

    Example
    | ${package_summary} | ${ping_delay}  | Ping Remote System | 192.168.255.1 |
    | should be true | ${package_summary[2]}<3 | #lost package should be less than 3 |
    | ${package_summary} | ${ping_delay}  | Ping Remote System | 192.168.255.1 | -n 10 | :1 |
    | should be true | ${ping_delay[2]}<100 | #first ping delay should be less than 100ms |
    | ${package_summary} | ${ping_delay}  | Ping Remote System | 192.168.255.1 | -n 10 | 5: |
    | should be true | ${ping_delay[2]}<100 | #ping delay except the top 5 should be less than 100ms |

    """
    connection_type = connections.get_current_connection_type()

##    option_list = ''
##    for option in options:
##        option_list = option_list + option + ' '
    ret = connections.execute_shell_command_without_check('ping %s %s' % (options, host))
    time_delay = []
    delay_max_min_avg = []
    statistic_delay = []
    if connection_type == 'Windows':
        lines = ret.split(os.linesep)
        delay_pattern1 = re.compile(r'(?i).*Reply from.*?time=(\d+)ms.*')
        delay_pattern2 = re.compile(r'(?i).*Reply from.*?time<(\d+)ms.*')
        for line in lines:
            if re.match(r'(?i).*Reply from.*?time.*(\d+)ms.*', line):
                time = delay_pattern1.match(line)
                if time:
                    tmp = time.groups()[0]
                    time_delay.append(int(tmp))
                else:
                    time = delay_pattern2.match(line)
                    if time:
                        tmp = time.groups()[0]
                        time_delay.append(int(tmp))
                    else:
                        time_delay.append(-1)
            else:
                result = re.search('.*Sent\s*=\s*(\d*).*Received\s*=\s*(\d*).*Lost\s*=\s*(\d*)', line)
                if result:
                    summary_result = result.groups()
        print "Total ping delay is:",time_delay

        if ""==ignore:
            statistic_delay = time_delay
        else:
            (start,end) = ignore.split(":")
            if ""==start:
                start = 0
            else:
                start = int(start)

            if ""==end:
                end = len(time_delay)
            else:
                end = int(end)

            for i in range(start,end):
                statistic_delay.append(time_delay[i])
        print "Statistic ping delay is:",statistic_delay

        invalid = statistic_delay.count(-1)
        for i in range(invalid):
            statistic_delay.remove(-1)
        print "Valid ping delay is:",statistic_delay


        if 0 < len(statistic_delay):
            list_max = max(statistic_delay)
            list_min = min(statistic_delay)
            list_avg = float(sum(statistic_delay))/float(len(statistic_delay))
            delay_max_min_avg.append(list_max)
            delay_max_min_avg.append(list_min)
            delay_max_min_avg.append(list_avg)
        else:
            delay_max_min_avg = [0,0,0]

    if connection_type == 'Linux':
        if line.find('packets') > 0:
            '4 packets transmitted, 0 received, 100% packet loss, time 3000ms'
            result = re.search('(\d+)\s*packets transmitted.*(\d+)\s*received', line)

    return (summary_result, delay_max_min_avg)

def ping_delay(host):
    """This keyword test the average Ping delay.

    | Input Parameters | Man. | Description |
    | host             | Yes  | Host IP address |

    | Return Value | a list contains three values which indicate Minimum/Maximum/Average time |

    Example
    | ${ping_result}  | Ping Delay | 10.68.149.182 -l 100/200/500 -n 50 |
    | Should Be True | ${ping_result[-1]} < 13 |
    """
    ret = connections.execute_shell_command_without_check('ping %s' % host)
    lines = ret.splitlines()
    for line in lines:
        if line.find('Minimum') > 0:
            result = re.search('^.*Minimum = (\d*)ms, Maximum = (\d*)ms, Average = (\d*)ms', line)
            return result.groups()

def stop_firewall():
    """This keyword stops PC firewall.

    | Input Parameters | Man. | Description |

    Example
    | Stop Firewall |
    """
    connections.execute_shell_command('sc stop TmPfw')

def wait_until_units_startup(timeout = '30', *units):
    """This keyword tests the reachability of given unit/units.

    | Input Parameters | Man. | Description |
    | timeout          | No   | Timeout for 'Ping' command', default is set to 30 sec |
    | *units           | No   | Units list which is for test |

    Example
    | Wait Until Units Startup | 600 | 192.168.255.1 | 192.168.255.129 |
    """
    not_ready_units = list(units)
    ready_units = []
    ping_time_interval = 10 # ping all units every 10 seconds
    time_is_up = int(timeout)

    while len(not_ready_units) != 0 and time_is_up > 0:
        start_ping_time = time.time() # get start ping time

        for unit in not_ready_units:
            ping_result = ping_remote_system(unit)
            if ping_result[0][2] == '0': # ping OK which means unit is ready
                ready_units.append(unit)

        # remove units which is already ping successfully
        for ready_unit in ready_units:
            try:
                not_ready_units.remove(ready_unit)
            except ValueError:
                pass
        ready_units = [] # empty the ready_units

        end_ping_time = time.time() # get end ping time
        consume_ping_time = int(end_ping_time - start_ping_time)
        time_is_up = time_is_up - consume_ping_time
        time.sleep(ping_time_interval)

    if len(not_ready_units) != 0: # still some units are not ready
        raise Exception, 'there are still some units (%s) not in working state' % not_ready_units

def get_pppoe_connection_ip_address():
    ret = connections.execute_shell_command_without_check('ipconfig')

    pppoe_connection_start = False

    lines = ret.splitlines()
    for line in lines:
        if line.find('PPP') >= 0:
            pppoe_connection_start = True
        if line.find('Address') >= 0 and pppoe_connection_start:
            pppoe_connection_ip_address = line.split(':')[-1].strip()
            break

    try:
        return pppoe_connection_ip_address
    except NameError:
        raise Exception, 'no any PPPoE connection found'

def get_multi_pppoe_connection_ip_address():
    pppoe_connection_ip_address = []
    ret = connections.execute_shell_command_without_check('ipconfig')

    pppoe_connection_start = False

    lines = ret.splitlines()
    for line in lines:
        if line.find('PPP') >= 0:
            pppoe_connection_start = True
        if line.find('Address') >= 0 and pppoe_connection_start:
            tmp = line.split(':')[-1].strip()
            print tmp
            pppoe_connection_start = False
            pppoe_connection_ip_address.append(tmp)

    if 0 == len(pppoe_connection_ip_address):
        raise Exception, 'no any PPPoE connection found'
    try:
        return pppoe_connection_ip_address
    except NameError:
        raise Exception, 'no any PPPoE connection found'


if __name__ == '__main__':
    connections.connect_to_host('10.69.71.114', '23', 'tdlte-tester', 'btstest')
    Bg_ping_start("10.69.71.115", "-n 10")
    time.sleep(5)
    Bg_ping_stop()
    print Bg_get_ping_result()
