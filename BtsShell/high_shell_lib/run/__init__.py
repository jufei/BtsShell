import sys
from threading import Thread
from types import MethodType, SliceType
from robot.libraries import BuiltIn
from BtsShell import BtsShell

#from keyword_template import *

#for unittest initial library
global IMPORTED_LIBRARY
IMPORTED_LIBRARY = None

def _check_and_split_tpi(ident, expected, lastempty = False, allowrange = False):
    list = str(ident).split(",")
    if len(list) != expected:
        raise RuntimeError, "Invalid Parameter '%s'" % (ident)
    for i in range(len(list)):
        if (i == len(list) - 1 and list[i] == "" and not lastempty) or (
            i != len(list) - 1 and list[i] == "") or (
            i != len(list) - 1 and list[i] != "" and not list[i].isdigit()) or (
            i == len(list) - 1 and list[i] != "" and not allowrange and not list[i].isdigit()):
            raise RuntimeError, "Invalid Parameter '%s'" % (ident)
    while len(list) < 3:
        list.append(None)
    return (list[0], list[1], list[2])

class AbstractObjectComparator:
    """
    Implements __cmp__ method which compares all the object's attributes.

    In case the object has list variable _compare_attributes, the variables
    in that list are checked when objects are compared. Otherwise all the
    object's attributes that does not start with underscore '_' are compared
    excluding methods.

    If there are any exceptions during this comparison, -1 will be returned.
    """

    def __cmp__(self, other):
#        print 'objects ', self, other
        try:
            if hasattr(self, '_compare_attributes'):
                attributes = getattr(self, '_compare_attributes')
            else:
                attributes = [ attr for attr in dir(self)
                               if not attr.startswith('_') and
                               type(getattr(self, attr)) is not MethodType ]
            for attr in attributes:
#                print "attr", attr
                difference = cmp(getattr(self, attr), getattr(other, attr))
#                print "diff", difference
                if  difference != 0:
                    return difference
            return 0
        except KeyboardInterrupt:
            raise
        except:
            return -1

class IpaMmlItem(AbstractObjectComparator):
    """ base class for items contained in IpaMmlDict """

    def __str__(self):
        """ support a nice string representation with all attribute values"""
        tmp = ",".join(sorted([ "%s=%s" % (item, getattr(self, item)) for item in dir(self)
                                if not item.startswith("_") and getattr(self, item) != None and
                                    type(getattr(self, item)) is not MethodType ] ))
        for i in range(len(tmp)):
            if ord(tmp[i]) > 127:
                tmp = tmp.replace(tmp[i], " ")
        return tmp

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

class IpaMmlDict(dict):
    """ A specialization of generic python dict with the following extensions/differences:
    - if a key/index does not exits IpaMml dict will not raise KeyError but return None
    - may be used like a list an element is addressed via an integer as index
      (does not work if you use integers as keys)
    - support a list of keys in the order they have been inserted: ordered_keys
    - supporting sorting of this ordered_keys attribute and thus the "list" IpaMmlDict itself
    - nice string representation also if objects are contained
    - contained object should be derived from IpaMmlItem (not mandatory)
    """


    def __init__(self,*args):
        """ should also be called by subclasses,
        otherwise you might have problems with empty IpaMmlDicts when the attribute ordered_keys is not present
        """
        dict.__init__(self,*args)
        self.ordered_keys = []

    def __str__(self):
        """ support a nice string representation """
        try:
            tmp = "\n".join([ str(key) + ':' + str(self[key]) for key in self.ordered_keys ])
            for i in range(len(tmp)):
                if ord(tmp[i]) > 127:
                    tmp = tmp.replace(tmp[i], " ")
            return tmp
        except AttributeError:
            return ""

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    def __getitem__(self, key):
        """ access the item identified by key, either behave like a dictionary or like a list
        return None is no item is found
        """
        if len(self)==0:
            return None
        if type(key) is SliceType:
            return self._get_ipamml_dict_from_slice(key)
        try:
            return dict.__getitem__(self,key)
        except KeyError:
            pass
        if type(key) == type(1):
            try:
                return dict.__getitem__(self, self.ordered_keys[key])
            except IndexError:
                pass
        return None

    def _get_ipamml_dict_from_slice(self, slice):
        new_dict = IpaMmlDict()
        for key in self.ordered_keys.__getitem__(slice):
            #TODO: Is there need to take copy/deepcopy from the item (copy module)
            new_dict[key] = self[key]
        return new_dict

    def __setitem__(self, key, item):
        """ store the new item in the dictionary and append the key to ordered_list """
        if type(key) == type(1):
            raise RuntimeError("IpaMmlDict does not support integer as key")
        dict.__setitem__(self, key, item)
        try:
            if key in self.ordered_keys:
                self.ordered_keys.remove(key)
            self.ordered_keys.append(key)
        except AttributeError:
            self.ordered_keys = [key, ]

    def __delitem__(self, key):
        """ remove the new item from the dictionary and remove the key from ordered_list,
        works both with key and index """
        try:
            dict.__delitem__(self, key)
            self.ordered_keys.remove(key)
        except KeyError:
            if type(key) == type(1):
                dict.__delitem__(self, self.ordered_keys[key])
                del(self.ordered_keys[key])


    def __getattr__(self, name):
        """ support direct access to the item's attributes if only a single item is contained """
        if len(self) != 1:
            raise AttributeError
        return getattr(self.values()[0], name)

    def length(self):
        """ only because x.length() looks nicer than x.__len__()"""
        return len(self)

    def _get_empty_container(self):
        """ needed so that select_entries_from_list can return the correct type of container,
        can be overwritten by subclasses """
        return IpaMmlDict()

    def sort(self,*args):
        """ sorts attribute orderd_keys and thus also IpaMmlDict itself if used as a list
        can be overwritten by subclasses if a special sorting algortihm is needed. """
        try:
            self.ordered_keys.sort(*args)
        except AttributeError:
            pass


