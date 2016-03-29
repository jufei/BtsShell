import subprocess, time, os, sys, re
from BtsShell import connections
from datetime import datetime
from BtsShell.high_shell_lib.common_operation import _GetRuntimeVar
from BtsShell.file_lib.common_operation import copyfile2remote

class BackgroundPinger:
    def __init__(self):
        pass
        
    def start_traffic(self, host, options):
        self.host = host
        self.options = options
        self.conn_type = connections.get_current_connection_type()
        self.log_file = "ping_%s.txt" % (host.split('.')[-1])#,\
                        #datetime.now().strftime("%Y/%m/%d/%H:%M:%S"))
        self.cmd_file = "pingcmd_%s.cmd" % (host.split('.')[-1])
        connections.set_shell_timeout(2)
        if self.conn_type.upper().strip() == "WINDOWS":
            cmd = "ping %s %s > %s 2>&1" %(self.host, self.options, self.log_file)
            connections.execute_shell_command_without_check('cd \\')
            ret = connections.execute_shell_command_without_check("ls")
            if ret.find(self.log_file) > 0:
                connections.execute_shell_command_without_check("rm -f %s" % self.log_file)
            if ret.find(self.cmd_file) > 0:
                connections.execute_shell_command_without_check("rm -f %s" % self.cmd_file)
            old_prompt = connections.set_host_prompt("\r")
            connections.execute_shell_command_without_check("copy con %s" \
                                                           % self.cmd_file)
            connections.execute_shell_command_without_check('@echo off')
            #connections.execute_shell_command_without_check('if "%1" == "h" goto begin')
            #connections.execute_shell_command_without_check('mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit')            
            #connections.execute_shell_command_without_check(':begin')            
            connections.execute_shell_command_without_check(cmd)
            
            old_prompt = connections.set_host_prompt(old_prompt)
            connections.execute_shell_command_without_check("\x1a")            
            connections.execute_shell_command_without_check("start /min %s" % self.cmd_file)
            #connections.execute_shell_command_without_check("rm -f %s" % self.cmd_file)
        else:
            raise Exception("not supported connection type: %s" % self.conn_type)

    def stop_traffic(self):
        if self.conn_type.upper().strip() == "WINDOWS":
            connections.execute_shell_command_without_check('taskkill /f /im ping.exe')

    def analyse_result(self):
        sents = 0
        recvs = 0
        delays = []
        if self.conn_type.upper().strip() == "WINDOWS":
            connections.execute_shell_command_without_check('cd \\')
            connections.execute_shell_command_without_check('cat '+ self.log_file)
            #ret = connections.execute_shell_command_without_check('cat %s' % self.log_file)
            if _GetRuntimeVar("BTS_CONTROL_PC_LAB") == connections.BTSTELNET._current.host:
                ret = open("C:\\%s" %self.log_file, 'r').read()
            else:
                copyfile2remote(_GetRuntimeVar("BTS_CONTROL_PC_LAB"), _GetRuntimeVar("BTS_CONTROL_PC_USERNAME"), _GetRuntimeVar("BTS_CONTROL_PC_PASSWORD")\
                                ,"C:\\%s" % self.log_file, "C:\\%s" % self.log_file, "scp")
                ret = open("C:\\%s" %self.log_file, 'r').read()
            lines = ret.splitlines()
            for line in lines:
                if line.find("Request timed out") >= 0 or line.find("error") >= 0:
                    sents += 1
                    delays.append(0)
                elif line.find("Reply from") >= 0:
                    sents += 1
                    recvs += 1
                    delay_result = re.match('.*Reply from.*time[<|=](\d+)ms.*', line, re.I)
                    if delay_result:
                        delays.append(int(delay_result.group(1)))
            
            if delays.count(0) >= 1:
                maxd = None
                avgd = None
                for i in range(delays.count(0)):delays.remove(0)
                if len(delays) == 0:
                    mind = None
                else:
                    mind = min(delays)
            else:
                maxd = max(delays)
                mind = min(delays)
                avgd = float(sum(delays))/float(len(delays))
        return ([sents, recvs, int(sents-recvs)], [maxd, mind, avgd])
                

if __name__ == "__main__":
    connections.connect_to_host('10.69.71.114', 23, 'tdlte-tester', 'btstest')
    p = BackgroundPinger()
    p.start_traffic("192.168.255.1", "-n 100")
    time.sleep(10)
    p.stop_traffic()
    print p.analyse_result()
    connections.disconnect_from_host()
