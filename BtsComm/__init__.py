"""
When reporting bugs or requesting new features, please use the IpaMml Issue Track System:
https://jira.inside.nokiasiemensnetworks.com/browse/IPATA
"""
#try by sjy    
try:
    mod = __import__("version", globals())
    __version__ = mod.version
except:
    __version__ = "0.0.0"

from telnet_connection import TelnetConnection
from ssh_connection import SshConnection
#from email_listener import EmailListener

def get_co_name(kw):
    if kw.func_code.co_name != '<lambda>':
        return kw.func_code.co_name
    else:
        return kw._co_name
    
def get_co_filename(kw):
    if kw.func_code.co_filename != '<string>':
        return kw.func_code.co_filename
    else:
        return kw._co_filename
    