def _extend_doc_string(method, objectClass):
    """ can be used to extend the doc string of a (keyword) method with the doc string of the class the method returns
    Thus you can describe the class and its attributes together with the class and
    do not need to repeat this description in the method's doc string """
    method.__doc__ += """
    ---
    info for object class %s:

    """ % objectClass.__name__
    method.__doc__ += objectClass.__doc__
    return



_mml_traces = []
class Record_mml:
    def __init__(self):
#        print "Listener.__init__ "
        self.tc=None
        self.suite=None
        self.filename = None
        self.file = None

    def start_suite(self, name, documentation):
#        print 'Suite Telnet Listener' + name, " "
        mock.start_trace(_mml_traces)
        self.suite = name
        self.filename = self.suite+"_mml.py"
        self.file=open(self.filename, mode="wb")
        self.file.write("suite_mml_responses ={}\n\n\n")
        self.file.write("# ==== definitons for suit setup ====\n\n")

    def end_suite(self, status, message):
        self.file.write("# ==== definitons for suit teardown ====\n\n")
        if len(_mml_traces) > 0:
            #there has been a suite teardown that needs to be recorded
            self.file.write("tc_mml_responses = {}\n")
            self.file.write("l=[]\n\n")
            for trace in _mml_traces:
                self.file.write('command_response = """')
                self.file.write(trace)
                self.file.write('"""\n')
                self.file.write("l.append(command_response)\n\n")
            self.file.write('tc_mml_responses[""] = l\n')
            self.file.write("suite_mml_responses['suite_teardown']=tc_mml_responses\n\n\n")
            _mml_traces[:] = []

        self.file.write("def get_mml_responses():\n")
        self.file.write("    return suite_mml_responses\n")
        self.file.close()

    def start_test(self, name, documentation, tags):
        global _mml_traces
        if len(_mml_traces) > 0:
            #there has been a suite setup that needs to be recorded
            self.file.write("tc_mml_responses = {}\n")
            self.file.write("l=[]\n\n")
            for trace in _mml_traces:
                self.file.write('command_response = """')
                self.file.write(trace)
                self.file.write('"""\n')
                self.file.write("l.append(command_response)\n\n")
            self.file.write('tc_mml_responses[""] = l\n')
            self.file.write("suite_mml_responses['suite_setup']=tc_mml_responses\n\n\n")
            _mml_traces[:] = []
#        print 'Testcase Listener' + name, " "
        self.tc = name.replace(" ","").lower()
        self.file.write("# ==== definitons for test case '%s' ====\n\n" % self.tc)

    def end_test(self,status, message):
        global _mml_traces
        if len(_mml_traces) > 0:
            self.file.write("tc_mml_responses = {}\n")
            self.file.write("l=[]\n\n")
            for trace in _mml_traces:
                self.file.write('command_response = """')
                self.file.write(trace)
                self.file.write('"""\n')
                self.file.write("l.append(command_response)\n\n")
            self.file.write('tc_mml_responses[""] = l\n')
            self.file.write("suite_mml_responses['%s']=tc_mml_responses\n\n\n" % self.tc)
            _mml_traces[:] = []

class Replay_mml:
    def __init__(self):
        self.mml_responses = {}
        self.tc=None
        self.suite=None
        self.module = None

    def start_suite(self, name, documentation):
#        print 'Suite Telnet Listener' + name, " "
        self.suite = name
        self.module = __import__(self.suite+"_mml", globals())
        self.suite_mml_responses = self.module.get_mml_responses()
        mock.start_mock()
        if self.suite_mml_responses.has_key("suite_setup"):
            key = "suite_setup"
        else:
            key = ""
        try:
            mock.set_mml_responses(self.suite_mml_responses[key])
        except KeyError:
            pass

    def end_suite(self, status, message):
        pass

    def start_test(self, name, documentation, tags):
