import time
import types
import serial
import re
from robot.errors import ExecutionFailed
from BtsComm import TelnetConnection
from BtsShell import connections
from BtsShell.common_lib.get_path import *
from BtsShell.file_lib.common_operation import *

#add '0' for variable TMA_VERSION By GuanXiaobing 2012-05-09
TMA_VERSION = ('unknown','0')



def tm500_connect(radio_card = '', radio_context = '0', chassis = '0', tm500_mode='NAS_MODE', ca_group = '0'):
    """This keyword connects to TM500.

    | Input Parameters | Man. | Description |
    | radio_card | No | if "" no card select, could be RC1 or RC2 or RC1_RC2 |
    | radio_context | No | radio card context defalut as 0 |
    | chassis | No | radio card chassis default as 0 |
    | tm500_mode | No | default as NAS_MODE, you can set as 'MTS_MODE' or others |
    Example
    | TM500 Connect |
    """

    ret = connections.execute_tm500_command_without_check('#$$CONNECT')
    if ret.upper().find('OK') < 0 and ret.upper().find('ALREADY CONNECTED') < 0:
        raise Exception, 'Connection to TM500 failed'
    ret += connections.execute_tm500_command('GSTS')

    if 'T2-RC-A6' in radio_card:    #added for 3CC
        ret += connections.execute_tm500_command('ABOT 0 0 1')

    if ''!= radio_card:
        ret += _tm500_select_radio_card(radio_card, radio_context, chassis)

    if 'T2-RC-A6' in radio_card:    #added for 3CC
        ret += connections.execute_tm500_command('SCAG 0 0 1 2')

    if ca_group == '1': #Volte CA case,
        ret += connections.execute_tm500_command('SCAG 0 0 1')

    #connections.execute_tm500_command('EREF 0 0 0')
    ret += connections.execute_tm500_command('GETR')
    # change the pause time for 'SCFG' command in order to get the full reponse
    try:
        old_pause_time = connections.set_pause_time('10')
        # ret += connections.execute_tm500_command('SCFG %s'%tm500_mode)
        ret += connections.execute_tm500_command_without_check('SCFG %s'%tm500_mode, '2048', '10')
        ret += connections.execute_tm500_command('STRT')
        ret += connections.execute_tm500_command('GVER')
    finally:
        connections.set_pause_time(old_pause_time)
    return ret


def _tm500_select_radio_card(radio_card, radio_context = '0', chassis = '0'):
    """This keyword selects TM500 radio card.

    | Input Parameters | Man. | Description |
    | radio_card       | Yes  | radio card name, such as 'RC1' or 'RC2' |
    | radio_context    | No   | the radio context to be associated with radio card, default is 0 |
    | chassis          | No   | the chassis containing the radio card, default is 0 |

    Example
    | TM500 Select Radio Card | RC1 |
    | TM500 Select Radio Card | RC2 |
    """
    #connections.execute_tm500_command('SELR %s %s %s COMBINED' % (radio_context, chassis, radio_card))
    rc_num = 0
    ret = ''
    if 'RC1' in radio_card.upper():
        ret += connections.execute_tm500_command('SELR %d 0 RC1 COMBINED' %rc_num)
        rc_num += 1
        ret += connections.execute_tm500_command('EREF 0 0 0')
    if 'RC2' in radio_card.upper():
        if radio_context == '0':
            ret += connections.execute_tm500_command('SELR %d 0 RC2 COMBINED' %rc_num)
            rc_num += 1
            ret += connections.execute_tm500_command('EREF 1 0 0')
        else:
            ret += connections.execute_tm500_command('ADDR %d 0 RC2 COMBINED' %(rc_num-1))
            ret += connections.execute_tm500_command('EREF 0 0 0')
    if 'T2-RC-A6' in radio_card.upper():
        ret += connections.execute_tm500_command('SELR %d 0 T2-RC-A6 COMBINED' %rc_num)
        rc_num += 1
        ret += connections.execute_tm500_command('EREF 2 0 0')
    return ret


