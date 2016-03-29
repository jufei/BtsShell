import re
import traceback

from BtsShell.helper import CommonItem, ParserException


class Icmp(CommonItem):
    def __init__(self, ip_data):
        """
        Internet Control Message Protocol
            Type: 8 (Echo (ping) request)
            Code: 0 ()
            Checksum: 0xfc5a [correct]
            Identifier: 0x0200
            Sequence number: 20225 (0x4f01)
            Data (32 bytes)

        0000  61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70   abcdefghijklmnop
        0010  71 72 73 74 75 76 77 61 62 63 64 65 66 67 68 69   qrstuvwabcdefghi
                Data: 6162636465666768696A6B6C6D6E6F707172737475767761...
                [Length: 32]
        """
        self.type = None
        self.code = None
        self.checksum = None
        self.identifier = None
        self.sequence_number = None
        self.data = None
        self.parse_icmp_packet(ip_data.pop(0))
        
    def parse_icmp_packet(self, icmp_packet):
        self.parse_icmp_header(icmp_packet)
        self.parse_icmp_data(icmp_packet)

    def parse_icmp_header(self, icmp_packet):
        try:
            self.type = re.search('Type:\s*(\d+)', icmp_packet, re.M).group(1)
            self.code = re.search('Code:\s*(\d+)', icmp_packet, re.M).group(1)
            self.checksum = re.search('Checksum:\s*0x(\w+)', icmp_packet, re.M).group(1)          
        except:
            print 'icmp packet:\n%s' % icmp_packet
            traceback.print_exc()
            raise ParserException, 'parse_icmp_header failed'

        # for ICMP packet with type 3 (destination unreachable)
        try:
            self.identifier = re.search('Identifier:\s*(\d+)', icmp_packet, re.M).group(1)
            self.sequence_number = re.search('Sequence number:\s*(\d+)', icmp_packet, re.M).group(1)
        except:
            pass

    def parse_icmp_data(self, icmp_packet):
        icmp_data = ''
        for line in icmp_packet.splitlines():
            if re.match('^\d+', line):
                icmp_data = icmp_data + line.split()[-1]
        self.data = icmp_data          
