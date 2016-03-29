"""In order to totally control Sequans dongle, please input the correct parameters:

For Sequans: ue_control_script, com_port, frequency
    Altair: port, frequency, imsi, name
    CPE: ip, name
   """
from sequans_connection import SequansControl
from altair_connection import Altair_control
from altaircpe_connection import AltairCPEControl
from dmcpe_connection import DMCPE_Control
from qualcomm_connection import Qualcomm_control
from longcheercpe_connection import LCCPE_Control

import threading , time

##attach_result = {}
##detach_result = {}
##attached_ip = {}
##attached_status = {}
##attached_cellid = {}
##enablelte_result = {}
##address_list = []

def __connect_to_dongle(specified_dict):
    if specified_dict['NAME'].upper() =='ALTAIR_CPE':
        return AltairCPEControl(specified_dict)
    elif specified_dict['NAME'].upper() =='SEQUANS_DONGLE':
        return SequansControl(specified_dict)
    elif specified_dict['NAME'].upper() =='ALTAIR_DONGLE':
        return Altair_control(specified_dict)
    elif specified_dict['NAME'].upper() =='QUALCOMM_DONGLE':
        return Altair_control(specified_dict)
    elif specified_dict['NAME'].upper() =='DEMING_CPE':
        return DMCPE_Control(specified_dict)
    elif specified_dict['NAME'].upper() =='LONGCHEER_CPE':
        return LCCPE_Control(specified_dict)
    elif specified_dict['NAME'].upper() =='GEMTEK_CPE':
        pass
    else:
        raise Exception,"Pls input the right UE type, example: \'name=ALTAIR_CPE\'"

def __rset_global_var():
    global attach_result
    global detach_result
    global attached_ip
    global attached_status
    global attached_cellid
    global enablelte_result
    global atcmd_result
    global address_list
    global reboot_result
    attach_result = {}
    detach_result = {}
    attached_ip = {}
    attached_status = {}
    attached_cellid = {}
    enablelte_result = {}
    atcmd_result = {}
    reboot_result = {}
    address_list = []

    
def __parse_args(args):
    __rset_global_var()    
    ue_list = []
    address_list = []
    def _get_ue_list(args):
        for item in args:
            key,value = item.split('=')
            specified_dict[str(key).upper()]=str(value).upper()
            #CPE
            if key.upper()=='IP' and (str(value) not in address_list):
                address_list.append(str(value))
            #Altair-dongle
            if key.upper() =='PORT' and (str(value) not in address_list):
                address_list.append(str(value))                
        if not specified_dict.has_key('NAME'):
            specified_dict['NAME']='ALTAIR_CPE'
        return specified_dict, address_list

    for arg in args:
        specified_dict={}
        #[ue1_list, ue2_list]
        if not '=' in arg:
            for item in arg:
                key,value = item.split('=')
                specified_dict[str(key).upper()]=str(value).upper()
                if key.upper()=='IP' and (str(value) not in address_list):
                    address_list.append(str(value))
                if key.upper() == 'PORT' and  (str(value) not in address_list):
                    address_list.append(str(value))
            if not specified_dict.has_key('NAME'):
                specified_dict['NAME']='ALTAIR_CPE'
        #[1=2, 2=3]
        else:
            specified_dict, address_list = _get_ue_list(args)
        if not specified_dict in ue_list:
            ue_list.append(specified_dict)
    return ue_list, list(set(address_list))

def _dongle_attach(ue_dic,ue_address):
    try:
        obj = __connect_to_dongle(ue_dic)
        #attach_result[address] = obj.dongle_attach()
        ret = obj.dongle_attach()
    except Exception,e:
        ret = None
        raise e
    finally:
        attach_result[ue_address] = ret

