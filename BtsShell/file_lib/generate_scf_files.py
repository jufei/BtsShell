import os
import time
from optparse import OptionParser
from ConfigParser import *
from BtsShell.file_lib.xml_control import change_xml_file

class CaseSConfigParser(RawConfigParser):
    def __init__(self):
        RawConfigParser.__init__(self)

    def optionxform(self, optionstr):
        return optionstr

    def _read(self, fp, fpname):
        """Parse a sectioned setup file.

        The sections in setup file contains a title line at the top,
        indicated by a name in square brackets (`[]'), plus key/value
        options lines, indicated by `name: value' format lines.
        Continuations are represented by an embedded newline then
        leading whitespace.  Blank lines, lines beginning with a '#',
        and just about everything else are ignored.
        """
        cursect = None                            # None, or a dictionary
        optname = None
        lineno = 0
        e = None                                  # None, or an exception
        while True:
            line = fp.readline()
            if not line:
                break
            lineno = lineno + 1
            # comment or blank line?
            if line.strip() == '' or line[0] in '#;':
                continue
            if line.split(None, 1)[0].lower() == 'rem' and line[0] in "rR":
                # no leading whitespace
                continue
            # continuation line?
            if line[0].isspace() and cursect is not None and optname:
                value = line.strip()
                if value:
                    cursect[optname] = "%s\n%s" % (cursect[optname], value)
            # a section header or option header?
            else:
                # is it a section header?
                mo = self.SECTCRE.match(line)
                if mo:
                    sectname = mo.group('header')
                    if sectname in self._sections:
                        cursect = self._sections[sectname]
                    elif sectname == DEFAULTSECT:
                        cursect = self._defaults
                    else:
                        cursect = {'__name__': sectname}
                        self._sections[sectname] = cursect
                    # So sections can't start with a continuation line
                    optname = None
                # no section header in the file?
                elif cursect is None:
                    raise MissingSectionHeaderError(fpname, lineno, line)
                # an option line?
                else:
                    mo = self.OPTCRE.match(line)
                    if mo:
                        optname, vi, optval = mo.group('option', 'vi', 'value')
                        if vi in ('=', ':') and ';' in optval:
                            # ';' is a comment delimiter only if it follows
                            # a spacing character
                            pos = optval.find(';')
                            if pos != -1 and optval[pos-1].isspace():
                                optval = optval[:pos]
                        optval = optval.strip()
                        # allow empty values
                        if optval == '""':
                            optval = ''

                        if cursect['__name__'] != 'Global':
                            optname = line.strip()
                            cursect[optname] = line.strip()
                        else:
                            optname = self.optionxform(optname.rstrip())
                            cursect[optname] = optval
                    else:
                        # a non-fatal parsing error occurred.  set up the
                        # exception but keep going. the exception will be
                        # raised at the end of the file and will contain a
                        # list of all bogus lines
                        if not e:
                            e = ParsingError(fpname)
                        e.append(lineno, repr(line))
        # if any parsing errors occurred, raise an exception
        if e:
            raise e
