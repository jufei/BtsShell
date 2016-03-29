import time
import serial
import os
import sys
import types
import struct
import socket
import logging
import binascii
import string
import random

DEBUG_LEVEL_NONE = 0

POWER_ON_PORT_1  = "01050000FF008C3A"
POWER_OFF_PORT_1 = "010500000000CDCA"
CHECK_PORT_1     = "010200000001B9CA"

POWER_ON_PORT_2  = "01050001FF00DDFA"
POWER_OFF_PORT_2 = "0105000100009C0A"
CHECK_PORT_2     = "010200010001E80A"

POWER_ON_PORT_3  = "01050002FF002DFA"
POWER_OFF_PORT_3 = "0105000200006C0A"
CHECK_PORT_3     = "010200020001180A"

POWER_ON_PORT_4  = "01050003FF007C3A"
POWER_OFF_PORT_4 = "0105000300003DCA"
CHECK_PORT_4     = "01020003000149CA"

POWER_ON_PORT_5  = "01050004FF00CDFB"
POWER_OFF_PORT_5 = "0105000400008C0B"
CHECK_PORT_5     = "010200040001F80B"

POWER_ON_PORT_6  = "01050005FF009C3B"
POWER_OFF_PORT_6 = "010500050000DDCB"
CHECK_PORT_6     = "010200050001A9CB"

DC_ON     = (0x40,0x30,0x30,0x57,0x52,0x30,0x30,0x31,0x30,0x30,0x30,0x30,0x32,0x34,0x36,0x2a,0x0d)
AC_ON     = (0x40,0x30,0x30,0x57,0x52,0x30,0x30,0x31,0x30,0x30,0x30,0x30,0x31,0x34,0x35,0x2A,0x0D)
POWER_OFF = (0x40,0x30,0x30,0x57,0x52,0x30,0x30,0x31,0x30,0x30,0x30,0x30,0x30,0x34,0x34,0x2a,0x0d)
POWER_ON  = (0x40,0x30,0x30,0x57,0x52,0x30,0x30,0x31,0x30,0x30,0x30,0x30,0x33,0x34,0x37,0x2a,0x0d)


class CSocketClient:

    def __init__(self, ServerIp = '127.0.0.1', ServerPort = 15004, ClientIp = "127.0.0.1", ClientPort = 12005, ConnectType = 'TCP', TimeOut = 5.0):

        self.DebugLevel = DEBUG_LEVEL_NONE
        self.IfConneted = False
        self.TimeOut = TimeOut
        self.ServerIp = ServerIp
        self.ServerPort = ServerPort
        self.ClientIp = ClientIp
        self.ClientPort = ClientPort
        self.ConnectType = ConnectType
        self.Socket = None
        self.__Log = CLogPrinter().CreatLogger('SocketConnection.CSocketClient')

    def open(self):
        # close previous connection
        if self.IfConneted == True:
            self.close()
        try:
            if self.ConnectType == 'TCP':
                self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            elif self.ConnectType == 'UDP':
                self.Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                self.__Log.error("Socket type '%s' is invalid!" % self.ConnectType)
                self.Socket = None
                self.IfConneted = False
                return False

            self.Socket.settimeout(self.TimeOut)
            self.Socket.bind((self.ClientIp, self.ClientPort))
            self.Socket.connect((self.ServerIp, self.ServerPort))
            self.IfConneted = True
            self.__Log.debug("'%s' socket '%s:%s' is established!" % (self.ConnectType, self.ServerIp, self.ServerPort))
            return True

        except Exception, p_ErrInfo:
            self.__Log.error(p_ErrInfo)
            return False

    def close(self):
        if self.IfConneted == True:
            self.Socket.close()
            self.IfConneted = False
        self.__Log.debug("'%s' socket '%s:%s' is closed!" % (self.ConnectType, self.ServerIp, self.ServerPort))
        return True

    def send(self, SendMsg = ''):
        p_marshalled = ""

        if self.IfConneted == False:
            self.__Log.error("'%s' socket '%s:%s' is closed, send failure!" %\
                             (self.ConnectType, self.ServerIp, self.ServerPort))
            return False

        for p in SendMsg:
            if isinstance(p, types.StringTypes) == False:
                p_marshalled += struct.pack("l", socket.htonl(p))
            else:
                p_marshalled += p

        try:
            self.Socket.send(p_marshalled)
            self.__Log.debug("Send message over '%s' socket '%s:%s' is success!" %\
                                 (self.ConnectType, self.ServerIp, self.ServerPort))
        except Exception, p_Err:
            self.__Log.error(p_Err)
            self.__Log.error("Send message over '%s' socket '%s:%s' is failed!" %\
                                 (self.ConnectType, self.ServerIp, self.ServerPort))
        return True

    def receive(self, maxMsgSize=4096, recTimeout=10.0):

        marshalled = []
        msg = ""

        if self.TimeOut != recTimeout:
            self.TimeOut = recTimeout

        try:
            if self.TimeOut == 0xFFFFFFFF:
                # infinite timeout
                self.TimeOut = None
            elif self.TimeOut > 0x7FFFFFFF:
                # to avoid errors
                self.TimeOut = 0x7FFFFFFF

            self.Socket.settimeout(self.TimeOut)
            (msg, address) = self.Socket.recvfrom(maxMsgSize)

        except Exception, p_Error:
            self.__Log.error(p_Error)
            self.__Log.error("No response received during the timeout '%s'." % recTimeout)
            msg = None

        return msg

