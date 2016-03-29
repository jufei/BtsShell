import time, os, sys
from BtsShell.high_shell_lib.run import _run_keyword as kw
from robot.libraries.BuiltIn import BuiltIn

from .common_operation import start_robot_remote_library
from BtsShell.application_lib.process import kill_process_by_sockets

from BtsShell.common_lib.get_path import get_tools_path_with_command
def _GetRuntimeVar(varname):
    try:
        if not varname.startswith("${"):
            varname = "${%s}" % varname
        return BuiltIn().replace_variables(varname)
    except:
        print "Can't get variable '%s' value" % varname
        return

class Two_log_check:
    def __init__(self, local_pc_conn, target_pc_conn, case_folder, 
                 local_btslog_dir, target_btslog_dir,
                 local_infomodel, target_infomodel):
        self.local_pc_conn = local_pc_conn
        self.target_pc_conn = target_pc_conn
        self.local_btslog_dir = local_btslog_dir#"D:\\temp\\BTSLogs\\"
        self.target_btslog_dir = target_btslog_dir
        self.case_folder = case_folder
        self.onair_check = ["now OnAir","PBCH"]
        
        self.local_infomodel = local_infomodel
        self.target_infomodel = target_infomodel
        self.local_infomodel_object = None
        self.target_infomodel_object = None
        self.onair_check_node = "/MRBTS-1/RAT-1/BBTOP_L-1/LCELL-*"
        self.onair_check_point = "onAirDone"
        
        self.local_need_check = True
        self.target_need_check = True
            
    def log2console(self, msg):
        sys.__stderr__.write(">>" + msg + os.linesep)
        
    def start_infomodel(self, im_obj, im_params):
        kill_process_by_sockets(im_params[1], im_params[2])
        if not hasattr(im_obj, "target_host"):
            #im_obj.setup_infomodel(address=im_params[1], port=im_params[2], update_interval=0, \
            #                        auto_reconnect=True, definitions_file_path=im_params[0])
            im_obj.setup_infomodel(address=im_params[1], port=im_params[2], update_interval=0, \
                                    auto_reconnect=True)
            im_obj.connect_infomodel()
            im_obj.start_infomodel_logger()
            self.log2console("local infomodel is started with " + im_params[1])
            return 
        else:
            #im_obj.setup_infomodel((im_params[1], im_params[2], 0, True, im_params[0]), {})
            im_obj.setup_infomodel((im_params[1], im_params[2], 0, True), {})
            #im_obj.setup_infomodel((im_params[0], im_params[1], im_params[2]), {})
            im_obj.connect_infomodel((), {})
            im_obj.start_infomodel_logger((), {})
            self.log2console("target infomodel is started with " + im_params[1])            
        
    def stop_infomodel_and_check_log(self, im_obj, flag):
        direction, logtag = flag.split("_", 1)
        if not im_obj:
            return True
        else:
            if hasattr(im_obj, "target_host"):
                try:
                    print "Save %s infomodel log" % direction
                    im_obj.save_infomodel_log(("C:/infomodel_log_%s" % direction, ), {})
                    im_obj.stop_infomodel_logger((), {})
                    print "Stop %s infomodel" % direction
                    im_obj.teardown_infomodel((),{})
                except Exception, e:
                    print e
            else:
                try:
                    print "Save %s infomodel log" % direction
                    im_obj.save_infomodel_log("C:/infomodel_log_%s" % direction)
                    im_obj.stop_infomodel_logger()
                    print "Stop %s infomodel" % direction
                    im_obj.teardown_infomodel()
                except Exception, e:
                    print e                
        
        func = self.local_log_copy_and_check if direction == "local" else self.target_log_copy_and_check
    
        print "copy %s log" % direction
        return func("im_final_%s" % logtag)

    def check_if_bts_is_onair_with_infomodel(self, im_obj, direction):
        if hasattr(im_obj, "target_host"):
            try:
                im_obj.query_infomodel(("count %s is >= 1" % self.onair_check_node, ), {})
                im_obj.query_infomodel(("every %s is [stateInfo.proceduralState=%s]" % (self.onair_check_node, self.onair_check_point),), {})
                print '>>>  %s Bts status is OnAir now!' % (direction)
                self.log2console('%s Bts status is OnAir now!' % (direction))                
                return True
            except Exception, e:
                print "%s BTS is still not OnAir, Err: " % direction, e
                return False
        else:
            try:
                im_obj.query_infomodel("count %s is >= 1" % self.onair_check_node)
                # every /MRBTS-1/RAT-1/BBTOP_L-1/LCELL-* is [stateInfo.proceduralState=onAirDone]
                im_obj.query_infomodel("every %s is [stateInfo.proceduralState=%s]" % (self.onair_check_node, self.onair_check_point))
                print '>>>  %s Bts status is OnAir now!' % (direction)
                self.log2console('%s Bts status is OnAir now!' % (direction))
                return True
            except Exception, e:
                print "%s BTS is still not OnAir, Err: " % direction, e
                return False
