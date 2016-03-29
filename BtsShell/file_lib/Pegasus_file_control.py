import os
import shutil
import re

def Change_Tps_For_Pegasus(src_file, target_file, need_modify=''):
    """Change pegasus Tps file .
    | Input Parameters  | Man. | Description |
    | src_file          | Yes  | The pegasus test file|
    | target_file       | Yes  | The last generated file which have been modified |
    | need_modify       | No   | The parameters which you want modified|

    Example
    | Change Tps For Pegasus| D:\\yongzhan\\Desktop\\LOM_Browser_get_rdcounters.xml | temp.xml |
                            |['_target:FSM1_FSP1_FARADAY7_CPU2']|
                            
    """    
    try:
        file_object = file(src_file, 'r')
    except:
        raise Exception, "test '%s' open failed" % src_file
    shutil.copy(src_file,target_file)
    try:
        new_file = file(target_file, 'w')
    except:
        raise Exception, "test '%s' open failed" % target_file

    lines = file_object.readlines()
    name_list = []
    value_list = []
    for item in need_modify:
        name,value = item.split(':', 1)
        name_list.append(name)
        value_list.append(value)        
    try:
        for line in lines:
            for i in range(len(name_list)):
                pat = '\s+.*(value=".*").*\s(name="%s")' % (name_list[i])
                if line.find(name_list[i]) > 0 and re.match(pat,line):
                    flag = line.split('"')[1]
                    pat_tmp = 'value="%s"' % flag
                    tmp_line = re.sub(pat_tmp,'value="%s"' %(value_list[i]),line)
                    line = tmp_line
                    print line                    
            new_file.write(line)

    finally:
        new_file.close()
        file_object.close()


def fetch_counters(counter_id,srcfile):
    """Can get counters from the Pegasus counter file(this file generatd by 
    Pegasus Tp --->TpStartRnDCounter)
    | Input Parameters  | Man. | Description |
    | counter_id        | Yes  | counter which exit in the log file|
    | srcfile           | Yes  | Pegasus counter file which generatd by TpStartRnDCounter |
    | Return value      | All of measurement result in this log |

    Example
    | Fetch Counters | 22000   | counter.csv  |
    | Fetch Counters | M8001C3 | counter.txt  |
    """
    try:
        file_object = file(srcfile, 'r')
    except:
        raise Exception, "counter log '%s' open failed" % srcfile

    lines = file_object.readlines()
    result = []
    try:
        for line in lines:
            items = line.split(',')
            if counter_id in items:
                result.append(items[3])
    finally:
        file_object.close()
        return result