def tm500_get_version():
    """This keyword gets TM500 version.

    | Input Parameters | Man. | Description |

    Example
    | TM500 Get Version |
    """
    old_pause_time = connections.set_pause_time('5')
    ret = connections.execute_tm500_command_without_check('GVER', '65536')
    connections.set_pause_time(old_pause_time)
    ret = ret.upper()
    TMA_info_list = 'unkonwn'
    flag = False
    global TMA_VERSION
    Version_label_SK = re.compile('VERSION LABEL: LTE-(\w+)-\w+_\w+_\w+_\w+_(\w+)_(\w+)_(\w+)_REV(\d+)',re.M)
    Version_label_LMB = re.compile('VERSION LABEL: LTE-(\w+)-\w+_\w+_\w+_(\w+)_(\w+)_(\w+)_REV(\d+)',re.M)

    ret_SK = Version_label_SK.search(ret)
    ret_LMB = Version_label_LMB.search(ret)

    if ret_SK:
        TMA_info_list = ret_SK.groups()
        flag = True
    elif ret_LMB:
        TMA_info_list = ret_LMB.groups()
        flag = True
    print TMA_info_list
    if flag:
        TMA_info_list = list(TMA_info_list)
        TMA_version_title = TMA_info_list.pop(0)

        temp_str = ''
        for item in TMA_info_list:
            temp_str = temp_str + item
        TMA_version_id = int(temp_str)
        TMA_VERSION = TMA_version_title,TMA_version_id


def _judge_version(modification_version):
    version_title,version_id = TMA_VERSION
    if version_id >= int(modification_version):
        return True
    else:
        return False


def tm500_disconnect():
    """This keyword disconnects from TM500.

    | Input Parameters | Man. | Description |

    Example
    | TM500 Disconnect |
    """
    connections.execute_tm500_command_without_check('#$$DISCONNECT')
    # ok_flag = False
    # for i in xrange(3):
    #     ret = _tm500_disconnect_once()
    #     if ret:
    #         ok_flag = True
    #         break
    #     else:
    #         print "tm500 disconnect failed '%s' times" % i
    #         time.sleep(5)
    #         continue
    # if ok_flag == False:
    #     raise Exception("TM500 disconnect failed for %s times" % i)


def _tm500_disconnect_once():
    start_time = time.time()
    ret = connections.execute_tm500_command_without_check('#$$DISCONNECT')
    if ret:
        if ret.upper().find('OK') < 0 and ret.upper().find('NOT CONNECTED') < 0:
            return False
        else:
            return True
    else:
        return False

def tm500_trigger_rrcReestablishmentRequest(cause, trigger_event, delay='0', c_rnti='', phys_cell_id='', short_mac_i=''):
    """This keyword trigger the RRC reestablishment request from TM500.

    | Input Parameters | Man. | Description |
    | cause            | Yes  | Reestablishment cause |
    | trigger_event    | Yes  | Trigger event |
    | delay            | No   | Time delay (in ms) after the trigger event before starting the re-establishment |
    | c_rnti           | No   | CRNTI in HEX string (4 digits) |
    | phys_cell_id     | No   | Physical Cell Identity |
    | short_mac_i      | No   | Short MAC I in HEX String (4 digits) |

    Example
    | TM500 Trigger RRCReestablishmentRequest | 0 | 6 |
    """

    connections.execute_tm500_command('FORW MTE RRCAPTTRIGGERRRCREESTABLISHMENTREQ [%s] [%s] [%s] [%s] [%s] [%s]' % \
                                      (c_rnti, phys_cell_id, short_mac_i, cause, trigger_event, delay))


def tm500_start_logging():
    """This keyword starts TM500 logging.

    | Input Parameters | Man. | Description |

    Example
    | TM500 Start Logging |
    """
    old_PauseTime = connections.set_pause_time("5")
    try:
        start_time = time.time()
        ret_1 = ''
        ret_2 = connections.execute_tm500_command_without_check('#$$START_LOGGING')
        ret_1_2 = ret_1 + ret_2
        while ret_1_2.upper().find('START_LOGGING 0X00 OK') < 0:
            if 60 < (time.time()- start_time):
                raise Exception, 'Start TM500 logging failed'
            ret_1 = ret_2
            ret_2 = connections.get_recv_content(1024)
            ret_1_2 = ret_1 + ret_2
        return ret_1_2
    finally:
        connections.set_pause_time(old_PauseTime)

