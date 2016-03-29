import re
import traceback

from BtsShell.helper import CommonItem, CommonDict, ParserException

MESSAGE_TYPE = {'1': 'Boot Request',
                '2': 'Boot Reply'
               }

class Dhcp(CommonItem):
    def __init__(self, udp_data):
        """
        Bootstrap Protocol
            Message type: Boot Reply (2)
            Hardware type: Ethernet
            Hardware address length: 6
            Hops: 0
            Transaction ID: 0x34499301
            Seconds elapsed: 0
            Bootp flags: 0x0000 (Unicast)
                0... .... .... .... = Broadcast flag: Unicast
                .000 0000 0000 0000 = Reserved flags: 0x0000
            Client IP address: 0.0.0.0 (0.0.0.0)
            Your (client) IP address: 10.68.160.15 (10.68.160.15)
            Next server IP address: 0.0.0.0 (0.0.0.0)
            Relay agent IP address: 0.0.0.0 (0.0.0.0)
            Client MAC address: NokiaSie_8b:ef:f8 (00:40:43:8b:ef:f8)
            Client hardware address padding: 00000000000000000000
            Server host name not given
            Boot file name not given
            Magic cookie: (OK)
            Option: (t=53,l=1) DHCP Message Type = DHCP Offer
                Option: (53) DHCP Message Type
                Length: 1
                Value: 02
            Option: (t=54,l=4) DHCP Server Identifier = 10.68.160.4
                Option: (54) DHCP Server Identifier
                Length: 4
                Value: 0A44A004
            Option: (t=51,l=4) IP Address Lease Time = 20 minutes
                Option: (51) IP Address Lease Time
                Length: 4
                Value: 000004B0
            Option: (t=1,l=4) Subnet Mask = 255.255.255.0
                Option: (1) Subnet Mask
                Length: 4
                Value: FFFFFF00
            Option: (t=28,l=4) Broadcast Address = 10.68.160.255
                Option: (28) Broadcast Address
                Length: 4
                Value: 0A44A0FF
            Option: (t=3,l=4) Router = 10.68.160.30
                Option: (3) Router
                Length: 4
                Value: 0A44A01E
            Option: (t=43,l=28) Vendor-Specific Information
                Option: (43) Vendor-Specific Information
                Length: 28
                Value: 0000000001040A4498C304040A0888F802040A0888F50604...
            End Option
        """
        self.operation = None
        self.hw_type = None
        self.hw_length = None
        self.hops = None
        self.transaction_id = None
        self.seconds_elapsed = None
        self.flags = None
        self.client_ip = None
        self.your_ip = None
        self.next_server_ip = None
        self.relay_agent_ip = None
        self.client_mac = None
        self.server_name = None
        self.boot_file_name = None
        self.options = CommonDict()
        self.parse_dhcp_packet(udp_data)

    def _split_options(self, options):
        lines = options.splitlines()
        temp_line = ''
        option_list = []
        for line in lines:
            if re.search('Option:\s*\(t=.*', line):
                if len(temp_line) != 0:
                    option_list.append(temp_line)
                temp_line = ''
            temp_line = temp_line + '\n' + line # DO NOT forget to add the new line
        option_list.append(temp_line)

        return option_list

    def parse_dhcp_packet(self, udp_data):
        dhcp_data = udp_data.pop(0)
        self.parse_dhcp_header(dhcp_data)
        options = self._split_options(dhcp_data)
        self.parse_dhcp_option(options)

    def parse_dhcp_header(self, dhcp_header):
        try:
            self.operation = re.search('Message\s*type:.*(\d+)', dhcp_header, re.M).group(1)
            self.hw_type = re.search('Hardware\s*type:.*(\w+)', dhcp_header, re.M).group(1)
            self.hw_length = re.search('Hardware\s*address\s*length:\s*(\d+)', dhcp_header, re.M).group(1)
            self.hops = re.search('Hops:\s*(\d+)', dhcp_header, re.M).group(1)
            self.transaction_id = re.search('Transaction\s*ID:.*0x(\w+)', dhcp_header, re.M).group(1)
            self.seconds_elapsed = re.search('Seconds\s*elapsed:\s*(\d+)', dhcp_header, re.M).group(1)
            self.flags = re.search('Bootp\s*flags:\s*(\w+)', dhcp_header, re.M).group(1)       
            self.client_ip = re.search('Client\s*IP\s*address:\s*(\d+\.\d+\.\d+\.\d+)', dhcp_header, re.M).group(1)
            self.your_ip = re.search('Your.*IP\s*address:\s*(\d+\.\d+\.\d+\.\d+)', dhcp_header, re.M).group(1)
            self.next_server_ip = re.search('Next\s*server\s*IP\s*address:\s*(\d+\.\d+\.\d+\.\d+)', dhcp_header, re.M).group(1)
            self.relay_agent_ip = re.search('Relay\s*agent\s*IP\s*address:\s*(\d+\.\d+\.\d+\.\d+)', dhcp_header, re.M).group(1)
            self.client_mac = re.search('Client\s*MAC\s*address:.*\((\w+:\w+:\w+:\w+:\w+:\w+)\)', dhcp_header, re.M).group(1)
        except:
            print 'dhcp header:\n%s' % dhcp_header
            traceback.print_exc()
            raise ParserException, 'parse_dhcp_header failed'

    def parse_dhcp_option(self, options):
        for option in options:
            dhcp_option = DhcpOption()
            try:
                dhcp_option.code = re.search('Option:\s*\((\d+)\)', option, re.M).group(1)
                dhcp_option.length = re.search('Length:\s*(\d+)', option, re.M).group(1)
                dhcp_option.value = re.search('Value:\s*(\d+)', option, re.M).group(1)
                self.options[dhcp_option.code] = dhcp_option
            except:
                pass

class DhcpOption(CommonItem):
    def __init__(self):
        """
        Option: (t=53,l=1) DHCP Message Type = DHCP Offer
            Option: (53) DHCP Message Type
            Length: 1
            Value: 02
        """
        self.code = None
        self.length = None
        self.value = None