def dongle_attach_without_check(args, Mulithread=False):
    """This keyword can be used to UE attach, till now can support Altair_cpe, Altair_dongle, sequans_dongle         
     Deming_cpe, Qualcomm_dongle   
    | Input Parameters       | Man. | Description |
    | args                   | Yes  | The sepecfic infomation of UE you want operate. |
    | Mulithread             | No   | Multithread flag, if you input a true value, it will \
                                      support multithread , Note that it will not display \
                                      specific process of attach when you open multithread |
    | Return value           | 0, attached; 1 not attached.
                               if you give a sequence of UE, will return a list of status by the sequence.|
    Example
    Should be defined in the BtsName.py file for every UE.
    #UE name can be : ALTAIR_DONGLE, ALTAIR_CPE, SEQUANS_DONGLE, GEMTEK_CPE, DEMING_CPE, QUALCOMM_DONGLE
    'UE1_INFO'      : ['name=ALTAIR_DONGLE', 'port=COM1', 'frequency=3800', 'imsi=8888888888888'],
    'UE2_INFO'      : ['name=ALTAIR_CPE', 'ip=192.168.255.101'],
    'UE3_INFO'      : ['name=SEQUANS_DONGLE', 'port=COM2', 'frequency=3800', 'imsi=6666666666666'],
    args = [ue1, ue2] or args = ue1
    | dongle_attach | args | 
    """
    ue_list, address_list= __parse_args(args)
    print ue_list,'**',address_list

    if Mulithread:
        try:
            th = []
            for i in range(len(ue_list)):
                t = threading.Thread(target=_dongle_attach,args=(ue_list[i],address_list[i]),name=i)
                th.append(t)
            for i in range(len(th)):
                th[i].start()
            for i in range(len(th)):
                th[i].join()
        finally:
            if len(attach_result) == 1:
                if attach_result[address_list[0]] != None:
                    return attach_result[address_list[0]]
                else:
                    raise Exception,"Attach failed."
            else:
                return [attach_result[item] for item in address_list]
    else:
        try:
            if len(ue_list) != 1:
                for i in range(len(ue_list)):
                    try:
                        _dongle_attach(ue_list[i],address_list[i])
                    except Exception,e:
                        print e
            else:
                _dongle_attach(ue_list[0],address_list[0])
        except Exception, e:
            print e
        finally:
            if len(attach_result) == 1:
                if attach_result[address_list[0]] in [None, 1]:
                    raise Exception,"Attach failed."
                else:
                    print "Attach successed !"
                    return attach_result[address_list[0]]
            else:
                return [attach_result[item] for item in address_list]
    print "All CPE have done."


def _dongle_detach(ue_dic,ue_address):
    try:
        obj = __connect_to_dongle(ue_dic)
        #attach_result[address] = obj.dongle_attach()
        ret = obj.dongle_detach()
    except Exception,e:
        ret = None
        raise e
    finally:
        detach_result[ue_address] = ret

def dongle_detach(args, Mulithread=False):
    """This keyword can be used to UE detach, till now can support CPE, Altair_dongle, sequans_dongle         
       For CPE, just disable Lte funcation.
       Usage and args is same as dongle_attach.
    """
    ue_list, address_list= __parse_args(args)
    print ue_list,'**',address_list
    if Mulithread:
        try:
            th = []
            for i in range(len(ue_list)):
                t = threading.Thread(target=_dongle_detach,args=(ue_list[i],address_list[i]),name=i)
                th.append(t)
            for i in range(len(th)):
                th[i].start()
            for i in range(len(th)):
                th[i].join()
        finally:
            if len(detach_result) == 1:
                if detach_result[address_list[0]] != None:
                    return detach_result[address_list[0]]
            else:
                return [detach_result[item] for item in address_list]
    else:
        try:
            if len(ue_list) != 1:
                for i in range(len(ue_list)):
                    try:
                        _dongle_detach(ue_list[i],address_list[i])
                    except Exception,e:
                        print e
            else:
                _dongle_detach(ue_list[0],address_list[0])
        except Exception, e:
            print e
        finally:
            if len(detach_result) == 1:
                if detach_result[address_list[0]] in [None, 1]:
                    raise Exception,"Detach failed."
                else:
                    print "Detach successed !"
                    return detach_result[address_list[0]]
            else:
                return [detach_result[item] for item in address_list]
    print "All CPE have done."