def tm500_stop_logging():
    """This keyword stops TM500 logging.

    | Input Parameters | Man. | Description |

    Example
    | TM500 Stop Logging |
    """
    old_PauseTime = connections.set_pause_time("5")
    try:
        start_time = time.time()
        ret_1 = ''
        ret_2 = connections.execute_tm500_command_without_check('#$$STOP_LOGGING')
        ret_1_2 = ret_1 + ret_2
        while ret_1_2.upper().find('STOP_LOGGING 0X00 OK') < 0:
            if 60 < (time.time()- start_time):
                raise Exception, 'Stop TM500 logging failed'
            ret_1 = ret_2
            ret_2 = connections.get_recv_content(65536)
            ret_1_2 = ret_1 + ret_2
    finally:
        connections.set_pause_time(old_PauseTime)


def tm500_data_log_folder(log_path):
    """This keyword starts TM500 logging.

    | Input Parameters | Man. | Description |
    | log_path         | Yes  | path for log saved |

    Example
    | TM500 Data Log Folder | C:\Temp |
    """

    cmd = '#$$DATA_LOG_FOLDER 1 %s' % log_path
    ret = connections.execute_tm500_command_without_check(cmd)


def tm500_set_DLSCHRX_logging():
    """This keyword starts TM500 logging.

    | Input Parameters | Man. | Description |

    Example
    | Tm500 Set DLSCHRX Logging |
    """

    connections.execute_tm500_command_without_check('#$$LC_CLEAR_ALL')
    connections.execute_tm500_command_without_check('#$$LC_ITM 1 1 1 Manual')

    connections.execute_tm500_command_without_check('#$$LC_GRP 1 1 0 1000 0 0 0 DLSCHRX #UE-1;-1#ALLUE=0')

    connections.execute_tm500_command_without_check('#$$LC_CAT 202 1 0 0')
    connections.execute_tm500_command_without_check('#$$LC_CAT 203 1 0 0')
    connections.execute_tm500_command_without_check('#$$LC_CAT 204 1 0 0')
    connections.execute_tm500_command_without_check('#$$LC_CAT 205 1 0 0')

    connections.execute_tm500_command_without_check('#$$LC_GRP 1 1 0 5 0 0 0 CQIREPORTING #UE-1;-1#ALLUE=0')
    connections.execute_tm500_command_without_check('#$$LC_CAT 262 1 0 0')
    connections.execute_tm500_command_without_check('#$$LC_CAT 263 1 0 0')
    connections.execute_tm500_command_without_check('#$$LC_CAT 264 1 0 0')

    connections.execute_tm500_command_without_check('#$$LC_ITM 0 0 0 Automatic')
    connections.execute_tm500_command_without_check('#$$LC_END')


def tm500_ue_detach():
    """This keyword does UE detach in TM500.

    | Input Parameters | Man. | Description |

    Example
    | TM500 UE Detach |
    """

    connections.execute_tm500_command_without_check('FORW MTE NASCONFIGEMMDEREGISTER 0')
    connections.execute_tm500_command_without_check('FORW MTE ACTIVATE -1')


def phy_override_cqi(cqi_value, ri_value = '1', pmi_value = '0'):
    """This keyword will change the CQI value.

    | Input Parameters | Man. | Description |
    | cqi_value        | Yes  | CQI value need to override |
    | ri_value         | No   | RI value need to override |
    | pmi_value        | No   | PMI value need to override |

    Example
    | Phy Override Cqi | 15 | 1 | 1 |
    """

    if '1' == ri_value:
        command = 'FORW MTE PHYOVERRIDECQI %s(%s((1{%s})))'%(ri_value, pmi_value, cqi_value)
    else:
        command = 'FORW MTE PHYOVERRIDECQI %s(%s((1{%s %s})))'%(ri_value, pmi_value, cqi_value, cqi_value)

    ret = connections.execute_tm500_command_without_check(command)

    if ret.find('SUCCEEDED') < 0:
        raise Exception, "command '%s' execution failed" % command
    time.sleep(2)
    return time.strftime('%H:%M:%S')

