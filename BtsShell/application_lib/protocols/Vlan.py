import re
import traceback

from BtsShell.helper import CommonItem, ParserException
from Ip import Ip
#from Arp import Arp
#from Llc import Llc


SUPPORTED_PROTOCOL = {'0x0806': 'ARP',
                      '0x0800': 'IP'}

class Vlan(CommonItem):
    def __init__(self, ethernet_data):
        """
        802.1Q Virtual LAN, PRI: 0, CFI: 0, ID: 401
            000. .... .... .... = Priority: 0
            ...0 .... .... .... = CFI: 0
            .... 0001 1001 0001 = ID: 401
            Type: ARP (0x0806)
            Trailer: 000000000000000000000000000000000000
        """
        self.priority = None
        self.cfi = None
        self.id = None
        self.type = 'LLC'
        self.parse_vlan_header(ethernet_data.pop(0))
        self.parse_vlan_data(ethernet_data)

    def parse_vlan_header(self, vlan_header):
        try:
            self.priority = re.search('Priority:.*(\d+)', vlan_header, re.M).group(1)
            self.cfi = re.search('CFI:\s*(\d+)', vlan_header, re.M).group(1)
            self.id = re.search('ID:\s*(\d+)', vlan_header, re.M).group(1)
        except:
            print 'vlan header:\n%s' % vlan_header
            traceback.print_exc()
            raise ParserException, 'parse_vlan_header failed'

        try:
            type_value = re.search('Type:.*\((.*)\)', vlan_header, re.M).group(1)
            self.type = SUPPORTED_PROTOCOL[type_value]
        except:
            pass


    def parse_vlan_data(self, vlan_data):
        if self.type not in SUPPORTED_PROTOCOL.values():
            print '*DEBUG* VLAN: the protocol %s is not supported' % self.type
            return
        if self.type == 'IP':
            self.ip = Ip(vlan_data)
        if self.type == 'ARP':
            print 'this is ARP'
            #self.arp = Arp(vlan_data)
        if self.type == 'LLC':
            print 'this is LLC'
            #self.llc = Llc(vlan_data)