class CLogPrinter:
    def __init__(self):
        """Initial logger configuration variable"""
        self.__Logger = None
        self.__LogTag = 'CheckLog'

    def InitConfigLogger(self, LogLevel = 1, LogFileName = 'SocketConnection.log', LogFileMode = 'w', LogOutput = 2):
        """Creat and cofig logger

        Log Level:0-DEBUG; 1-INFO; 2-WARN; 3-ERROR; 4-FATAL
        LogOutput: 0-Only stdout; 1-Only file; 2-Both stdout and file
        """
        #Check input argv
        DirName = os.path.dirname(LogFileName)
        if not os.path.isdir(DirName):
            print "FATAL: Log directrory %s is not exist, please check your configuration" % DirName
            sys.exit(1)
        #Log level convertion
        if LogLevel == 0:
            self.__LogLevel = logging.DEBUG
        elif LogLevel == 1:
            self.__LogLevel = logging.INFO
        elif LogLevel == 2:
            self.__LogLevel = logging.WARN
        elif LogLevel == 3:
            self.__LogLevel = logging.ERROR
        elif LogLevel == 4:
            self.__LogLevel = logging.FATAL
        else:
            #the defalut log level is info
            self.__LogLevel = logging.INFO
        #Log output method convertion
        if LogOutput == 0:
            FileHandlerSwitch = 0
            StdHandlerSwitch = 1
        elif LogOutput == 1:
            FileHandlerSwitch = 1
            StdHandlerSwitch = 0
        else:
            FileHandlerSwitch = 1
            StdHandlerSwitch = 1
        #Basic config for file handler
        if FileHandlerSwitch:
            logging.basicConfig(filename = LogFileName,
                                filemode = LogFileMode,
                                format = '<%(asctime)s> %(module)s/%(name)s/line %(lineno)d, %(levelname)s: %(message)s',
                                level = self.__LogLevel)
        #creat logger
        self.__Logger = logging.getLogger(self.__LogTag)
        #creat handler
        self.__Handler = logging.StreamHandler(sys.stdout)
        #set level
        self.__Handler.setLevel(self.__LogLevel)
        #set format
        p_Formatter = logging.Formatter('%(module)s/%(name)s/%(levelname)s: %(message)s')
        self.__Handler.setFormatter(p_Formatter)
        ##set filter
        #filter=logging.Filter('tester')
        #self.handler.addFilter(filter)
        #load handler to logger
        if StdHandlerSwitch:
            self.__Logger.addHandler(self.__Handler)
        return True

    def CreatLogger(self, LogTag = 'A2A'):
        """Creat a logger

        Input:[1]LogTag, seem like 'A2ALog.main', 'A2ALog.common', 'A2ALog.common.find'
        Output:[1]logger for print
        """
        self.__LogTag = LogTag
        self.__Logger = logging.getLogger(self.__LogTag)
        return self.__Logger

    def DisableDebugLog(self):
        """Set log level

        Log Level:0-DEBUG; 1-INFO; 2-WARN; 3-ERROR; 4-FATAL
        """
        #self.__Handler.setLevel(self.__LogLevel)
        logging.disable(logging.DEBUG)
        return True

    def CloseLogger(self):
        """Close logger"""
        self.__Handler.flush()
        self.__Logger.removeHandler(self.__Handler)
        return True


