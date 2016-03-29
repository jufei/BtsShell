import re
import traceback

from BtsShell.helper import CommonItem, ParserException
SUPPORTED_X2AP_PROCEDURE  = {'0' : 'initiatingMessage',
                             '1' : 'successfulOutcome',
                             '2' : 'unsuccessfulOutcome'
                             }
SUPPORTED_X2AP_TYPE =  {'0' : 'handoverPreparation',
                        '1' : 'handoverCancel',
                        '2' : 'LoadIndication',
                        '3' : 'errorIndication',
                        '4' : 'snStatusTransfer',
                        '5' : 'uEContextRelease',
                        '6' : 'X2 Setup',
                        '7' : 'Reset',
                        '8' : 'NBConfigurationUpdate',
                        '9' : 'Resource Status Reporting Initiation',
                        '10' : 'Resource Status Reporting',
                        '11' : 'Private Message',
                        '12' : 'Mobility Settings Change',
                        '13' : 'Radio Link Failure Indication',
                        '14' : 'HandoverReport',
                        '15' : 'CellActivation'
                        }


class X2ap(CommonItem):
    def __init__(self, ip_data):
        """
    EUTRAN X2 Application Protocol (X2AP)
    X2AP-PDU: initiatingMessage (0)
        initiatingMessage
            procedureCode: id-uEContextRelease (5)
            criticality: ignore (1)
            value
                UEContextRelease
                    protocolIEs: 2 items
                        Item 0: id-Old-eNB-UE-X2AP-ID
                            ProtocolIE-Field
                                id: id-Old-eNB-UE-X2AP-ID (10)
                                criticality: reject (0)
                                value
                                    UE-X2AP-ID: 2035
                        Item 1: id-New-eNB-UE-X2AP-ID
                            ProtocolIE-Field
                                id: id-New-eNB-UE-X2AP-ID (9)
                                criticality: reject (0)
                                value
                                    UE-X2AP-ID: 2475
        """
        self.X2AP_PDU = None
        self.procedureCode = None
        self.parse_X2AP_segment(ip_data.pop(0))

    def parse_X2AP_segment(self, ip_data):
        X2AP_info = self._split_X2AP(ip_data)
        self.parse_X2AP_header(X2AP_info[0])
        self.parse_X2AP_data(X2AP_info[-1])

    def parse_X2AP_header(self,ip_data):
        try:
            self.X2APPdu_id = re.search('X2AP-PDU:.*\((\d+)\)', ip_data, re.M).group(1)
            self.ProcedureCode_id = re.search('procedureCode:.*\((\d+)\)', ip_data, re.M).group(1)

        except:
            raise ParserException, 'parse_X2AP_header failed'

    def parse_X2AP_data(self,ip_data):
        items_dict = self._parse_items(ip_data)
        self.items = items_dict

    def _parse_items(self,X2AP_data):
        items_list = []
        lines = X2AP_data.splitlines()
        temp_line = ''
        item_dirc = {}
        title_list = []

        try:
            for line in lines:
                if re.search('(\s)Item 0:.*',line):
                    temp_list = line.split("Item 0")
                    start_space_num = len(temp_list[0])
                    item_tilte = re.match('.*Item.*(\d):.*id-(\w+.*)',line).group(2)
                    title_list.append(item_tilte)
                    break

            for line in lines:
                if re.search('Item.*(\d):.*',line):
                    num = int(re.match('.*Item.*(\d):.*',line).group(1))
                    temp_list = line.split("Item %s" %num)
                    space_num = len(temp_list[0])
                    
                    if space_num == start_space_num :
                        item_tilte = re.match('.*Item.*(\d).*id-(\w+.*)',line).group(2)
                        if item_tilte not in title_list:
                            title_list.append(item_tilte)
                        #print title_list
                        
                        
                    if len(temp_line) !=0 and space_num ==  start_space_num :
                        items_list.append(temp_line)
                        temp_line = ''
                temp_line =  temp_line +  line + '\n'

            items_list.append(temp_line)
            len1 = len(items_list)
            len2 = len(title_list)
            #print len1,len2
            
            try:
                if len1 == len2 :
                    for index in xrange(len1):
                        item_dirc[title_list[index]] = items_list[index]
            except:
                raise 'have wrong list!'
            return item_dirc
        except:
            raise 'the wrong when parse items!'


    def _split_X2AP(self,ip_data):
        item_info = []
        lines = ip_data.splitlines()
        temp_line = ''
        
        try:
            for line in lines:
                temp_line = temp_line + line + '\n'
                if re.search('protocolIEs:.*(\d).*',line):
                    if len(temp_line) != 0:
                        item_info.append(temp_line)
                    temp_line = ''
            item_info.append(temp_line)
            return item_info
        except:
            raise 'have some prolems!'
