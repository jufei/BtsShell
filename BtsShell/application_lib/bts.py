from BtsShell import connections
import socket, time, os, re, traceback
from BtsShell.common_lib.get_path import *

import urllib2
import urllib
import base64

try:
    from RobotWS.CommonLib.logging import global_logger as log
except:
    class logger:
        def info(self, string):
            print "*INFO* %s" % string
    log = logger()

class FTMControl(object):
    def __init__(self, ftm_host, username, password):
        self.name = __name__
        self.ftm_host = ftm_host
        self.username = username
        self.password = password
        self.max_retry_times = 3
        self.retry_sleep_sec = 5
        socket.setdefaulttimeout(30)
        self._auth_encoded = base64.encodestring('%s:%s' % (username, password))[:-1]        
        
    def _get_req_data(self, service_type):
        url = "https://%s/protected/%s.html" % (self.ftm_host, service_type)
        req = urllib2.Request(url)
        req.add_header('Authorization', 'Basic %s' % self._auth_encoded)
        log.info("request on FTM: '%s'" % url)
        _, _, page_content = self._open_http_request(req, 1, 1)
        stamp = token = None
        for line in page_content.splitlines():
            if "name=stamp" in line:
                stamp = line.split('"')[1]
                continue
            if "name=token" in line:
                token = line.split('"')[1]
                break
        return stamp, token
        
    def _open_http_request(self, req, try_cnt, max_retry_times):
        try:
            response = urllib2.urlopen(req)
            return_code = response.getcode()
            page_content = response.read()
            log.info('try: %s/%s, http return code: %s' % (try_cnt, max_retry_times, return_code))
        except urllib2.HTTPError, http_e:
            response = None
            return_code = http_e.code
            log.info('try: %s/%s, http error code: %s' % (try_cnt, max_retry_times, return_code))
        return response, return_code, page_content

    def enable_ssh_on_fsm(self):
        """
        usage: enable_ssh_on_fsm
        Will try to enable the SSH service on FSM
        """
        return self.call_cgi_script_on_ftm("protected/enableSsh.cgi",
                                           service_type="sshservice")

    def disable_ssh_on_fsm(self):
        """
        usage: disable_ssh_on_fsm
        Will try to disable the SSH service on FSM
        """
        return self.call_cgi_script_on_ftm("protected/disableSsh.cgi",
                                           service_type="sshservice")

    def check_ssh_status(self):
        """
        usage: enable_ssh_on_fsm
        Will try to enable the R&D ports on FSM
        """
        return self.call_cgi_script_on_ftm("protected/sshServiceStatus.cgi", 
                                           service_type="sshservice")

    def check_rdport_status(self):
        """
        usage: enable_ssh_on_fsm
        Will try to disable the R&D ports on FSM
        """
        return self.call_cgi_script_on_ftm("protected/rndPortServiceStatus.cgi", 
                                           service_type="RndPortsService")    
    
    def enable_rdport_on_fsm(self):
        """
        usage: enable_ssh_on_fsm
        Will try to enable the R&D ports on FSM
        """
        return self.call_cgi_script_on_ftm("protected/enableRndPorts.cgi",
                                           service_type="RndPortsService")

    def disable_rdport_on_fsm(self):
        """
        usage: enable_ssh_on_fsm
        Will try to disable the R&D ports on FSM
        """
        return self.call_cgi_script_on_ftm("protected/disableRndPorts.cgi",
                                           service_type="RndPortsService")

    def call_cgi_script_on_ftm(self, url_suffix, service_type):
        """
        usage: call_cgi_script_on_ftm(url_suffix)
        Will authenticate on FTM and call the CGI script at location
         "https://192.168.255.129/" + <url_suffix>"
        """
        proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)  
        stamp, token = self._get_req_data(service_type)
        url_prefix = "https://%s/" % self.ftm_host
        req_data = {"stamp" : stamp,
                    "token" : token, 
                    "frame" : service_type}
        data_suffix = urllib.urlencode(req_data)
        url = "%s%s?%s" % (url_prefix, url_suffix, data_suffix)
        
        log.info("Calling CGI script on FTM: '%s'" % url)
        req = urllib2.Request(url)
        req.add_header('Authorization', 'Basic %s' % self._auth_encoded)
        
        try_cnt = 0
        response = None 
        max_retry_times = self.max_retry_times
        retry_sleep_sec = self.retry_sleep_sec

        while not response and try_cnt < max_retry_times:
            try_cnt += 1
            try:
                response, _ret_code, page_content = self._open_http_request(req, 
                                                                            try_cnt, 
                                                                            max_retry_times)
            except Exception, error:
                response = None               
                log.info('try: %s/%s, urlib2 exception: %s' % (try_cnt, max_retry_times, error))
            if not response and try_cnt < max_retry_times:
                log.info("waiting %s seconds before next retry ..." % retry_sleep_sec)
                time.sleep(retry_sleep_sec)
        if response:
            log.info(page_content)
            return page_content
        else:
            raise Exception("Open '%s' failed!" % url)

