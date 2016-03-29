#!/usr/bin/env python
# -*- coding: cp936 -*-
##The Script should Run in Robot 2.8.3
"""
This file use to change $ to @ in variable table when its type is list
Usage Example:
Want to modify suite files in D:\work\TestCase\RL45\SON, execute this script in command line
python modify_suite_element.py D:\work\TestCase\RL45\SON
Add By GuanXiaobing 2014-01-27
"""

import os
import sys
import re
import time
from robot.api import TestData

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
LOG_DIRECTORY = os.path.join(BASE_DIRECTORY, 'logs')
LOG_FILE = os.path.join(LOG_DIRECTORY,
                        'testsuite_modify_%s.log' % time.strftime('%Y%m%d%H%M'))
SKIP_PATH = ['.svn','Variables']

#===============================================================================
#Function to generate a execution log file 
#===============================================================================
def _log(msg,file_name = LOG_FILE):
    try:
        file_handle = open(file_name, 'a')
    except:
        try:
            os.mkdir(LOG_DIRECTORY)
            file_handle = open(file_name, 'a')
        except:
            raise Exception, 'open log file %s failed' % file_name

    try:
        file_handle.write('%s %s\n' % (time.ctime(), msg))
    finally:
        file_handle.close()


#===============================================================================
# The Funtion to traverse all suite files
#===============================================================================

class traverse_testsuite_files():
    def __init__(self,case_root_path):
        self.root_path = case_root_path
            
    def deep_search(self,case_root_path,file_filter = "html", if_deep_walk = True):
        """
        search test suite files, and default file filter is html
        """
        try:
            content_list = os.listdir(case_root_path)
            for item in content_list:
                try:
                    file_path = os.path.join(case_root_path,item)
                    if os.path.isdir(file_path):
                        if item in SKIP_PATH:
                            continue
                        else:
                            self.deep_search(file_path)
                    else:
                        if item.endswith('.html'):
                            self.modify_variable_symbol(file_path)
                except:
                    _log("ERROR: Get Path failed:%s" %item)                    
                    continue
                                            
        except Exception,e:
            _log("ERROR: deep_search failed:%s" %e)
    
    def modify_variable_symbol(self,file_):
        """
        analysis rebot html file, if varialbe type is List and symbol is $, change it to @
        """
        #recurrence function for forloop in steps
        def _check_variable_changed(step):
            if step.is_for_loop():
                for i_num in xrange(0,len(step.items)):
                    if step.items[i_num] in need_modify_var_dist.keys():
                        step.items[i_num] = need_modify_var_dist[step.items[i_num]]
                for sub_step in step.steps:
                    _check_variable_changed(sub_step)
            else:
                for arg_num in xrange(0,len(step.args)):
                    if step.args[arg_num] in need_modify_var_dist.keys():
                        step.args[arg_num] = need_modify_var_dist[step.args[arg_num]]
                        
        try:
            try:
                print " %s" %file_
                suite = TestData(source = "%s" %(file_))
            except Exception,e:
                err_str = 'ERROR: TestData analyze file [%s] Failed' % file_
                reason_str = 'Reason: %s' %e
                _log(err_str)
                _log(reason_str)
                print err_str
                print reason_str
                return False
                
            #Get need to modified list
            need_modify_var_dist = {}
            for var in suite.variable_table.variables:
                if len(var.value) > 1 and var.name.startswith("$"):
                    new_name = var.name.replace('${','@{')
                    #Add this variable to modified dict
                    need_modify_var_dist[var.name] = new_name
                    #Modify $ to @
                    var.name = new_name
            #Check and Modify changed Variable in Keyword table
##            for keyword in suite.keywords:
##                for step_ in keyword.steps:
##                    _check_variable_changed(step_)
##            #Check and Modify changed Variable in TestCase table
##            for case in suite.testcase_table.tests:
##                for step in case.steps:
##                    _check_variable_changed
                    
            suite.save()
            if len(need_modify_var_dist):
                _log('INFO: Modify file [%s] Variable successful' % file_)
                _log('INFO: Changed Variable list is %s' %need_modify_var_dist)
            
        except Exception,e:
            _log('ERROR: Modify file [%s] Variable Failed' % file_)
            _log('ERROR: reason  is %s' % e)

        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        _log('ERROR: usage is wrong, exit') 
        exit(1)
    case_root_path = sys.argv[1]
    print "**************************************************"
    print "Note: This script can't change resource files!"
    print "**************************************************"
    try:
        obj = traverse_testsuite_files(case_root_path)
        obj.deep_search(obj.root_path)
    except Exception,e:
        _log('ERROR: Modify file Variable Failed')
        _log('ERROR: reason  is %s' % e)  
