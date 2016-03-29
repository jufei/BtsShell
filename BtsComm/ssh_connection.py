#  $Id $

from robot import utils, utils
import telnetlib
#import select
from logger import Logger
import re
import thread
import os

class SshConnection:

    def __init__(self, host, port, prompt, timeout="10sec", newline='CRLF'):
        try:
            import paramiko
        except:
            raise RuntimeError("Can't import paramiko library, can't use ssh function.")
    
        port = port == '' and 22 or int(port)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #self.client.connect(host, port)
        self.host = host
        self.port = port
        self.channel = None    
        self._prompt = None
        self.set_prompt(prompt)
        self._timeout = float(utils.timestr_to_secs(timeout))
        self._newline = newline.upper().replace('LF','\n').replace('CR','\r')
        self._loglevel = "INFO"
        self._log_buffering = False
        self._log_buffer = ""

    def __str__(self):
        return str(self.host) + ":" + str(self.port) + " " + repr(self)

    def __del__(self):
        """Override ssh.__del__ because it sometimes causes problems"""
        pass

    def set_timeout(self, timeout):
        """Sets the timeout used in read operations to given value represented as timestr, e.g. "120 sec".

        The read operations will for this time before starting to read from
        the output. To run operations that take a long time to generate their
        complete output, this timeout must be set accordingly.
        """
        old = utils.secs_to_timestr(self._timeout)
        self._timeout = float(utils.timestr_to_secs(timeout))
        return old

    def set_loglevel(self, loglevel):
        old = self._loglevel
        self._loglevel = loglevel
        return old

    def close_connection(self, loglevel=None):
        """Closes current Ssh connection.

        Logs and returns possible output.
        """
        loglevel = loglevel == None and self._loglevel or loglevel
        self.client.close()       
        self._log("Disconnect from %s" % str(self), "INFO")
        return 

    def login(self, username, password, login_prompt='login: ',
              password_prompt='Password: '):
        """Logs in to SSH server with given user information.

        The login keyword reads from the connection until login_prompt is
        encountered and then types the username. Then it reads until
        password_prompt is encountered and types the password. The rest of the
        output (if any) is also read and all text that has been read is
        returned as a single string.

        Prompt used in this connection can also be given as optional arguments.
        """
        self.client.connect(self.host, self.port, username, password)        

    def write(self, text):
        """Writes given text over the connection and appends newline"""
        self.write_bare(text + self._newline)

    def write_bare(self, text):
        """Writes given text over the connection without appending newline"""
        try:
            text = str(text)
        except UnicodeError:
            msg = 'Only ascii characters are allowed in ssh. Got: %s' % text
            raise ValueError(msg)
        if self.channel is None:
            self.channel = self.client.invoke_shell()
            #TODO: Get timeout and log level here
            #TBD, hsun
            #print self.read_until(">", 30)
            #To get the stderr also to stdout
            self.channel.set_combine_stderr(True) 
        self.channel.sendall(text)

    def read_until(self, expected, timeout):
        data = ''
        start_time = time.time()
        while time.time() < float(timeout) + start_time :
            if self.channel.recv_ready():
                data += self.channel.recv(1)
            if data.count(expected) > 0:
                #print "data=", data, "."
                return data
        return data
    
    def read(self, loglevel=None):
        """Reads and returns/logs everything currently available on the output.

        Read message is always returned and logged but log level can be altered
        using optional argument. Available levels are TRACE, DEBUG, INFO and
        WARN.
        """
        loglevel = loglevel == None and self._loglevel or loglevel
        ret = self.read_very_eager()
        self._log(ret, loglevel)
        return ret
    def read_very_eager(self):
        if self.channel is None:
            return ""
        data = ''
        stime = time.time()
        while self.channel.recv_ready():
            data += self.channel.recv(100000)
        return data
    
    def read_until_prompt(self, loglevel=None):
        """Reads from the current output until prompt is found.

        Expected is a list of regular expressions, and keyword returns the text
        up until and including the first match to any of the regular
        expressions.
        """
        loglevel = loglevel == None and self._loglevel or loglevel 
        ret = self.expect(self._prompt, self._timeout)
        if ret[0] == -1 :
            self._log(ret[2],'INFO')
            raise AssertionError("No match found for prompt '%s'"
                                 % (utils.seq2str([x.pattern for x in self._prompt ], lastsep=' or ')))
        self._log(ret[2], loglevel)
        return ret[2]

    def set_prompt(self, *prompt):
        """Sets the prompt used in this connection to 'prompt'.

        'prompt' can also be a list of regular expressions
        """
        old_prompt = self._prompt
        if len(prompt) == 1:
            if isinstance(prompt[0], basestring):
                self._prompt = list(prompt)
            else:
                self._prompt = prompt[0]
        else:
            self._prompt = list(prompt)
        indices = range(len(self._prompt))    
        for i in indices:
            if isinstance(self._prompt[i], basestring):
                self._prompt[i] = re.compile(self._prompt[i], re.MULTILINE)
        return old_prompt

    def start_log_buffer(self):
        """ start copying the print outputs of _log into the log buffer """
        self._log_buffer = ""
        self._log_buffering = True

    def write_log_buffer(self, loglevel):
        """ print the log buffer with the specified loglevel and clear the buffer """
        if self._log_buffer:
            self._log_buffering = False
            self._log(self._log_buffer, loglevel)
            self._log_buffer = ""
            self._log_buffering = True

    def stop_log_buffer(self):
        """ stop copying the print output of _log into the log buffer and clear the buffer """
        self._log_buffering = False
        self._log_buffer = ""

    def _log(self, msg, loglevel=None):
        loglevel = loglevel == None and self._loglevel or loglevel
        msg = msg.strip()
        if msg != '' and loglevel is not None:
            print '*%s* %s' % (loglevel.upper(), msg)
        if self._log_buffering:
            self._log_buffer += msg
    def _remove_unused_char(self, data):
        i = 0;
        while i < len(data):
            if data[i] == chr(8):
                if i == 0:                        # BS is first element
                    data = data[1:]              # remove it form buffer and the last from the queue if not LF or CR           
                else:
                    if data[i-1] == chr(10) or data[i-1] == chr(13):
                        data = data[:i] + data[i + 1:]        # remove only BS from buffer
                    else:
                        data = data[:i-1] + data[i + 1:]      # remove BS and previous char from buffer
                        i = i - 1
            else:
                i = i + 1
        return data
                
    def expect(self, regexps, timeout=None):
        start_time = time.time()
        data = ''
        regexps = [ re.compile(expr) for expr in regexps ]
        while time.time() < start_time + int(timeout):
            if self.channel.recv_ready():                
                data += self.channel.recv(1)
                #print "recvdata=", data, "."
            matching_pattern = [ pattern for pattern in regexps 
                                 if pattern.search(data) ]
            if len(matching_pattern) > 0:
                pattern = matching_pattern[0]
                data = self._remove_unused_char(data)
                return (regexps.index(pattern), pattern.search(data), data)
        return (-1, None, data)