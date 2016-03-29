import re
import traceback

from BtsShell.helper import CommonItem, ParserException
from Icmp import Icmp
from Udp import Udp
from Tcp import Tcp
from Sctp import Sctp

SUPPORTED_PROTOCOL = ['ICMP', 'TCP', 'UDP', 'SCTP']

class Ip(CommonItem):
    def __init__(self, ethernet_data):
        """
        Internet Protocol, Src: 10.68.136.161 (10.68.136.161), Dst: 10.140.19.82 (10.140.19.82)
            Version: 4
            Header length: 20 bytes
            Differentiated Services Field: 0x00 (DSCP 0x00: Default; ECN: 0x00)
                0000 00.. = Differentiated Services Codepoint: Default (0x00)
                .... ..0. = ECN-Capable Transport (ECT): 0
                .... ...0 = ECN-CE: 0
            Total Length: 1300
            Identification: 0x7ecc (32460)
            Flags: 0x02 (Don't Fragment)
                0.. = Reserved bit: Not Set
                .1. = Don't fragment: Set
                ..0 = More fragments: Not Set
            Fragment offset: 0
            Time to live: 60
            Protocol: TCP (0x06)
            Header checksum: 0x0a55 [correct]
                [Good: True]
                [Bad : False]
            Source: 10.68.136.161 (10.68.136.161)
            Destination: 10.140.19.82 (10.140.19.82)
        """
        """
        Internet Protocol Version 6
            0110 .... = Version: 6
                [0110 .... = This field makes the filter "ip.version == 6" possible: 6]
            .... 0000 0000 .... .... .... .... .... = Traffic class: 0x00000000
            .... .... .... 0000 0000 0000 0000 0000 = Flowlabel: 0x00000000
            Payload length: 32
            Next header: ICMPv6 (0x3a)
            Hop limit: 255
            Source: fe80::21c:25ff:fe20:4df7 (fe80::21c:25ff:fe20:4df7)
            Destination: ff02::1:ffe4:a540 (ff02::1:ffe4:a540)
        """
        self.version = None
        self.header_length = None
        self.tos = None
        self.dscp = None
        self.total_length = None
        self.identification = None
        self.flags = None
        self.fragment_offset = None
        self.ttl = None
        self.protocol = None
        self.checksum = None
        self.source_ip = None
        self.destination_ip = None
        self.parse_ip_header(ethernet_data.pop(0))
        self.parse_ip_data(ethernet_data)

    def parse_ip_header(self, ip_header):
        try:
            self.version = re.search('Version:\s*(\d+)', ip_header, re.M).group(1)
            self.header_length = re.search('Header length:\s*(\d+)', ip_header, re.M).group(1)
            self.tos = re.search('Differentiated Services Field:\s*0x(\w+)', ip_header, re.M).group(1)
            self.dscp = re.search('Differentiated Services Codepoint:\s*.*0x(\w+)', ip_header, re.M).group(1)
            self.total_length = re.search('Total Length:\s*(\d+)', ip_header, re.M).group(1)
            self.identification = re.search('Identification:\s*\w*\s*\((\d+)\)', ip_header, re.M).group(1)
            self.flags = re.search('Flags:\s*0x(\d+)', ip_header, re.M).group(1)
            self.fragment_offset = re.search('Fragment offset:\s*(\d+)', ip_header, re.M).group(1)
            self.ttl = re.search('Time to live:\s*(\d+)', ip_header, re.M).group(1)
            self.protocol = re.search('Protocol:\s*(\w+)', ip_header, re.M).group(1)
            self.checksum = re.search('Header checksum:\s*(\w+)', ip_header, re.M).group(1)
            self.source_ip = re.search('Source:\s*([\d.]+)', ip_header, re.M).group(1)
            self.destination_ip = re.search('Destination:\s*([\d.]+)', ip_header, re.M).group(1)
        except:
            print 'ip header:\n%s' % ip_header
            traceback.print_exc()
            raise ParserException, 'parse_ip_header failed'


    def parse_ip_data(self, ip_data):
        if self.protocol not in SUPPORTED_PROTOCOL:
            print '*DEBUG* IP: the protocol %s is not supported' % self.protocol
            return
        if self.protocol == 'ICMP':
            self.icmp = Icmp(ip_data)
        if self.protocol == 'UDP':
            self.udp = Udp(ip_data)
        if self.protocol == 'TCP':
            self.tcp = Tcp(ip_data)
        if self.protocol == 'SCTP':
            self.sctp = Sctp(ip_data)