#         obj = None
#         if hasattr(im_obj, "target_host"):
#             try:
#                 obj = im_obj.get_infomodel_object((self.infomodel_check_node, ), {})
#             except Exception, e:
#                 print e
#                 print "can't get target infomodel obj %s" % self.infomodel_check_node
#                 self.log2console("can't get target infomodel obj %s" % self.infomodel_check_node)
#                 return False
#         else:
#             try:
#                 obj = im_obj.get_infomodel_object(self.infomodel_check_node)
#             except Exception, e:
#                 print e
#                 print "can't get local infomodel obj %s" % self.infomodel_check_node
#                 self.log2console("can't get local infomodel obj %s" % self.infomodel_check_node)
#                 return False             
# # 
#         if not obj:return False
#         print "*INFO* %s Current status" %(direction), obj
# 
#         if obj["StateInfo"]["ProceduralState"] != self.onair_check_infomodel:
#             print '>>>  %s Bts status is up to "%s" now!' % (direction, obj["StateInfo"]["ProceduralState"])
#             self.log2console('%s Bts status is up to "%s" now!' %(direction, obj["StateInfo"]["ProceduralState"])
#             return False
#         else:
#             print '>>>  %s Bts status is OnAir now!' % (direction)
#             self.log2console('%s Bts status is OnAir now!' % (direction))
#             return True

        
    def local_log_copy_and_check(self, flag):
        #local bts log copy
        kw("switch_host_connection", self.local_pc_conn)
        local_src_bts_log = kw("get_last_modified_file", self.local_btslog_dir, "LOG")
        local_save_bts_log = os.path.join(self.case_folder,"local_check_onair_%s.LOG"%flag)
        kw("file_copy", local_src_bts_log, local_save_bts_log)
        #local bts log check
        if self.local_infomodel_object:
            checkpoint = "PBCH"
            try:
                kw("file_copy", "C:/infomodel_log_local.ims2", os.path.join(self.case_folder, "infomodel_log_local.ims2"))
                kw("execute_shell_command_without_check", "rm -rf C:/infomodel_log_local.ims2")
            except Exception, e:
                print "*WARN* Copy local infomodel log failed! Err: ", e
        else:
            checkpoint = _GetRuntimeVar("ONAIR_CHECK")
        try:
            kw("file_should_contain", local_save_bts_log, checkpoint)
        except Exception, e:
            print e
            return False

        return True

    def target_log_copy_and_check(self, flag):
        #target bts log copy
        kw("switch_host_connection", self.target_pc_conn)
        target_src_bts_log = kw("get_last_modified_file", self.target_btslog_dir, "LOG")
        target_save_bts_log = os.path.join(self.case_folder,"target_check_onair_%s.LOG"%flag)
        kw("switch_host_connection", self.local_pc_conn)
        kw("copyfile2local", self.target_pc_conn.host, self.target_pc_conn.user, \
                  self.target_pc_conn.password, target_src_bts_log, target_save_bts_log)
        #target bts log check
        if self.local_infomodel_object:
            checkpoint = "PBCH"
            try:
                kw("copyfile2local", self.target_pc_conn.host, self.target_pc_conn.user, \
                  self.target_pc_conn.password, "C:/infomodel_log_target.ims2", os.path.join(self.case_folder, "infomodel_log_target.ims2"))
                kw("switch_host_connection", self.target_pc_conn)
                kw("execute_shell_command_without_check", "rm -rf C:/infomodel_log_target.ims2")
                kw("switch_host_connection", self.local_pc_conn)
            except Exception, e:
                print "*WARN* Copy target infomodel log failed! Err: ", e
        else:
            checkpoint = _GetRuntimeVar("TARGET_ONAIR_CHECK")      
        try:
            kw("file_should_contain", target_save_bts_log, checkpoint)
        except Exception, e:
            print e
            return False
        return True

    def wait_onair(self, local_flag, target_flag, log_tag, total_duration, sleep_time):
        from BtsShell.network_lib import wait_until_units_startup
        duration = 0
        start_time = time.clock()
        from BtsShell.network_lib import wait_until_units_startup
        if local_flag:self.local_need_check = False
        if target_flag:self.target_need_check = False
            
        if self.local_infomodel and not local_flag:
            kw("switch_host_connection", self.local_pc_conn)
            self.log2console("wait local FCM start up ...")
            wait_until_units_startup(150, self.local_infomodel[1])
            tools_path = get_tools_path_with_command()
            enable_rd_port_cmd = "%s/wget.exe --user=Nemuadmin --password=nemuuser \
--no-check-certificate https://192.168.255.129/protected/enableRndPorts.cgi \
-t 1 --timeout=10 -q -O -" % tools_path
            #kw("execute_shell_command_without_check", enable_rd_port_cmd)
            
            print ">>> Begin to start local infomodel with ", self.local_pc_conn.host
            from bts_infomodel import bts_infomodel
            self.local_infomodel_object = None
            self.local_infomodel_object = bts_infomodel()
            self.start_infomodel(self.local_infomodel_object, self.local_infomodel)
            print ">>> Local Infomodel is started with ", self.local_pc_conn.host
    
        if self.target_infomodel and not target_flag:
            kw("switch_host_connection", self.target_pc_conn)
            self.log2console("wait target FCM start up ...")
            wait_until_units_startup(40, self.target_infomodel[1])
            tools_path = get_tools_path_with_command()
            enable_rd_port_cmd = "%s/wget.exe --user=Nemuadmin --password=nemuuser \
--no-check-certificate https://192.168.255.129/protected/enableRndPorts.cgi \
-t 1 --timeout=10 -q -O -" % tools_path                        
            #kw("execute_shell_command_without_check", enable_rd_port_cmd)
            
            print ">>> Begin to start target infomodel with ", self.target_pc_conn.host
            self.target_infomodel_object = None
            rpid = start_robot_remote_library("bts_infomodel", self.target_pc_conn.host, "8271", "True")  
            from robot.libraries.Remote import Remote
            self.target_infomodel_object = Remote("%s:8271" % (self.target_pc_conn.host))  
                      
            from functools import partial
            for kw_name in self.target_infomodel_object.get_keyword_names():
                setattr(self.target_infomodel_object, kw_name, partial(self.target_infomodel_object.run_keyword, kw_name))
            setattr(self.target_infomodel_object, "target_host", self.target_pc_conn.host)    
          
            self.start_infomodel(self.target_infomodel_object, self.target_infomodel)
            
            print ">>> Target Infomodel is started with ", self.target_pc_conn.host
        time.sleep(60)
        while (not local_flag or not target_flag) \
                  and (duration < total_duration):
            print ">>> checking onair ..."
            if not local_flag:
                print ">>> checking local bts..."
                if self.local_infomodel:
                    local_flag = self.check_if_bts_is_onair_with_infomodel(self.local_infomodel_object, "local")
                else:
                    local_flag = self.local_log_copy_and_check(log_tag)
            if not target_flag:
                print ">>> checking target bts..."
                if self.target_infomodel:
                    target_flag = self.check_if_bts_is_onair_with_infomodel(self.target_infomodel_object, "target")
                else:
                    target_flag = self.target_log_copy_and_check(log_tag)
            time.sleep(sleep_time)
            duration = time.clock() - start_time
        
        local_pbchflag = self.stop_infomodel_and_check_log(self.local_infomodel_object, "local_%s" % log_tag)
        target_pbchflag = self.stop_infomodel_and_check_log(self.target_infomodel_object, "target_%s" % log_tag)
        
        if local_flag and self.local_need_check and local_pbchflag:
            print "*INFO* Local bts is OnAir !"
            self.log2console("Local bts is OnAir !")
        
        if target_flag and self.target_need_check and target_pbchflag:
            print "*INFO* Target bts is OnAir now !"
            self.log2console("Target bts is OnAir !")
            
        return local_flag, target_flag

