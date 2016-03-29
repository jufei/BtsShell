import os, sys, re, time
from _winreg import OpenKey, CloseKey, QueryInfoKey, EnumKey, QueryValueEx, SetValueEx, REG_SZ, HKEY_LOCAL_MACHINE, KEY_ALL_ACCESS

def _get_system_network_info():
    networkinfo = {}
    if sys.platform == "win32":
        ethnet_flag = "adapter"
        device_flag = "Description"
        macaddr_flag = "Physical Address"
        
        ethnetname = devicename = macaddr = None
        pipe = os.popen(os.path.join(r'c:\windows\system32', 'ipconfig') + ' /all')
        for line in pipe:
            if ethnet_flag in line:
                ethnetname = line.split(":")[0].split(ethnet_flag)[-1].strip()
            if ethnetname != None and device_flag in line:
                devicename = line.split(':')[-1].strip()
            if devicename != None and macaddr_flag in line:
                temp_mac = line.split(':')[-1].strip()
                if re.match('^([0-9a-f][0-9a-f]-){5}[0-9a-f][0-9a-f]$', temp_mac, re.I):
                     macaddr = temp_mac
            if ethnetname != None and devicename != None and  macaddr != None:
                networkinfo[ethnetname] = devicename, macaddr
                ethnetname = devicename = macaddr = None                    
    else:
        for line in os.popen("/sbin/ifconfig"):
            if 'Ether' in line:
                value = line.split()[4]
                networkinfo.append(value)       
    return networkinfo

def restart_network_card(name):
    """This keyword is used to restart network card

    |  Input Parameters   | Man. | Description |
    |      name           | Yes  | network connection name  | 
    
    Example
    | restart_network_card  | BTS  |
    | restart_network_card  | LAB  |   
    """     
    shutdown_cmd = os.path.join(r'c:\windows\system32', 'netsh') + \
                 ' interface set interface name=%s admin=disabled' % name
    start_cmd = os.path.join(r'c:\windows\system32', 'netsh') + \
                     ' interface set interface name=%s admin=enabled' % name
    print "Exec cmd: ", shutdown_cmd
    if os.system(shutdown_cmd) == 0:
        print "Shutdown the network card %s success" % name
        time.sleep(2)
        print "Exec cmd: ", start_cmd
        if os.system(start_cmd) == 0:
            print "Restart the network card %s success" % name
            return
    print "Restart the network card failed !"
        

def modify_pc_mac_address(network_name, macaddress, restart_netcard=True):
    """This keyword is used to modify the PC mac address

    |  Input Parameters   | Man. | Description |
    |       network_name  | Yes  | network connection name |
    |       macaddress    | Yes  | The MAC address you want change to  |
    |  restart_netcard    | No   | whether restart the net card you given or not  |

    Example
    | modify_mac_address  | BTS  | E0-9D-31-26-8F-8D |
    | modify_mac_address  | LAB  | e09d31268f8d      |   
    """    
    MACADDRESS_KEY="SYSTEM\\CurrentControlSet\\Control\\Class\\{4D36E972-E325-11CE-BFC1-08002bE10318}"
    
    networkinfo = _get_system_network_info() #{network_name: (devicename, macaddr)}
    
    if not networkinfo.has_key(network_name):
        raise Exception, "The network name you given(%s) is not exists on this computer !" % network_name
    if re.match('^([0-9a-f][0-9a-f]-){5}[0-9a-f][0-9a-f]$', macaddress, re.I) or \
    re.match('^([0-9a-f][0-9a-f]){5}[0-9a-f][0-9a-f]$', macaddress, re.I): 
        pass
    else:
        raise Exception, "The macaddress you given is invalid ! Should be like E0-9D-31-26-8F-8D or e09d31268f8d"
        
    key = OpenKey(HKEY_LOCAL_MACHINE, MACADDRESS_KEY)
    countkey = QueryInfoKey(key)[0]
    keylist = []
    mackeyinfo = {}
    
    for i in range(int(countkey)):
        name = EnumKey(key, i) 
        keylist.append(name)
    CloseKey(key)
    
    for subkey in keylist:
        macaddress_subkey = MACADDRESS_KEY + '\\' + subkey
        try:
            mac_key = OpenKey(HKEY_LOCAL_MACHINE, macaddress_subkey)
            value, type = QueryValueEx(mac_key, "DriverDesc")
            for k, v in networkinfo.items():
                if v[0] == value:
                    currentmact = v[1]
                    mackeyinfo[macaddress_subkey] = value, currentmact #devicename, currentmact
                    print 'OrignalMacInfo >> %s: %s MAC: %s' %(subkey, value, currentmact)
                    break
        except Exception, e:
            #print "*WARN* ", e
            value='None'
        finally:
            CloseKey(mac_key)
    print "Start modify %s MAC address to %s" % (network_name, macaddress)
    for k in mackeyinfo.keys():
        if mackeyinfo[k][0] == networkinfo[network_name][0]:
            dest_key = k
    print "The registry key is: ", dest_key
    
    d_key=OpenKey(HKEY_LOCAL_MACHINE, dest_key, 0, KEY_ALL_ACCESS)
    SetValueEx(d_key,"NetworkAddress", 0, REG_SZ, macaddress)
    print "Mac address is modified success !"
    CloseKey(key)
    if restart_netcard:
        restart_network_card(network_name)

if __name__=='__main__':
    
    
#     modify_mac_address_by_device_name("Realtek RTL8139 Family PCI Fast Ethernet NIC", "00-27-19-8F-BB-05")
#     restart_network_card("bts")
    modify_pc_mac_address("WirelessNetwork", "E0-9D-31-26-8F-8A")