def tm500_convert_to_text(pause_time='3', timeout='30'):
    """This keyword converts the TM500 log to text files.

    | Input Parameters | Man. | Description |
    | pause_time       | No   | Default pause time is 3 seconds |
    | timeout          | No   | Time out to get successful response, default is 30 |

    Example
    | TM500 Convert To Text |
    """
    old_PauseTime = connections.set_pause_time(pause_time)
    try:
        start_time = time.time()
        timeout = int(timeout)
        ret_1 = ''
        ret_2 = connections.execute_tm500_command_without_check('#$$CONVERT_TO_TEXT 0', '16777216')
        ret_1_2 = ret_1 + ret_2
        # while (ret_1_2.upper().find('CONVERT_TO_TEXT 0X00 OK') < 0) and ((time.clock()- start_time) < timeout):
        while (ret_1_2.upper().find('C: CONVERT_TO_TEXT') < 0) and ((time.time()- start_time) < timeout):
            ret_1 = ret_2
            ret_2 = connections.get_recv_content(65536)
            ret_1_2 = ret_1 + ret_2
    finally:
        connections.set_pause_time(old_PauseTime)
    return ret_1_2


def __tm500_start_L1THOUGHPUT_logging():

    connections.execute_tm500_command_without_check('#$$LC_CLEAR_ALL')
    connections.execute_tm500_command_without_check('#$$LC_ITM 1 1 1 Manual')

    connections.execute_tm500_command_without_check('#$$LC_GRP 1 1 1 10 0 0 0 L1THROUGHPUT #UE-1;-1#ALLUE=0')
    #connections.execute_tm500_command_without_check('#$$LC_CAT 281 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 282 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 283 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 284 1 1 1')

    connections.execute_tm500_command_without_check('#$$LC_GRP  1 1 1 10 0 0 0 ProtocolLog #UE-1;-1\#ALLUE=0')
    connections.execute_tm500_command_without_check('#$$LC_CAT 1030 1 1 1')

    connections.execute_tm500_command_without_check('#$$LC_GRP  1 1 1 10 0 0 0 UEOVERVIEW #UE-1;-1\#ALLUE=0')
    #connections.execute_tm500_command_without_check('#$$LC_CAT 301 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 302 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 303 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 304 1 1 1')

    connections.execute_tm500_command_without_check('#$$LC_ITM 0 0 0 Automatic')

    connections.execute_tm500_command_without_check('#$$LC_END')


def __tm500_logging_Clear_all():
    connections.execute_tm500_command_without_check('#$$LC_CLEAR_ALL')
    connections.execute_tm500_command_without_check('#$$LC_ITM 1 1 1 Manual')


def __tm500_logging_L1THROUGHPUT():
    connections.execute_tm500_command_without_check('#$$LC_GRP 1 1 1 1 0 0 0 L1THROUGHPUT #UE-1;')
    #connections.execute_tm500_command_without_check('#$$LC_CAT 281 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 282 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 283 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 284 1 1 1')


def __tm500_logging_ProtocolLog():
    connections.execute_tm500_command_without_check('#$$LC_GRP 1 1 1 1 0 0 0 ProtocolLog #UE-1;')
    connections.execute_tm500_command_without_check('#$$LC_CAT 1030 1 1 1')


def __tm500_logging_CQIREPORTING():
    connections.execute_tm500_command_without_check('#$$LC_GRP 1 1 1 1 0 0 0 CQIREPORTING #UE-1;')
    #connections.execute_tm500_command_without_check('#$$LC_CAT 261 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 262 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 263 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 264 1 1 1')


def __tm500_logging_DLSCHRX():
    connections.execute_tm500_command_without_check('#$$LC_GRP 1 1 1 1 0 0 0 DLSCHRX #UE-1;')
    #connections.execute_tm500_command_without_check('#$$LC_CAT 201 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 202 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 203 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 204 1 1 1')
    #connections.execute_tm500_command_without_check('#$$LC_CAT 205 1 1 1')