def ConfigLogger(LogFile):
    """Config logger for application"""
    p_LogFileTmp = LogFile
    p_LogPrtTmp = CLogPrinter()
    p_LogPrtTmp.InitConfigLogger(0, p_LogFileTmp, 'a')
    p_LogTmp = p_LogPrtTmp.CreatLogger('SocketConnection.Main')

    return (p_LogPrtTmp, p_LogTmp)

def ReadMsg(MsgExcelPath):
    """"""
    p_MsgExcelPath = MsgExcelPath
    p_Logging = CLogPrinter().CreatLogger('SocketConnection.ReadMsg')
    p_MsgBody = ""

    if not os.path.isfile(p_MsgExcelPath):
        p_Logging.error("Excel %s does not exists!" % p_MsgExcelPath)
        return p_MsgBody

    try:
        p_MsgExcel = xlrd.open_workbook(p_MsgExcelPath)

        if 'Message' in p_MsgExcel.sheet_names():
            p_MsgSheet = p_MsgExcel.sheet_by_name('Message')
            p_ColList = p_MsgSheet.row_values(0)

            if ("Value") in p_ColList and (p_MsgSheet.nrows > 1):
                p_ElementValueCol = p_ColList.index("Value")

                for p_ElementValue in p_MsgSheet.col_values(p_ElementValueCol)[1:]:
                    p_ElementValue = str(p_ElementValue).upper().replace('0X', '')
                    p_MsgBody = string.join((p_MsgBody, p_ElementValue), '')

            else:
                p_Logging.error("Message body is empty!")
        else:
           p_Logging.error("There is no message in excel!")

        return p_MsgBody

    except Exception, p_Error:
        p_Logging.error(p_Error)
        return ""

def ReadConnectInfo(MsgExcelPath):
    """"""
    p_MsgExcelPath = MsgExcelPath
    p_Logging = CLogPrinter().CreatLogger('SocketConnection.ReadConnectInfo')

    Src_IP = None
    Des_IP = None
    Src_Port = None
    Des_Port = None
    Protocol_Type = None
    p_ConnectInfo = {}

    if not os.path.isfile(p_MsgExcelPath):
        p_Logging.error("Excel %s does not exists!" % p_MsgExcelPath)
        return (Src_IP, Src_Port, Des_IP, Des_Port, Protocol_Type)

    try:
        p_MsgExcel = xlrd.open_workbook(p_MsgExcelPath)

        if 'IP' in p_MsgExcel.sheet_names():
            p_IpSheet = p_MsgExcel.sheet_by_name('IP')
            p_ColList = p_IpSheet.row_values(0)
            p_ValueList = p_IpSheet.row_values(1)

            for p_No in xrange(len(p_ColList)):
                p_ConnectInfo[p_IpSheet.cell_value(0, p_No)] = p_IpSheet.cell_value(1, p_No)

            if [u'Src_IP', u'Des_IP', u'Src_Port', u'Des_Port', u'Protocol_Type'] == p_ConnectInfo.keys():
                Src_IP = p_ConnectInfo[u'Src_IP']
                Des_IP = p_ConnectInfo[u'Des_IP']
                Src_Port = p_ConnectInfo[u'Src_Port']
                Des_Port = p_ConnectInfo[u'Des_Port']
                Protocol_Type = p_ConnectInfo[u'Protocol_Type']
            else:
                p_Logging.error("Connection informaiton is empty!")
        else:
           p_Logging.error("There is no IP information in excel!")

        return (Src_IP, Src_Port, Des_IP, Des_Port, Protocol_Type)

    except Exception, p_Error:
        p_Logging.error(p_Error)
        return (Src_IP, Src_Port, Des_IP, Des_Port, Protocol_Type)

def tm500_power_on(port='COM1'):
    """This keyword power on TM500.

    | Input Parameters | Man. | Description |
    | port             | Yes  | com port |

    Example
    | Tm500 Power On | COM1 |

    """
    try:
        ser=serial.Serial(port,baudrate=9600,bytesize=7,parity='E',xonxoff=1,stopbits=2,timeout=0)
    except:
        raise Exception,"Open Serial failed port='%s' " %port

    POWER_ON_CMD= '%c'* len(POWER_ON) % POWER_ON
    try:
        ser.write(POWER_ON_CMD)
        print "TM500 Power ON"
    finally:
        ser.close()

