import re
import traceback
from S1ap import S1ap
from X2ap import X2ap
from BtsShell.helper import CommonItem, ParserException

SUPPORTED_SCTP_CHUNK = {'0': 'DATA',
                        '1': 'INIT',
                        '2': 'INIT_ACK',
                        '3': 'SACK',
                        '4': 'HEARTBEAT',
                        '5': 'HEARTBEAT_ACK',
                        '6': 'ABORT',
                        '7': 'SHUTDOWN',
                        '8': 'SHUTDOWN_ACK',
                        '9': 'ERROR',
                        '10': 'COOKIE_ECHO',
                        '11': 'COOKIE_ACK',
                        '12': 'ECNE',
                        '13': 'CWR',
                        '14': 'SHUTDOWN_COMPLETE'
                        }
SUPPORTED_SCTP_PAYLOAD_PROTOCOL = {'27': 'X2AP',
                                   '18': 'S1AP',
                                   }

SUPPORTED_SCTP_CHUNK_PARAMETERS = {'0x0005': ['IPV4_ADDRESS', 'IP Version 4 address:\s*([\d.]+)'],
                                   }

class SctpChunkParameter(CommonItem):
    def __init__(self):
        self.type_value = None
        self.type = None
        self.length = None
        self.value = None
        

class Sctp(CommonItem):
    def __init__(self, ip_data):
        """
        Stream Control Transmission Protocol, Src Port: 36412 (36412), Dst Port: 36412 (36412)
            Source port: 36412
            Destination port: 36412
            Verification tag: 0x00000000
            Checksum: 0xf2c1bb34 (not verified)
            INIT chunk (Outbound streams: 8, inbound streams: 8)
                Chunk type: INIT (1)
                    0... .... = Bit: Stop processing of the packet
                    .0.. .... = Bit: Do not report
                Chunk flags: 0x00
                Chunk length: 44
                Initiate tag: 0x44764af0
                Advertised receiver window credit (a_rwnd): 55296
                Number of outbound streams: 8
                Number of inbound streams: 8
                Initial TSN: 1840817703
                Supported address types parameter (Supported types: IPv4)
                    Parameter type: Supported address types (0x000c)
                        0... .... .... .... = Bit: Stop processing of chunk
                        .0.. .... .... .... = Bit: Do not report
                    Parameter length: 6
                    Supported address type: IPv4 address (5)
                    Parameter padding: 0000
                ECN parameter
                    Parameter type: ECN (0x8000)
                        1... .... .... .... = Bit: Skip parameter and continue processing of the chunk
                        .0.. .... .... .... = Bit: Do not report
                    Parameter length: 4
                Forward TSN supported parameter
                    Parameter type: Forward TSN supported (0xc000)
                        1... .... .... .... = Bit: Skip parameter and continue processing of the chunk
                        .1.. .... .... .... = Bit: Do report
                    Parameter length: 4
                Adaptation Layer Indication parameter (Indication: 0)
                    Parameter type: Adaptation Layer Indication (0xc006)
                        1... .... .... .... = Bit: Skip parameter and continue processing of the chunk
                        .1.. .... .... .... = Bit: Do report
                    Parameter length: 8
                    Indication: 0x00000000
        """
        self.source_port = None
        self.destination_port = None
        self.verification_tag = None
        self.checksum = None
        self.chunk_type = None
        self.chunk_flag = None
        self.chunk_length = None
        self.s1ap = None
        self.chunk_parameters = {}
        self.parse_sctp_segment(ip_data)
        

    def parse_sctp_segment(self, ip_data):
        self.parse_sctp_header(ip_data.pop(0))
        self.parse_sctp_data(ip_data)
        
    def parse_sctp_header(self, sctp_header):
        try:
            self.source_port = re.search('Source port:.*(\d+)', sctp_header, re.M).group(1)
            self.destination_port = re.search('Destination port:.*(\d+)', sctp_header, re.M).group(1)
            self.verification_tag = re.search('Verification tag:\s*(\w+)', sctp_header, re.M).group(1)
            self.checksum = re.search('Checksum:\s*(\d+)', sctp_header, re.M).group(1)
            self.chunk_type = SUPPORTED_SCTP_CHUNK[re.findall('Chunk type:\s+\w+\s*\((\d+)\)', sctp_header, re.M)[-1]]
            self.chunk_flag = re.search('Chunk flags:\s*0x(\w+)', sctp_header, re.M).group(1)
            self.chunk_length = re.search('Chunk length:\s*(\d+)', sctp_header, re.M).group(1)
            self.parse_sctp_chunk_parameters(sctp_header)
        except:
            print 'sctp header:\n%s' % sctp_header
            traceback.print_exc()
            raise ParserException, 'parse_sctp_header failed'

    def parse_sctp_chunk_parameters(self, sctp_header):
        if self.chunk_type == 'DATA':
            sctp_chunk_parameter = SctpChunkParameter()
            sctp_chunk_parameter.type = 'PAYLOAD_PROTOCOL_ID'
            sctp_chunk_parameter.value = SUPPORTED_SCTP_PAYLOAD_PROTOCOL[re.search('Payload protocol identifier:.*\((\d+)\)', sctp_header, re.M).group(1)]
            self.chunk_parameters[sctp_chunk_parameter.type] = sctp_chunk_parameter
            return
        
        parameter_list = self._split_sctp_chunk_parameters(sctp_header)

        for parameter in parameter_list:
            sctp_chunk_parameter = SctpChunkParameter()
            try:
                sctp_chunk_parameter.type_value = re.search('Parameter type:.*\((\w+)\)', parameter, re.M).group(1)
                sctp_chunk_parameter.length = re.search('Parameter length:.*\(\d+)', parameter, re.M).group(1)
            except:
                pass

            if sctp_chunk_parameter.type_value in SUPPORTED_SCTP_CHUNK_PARAMETERS.keys():
                sctp_chunk_parameter.type = SUPPORTED_SCTP_CHUNK_PARAMETERS[sctp_chunk_parameter.type_value][0]
                self._parse_chunk_parameter_value(parameter, sctp_chunk_parameter)
            else: # chunk parameter type is not supported, continue to next chunk parameter
                print '*DEBUG* SCTP: the chunk parameter %s is not supported' % sctp_chunk_parameter.type
                continue

            try:
                if sctp_chunk_parameter.type not in self.chunk_parameters.keys():
                    self.chunk_parameters[sctp_chunk_parameter.type] = []
                    self.chunk_parameters[sctp_chunk_parameter.type].append(sctp_chunk_parameter)
                else:
                    self.chunk_parameters[sctp_chunk_parameter.type].append(sctp_chunk_parameter)
            except KeyError:
                pass
              

    def _split_sctp_chunk_parameters(self, sctp_header):
        lines = sctp_header.splitlines()
        temp_line = ''
        parameter_list = []
        for line in lines:
            if re.match('^\s+[A-Z]+.*parameter', line): # any line starts with space and capitalized letter
                if len(temp_line) != 0:
                    parameter_list.append(temp_line)
                temp_line = ''
            temp_line = temp_line + '\n' + line # DO NOT forget to add the new line
        parameter_list.append(temp_line)

        return parameter_list[1:]

    def _parse_chunk_parameter_value(self, parameter_data, sctp_chunk_parameter):
        sctp_chunk_parameter.value = re.search(SUPPORTED_SCTP_CHUNK_PARAMETERS[sctp_chunk_parameter.type_value][-1],
                                               parameter_data, re.M).group(1)

    def parse_sctp_data(self, sctp_data):
        try:
            if self.chunk_type == 'DATA':
                if self.chunk_parameters['PAYLOAD_PROTOCOL_ID'].value == 'S1AP':
                    self.s1ap = S1ap(sctp_data)
                    #pass
                if self.chunk_parameters['PAYLOAD_PROTOCOL_ID'].value == 'X2AP':
                    self.x2ap = X2ap(sctp_data)
            else:
                print '*DEBUG* SCTP: the protocol %s is not supported' % self.chunk_parameters['PAYLOAD_PROTOCOL_ID'].value
                return
        except KeyError:
            pass