def __tm500_logging_ULSRS():
    connections.execute_tm500_command_without_check('#$$LC_GRP 1 1 1 1 0 0 0 ULSRS #UE-1;')
    connections.execute_tm500_command_without_check('#$$LC_CAT 210 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 212 1 1 1')


def __tm500_logging_DLL1L2CONTROL():
    connections.execute_tm500_command_without_check('#$$LC_GRP 1 1 1 1 0 0 0 DLL1L2CONTROL #UE-1;')
    #connections.execute_tm500_command_without_check('#$$LC_CAT 91 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 92 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 93 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 94 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 95 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 96 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 97 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 98 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 99 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 100 1 1 1')


def __tm500_logging_PRACHTX():
    connections.execute_tm500_command_without_check('#$$LC_GRP 1 1 1 1 0 0 0 PRACHTX #UE-1;')
##    connections.execute_tm500_command_without_check('#$$LC_CAT 351 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 352 1 1 1')


def __tm500_logging_ULSCHTX():
    global TMA_VERSION
    version_title,version_id = TMA_VERSION
    version_return = _judge_version(32002)

    connections.execute_tm500_command_without_check('#$$LC_GRP 1 1 1 1 0 0 0 ULSCHTX #UE-1;')
    if version_title == 'MUE' and version_return:
        connections.execute_tm500_command_without_check('#$$LC_CAT 82 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 83 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 85 1 1 0')

    else:
        connections.execute_tm500_command_without_check('#$$LC_CAT 82 1 1 1')
        connections.execute_tm500_command_without_check('#$$LC_CAT 83 1 1 1')
        connections.execute_tm500_command_without_check('#$$LC_CAT 85 1 1 1')

    if version_title == 'MUE':
        connections.execute_tm500_command_without_check('#$$LC_CAT 802 1 1 1')

def __tm500_logging_DLHARQRX():
    connections.execute_tm500_command_without_check('#$$LC_GRP 1 1 1 1 0 0 0 DLHARQRX #UE-1;')
    connections.execute_tm500_command_without_check('#$$LC_CAT 40 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 41 1 1 1')

def __tm500_logging_ULHARQTX():
    connections.execute_tm500_command_without_check('#$$LC_GRP 1 1 1 1 0 0 0 ULHARQTX #UE-1;')
    connections.execute_tm500_command_without_check('#$$LC_CAT 160 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 161 1 1 1')


def __tm500_logging_UEOVERVIEW():
    connections.execute_tm500_command_without_check('#$$LC_GRP  1 1 1 10 0 0 0 UEOVERVIEW #UE-1;-1\#ALLUE=0')
    #connections.execute_tm500_command_without_check('#$$LC_CAT 301 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 302 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 303 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 304 1 1 1')


def __tm500_logging_RLCTXSTATS():
    connections.execute_tm500_command_without_check('#$$LC_GRP  1 1 1 10 0 0 0 RLCTXSTATS #UE-1;')
    #connections.execute_tm500_command_without_check('#$$LC_CAT 151 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 152 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 153 1 1 1')

def __tm500_logging_RLCRXSTATS():
    connections.execute_tm500_command_without_check('#$$LC_GRP  1 1 1 10 0 0 0 RLCRXSTATS #UE-1;')
    connections.execute_tm500_command_without_check('#$$LC_CAT 141 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 142 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 143 1 1 1')

def __tm500_logging_L1DLRSPOWER():
    connections.execute_tm500_command_without_check('#$$LC_GRP  1 1 1 10 0 0 0 L1DLRSPOWER #UE-1;')
    #connections.execute_tm500_command_without_check('#$$LC_CAT 111 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 112 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 113 1 1 1')


def __tm500_logging_MACTX():
    connections.execute_tm500_command_without_check('#$$LC_GRP  1 1 1 10 0 0 0 MACTX #UE-1;')
    #connections.execute_tm500_command_without_check('#$$LC_CAT 61 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 62 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 63 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 64 1 1 1')
    connections.execute_tm500_command_without_check('#$$LC_CAT 65 1 1 1')