#        print 'Testcase Listener' + name, " "
        self.tc = name.replace(" ","").lower()
        if self.suite_mml_responses.has_key(self.tc):
            key = self.tc
        else:
            key = ""
        try:
            mock.set_mml_responses(self.suite_mml_responses[key])
        except KeyError:
            pass

    def end_test(self,status, message):
        if self.suite_mml_responses.has_key("suite_teardown"):
            key = "suite_teardown"
        else:
            key = ""
        try:
            mock.set_mml_responses(self.suite_mml_responses[key])
        except KeyError:
            pass

def start_command_on_cloned_connection(callableObj, *args, **kwargs):
    """Start a background command on a cloned connection.
    The command continues in the background until stop_command_on_connection is executed.
    """
    current = connections.get_current_telnet()._current
    print "old id '%s'" % current
    new_connection = connections.get_current_telnet().clone_connection()
    print "new id '%s'" % new_connection
    try:
        callableObj(*args, **kwargs)
        return new_connection
    finally:
        connections.get_current_telnet().switch_ipa_connection(current)

def stop_command_on_connection(connection_id, stop_char=chr(3), callableObj=None, *args, **kwargs):
    """ Stop a background command that was started with start_command_on_cloned_connection
    """
    if stop_char is None or stop_char == "" :
        stop_char = chr(3)
    current = connections.get_current_telnet()._current
    connections.get_current_telnet().switch_ipa_connection(connection_id)
    try:
        connections.get_current_telnet().write_bare(stop_char)
        response = connections.get_current_telnet().read_until_prompt()
        return response
    finally:
        if callableObj != None:
            callableObj(*args, **kwargs)
        connections.get_current_telnet().disconnect_from_ipa()
        connections.get_current_telnet().switch_ipa_connection(current)

def parallel_execute_command(callableObj, args_list):
    """use some parallel thread to do some """
    current = connections.get_current_telnet()._current
    thread_list = []
    for i in range(len(args_list)):
        t = Thread(target=callableObj,args=args_list[i])
        t.start()
        thread_list.append(t)
#        time.sleep(0.1)

    not_all_end = True
    while not_all_end:
        not_all_end = False
        for t in thread_list:
            not_all_end = not_all_end or t.isAlive()

    connections.get_current_telnet().switch_ipa_connection(current)

def ishex(string):
    for c in string:
        if not ('0' <= c <= '9' or 'a' <= c <= 'f' or 'A' <= c <= 'F'):
            return False
    return True

def _import_library(cls, *arg):
    global IMPORTED_LIBRARY
    if cls is not None:
        IMPORTED_LIBRARY = cls(*arg)
    else:
        IMPORTED_LIBRARY = None
    return IMPORTED_LIBRARY

class IPALibrary(object):
    def __init__(self):
        self.ipamml_lib = hasattr(IpaMml, 'inst') and IpaMml.inst or IpaMml()
        #import FunctionLib as lib
        #self.func_lib = hasattr(lib.FunctionLib, 'inst') and lib.FunctionLib.inst or lib.FunctionLib()

    def __getattr__(self, name):
        if self.ipamml_lib._keywords.has_key(name):
            return getattr(self.ipamml_lib, name)
        else:
            raise RuntimeError, "keyword:%s is not in IpaMml library!" % name

def _run_keyword(kw_function, *args, **kwargs):
    """ Can be used instead of robot buildin keyword run_keyword with the follwoing differences:
    run_keyword takes a keyword name as argument
    _try_run_keyword takes a keyword method/function as argument
    run_keyword only works in Robot environment and not in a simple unit test environement.
    _try_run_keyword also works in unit test environment when no Robot framework is available.
    """
    raise_err = False
    out_robot = False
    if(kwargs.has_key('raise_err')):
        raise_err = kwargs['raise_err'] == 'Yes' and True or False
        del(kwargs['raise_err'])
    if(kwargs.has_key('out_robot')):
        out_robot = kwargs['out_robot'] == 'Y' and True or False
        del(kwargs['out_robot'])
    global IMPORTED_LIBRARY
    if IMPORTED_LIBRARY is None:
        IMPORTED_LIBRARY = BtsShell()

    try:
        if isinstance(kw_function, basestring):
            kw_function = getattr(IMPORTED_LIBRARY, kw_function.replace(" ", "_").lower())
            result = kw_function(*args, **kwargs);
        else:
            builtin = BuiltIn.BuiltIn()
            kw_name = isinstance(kw_function, basestring) and kw_function or kw_function.__name__
            result = builtin.run_keyword(kw_name,  *args, **kwargs);
    except:
        type, value, my_traceback = sys.exc_info()
        if str(value).endswith("'get_handler'"):
            if isinstance(kw_function, basestring) :
                #if "__ipamml_singleton__" not in globals():
                #    global __ipamml_singleton__
                #    __ipamml_singleton__ = IpaMml()
                kw_function = getattr(IMPORTED_LIBRARY, kw_function.replace(" ", "_").lower())
            try:
                result = kw_function(*args, **kwargs);
            except KeyboardInterrupt:
                raise
            except:
