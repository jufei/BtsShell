from BtsShell import connections
import time
import types


def Start_emulator(version_path='/root/Desktop/LTE_emu_Feb11_v100'):    
    """Start emulator with emumgr.sh script and the check if the four process is ok .    
    | Input Parameters | Man. | Description |
    | version_path     | No   | The emulator version path (start emulator with this packege)|
    | checklist        | No   | The keyword list will be checked after emulator start and these keywords will displayed with 'ps -fe' command|
    Example
    | Start_emulator | '/root/Desktop/LTE_emu_Feb11_v100' |'[./HSS,./MME]'|    
    """
    #Emulator_prompt=["^.*\[%s@.* ~\]# "%username,]
    Emulator_prompt=["#"] 
    #connections.set_host_prompt(Emulator_prompt)
    connections.execute_shell_command_without_check('export DISPLAY=:0.0')
    connections.execute_shell_command_without_check('cd "%s"/scripts/' % version_path)
    startcheck = connections.execute_shell_command_without_check('./emumgr.sh start')
       

def Stop_emulator(version_path='/root/Desktop/LTE_emu_Feb11_v100'):
    """Stop emulator with emumgr.sh script and the check if the four process ,make sure the process is stoped proprely.
    | Input Parameters | Man. | Description |
    | version_path     | No   | The emulator version path (start emulator with this packege)|
    Example
    | Start_emulator | '/root/Desktop/LTE_emu_Feb11_v100' |'[./HSS,./MME]'|    
    """
    Emulator_prompt=["#"] 
    #connections.set_host_prompt(Emulator_prompt)
    connections.execute_shell_command_without_check('export DISPLAY=:0.0')
    connections.execute_shell_command_without_check('cd "%s"/scripts/' % version_path)
    connections.execute_shell_command_without_check('./emumgr.sh stop')
    time.sleep(5)
    processcheck = connections.execute_shell_command_without_check('ps -fe')
    checklist = ['HSS','MME','UPE','INET']
    for proce in checklist:
        proceprompt = './%s' % proce
        if processcheck.find(proceprompt)>0:
            connections.execute_shell_command_without_check('killall -9 %s' %proce)
    else:
        pass
        
         
def __Replace_emulator_configfile(config_file_path,version_path='/root/Desktop/LTE_emu_Feb11_v100',config_bakpath='/root/Desktop/config_bak',time_prefix='1'):
    """Move old configfile to config_bakpath, then copy a new config file to version_path    
    | Input Parameters | Man. | Description |
    | config_file_path | yes  | This file contain the configfile of your emulator|
    | version_path     | No   | The emulator version path (start emulator with this packege)|
    | config_bakpath   | No   | This is a path that will resave you courrent configfile,this path must exist|
    Example
    | Replace_emulator_configfile | '/root/Desktop/configfile'|'/root/Desktop/LTE_emu_Feb11_v100'|'/root/Desktop/config_bak' |
    """
    #connections.execute_shell_command_without_check('rm -rf %s/config/parameters.ini' %version_path)
    mv_cmd = 'mv %s/config/parameters.ini  "%s/parameters_bak_%s.ini"' %(version_path ,config_bakpath, time_prefix)
    connections.execute_shell_command_without_check(mv_cmd)
    cp_cmd = "cp %s/parameters.ini %s/config/" %(config_file_path ,version_path)
    connections.execute_shell_command_without_check(cp_cmd)


