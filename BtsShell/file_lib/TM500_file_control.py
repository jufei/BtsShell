from __future__ import with_statement
import os
import types
import shutil
import re
import math
import glob
from xml.dom import minidom
import codecs


def change_tm500_script_file(src_File_Dir, target_File_Dir, Need_to_Modify=''):
    """Change tm500 attach_script file if the script changed and copy modified file with new name to target.

    | Input Paramaters | Man. | Description |
    | src_File_Dir     | yes  | Absolute path of attach_script file you want to modify |
    | target_File_Dir  | yes  | new attach_script file name(No path informatino,share absolute path with src_File_Dir) |
    | Need_to_Modify   | no   | new  [key:value] list you want to modify |

    Example
    | ${list}= | Create List | PHYCONFIGULTIMING:0 |
    | Change Tm500 Script File | C:\\Temp\\attach.xml | C:\\Temp\\attach_new_file.xml | ${list} |

    Note:
    if Need_to_Modify is string type but not empty string,the function will raise ValueError exception,
    if Need_to_Modify is neither string type nor list type,the function will raise TypeError exception.
    """

    path = os.path.dirname(src_File_Dir)
    target_name_temp=target_File_Dir
    if path == '':
        target_File_Dir='.\\'+target_File_Dir
    else:
        target_File_Dir = path + '\\'+target_File_Dir

    #step 1: if the Need_to_Modify is empty string,the function just do copy job,if it's othertype,raise TypeError
    if type(Need_to_Modify)is not types.ListType:
        if Need_to_Modify=='':
            shutil.copyfile(src_File_Dir, target_File_Dir)
            return
        else:
            print 'ERROR:The input must be a empty string or a LIST(3rd parameter)!'
            raise TypeError

    #step 2:  order parameters
    Key_List = []
    Value_List = []
    para_len=0
    try:
        for target in Need_to_Modify:
             if len(target)==0:
                para_len=para_len+1
                continue
             tmp = target.split(':')
             Key_List.append(tmp[0].upper())
             Value_List.append(tmp[1].upper())
        if  para_len ==  len(Need_to_Modify):
             #if Need_to_Modify is a list['','',''],copy the old script.
             shutil.copyfile(src_File_Dir, target_File_Dir)
             return
    except:
        print ''''ERROR:The input parameter must be one ':' involved (3rd parameter)!'''
        raise TypeError

    #step 3: renew  parameters
    f = file(src_File_Dir,'r')
    file_target = open(target_File_Dir,'w')
    try:
        for line in f.readlines():
            line=line.upper()
            temp=line
            if  len(line.strip())==0 or line.startswith('#'):
                continue
            for i in range(0,len(Key_List)):
                 pattern = re.compile(('%s\s+.*\\n') % Key_List[i])
                 if re.search(pattern,line):
                    if Key_List[i] == 'USIMCONFIG' and 15==len(Value_List[i]):                        
                        old = re.search("\[(\d{15})\s", line)
                        if old:
                            old_sim = old.groups()[0]
                            temp = line.replace(old_sim, Value_List[i])   
                        else:
                            print "Not find USIMCONFIG"
                    else:
                        temp = re.sub(pattern,'%s %s\\n'% (Key_List[i],Value_List[i]),line)
                        
            file_target.write(temp)
    finally:
        f.close()
        file_target.close()