def get_dongle_ip_address(args, Mulithread=False):
    """This keyword can be used to get ue attached ip, till now can support CPE, Altair_dongle, sequans_dongle         
       Usage and args is same as dongle_attach. Only return the ip of ue.
    """
    ue_list, address_list= __parse_args(args)
    print ue_list,'**',address_list
    if Mulithread:
        try:
            th = []
            for i in range(len(ue_list)):
                t = threading.Thread(target=_get_dongle_ip_address,args=(ue_list[i],address_list[i]),name=i)
                th.append(t)
            for i in range(len(th)):
                th[i].start()
            for i in range(len(th)):
                th[i].join()
        finally:
            if len(attached_ip) == 1:
                if attached_ip[address_list[0]] != None:
                    return attached_ip[address_list[0]]
                else:
                    raise "Get dongle [%s] attached ip failed!" % address_list[0]
            else:
                return [attached_ip[item] for item in address_list]
    else:
        try:
            if len(ue_list) != 1:
                for i in range(len(ue_list)):
                    try:
                        _get_dongle_ip_address(ue_list[i],address_list[i])
                    except Exception,e:
                        print e
            else:
                _get_dongle_ip_address(ue_list[0],address_list[0])
        except Exception, e:
            print e
        finally:
            if len(attached_ip) == 1:
                if attached_ip[address_list[0]] != None:
                    return attached_ip[address_list[0]]
                else:
                    raise "Get dongle [%s] attached ip failed!" % address_list[0]
            else:
                return [attached_ip[item] for item in address_list]
    print "All CPE have done."

def _get_dongle_ip_address(ue_dic,ue_address):
    try:
        obj = __connect_to_dongle(ue_dic)
        ret = obj.get_dongle_ip_address()
    except Exception,e:
        ret = None
        raise e
    finally:
        attached_ip[ue_address] = ret

def _check_dongle_attach_status(ue_dic,ue_address):
    try:
        obj = __connect_to_dongle(ue_dic)
        ret = obj.check_dongle_attach_status()
    except Exception,e:
        ret = None
        raise e
    finally:
        attached_status[ue_address] = ret

def check_dongle_attach_status(args, Mulithread=False):
    """This keyword can be used to check ue attach status.till now can support CPE, sequans_dongle
       Usage and args is same as dongle_attach. Only will return the status of ue.
    """
    ue_list, address_list= __parse_args(args)
    print ue_list,'**',address_list

    if Mulithread:
        try:
            th = []
            for i in range(len(ue_list)):
                t = threading.Thread(target=_check_dongle_attach_status,args=(ue_list[i],address_list[i]),name=i)
                th.append(t)
            for i in range(len(th)):
                th[i].start()
            for i in range(len(th)):
                th[i].join()
        finally:
            if len(attached_status) == 1:
                if attached_status[address_list[0]] != None:
                    return attached_status[address_list[0]]
                else:
                    raise "Get dongle [%s] attach failed!" % address_list[0]
            else:
                return [attached_status[item] for item in address_list]
    else:
        try:
            if len(ue_list) != 1:
                for i in range(len(ue_list)):
                    try:
                        _check_dongle_attach_status(ue_list[i],address_list[i])
                    except Exception,e:
                        print e
            else:
                _check_dongle_attach_status(ue_list[0],address_list[0])
        except Exception, e:
            print e
        finally:
            if len(attached_status) == 1:
                if attached_status[address_list[0]] != None:
                    return attached_status[address_list[0]]
                else:
                    raise "Get dongle [%s] attach failed!" % address_list[0]
            else:
                return [attached_status[item] for item in address_list]
    print "All CPE have done."

def _get_attached_btscell_id(ue_dic, ue_address):
    try:
        obj = __connect_to_dongle(ue_dic)
        ret = obj.get_attached_btscell_id()
    except Exception,e:
        ret = None
        raise e
    finally:
        attached_cellid[ue_address] = ret

def get_attached_btscell_id(args, Mulithread=False):
    """This keyword can be used to get ue attached bts/cell id.till now can support CPE
       Usage and args is same as dongle_attach. Only will return the attached cellid of ue.
    """
    ue_list, address_list= __parse_args(args)
    print ue_list,'**',address_list
    if Mulithread:
        try:
            th = []
            for i in range(len(ue_list)):
                t = threading.Thread(target=_get_attached_btscell_id,args=(ue_list[i],address_list[i]),name=i)
                th.append(t)
            for i in range(len(th)):
                th[i].start()
            for i in range(len(th)):
                th[i].join()
        finally:
            if len(attached_cellid) == 1:
                if attached_cellid[address_list[0]] != None:
                    return attached_cellid[address_list[0]]
                else:
                    raise "Get dongle [%s] attached bts/cellid failed!" % address_list[0]
            else:
                return [attached_cellid[item] for item in address_list]
    else:
        try:
            if len(ue_list) != 1:
                for i in range(len(ue_list)):
                    try:
                        _get_attached_btscell_id(ue_list[i],address_list[i])
                    except Exception,e:
                        print e
            else:
                _get_attached_btscell_id(ue_list[0],address_list[0])
        except Exception, e:
            print e
        finally:
            if len(attached_cellid) == 1:
                if attached_cellid[address_list[0]] != None:
                    return attached_cellid[address_list[0]]
                else:
                    raise "Get dongle [%s] attached bts/cellid failed!" % address_list[0]
            else:
                return [attached_cellid[item] for item in address_list]
    print "All CPE have done."

