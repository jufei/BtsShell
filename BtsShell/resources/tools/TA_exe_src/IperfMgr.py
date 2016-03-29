import subprocess, sys, shutil, traceback, os

__author__ = "ZhangYongchao"


def start_iperf(args, filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except Exception, e:
            print "*WARN* Exception: %s" %e
            os.system("rm -f %s" %filename)
    try:
        p = subprocess.Popen(args, stdout=open(filename, 'a'))
        p.wait()
    except:
        print traceback.print_exc()
    finally:
        pass

def getfilename():
    for arg in sys.argv[1:]:
        if arg == '-o':
            return sys.argv[1:][sys.argv[1:].index(arg)+1]

def parse_args(args):
    item = ''
    for arg in args[:-2]:
        item = item + ' ' + arg
    return item.strip()

if __name__ == "__main__":
    filename = getfilename()
    args = parse_args(sys.argv[1:])
    print "*INFO* Cmd: \"%s\"" %args
    if filename:
        print "*INFO* Will record log to \"%s\"" % filename
        start_iperf(args, filename)
    else:
        raise Exception, "*ERROR* Your input filename is none!"