def generate_scf_files(file_path):
    """ This keyword generate kinds of SCF folder and files in specifical directory.
    Under the -f folder, there should be a "golden" folder, "SCFC_1.xml" and "config.ini" file in it.
    Kinds of SCF folder and file also will be create in this folder.

    Use in DOS command line:
        <python generate_scf_files.py -f C:\Python25\Lib\site-packages\BtsShell\resources\scripts\Ford>
    Use in robot case:
    | Input Parameters  | Man. | Description |
    | file_path          | Yes  | The target folder to create kinds of configuration files|

    Example
    | generate_scf_files| d:\\Python25\\Lib\\site-packages\\BtsShell\\resources\\scripts\\Ford |

    """
    config = CaseSConfigParser()
    ini_path = os.path.join(file_path, "golden", "config.ini")
    print ini_path
    cfgfile = open(ini_path, 'rw')
    config.readfp(cfgfile)
    scf_name = config.get("Global", "scf_name")
    src_scf_path = os.path.join(file_path, "golden", scf_name)
    """
    1. get dirctorys name from Global such as ['20M_TM1_15', '20M_TM2_25']
    2. get kinds of configuration modify list
    {'TM1': ['dlInterferenceSpatialMode:SingleTX', 'syncSigTxMode:SingleTx',
            'dlMimoMode:SingleTX', 'numOfTxPorts:1'],
     'TM2': ['dlInterferenceSpatialMode:TXDiv', 'syncSigTxMode:TxDiv',
            'dlMimoMode:TXDiv', 'numOfTxPorts:2'],
     '27': ['tddSpecSubfConf:7', 'tddFrameConf:2'],
     '15': ['tddSpecSubfConf:5', 'tddFrameConf:1'],
     '25': ['tddSpecSubfConf:5', 'tddFrameConf:2'],
     '17': ['tddSpecSubfConf:7', 'tddFrameConf:1'],
     '10M': ['chBw:10 MHz', 'iniPrbsUl:50'],
     '20M': ['chBw:20 MHz', 'iniPrbsUl:100']}
    """
    dirs = []
    key_value_dict = {}
    sections = config.sections()
    for section in sections:
        options = config.options(section)
        tmp = []
        for option in options:
            print section, option
            value = config.get(section, option)
            if "Global"==section and "true"==value:
                dirs.append(option)
            if "Global"!=section:
                tmp.append(value)

        print tmp
        if "Global"!=section:
            key_value_dict[section]=tmp
    """
    Get configuration list from directory name,
    such as:
        {'20M_TM1_15': ['chBw:20 MHz', 'iniPrbsUl:100',
                        'dlInterferenceSpatialMode:SingleTX',
                        'syncSigTxMode:SingleTx', 'dlMimoMode:SingleTX',
                        'numOfTxPorts:1', 'tddSpecSubfConf:5', 'tddFrameConf:1'],
        '20M_TM2_25': [ 'chBw:20 MHz', 'iniPrbsUl:100',
                        'dlInterferenceSpatialMode:TXDiv', \
                        'syncSigTxMode:TxDiv', 'dlMimoMode:TXDiv',
                        'numOfTxPorts:2', 'tddSpecSubfConf:5', 'tddFrameConf:2']}
    """
    dir_dict = {}
    for dir in dirs:
        keys = dir.split("_")
        tmp = []
        for key in keys:
            tmp += key_value_dict[key.upper()]
        dir_dict[dir] = tmp
    for dir in dirs:
        tar_dir = os.path.join(file_path, dir)
        if os.path.exists(tar_dir):
            print "Dir '%s' is exist."%tar_dir
        else:
            os.makedirs(tar_dir)
            print "Create dir '%s' ok."%tar_dir
        modify_list = dir_dict[dir]
        change_xml_file(src_scf_path, os.path.join(tar_dir, scf_name), modify_list)

if __name__ == '__main__':
    """ This script create kinds of configuraion folder and files in specifical directory.
        Under the -f folder, there should be a "Golden" folder, "SCFC_1.xml" and "config.ini" file in it.

        Kinds of configuration folder and file also will be create in this folder.
        Usage:
            dos command line: python create_config_file -f "C:\Python25\Lib\site-packages\BtsShell\resources\scripts\Ford"
    """
    description = "scf configuration create for TDLTE I&V testing.       \
                   Author: Chen Jin(61368521)                  \
                   Email: jin_emily.chen@nsn.com                         \
                   Data: 2012-8-7                                                                         \
                   Version: 1.0.0"
    parser = OptionParser(description = description)
    parser.add_option("-f", "--filepath",
                              action = "store",
                              dest = "filepath",
                              type = "string",
                              default = "",
                              help = "upload or download file by ftp.")

    (options, args) = parser.parse_args()
    filepath = options.filepath

    generate_scf_files(filepath)

