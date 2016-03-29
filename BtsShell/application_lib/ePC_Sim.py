import telnetlib, time, sys, os, random, traceback


USERPROMPT = "ogin:"
PASSWORDPROMPT = "assword:"


class CTelnet:

    def __init__(self, host, port = 23, prompt = '#', user = 'root', passwd = 'root', timeout = 10):
        self.host = host
        self.port = port
        self.prompt = prompt
        self.user = user
        self.passwd = passwd
        try:
            self.timeout = float(timeout)
        except:
            print "Timeout is not float type!"
            self.timeout = 10
        self.tn = None
        if self.Connect():
            print "Telnet socket setup success!"
        else:
            print "Telnet socket setup failure!"
            raise Exception, "Telnet socket setup failure!"
            
        if self.tn:
            print "CTelnet object initialize success!"
        else:
            print "CTelnet object initialize failed!"

   
    def Connect(self):
        """Setup telnet connection
            Input parameters:
                n/a
            Output parameters:
                1. True if success.
                    False if failed.
               
        """
        tn = None
        
        #os.system("TASKKILL /F /IM telnet*")
    
        #time.sleep(2)
        
        if os.system("ping %s -n 1 -w 3" % self.host) != 0:
            return False
        
        try:
            tn = telnetlib.Telnet(self.host, self.port)

        except:
            print "Open telnet connection error because of IP wrong or Port is accopied!"
            return False
        
        if not tn:
            print "Open telnet connection failure!"
            return False
        
        try:
            # Input User Name
            p_UserPrompt = tn.read_until(USERPROMPT, self.timeout)
            print p_UserPrompt
            if USERPROMPT not in p_UserPrompt:
                print "ERR: User name prompt keyword '%s' is not in content!" % (USERPROMPT)
                return False
            tn.write( self.user + "\r\n" )

            # Input Password
            p_PasswordPrompt = tn.read_until(PASSWORDPROMPT, self.timeout)
            print p_PasswordPrompt
            if PASSWORDPROMPT not in p_PasswordPrompt:
                print "ERR: Password prompt keyword '%s' is not in content!" % (PASSWORDPROMPT)
                return False
            tn.write( self.passwd + "\r\n" )

            # Check if logined
            p_LoginPrompt = tn.read_until(self.prompt, self.timeout)
            print p_LoginPrompt
            if "#" in p_LoginPrompt:
                self.tn = tn
                
            else:
                self.Disconnect()
                return False
                
            #print tn.get_socket()

            return True
        
        except Exception, e:
            traceback.print_exc()

            print e
            print "Telnet authentication failure!"
            return False



        
    def Disconnect(self):
        if self.tn:
            return self.tn.close()
        else:
            return True

    def __CheckConnectStatus(self):
        """Check telnet connection status
            Input:
                N/A
            Output:
                'True' if connection is alive
                'False' if connection is down
        """
        if not self.tn:
            print "Connection is down!"
            return False
        else:
            print "Connection is alive!"
            return True

        
    def SendCmd(self, command):
        """Send command in telnet socket connection
            Input:
                1. Command
            Output:
                True if execute success.
                False if execute failure.
        """
        if not self.__CheckConnectStatus():
            print "Non telnet connection!"
            return False

        if command == None or command == False:
            print "No valid command to run."
            return True
        else:
            command = str(command) + "\r\n"
            print self.prompt + command
            
        try:
            self.tn.read_very_eager() 
            self.tn.write(command)
            p_Output = self.tn.read_until(self.prompt, self.timeout)
            print p_Output
            return p_Output

        except:
            print "Write command failure"
            return False

    def SendCmdWithKeyWord(self, command, RetKeyword):
        """Send command in telnet socket connection
            Input:
                1. Command
            Output:
                True if execute success.
                False if execute failure.
        """
        if not self.__CheckConnectStatus():
            print "Non telnet connection!"
            return False

        if command == None or command == False:
            print "No valid command to run."
            return True
        else:
            command = str(command) + "\r\n"
            print self.prompt + command
            
        try:
            self.tn.read_very_eager()
            self.tn.write(command)
            p_Output = self.tn.read_until(RetKeyword, self.timeout)
            print p_Output
            return p_Output

        except:
            print "Write command failure"
            return False


