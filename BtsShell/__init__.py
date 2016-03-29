"""
This library supports keywords to
   - log in to a remote Linux or Microsoft Windows host via telnet
   - execute any command supported by the underlying operting system

| Main Responsible   | E-Mail Address |
| TDLTE IV TA        | COO RA RD LTE TDD TA List |

When reporting bugs or requesting new features, please use the Issue Track System:
https://jira.inside.nokiasiemensnetworks.com/browse/TDLTETA
"""
import os.path
from types import MethodType, FunctionType
import sys
import __main__
from robot import version
ROBOT_VERSION = version.get_version()

from BtsComm import get_co_name, get_co_filename

#import connections

try:
    mod = __import__("version", globals())
    __version__ = mod.version
except:
    __version__ = "0.5.0"

class BtsShell:

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self._keywords = self._scan_keywords()
        if ROBOT_VERSION >= '2.1':
            pass
            #from BtsComm.robot_html_logger_21 import RobotLogHooker
        else:
            from BtsComm.robot_html_logger import RobotLogHooker
        #self.hook = RobotLogHooker()
        BtsShell.inst = self

    def get_BtsShell_Version(self):
        """Returns the version of the underlying BtsShell Library
        """
        return __version__

    def get_keyword_names(self):
        return self._keywords.keys() + self._get_my_keywords()

    def get_whole_keyword_names(self):
        return self.keyword_names + self._get_my_keywords()

    def __getattr__(self, name):
        try:
            return self._keywords[name]
        except KeyError:
            raise AttributeError

    def _get_my_keywords(self):
        return [ attr for attr in dir(self)
                 if not attr.startswith('_') and type(getattr(self, attr)) is MethodType ]

    def _scan_keywords(self):
        keywords = []
        basedir = os.path.dirname(os.path.abspath(__file__))
        for path in os.listdir(basedir):
            try:
                path = os.path.join(basedir, path)
                if os.path.isfile(path) and path.endswith('_lib.py'):
                    keywords += self._scan_keywords_from_file(path)
                elif os.path.isdir(path) and path.endswith('_lib'):
                    empty_dir=self._check_empty_dir(path)
                    if empty_dir:
                         continue
                    keywords += self._scan_keywords_from_dir(path)
                elif os.path.isdir(path) and path.endswith('connections'):
                    keywords += self._scan_keywords_from_dir(path)
            except Exception,e:
                self.output_error_in_robot_log(e)
                continue

        kwdict=dict([ (kw.__name__.lower(), kw) for kw in keywords ])
        return kwdict

    def _scan_keywords_from_file(self, path):
        mod_name = os.path.splitext(os.path.basename(path))[0]
        return self._scan_keywords_from_module(mod_name)

    def _scan_keywords_from_dir(self, path):
        mod_name = os.path.basename(path)
        return self._scan_keywords_from_module(mod_name)

    def _scan_keywords_from_module(self, name):
        mod = __import__(name, globals())
        kws = [ getattr(mod, attr) for attr in dir(mod)
                if not attr.startswith('_') ]
        kws = [ kw for kw in kws if type(kw) in [MethodType, FunctionType] ]

        #return false, if the keyword isn't defined in the module. It's used to
        #avoid the keyword be exported that importing from other module.
        def check_in_module(kw, mod):
            kw_file = os.path.abspath(get_co_filename(kw))
            if os.path.basename(kw_file).startswith('decorators'):
                try:
                    kw_file = os.path.abspath(kw._co_filename)
                except:
                    pass
            mod_file = os.path.abspath(mod.__file__)
            (def_mod) = os.path.dirname(kw_file)
            (cur_mod) = os.path.dirname(mod_file)
            result = def_mod.lower() == cur_mod.lower()
            if result == False:
                '''print "'%s' defined in '%s' != %s" % (kw.__name__,
                                                      kw_file,
                                                      mod_file)
                '''
                bn = lambda x:os.path.basename(x).lower()
                if bn(def_mod) == bn(cur_mod) and mod_file.endswith(".pyc"):
                    print "!!!Please remove all .pyc in library path!!!"
                    sys.exit(1)
            return result

        return [ kw for kw in kws if check_in_module(kw, mod) ]

    def _check_empty_dir(self,path):
        empty=True
        files=os.listdir(path)
        for file in files:
            if str(file).endswith("py"):
                empty=False
        if empty:
            self._remove_pyc_in_directory(path)
        return empty

    def _remove_pyc_in_directory(self,directory):
        paths = os.listdir(directory)
        for path in paths:
            path = os.path.join(directory, path)
            if os.path.isdir(path):
                self._remove_pyc_in_directory(path)
            elif str(path).endswith(".pyc"):
                os.remove(path)
        paths = os.listdir(directory)
        if len(paths)==0:
            os.rmdir(directory)

    def output_error_in_robot_log(self, e):
        import robot, traceback
        if ROBOT_VERSION >= '2.1':
            syslog = robot.output.LOGGER
            from robot.output.loggerhelper import Message
            syslog.message(Message("%s:%s" % ('Import Keyword Error', e.message), 'ERROR'))
            syslog.message(Message(traceback.format_exc(), 'ERROR'))
        else:
            syslog = robot.output.SYSLOG
            syslog.error("*ERROR* %s:%s" % ('Import Keyword Error', e.message))
            syslog.error(traceback.format_exc())

if __name__ == "__main__":
    obj = BtsShell()
    for kw, co in obj._keywords.items():
        print "%-50s" % kw, co.func_code.co_filename
    print len(obj._keywords)