def __tm500_logging_L1RBPOWERS():
    connections.execute_tm500_command_without_check('#$$LC_GRP  1 1 1 10 0 0 0 L1RBPOWERS #UE-1;')
    connections.execute_tm500_command_without_check('#$$LC_CAT 4201 1 1 0')
    connections.execute_tm500_command_without_check('#$$LC_CAT 4202 1 1 0')

def __tm500_logging_L1CELLWATCH():
    connections.execute_tm500_command_without_check('#$$LC_GRP  1 1 1 10 0 0 0 L1CELLWATCH #UE-1;')
    connections.execute_tm500_command_without_check('#$$LC_CAT 104 1 1 0')


def __tm500_logging_MACRX():
    global TMA_VERSION
    version_title,version_id = TMA_VERSION
    version_return = _judge_version(32000)

    connections.execute_tm500_command_without_check('#$$LC_GRP  1 1 1 10 0 0 0 MACRX #UE-1;')
    if version_title == 'MUE' and version_return:
        connections.execute_tm500_command_without_check('#$$LC_CAT 122 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 123 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 124 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 125 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 126 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 127 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 128 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 129 1 1 0')

    else:
        connections.execute_tm500_command_without_check('#$$LC_CAT 122 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 123 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 124 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 125 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 126 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 127 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 128 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 129 1 1 0')

    if version_title == 'MUE':
        connections.execute_tm500_command_without_check('#$$LC_CAT 1202 1 1 0')

def __tm500_logging_SYSOVERVIEW():
    global TMA_VERSION
    version_title,version_id = TMA_VERSION
    version_return = _judge_version(32000)

    connections.execute_tm500_command_without_check('#$$LC_GRP  1 1 1 10 0 0 0 SYSOVERVIEW #UE-1;')
    if version_title == 'MUE':
        connections.execute_tm500_command_without_check('#$$LC_CAT 362 1 1 0')
        connections.execute_tm500_command_without_check('#$$LC_CAT 363 1 1 0')


def __tm500_logging__LC_END():
    connections.execute_tm500_command_without_check('#$$LC_ITM 0 0 0 Automatic')
    connections.execute_tm500_command_without_check('#$$LC_END')



def tm500_reboot_by_serial(tm500_pc_conn):
    """This keyword reboot TM500 by serial port command.

    | Input Parameters | Man. | Description |
    | tm500_pc_conn | Yes | Connection object of TM500 control PC |

    Example
    | tm500_reboot_by_serial_port | ${TM500_Control_pC_connection} |
    """
    reboot_exe_dir =  os.path.join(get_tools_path(), "tm500_reboot_by_serial.exe")
    connections.switch_host_connection(tm500_pc_conn)
    connections.execute_shell_command_without_check("TASKKILL /F /IM hypertrm.exe")
    connections.execute_shell_command_without_check("TASKKILL /F /IM TmaApplication.exe")

    old_timeout = connections.set_shell_timeout('300')
    try:
        ret = connections.execute_shell_command(reboot_exe_dir)
    except:
        ret = connections.execute_shell_command(reboot_exe_dir)
        #connections.execute_shell_command_without_check('\x03')
    finally:
        connections.set_shell_timeout(old_timeout)

def tm500_reboot():
    """This keyword used for reboot TM500 by TMA command.

    | Input Parameters | Man. | Description |
    |                  | No   |   |

    Example
    | tm500_reboot |
    """
    old_PauseTime = connections.set_pause_time("2")
    try:
        connections.set_pause_time("100")
        ret = connections.execute_tm500_command_without_check('RBOT')
        if ret.upper().find('OK') < 0 or ret.upper().find('THE TMA HAS RE-CONNECTED AUTOMATICALLY') < 0:
            raise ExecutionFailed, "command 'RBOT' execution failed"
        return ret
    finally:
        connections.set_pause_time(old_PauseTime)

def TM500_status_check(TM500_status_check_SCRIPT):
    """This keyword used for check TM500 status by TM500 COM port.

    | Input Parameters          | Man. | Description |
    | TM500_status_check_SCRIPT |  Yes | the dir of script  |

    Example
    | TM500_status_check(script_name)  |
    """
    old_timeout = connections.set_shell_timeout('300')
    try:
        ret = connections.execute_shell_command_without_check(TM500_status_check_SCRIPT)
        return ret
    finally:
        connections.set_shell_timeout(old_timeout)