def tm500_power_off(port='COM1'):
    """This keyword power off TM500.

    | Input Parameters | Man. | Description |
    | port             | Yes  | com port |

    Example
    | Tm500 Power Off | COM1 |
    """

    try:
        ser=serial.Serial(port,baudrate=9600,bytesize=7,parity='E',xonxoff=1,stopbits=2,timeout=0)
    except:
        raise Exception,"Open Serial failed port='%s' " %port

    AC_OFF_CMD = '%c'* len(DC_ON) % DC_ON
    try:
        ser.write(AC_OFF_CMD)
        print "TM500 Power OFF"
    finally:
        ser.close()

def power_on(vendor_info='COM1'):
    """This keyword power on BTS.

    | Input Parameters | Man. | Description |
    | vendor_info      | Yes  | PB COM port or IP  |

    Example
    | Power On ||
    | Power On | ${POWER_BREAK_IP}:${POWER_BREAK_OUTPUT}:${BTS_CONTROL_PC_LAB} |
    """

    tmp = vendor_info.split(':')

    if 3 == len(tmp):
        PowerBreaker_Ip   = tmp[0]
        PowerBreaker_Port = tmp[1]
        BtsControlPC_ip   = tmp[2]

        Log_Path = os.path.join(os.getcwd(), "SocketConnection.log")
        (p_LogPrtTmp, p_LogTmp) = ConfigLogger(Log_Path)
        p_Logging = CLogPrinter().CreatLogger('SocketConnection.Main')

        p_Socket = None

        if '1' == PowerBreaker_Port:
            CHECK_PORT    = CHECK_PORT_1
            POWER_ON_PORT = POWER_ON_PORT_1
        elif '2' == PowerBreaker_Port:
            CHECK_PORT    = CHECK_PORT_2
            POWER_ON_PORT = POWER_ON_PORT_2
        elif '3' == PowerBreaker_Port:
            CHECK_PORT    = CHECK_PORT_3
            POWER_ON_PORT = POWER_ON_PORT_3
        elif '4' == PowerBreaker_Port:
            CHECK_PORT    = CHECK_PORT_4
            POWER_ON_PORT = POWER_ON_PORT_4
        elif '5' == PowerBreaker_Port:
            CHECK_PORT    = CHECK_PORT_5
            POWER_ON_PORT = POWER_ON_PORT_5
        elif '6' == PowerBreaker_Port:
            CHECK_PORT    = CHECK_PORT_6
            POWER_ON_PORT = POWER_ON_PORT_6
        else:
            raise Exception, "PowerBreaker_Port out of range!"

        try:
            p_Socket = CSocketClient(PowerBreaker_Ip, 4001, BtsControlPC_ip, random.randint(1025, 2047) , "TCP", 5)
            if p_Socket.open():
                # power on
                if p_Socket.send(binascii.a2b_hex(POWER_ON_PORT)):
                    p_Logging.debug("Send message POWER_ON_PORT_%s %s over socke success!" \
                        % (PowerBreaker_Port, POWER_ON_PORT))
                else:
                    raise Exception, "Send message POWER_ON_PORT_%s failed!" % PowerBreaker_Port

                p_Logging.debug("Receive POWER ON PORT %s message--> %s" \
                    % (PowerBreaker_Port ,binascii.b2a_hex(p_Socket.receive())))

                #check port
                if p_Socket.send(binascii.a2b_hex(CHECK_PORT)):
                    p_Logging.debug("Send message CHECK_PORT_%s %s over socke success!" \
                        % (PowerBreaker_Port, CHECK_PORT))
                else:
                    raise Exception, "Send message CHECK_PORT_%s failed!" % PowerBreaker_Port

                p_Logging.debug("Receive CHECK PORT %s closed message--> %s" \
                    % (PowerBreaker_Port, binascii.b2a_hex(p_Socket.receive())))

            else:
                raise Exception, "Socket can't be established, send message failure!"

        except Exception, p_Err:
            p_Logging.error(p_Err)

        finally:
            if p_Socket:
                p_Logging.info("Socket release!")
                p_Socket.close()

    else:
        port = vendor_info

        try:
            ser=serial.Serial(port,baudrate=9600,bytesize=7,parity='E',xonxoff=1,stopbits=2,timeout=0)
        except:
            raise Exception,"Open Serial failed port='%s' " %port

        POWER_ON_CMD = '%c'* len(POWER_ON) % POWER_ON
        try:
            ser.write(POWER_ON_CMD)
            print "BTS Power ON"
        finally:
            ser.close()

