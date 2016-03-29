from BtsShell import connections
import re
import time

class _EMSsim:
    osprompt = None
    screenname = None
    
    @classmethod
    def close_session(cls):
        if not cls.is_session_exist():
            return True
        cls.enter_session()
        connections.execute_ssh_command_bare("q\r")
        time.sleep(1)
        connections.get_ssh_recv_content()
        if cls.is_session_exist():
            respat = re.compile("(?im)^\s*(\d+)\.%s.*" % cls.screenname)
            res_result = respat.search(connections.execute_ssh_command_without_check("screen -ls"))
            if res_result:
                session_pid = res_result.group(1)
            connections.execute_ssh_command_without_check("kill -9 %s" % session_pid)
            connections.execute_ssh_command_without_check("screen -wipe")
            if cls.is_session_exist():
                print "*WARN* Close emssim session failed !"
                return False
            print "Close emssim session succeed."
            return True
        return True
        
    @staticmethod        
    def is_session_exist():
        ret = connections.execute_ssh_command_without_check("screen -ls")
        if "No Sockets found" not in ret :
            return True
        else:
            print "No session exist !"
            return False
        
    @classmethod  
    def enter_session(cls):
        connections.execute_ssh_command_bare("screen -S %s -d\r" % cls.screenname)
        time.sleep(1)
        connections.get_ssh_recv_content()
        connections.execute_ssh_command_bare("screen -S %s -r\r" % cls.screenname)
        time.sleep(1)
        ret = connections.get_ssh_recv_content()     
        return ret
    
    @classmethod    
    def detach_session(cls):
        ctrl_a = chr(int(1))
        connections.execute_ssh_command_bare(ctrl_a + 'd' + '\r')
        time.sleep(1)
        q_ret = connections.get_ssh_recv_content()
       
#        connections.execute_ssh_command_bare("!screen -S %s -d\r" % cls.screenname)
#        time.sleep(1)
#        q_ret = connections.get_ssh_recv_content()
        if ("detached" in q_ret.lower()) and ("error" not in q_ret.lower()):
            print "Quit EMSsim screen success !"
        else:
            print "*WARN* Quit EMSsim screen failed !"
        return q_ret
    
def connect_to_emssim_server(host, port=22, user="flexi34", passwd="flexi34", prompt=".*\$$", timeout=15):
    if isinstance(prompt, basestring):
        prompt = re.compile(prompt)
    _EMSsim.osprompt = prompt
    _EMSsim.screenname = "emssim_%s" % user
    return connections.connect_to_ssh_host(host, port, user, passwd, prompt, timeout)
    
def start_emssim():
    screen_name = _EMSsim.screenname
    cmd = "screen -S %s -d -m ./start -MARK_CMD 1" % screen_name
    connections.execute_ssh_command_without_check("cd ~")
    #connections.execute_ssh_command_without_check("ls -al --color=no")
    old_prompt = connections.SSHCONNECTION._current._prompt
    if not isinstance(old_prompt, basestring):
        old_pattern = old_prompt.pattern
    print "*INFO* Old prompt is '%s'" % old_pattern
    
    _EMSsim.close_session()
    connections.execute_ssh_command_without_check(cmd)
    if _EMSsim.is_session_exist():
        print "EMSsim screen started success !"
    else:
        raise Exception, "EMSsim screen started failed !"
    start_ret = _EMSsim.enter_session()
    check_points = ["Created BTS", "Connected", "FBOX", "|Received Flexi IP"]
    for cp in check_points:
        if cp not in start_ret:
            print "*WARN* The EMSsim start failed ! flag \"%s\" not found." % cp
            raise Exception, "EMSsim start failed !"
    print "*INFO* EMSsim start up success !"
    _EMSsim.detach_session()
    time.sleep(30)
    
def stop_emssim():
    _EMSsim.close_session()

def execute_emssim_command(cmd):
    if not _EMSsim.is_session_exist():
        raise Exception, "emssim session is not started!"
    _EMSsim.enter_session()
    old_prompt = connections.set_ssh_prompt(re.compile(">\|#..*"))
    old_timeout = connections.set_ssh_timeout(120)
    try:
        exec_ret = connections.execute_ssh_command_without_check(cmd)
        success_cp = ">|#S"
        failed_points = ">|#F"
        if failed_points in exec_ret:
            raise Exception, "EMSsim cmd('%s') executed failed !" %(cmd)
        if success_cp not in exec_ret:
            raise Exception, "EMSsim cmd('%s') executed failed !" %(cmd)
    except Exception, e:
        raise e
    finally:
        connections.set_ssh_prompt(old_prompt)
        connections.set_ssh_timeout(old_timeout)
        _EMSsim.detach_session()
    print "*INFO* EMSsim cmd(%s) executed success !" %(cmd)
    return exec_ret

if __name__ == "__main__":

    connect_to_emssim_server("10.68.179.237")
    #connect_to_emssim_server("10.69.65.36", 22, "root", "root", "#")
    start_emssim()
    
    time.sleep(5)

    ret = execute_emssim_command("ls")
    ret = execute_emssim_command("discover")

    stop_emssim()
    print "++++++++++++"
    print ret
    connections.disconnect_from_ssh()