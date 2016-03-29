import telnetlib, time, sys, os, random

class CTelnet:

    def __init__(self, host, port = 2323, prompt = '$', user = '', passwd = '', timeout = 10):
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
        
        os.system("TSKILL /A telnet")
        time.sleep(2)
        
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

            # Check if logined
            p_LoginPrompt = tn.read_until(self.prompt, self.timeout)
            print p_LoginPrompt
            if self.prompt not in p_LoginPrompt:
                print "ERR: Login prompt keyword '%s' is not in content!" % (self.prompt)
                return False
            
            #print tn.get_socket()
            self.tn = tn
            return True
        except:
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

        
    def SendCmd(self, command, RetKeyword = None):
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
            self.tn.write(command)
            p_Output = self.tn.read_until(self.prompt, self.timeout)
            print p_Output
            return p_Output

        except:
            print "Write command failure"
            return False



if __name__== '__main__':
    
    abc = CTelnet("192.168.254.129")
    abc.SendCmd('pwd')