def bts_ssh_and_rd_port_operate(ssh_rnd, enable_disable_check, user='Nemuadmin',\
                                     pwd='nemuuser',host='192.168.255.129',):
    """This keyword enable/disable SSH/RND port.

    | Input Paramaters      | Man. | Description |
    | ssh_rnd               | yes  | 0--ssh     1--RnD_port 2--ssh&RnD_port |
    | enable_disable_check  | yes  | 0--disable 1--enable   2--check |
    | user                  | No   | default is 'Nemuadmin' |
    | pwd                   | No   | default is 'nemuuser' |
    | host                  | No   | default is '192.168.255.129' |
    Example
    | bts_ssh_and_rd_port_operate | 0 | 1 | #enable bts ssh |
    | bts_ssh_and_rd_port_operate | 1 | 1 | #enable bts RD port |
    | bts_ssh_and_rd_port_operate | 2 | 1 | #enable bts SSH and RD port |
    | bts_ssh_and_rd_port_operate | 0 | 0 | #disable bts ssh |
    | bts_ssh_and_rd_port_operate | 1 | 0 | #disable bts RD port |
    | bts_ssh_and_rd_port_operate | 2 | 0 | #disable bts SSH and RD port |
    | bts_ssh_and_rd_port_operate | 0 | 2 | #check bts ssh |
    | bts_ssh_and_rd_port_operate | 1 | 2 | #check bts RD port |
    | bts_ssh_and_rd_port_operate | 2 | 2 | #check bts SSH and RD port |
    """
    
    ftm_ctrl = FTMControl(host, user, pwd)
    
    enable_disable_check = int(enable_disable_check.strip())
    ssh_rnd = int(ssh_rnd.strip())
    if 1 == enable_disable_check:
        if 0 == ssh_rnd :
            ret = ftm_ctrl.enable_ssh_on_fsm()
        elif 1 == ssh_rnd :
            ret = ftm_ctrl.enable_rdport_on_fsm()
        elif 2 == ssh_rnd :
            ret1 = ftm_ctrl.enable_ssh_on_fsm()
            ret2 = ftm_ctrl.enable_rdport_on_fsm()
            ret = ret1+"\n"+ret2
        else:
            raise Exception, "Please check your arg1, should be 0/1/2"

    elif 0 == enable_disable_check:
        if 0 == ssh_rnd:
            ret = ftm_ctrl.disable_ssh_on_fsm()
        elif 1 == ssh_rnd:
            ret = ftm_ctrl.disable_rdport_on_fsm()
        elif 2 == ssh_rnd:
            ret1 = ftm_ctrl.disable_ssh_on_fsm()
            ret2 = ftm_ctrl.disable_rdport_on_fsm()
            ret = ret1+"\n"+ret2
        else:
            raise Exception, "Please check your arg1, should be 0/1/2"
    elif 2 == enable_disable_check:
        if 0 == ssh_rnd:
            ret = ftm_ctrl.check_ssh_status()
        elif 1 == ssh_rnd:
            ret = ftm_ctrl.check_rdport_status()
        elif 2 == ssh_rnd:
            ret1 = ftm_ctrl.check_ssh_status()
            ret2 = ftm_ctrl.check_rdport_status()
            ret = ret1+"\n"+ret2
        else:
            raise Exception, "Please check your arg1, should be 0/1/2"
    else:
        raise Exception, "Please check your arg2, should be 0/1/2"
    return ret

