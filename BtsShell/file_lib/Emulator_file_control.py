# -*- coding: cp936 -*-
import os
import types
import shutil
import re



def change_emulator_configfile(src_File_Dir, target_File_Dir, Need_to_Modify=''):
    """This keyword can change emulator configfile ,such as parameters.ini. It can distinguish different node's same keyvalue
    
    | Input Paramaters | Man. | Description |
    | src_File_Dir     | yes  | Absolute path of attach_script file you want to modify |
    | target_File_Dir  | yes  | new attach_script file name(No path informatino,share absolute path with src_File_Dir) |
    | Need_to_Modify   | no   | new  [key:value] list you want to modify |
          
    Example
    |change_emulator_configfile |'parameters.ini'|'parameters_m.ini'|['HSS-1:diaPort=1','ENB-1:taId=250']|

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
            print "*INFO* Empty inputs, copy a new file: \"%s\"." %target_File_Dir
            return
        else:
            print 'ERROR:The input must be a empty string or a LIST(3rd parameter)!'
            raise TypeError
        
    #step 2:  handle parameters
    Object_list = []
    Key_List = [] 
    Value_List = []
    para_len=0
    try:
        for target in Need_to_Modify:
            if len(target)==0:             
                para_len=para_len+1
                continue
            tmp = target.split(':', 1)
            Object_list.append(tmp[0])
            Key_List.append(tmp[1].split('=', 1)[0])
            Value_List.append(tmp[1].split('=', 1)[1])
        if  para_len ==  len(Need_to_Modify):
            #if Need_to_Modify is a list['','',''],copy the old script.
            shutil.copyfile(src_File_Dir, target_File_Dir) 
            return        
    except:
        print ''''ERROR:The input parameter must be one ':' involved (3rd parameter)!'''
        raise TypeError
    
    #step 3: change new line and write it to target file
    f = file(src_File_Dir,'rb')
    file_target = open(target_File_Dir,'wb')
    linedic = f.readlines()
    currnode = ''
    
    try:
        for i in range(len(linedic)):
            tmpline = linedic[i]
            if len(linedic[i])==0 or linedic[i].startswith('#'):
                file_target.write(tmpline)
                continue
            for j in range(len(Object_list)):
                node_pattern = re.compile(('\[.*\]'))
                if re.search(node_pattern,linedic[i]):
                    currnode = linedic[i]                   
            for z in range(len(Key_List)):
                key_pattern = re.compile(('%s=.*\\n') % Key_List[z])
                tmpt='[%s]\n'%Object_list[z]
                if re.search(key_pattern,linedic[i]) and currnode ==tmpt:
                    tmp = re.sub(key_pattern,'%s=%s\\n'% (Key_List[z],Value_List[z]),linedic[i])
                    tmpline = tmp
                    currnodename = currnode.strip().lstrip("[").rstrip("]")
                    print "*INFO* Have modify parameter from \"%s:%s\" to \"%s:%s=%s\" success." \
                          %(currnodename, linedic[i].strip(), currnodename, Key_List[z], Value_List[z])
            file_target.write(tmpline)
            
    finally:
        f.close()
        file_target.close()


def Add_macro_command_to_macrofile(src_File_Dir, target_File_Dir, Need_to_Add=''):
    """This keyword can add macro cmd to macro file. This macro can delivered as a list
    
    | Input Paramaters | Man. | Description |
    | src_File_Dir     | yes  | Absolute path of attach_script file you want to modify |
    | target_File_Dir  | yes  | new attach_script file name(No path informatino,share absolute path with src_File_Dir) |
    | Need_to_Add      | no   | new string list you want to add |
          
    Example 
    |Add_macro_command_to_macrofile |'macro_hss.mac'|'macro_hss_tmp.mac'|['$rst$','hssap  hssap_reset','r','macro EndAndRun']|

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
    if type(Need_to_Add)is not types.ListType:
        if Need_to_Add=='':
            shutil.copyfile(src_File_Dir, target_File_Dir) 
            return
        else:
            print 'ERROR:The input must be a empty string or a LIST(3rd parameter)!'
            raise TypeError
        
    #step 2:  handle parameters
    para_len = 0
    try:
        for target in Need_to_Add:
             if len(target)==0:             
                para_len=para_len+1
                continue
        if  para_len ==  len(Need_to_Add):
             #if Need_to_Modify is a list['','',''],copy the old script.
             shutil.copyfile(src_File_Dir, target_File_Dir) 
             return        
    except:
        print ''''ERROR:The input parameter must be one ':' involved (3rd parameter)!'''
        raise TypeError
    
    #step 3: change new line and write it to target file
    f = file(src_File_Dir,'rb')
    file_target = open(target_File_Dir,'wb')
    linedic = f.readlines()
    
    try:
        for i in range(len(linedic)):
            tmpline = linedic[i]
            file_target.write(tmpline)
        for j in range(len(Need_to_Add)):
            tmpline = '%s \n' %Need_to_Add[j]
            file_target.write(tmpline)
                 
    finally:
        f.close()
        file_target.close()
        

    

if __name__ == '__main__':
    print change_emulator_configfile('parameters.ini','parameters_m.ini',['HSS-1:diaPort=1','ENB-1:taId=250'])
    #print Add_macro_command_to_macrofile('macro_hss.mac','macro_hss_tmp.mac',['$rst$','hssap  hssap_reset','r','macro EndAndRun'])
    pass 