def _enable_lte_funcation(ue_dic,ue_address):
    try:
        obj = __connect_to_dongle(ue_dic)
        #attach_result[address] = obj.dongle_attach()
        ret = obj.enable_lte_funcation()
    except Exception,e:
        ret = None
        raise e
    finally:
        enablelte_result[ue_address] = ret

def enable_lte_funcation(args, Mulithread=False):
    """This keyword can be used to enable CPE lte funcation. till now can support CPE
       Usage and args is same as dongle_attach. 
    """
    ue_list, address_list= __parse_args(args)
    print ue_list,'**',address_list
    if Mulithread:
        try:
            th = []
            for i in range(len(ue_list)):
                t = threading.Thread(target=_enable_lte_funcation,args=(ue_list[i],address_list[i]),name=i)
                th.append(t)
            for i in range(len(th)):
                th[i].start()
            for i in range(len(th)):
                th[i].join()
        finally:
            if len(enablelte_result) == 1:
                if enablelte_result[address_list[0]] != None:
                    return enablelte_result[address_list[0]]
                else:
                    raise "enableLte funcation failed [%s] !" % address_list[0]
            else:
                return [enablelte_result[item] for item in address_list]
    else:
        try:
            if len(ue_list) != 1:
                for i in range(len(ue_list)):
                    try:
                        _enable_lte_funcation(ue_list[i],address_list[i])
                    except Exception,e:
                        print e
            else:
                _enable_lte_funcation(ue_list[0],address_list[0])
        except Exception, e:
            print e
        finally:
            if len(enablelte_result) == 1:
                if enablelte_result[address_list[0]] in [None, 1]:
                    raise "enableLte funcation failed [%s] !" % address_list[0]
                else:
                    print "enableLte funcation successed !"
                    return enablelte_result[address_list[0]]
            else:
                return [enablelte_result[item] for item in address_list]
    print "All CPE have done."


def _execute_at_cmd_on_dongle(at_cmd, ue_dic, ue_address):
    try:
        obj = __connect_to_dongle(ue_dic)
        #attach_result[address] = obj.dongle_attach()
        ret = obj.execute_at_command(at_cmd)
    except Exception,e:
        ret = None
        raise e
    finally:
        atcmd_result[ue_address] = ret

def execute_at_cmd_on_dongle(args, at_cmd, Mulithread=False):
    """send stardand AT cmd to cpe, only support altair and Deming cpe.
    """
    at_cmd = str(at_cmd)
    ue_list, address_list= __parse_args(args)
    print ue_list,'**',address_list
    if Mulithread:
        try:
            th = []
            for i in range(len(ue_list)):
                t = threading.Thread(target=_execute_at_cmd_on_dongle,args=(at_cmd, ue_list[i], address_list[i]),name=i)
                th.append(t)
            for i in range(len(th)):
                th[i].start()
            for i in range(len(th)):
                th[i].join()
        finally:
            if len(atcmd_result) == 1:
                if atcmd_result[address_list[0]] != None:
                    return atcmd_result[address_list[0]]
                else:
                    raise "execute at command funcation failed [%s] !" % address_list[0]
            else:
                return [atcmd_result[item] for item in address_list]
    else:
        try:
            if len(ue_list) != 1:
                for i in range(len(ue_list)):
                    try:
                        _execute_at_cmd_on_dongle(at_cmd, ue_list[i],address_list[i])
                    except Exception,e:
                        print e
            else:
                _execute_at_cmd_on_dongle(at_cmd, ue_list[0],address_list[0])
        except Exception, e:
            print e
        finally:
            if len(atcmd_result) == 1:
                if atcmd_result[address_list[0]] != None:
                    return atcmd_result[address_list[0]]
                else:
                    raise "execute at command funcation failed [%s] !" % address_list[0]
            else:
                return [atcmd_result[item] for item in address_list]
    print "All CPE have done."

def _dongle_reboot(ue_dic,ue_address):
    try:
        obj = __connect_to_dongle(ue_dic)
        #attach_result[address] = obj.dongle_attach()
        ret = obj.dongle_reboot()
    except Exception,e:
        ret = None
        raise e
    finally:
        reboot_result[ue_address] = ret