def _bts_ssh_and_rd_port_operate(ssh_rnd, enable_disable_check, user='Nemuadmin',\
                                     pwd='nemuuser',host='192.168.255.129',):
    """This keyword enable/disable SSH/RND port.

    | Input Paramaters      | Man. | Description |
    | ssh_rnd               | yes  | 0--ssh     1--RnD_port 2--ssh&RnD_port |
    | enable_disable_check  | yes  | 0--disable 1--enable   2--check |
    | user                  | No   | default is 'Nemuadmin' |
    | pwd                   | No   | default is 'nemuuser' |
    | host                  | No   | default is '192.168.255.129' |
    Example
    | bts_ssh_and_rd_port_operate | 0 | 1 | #enable bts ssh |
    | bts_ssh_and_rd_port_operate | 1 | 1 | #enable bts RD port |
    | bts_ssh_and_rd_port_operate | 2 | 1 | #enable bts SSH and RD port |
    | bts_ssh_and_rd_port_operate | 0 | 0 | #disable bts ssh |
    | bts_ssh_and_rd_port_operate | 1 | 0 | #disable bts RD port |
    | bts_ssh_and_rd_port_operate | 2 | 0 | #disable bts SSH and RD port |
    | bts_ssh_and_rd_port_operate | 0 | 2 | #check bts ssh |
    | bts_ssh_and_rd_port_operate | 1 | 2 | #check bts RD port |
    | bts_ssh_and_rd_port_operate | 2 | 2 | #check bts SSH and RD port |
    """
    wget_exe = os.path.join(get_tools_path(), "wget.exe")
    wget_path = wget_exe + \
    " --user=%s --password=%s --no-check-certificate https://%s/protected/"\
                %(user,pwd, host)
    wget_option = " -t 1 --timeout=10 -q -O -"

    enable_ssh = "enableSsh.cgi"
    disable_ssh = "disableSsh.cgi"
    check_ssh = "sshServiceStatus.cgi"
    enable_rd_port = "enableRndPorts.cgi"
    disable_rd_port = "disableRndPorts.cgi"
    check_rd_port = "rndPortServiceStatus.cgi"

    enable_ssh_cmd = wget_path + enable_ssh + wget_option
    disable_ssh_cmd = wget_path + disable_ssh + wget_option
    check_ssh_cmd = wget_path + check_ssh + wget_option
    enable_rd_port_cmd = wget_path + enable_rd_port + wget_option
    disable_rd_port_cmd = wget_path + disable_rd_port + wget_option
    check_rd_port_cmd = wget_path + check_rd_port + wget_option

    enable_disable_check = int(enable_disable_check.strip())
    ssh_rnd = int(ssh_rnd.strip())
    if 1 == enable_disable_check:
        if 0 == ssh_rnd :
            ret = connections.execute_shell_command(enable_ssh_cmd)
        elif 1 == ssh_rnd :
            ret = connections.execute_shell_command(enable_rd_port_cmd)
        elif 2 == ssh_rnd :
            ret1 = connections.execute_shell_command(enable_ssh_cmd)
            ret2 = connections.execute_shell_command(enable_rd_port_cmd)
            ret = ret1+"\n"+ret2
        else:
            raise Exception, "Please check your arg1, should be 0/1/2"

    elif 0 == enable_disable_check:
        if 0 == ssh_rnd:
            ret = connections.execute_shell_command(disable_ssh_cmd)
        elif 1 == ssh_rnd:
            ret = connections.execute_shell_command(disable_rd_port_cmd)
        elif 2 == ssh_rnd:
            ret1 = connections.execute_shell_command(disable_ssh_cmd)
            ret2 = connections.execute_shell_command(disable_rd_port_cmd)
            ret = ret1+"\n"+ret2
        else:
            raise Exception, "Please check your arg1, should be 0/1/2"
    elif 2 == enable_disable_check:
        if 0 == ssh_rnd:
            ret = connections.execute_shell_command(check_ssh_cmd)
        elif 1 == ssh_rnd:
            ret = connections.execute_shell_command(check_rd_port_cmd)
        elif 2 == ssh_rnd:
            ret1 = connections.execute_shell_command(check_ssh_cmd)
            ret2 = connections.execute_shell_command(check_rd_port_cmd)
            ret = ret1+"\n"+ret2
        else:
            raise Exception, "Please check your arg1, should be 0/1/2"
    else:
        raise Exception, "Please check your arg2, should be 0/1/2"
    return ret