def power_off(vendor_info='COM1'):
    """This keyword power off BTS.

    | Input Parameters | Man. | Description |
    | vendor_info      | Yes  | PB COM port or IP  |

    Example
    | Power Off ||
    | Power Off | ${POWER_BREAK_IP}:${POWER_BREAK_OUTPUT}:${BTS_CONTROL_PC_LAB} |
    """

    tmp = vendor_info.split(':')

    if 3 == len(tmp):
        PowerBreaker_Ip   = tmp[0]
        PowerBreaker_Port = tmp[1]
        BtsControlPC_ip   = tmp[2]

        Log_Path = os.path.join(os.getcwd(), "SocketConnection.log")
        try:
            if os.path.isfile(Log_Path):
                os.remove(Log_Path)

            if not os.path.isdir(os.path.dirname(Log_Path)):
                DirCreate(os.path.dirname(Log_Path))

        except:
            print "Couldn't remove old log file but continues..."

        (p_LogPrtTmp, p_LogTmp) = ConfigLogger(Log_Path)
        p_Logging = CLogPrinter().CreatLogger('SocketConnection.Main')

        p_Socket = None

        if '1' == PowerBreaker_Port:
            CHECK_PORT    = CHECK_PORT_1
            POWER_OFF_PORT = POWER_OFF_PORT_1
        elif '2' == PowerBreaker_Port:
            CHECK_PORT    = CHECK_PORT_2
            POWER_OFF_PORT = POWER_OFF_PORT_2
        elif '3' == PowerBreaker_Port:
            CHECK_PORT    = CHECK_PORT_3
            POWER_OFF_PORT = POWER_OFF_PORT_3
        elif '4' == PowerBreaker_Port:
            CHECK_PORT    = CHECK_PORT_4
            POWER_OFF_PORT = POWER_OFF_PORT_4
        elif '5' == PowerBreaker_Port:
            CHECK_PORT    = CHECK_PORT_5
            POWER_OFF_PORT = POWER_OFF_PORT_5
        elif '6' == PowerBreaker_Port:
            CHECK_PORT    = CHECK_PORT_6
            POWER_OFF_PORT = POWER_OFF_PORT_6
        else:
            raise Exception, "PowerBreaker_Port out of range!"

        try:
            p_Socket = CSocketClient(PowerBreaker_Ip, 4001, BtsControlPC_ip, random.randint(1025, 2047) , "TCP", 5)
            if p_Socket.open():
                # power off
                if p_Socket.send(binascii.a2b_hex(POWER_OFF_PORT)):
                    p_Logging.debug("Send message POWER_OFF_PORT_%s %s over socke success!" \
                        % (PowerBreaker_Port, POWER_OFF_PORT))
                else:
                    raise Exception, "Send message POWER_OFF_PORT_%s failed!" % PowerBreaker_Port

                p_Logging.debug("Receive POWER OFF PORT %s message--> %s" \
                    % (PowerBreaker_Port ,binascii.b2a_hex(p_Socket.receive())))

                #check port
                if p_Socket.send(binascii.a2b_hex(CHECK_PORT)):
                    p_Logging.debug("Send message CHECK_PORT_%s %s over socke success!" \
                        % (PowerBreaker_Port, CHECK_PORT))
                else:
                    raise Exception, "Send message CHECK_PORT_%s failed!" % PowerBreaker_Port

                p_Logging.debug("Receive CHECK PORT %s breaken message--> %s" \
                    % (PowerBreaker_Port, binascii.b2a_hex(p_Socket.receive())))

            else:
                raise Exception, "Socket can't be established, send message failure!"

        except Exception, p_Err:
            p_Logging.error(p_Err)

        finally:
            if p_Socket:
                p_Logging.info("Socket release!")
                p_Socket.close()

    else:
        port = vendor_info

        try:
            ser=serial.Serial(port,baudrate=9600,bytesize=7,parity='E',xonxoff=1,stopbits=2,timeout=0)
        except:
            raise Exception,"Open Serial failed port='%s' " %port

        DC_OFF_CMD = '%c'* len(AC_ON) % AC_ON
        try:
            ser.write(DC_OFF_CMD)
            print "BTS Power OFF"
        finally:
            ser.close()
power_on()


if __name__ == "__main__":
    #power_on()
    #power_on('10.68.160.131:10.140.86.97:6')
    pass
