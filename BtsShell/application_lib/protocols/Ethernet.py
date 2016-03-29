import re
import traceback

from BtsShell.helper import CommonItem, ParserException
from Ip import Ip
from Vlan import Vlan

SUPPORTED_PROTOCOL = {'0x0800': 'IP',
                      '0x8100': 'VLAN'}
#SUPPORTED_PROTOCOL = ['IP', 'VLAN']
           
class Ethernet(CommonItem):
    def __init__(self, frame_data):
        """
        Ethernet II, Src: HewlettP_c3:8d:00 (00:17:a4:c3:8d:00), Dst: Dell_c3:bf:b8 (a4:ba:db:c3:bf:b8)
            Destination: Dell_c3:bf:b8 (a4:ba:db:c3:bf:b8)
                Address: Dell_c3:bf:b8 (a4:ba:db:c3:bf:b8)
                .... ...0 .... .... .... .... = IG bit: Individual address (unicast)
                .... ..0. .... .... .... .... = LG bit: Globally unique address (factory default)
            Source: HewlettP_c3:8d:00 (00:17:a4:c3:8d:00)
                Address: HewlettP_c3:8d:00 (00:17:a4:c3:8d:00)
                .... ...0 .... .... .... .... = IG bit: Individual address (unicast)
                .... ..0. .... .... .... .... = LG bit: Globally unique address (factory default)
            Type: IP (0x0800)
        """
        """
        IEEE 802.3 Ethernet 
            Destination: NETBIOS- (03:00:00:00:00:01)
                Address: NETBIOS- (03:00:00:00:00:01)
                .... ...1 .... .... .... .... = IG bit: Group address (multicast/broadcast)
                .... ..1. .... .... .... .... = LG bit: Locally administered address (this is NOT the factory default)
            Source: Fuji-Xer_82:34:19 (08:00:37:82:34:19)
                Address: Fuji-Xer_82:34:19 (08:00:37:82:34:19)
                .... ...0 .... .... .... .... = IG bit: Individual address (unicast)
                .... ..0. .... .... .... .... = LG bit: Globally unique address (factory default)
            Length: 192
        """
        self.source_mac = None
        self.destination_mac = None
        self.type = None
        self.parse_ethernet_header(frame_data.pop(0))
        self.parse_ethernet_data(frame_data)

    def parse_ethernet_header(self, ethernet_header):
        try:
            self.source_mac = re.search('Source:.*?\(([a-zA-Z0-9:]+)\)', ethernet_header, re.M).group(1)
            self.destination_mac = re.search('Destination:.*?\(([a-zA-Z0-9:]+)\)', ethernet_header, re.M).group(1)
            type_value = re.search('Type:.*\((.*)\)', ethernet_header, re.M).group(1)
            self.type = SUPPORTED_PROTOCOL[type_value]
        except:
            try:
                self.source_mac = re.search('Source:.*?\(([a-zA-Z0-9:]+)\)', ethernet_header, re.M).group(1)
                self.destination_mac = re.search('Destination:.*?\(([a-zA-Z0-9:]+)\)', ethernet_header, re.M).group(1)
                self.type = 'LLC'
            except Exception, data:
                print 'ethernet header:\n%s' % ethernet_header
                traceback.print_exc()
                raise ParserException, 'parse_ethernet_header failed'

    def parse_ethernet_data(self, ethernet_data):
        if self.type not in SUPPORTED_PROTOCOL.values():
            print '*DEBUG* Ethernet: the protocol %s is not supported' % self.type
            return
        if self.type == 'IP':
            self.ip = Ip(ethernet_data)
        if self.type == 'VLAN':
            self.vlan = Vlan(ethernet_data)