def tm500_logging_select(log_option= 'ProtocolLog', number_of_ue = '0'):
    """Deprecated, use tm500_logging_select_from_file
    This keyword will select TM500 logging types.

    | Input Parameters | Man. | Description |
    | log_option       | Yes  | logging types with the same name as displayed |
    | number_of_ue     | No   | Number of UEs need to be logged, default is 0 which means single UE |

    Example
	| ${loggint_types} = | create list | DLSCHRX | ProtocolLog | CQIREPORTING |
    | TM500 Logging Select  | ULSCHTX  | ${logging_types} |

    Note: Till now the log types we can select are:
    DLSCHRX,DLHARQRX,ULHARQTX,L1THROUGHPUT, ProtocolLog,ULSCHTX, CQIREPORTING, ULSRS, DLL1L2CONTROL, PRACHTX,RLCTXSTATS
    RLCRXSTATS L1DLRSPOWER MACTX,L1CELLWATCH
    """
    tm500_get_version()
    old_pause_time = connections.set_pause_time('0')

    try:
        ret = _tm500_logging_select(log_option, number_of_ue)
        return ret
    finally:
        connections.set_pause_time(old_pause_time)

def _tm500_logging_select(log_option= 'ProtocolLog', number_of_ue = '0'):
    __tm500_logging_Clear_all()

    try:
        numbers = int(number_of_ue)
        if numbers > 32:
            raise Exception, 'given number_of_ue greater than expected 32, got is %s' % number_of_ue
    except:
        raise Exception, 'given number_of_ue must be integer, not got %s' % number_of_ue

    if numbers != 0:
        number_list = range(numbers)

        group_name = 'UE %s-%s' % (min(number_list), max(number_list))
        group = ''
        for number in number_list:
            group += str(number)
            if number != number_list[-1]:
                group += ','
        connections.execute_tm500_command_without_check('#$$LC_END')
        connections.execute_tm500_command('#$$LC_UE_GROUP \"%s\" \"%s\"' % (group_name, group))

    if type(log_option) == types.UnicodeType:
        if log_option in ['DLSCHRX', 'L1THROUGHPUT', 'ProtocolLog', 'ULSCHTX', 'CQIREPORTING', 'DLHARQRX', \
                          'ULSRS', 'DLL1L2CONTROL', 'PRACHTX', 'UEOVERVIEW', 'RLCTXSTATS','RLCRXSTATS', 'L1DLRSPOWER', \
                          'MACTX','MACRX','SYSOVERVIEW','L1RBPOWERS','ULHARQTX','L1CELLWATCH']:
            func_name = "__tm500_logging_%s()" % (log_option)
            exec(func_name)
        else:
            __tm500_logging_ProtocolLog()
    elif isinstance(log_option, list):
        log_flag = False
        if 'DLSCHRX' in log_option:
            __tm500_logging_DLSCHRX()
            log_flag = True
        if 'ULSCHTX' in log_option:
            __tm500_logging_ULSCHTX()
            log_flag = True
        if 'L1THROUGHPUT' in log_option:
            __tm500_logging_L1THROUGHPUT()
            log_flag = True
        if 'ProtocolLog' in log_option:
            __tm500_logging_ProtocolLog()
            log_flag = True
        if 'CQIREPORTING' in log_option:
            __tm500_logging_CQIREPORTING()
            log_flag = True
        if 'ULSRS' in log_option:
            __tm500_logging_ULSRS()
            log_flag = True
        if 'DLL1L2CONTROL' in log_option:
            __tm500_logging_DLL1L2CONTROL()
            log_flag = True
        if 'PRACHTX' in log_option:
            __tm500_logging_PRACHTX()
            log_flag = True
        if 'DLHARQRX' in log_option:
            __tm500_logging_DLHARQRX()
            log_flag = True
        if 'UEOVERVIEW' in log_option:
            __tm500_logging_UEOVERVIEW()
            log_flag = True
        if 'RLCTXSTATS' in log_option:
            __tm500_logging_RLCTXSTATS()
            log_flag = True
        if 'RLCRXSTATS' in log_option:
            __tm500_logging_RLCRXSTATS()
            log_flag = True
        if 'L1DLRSPOWER' in log_option:
            __tm500_logging_L1DLRSPOWER()
            log_flag = True
        if 'MACTX' in log_option:
            __tm500_logging_MACTX()
            log_flag = True
        if 'MACRX' in log_option:
            __tm500_logging_MACRX()
            log_flag = True
        if 'SYSOVERVIEW' in log_option:
            __tm500_logging_SYSOVERVIEW()
            log_flag = True

        if 'L1RBPOWERS' in log_option:
            __tm500_logging_L1RBPOWERS()
            log_flag = True

        if 'ULHARQTX' in log_option:
            __tm500_logging_ULHARQTX()
            log_flag = True
        if 'L1CELLWATCH' in log_option:
            __tm500_logging_L1CELLWATCH()
            log_flag = True

        if not log_flag:
            __tm500_logging_ProtocolLog()
    else:
        __tm500_logging_ProtocolLog()

    __tm500_logging__LC_END()


