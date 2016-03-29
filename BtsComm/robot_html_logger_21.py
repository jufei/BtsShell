#  $Id $

"""
This module is a tools to reduce the size of robot log files. it 
catch all log of the keyword output. it's generate a HTML log file
for every keyword, and save a link to the keywords log in test case log files.

it's not use dynamic library to catch output log, because that can't catch the log
of robot. (like: arguments, return)

"""

import os
import cStringIO
import threading
import robot
from robot.output.xmllogger import XmlLogger
from robot.output.loggerhelper import Message
from robot.utils.xmlwriter import XmlWriter
from robot.utils import FileNameGenerator
import robot.utils as utils
from xml.sax.saxutils import XMLGenerator

INITED_HOOKER = None

class BufferXMLGenerator(XMLGenerator):
    def startElement(self, name, attrs):
        if name != "robot":
            XMLGenerator.startElement(self, name, attrs)

    def endElement(self, name):
        if name != "robot":
            XMLGenerator.endElement(self, name)
        
def buffer_supported_xmlwrite_init(self, path):
    self.path = path
    if path.startswith("buf:"):
        self._output = cStringIO.StringIO()
        self._writer = BufferXMLGenerator(self._output, 'UTF-8')
    else:
        import os
        if os.path.exists(path):
            #echo("can't overwriting file:%s\n" % path)
            #raise Exception, "can't overwriting file:%s" % path
            pass
                  
        self._output = open(path, 'wb') 
        self._writer = XMLGenerator(self._output, 'UTF-8')
        self._writer.startDocument()
    self.closed = False    

class DynamicHtmlLogger(object):
    def __init__(self, cracker=None):
        self.keyword_logger = []
        self.cracker = cracker
        self.inited_log_viewer = False
        self.html_output_idgen = utils.IdGenerator()
        self.html_output_idgen._ids['kw'] = 900000
    
    def __getattr__(self, name):
        #echo("__getattr__:%s\n" % name)
        if name == 'cur_logger':
            return self.keyword_logger[-1]
        elif name == 'file_name':
            self.file_name = FileNameGenerator(self.cracker.log_file)
            return self.file_name
                
        raise AttributeError, "Not found attribute '%s'" % name
        
    def start_keyword(self, kw):
        #echo("kw:%s, keyword_logger:%s,,,%s\n" % (kw.name, len(self.keyword_logger), self))
        if self.cracker.max_logsize > 0:            
            if len(self.keyword_logger) == 0:
                self.keyword_logger.append(self.cracker.hold_up_output_xml())
                
            self.cur_logger.start_keyword(kw)
            if self.inited_log_viewer is False:
                self.cracker.insert_log_viewer(self.cur_logger)
                self.inited_log_viewer = True
            
            l = XmlLogger("buf:01")
            l._writer = l._get_writer(*l._writer_args)
            l._log_message_is_logged = self.keyword_logger[-1]._log_message_is_logged
            self.keyword_logger.append(l)
            
    def end_keyword(self, kw):
        #echo("end kw:%s\n" % kw.name)
        if self.cracker.max_logsize > 0:
            logger = self.keyword_logger.pop()
            self._merge_keyword_log(logger, kw)
            
            if len(self.keyword_logger) == 1:
                self.cracker.recover_output_xml()
                self.keyword_logger = []
            else:
                self.cur_logger.end_keyword(kw)
                
    def start_test(self, t):
        #echo("start_testcase...")
        self.inited_log_viewer = False
        
    def log_message(self, msg):
        if len(self.keyword_logger) > 0:
            self.cur_logger.log_message(msg)
        
    def _merge_keyword_log(self, log, kw):
        buffer = log._writer._output.getvalue()
        #echo("buffer:%s" % buffer)
        if len(buffer) < self.cracker.max_logsize or kw.status != 'PASS':
            #write buffered log to parent
            self.cur_logger._writer._writer._write(buffer)
        else:
            save_as = self.file_name.get_name()
            try:
                self.convert_xml_log_to_html(buffer, save_as)
            except:
                import sys
                type, value, traceback = sys.exc_info()
                echo(str(value))
            
            link_path = "%s" % (save_as)
            link_msg = '<a href="%s" target="blank">%s</a>'%(link_path, link_path)
            self.cur_logger.log_message(Message(link_msg, 'INFO', True))
    
    def convert_xml_log_to_html(self, xml_log, save_as=""):
        #echo("save_as:%s\n" % (save_as))
        #import robot.utils as utils
        keyword_wrapper = """
            <kw type="kw" name="dummy" timeout="">
            <doc>dummy.</doc>
            <arguments>
            </arguments>
            %s
            <status status="PASS" endtime="20081116 00:19:46.765" starttime="20081116 00:19:46.765"></status>
            </kw>
            """
        
        root_node = utils.DomWrapper(None, keyword_wrapper % xml_log)
        output = open(os.path.join(self.cracker.work_dir, save_as), 'wb')
        from robot.output.readers import Keyword
        serializer = KeywordSerializer(output, self.html_output_idgen)
        kw = Keyword(root_node)
        for child in kw.children:
            child.serialize(serializer)
        #output.write(xml_log)
        output.close()

