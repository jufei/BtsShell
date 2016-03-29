import re
import traceback

from BtsShell.helper import CommonItem, ParserException

SUPPORTED_TCP_PORT = ['80', '8080', '21', '23']

class Tcp(CommonItem):
    def __init__(self, ip_data):
        """
        Transmission Control Protocol, Src Port: ssh (22), Dst Port: h323hostcallsc (1300), Seq: 83125, Ack: 53, Len: 212
            Source port: ssh (22)
            Destination port: h323hostcallsc (1300)
            [Stream index: 1]
            Sequence number: 83125    (relative sequence number)
            [Next sequence number: 83337    (relative sequence number)]
            Acknowledgement number: 53    (relative ack number)
            Header length: 20 bytes
            Flags: 0x18 (PSH, ACK)
                0... .... = Congestion Window Reduced (CWR): Not set
                .0.. .... = ECN-Echo: Not set
                ..0. .... = Urgent: Not set
                ...1 .... = Acknowledgement: Set
                .... 1... = Push: Set
                .... .0.. = Reset: Not set
                .... ..0. = Syn: Not set
                .... ...0 = Fin: Not set
            Window size: 81
            Checksum: 0x8bb5 [validation disabled]
                [Good Checksum: False]
                [Bad Checksum: False]
            [SEQ/ACK analysis]
                [Number of bytes in flight: 83336]
        """
        """
        Transmission Control Protocol, Src Port: ici (2200), Dst Port: mcreport (8003), Seq: 0, Len: 0
           Source port: ici (2200)
           Destination port: mcreport (8003)
           [Stream index: 0]
           Sequence number: 0    (relative sequence number)
           Header length: 40 bytes
           Flags: 0x02 (SYN)
               0... .... = Congestion Window Reduced (CWR): Not set
               .0.. .... = ECN-Echo: Not set
               ..0. .... = Urgent: Not set
               ...0 .... = Acknowledgement: Not set
               .... 0... = Push: Not set
               .... .0.. = Reset: Not set
               .... ..1. = Syn: Set
                   [Expert Info (Chat/Sequence): Connection establish request (SYN): server port mcreport]
                       [Message: Connection establish request (SYN): server port mcreport]
                       [Severity level: Chat]
                       [Group: Sequence]
               .... ...0 = Fin: Not set
           Checksum: 0xa0ad [validation disabled]
               [Good Checksum: False]
               [Bad Checksum: False]
           Options: (20 bytes)
               Maximum segment size: 1460 bytes
               SACK permitted
               Timestamps: TSval 357974, TSecr 0
               NOP
               Window scale: 4 (multiply by 16)
       """
        self.source_port = None
        self.destination_port = None
        self.sequence_number = None
        self.acknowledgement_number = None
        self.header_length = None
        self.flags = None
        self.window_size = None
        self.checksum = None
        self.parse_tcp_segment(ip_data)
        
    def parse_tcp_segment(self, ip_data):
        self.parse_tcp_header(ip_data.pop(0))
        self.parse_tcp_data(ip_data)

    def parse_tcp_header(self, tcp_header):
        try:
            self.source_port = re.search('Source port:.*\((\d+)\)', tcp_header, re.M).group(1)
            self.destination_port = re.search('Destination port:.*\((\d+)\)', tcp_header, re.M).group(1)
            self.sequence_number = re.search('Sequence number:\s*(\d+)', tcp_header, re.M).group(1)
            self.acknowledgement_number = re.search('Acknowledgement number:\s*(\d+)', tcp_header, re.M).group(1)
            self.header_length = re.search('Header length:\s*(\d+)', tcp_header, re.M).group(1)
            self.flags = re.search('Flags:\s*0x(\w+)', tcp_header, re.M).group(1)
            self.window_size = re.search('Window size:\s*(\d+)', tcp_header, re.M).group(1)
            self.checksum = re.search('Checksum:\s*0x(\w+)', tcp_header, re.M).group(1)
        except:
            try:
                self.source_port = re.search('Source port:.*\((\d+)\)', tcp_header, re.M).group(1)
                self.destination_port = re.search('Destination port:.*\((\d+)\)', tcp_header, re.M).group(1)
                self.sequence_number = re.search('Sequence number:\s*(\d+)', tcp_header, re.M).group(1)
                self.header_length = re.search('Header length:\s*(\d+)', tcp_header, re.M).group(1)
                self.flags = re.search('Flags:\s*0x(\w+)', tcp_header, re.M).group(1)
                self.checksum = re.search('Checksum:\s*0x(\w+)', tcp_header, re.M).group(1)
            except:
                print 'tcp segment:\n%s' % tcp_header
                traceback.print_exc()
                raise ParserException, 'parse_tcp_header failed'

    def parse_tcp_data(self, tcp_data):
        if self.destination_port not in SUPPORTED_TCP_PORT and \
           self.source_port not in SUPPORTED_TCP_PORT:
            print '*DEBUG* TCP: the TCP port (src: %s dest: %s) is not supported' % (self.source_port, self.destination_port)
            return