def tm500_logging_select_from_file(log_file_path,
                                    log_option='ProtocolLog',
                                    number_of_ue='0',
                                    pause_time='0.5'):
    """This keyword will select TM500 logging types by your raw log file script.

    | Input Parameters | Man. | Description |
    | log_file_path    | Yes  | raw log file script path |
    | log_option       | No   | log types need to select |
    | number_of_ue     | No   | Number of UEs need to be logged, default is 0 which means single UE |

    Example
	| ${loggint_types} = | create list | DLSCHRX | ProtocolLog | CQIREPORTING |
    | tm500_logging_select_from_file  | d:\\tm500_log.txt  | ${logging_types} |

    Note: log types base on your log file content:
    if the content as follow, so there are two type support in log select, \
       and type must be "L1CELLHANDOVER" and "ProtocolLog", case sensitive.
    ----------------------------------------
    #$$LC_GRP 0 0 0 200 0 0 0 L1CELLHANDOVER
    #$$LC_CAT 3703 0 0 0 #GRP:L1CELLHANDOVER
    #$$LC_GRP 0 0 0 1 0 0 0 ProtocolLog
    #$$LC_CAT 1030 0 0 0 #GRP:ProtocolLog
    ----------------------------------------
    """
    file_content = file_read(log_file_path, "string")
    log_options = []
    if number_of_ue == '0':
        log_opt_cmds = ['#$$LC_CLEAR_ALL',
                        '#$$LC_UE_GROUP "" "0"',
                        '#$$LC_ITM 1 1 1 Manual']
        file_content_new = file_content.replace('UE All', 'UE 0')
    else:
        num = int(number_of_ue)-1
        log_opt_cmds = ['#$$LC_CLEAR_ALL',
                        '#$$LC_UE_GROUP "" "0-%s"' %num,
                        '#$$LC_ITM 1 1 1 Manual']
        file_content_new = file_content.replace('UE All', 'UE 0-%s'%num)
    file_content = file_content_new.splitlines()
    if not isinstance(log_option, list):
        log_options.append(str(log_option))
    else:
        log_options = log_option

    for content in file_content:
        for log in log_options:
            if log in content:
                log_opt_cmds.append(content.strip())
                break

    log_opt_cmds.append('#$$LC_ITM 0 0 0 Automatic')
    log_opt_cmds.append('#$$LC_END')
    old_pause_time = connections.set_pause_time(pause_time)

    ret = ''
    try:
        for cmd in log_opt_cmds:
            #print cmd
            ret += connections.execute_tm500_command_without_check(cmd, '2048', '0')
    finally:
        connections.set_pause_time(old_pause_time)
    return ret

if __name__ == '__main__':

    ret = tm500_logging_select_from_file("D:\\work\\all problems\\tm500log\\tm500.txt",
                                        ['ProtocolLog','RLCRXSTATS'])
    #print ret
    #TM500_CONVERT_TO_TEXT()
    pass