def __Start_one_process_of_emulator(process='HSS' ,errorlist = [],version_path='/root/Desktop/LTE_emu_Feb11_v100'):    
    """Start one process of emulator, and check if error happens .   
    | Input Parameters | Man. | Description |
    | version_path     | Yes  | The emulator version path (start emulator with this packege)|
    | process          | Yes  | 
    | errorlist        | Yes  | The keyword list will be checked after emulator start and these keywords will displayed with 'ps -fe' command|
    Example
    | Start_one_process_of_emulator |'HSS'|['aborted','error']|'/root/Desktop/LTE_emu_Feb11_v100' |    
    """
    chlist = []
    if type(errorlist) != types.ListType:
        chlist.append(errorlist)
    else:
        chlist = errorlist

    if process =='HSS' or process =='hss': 
        connections.execute_shell_command_without_check('cd "%s"/cn/emutop/system/hss' % version_path)
        old_prompt = connections.set_host_prompt('state(\s+):(\s*)initialized')        
        processcheck = connections.execute_shell_command_without_check('./hss')
        for error in chlist:
            if processcheck.find(error)>0:
                raise Exception, 'Error %s happend !' %error
        #connections.set_host_prompt('^:\s$')
        #connections.execute_shell_command_without_check('\r')
        connections.set_host_prompt(old_prompt)
        
    elif process =='MME' or process =='mme':
        connections.execute_shell_command_without_check('cd "%s"/cn/emutop/system/mme' % version_path)
        old_prompt = connections.set_host_prompt('state(\s+):(\s*)initialized')
        processcheck = connections.execute_shell_command_without_check('./mme')
        time.sleep(3)
        for error in chlist:
            if processcheck.find(error)>0:
                raise Exception ,'Error %s happend !' %error        
        #connections.set_host_prompt('^:\s$')
        #connections.execute_shell_command_without_check('\r')
        connections.set_host_prompt(old_prompt)

    elif process =='UPE' or process =='upe':
        connections.execute_shell_command_without_check('cd "%s"/cn/emutop/system/upe' % version_path)
        old_prompt = connections.set_host_prompt('Generate(\s+)gtp')  
        processcheck = connections.execute_shell_command_without_check('./upe')
        time.sleep(3)
        for error in chlist:
            if processcheck.find(error)>0:
                raise Exception ,'Error %s happend !' %error
        #connections.set_host_prompt('^:\s$')
        #connections.execute_shell_command_without_check('\r')
        connections.set_host_prompt(old_prompt)
        
    elif process =='INET' or process =='inet':
        connections.execute_shell_command_without_check('cd "%s"/cn/emutop/system/inet' % version_path)
        old_prompt = connections.set_host_prompt('.*parameters.ini')
        processcheck = connections.execute_shell_command_without_check('./inet')
        time.sleep(3)
        for error in chlist:
            if processcheck.find(error)>0:
                raise Exception ,'Error %s happend !' %error
        connections.set_host_prompt(old_prompt)
    else:
        raise Exception ,"The process you input is wrong !"

def Check_emulator_process(processlist =['HSS','MME','UPE','INET']):
    """This keyword can check the emulator'four processes , it can be used after restart of emulator
    | Input Parameters | Man. | Description |
 
    Example
    | Check_emulator_process |  
    """
    processcheck = connections.execute_shell_command_without_check('ps -fe')
    processlist = ['HSS','MME','UPE','INET']
    for proce in processlist:
        proceprompt = './%s' % proce
        if processcheck.find(proceprompt)<0:
            raise Exception , 'Process %s not started !' %proce        
    else:
        pass

def __Execute_macro_command(macro_cmd):
    """This keyword can execute macro command in emulator's process
    | Input Parameters | Man. | Description |
 
    Example
    | Execute_macro_command | attach_db |
    """
    old_prompt = connections.set_host_prompt(':(\s+)')
    connections.execute_shell_command_without_check('\r')
    print 'bb','\r','aaa'
    connections.set_host_prompt('^Waiting.*(\.+)')
    ret_macro = connections.execute_shell_command_without_check(macro_cmd)
    #connections.set_host_prompt('state(\s+):(\s*)initialized')
    #ret = connections.execute_shell_command_without_check('run')
    connections.set_host_prompt(old_prompt)
    return ret_macro


        
   # for proce in chlist:
    #    if processcheck.find(proce)<0:
     #       raise Exception, "Process %s not start" % proce


    
    
