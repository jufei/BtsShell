import os
import inspect
from BtsShell import connections

def get_btsshell_path():
    this_file = inspect.getfile(inspect.currentframe())
    path = os.path.dirname(os.path.dirname(this_file))
    return path

def get_btsshell_path_with_command():
    seper = "*SEP*"
    cmd = '''python -c "import BtsShell, os;print '%s',os.path.dirname(BtsShell.__file__)"''' % seper
    ret = connections.execute_shell_command_without_check(cmd)
    if seper not in ret:
        raise Exception, "Can't get BtsShell path with python command"
    else:
        for ln in ret.splitlines()[::-1]:
            if seper in ln:
                return ln.split(seper, 3)[-1].strip()

def get_tools_path_with_command():
    path = get_btsshell_path_with_command()
    tools_path = os.path.join(path, "resources", "tools")
    return tools_path

def get_tools_path():
    return r'C:\Python27\lib\site-packages\BtsShell\resources\tools'
    path = get_btsshell_path()
    tools_path = os.path.join(path, "resources", "tools")
    return tools_path

if __name__ == "__main__":
    connections.connect_to_host("10.69.71.115", 23, "tdlte-tester", "btstest")
    print "<<"
    path = get_tools_path_with_command()
    print ">>", "%s" %path
    print "<<"
    connections.disconnect_all_hosts()