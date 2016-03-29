import os
import xlrd
import csv




def _parse_csv(file_path, start_line_num, get_item):
    csvfile = file(file_path, 'rb')
    result = csv.reader(csvfile)
    content_list = []
    for line in result:
        content_list.append(line)
    csvfile.close()    
    title_line =  content_list[start_line_num-1]
    index_list = []
    for item in get_item:
        index_list.append(title_line.index(item))        
      
    data = {}
    for i in range(start_line_num, len(content_list)):        
        content = content_list[i]  
        if 0 == len(content):
            continue   
        data[i] = {}  
        for j in range(len(index_list)):
            key = get_item[j]
            index = index_list[j]            
            value = content[index]            
            data[i][key] = str(value)          
    return data   
    
def _parse_excel(file_path, sheet_name, item_title_line_num, get_item_list):
    data = {}

    if os.path.isfile(file_path):
        try:
            sWorkBook = xlrd.open_workbook(file_path)
            if sheet_name in sWorkBook.sheet_names():
                sheetIndex = sWorkBook.sheet_by_name(sheet_name)
                item_list =  sheetIndex.row_values(item_title_line_num)
                index_list = []
                for item in get_item_list:
                    index = item_list.index(item)
                    index_list.append(index)

                
                
                for i in range(item_title_line_num+1, sheetIndex.nrows):
                    #data = {}
                    item_list =  sheetIndex.row_values(i)
                    tmp = i
                    data[tmp] = {}
                    for j in range(len(index_list)):
                        index = index_list[j]
                        item = get_item_list[j]
                        data[tmp][item] = str(item_list[index])

               
                return data


            else:
                print "WRN - Sheet %s not exist!" % sheetName
                return None
        except Exception, p_Err:
            print "ERR - %s" % p_Err

    else:
        print "WRN - Excel file %s not exist!" % sheetName
        return None

def _check_condition(key_value, single_data):
    #print key_value, single_data
    k, v = key_value.split('=') 
    if single_data[k] == v: 
        return True
    else:
        return False
        
def _get_value_by_condition(data, get_index, condition):
    result_list = []
    for d in data:
        flag = 0
        for c in condition:
            ret = _check_condition(c, data[d])
            if ret == True:
                flag += 1
        if flag == len(condition):
            result_list.append(data[d][get_index])        
    result_list.sort()
    result_list = set(result_list)
    return result_list, len(result_list)

def _parse_condition(precondition):
    item_list = []
    condition = []
    for c in precondition:
        k,v = c.split('=')        
        if v == '?':
            get_index = k
        else:
            condition.append(c)
        item_list.append(k)
    return item_list, get_index, condition
         
def get_csv_col_value(csv_path, start_line, pre_condition):
    item_list, get_index, condition = _parse_condition(pre_condition)     
       
    data = _parse_csv(csv_path, start_line, item_list) 
    
    result_list, num = _get_value_by_condition(data, get_index, condition)  
    
    return result_list, num        

def get_xls_col_value(xls_path, sheet_name, start_line, pre_condition):
    item_list, get_index, condition = _parse_condition(pre_condition)     
       
    data = _parse_excel(xls_path, sheet_name, start_line, item_list) 
    
    result_list, num = _get_value_by_condition(data, get_index, condition)  
    
    return result_list, num  

def list_compare(a_list, b_list):
    
    tmp1 = []
    for c in a_list:
        if c not in b_list:
            tmp1.append(c)

    
    tmp2 = []
    for c in b_list:
        if c not in a_list:
            tmp2.append(c)

    
    if len(tmp1)==0 and len(tmp2)==0:
        return True
    else:
        if len(tmp1)!=0:
            print "in a but not in b list is: ", tmp1
        if len(tmp2)!=0:
            print "in b but not in a list is: ", tmp2
            
        return False
        
           
if __name__ == '__main__':    

    xls_path = "D:\\work\\all problems\\other\\13w13 pangyuhua jira\\RISE_PM.xls"
    preconditon = ['Measurement=LTE Cell Resource',
                    'Document state=PUBLISHED', 
                    'Network element abbreviation=?']
    xls_list, xls_length = get_xls_col_value(xls_path, "Sheet1", 7, preconditon)
    
    csv_path = "D:\\work\\all problems\\other\\13w13 pangyuhua jira\\PMSummary_eNB889_BTS_20130325.csv"
    condition = ['Measurement type=LTE Cell Resource', 'Counter=?']
    csv_list, csv_length =  get_csv_col_value(csv_path, 3, condition)
    
    print "csv list length is: %s\nContent is: %s"%(csv_length, csv_list)
    print 
    print "xls list length is: %s\nContent is: %s"%(xls_length, xls_list) 
    
    print list_compare(csv_list, xls_list)
    

    