def get_special_value_from_tm500_log(tm500_log, columnName):
    """This keyword reads TM500 log to get MCS value.

    | Input Parameters  | Man. | Description |
    | tm500_log         | Yes  | tm500 log file directory |
    | columnName        | No   | name want to read, such as "MCS", "SFN" and so on |

    | Return value | The list contains different MCS values with reading order |

    Example
    | Get MCS Value From TM500 Log | C:\\100601_113514_TDLTE-B7HGT2X_DLSCHRX_NA_0001.csv | mcs |
    """

    try:
        file_handle = file('%s' % (tm500_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_log

    lines = file_handle.readlines()
    mcs_list = []

    try:
        for line in lines:
            items = line.split(',')
            if columnName in items:
                position = items.index(columnName)
            if re.match('^\d.*\d+:\d+:\d+:\d+\,\d+', line):
                mcs_value = items[position]
                # exclude MCS value which is not integer or already in list
                if mcs_value not in mcs_list and '.' not in mcs_value:
                    mcs_list.append(mcs_value)
    finally:
        file_handle.close()
        return mcs_list

def solve_time_period_tm500(tm500_log, period):
    """This keyword reads tm500 log to get time period value.

    | Input Parameters  | Man. | Description |
    | tm500_log         | Yes  | tm500 log file directory |
    | period            | Yes  | srs's period we design |

    | Return value |is the different is right for peroid |

    Example
    | Solve Time Period Tm500 | C:\\100601_113514_TDLTE-B7HGT2X_DLSCHRX_NA_0001.csv | 10ms |
    """

    try:
        file_handle = file('%s' % (tm500_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_log
    lines = file_handle.readlines()
    time_list = []
    SFN_list = []
    d = []
    flag = 0
    try:
        for line in lines:
            items = line.split(',')
            if re.match('^\d.*\d+:\d+:\d+:(\d+)\,\d+', line):
                m=re.match('^\d.*\d+:\d+:\d+:(\d+)\,\d+', line)
                time_list.append(int(m.group(1)))
            if 'SFN' in items:
                position = items.index('SFN')
                SFN_list.append(items[position])
        for i in range(0,len(time_list)-1):
            diff=time_list[i+1]-time_list[i]
            diff1=SFN_list[i+1]-SFN_list[i]
            if diff<0:
                diff=1000+time_list[i+1]-time_list[i]
            if  str(diff)+'ms' == period:
                flag = 0
            if  str(diff)+'ms' != period:
                if diff/diff1 + 'ms' == period:
                    flag = 0
                else:
                    flag = 1
                print time_list[i+1],time_list[i],i

    finally:
        file_handle.close()
        if flag == 0:
            return True
        else:
            return False


def get_value_and_time_from_tm500_log(tm500_log, columnName="MCS"):
    """This keyword reads TM500 log to get special value and repeat time.

    | Input Parameters  | Man. | Description |
    | file_dir          | Yes  | TM500 log to be read |
    | column_name       | No   | Default is 'MCS' |

    | Return value | A dictionary contains different special values and time with reading order |

    Example
    | Get MCS Value and Time From TM500 Log | C:\\100601_113514_TDLTE-B7HGT2X_DLSCHRX_NA_0001.csv | mcs |
    """

    try:
        file_handle = file('%s' % (tm500_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_log

    lines = file_handle.readlines()
    mcs_dict = {}

    try:
        for line in lines:
            items = line.split(',')
            if columnName in items:
                position = items.index(columnName)
            if re.match('^\d.*\d+:\d+:\d+:\d+\,\d+', line):
                mcs_value = items[position]
                mcs_list = mcs_dict.keys()
                if mcs_value in mcs_list:
                    mcs_dict[mcs_value] = mcs_dict[mcs_value] + 1
                if mcs_value not in mcs_list and '.' not in mcs_value:
                    mcs_dict[mcs_value] = 1
    finally:
        file_handle.close()
        return mcs_dict


def get_TM500_average_value_and_contrast_base(tm500_log, columnName, base_value, filter_data=1000):
    """This keyword reads TM500 log to get value and calc the average ,then Contrast to Base.

    | Input Parameters  | Man. | Description  |
    | file_dir          | Yes  | tm500 log file directory |
    | columnName        | Yes  | read columndata by columnname  |
    | base_value        | Yes  | Contrast to average |
    | filter_data       | No   | if low than filter_data, del it |

    | Return value      |if return True ,avarage larger than  base_value,vice versa |

    Example
    | Get Tm500 Average Value And Contrast Base | D:\pechu\100812_141923_TDLTE-77HGT2X_L1THROUGHPUT_NA_0001.csv | Average DL SCH throughput per UE(kbps) | 1000 |
    """
    try:
        file_handle = file('%s' % (tm500_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_log

    lines = file_handle.readlines()
    data_list = []
    data_ave=0
    base_value=float(base_value)
    filter_data = float(filter_data)
    try:
        for line in lines:
            items = line.split(',')
            if columnName in items:
                position = items.index(columnName)
            if re.match('^\d.*\d+:\d+:\d+:\d+\,\d+,\d+',line):
                # exclude  value which is not integer or low than filter
                if  items[position] == '-' or items[position]== '-\n' or int(items[position]) <= filter_data  :
                    continue
                else:
                    data_value = int(items[position])
                data_list.append(data_value)
        data_ave=round(float(sum(data_list))/float(len(data_list)), 3)
    finally:
        print data_list
        file_handle.close()
        print data_ave
        if data_ave >= base_value :
            return True
        else  :
            return False


def get_highest_column_value_from_tm500_log(tm500_log, columnName):
    """This keyword reads tm500 log to get the highest value.

    | Input Parameters  | Man. | Description  |
    | tm500_log         | Yes  | tm500 log file directory  |
    | columnName        | Yes  | read columndata by columnname  |

    Example
    | Get Highest Column Value From Tm500 Log | C:\\100601_113514_TDLTE-B7HGT2X_DLSCHRX_NA_0001.csv | TB Size (TB: 0) |
    """

    try:
        file_handle = file('%s' % (tm500_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_log

    lines = file_handle.readlines()
    max_tbsize = 0
    tbsize_list = []
    print tbsize_list
    try:
        for line in lines:
            items = line.split(',')
            if columnName in items:
                position = items.index(columnName)
                print position
            if re.match('^\d+', line):
                if re.match('\d+', items[position]):
                    tbsize_list.append(int(items[position]))
        print tbsize_list
    finally:
        file_handle.close()
        if tbsize_list != []:
            return max(tbsize_list)
        else:
            raise Exception,'Tbsize_list is empty,please check log if have value or not'


def check_keywod_constant_value_from_tm500_log(tm500_log, KeyWord = 'CodeWord', Value = 1):
    """This keyword reads TM500 log to get MCS value.

    | Input Parameters  | Man. | Description  |
    | file_dir          | Yes  | tm500 log file directory  |
    | KeyWord           | Yes  | Keyword in TM500 log  |
    | Value             | Yes  | Keyword value  |

    | Return value      | KeyWord list |

    Example
    | Check Keywod Constant Value From Tm500 Log | C:\\100601_113514_TDLTE-B7HGT2X_DLSCHRX_NA_0001.csv | MCS | 28 |
    """

    try:
        file_handle = file(tm500_log, 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_log

    lines = file_handle.readlines()
    mcs_list = []

    try:
        for line in lines:
            items = line.split(',')
            if KeyWord in items:
                position = items.index(KeyWord)
            if re.match('^\d.*\d+:\d+:\d+:\d+', line):
                mcs_value = items[position]
                # exclude MCS value which is not integer or already in list
                if mcs_value not in mcs_list and '.' not in mcs_value and '-' not in mcs_value:
                    mcs_list.append(mcs_value)
    finally:
        file_handle.close()

    mcs_number = len(mcs_list)
    try:
        if mcs_number != 1:
            raise Exception,'*WARN*there is somthing wrong with MCS list: %s' % mcs_list
        if mcs_list[0] != Value:
            raise Exception,'*WARN*there is somthing wrong with MCS list: %s' % mcs_list
    except IndexError:
        pass


def get_max_min_average_value_from_tm500_log(tm500_log, columnName, tag = ''):
    """This keyword reads TM500 log to get Max Min and Average value in specified column.

    | Input Parameters  | Man. | Description |
    | file_dir          | Yes  | TM500 log file directory |
    | search_order      | No   | Column name |

    | Return value | The list contains different MCS values with reading order |

    Example
    | Get Max Min Average Value From Tm500 Log | C:\\100601_113514_TDLTE-B7HGT2X_DLSCHRX_NA_0001.csv | Subframe |
    """

    try:
        file_handle = file('%s' % (tm500_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_log

    lines = file_handle.readlines()
    max_value = 0
    min_value = 999999
    average_value = 0
    valid_line_Num = 0
    value_list = []
    try:
        for line in lines:
            items = line.split(',')
            if columnName in items:
                position = items.index(columnName)
            if re.match('^\d.*\d+:\d+:\d+:\d+\,\d+', line):
                if '-' not in items[position]:
                    try:
                        intValue = int(items[position])
                    except:
                        intValue = float(items[position])
                    value_list.append(intValue)
                """
                if intValue >= max_value:
                    max_value = intValue
                elif intValue <= min_value:
                    min_value = intValue
                average_value += intValue
                valid_line_Num += 1
                """

    finally:
        file_handle.close()
        if '' == tag:
            return max(value_list), min(value_list), sum(value_list)/len(value_list)
        else:
            return max(value_list), min(value_list), sum(value_list)/len(value_list), value_list
        #return max_value, min_value, average_value/valid_line_Num



def get_max_value_of_sum_two_column(tm500_log, columnName_first, columnName_second):
    """This keyword reads TM500 log to get plus of the two column and return as a list,
       then return the maximun of this list.
    | Input Parameters  | Man. | Description |
    | file_dir          | Yes  | TM500 log file directory |
    | search_order      | Yes  | columnName_first |
    | search_order      | Yes  | columnName_second |

    | Return value | Return the max value of two column plus |
    Example
    | Get Max Value Of Sum Two Column | C:\\100601_113514_TDLTE-B7HGT2X_DLSCHRX_NA_0001.csv | TB Size (TB: 0) | TB Size (TB: 1) |
    """

    try:
        file_handle = file('%s' % (tm500_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_log

    lines = file_handle.readlines()
    max_tbsize = 0
    tbsize_list = []
    try:
        for line in lines:
            items = line.split(',')
            if columnName_first and columnName_second in items:
                position_first = items.index(columnName_first)
                position_second = items.index(columnName_second)

            if re.match('^\d+', line):
                if re.match('\d+', items[position_first]) and re.match('\d+', items[position_second]):
                    tbsize_list.append(int(items[position_first]) + int(items[position_second]))
        #print tbsize_list
    finally:
        file_handle.close()
        return max(tbsize_list)


def get_all_of_a_column_vaule_as_a_list(tm500_log, columnName):
    """This keyword reads TM500 log to get all of a column value as a list, and return it.
       In addition it will print the value appeard maximum times and print it's appeard time.

    | Input Parameters  | Man. | Description |
    | tm500_log         | Yes  | TM500 log file directory |
    | columnName        | Yes  | columnName you want get |

    | Return value      | get_all_of_a_column_vaule_as_a_list |

    Example
    | Get All Of A Column Vaule As A List | C:\\100601_113514_TDLTE-B7HGT2X_DLSCHRX_NA_0001.csv | TB Size (TB: 0) |
    """

    try:
        file_handle = file('%s' % (tm500_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_log

    lines = file_handle.readlines()
    mcs_dict = {}
    mcs_list = []
    try:
        for line in lines:
            items = line.split(',')
            if columnName in items:
                position = items.index(columnName)
            if re.match('^\d.*\d+:\d+:\d+:\d+\,\d+', line):
                mcs_value = items[position]
                mcs_list = mcs_dict.keys()
                if mcs_value in mcs_list:
                    mcs_dict[mcs_value] = mcs_dict[mcs_value] + 1
                    mcs_list.append(mcs_value)
                if mcs_value not in mcs_list and '.' not in mcs_value:
                    mcs_dict[mcs_value] = 1
        #value max appear times
        print max(mcs_dict.values())
        print max(mcs_dict.keys())

    finally:
        file_handle.close()
        return mcs_list

def Check_signalling_appeared_in_specified_order(Protocal_log,mesg_list):
    """Check tm500 protocal's signalling in given squence
    | Input Parameters  | Man. | Description |
    | Protocal_log      | Yes  | TM500 protocal log |
    | mesg_list         | Yes  | columnName_first |

    | Return value | Return the appeared times of one mesg |
    Example
    | Check_signalling_appeared_in_specified_order | C:\\100601_113514_TDLTE-B7HGT2X_DLSCHRX_NA_0001.csv |mesg_list |
    """
    count = 0
    try:
        file_handle = file('%s' % (Protocal_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" %Protocal_log
    if type(mesg_list) is not types.ListType:
        print 'Error:The mesg list you input is not a list type'
        raise TypeError

    lines = file_handle.readlines()
    try:
        for line in lines :
            items = line.split(',')
            mesg_pattern = "  message c1 : %s : {\n" % (mesg_list[0])
            if mesg_pattern == items[0]:
                del mesg_list[0]
                print mesg_pattern
            if len(mesg_list)==0:
                break
        if len(mesg_list)==0:
            pass
        else:
            raise Exception, "The mesg_list you input doesn't appeared in your list order"

    finally:
        file_handle.close()

def Get_signalling_appeared_times(Protocal_log,singalling):
    """Check tm500 protocal log to get the appeared times of one mesg
    | Input Parameters  | Man. | Description |
    | Protocal_log      | Yes  | TM500 protocal log |
    | signalling        | Yes  | columnName_first |

    | Return value | Return the appeared times of one mesg |
    Example
    | Get_signalling_appeared_times | C:\\100601_113514_TDLTE-B7HGT2X_DLSCHRX_NA_0001.csv | TB Size (TB: 0) | TB Size (TB: 1) |
    """
    count = 0
    try:
        file_handle = file('%s' % (Protocal_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" %Protocal_log

    lines = file_handle.readlines()
    mesg_pattern = "  message c1 : %s : {\n" % (singalling)
    try:
        for line in lines:
            items = line.split(',')
            if mesg_pattern == items[0]:
                count += 1
            else:
                pass
    finally:
        file_handle.close()
        return count

def Get_average_value_of_last_dozen_of_row(Tm500_log,Columnname,Linenum =100):
    """Check tm500 log to get last dozen of clumn's average value
    | Input Parameters  | Man. | Description |
    | Tm500_log         | Yes  | TM500 log |
    | Columnname        | Yes  | Columnname |
    | Linenum           | No   | The num of lines you want get|

    | Return value | Return the appeared times of one mesg |
    Example
    | Get_average_value_of_last_dozen_of_row |101115_104554_TDLTE-B7HGT2X_DLSCHRX_NA_0001.csv | TB Size (TB: 0) |100 |
    """
    try:
        file_handle = file('%s' % (Tm500_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" %Tm500_log
    Linenum = int(Linenum)
    lines = file_handle.readlines()
    tmp = []
    count = 0
    try:
        for line in lines:
            items = line.split(',')
            if Columnname in items:
                index= items.index(Columnname)
            if re.match('^\d+',line):
                if re.match('\d+|\-',items[index]):
                    tmp.append(items[index])
        del tmp[len(tmp)-1]
        for i in range(Linenum):
            if re.match('\d+',tmp[len(tmp)-i-1]):
                thisnum = int(tmp[len(tmp)-i-1])
                count += thisnum

    finally:
        file_handle.close()
        return int(count)/Linenum

def check_dl_ul_subframe_in_tm500_log(tm500_log, columnName_first, columnName_second, uldl, UD_config):
    """This keyword reads TM500 log to verify down-link subframe is null in up-link frame,
       up-link subframe is null in down-link frame.
    | Input Parameters  | Man. | Description                   |
    | tm500_log         | Yes  | TM500 log file directory      |
    | columnName_first  | Yes  | columnName_first              |
    | columnName_second | Yes  | columnName_second             |
    | uldl              | Yes  | ul subframe or dl subframe    |
    | UD_config         | Yes  | uplink-downlink configuration |

    | Return value      | True or False                        |
    Example
    | check dl ul subframe in tm500 log | C:\\U_ULSCHTX_NA_0001.csv | Subframe | Modulation scheme | UL | 1 |
    """

    try:
        file_handle = file('%s' % (tm500_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_log

    lines = file_handle.readlines()
    first_list = []
    second_list = []
    try:
        for line in lines:
            items = line.split(',')
            if columnName_first and columnName_second in items:
                position_first = items.index(columnName_first)
                position_second = items.index(columnName_second)
            if re.match('^\d+', line):
                first_value = items[position_first]
                first_list.append(first_value)

                second_value = items[position_second]
                second_list.append(second_value)
    finally:
        file_handle.close()

    for i in range(len(first_list) - 1):
        if uldl == 'UL' and UD_config == '1' and first_list[i] in ('0', '4', '5', '9') and second_list[i] not in ('', '-'):
            print first_list[i], second_list[i]
            raise Exception, "DL subframe is not NULL in configuration 1"

        if uldl == 'UL' and UD_config == '2' and first_list[i] in ('0', '3', '4', '5', '8', '9') and second_list[i] not in ('', '-'):
            print first_list[i], second_list[i]
            raise Exception, "DL subframe is not NULL in configuration 2"

        if uldl == 'DL' and UD_config == '1' and first_list[i] in ('2', '3', '7', '8') and second_list[i] not in ('', '-'):
            print first_list[i], second_list[i]
            raise Exception, "UL subframe is not NULL in configuration 1"

        if uldl == 'DL' and UD_config == '2' and first_list[i] in ('2', '7') and second_list[i] not in ('', '-'):
            print first_list[i], second_list[i]
            raise Exception, "UL subframe is not NULL in configuration 2"

    return True


def get_cqi_ri_value_from_tm500_log(log_path, cqi, ri):
    """This keyword read tm500 protocol log to get cqi and ri value.
    | Input Parameters  | Man. | Description                  |
    | log_path          | Yes  | tm500 protocol log directory |
    | cqi               | Yes  | cqi-pmi-ConfigIndex          |
    | ri                | Yes  | ri-ConfigIndex               |
    | Return value      | cqi and ri value                    |
    Example
    | get_cqi_ri_value_from_tm500_log | C:\\***.csv | cqi-pmi-ConfigIndex | ri-ConfigIndex |
    """
    try:
        file_handle = file('%s' % (log_path), 'r')
    except:
        raise Exception, "tm500 log '%s' open failed" % log_path
    cqi_value = None
    ri_value = None
    lines = file_handle.readlines()
    pattern1 = ".*%s\s+(\d+).*" % (cqi)
    pattern2 = ".*%s\s+(\d+).*" % (ri)
    try:
        for line in lines:
            search_result1 = re.search(pattern1, line)
            if search_result1:
                cqi_value = search_result1.group(1)
                continue
            search_result2 = re.search(pattern2, line)
            if search_result2:
                ri_value = search_result2.group(1)
                continue
        if cqi_value or ri_value:
            return cqi_value, ri_value
        else:
            raise Exception, "This tm500 log do not include CQI&RI information"
    finally:
        file_handle.close()

def check_RI_value_in_tm500_protocol_log(MOD, ri, cqi=''):
    """This keyword check RI value according to ri and cqi value.
    | Input Parameters  | Man. | Description        |
    | MOD               | Yes  | 7 modes            |
    | ri                | Yes  | ri value           |
    | cqi               | No   | cqi value          |
    | Return value      | True or False             |
    Example
    | check_RI_value_in_tm500_protocol_log | "Mode1" | 161 |
    | check_RI_value_in_tm500_protocol_log | "Mode2" | 21  | 9 |
    """
    if type(ri) != type(1):
        try:
            ri = int(ri)
        except:
            raise Exception, 'ri given value %s is not integer' % ri
    if type(cqi) != type(1):
        try:
            cqi = int(cqi)
        except:
            raise Exception, 'cqi given value %s is not integer' % cqi

    if MOD == "Mode1":
        if ri >= 161 and ri <=321 and ((ri-161) % 20 == 0 or (ri-171) % 20 == 0):
            print "right"
            return True
        else:
            raise Exception, "false"

    elif MOD == "Mode2":
        if (cqi == 9 or cqi == 14) and (ri-1) % 10 == 0:
            print "right"
            return True
        elif (cqi == 8 or cqi == 13) and (ri-4) % 10 == 0:
            print "right"
            return True
        else:
            raise Exception, "false"

    elif MOD == "Mode3":
        if ri >= 161 and ri <=321 and ((ri-161) % 10 == 0 or (ri-171) % 10 == 0):
            print "right"
            return True
        else:
            raise Exception, "false"

    elif MOD == "Mode4":
        if ri >= 161 and ri <=321 and ((ri-161) % 40 == 0 or (ri-171) % 40 == 0):
            print "right"
            return True
        else:
            raise Exception, "false"

    elif MOD == "Mode5":
        if (cqi == 9 or cqi == 14) and (ri-1) % 20 == 0:
            print "right"
            return True
        elif (cqi == 8 or cqi == 13) and (ri-4) % 20 == 0:
            print "right"
            return True
        else:
            raise Exception, "false"

    elif MOD == "Mode6":
        if (ri-4) % 10 == 0:
            print "right"
            return True
        else:
            raise Exception, "false"

    elif MOD == "Mode7":
        if (ri-4) % 20 == 0:
            print "right"
            return True
        else:
            raise Exception, "false"

    else:
        raise Exception, "false"

def check_DCI_format(tm500_log, columnName_first, columnName_second, key):
    """This keyword reads TM500 log to get columnName_second value as a list according to columnName_first value.
       For example, when column 'Service Type' is 'DBCH', and column 'DCI Format' should only contain 'Format 1A'.

    | Input Parameters  | Man. | Description                               |
    | tm500_log         | Yes  | TM500 log file directory                  |
    | columnName_first  | Yes  | such as 'Service Type'                    |
    | columnName_second | Yes  | such as 'DCI Format'                      |
    | key               | Yes  | columnName_first 's value, such as 'RACH' |

    | Return value      | True or False                                    |

    Example
    | check_DCI_format | 'D:\\DLL1L2CONTROL_NA_0001.csv' | 'Service Type' | 'DCI Format' | 'DL-SCH' |
    | check_DCI_format | 'D:\\DLL1L2CONTROL_NA_0001.csv' | 'Service Type' | 'DCI Format' | 'PCH'    |
    | check_DCI_format | 'D:\\DLL1L2CONTROL_NA_0001.csv' | 'Service Type' | 'DCI Format' | 'DBCH'   |
    | check_DCI_format | 'D:\\DLL1L2CONTROL_NA_0001.csv' | 'Service Type' | 'DCI Format' | 'RACH'   |
    """

    try:
        file_handle = file('%s' % (tm500_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_log

    lines = file_handle.readlines()
    value_list = []

    try:
        for line in lines:
            items = line.split(',')
            if columnName_first and columnName_second in items:
                position_first = items.index(columnName_first)
                position_second = items.index(columnName_second)

            if re.match('^\d.*\d+:\d+:\d+:\d+\,\d+', line):

                if items[position_first] == key:
                    value_list.append(items[position_second])

    finally:
        file_handle.close()

    if key == 'DL-SCH' and 'Format 1A' not in value_list:
        raise Exception, "when Service Type is 'DL-SCH', DCI Format does not contain 'Format 1A'"
        return False

    if key == 'PCH' and 'Format 1A' not in value_list:
        raise Exception, "when Service Type is 'PCH', DCI Format does not contain 'Format 1A'"
        return False

    for i in range(len(value_list)):
        if key == 'DBCH' and value_list[i] != 'Format 1A':
            raise Exception, "when Service Type is 'DBCH', DCI Format is not only 'Format 1A'"
            return False

        if key == 'RACH' and value_list[i] != 'Format 1A':
            raise Exception, "when Service Type is 'RACH', DCI Format is not only 'Format 1A'"
            return False

    return True

def get_drx_start_offset(protocal_log):
    """ This keyword read tm500 protocol log, find character string "longDRX-CycleStartOffset sf80 : 73"
        return two integer, e.g. 80 73

    | Input Parameters  | Man. | Description |
    | protocal_log      | Yes  | protocol log directory |

    | Return value | two integer |

    Example
    | get drx start offset | D:\\TM500 log\\U_PROT_LOG_ALL.csv |
    """

    try:
        file_handle = file('%s' % (protocal_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % protocal_log

    lines = file_handle.readlines()

    try:
        for line in lines:
            search_result = re.search('.*longDRX-CycleStartOffset sf(\d+) : (\d+).*', line)
            if search_result:
                offset1 = search_result.groups()[0]
                offset2 = search_result.groups()[1]
                return offset1, offset2
        raise Exception, "This log do not include DRX start offset information"
    finally:
        file_handle.close()

def check_drx_offset_in_cqi_log(tm500_CQI_log, drx_offset1, drx_offset2):
    """ This keyword read tm500 cqi log, input parameter drx_offset1 and drx_offset2,
        are return value of get_drx_start_offset.
        According to formula: (SFN*10 + Subframe) MOD drx_offset1 == drx_offset2,
        SFN and Subframe are column name of tm500 cqi log.
        If formula true, column Rank should not be '-'

    | Input Parameters  | Man. | Description |
    | tm500_CQI_log     | Yes  | cqi log directory                    |
    | drx_offset1       | Yes  | return value of get_drx_start_offset |
    | drx_offset2       | Yes  | return value of get_drx_start_offset |

    Example
    | check drx offset in cqi log | D:\\TM500 log\\CQIREPORTING_ALL_0001.csv | 80 | 73 |
    """

    drx_offset1 = int(drx_offset1)
    drx_offset2 = int(drx_offset2)

    try:
        file_handle = file('%s' % (tm500_CQI_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_CQI_log

    lines = file_handle.readlines()

    try:
        for line in lines:
            items = line.split(',')
            if 'SFN' in items:
                position_SFN = items.index('SFN')
                position_Subframe = items.index('Subframe')
                position_Rank = items.index('Rank')

            if re.match('^\d.*\d+:\d+:\d+:\d+\,\d+', line):
                SFN = int(items[position_SFN])
                Subframe = int(items[position_Subframe])

                if (SFN * 10 + Subframe) % drx_offset1 == drx_offset2 and items[position_Rank] == '-':
                    raise Exception,"when SFN is '%s' and Subframe is '%s', Rank should not be -" % \
                          (items[position_SFN], items[position_Subframe])

    finally:
        file_handle.close()

    return True

def get_IE_value_from_protocol_log(tm500_protocol_log, ie_name):
    """This keyword used for getting IE value from TM500 protocol log.

    | Input Parameters   | Man. | Description |
    | tm500_protocol_log | Yes  | tm500 protocol log file location |
    | ie_name            | Yes  | the name of IE(Info element) |

    | Return value | The value of the IE value list in the tm500 protocol log |

    Example
    | get_IE_value_from_protocol_log | C:\\110615_205223_U_PROT_LOG_ALL.csv |  preambleTransMax  |
    """

    try:
        file_handle = file('%s' % (tm500_protocol_log), 'r')
    except:
        raise Exception, "TM500 protocol log '%s'  open failed" % tm500_protocol_log

    try:
        pattern = '^.*%s(\s+:?\'?)(-?\w+)(.*)' %ie_name
        lines = file_handle.readlines()
        value_list = []

        for line in lines:
            ret = re.match(pattern, line)
            if ret:
                value_list.append(ret.group(2))

    finally:
        file_handle.close()
        if len(value_list) == 0:
            raise Exception, "Can not found the IE_name in portocol log.Please check the IE name \
                               is right or not !"
        return value_list

def get_column_value_from_tm500_log(tm500_log, *column_names):
    """This keyword reads TM500 log to get column value as list.

    | Input Parameters  | Man. | Description |
    | tm500_log         | Yes  | TM500 log file directory |
    | column_names      | No   | Column names |

    | Return value | The tuple contains number of lists which corresponding with values |

    Example
    | Get Column Value From TM500 Log | C:\\100601_113514_TDLTE-B7HGT2X_ULSCHTX_NA_0001.csv | PUCCH Format | TB size | Scheduling Request |
    """

    ret = glob.glob("%s" %(tm500_log))
    print ret
    if len(ret) ==1:
        tm500_log = ret[0]
    else:
        raise Exception, "Pls input a right file name!"

    try:
        file_handle = file('%s' % (tm500_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_log

    lines = file_handle.readlines()

    class Column:
        sequence = 1
        def __init__(self, name):
            self.name = name
            self.position = None
            self.value_list = []
            self.sequence = Column.sequence
            Column.sequence += 1
        def __cmp__(self, other):
            return cmp(self.sequence, other.sequence)

    columns = {}
    column_value_list = []
    for column_name in column_names:
        columns[column_name] = Column(column_name)
        column_value_list.append([])

    position_found = False

    try:
        for line in lines:
            items = line.split(',')
            if not position_found:
                for column_name in columns.keys():
                    if column_name in items:
                        columns[column_name].position = items.index(column_name)
                position_found = True
                for column in columns.values():
                    if not column.position:
                        position_found = False
            if re.match('^\d?.*(\d+:)+\d+', line):
                for column_name in columns.keys():
                    try:
                        columns[column_name].value_list.append(items[columns[column_name].position].replace('\n', ''))
                    except:
                        pass
        # make column_list the same order as user input
        column_list = [column for column in columns.values()]
        column_list.sort()
        column_value_list = [column.value_list for column in column_list]
    finally:
        file_handle.close()
        return len(column_value_list) ==1 and column_value_list[0] or column_value_list

def get_column_values_according_another_column(tm500_log, basic_column, basic_value, *column_names):
    """This keyword reads TM500 log to get column values according another column value

    | Input Parameters  | Man. | Description |
    | tm500_log         | Yes  | TM500 log file directory |
    | basic_column      | No   | Basic Column names |
    | basic_value       | No   | Basic value |
    | *column_names     | No   | Column names|

    | Return value | The tuple contains number of lists which corresponding with values |

    Example
    | get_column_value_according_one_column_value | test.csv | MIMO transmission | asdf | Virtual RB Type |
    """
    ret = glob.glob("%s" %(tm500_log))
    print "*INFO* You log file is:" ,ret
    if len(ret) ==1:
        tm500_log = ret[0]
    else:
        raise Exception, "Pls input a right file name!"

    with file(tm500_log, 'r') as file_handle:
        lines = file_handle.readlines()
    
    basic_position = ""
    comp_column = []
    result = []
    class Column:
        def __init__(self,name):
            self.name = name
            self.value = []
            self.position = None

    for line in lines:
        items = line.split(',')
        if not basic_position:
            if basic_column in items:
                basic_position = items.index(basic_column)
            else:
                continue
            for column in column_names:
                if column in items:
                    comp_column.append(Column(column))
                    comp_column[-1].position = items.index(column)
        if re.match('^\d.*\d+:\d+:\d+:\d+\,(\d+|-|(NA))', line):
            if items[basic_position] == basic_value:
                for colum in comp_column :
                    if colum.position:
                        colum.value.append(items[colum.position])
    result = [column.value for column in comp_column]
    return len(result) ==1 and result[0] or result



def _modify_Filezilla_config_file(TMA_version,file_path):
    """This keyword used for modification Filezilla config file to change TM500 version.
    | Input Parameters  | Man. | Description |
    | TMA_version       | Yes  | want to change to the tm500 version |
    | file_path         | Yes  | Filezilla config file's path  |

    Example
    | modify_Filezilla_config_file | TMA_version | file_path |
    """

    xmldoc = minidom.parse(file_path)
    flag = _parse_xml(xmldoc,TMA_version)
    print flag

    if flag == True:
        try:
            file_Object = file(file_path, 'w')
            writer = codecs.lookup('utf-8')[3](file_Object)
            xmldoc.writexml(writer, encoding = 'utf-8')
        finally:
            writer.close()
    if flag == False:
            raise Exception, "The version of TMA is wrong,please check"


def _parse_xml(_xmldoc,TMA_version,username = 'fts24_manf',option = 'IsHome',value1 = '1',value2 = '0'):
    flag = False
    root = _xmldoc.firstChild
    items = root.childNodes
    for elem in items:
        if elem.nodeType == elem.ELEMENT_NODE:
            if elem.tagName == 'Users':
                users = elem.childNodes
                for user in users :
                    if user.nodeType == user.ELEMENT_NODE:
                        if user.getAttribute(user.attributes.keys()[0]) == username:
                            Pes = user.childNodes
                            for Pe in Pes:
                                if Pe.nodeType == Pe.ELEMENT_NODE:
                                    if Pe.tagName == 'Permissions':
                                        Dirs = Pe.childNodes
                                        for Dir in Dirs:
                                            if Dir.nodeType == Dir.ELEMENT_NODE:
                                               if TMA_version in Dir.getAttribute(Dir.attributes.keys()[0]):
                                                   flag = True
                                                   Opts = Dir.childNodes
                                                   for Opt in Opts:
                                                       if Opt.nodeType == Opt.ELEMENT_NODE:
                                                           if Opt.getAttribute(Opt.attributes.keys()[0]) == option:
                                                               Opt.replaceChild(_xmldoc.createTextNode(value1),Opt.firstChild)
                                               else:
                                                    Opts = Dir.childNodes
                                                    for Opt in Opts:
                                                        if Opt.nodeType == Opt.ELEMENT_NODE:
                                                            if Opt.getAttribute(Opt.attributes.keys()[0]) == option:
                                                                Opt.replaceChild(_xmldoc.createTextNode(value2),Opt.firstChild)
    return flag


def check_delta_DRS_result(tm500_log, mean_baseValue, variance_baseValue):
    """This keyword reads TM500 L1RBPOWERS log, get mean and variance value
       from Power Delta (Port 7 RB: 0) to Power Delta (Port 7 RB: 99),
       then compare with given mean_baseValue and variance_baseValue,
       if mean smaller than mean_baseValue, or variance larger than variance_baseValue, raise Exception.

    | Input Parameters   | Man. | Description                            |
    | tm500_log          | Yes  | TM500 L1RBPOWERS log file directory    |
    | mean_baseValue     | Yes  | given parameter, compare with mean     |
    | variance_baseValue | Yes  | given parameter, compare with variance |
                  |
    Example
    | check_delta_DRS_result | 'D:\\L1RBPOWERS_NA_0001.csv' | '5' | '2' |
    """

    data_list7 = []
    position7  = []
    column7    = []

    mean_baseValue     = float(mean_baseValue)
    variance_baseValue = float(variance_baseValue)

    for i in range(100):
        position7.append('Power Delta (Port 7 RB: %s)(dBm/SC)' % str(i))

    try:
        file_handle = file('%s' % (tm500_log), 'r')
    except:
        raise Exception, "TM500 log '%s' open failed" % tm500_log

    lines = file_handle.readlines()

    try:
        for line in lines:
            items = line.split(',')
            if position7[0] in items:
                SFN_position = items.index('SFN')
                for i in range(100):
                    column7.append(items.index(position7[i]))

            if re.match('^\d.*\d+:\d+:\d+:\d+\,\d+',line):
                SFN_number = items[SFN_position]
                data_list7 = []
                for i in range(100):
                    data_list7.append(items[column7[i]])
                print data_list7
                ret7 = _mean_variance(data_list7)
                print ret7

                if ret7[0] < mean_baseValue:
                    raise Exception, 'SFN %s Power Delta (Port 7) mean %s is smaller than %s!' \
                        %(SFN_number, ret7[0], mean_baseValue)

                if ret7[1] > variance_baseValue:
                    raise Exception, 'SFN %s Power Delta (Port 7) variance %s is larger than %s!' \
                        %(SFN_number, ret7[1], variance_baseValue)

    finally:
        file_handle.close()

def _mean_variance(data_list):
    """
    This keyword compute mean and variance from a list, return them.
    """
    if len(data_list) == 0:
        raise Exception, 'There is no data in list!'
    summation1 = 0
    summation2 = 0
    for i in range(len(data_list)):
        if '-' != data_list[i]:
            summation1 += float(data_list[i])
    mean = summation1/len(data_list)

    for i in range(len(data_list)):
        summation2 += math.pow((float(data_list[i]) - mean), 2)
    variance = math.sqrt(summation2 / (len(data_list)-1))

    return mean, variance

if __name__ == '__main__':
    log = "E:\\huangchao\\set_attenuation\\11\\third_ttiTraceUL.csv"
    print get_column_values_according_another_column(log, 'ETtiTraceUlParUe_numDrb', '1',\
                                               'ETtiTraceUlParUe_sinrPusch', 'ETtiTraceUlParUe_rssiPusch')
    #print get_column_value_from_tm500_log(log, "ETtiTraceUlParCell_numUesCs")
    #print get_srs_info_as_a_list('D:\\ULSRS_NA.csv', "Penultimate Location", 'SFN', '39')
    #print get_cqi_ri_value_from_tm500_log('D:\\test\\Liming\\UE00.csv', 'cqi-pmi-ConfigIndex', 'ri-ConfigIndex')
    #print get_max_min_average_value_from_tm500_log('D:\UEoverview.csv', 'UL-SCH BLER')
    #print check_delta_DRS_result('D:\\L1RBPOWERS_NA_0001.csv', '5', '2')
    #mo = ['UsimConfig:262030020000083', 'PhyConfigSysCap: 2 8 4']
    #change_tm500_script_file("d:\\attach_MIMO.txt", "attach_MIMO1.txt", mo)
    pass
