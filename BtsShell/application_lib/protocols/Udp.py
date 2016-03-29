import re
import traceback

from BtsShell.helper import CommonItem, ParserException
from Gtp import Gtp
from Dhcp import Dhcp

SUPPORTED_UDP_PORT = ['53', '2152', '67', '68']

class Udp(CommonItem):
    def __init__(self, ip_data):
        """
        User Datagram Protocol, Src Port: mdns (5353), Dst Port: mdns (5353)
            Source port: mdns (5353)
            Destination port: mdns (5353)
            Length: 95
            Checksum: 0x182b [validation disabled]
                [Good Checksum: False]
                [Bad Checksum: False]
        """
        self.source_port = None
        self.destination_port = None
        self.length = None
        self.checksum = None
        self.parse_udp_datagram(ip_data)

    def parse_udp_datagram(self, ip_data):
        self.parse_udp_header(ip_data.pop(0))
        self.parse_udp_data(ip_data)

    def parse_udp_header(self, udp_header):
        try:
            self.source_port = re.search('Source port:.*\((\d+)\)', udp_header, re.M).group(1)
            self.destination_port = re.search('Destination port:.*\((\d+)\)', udp_header, re.M).group(1)
            self.length = re.search('Length:\s*(\w+)', udp_header, re.M).group(1)
            self.checksum = re.search('Checksum:\s*0x(\w+)', udp_header, re.M).group(1)
        except:
            print 'udp datagram:\n%s' % udp_header
            traceback.print_exc()
            raise ParserException, 'parse_udp_header failed'

    def parse_udp_data(self, udp_data):
        if self.destination_port not in SUPPORTED_UDP_PORT and \
           self.source_port not in SUPPORTED_UDP_PORT:
            print '*DEBUG* UDP: the UDP port (src: %s dest: %s) is not supported' % (self.source_port, self.destination_port)
            return
        if self.destination_port == '53': # DNS
            print 'this is DNS'
            #self.dns = Dns(udp_data)
        if self.destination_port == '2152':
            self.gtp= Gtp(udp_data)
        if self.destination_port == '67' or self.destination_port == '68':
            self.dhcp = Dhcp(udp_data)