def set_rd_parameter(msg):
    """This keyword used to set R&D parameter.

    | Input Paramaters      | Man. | Description |
    | msg                   | yes  |wireshark mesage |
    Example
    | set_rd_parameter | '00:00:20:11:12:31:16:06:12:31:16:06:00:1c:00:00:00:00:00:03:00:00:00:01:00:00:00:00' |
    | set_rd_parameter | '00 00 20 11 12 31 16 06 12 31 16 06 00 1c 00 00 00 00 00 03 00 00 00 01 00 00 00 00' |

    """
    host = '192.168.255.1'
    port = 15004
    
    def generate_mesg(wireshark_mesg):
        spliter = re.match("\d{2}([ :])\d{2}", wireshark_mesg.strip()).group(1)
        hex_list = wireshark_mesg.split(spliter)
        return ''.join([chr(int(item,16))for item in hex_list])
    
    try:
        mesg = generate_mesg(msg)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5) 
        sock.connect((host, int(port)))
        sock.send(mesg)
        time.sleep(1)
        try:
            ret = sock.recv(1024)
            print '**',str(ret) ,'**'
        except:
            print "Read socket error: \n",
            traceback.print_exc()
        print "Set RD parameter successed !"
    except Exception, e:
        print '**ERROR**: Send msg failed: \"%s\"' % (mesg)
        raise e
    finally:
        sock.close()

def get_oms_version(ip, user, pwd, su_pwd='nsn'):  
    """This keyword return oms version.

    | Input Paramaters      | Man. | Description |
    | ip                    | yes  | oms ip information |
    | user                  | yes  | login username |
    | pwd                   | yes  | login password |
    | su_pwd                | No  | su root password, defaul as 'nsn' |            
    Example
    | get_oms_version | 10.68.160.250 | Nemuadmin | nemuuser |
    
    print as <OMS version is $$CLA-0	R_GOMS7_1.3.2.0.release_oms.corr2$$>
    """      
    connections.connect_to_ssh_host(ip, 22, user, pwd, prompt='$')
    connections.set_ssh_prompt('word:')
    connections.execute_ssh_command_without_check('su -')    
    connections.set_ssh_prompt('#')
    connections.execute_ssh_command_without_check(su_pwd) 
    ret = connections.execute_ssh_command_without_check("currentset") 
    lines = ret.splitlines()
    for line in lines:
        if line.startswith('CLA'):
            print "OMS version is $$%s$$" % line            
            return line
    raise Exception("Get OMS version failed")

def get_netact_version(ip, user, pwd, 
                        big_version_tag='netact/',                         
                        prompt='~]$'):    
    """This keyword return netact version.

    | Input Paramaters      | Man. | Description |
    | ip                    | yes  | netact ip information |
    | user                  | yes  | login username |
    | pwd                   | yes  | login password |
    | big_version_tag       | No   | default as 'netact/'| 
    | prompt                | No   | defaul as '~]$' |            
    Example
    | get_netact_version | 10.91.102.112 | omc2 | zhouhang2 |
    
    20140828 test on 10.91.102.112 return value as:        
        netact/product/14.7.1.3263
        netact_cup/14.7.1.3263/14.7.1.3263.482
        
    print as <Netact version is $$14.7.0.9.3084_54213$$>  First version
    print as <Netact version is $$14.7.1.3263_14.7.1.3263.482$$>  Second version
    """     
    connections.connect_to_ssh_host(ip, 22, user, pwd, prompt)
    ret = connections.execute_ssh_command_without_check('cat /etc/mpp-netact-release')
    lines = ret.splitlines()[1:-1]
    tmp = ''
    for line in lines:
        tmp += line + '; '
    print "Netact version is $$%s$$" % (tmp)
    return lines


if __name__ == '__main__':
    print bts_ssh_and_rd_port_operate("2", "1", host="10.69.66.132")