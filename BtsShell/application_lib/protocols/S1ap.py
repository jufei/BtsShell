import re
import traceback

from BtsShell.helper import CommonItem, ParserException
SUPPORTED_S1AP_PROCEDURE  = {'0' : 'initiatingMessage',
                             '1' : 'successfulOutcome',
                             '2' : 'unsuccessfulOutcome'
                             }
SUPPORTED_S1AP_TYPE =  {'0' : 'HandoverPreparation',
                        '1' : 'HandoverResourceAllocation',
                        '2' : 'HandoverNotification',
                        '3' : 'PatchSwitchRequest',
                        '4' : 'HandoverCancellation',
                        '5' : 'E-RABSetup',
                        '6' : 'E-RABModify',
                        '7' : 'E-RABRelease',
                        '8' : 'E-RABReleaseIndication',
                        '9' : 'InitialContextSetup',
                        '10' : 'Paging',
                        '11' : 'DownlinkNAStransport',
                        '12' : 'initialUEMessage',
                        '13' : 'uplinkNAStransport',
                        '14' : 'Reset',
                        '15' : 'ErrorIndication',
                        '16' : 'NASNonDeliveryIndication',
                        '17' : 'S1Setup',
                        '18' : 'UEContextReleaseRequest',
                        '19' : 'DownlinkS1CDMA2000Tunneling',
                        '20' : 'UplinkS1CDMA2000Tunneling',
                        '21' : 'UEContextModification',
                        '22' : 'UECapabilityInfoIndication',
                        '23' : 'UEContextRelease'
                        }


class S1ap(CommonItem):
    def __init__(self, ip_data):
        """
    S1 Application Protocol
    S1AP-PDU: initiatingMessage (0)
      initiatingMessage
        procedureCode: id-S1Setup (17)
        criticality: reject (0)
        value
        S1SetupRequest
            protocolIEs: 2 items
            Item 0: id-Global-ENB-ID
                ProtocolIE-Field
                id: id-Global-ENB-ID (59)
                criticality: reject (0)
                value
                    Global-ENB-ID
                    pLMNidentity: 62f230
                    Mobile Country Code (MCC): Germany (Federal Republic of) (262)
                    Mobile Network Code (MNC): E-Plus Mobilfunk GmbH & Co. KG (03)
                    eNB-ID: macroENB-ID (0)
                    macroENB-ID: 00002e [bit length 20, 4 MSB pad bits, .... 0000  0000 0000  0010 0000 decimal value 32]
            Item 1: id-eNBname
                ProtocolIE-Field
                  id: id-eNBname (60)
                  criticality: ignore (1)
                  value
                    0... .... Extension Present Bit: False
                    ENBname: Chevrolet
        """
        self.S1AP_PDU = None
        self.procedureCode = None
        self.parse_s1ap_segment(ip_data.pop(0))

    def parse_s1ap_segment(self, ip_data):
        s1ap_info = self._split_s1ap(ip_data)
        self.parse_s1ap_header(s1ap_info[0])
        self.parse_s1ap_data(s1ap_info[-1])

    def parse_s1ap_header(self,ip_data):
        try:
            self.S1apPdu_id = re.search('S1AP-PDU:.*\((\d+)\)', ip_data, re.M).group(1)
            self.ProcedureCode_id = re.search('procedureCode:.*\((\d+)\)', ip_data, re.M).group(1)

        except:
            raise ParserException, 'parse_s1ap_header failed'

    def parse_s1ap_data(self,ip_data):
        items_dict = self._parse_items(ip_data)
        self.items = items_dict

    def _parse_items(self,s1ap_data):
        items_list = []
        lines = s1ap_data.splitlines()
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
                if re.match('.*Item\s+(\d):.*',line):
                    num = int(re.match('.*Item.*(\d):.*',line).group(1))
                    temp_list = line.split("Item %s" %num)
                    space_num = len(temp_list[0])
                    
                    if space_num == start_space_num :
                        item_tilte = re.match('.*Item\s*(\d).*id-(\w+.*)',line).group(2)
                        if item_tilte not in title_list:
                            title_list.append(item_tilte)
                        
                        
                    if len(temp_line) !=0 and space_num ==  start_space_num :
                        items_list.append(temp_line)
                        temp_line = ''
                temp_line =  temp_line +  line + '\n'

            items_list.append(temp_line)
            len1 = len(items_list)
            len2 = len(title_list)
            
            try:
                if len1 == len2 :
                    for index in xrange(len1):
                        item_dirc[title_list[index]] = items_list[index]
            except:
                raise 'have wrong list!'
            return item_dirc
        except:
            raise 'the wrong when parse items!'


    def _split_s1ap(self,ip_data):
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
