import re
import traceback

from BtsShell.helper import CommonDict, CommonItem, ParserException
from Ethernet import Ethernet

class Frames(CommonDict):
    def __init__(self, frames):
        for frame in frames:
            try:
                ethernet_frame = Frame(frame)
                self[ethernet_frame.number] = ethernet_frame
            except ParserException:
                if frame == frames[-1]:
                    pass
                else:
                    raise Exception, 'parse ethernet frame failed, \n%s' % frame
            
class Frame(CommonItem):
    def __init__(self, frame):
        """
        Frame 1 (1314 bytes on wire, 1314 bytes captured)
            Arrival Time: Feb 16, 2011 11:09:08.938868000
            [Time delta from previous captured frame: 0.000000000 seconds]
            [Time delta from previous displayed frame: 0.000000000 seconds]
            [Time since reference or first frame: 0.000000000 seconds]
            Frame Number: 1
            Frame Length: 1314 bytes
            Capture Length: 1314 bytes
            [Frame is marked: False]
            [Protocols in frame: eth:ip:tcp:vnc]
        """
        protocol_list = self.split_protocol(frame)

        self.number = None
        self.length = None
        self.protocol = None
        self.parse_frame(protocol_list.pop(0))
        self.ethernet = Ethernet(protocol_list)

    def split_protocol(self, strings):
        lines = strings.splitlines()
        temp_line = ''
        protocol_list = []
        for line in lines:
            if re.match('^[a-zA-Z0-9]+', line): # any line starts with alph
                if len(temp_line) != 0:
                    protocol_list.append(temp_line)
                temp_line = ''
            temp_line = temp_line + '\n' + line # DO NOT forget to add the new line
        protocol_list.append(temp_line)

        return protocol_list
        
        
    def parse_frame(self, frame_data):
        try:
            self.number = re.search('Frame Number:\s*(\d+)', frame_data, re.M).group(1)
            self.length = re.search('Frame Length:\s*(\d+)', frame_data, re.M).group(1)
            self.protocol = re.search('Protocols in frame\s*\w*:\s*([A-Za-z:]+)', frame_data, re.M).group(1)
        except Exception, data:
                print 'frame header:\n%s' % frame_data
                traceback.print_exc()
                raise ParserException, 'parse_frame failed'