def Connect_to_ePCSim_Server(host, username = 'root', password = 'root', timeout = 60):
    """ DEPRECATED Use "Connect to ePC Simulation Server" instead
    This function is used to connect to ePC Simulation server
    | Input Parameters | Man. | Description |
    |     host  | Yes  | IP of the ePC Simulation server |
    | username  |  No  | default is "root" |
    | password  |  No  | default is "root" |
    | timeout   |  No  | default is 60
    Example
    | Connect to ePC Simulation Server | 10.69.65.36 |
    """
    ePCSim_Connection = CTelnet(host, 23, '#', username, password, timeout)
    return ePCSim_Connection

def Start_ePCSim(ePCSim_conn, egate_port_number='20111', edaemon_port_number='10111'):
    """ DEPRECATED Use "Start ePC Simulation" instead
    This function is used to start ePC Simulation
    | Input Parameters | Man. | Description |
    | ePCSim_conn | Yes  | The handler returned from Connect_to_ePCSim_Server |
    | egate_port_number  |  No  | default is 20111 |
    | edaemon_port_number  |  No  | default is 10111 |
    Example
    | Start ePC Simulation | ePCSim_Connection | 20111 | 10111 |
    """
    ePCSim_conn.SendCmd("pkill egate")
    ePCSim_conn.SendCmd("pkill edaemon")
    ePCSim_conn.SendCmd("cd /home/epc_sim")
    ePCSim_conn.SendCmd("./egate --port " + egate_port_number)
    ePCSim_conn.SendCmd("./edaemon --port " + edaemon_port_number)
    ePCSim_conn.prompt = "EGATE>"
    ePCSim_conn.SendCmdWithKeyWord("telnet localhost 20111", "EGATE>")
    ePCSim_conn.SendCmdWithKeyWord("cfg file=epc.cfg", "CHANGE STATE: CONFIGURED")
    ePCSim_conn.SendCmdWithKeyWord("start", "CHANGE STATE: ACTIVE")

def Execute_ePCSim(ePCSim_conn, command):
    """ DEPRECATED Use "Execute ePC Simulation Command" instead
    This function is used to execute ePC Simulation command
    | Input Parameters | Man. | Description |
    | ePCSim_conn | Yes  | The handler returned from Connect_to_ePCSim_Server |
    | command  |  Yes | ePC Simulation command |
    Example
    | Execute ePC Simulation | ePCSim_Connection | info |
    """
    ePCSim_conn.prompt = "EGATE>"
    ePCSim_conn.SendCmd(command)

def Stop_ePCSim(ePCSim_conn):
    """ DEPRECATED Use "Stop ePC Simulation" instead
    This function is used to execute ePC Simulation command
    | Input Parameters | Man. | Description |
    | ePCSim_conn | Yes  | The handler returned from Connect_to_ePCSim_Server |
    Example
    | Stop ePC Simulation | ePCSim_Connection |
    """
    ePCSim_conn.SendCmd("exit")
    ePCSim_conn.prompt = "#"
    ePCSim_conn.SendCmd("pkill egate")
    ePCSim_conn.SendCmd("pkill edaemon")

def Disconnect_from_ePCSim_Server(ePCSim_conn):
    """ DEPRECATED Use "Disconnect from ePC Simulation Server" instead
    This function is used to execute ePC Simulation command
    | Input Parameters | Man. | Description |
    | ePCSim_conn | Yes  | The handler returned from Connect_to_ePCSim_Server |
    Example
    | Disconnect from ePC Simulation Server | ePCSim_Connection |
    """
    ePCSim_conn.Disconnect()


if __name__== '__main__':
    
    ePC = Connect_to_ePCSim_Server("10.69.65.36")
    Start_ePCSim(ePC,'20111','10111')
    Execute_ePCSim(ePC,"info")
    Execute_ePCSim(ePC,"ue_disp")
    Stop_ePCSim(ePC)
    Disconnect_from_ePCSim_Server(ePC)
