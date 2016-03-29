import os
import re
from lxml import etree
from common_operation import *
class ParseXML:
    """
    element attributes:
         ['__class__', '__contains__', '__copy__', '__deepcopy__', '__delattr__',
         '__delitem__', '__doc__', '__getattribute__', '__getitem__', '__hash__',
         '__init__', '__iter__', '__len__', '__new__', '__nonzero__', '__reduce__',
         '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__',
         '__str__', '_init', 'addnext', 'addprevious', 'append', 'attrib', 'base',
         'clear', 'extend', 'find', 'findall', 'findtext', 'get', 'getchildren',
         'getiterator', 'getnext', 'getparent', 'getprevious', 'getroottree',
         'index', 'insert', 'items', 'iter', 'iterancestors', 'iterchildren',
         'iterdescendants', 'iterfind', 'itersiblings', 'itertext', 'keys',
         'makeelement', 'nsmap', 'prefix', 'remove', 'replace', 'set',
         'sourceline', 'tag', 'tail', 'text', 'values', 'xpath']
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.tree = None
        self.root = None
        self.attributes = None
        try:
            xmlfile = open(self.filepath, "rb")
            self.tree = etree.parse(xmlfile)
            xmlfile.close()
            self.root = self.tree.getroot()

            self.attributes = self.root.attrib
        except:
            raise Exception, "Open '%s' file failed!" % filepath

    def write_xml_file(self, filepath):
        folder, name = os.path.split(filepath)
        if os.path.exists(folder):
            self.tree.write(filepath)
        else:
            raise Exception, "Folder '%s' don't exisit!"%folder

    def element_to_string(self, element):
        return etree.tostring(element)

    def string_to_element(self, string):
        return etree.fromstring(string)

    def get_ele_parent(self, element, level=1):
        for i in xrange(level):
            element = element.getparent()
            if element == self.root:
                return self.root
        return element

    def get_ele_previous(self, element):
        return element.getprevious()

    def get_ele_next(self, element):
        return element.getnext()

    def get_ele_tag(self, element):
        return element.tag

    def get_ele_attr(self, ele, attr):
        attributes = ele.attrib
        return attributes.get(attr)

    def get_ele_text(self, element):
        return element.text

    def modify_ele_text(self, element, new_text):
        element.text = new_text

    def get_element(self, tag, ele="ALL", all_match=False):
        element_list = []
        if "ALL" == ele:
            scope = self.root.iter()
        else:
            scope = ele.iter()
        for i in scope:
            if tag in i.tag:
                element_list.append(i)
        if not element_list:
            raise Exception, "Can't find tag name as '%s' in '%s'" \
                            % (tag, self.filepath)
        else:
            if all_match:
                return element_list
            else:
                return element_list[0]

    def get_ele_full_path(self, element):
        tmp = str(element.tag)
        index = tmp.find("}")
        if index>0:
            ele_name = tmp[index+1:]
        else:
            ele_name = tmp
        if self.root != element:
            parent_path = self.get_ele_full_path(self.get_ele_parent(element))
            tmp = parent_path + ".." + ele_name
            return tmp
        return ele_name

    def get_ele_iter_children(self, ele='ALL'):
        result_list = []
        if "ALL" == ele:
            scope = self.root.iter()
        else:
            scope = ele.iter()
        for s in scope:
            if s != ele:
                result_list.append(s)
        return result_list


    def find_all_element_by_specifical_text(self, text, ele="ALL"):
        if "ALL" == ele:
            scope = self.root.iter()
        else:
            scope = ele.iter()
        specifical_ele = []
        for i in scope:
            if  text == i.text:
                specifical_ele.append(i)
        return specifical_ele

    def find_all_element_by_tag(self, tag):
        specifical_ele = []
        for i in self.root.iter():
            if (0<=i.tag.find(tag)) and (tag in i.tag):
                specifical_ele.append(i)
        return specifical_ele

    def find_ele_by_attribute(self, tag, attr_name, attr_text):
        specifical_ele = []
        for i in self.root.iter():
            if (0<=i.tag.find(tag)) and (attr_text == i.get(attr_name)):
                specifical_ele.append(i)
        return specifical_ele

    def find_ele_by_part_attr(self, tag, attr_name, attr_text):
        """design for change tma version
        type as follow:
        1. <Permission Dir="C:\Program Files\Aeroflex\TM500\LTE - K4.3.2.REV02\ppc_pq\public\ftp_root">
        </Permission>
        2. scfc tag as "{xxxx}p"
        | find_ele_by_part_attr | "Permission" | "Dir" | "C:\Program Files\Aeroflex\TM500" |
        return all attribute as "C:\Program Files\Aeroflex\TM500"
        """
        specifical_ele = []
        for i in self.root.iter():
            if 0 <= i.tag.find(tag)  \
                    and i.get(attr_name)!= None  \
                    and 0 <= i.get(attr_name).find(attr_text):
                specifical_ele.append(i)
        return specifical_ele


    def get_ele_text_by_attr(self, element, attr_name, attr_value):
        """design for type as follow:
        <Permission Dir="C:\Program Files\Aeroflex\TM500\LTE - K4.3.2.REV02\ppc_pq\public\ftp_root">
        <Option Name="IsHome">1</Option>
        </Permission>
        """
        for ele in element.iter():
            if attr_value == ele.get(attr_name):
                return ele, ele.text

    def set_ele_attr(self, ele, attr_name, attr_new_value):
        """<managedObject   class="a"
                            distName="b"
                            version="c">
        sapmle as:
            set_ele_attr(mo, "class", "a")
            set_ele_attr(mo, "distName", "b")
            set_ele_attr(mo, "version", "c")
        """
        ele.set(attr_name, attr_new_value)

    def insert_ele(self, tar_ele, new_ele, location=0):
        """insert one element in parent element type as:
        <managedObject>  #tar_ele
            <p name="a3Offset">5</p>  #new_ele
        </managedObject>
        """
        tar_ele.insert(location, new_ele)

    def del_ele(self, element):
        try:
            parent = self.get_ele_parent(element)
            parent.remove(element)
            print "remove element '%s' from '%s' is ok."%(element.tag, parent.tag)
        except:
            print "the parent of element '%s'  is not exist, maybe delete already."%(element)
            pass

class ParseXmlDict(ParseXML) :
    def __init__(self, filepath):
        ParseXML.__init__(self, filepath)
        self.all_element_dictionary_list = []
        self.key_words = ['next',
                          'parent',
                          'grandfather',
                          'g_grandfather',
                          'children',
                          'previous',
                          'iterchild',
                          'siblings']

    def create_xml_dictionary(self):
        for ele in self.root.iter():
            data = {}
            path = self.get_ele_full_path(ele)
            data['obj'] = ele
            data['path'] = path
            tag = str(ele.tag)
            index = tag.find("}")
            if index > 0:
                tag = tag[index+1:]
            data['tag'] = tag
            data['text'] = ele.text
            data['children'] = ele.getchildren()
            data['parent'] = ele.getparent()
            if data['parent'] is not None:
                data['grandfather'] = data['parent'].getparent()
            else:
                data['grandfather'] = data['parent']
            if data['grandfather'] is not None:
                data['g_grandfather'] = data['grandfather'].getparent()
            else:
                data['g_grandfather'] = data['grandfather']
            data['attribute'] = ele.items()
            data['previous'] = ele.getprevious()
            data['next'] = ele.getnext()
            data['iterchild'] = self.get_ele_iter_children(ele)

            self.all_element_dictionary_list.append(data)

        #add siblings attribute for dictionary
        for obj in self.all_element_dictionary_list:
            if 1 < len(obj['children']):
                siblings_list = obj['children']
                self.add_siblings_in_ele_dicitionary(siblings_list)

        for obj in self.all_element_dictionary_list:
            if (None == obj['previous']) and (None == obj['next']):
                obj['siblings'] = []
        #print self.all_element_dictionary_list

    def add_siblings_in_ele_dicitionary(self, siblings_list):
        for siblings in siblings_list:
            #print siblings_list
            for obj in self.all_element_dictionary_list:
                if siblings == obj['obj']:
                    del_self_list = [ a for a in siblings_list]
                    del_self_list.remove(siblings)
                    obj['siblings'] = del_self_list


    def find_ele_dict_by_path(self, condition, scope="all"):
        ele_list = []
        for ele_dict in self.all_element_dictionary_list:
            if ele_dict['path'] == condition:
                ele_list.append(ele_dict)

        return ele_list

    def find_ele_dict_by_attr_or_text(self, attr_or_text, scope="all", flag=True):

        ele_list = []
        key, value = attr_or_text.split('=', 1)
        key = key.strip()
        value = value.strip("\"")

        if scope == "all":
            content = self.all_element_dictionary_list
        else:
            content = scope

        for ele_dict in content:
            if key == 'text':
                if value.count('.*')>0:
                    if ele_dict['text'] and \
                            re.search(value, ele_dict['text']):
                        ele_list.append(ele_dict)
                else:
                    if ele_dict['text'] == value:
                        ele_list.append(ele_dict)

            elif key == 'tag':
                if value.count('.*')>0:
                    if ele_dict['tag'] and re.search(value, ele_dict['tag']):
                        ele_list.append(ele_dict)
                else:
                    if ele_dict['tag'] == value:
                        ele_list.append(ele_dict)

            else:
                for attr_pair in ele_dict['attribute']:
                    if attr_pair[0] == key:
                        if True == flag:
                            if value.count('.*') > 0:
                                if re.search(value, attr_pair[1]):
                                    ele_list.append(ele_dict)
                            else:
                                if attr_pair[1] == value:
                                    ele_list.append(ele_dict)
                        elif False == flag:
                            if value.count('.*') > 0:
                                if not re.search(value, attr_pair[1]):
                                    ele_list.append(ele_dict)
                            else:
                                if attr_pair[1] != value:
                                    ele_list.append(ele_dict)
        return ele_list

    def find_ele_dict_by_attr_and_text(self, attr_and_text, scope="all", flag=True):

        ele_list = []

        con1, con2 = attr_and_text.split('&&')
        con1 = con1.strip()
        con2 = con2.strip()
        con1_ele_list = self.find_ele_dict_by_attr_or_text(con1, scope, flag)
        if len(con1_ele_list)==0:
            raise Exception, "No element find by the condition of '%s'"%con1_ele_list
        else:
            con2_ele_list = self.find_ele_dict_by_attr_or_text(con2, con1_ele_list, flag)
        return con2_ele_list

    def find_ele_dict_by_path_and_attr_or_text(self, path, attr_or_text, scope="all"):
        ele_list = []
        ele_dict = self.find_ele_dict_by_attr_or_text(attr_or_text, scope,flag)
        for ele in ele_dict:
            if '.*' == path:
                ele_list.append(ele)
            else:
                if ele['path'] == path:
                    ele_list.append(ele)

        return ele_list


    def find_dict_by_obj(self, obj_list):
        target_ele_dict_list = []

        if not isinstance(obj_list, list):
            obj_list = [obj_list]
        for ele_dict in self.all_element_dictionary_list:
            for obj in obj_list:
                if ele_dict['obj'] == obj:
                    target_ele_dict_list.append(ele_dict)
        return target_ele_dict_list



    def parse_condition(self, condition, scope="all", flag=True):

        all_ele = []
        simple_flag = True
        for key in self.key_words:
            if key in condition:
                simple_flag = False

        if (simple_flag and condition.count(" not ")==0):
            if condition.count('>>')==0 and \
                    condition.count('&&')==0 and \
                    condition.count('=')==0 :
                # print ">>start find element by tag path" #commit by jufei
                all_ele = self.find_ele_dict_by_path(condition, scope)

            elif condition.count('>>')==0 and\
                    condition.count('&&')==0 and \
                    condition.count('=')>=1:
                # print ">>start find element by attribute or text" #commit by jufei
                all_ele = self.find_ele_dict_by_attr_or_text(condition, scope, flag)

            elif condition.count('>>')==1:
                # print ">>start find element by path and attribute or text" #commit by jufei
                path, attr_or_text = condition.split('>>')
                path = path.strip()
                attr_or_text = attr_or_text.strip()
                all_ele = self.find_ele_dict_by_path_and_attr_or_text(path, attr_or_text, scope)
            elif condition.count('&&')==1:
                # print ">>start find element by attribute and text"  #commit by jufei
                all_ele = self.find_ele_dict_by_attr_and_text(condition, scope, flag)
            else:
                raise Exception,  "please check condition, by path or attribute"

        elif condition.count(' not ') == 1:
            print ">>start find by path then attribute not fill the condition"
            con1, con2 = condition.split('not')
            con1 = con1.strip()
            con2 = con2.strip()
            first_conditon = self.parse_condition(con1)
            if first_conditon ==[]:
                raise Exception, 'Not find first condition element'

            all_ele += self.parse_condition(con2, first_conditon, False)

        elif (not simple_flag and condition.count(" not ")==0):
            #print "parse condition type as %s"%self.key_words
            tmp_con = condition.split()
            tmp_con.reverse()
            for tmp in tmp_con:
                if tmp not in self.key_words:
                    continue
                else:
                    key = tmp.strip()
                    # print ">>start to split %s keyword"%key #By jufei
                    con1, con2 = condition.split(key)

                    con1 = con1.strip()
                    con2 = con2.strip()
                    con1_ele = self.parse_condition(con1)

                    if con1_ele ==[]:
                        raise Exception, 'Not find %s element'%con1
                    else:
                        pass

                    result_dict = []
                    for ele in con1_ele:
                        result_list = ele[key]
                        result_dict += self.find_dict_by_obj(result_list)

                    if "" == con2:
                        all_ele = result_dict
                    else:
                        all_ele += self.parse_condition(con2, result_dict)
                    break
        else:
            raise Exception, 'check parse condition'

        return all_ele

    def xml_common_operation(self, modify, stop_flag):
        read_value_list = []
        self.create_xml_dictionary()
        for mod in modify:
            ele_list = []
            cmd, target, condition = mod.split('|')
            cmd = cmd.strip().lower()
            target = target.strip()
            condition = condition.strip()
            target_dict = self.parse_condition(condition)

            for t in target_dict:
                ele_list.append(t['obj'])

            if ele_list==None or ele_list==[]:
                if stop_flag:
                    print "No element find by condition -> %s\n"%condition
                    continue
                else:
                    raise Exception, "please check condition -> %s"%condition
            # print "<<find %s matched element."%(len(ele_list)) #commet by jufei
            for element in ele_list:
                if 'read' == cmd:
                    if '' == target:
                        content = self.element_to_string(element)
                        read_value_list.append(content)
                        print "read element with condition '%s' ok.\n"%condition

                    elif target=='text':
                        target_value = self.get_ele_text(element)
                        read_value_list.append(target_value)
                        print "read text is '%s' with condition '%s' ok.\n"\
                                    %(target_value, condition)
                    elif target!='text':
                        target_value = self.get_ele_attr(element, target)
                        read_value_list.append(target_value)
                        print "read attribute value is '%s' with condidtion '%s' ok.\n"\
                                    %(target_value, condition)

                elif 'modify' == cmd:
                    key, value = target.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key=='text':
                        self.modify_ele_text(element, value)
                        # print "modify text as '%s' with condition '%s' ok.\n"\
                        #             %(value, condition)
                    elif key!='text':
                        self.set_ele_attr(element, key, value)
                        # print "modify attribute '%s'' value as '%s' with condition '%s' ok.\n"\
                        #             %(key, value, condition)
                    else:
                        print 'modify wrong'

                elif 'add' == cmd:
                    add_ele = self.string_to_element(target)
                    self.insert_ele(element, add_ele,-1)
                    print "add element '%s' in condition element '%s' ok.\n"\
                                %(target, condition)
                elif 'delete' == cmd:
                    self.del_ele(element)
                    print "delete element with condition '%s' ok.\n"%condition
                else:
                    print 'please check the command, not add/delete/modify/read but as %s'%cmd
        return read_value_list



def check_pm_file(file_path, tag_name):
    """This keyword parse PMxxxx.xml, get localMoid's text by tag 'M8000x'.
    - <MO>
      <baseId>NE-MRBTS-51</baseId>
      <localMoid>DN:NE-LNBTS-51/LNCEL-23809/MCC-04/MNC-08</localMoid>
      </MO>
    - <NE-WBTS_1.0 measurementType="LTE_Cell_Load">
      <M8001C6>0</M8001C6>
      <M8001C7>0</M8001C7>
    | Input Parameters  | Man.  | Description |
    | file path         | Yes   | PM file full path  |
    | tag_name          | Yes   | tag such as 'M8001' or 'M8002' |
    | Return value      | split list by '/' of localMoid's text |

    Example
    | parse pm file | 'D:\\PM.xml' | 'M8001' |
    """
    xml = ParseXML(file_path)
    ele = xml.get_element(tag_name)
    parent = xml.get_ele_parent(ele)
    previous = xml.get_ele_previous(parent)
    local_moid =  xml.get_element("localMoid", previous)
    local_moid_text = xml.get_ele_text(local_moid)
    tmp = local_moid_text.split("/")
    return tmp

def get_vendor_version(file_path):
    """This keyword get vendor file version by parse Filedirectly.xml.
    | Input Parameters  | Man.  | Description |
    | file path         | Yes   | FileDirectly.xml file full path  |
    | Return value      | current BTS vendor version |

    Example
    | ${Vendor_file_version} | get_vendor_version | 'D:\\FileDirectly.xml' |
    """
    vendor_name = ""
    xml = ParseXML(file_path)
    element = xml.find_ele_by_attribute("fileElement", "name", "vendor")
    for ele in element:
        vendor_name = ele.get("name")+ ele.get("version")
        return vendor_name
    raise Exception, "Can't find vendor version"

def change_bpf_file(src_file, target_file, modify):
    """ this keyword modify bpf file support 2 types as follow:
    type1: modify = "Temp.Ind.Sensor.Type:FTM|MAX.HW_SW_ID:21"
        <Property>
	   	   <Name>MAX.HW_SW_ID</Name>                #find condition3
	   		<Value>255</Value>                      #modify target
	   </Property>
	</Protected.Properties>
	<CLIC.CONFIGS>
		<CLIC.CONFIG name="FlexiBTS">
			<Property>
				<Name>Temp.Ind.Sensor.Type</Name>   #find condition2
				<Value>FTM</Value>                  #find condition1
			</Property>

    type2:  modify = "T.Fsp.Down.Activation:34"
    <Property>
        <Name>T.Fsp.Down.Activation</Name>          #find condition
        <Value>90</Value>                           #modify target
    </Property>
    | Input Parameters  | Man. | Description |
    | src_file          | Yes  | Path of FlexiBTSProperties file            |
    | tar_file          | Yes  | file name and path of file after modified  |
    | modify            | No   | modify parameter type as sting             |

    Example
    | change_bpf_file | D:\\FlexiBTSProperties.xml | D:\\new_bpf.xml | 'T.Fsp.Down.Activation:6' |
    | change_bpf_file | D:\\FlexiBTSProperties.xml | D:\\new_bpf.xml | 'Temp.Ind.Sensor.Type:FTM|MAX.HW_SW_ID:21' |
    """
    xml = ParseXML(src_file)
    if (1 == modify.count("|")) and (2 == modify.count(":")):
        mod = modify.split('|')
        (find_name, find_value) = mod[0].split(':')
        (tar_name, tar_value) = mod[1].split(':')
        eles = xml.find_all_element_by_specifical_text(find_value)
        for ele in eles:
            if find_name == xml.get_ele_text(xml.get_ele_previous(ele)):
                print "xml find Name as '%s' and Value as '%s'"%(find_name, find_value)
                parent = xml.get_ele_parent(ele, 3)
                for pre in xml.get_ele_previous(parent):
                    tar = xml.find_all_element_by_specifical_text(tar_name, pre)
                    for ta in tar:
                        mod = xml.get_ele_next(ta)
                        xml.modify_ele_text(mod, tar_value)
                        print "xml find Name as '%s' and modify Value as '%s' ok."%(tar_name, tar_value)
    elif 1 == modify.count(":"):
        (find_name, tar_value) = modify.split(':')
        eles = xml.find_all_element_by_specifical_text(find_name)
        print "xml find '%s' Name as '%s'"%(len(eles), find_name)
        for ele in eles:
            tar = xml.get_ele_next(ele)
            xml.modify_ele_text(tar, tar_value)
            print "xml modify Value as '%s' ok."%tar_value

    xml.write_xml_file(target_file)


def get_passive_sw_version(src_file):
    """ this keyword get passive Software Release Version by parse /ram/CurrentBD.xml file
    | Input Parameters  | Man. | Description |
    | src_file          | Yes  | full path of CurrentBD file            |
    | Return value      | psssive version |
    Example
    | ${passive_sw_version} | get_passive_sw_version | "D:\\work\\2012\\xml\\CurrentBD.xml" |

    """
    xml = ParseXML(src_file)
    ele = xml.get_element("currentBD")
    passive_version = xml.get_ele_attr(ele, "passiveSoftwareReleaseVersion")
    if None == passive_version:
        raise Exception, "Get passive sw version failed."
    return passive_version


def modify_plan_file(src_file, tar_file, modify_list):
    """ this keyword modify plan file's managedObject attribute and add new element
    | Input Parameters  | Man. | Description |
    | src_file          | Yes  | full path of plan templete file            |
    | tar_file          | Yes  | full path of modified plan file            |
    | modify_list       | Yes  | attribute value and new element content    |
    Example
    | ${modify_list} | Create List | class:a | listName:b | version:c | $add$a3Offset:d |
    | modify_plan_file | "D:\\work\\2012\\xml\\plan.xml" | "D:\\work\\2012\\xml\\plan_new.xml" | ${modify_list} |

    """
    xml = ParseXML(src_file)
    mo = xml.get_element("managedObject")
    for modify in modify_list:
        if modify.startswith("$add$"):
            attr_value, text = modify[5:].split(":")
            #create new element with attribute
            new = etree.Element('p', name=attr_value)
            #add text element
            new.text = text
            #add new element to mo
            xml.insert_ele(mo, new)
            print "add new element <p name=\"%s\">%s</p>' in managedObject ok."%(attr_value, text)
        else:
            attr_name, attr_value = modify.split(":")
            xml.set_ele_attr(mo, attr_name, attr_value)
            print "modify attribute '%s' as '%s' in managedObject ok."%(attr_name, attr_value)
    xml.write_xml_file(tar_file)


def delete_xml_element(src_file, tar_file, modify_list):
    """ this keyword delete xml file's managedObject or list
      if the delete element or parent element is not exist
        just ignore it withour raise Exception.
    | Input Parameters  | Man. | Description |
    | src_file          | Yes  | full path of plan templete file            |
    | tar_file          | Yes  | full path of modified plan file            |
    | modify_list       | Yes  | mo or list with arrtribute value content    |
    Example
    | ${modify_list} | Create List | mo:ANTL-1 | list:resourceList | delete||distName=.*MOPR-2/MORED-0 |
    | modify_plan_file | "D:\\SCFC.xml" | "D:\\SCFC_new.xml" | ${modify_list} |

    """
    modify_list_new = []

    if not isinstance(modify_list, list):
        modify_list = [str(modify_list)]

    for modify in modify_list:
        if modify.startswith("mo"):
            attr_name, attr_value = modify.split(":")
            modify_list_new.append('delete||distName=.*%s.*'%attr_value)
        elif modify.startswith("list"):
            tag_name, attr_value = modify.split(":")
            modify_list_new.append('delete||name=%s'%attr_value)
        elif modify.count('|') == 2:
            modify_list_new.append(modify)
        else:
            print "Error - Not support type '%s'\n"%modify

    common_xml_operation(src_file, tar_file, modify_list_new, True)
    #xml.write_xml_file(tar_file)
    #_add_miss_info(tar_file)
def read_configuration_file(file_dir, key):
    """This keyword reads BTS configuration file (xml format) such as SCF_1.xml and config.xml.

    | Input Parameters  | Man. | Description |
    | file_dir          | Yes  | Configuration file directory |
    | key               | Yes  | Key for search |

    | Return value | The value for search key |

    Example
    | Read Configuration File | C:\\SCF_1.xml | localIpAddr |
    | Read Configuration File | C:\\SCF_1.xml | LNCEL:phyCellId |
    | Read Configuration File | C:\\SCF_1.xml | distName=LNCEL-3307:a3Offset |
    | Read Configuration File | C:\\SCF_1.xml | alToggSuppList:alToggAmount|faultName=FT_61050_Missing or non-compliant SFP module |
    | Read Configuration File | C:\\SCF_1.xml | antlIdList:: |
    """

    xml = ParseXML(file_dir)
    if 0 == key.count(':') and 0 == key.count('|'):
        ele = xml.find_ele_by_attribute("p", "name", key.strip())
        return xml.get_ele_text(ele[0])

    elif 1 == key.count(':') and 0 == key.count('|') and 0 == key.count('='):
        (parent_attr_value, attr_value) = key.split(':')
        ele = xml.find_ele_by_attribute("managedObject", "class", parent_attr_value)
        (ele, text) = xml.get_ele_text_by_attr(ele[0],
                                               "name",
                                               attr_value.strip())
        return text

    elif 1 == key.count(':') and 0 == key.count('|') and 1 == key.count('='):
        (parent_attr, attr_value) = key.split(':')
        (parent_attr_name, parent_attr_value) = parent_attr.split('=')

        ele = xml.find_ele_by_part_attr("managedObject",
                                         parent_attr_name.strip(),
                                         parent_attr_value.strip())

        for index in range(len(ele)):
            try:
                (ele, text) = xml.get_ele_text_by_attr(ele[index],
                                               "name",
                                               attr_value.strip())
                break
            except:
                continue

        return text

    elif 1 == key.count(':') and 1 == key.count('|'):
        (front, condition) = key.split('|')
        (condition_attr_value, condition_text) = condition.split('=')
        (parent_attr_value, attr_value) = front.split(':')
        ele = xml.find_ele_by_attribute("list",
                                        "name",
                                        parent_attr_value.strip())
        for son in ele[0].iter():
            if condition_text == son.text:
                for s in son.getparent():
                    if s.get("name") == attr_value:
                        return s.text

    elif 2 == key.count(':'):
        child = []
        condition = key.strip('::')
        ele = xml.find_ele_by_attribute("list", "name", condition)
        for son in ele[0].iter():
            child.append(son.text)
        del child[0]
        return child



class ScfXml(ParseXML):
    def __init__(self, filepath):
        ParseXML.__init__(self, filepath)

    def find_attribute_and_modify_text(self, element, attr_name, attr_value, text_value):
        if (element.get(attr_name) != None) and (attr_value.upper() == element.get(attr_name).upper()):
            if element.text == None:#there is some element don't have text content. it's none.
                element.text = text_value
                return True
            elif element.text.strip() != "":
                element.text = text_value
                return True
            elif len(element.getchildren()) == 1 and len(element.values())==1 and element.values()[0].upper() == attr_value.upper():
                element.getchildren()[0].text = text_value
                return True

            else:
                print "**Error** Please check your condition"
        return False

    #used by change_xml_file, Type-1,5: 'iniMcsUl:20','iniMcsDl:28','phichRes:$N=2$'
    def find_and_modify_by_name(self, name, value):
        find_flag = False
        for son in self.root.iter():
            find = self.find_attribute_and_modify_text(son, "name", name, value)
            if find:
                find_flag = 1
                print "xml modify '%s.%s:%s' ok."%(self.get_ele_full_path(son), name, value)

        if 0==find_flag:
            raise Exception, "xml not find any name as '%s'"%name

    #used by change_xml_file, Type-2,3: 'LNBTS-19:actCellTrace=111', 'LNBTS-19:amRlcPBTab1:dlPollByte=222'
    def find_and_modify_by_mo_list_name(self, mo, lt, name, value):
        find_flag = 0
        mo_flag = 0
        list_flag = 0
        for son in self.root.iter():
            if 0 <= son.tag.find('managedObject') \
                    and None != son.get("distName") \
                    and 0 <= son.get("distName").upper().find(mo.upper()):
                mo_flag = 1
                for s in son.iter():
                    if 'NULL' == lt:
                        list_flag = 1
                        find = self.find_attribute_and_modify_text(s, "name", name, value)
                        if find:
                            find_flag = 1
                            print "xml modify '%s:%s=%s' ok."\
                                  %(mo, name, value)

                    else:
                        if 0 <= s.tag.find('list')  \
                                and s.get("name") != None \
                                and lt.upper() == s.get("name").upper():
                            list_flag = 1
                            for j in s.iter():
                                find = self.find_attribute_and_modify_text(j, "name", name, value)
                                if find:
                                    find_flag = 1
                                    print "xml modify '%s:%s:%s=%s' ok."\
                                                  %(mo, lt, name, value)

        if 0 == mo_flag:
            raise Exception, "xml can't find mo '%s' rest as '%s:%s=%s'"%(mo, lt, name, value)
        if 0 == list_flag:
            raise Exception, "xml can't find mo:list '%s:%s' rest as '%s=%s'"%(mo, lt, name, value)
        if 0 == find_flag:
            raise Exception, "xml can't find '%s:%s:%s=%s'"%(mo, lt, name, value)

    #used by change_xml_file, Type-4: 'LNBTS-19:integrityPrefL:eia1=444|eia0=1'
    def find_and_modify_by_condition(self, mo, lt, name, value, fname, fvalue):
        find_flag = 0
        mo_flag = 0
        list_flag = 0
        for son in self.root.iter():
            if 0 <= son.tag.find('managedObject') \
                     and None != son.get("distName") \
                     and 0 <= son.get("distName").upper().find(mo.upper()):
                mo_flag = 1
                for s in son.iter():
                    if 'NULL' == lt:
                        list_flag = 1
                        if 0 <= s.tag.find('}p') \
                                and s.get('name') != None \
                                and s.get('name').upper() == fname.upper() \
                                and fvalue == s.text:
                            for k in s.getparent():
                                if  k.get('name') != None and \
                                        k.get('name').upper() == name.upper():
                                    k.text = value
                                    find_flag = 1
                                    print "xml modify '%s:%s=<%s>|%s=%s' ok."%\
                                          (mo, name, value, fname, fvalue)
                    else:
                        if 0<= s.tag.find('list') \
                                and s.get("name") != None \
                                and lt.upper() == s.get("name").upper():
                            list_flag = 1
                            for j in s.iter():
                                if  j.get('name') != None \
                                        and (j.get('name').upper() == fname.upper()) \
                                        and (fvalue.upper() == j.text.upper()):
                                    for k in j.getparent():
                                        if  k.get('name') != None \
                                                and k.get('name').upper() == name.upper():
                                            k.text = value
                                            find_flag = 1
                                            print "xml modify '%s:%s:%s=<%s>|%s=%s' ok."\
                                                  %(mo, lt, name, value, fname, fvalue)
        #print mo_flag, list_flag
        if 0 == mo_flag:
            raise Exception, "xml can't find mo '%s' rest as '%s:%s=%s|%s=%s'"%\
                                (mo, lt, name, value, fname, fvalue)
        if 0 == list_flag:
            raise Exception, "xml can't find mo:list '%s:%s' rest as '%s=%s|%s=%s'"%\
                                (mo, lt, name, value, fname, fvalue)
        if 0 == find_flag:
            raise Exception, "xml can't find '%s:%s:%s=%s|%s=%s'"%\
                                (mo, lt, name, value, fname, fvalue)

    #used by change_xml_file, Type-6: 'MRBTS-666','LNBTS-777'
    def find_and_modify_all_mo(self, name, value):
        replace_count = 0
        for son in self.root.iter():
            if 0 <= son.tag.find('managedObject') \
                    and son.get("distName") != None \
                    and 0 <= son.get("distName").upper().find(name.upper()):
                tmp = son.get('distName').split('/')
                for j in range(len(tmp)):
                    if 0 <= tmp[j].find(name):
                        tmp[j] =  value
                        replace_count+=1

                new = '/'.join(tmp)
                son.set('distName', new)
        print "replace count is %d"%replace_count

def _add_miss_info(target_file):
    miss_info = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
    lines = file_read(target_file, "string")
    if not miss_info in lines:
        lines = miss_info + lines
        file_write(target_file, lines)

def change_xml_file(src_file, target_file, need_to_modify):
    """This keyword can change scf file with different input parameter, now can
      support this below four types of input parameter:
          1,A:B 2,A:B=C 3,A:B:C=D 4,A:B:C=D|E=F 5,A:$B=2$ 6,Exception
    1),With the first type A:B, this script will change all of the A in scf file to B.
    2),3),With the second and third type, first it will find the MO A, and then change it's
      childnode B to C or B's childnode C to D.
    4),With the fourth type, first it will find the MO A, and then find it's childnode B,
      then find B's childnode C and judge if the B's childnode E's value is F,if it is,
      change C to D,else Do next.
    5),If you want to change parameter's value such as <p name="phichRes">N = 1/2</p>,
      please write phichRes:$N=2$ in case.
    6),replace all of the exception type . For example, MRBTS-34 will replace all of
      the MRBTS value in scf to MRBTS-34, you also can type other value in MO.
      Such as LNCELL ,LNBTS etc
    The four types of parameter can mix in your case.

    | Input Parameters  | Man. | Description |
    | src_File_Dir      | Yes  | Path of config file  |
    | target_File_Dir   | Yes  | file name and path of file after modified  |
    | Need_to_Modify    | No   | Parameters need to modified, multi para modify should be a list, if only one para modify could be string |

    Example
    ${new_para_value} = ['antId:111','ANTL-1:rModId=555', 'ANTL-2:rModId=666',
                      'SMOD-1:linkList:radioMaster=sam|linkId=1',
                      'SMOD-1:linkList:radioMaster=Jone|linkId=2',
                      'RMOD-1:connectionList:sModId=samzhang','MRBTS-34','LNCEL-34'
                      'phichRes:$N=2$']
    | Change XML File   | D:\\SCF_1.xml  | SCF_new.xml | ${new_para_value} |
    | Change XML File   | D:\\SCF_1.xml  | SCF_new.xml | LNBTS-1852:actCellTrace=true |
    | Change XML File   | D:\\SCF_1.xml  | SCF_new.xml | ${EMPTY} |
    | Change XML File   | D:\\SCF_1.xml  | SCF_new.xml | ${None} |
     """

    print "Source file: '%s'"%src_file
    print "Target file: '%s'"%target_file
    if not isinstance(need_to_modify, list):
        if "" == need_to_modify or None == need_to_modify or " " == need_to_modify:
            print "xml don't need to modify! \nJust copy '%s' to '%s'"%(src_file, target_file)
            shutil.copyfile(src_file, target_file)
            return
        else:
            tmp = []
            tmp.append(need_to_modify)
            need_to_modify = tmp

    elif 0 == len(need_to_modify):
        print "xml don't need to modify! \nJust copy '%s' to '%s'"%(src_file, target_file)
        shutil.copyfile(src_file, target_file)
        return

    need_to_modify = set(need_to_modify)
    print "source modify list: ", need_to_modify

    key_type0 = []
    value_type0 = []

    mo1 = []
    list1 = []
    key_type1 = []
    value_type1 = []

    mo2 = []
    list2 = []
    find_name2 = []
    find_value2 = []
    key_type2 = []
    value_type2 = []

    key_type4 = []
    value_type4 = []

    type5 = []


    for target in need_to_modify:
        # Type-1,5: 'iniMcsUl:20','iniMcsDl:28','phichRes:$N=2$'
        if target.count(':') == 1 and target.count('|') == 0 \
           and (target.count('=') == 0 or target.count('$') == 2):
            (key, value) = target.split(':')
            key_type0.append(key.strip())
            value = value.strip().lstrip('$').rstrip('$')
            value_type0.append(value)

        # Type-2,3: 'LNBTS-19:actCellTrace=111', 'LNBTS-19:amRlcPBTab1:dlPollByte=222'
        elif target.count('|') == 0 and target.count('=') == 1\
                and target.count(':') >= 1:
            (name,value) = target.split('=')
            tmp = name.split(':')
            list_name = 'NULL'
            if 3 == len(tmp):
                list_name = tmp[1]
            mo1.append(tmp[0].strip())
            list1.append(list_name.strip())
            key_type1.append(tmp[-1].strip())
            value_type1.append(value.strip())

        # Type-4: 'LNBTS-19:integrityPrefL:eia1=444|eia0=1'
        elif target.count('|') == 1:
            (front, condition) = target.split('|')
            find_name_tmp2, find_value_tmp2 =  condition.split('=')
            find_name2.append(find_name_tmp2.strip())
            find_value2.append(find_value_tmp2.strip())

            (name,value) = front.split('=')
            tmp = name.split(':')
            list_name = 'NULL'
            if 3 == len(tmp):
                list_name = tmp[1]
            mo2.append(tmp[0].strip())
            list2.append(list_name.strip())
            key_type2.append(tmp[-1].strip())
            value_type2.append(value.strip())

        # Type-6: 'MRBTS-666','LNBTS-777'
        elif target.count(':') == 0 and target.count('=') == 0 and target.count('-') == 1:
            tmp = target.split('-')
            key_type4.append(tmp[0].strip())
            value_type4.append(target.strip())
        elif target.count('|') == 2:
            type5.append(target)
        else:
            msg = "Current support type as <1,A:B 2,A:B=C 3,A:B:C=D 4,A:B:C=D|E=F 5,A:$B=2$ 6,LNCEL-xxx>"
            raise Exception, "'%s' can't be parsed as any type. Please check.\n%s"%(target, msg)


    xml = ScfXml(src_file)

    # Type-1,5: 'iniMcsUl:20','iniMcsDl:28','phichRes:$N=2$'
    for i in range(len(key_type0)):
        xml.find_and_modify_by_name(key_type0[i], value_type0[i])

    # Type-2,3: 'LNBTS-19:actCellTrace=111', 'LNBTS-19:amRlcPBTab1:dlPollByte=222'
    for i in range(len(key_type1)):
        xml.find_and_modify_by_mo_list_name(mo1[i], list1[i], key_type1[i], value_type1[i])

    # Type-4: 'LNBTS-19:integrityPrefL:eia1=444|eia0=1'
    for i in range(len(key_type2)):
        xml.find_and_modify_by_condition(mo2[i], list2[i], key_type2[i], \
                                     value_type2[i], find_name2[i], find_value2[i])

    # Type-6: 'MRBTS-666','LNBTS-777'
    for i in range(len(key_type4)):
        xml.find_and_modify_all_mo(key_type4[i], value_type4[i])

    xml.write_xml_file(target_file)

    common_xml_operation(target_file, target_file, type5)

    _add_miss_info(target_file)



    pass#

"""
<?xml version="1.0" encoding="UTF-8"?>
 <raml version="2.1" xmlns="raml21.xsd">
  <cmData type="actual" scope="all">
   <header>
    <log dateTime="Fri May 11 18:01:58 +0800 2012" action="create" user="RROM"></log>
    <log dateTime="Fri May 11 18:07:02 +0800 2012" action="created" user="tdlte-tester" appInfo="Nokia Siemens Networks BTS Site Manager" appVersion="LNT2.0"></log>
   </header>
   <managedObject class="LNREL" distName="MRBTS-9/LNBTS-9/LNCEL-2305/LNREL-387" operation="create" version="LNT2.0">
    <p name="cellIndOffNeigh">0dB</p>
    <list name="ecgiPlmnId">
	<p name="antId">ANT1</p>
	<p name="phichRes">N = 1/2</p>
     <item>
      <p name="mcc">262</p>
     </item>
    </list>
   </managedObject>
   <managedObject class="ANTL" distName="MRBTS-10/ANTL-1" operation="create" version="LNT2.0">
     <p name="additionalRxGain">0</p>
	 <p name="antId">ANT1</p>
   </managedObject>
  </cmData>
 </raml>
 """


def common_xml_operation(src_file, tar_file, modify, stop_flag=False):
    """This keyword operate xml file such as modify/read attribute/text or add/delete element
    | Input Parameters  | Man. | Description |
    | src_file          | Yes  | Path of config file  |
    | tar_file          | Yes  | file name and path of file after modified  |
    | modify            | No   | change command and condition |
    \n
    1. Basic infomation about XML structure:
        a. What's attribute?
        b. What's tag?
        c. What's text?
        <managedObject class="LNREL" version="LNT2.0">
            <p name="additionalRxGain">0</p>
            <p name="antId">ANT1</p>
        </managedObject>
        | tag | manageObject |
        | attribute_name | class | version | name |
        | attribute_value | LNREL | LNT2.0 | antId |
        | text | ANT1 |
        | element tag full path | manageObject.p |
        | element with special attribute | class="ANTL" |
    \n
    2. Condition format:
        Sample as: "a|b|c"
        Description as: "action | modify/read attribute_value/text | the way to find target element"
        a. What do you want to do? action -> add/delete/modify/read
            (1) add -> element, format as "add|<p name=\"antId2\">ANT2</p>|tag=managedObject"
            (2) delete -> element, format as "delete||name=additionalRxGain"
            (3) modify -> attribute_value or text, format as "modify|text=60|name=additionalRxGain"
            (4) read -> attribute_value or text, format as "read|class|tag=managedObject"
        b. What need to modify/read/add?
            (1) "text=xxx" means modify the text content
            (2) "name=xxxx" means modify the attribute value
            (3) "text" means read the text content
            (4) "name" means read the attribute as "name"'s value
            (5) "<p>222</p>" means add the content
        c. How to locate the target element?
            <managedObject class="LNREL" version="LNT2.0">
                <p name="additionalRxGain">0</p>
                <p name="antId">ANT1</p>
            </managedObject>
           | No. | Type | Condition | Locate element |
           | 1 | by full tag path | managedObject..p | <p name="additionalRxGain">0</p><p name="antId">ANT1</p> |
           | 2 | by special attribute value | name=additionalRxGain | <p name="additionalRxGain"> |
           | 3 | by attribute and text content | name=antId && text=ANT1 | <p name="antId">ANT1</p> |
           | 4.1 | by complex relation 'parent' | text=ANT1 parent class=LNREL | <managedObject class="LNREL" version="LNT2.0"> |
           | 4.2 | by complex relation 'siblings' | name=antlId && text=ANT1 siblings name=additionalRxGain" | <p name="additionalRxGain">0</p> |
                Current support relation -> 'parent',
                                            'children',
                                            'previous',
                                            'next',
                                            'iterchild',
                                            'siblings'

    3. Detail sample for aruguents:
    | ${moidfy} | create list | modify |distname=0 |raml..cmData..managedObject | #modify attribute value by full tag path |
    | ...       | ...         | modify |key=2 |raml..cmData..managedObject | #add new attribute by full tag path |
    | ...       | ...         | modify |text=1| raml..cmData..header.log | #modify text by full tag path |
    | ...       | ...         | modify |text=22 |name=add..*onalRxGain | #modify text by special attribute value |
    | ...       | ...         | modify |text=bb |distName=\"MRBTS-10/ANTL-1\" children name=antId | #modify text by parent and children attribute |
    | ...       | ...         | modify |text=60 |name=antlId && text=2 siblings name=txRxUsage |
    | ...       | ...         | modify |text=abc |distName=.*MODPR-0 iterchild name=idleLBPercentageOfUes |
    | ...       | ...         | read |action |raml..cmData..header..log | #read attribute value by full tag path |
    | ...       | ...         | read || raml..cmData..header | #read element content by full tag path |
    | ...       | ...         | add |<p name=\"abc\">1</p>| name=add.*onalRxGain parent | #add siblings element with special attribute's |
    | ...       | ...         | delete || action="created" | #delete element with special attribute |
    | ${read_value} | common xml operation | d:\\scfc_1.xml | d:\\scfc_modify.xml | ${modify} |
    """
    xml = ParseXmlDict(src_file)
    if not isinstance(modify, list):
        modify = [str(modify)]
    read_value_list = xml.xml_common_operation(modify, stop_flag)
    xml.write_xml_file(tar_file)
    _add_miss_info(tar_file)
    return read_value_list

if __name__ == '__main__':
    """
    modify = ['modify   | distname=0 | raml..cmData..managedObject',
              'modify   | text=1=3   | raml..cmData..header..log',
              'modify   | text=22   | name=add.*onalRxGain',
              'modify   | text=bb   | distName=\"MRBTS-10/ANTL-1\" children name=antId',
              'read     | action    | raml..cmData..header..log',
              'read     |           | raml..cmData..header ',
              'add      | <p name=\"abc\">1</p>\n | name=add.*onalRxGain parent ',
              'delete   |           | name="cellIndOffNeigh" ']
    """
    #modify = ['delete |  | raml..cmData..managedObject not distName=PLMN-PLMN/MRBTS-816/LNBTS-816/LNCEL-1895.*']
    #print common_xml_operation("D:\\work\\xml\\original_Export_File_eNB816.xml", 'D:\\work\\xml\\modify.xml', modify)
    #modify = [#'modify | text=2 | text=CPLANE previous',
            #'read | text | text=CPLANE next']#itersiblings name=dscp
            #'delete |  | name=moPrId && text=1 parent']
            #"modify | text=60 | class=MODPR children name=idleLBPercentageOfUes"]
            #"modify | text=60 | name=antlId && text=2 siblings name=txRxUsage",
            #"modify | text=60 | distName=.*MODPR-0 iterchild name=idleLBPercentageOfUes"]
    #modify =      ["mo:LNADJ-30", "mo:LNADJL-5", "mo:adfadfa", "mo:LNADJL-4", "aa:dd"]#]
    modify = ['read|text|text=.*LNCEL-8451.*ECI-8450.* parent next iterchild tag=.*8015C0']
    #print common_xml_operation("d:\\work\\xml\\PM.BTS-33.20130618.134500.LTE.xml", 'd:\\2.xml', modify)
    """
    print read_configuration_file("d:\\work\\xml\\Export_File.xml", "distName=PLMN-PLMN/MRBTS-803/LNBTS-803/LNCEL-770:angle")
    print read_configuration_file("d:\\work\\xml\\Export_File.xml", "distName=PLMN-PLMN/MRBTS-803/LNBTS-803/LNCEL-771:angle")
    print read_configuration_file("d:\\work\\xml\\Export_File.xml", "distName=PLMN-PLMN/MRBTS-803/RET-1:angle")
    modify = ["read|text|distName=.*LNCEL-770 iterchild name=angle",
              "read|text|distName=.*LNCEL-771 iterchild name=angle",
              "read|text|distName=PLMN-PLMN/MRBTS-803/RET-1 iterchild name=angle"]#]
    print common_xml_operation("d:\\work\\xml\\Export_File.xml", 'd:\\2.xml', modify)
    """
    modify = [#'MODIMP-1:idleLBHrpdCelResPrio=1', 'MODIMP-1:idleLBRttCelResPrio=2',
        #'MOIMP-1:idleLBHrpdCelResPrio=3', 'CDFIM-1:rttBdClList:idleLBRttCelResPrio=6',
        #'IRFIM-1:idleLBEutCelResPrio=', 'IRFIM-2:idleLBEutCelResPrio=',
        #'LNBTS-1821:actSelMobPrf=true', 'CDFIM-1:hrpdBdClList:hrpdBdClBcl=1bc',
        #'MOIMP-1:idleLBRttCelResPrio=4', 'CDFIM-1:rttBdClList:rttBdClBcl=0bc',
       # 'LNBTS-1821:actIdleLB=true', 'LNCEL-5377:idleLBPercentageOfUes=100',
        #'MODPR-0:idleLBPercentageOfUes=100', 'UFFIM-1:idleLBUtranTddCelResPrio=',
        #'LNMME-0:ipAddrPrim=10.68.170.89',
        'CDFIM-1:hrpdBdClList:idleLBHrpdCelResPrio=7',
        #'MOPR-1:idleLBPercentageOfUes=100', 'LNCEL-5377:idleLBCellReSelPrio=',
        #'GNFL-1:idleLBGeranCelResPrio='
        ]
    #change_xml_file("D:\\tools\\for work\\SCFC_1.xml", "D:\\tools\\for work\\SCFC_12.xml",modify)
    print read_configuration_file("d:\\SCFC_41.xml", "distName=LNCEL-4610:a3Offset")
   # print common_xml_operation("d:\\SCFC_41.xml", 'd:\\2.xml', ["read|text|distName=.*LNCEL-4610 children name=a3Offset"])
