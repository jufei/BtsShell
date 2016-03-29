import re
import traceback

from BtsShell.helper import CommonItem, ParserException

GTP_MESSAGE_TYPE = {'0x01': 'Echo Request',
                    '0x02': 'Echo Response',
                    '0xff': 'G-PDU'
                   }

class Gtp(CommonItem):
    def __init__(self, udp_data):
        """
        GPRS Tunneling Protocol
            Flags: 0x32
                001. .... = Version: GTP release 99 version (1)
                ...1 .... = Protocol type: GTP (1)
                .... 0... = Reserved: 0
                .... .0.. = Is Next Extension Header present?: no
                .... ..1. = Is Sequence Number present?: yes
                .... ...0 = Is N-PDU number present?: no
            Message Type: Echo request (0x01)
            Length: 4
            TEID: 0x00000000
            Sequence number: 0x0008
            N-PDU Number: 0x00
            Next extension header type: No more extension headers (0x00)
        """
        self.flags = None
        self.message_type = None
        self.length = None
        self.teid = None
        self.sequence_number = None
        self.npdu_number = None
        self.parse_gtp_packet(udp_data)

    def parse_gtp_packet(self, udp_data):
        self.parse_gtp_header(udp_data.pop(0))
        self.parse_gtp_data(udp_data)

    def parse_gtp_header(self, gtp_header):
        try:
            self.flags = re.search('Flags:.*0x(\w+)', gtp_header, re.M).group(1)
            message_id = re.search('Message\s*Type:.*(0x\w+)', gtp_header, re.M).group(1)
            self.message_type = GTP_MESSAGE_TYPE[message_id]
            self.length = re.search('Length:\s*(\d+)', gtp_header, re.M).group(1)
            self.teid = re.search('TEID:\s*0x(\w+)', gtp_header, re.M).group(1)
        except:
            print 'gtp header:\n%s' % gtp_header
            traceback.print_exc()
            raise ParserException, 'parse_gtp_header failed'

        try: # these two attributes are optional
            self.sequence_number = re.search('Sequence\s*number:.*0x(\w+)', gtp_header, re.M).group(1)
            self.npdu_number = re.search('N-PDU\s*Number:.*0x(\w+)', gtp_header, re.M).group(1)
        except:
            pass

    def parse_gtp_data(self, gtp_data):
        self.data = gtp_data
