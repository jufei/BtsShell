from __future__ import with_statement
import os, sys, re, time
from datetime import datetime

from robot import version
ROBOT_VERSION = version.get_version()

def gettime():
    if ROBOT_VERSION >= '2.7':
        return datetime.now().strftime("%Y%m%d %H:%M:%S.000")
    else:
        return datetime.now().strftime("%Y%m%d %H:%M:%S")
    
    
def _date_to_second(time_string):
    if len(time_string)==19:
        time_string = time_string.replace(' ','-').replace(':', '-') 
    elif len(time_string) == 14: 
        t_list = []
        for i in range(0, 14, 2):
            t_list.append(time_string[i:i+2])

        time_string = '-'.join(t_list)  
        time_string = time_string.replace('-','',1)       
    else:
        raise Exception, "Time format is not match, it should be \
'2011-02-28 17:44:30' or '2011-02-28-17-44-30' or '20130827122619'"    
        
    return time.mktime(time.strptime(time_string, "%Y-%m-%d-%H-%M-%S"))

def _second_to_date(second, format=1):
    format_time = ""
    if 1 ==  int(format): 
        format_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(second))
    elif 2 ==  int(format): 
        format_time = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(second))        
    elif 3 ==  int(format): 
        format_time = time.strftime("%Y%m%d%H%M%S",time.localtime(second))  
    else:    
        format_time = time.strftime("%Y%m%d%H%M%S",time.localtime(second))  
    return format_time

def get_start_end_time(string, timeout):
    start_time = None
    end_time = None
    tmp = re.search('(\d{8}\s\d{2}:\d{2}:\d{2})', string)
    if tmp:
        start_time = tmp.group(1)
        sec = _date_to_second(start_time.replace(':', '').replace(' ', ''))
        end_time = _second_to_date(sec + timeout*60).replace('-', '')
      
    return start_time, end_time

class BeautifulOutput:
    def __init__(self, strings, timeout):
        self.start_time = None
        self.end_time = None
        self.start_time, self.end_time = get_start_end_time(strings, timeout)
        
        if (self.start_time == None):
            self.start_time = gettime()
        else:
            if ROBOT_VERSION >= '2.7':
                self.start_time += '.000'
            
        if (self.end_time == None):
            self.end_time = gettime()        
        else:
            if ROBOT_VERSION >= '2.7':
                self.end_time += '.000'
        print self.start_time, self.end_time      
        self.lines = strings.splitlines()
        self.uncomplete = []
        self.starttag = None
        if self.lines[-1].strip() != "" and self.lines[-1].startswith("<"):
            self.lines.pop()
        if self.lines[-1].strip() == "":
            self.lines.pop()

    
        
    def fix_output(self):
        for ln in self.lines:
            if re.match("<\?xml version=.*\?>", ln):
                continue
            elif re.match("<(?P<tag>\w+).*>.*</(?P=tag)>", ln):
                continue
            elif re.match("^<(\w+?)>$", ln): #<tag>
                self.starttag = re.match("^<(\w+?)>$", ln).group(1)
                self.uncomplete.append(self.starttag)
            elif re.match("^<(\w+?) .*?>$", ln): #<tag att=asd>
                self.starttag = re.match("^<(\w+?) .*?>$", ln).group(1)
                self.uncomplete.append(self.starttag)
            elif re.match("^<(\w+?) .*$", ln): #<tag xxxx
                self.starttag = re.match("^<(\w+?) .*$", ln).group(1)
                self.uncomplete.append(self.starttag)
            elif re.match("^<(\w+?)>.*$", ln): #<tag xxxx
                self.starttag = re.match("^<(\w+?)>.*$", ln).group(1)
                self.uncomplete.append(self.starttag)
            elif re.match("^.*</(\w+?)>$", ln): #xxx </tag>
                if self.uncomplete[-1] == re.match(".*?</(\w+?)>$", ln).group(1):
                    self.uncomplete.pop()
                else:
                    print "*WARN* the tag \"%s\" in line %d is strange, last tag is: %s" \
                     % (re.match(".*?</(\w+?)>$", ln).group(1), self.lines.index(ln)+1, self.uncomplete[-1])
            elif re.match("^</(\w+)>$", ln):
                if self.uncomplete[-1] == re.match("^</(\w+)>$", ln).group(1):
                    self.uncomplete.pop()
                else:
                    print "*WARN* the tag \"%s\" in line %d is uncomplete, last tag is: %s" \
                     % (re.match("^</(\w+)>$", ln).group(1), self.lines.index(ln)+1, self.uncomplete[-1])
        
        for i in range(len(self.uncomplete)):
            tag = self.uncomplete.pop()
            ln = "</%s>" % tag
            if tag == 'kw' or tag == 'suite' or tag == 'test':
                status_line = '<status status="FAIL" endtime="%s" starttime="%s"></status>' \
                            % (self.end_time, self.start_time)
                self.lines.append(status_line)
            self.lines.append(ln)
        return '\n'.join(self.lines)        




def fix_xml(src_xml, des_xml, timeout):
    with open(src_xml, 'r') as src:
        f_content = src.read()       

        obj = BeautifulOutput(f_content, timeout)
        with open(des_xml, 'w') as des:
            des.write(obj.fix_output())

if __name__ == "__main__":
    fix_xml("D:\\work\\all problems\\10_SWDL_With_SEM.xml", 
            "D:\\work\\all problems\\10_SWDL_With_SEM2.xml", 20)