#                traceback.print_exc(10)
                if(raise_err):
                    raise
                else:
                    raise errors.IpaMmlException("")
        else:
            raise

    return result


def _purge_mml_command(command, pattern=[(r",\s*:", ":"), (r",\s*;", ";"), (r":\s*;", ";")]):
    """
    ",\s*:" --> ":"
    ",\s*;" --> ";"
    ":\s*;" --> ";"
    """
    for pat, rep in pattern:
        while (1):
            lst = re.split(pat, command)
            command = rep.join(lst)
            if len(lst) == 1:
                break
    return command

import re

def _parse_by_start_positions(output, head, attributes=None, key_attribute=None, decorator_func=None, skippable_patterns=[r"^--", ], critical_patterns=[r"^COMMAND", ]):
    """
    attributes - list of attribute names, by default is lower of each item in head (whitespace replaced with underscore)
    key_attribute - could be one attribute name or a function (items, item) for calculation, by default is the first item of attributes
    decorator_func - could be a function (items, item) for item decoration, will be called when each item is ready
    skippable_patterns - patterns to be skipped
    critical_patterns - patterns to trigger exit from function

    go through output line by line
        critical?       -y-> exit from loop
        empty?          -y-> next line
        skipped?        -y-> next line
        positions ready -y-> make item -> decorate item -> put it into items with key comes from key_attribute
        calculate positions

    return (items, rest lines)
    """

    if not isinstance(head, list) or not head:
        raise "missing head information"

    if attributes == None:
        attributes = []
        for field in head:
            attributes.append("_".join(field.lower().split()))

    if not isinstance(attributes, list) or (len(attributes) != len(head) and head[0] != "-"):
        raise "unmatched head and attributes"

    if not key_attribute:
        key_attribute = attributes[0]

    items = IpaMmlDict()
    positions = []
    lines = output.splitlines()
    for line_ix in range(len(lines)):
        line = lines[line_ix]

        critical = False
        for pattern in critical_patterns:
            if re.match(pattern, line):
                critical = True
                break
        if critical:
            break

        if not line.strip():
            continue

        skippable = False
        for pattern in skippable_patterns:
            if re.match(pattern, line):
                skippable = True
                break
        if skippable:
            continue

        if positions:
            item = IpaMmlItem()
            for field_ix in range(len(head)):
                if field_ix != len(head) - 1:
                    setattr(item, attributes[field_ix], line[positions[field_ix]:positions[field_ix+1]].strip())
                else:
                    setattr(item, attributes[field_ix], line[positions[field_ix]:].strip())
            if callable(decorator_func):
                decorator_func(items, item)
            if callable(key_attribute):
                items[key_attribute(items, item)] = item
            else:
                items[getattr(item, key_attribute)] = item
            continue

        if line.strip().startswith(head[0]) and not positions and head[0] != '-':
            try:
                for field in head:
                    if not positions:
                        positions.append(line.index(field))
                    else:
                        positions.append(line.index(field, positions[-1] + 1))
            except Exception, err:
                errors._reraise_critical_exceptions(err)
                positions = []
            continue
        elif not positions and re.match("^[\s-]+$", line) and head[0] == '-':
            start = False
            for ix in range(len(line)):
                if line[ix] != '-':
                    start = False
                    continue
                if start is False:
                    start = True
                    positions.append(ix)

    if line_ix == len(lines):
        return (items, None)
    else:
        return (items, "\n".join(lines[line_ix:]))

def _compare_version(ver1, ver2):
    import re;
    maijor_version = ['CB', 'A9']
    if ver1[:2] != ver2 [:2]:
        for i in maijor_version:
            if i == ver1[:2]: return -1
            if i == ver2[:2]: return 1

    ver1_group = re.search("(\d+)[._](\d+)[-_](\d+)", ver1) #.groups()
    ver2_group = re.search("(\d+)[._](\d+)[-_](\d+)", ver2) #.groups()
    if ver1_group and ver2_group:
        for i in range(3):
            result = cmp(int(ver1_group.group(i+1)),
                         int(ver2_group.group(i+1)))
            if result != 0: return result

        return 0
    else:
        raise RuntimeError, "Invalid version '%s'" % (ver1_group and ver2 or ver1)