def dongle_reboot(args, Mulithread=False):
    """This keyword is used for reboot cpe, only support dm and altair cpe.
    """
    ue_list, address_list= __parse_args(args)
    print ue_list,'**',address_list

    if Mulithread:
        try:
            th = []
            for i in range(len(ue_list)):
                t = threading.Thread(target=_dongle_reboot,args=(ue_list[i],address_list[i]),name=i)
                th.append(t)
            for i in range(len(th)):
                th[i].start()
            for i in range(len(th)):
                th[i].join()
        finally:
            if len(attach_result) == 1:
                if reboot_result[address_list[0]] != None:
                    return reboot_result[address_list[0]]
                else:
                    raise Exception,"Reboot failed."
            else:
                return [reboot_result[item] for item in address_list]
    else:
        try:
            if len(ue_list) != 1:
                for i in range(len(ue_list)):
                    try:
                        _dongle_reboot(ue_list[i],address_list[i])
                    except Exception,e:
                        print e
            else:
                _dongle_reboot(ue_list[0],address_list[0])
        except Exception, e:
            print e
        finally:
            if len(reboot_result) == 1:
                if reboot_result[address_list[0]] in [None, 1]:
                    raise Exception,"Reboot failed."
                else:
                    print "UE Reboot successed !"
                    return reboot_result[address_list[0]]
            else:
                return [reboot_result[item] for item in address_list]
    print "All CPE have done."

def set_cqi_ri(*args):
    obj,address = __connect_to_dongle(args)
    return obj.set_cqi_ri()

def dongle_attach(args, Mulithread=False):
    result = dongle_attach_without_check(args, Mulithread)
    list_num = len([i for i in args if isinstance(i, list)])
    ue_num = 1 if list_num == 0 else list_num
    if ue_num == 1:
        bts_cell = get_attached_btscell_id(args)
        btsid = bts_cell.split('/')[0]
        from BtsShell.high_shell_lib.common_operation import _GetRuntimeVar
        if btsid == str(_GetRuntimeVar('BTS_ID')):
            return result
        else:
            print "*WARN* Your UE have not attached to your BTS."
            print "*WARN* Attached to BTS:%s, the BTS you config is %s" %(btsid, _GetRuntimeVar('BTS_ID'))
            print "*INFO*  reboot and attach again."
            dongle_reboot(args)
            result = dongle_attach_without_check(args)
            bts_cell = get_attached_btscell_id(args)
            btsid = bts_cell.split('/')[0]
            if btsid == str(_GetRuntimeVar('BTS_ID')):
                return result
            else:
                raise Exception, """Your UE have not attached to your BTS again! Pls check !
Attached to BTS:%s, the BTS you config is %s""" %(btsid, _GetRuntimeVar('BTS_ID'))
    else:
        return result
            

if __name__ == '__main__':

    #AltairDongle-TEST
    #import sys

    #from BtsShell import connections
    #connections.connect_to_host('localhost', 23, 'tdlte-tester', '1')
    port = "COM5"
    args1= ['name=QUALCOMM_DONGLE', 'port=%s' %port]
    args2= ['name=LONGCHEER_CPE', 'ip=192.168.1.1']
    args3= ['name=DEMING_CPE', 'ip=192.168.0.1']
    
    #print dongle_reboot(args2)
    
    a = execute_at_cmd_on_dongle(args2, "AT%VER")
#    id = get_attached_btscell_id(args1)
#    b = dongle_detach(args1)
#    print a, id ,b
#    print dongle_reboot(args1)
    
    #connections.disconnect_from_host()
    """
    #CPE-TEST:
    #_dongle_attach({'IP': '192.168.255.201','NAME': 'CPE'},'192.168.255.201')
    #print dongle_attach(['name=CPE','ip=192.168.15.1'])
    print dongle_attach([['ip=192.168.15.1'],['name=CPE','ip=192.168.15.1']])
    print get_attached_btscell_id(['name=CPE','ip=192.168.15.1'])
    print check_dongle_attach_status(['name=CPE','ip=192.168.15.1'])
    print get_dongle_ip_address(['name=CPE','ip=192.168.15.1'])
    print dongle_detach(['name=CPE','ip=192.168.15.1'])
    print enable_lte_funcation(['name=CPE','ip=192.168.15.1'])
    #obj = CpeControl({'IP': '192.168.15.1'})
    #obj.enable_lte_funcation()
    """

