#  Copyright 2008-2013 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import re
import sys
import inspect
import traceback
from StringIO import StringIO
from SimpleXMLRPCServer import SimpleXMLRPCServer
from xmlrpclib import Binary
try:
    import signal
except ImportError:
    signal = None
try:
    from collections import Mapping
except ImportError:
    Mapping = dict


BINARY = re.compile('[\x00-\x08\x0B\x0C\x0E-\x1F]')


class RobotRemoteServer(SimpleXMLRPCServer):
    allow_reuse_address = True

    def __init__(self, library, host='127.0.0.1', port=8270, allow_stop=True):
        SimpleXMLRPCServer.__init__(self, (host, int(port)), logRequests=False)
        self._library = library
        self._allow_stop = allow_stop
        self._shutdown = False
        self._register_functions()
        self._register_signal_handlers()
        self._log('Robot Framework remote server starting at %s:%s'
                  % (host, port))
        self.serve_forever()

    def _register_functions(self):
        self.register_function(self.get_keyword_names)
        self.register_function(self.run_keyword)
        self.register_function(self.get_keyword_arguments)
        self.register_function(self.get_keyword_documentation)
        self.register_function(self.stop_remote_server)

    def _register_signal_handlers(self):
        def stop_with_signal(signum, frame):
            self._allow_stop = True
            self.stop_remote_server()
        if hasattr(signal, 'SIGHUP'):
            signal.signal(signal.SIGHUP, stop_with_signal)
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, stop_with_signal)

    def serve_forever(self):
        while not self._shutdown:
            self.handle_request()

    def stop_remote_server(self):
        prefix = 'Robot Framework remote server at %s:%s ' % self.server_address
        if self._allow_stop:
            self._log(prefix + 'stopping')
            self._shutdown = True
        else:
            self._log(prefix + 'does not allow stopping', 'WARN')
        return True

    def get_keyword_names(self):
        get_kw_names = getattr(self._library, 'get_keyword_names', None) or \
                       getattr(self._library, 'getKeywordNames', None)
        if inspect.isroutine(get_kw_names):
            names = get_kw_names()
        else:
            names = [attr for attr in dir(self._library) if attr[0] != '_'
                     and inspect.isroutine(getattr(self._library, attr))]
        return names + ['stop_remote_server']

    def run_keyword(self, name, args, kwargs=None):
        args, kwargs = self._handle_binary_args(args, kwargs or {})
        result = {'status': 'PASS', 'return': '', 'output': '',
                  'error': '', 'traceback': ''}
        self._intercept_stdout()
        try:
            return_value = self._get_keyword(name)(*args, **kwargs)
        except:
            result['status'] = 'FAIL'
            result['error'], result['traceback'] = self._get_error_details()
        else:
            result['return'] = self._handle_return_value(return_value)
        result['output'] = self._restore_stdout()
        return result

    def _handle_binary_args(self, args, kwargs):
        args = [self._handle_binary_arg(a) for a in args]
        kwargs = dict([(k, self._handle_binary_arg(v)) for k, v in kwargs.items()])
        return args, kwargs

    def _handle_binary_arg(self, arg):
        return arg if not isinstance(arg, Binary) else str(arg)

    def get_keyword_arguments(self, name):
        kw = self._get_keyword(name)
        if not kw:
            return []
        return self._arguments_from_kw(kw)

    def _arguments_from_kw(self, kw):
        args, varargs, kwargs, defaults = inspect.getargspec(kw)
        if inspect.ismethod(kw):
            args = args[1:]  # drop 'self'
        if defaults:
            args, names = args[:-len(defaults)], args[-len(defaults):]
            args += ['%s=%s' % (n, d) for n, d in zip(names, defaults)]
        if varargs:
            args.append('*%s' % varargs)
        if kwargs:
            args.append('**%s' % kwargs)
        return args

    def get_keyword_documentation(self, name):
        if name == '__intro__':
            return inspect.getdoc(self._library) or ''
        if name == '__init__' and inspect.ismodule(self._library):
            return ''
        return inspect.getdoc(self._get_keyword(name)) or ''

    def _get_keyword(self, name):
        if name == 'stop_remote_server':
            return self.stop_remote_server
        kw = getattr(self._library, name, None)
        if inspect.isroutine(kw):
            return kw
        return None

    def _get_error_details(self):
        exc_type, exc_value, exc_tb = sys.exc_info()
        if exc_type in (SystemExit, KeyboardInterrupt):
            self._restore_stdout()
            raise
        return (self._get_error_message(exc_type, exc_value),
                self._get_error_traceback(exc_tb))

    def _get_error_message(self, exc_type, exc_value):
        name = exc_type.__name__
        message = str(exc_value)
        if not message:
            return name
        if name in ('AssertionError', 'RuntimeError', 'Exception'):
            return message
        return '%s: %s' % (name, message)

    def _get_error_traceback(self, exc_tb):
        # Latest entry originates from this class so it can be removed
        entries = traceback.extract_tb(exc_tb)[1:]
        trace = ''.join(traceback.format_list(entries))
        return 'Traceback (most recent call last):\n' + trace

    def _handle_return_value(self, ret):
        if isinstance(ret, basestring):
            return self._handle_binary_result(ret)
        if isinstance(ret, (int, long, float)):
            return ret
        if isinstance(ret, Mapping):
            return dict([(self._str(key), self._handle_return_value(value))
                         for key, value in ret.items()])
        try:
            return [self._handle_return_value(item) for item in ret]
        except TypeError:
            return self._str(ret)

    def _handle_binary_result(self, result):
        if not BINARY.search(result):
            return result
        try:
            result = str(result)
        except UnicodeError:
            raise ValueError("Cannot represent %r as binary." % result)
        return Binary(result)

    def _str(self, item):
        if item is None:
            return ''
        return str(item)

    def _intercept_stdout(self):
        # TODO: What about stderr?
        sys.stdout = StringIO()

    def _restore_stdout(self):
        output = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        return self._handle_binary_result(output)

    def _log(self, msg, level=None):
        if level:
            msg = '*%s* %s' % (level.upper(), msg)
        print msg
        global LOGPATH
        print >> file(os.path.join(LOGPATH, "robotRemoteserver.log"), "a"), msg
        