def _bts_restart(port):
    kw("Power Off", port)
    time.sleep(5)
    kw("Power On", port)



def check_two_bts_onair( local_check_flag = False, target_check_flag = False, \
                         max_wait_time='900', get_log_interval='180'):
    local_pc_conn = _GetRuntimeVar("BTS_CONTROL_PC_CONNECTION")
    target_pc_conn = _GetRuntimeVar("TARGET_BTS_CONTROL_PC_CONNECTION")
    case_folder = _GetRuntimeVar("TARGET_LOG_DIRECTORY")
    local_pb_port = _GetRuntimeVar("BTS_POWERBREAK_PORT")
    target_pb_port = _GetRuntimeVar("TARGET_BTS_POWERBREAK_PORT")
    local_btslog_exe_dir = _GetRuntimeVar("BTSLOG_EXE_DIR")
    target_btslog_exe_dir = _GetRuntimeVar("TARGET_BTSLOG_EXE_DIR")
    local_btslog_dir = _GetRuntimeVar("BTSLOG_DIR")
    target_btslog_dir = _GetRuntimeVar("TARGET_BTSLOG_DIR")
    INFOMODEL = None
    ONAIR_CHECK_TOOL = _GetRuntimeVar("ONAIR_CHECK_TOOL")
    if ONAIR_CHECK_TOOL.strip().upper() == "INFOMODEL":
        IM_JAR_PATH = _GetRuntimeVar("IM_JAR_PATH")
        BTS_INFOMODEL_IP = _GetRuntimeVar("BTS_INFOMODEL_IP")
        BTS_INFOMODEL_PORT = _GetRuntimeVar("BTS_INFOMODEL_PORT")
        INFOMODEL = [IM_JAR_PATH, BTS_INFOMODEL_IP, BTS_INFOMODEL_PORT]
    
    TARGET_INFOMODEL = None        
    TARGET_ONAIR_CHECK_TOOL = _GetRuntimeVar("TARGET_ONAIR_CHECK_TOOL")
    if TARGET_ONAIR_CHECK_TOOL.strip().upper() == "INFOMODEL":
        TARGET_IM_JAR_PATH = _GetRuntimeVar("TARGET_IM_JAR_PATH")
        TARGET_BTS_INFOMODEL_IP = _GetRuntimeVar("TARGET_BTS_INFOMODEL_IP")
        TARGET_BTS_INFOMODEL_PORT = _GetRuntimeVar("TARGET_BTS_INFOMODEL_PORT")
        TARGET_INFOMODEL = [TARGET_IM_JAR_PATH, TARGET_BTS_INFOMODEL_IP, TARGET_BTS_INFOMODEL_PORT]
        
    max_wait_time = float(max_wait_time)
    get_log_interval = float(get_log_interval)

    two_log = Two_log_check(local_pc_conn, target_pc_conn, case_folder, 
                            local_btslog_dir, target_btslog_dir,
                            INFOMODEL, TARGET_INFOMODEL)
    local_check_flag, target_check_flag = two_log.wait_onair(local_check_flag, \
                        target_check_flag, 1, max_wait_time, get_log_interval)

    if (not local_check_flag):        
        kw("switch_host_connection", local_pc_conn)
        _bts_restart(local_pb_port)
        kw("start_btslog", local_btslog_exe_dir, "UDP")
 
    if (not target_check_flag):        
        kw("switch_host_connection", target_pc_conn)
        _bts_restart(target_pb_port)
        kw("start_btslog", target_btslog_exe_dir, "UDP")
 
    local_check_flag, target_check_flag = two_log.wait_onair(local_check_flag, \
                        target_check_flag, 2,  max_wait_time, get_log_interval)

    if  (not local_check_flag) or (not target_check_flag):
        fail_info = ""
        if (not local_check_flag):
            fail_info += "Local bts onair failed!\n"
        if (not target_check_flag):
            fail_info += "Target bts onair failed!\n"
        raise Exception, fail_info

def _calibration_two_bts(local_pc_conn, target_pc_conn):
    time.sleep(180)
    kw("switch_host_connection", local_pc_conn)
    kw("start_btslog", BTSLOG_EXE_DIR, "UDP")
    kw("switch_host_connection", target_pc_conn)
    kw("start_btslog", BTSLOG_EXE_DIR, "UDP")

    time.sleep(60)

    kw("switch_host_connection", local_pc_conn)
    local_src_bts_log = kw("get_last_modified_file", btslog_dir, "LOG")
    kw("file_copy", local_src_bts_log, local_save_bts_log)
    kw("stop_btslog")

    kw("switch_host_connection", target_pc_conn)
    target_src_bts_log = kw("get_last_modified_file", btslog_dir, "LOG")
    kw("stop_btslog")
    kw("switch_host_connection", local_pc_conn)
    kw("copyfile2local", target_pc_conn.host, target_pc_conn.user, \
              target_pc_conn.password, target_src_bts_log, target_save_bts_log)


if __name__ == '__main__':
    check_two_bts_onair()
    pass
