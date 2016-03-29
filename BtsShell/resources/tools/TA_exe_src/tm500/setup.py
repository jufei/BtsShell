from distutils.core import setup
import py2exe
import sys, os

includes = ["encodings", "encodings.*"]

Pwd = os.getcwd()

MainPyFile = os.path.join(Pwd, 'tm500_serial_operation.py')

Myoptions = {"py2exe":
    {"compressed": 1,
     "optimize": 2,
     "ascii": 1,
     "includes":includes,
     "bundle_files": 1}
    }

setup(  
    version = "0.1", 
    description = "This tool is used for check tm500_status", 
    name = "tm500_status_check.exe",   
    options = Myoptions,     
    zipfile = None,
    console=[{"script": MainPyFile}],)

print "Generate exe OK!"
sys.exit(0)