class RobotRemoteServerException(Exception):
    """RobotRemoteServerException"""
    pass


def parse_parameters():
    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option("-l", "--library", action="store", type="string", dest="library")
    parser.add_option("-i", "--ip", action="store", type="string", dest="host")
    parser.add_option("-p", "--port", action="store", type="string", dest="port")
    parser.add_option("-s", "--allow_stop", action="store", type="string", dest="allow_stop")

    (options, args) = parser.parse_args()

    lib_name = "BtsShell"
    if options.library:
        lib_name = options.library  
        try:
            library = __import__(lib_name)
        except:
            pass
        
        if not callable(library):
            try:
                #exec("from %s import %s as %s" %(lib_name, lib_name, lib_name))
                library = getattr(library, lib_name)
            except:
                pass
    
        if not callable(library):
            raise RobotRemoteServerException("library you given can not be imported !")         
        else:
            inst = library()
    else:
        from BtsShell import BtsShell
        inst = BtsShell()

    if options.host:
        host = options.host
    else:
        import socket
        ips = socket.gethostbyname_ex(socket.gethostname())[-1]
        for ip in ips:
            if ip.startswith("10."):
                host = ip
                break
        else:
            host = ips[0]
            
    if options.port:
        port = options.port
    else:
        port = 8270

    if options.allow_stop:
        allow_stop = options.allow_stop
    else:
        allow_stop = True

    return inst, host, port, allow_stop, lib_name

import os, platform

def createLogFolder(lib_name):
    systype = platform.system()
    if systype == "Windows":
        rootpath = os.path.abspath("C:\\")
    else:
        rootpath = os.path.abspath("/")
    logpath = os.path.join(rootpath, lib_name + "_RemoteLog") 
    try:
        if os.path.exists(logpath):
            __import__('shutil').rmtree(logpath)
        os.mkdir(logpath)
    except:
        pass
    return logpath
    
if __name__ == "__main__":
    inst, host, port, allow_stop, lib_name = parse_parameters()
    global LOGPATH
    LOGPATH = createLogFolder(lib_name)
    RobotRemoteServer(inst, host, port, allow_stop)
    