class DummyXmlWriter:
    def __init__(self, original_writer):
        self.writer = original_writer
        
    def start(self, name, attributes={}, newline=True):
        pass
    def content(self, content):
        pass
    def end(self, name, newline=True):
        pass
    def element(self, name, content=None, attributes={}, newline=True):
        pass
    def close(self):
        pass
    
    def __getattr__(self, name):
        if name in ["path", "closed"]:
            return getattr(self.writer, name)
        else:
            raise AttributeError, "DummyXmlWriter instance has no attribute '%s'" % name

class RobotLogCracker():
    
    def __init__(self, xmllogger):
        self.attribute = ['work_dir', 'output_dir', 'max_logsize', 'log_file']
        XmlWriter.__init__ = buffer_supported_xmlwrite_init
        self.orginal_writer = None
        self.xmllogger = xmllogger
        
    def _value(self, name):
        var_evaluator = robot.variables.GLOBAL_VARIABLES.replace_string
        return var_evaluator(name)
    
    def hold_up_output_xml(self):
        #echo("hold_up_output_xml:%s\n" % self.xmllogger._writer)
        if self.xmllogger._writer is not None and \
            not isinstance(self.xmllogger._writer, DummyXmlWriter):
            #echo("hold_up_output_xml..\n")
            self.orginal_writer = self.xmllogger._writer
            self.xmllogger._writer = DummyXmlWriter(self.orginal_writer)
        elif self.xmllogger._writer is None:
            #echo("!!!The XML write is None.!!!")
            return self.xmllogger
        else:
            echo("!!!The XML logger have not recover.!!!")
        xml_logger = XmlLogger("buf:01")
        if self.orginal_writer: xml_logger._writer = self.orginal_writer
        xml_logger._log_message_is_logged = self.xmllogger._log_message_is_logged
        return xml_logger
        #return self.xmllogger._writer
    
    def recover_output_xml(self):
        #echo("recover_output_xml:%s\n" % self.orginal_writer)
        if self.orginal_writer is not None:
            self.xmllogger._writer = self.orginal_writer 
    
    def __getattr__(self, name):
        #init lazying attribute
        if name in self.attribute:
            self._max_logsize()
            if self.max_logsize > 0: 
                self._output_dir()
                self._log_file()
                
        if hasattr(self, name):
            return getattr(self, name)
        
        #echo("xxxxxxxxxxx'%s'xxxxxxxxx" % name)
        raise RuntimeError, "Not found attribute '%s' in RobotLogCracker." % name
    
    def _max_logsize(self):
        try:
            self.max_logsize = int(self._value("${logsize}"))
        except:
            self.max_logsize = 0
        #echo("logsize:%s" % self.max_logsize)
        #return self.max_logsize
    
    def _output_dir(self):
        try:
            out_file = self._value("${OUTPUT_FILE}")
            self.work_dir = os.path.dirname(out_file)

            out_file = os.path.basename(out_file)
            self.output_dir = os.path.splitext(out_file)[0]               
        except:
            self.output_dir = "output_"
        
        out_dir = os.path.join(self.work_dir, self.output_dir)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
            
        self._copy_viewer_to_directory(out_dir)
    
    def _log_file(self):
        self.log_file = self._value("${LOG_FILE}") 
        if self.log_file is None or not self.log_file.endswith(".html"):
            self.log_file = "log.html"
            
        self.log_file = "%s/%s" % (self.output_dir,
                                    os.path.basename(self.log_file))
        #echo("log file:%s\n" % self.log_file)
    
    def _copy_viewer_to_directory(self, dst):
        import shutil
        base_dir = os.path.dirname(__file__)
        for name in ('logviewer-0.1.jar', 'log_viewer.js'):
            dst_file = os.path.join(dst, name)
            if not os.path.exists(dst_file):
                shutil.copy(os.path.join(base_dir, name), dst_file)
                
    def insert_log_viewer(self, logger):
        link_msg = ''
        
        base_dir = self.output_dir
        link_msg = '<applet id="log_viewer" code="org.robot.log.LogViewerApplet.class" MAYSCRIPT ' + \
                    ' archive="%s/logviewer-0.1.jar" width="1px" height="1px" ></applet>' % base_dir
                    
        link_msg += '<script type="text/javascript" ' + \
                   'src="%s/log_viewer.js" ></script>' % base_dir
         
        logger.log_message(Message(link_msg, 'INFO', True))
                

def RobotLogHooker():
    global INITED_HOOKER
    if INITED_HOOKER == None and robot.output.OUTPUT:
        from robot.output.logger import LOGGER
        for e in LOGGER._loggers:
            if hasattr(e, 'logger') and \
                isinstance(e.logger, DynamicHtmlLogger): return
            
        cracker = RobotLogCracker(robot.output.OUTPUT._xmllogger)
        LOGGER.register_logger(DynamicHtmlLogger(cracker))
        LOGGER._loggers.insert(0, LOGGER._loggers.pop())
        INITED_HOOKER = True
        
    return INITED_HOOKER

from robot.serializing.logserializers import LogSerializer
class KeywordSerializer(LogSerializer):
    def __init__(self, output, idgen):
        self._writer = utils.HtmlWriter(output)
        #self._writer.whole_element('h2', 'Test Execution Log')
        self._idgen = idgen
        self._suite_level = 0

def echo(msg):
    import sys
    sys.__stdout__.write(msg)
