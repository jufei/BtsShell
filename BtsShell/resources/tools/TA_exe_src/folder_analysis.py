from __future__ import with_statement
import re
import os
import glob

def file_read(file_path, output_format="list", read_mode = 'r'):
    if not os.path.isfile(file_path):
        raise Exception, "File %s does not exists" % (file_path)
    try:
        with open(file_path, read_mode) as file_obj:
            if "string" == output_format:
                return file_obj.read()
            else:
                return file_obj.readlines()
    except IOError:
        raise Exception, "Open %s failed!" % (file_path)


              
f_list = []    

def get_folder_files_path(folder_dir, ext='LOG'):      
    if not os.path.exists(folder_dir):
        raise Exception, "'%s' is not exist!" % folder_dir
    multi_tupple = os.walk(folder_dir)
    
    for root, folders, files in multi_tupple :
        #print root, len(folders), folders,  len(files),files
        for folder in folders:             
            get_folder_files_path(os.path.join(root, folder))  
        for file_name in files:     
            if file_name.endswith(ext): 
                f_list.append(os.path.join(root, file_name)) 
        break    
    return f_list
                   


def _check_file_contain_not_contain_kw(folder_path, check_list):
    all_result = []
    f_all = get_folder_files_path(folder_path)
    for f in f_all:
        file_dict = {}
        file_dict['name'] = f
        #file_dict['Y'] = []
        #file_dict['N'] = []
        f_content = file_read(f,'string')
        for check in check_list:
            
            num = f_content.count(check)
            file_dict[check] = num
                
        #print file_dict
        all_result.append(file_dict)
    
    #for r in all_result:
    #    if 0 == len(r['Y']):
    #        print "This file '%s' contain nothing."%r['name']
    #    if 1 < len(r['Y']):
    #        print "This file '%s' contain more than one conditions '%s'."%(r['name'],r['Y'])
    return all_result    

def _statistic_kw_appear_times(result_list, check_list):
    check_dict = {}
    for check in check_list:
        check_dict[check] = 0
    for result in result_list:        
        for check in check_list:
            #print check, result
            #print check_dict[check] , result[check]
            check_dict[check] += result[check]
        
    #for c in check_dict.keys():
    #    print "kw:'%s', times:'%s'"%(c , check_dict[c])  
    return check_dict
    
def _calcute_finally_result(check_dict):
    result_list = []
    weight_all = 0
    actual_all = 0
    for check in check_dict.keys():
        new_dict = {}
        new_dict['name'] = check
        weight = int(re.search('weight=(\d+)',check).groups()[0])
        new_dict['weight'] = weight
        actual = check_dict[check]
        new_dict['actual'] = actual
        weight_all += weight
        actual_all += actual
        result_list.append(new_dict)
    
    all_expect = 0
    all_sqr = 0
    for r in result_list:
         expect = actual_all*r['weight']/weight_all
         r['expect'] = expect
         all_expect += expect
         all_sqr += (r['expect']-r['actual'])**2

    for result in result_list:
        print  "kw:'%s', weight is '%s', \tactual times is '%s', \texpect num is '%s'"%\
                (result['name'],result['weight'],result['actual'],result['expect']) 
    
    print "total weight is '%s', total actual is '%s', total expect num is '%s'"\
                %(weight_all, actual_all, all_expect) 
    
    print "all sqr_num is : ",all_sqr  
    finally_result = all_sqr**0.5 / all_expect
    print "finally result is : ", finally_result
    return finally_result

def check_and_calcute_test_result(folder_path, check_list, expect_value):
    ret = _check_file_contain_not_contain_kw(folder_path, check_list) 
    check_dict = _statistic_kw_appear_times(ret, check_list)  
    finally_result = _calcute_finally_result(check_dict)
    if finally_result >= expect_value:
        raise Exception, "The finally result is %s >= %s(expect value)"%\
                    (finally_result, expect_value)
        
    
if __name__ == '__main__':
    check_list = ['balancing: CDMA RTT bandClass=0 weight=30',
                  'balancing: CDMA HRPD bandClass=1 weight=30',
                  'balancing: GERAN bandInd=0 weight=30',
                  'balancing: EUTRA dlCarFreq=111 weight=30',
                  'balancing: EUTRA dlCarFreq=38000 weight=30',
                  'balancing: UTRA TDD dlCarFreq=10067 weight=30',
                  'balancing: EUTRA dlCarFreq=222 weight=15 prio=4']    
    folder_path1 = "D:\\work\\caobin\\testing_log_for_ta"  
    
    ck_list = ['Main target for load balancing: CDMA RTT bandClass=0 weight=10',
                 'Main target for load balancing: CDMA HRPD bandClass=1 weight=10',
                 'Main target for load balancing: GERAN bandInd=0 weight=20',
                 'Main target for load balancing: EUTRA dlCarFreq=111 weight=20',
                 'Main target for load balancing: UTRA TDD dlCarFreq=10067 weight=20']
    folder_path = "D:\\work\\caobin\\BtslogZipDir"              
    check_and_calcute_test_result(folder_path, ck_list, 10)  
      