import os
import sys
import array
import ftplib
from BtsShell import connections
from BtsShell.common_lib.get_path import *
MemDumperTool = os.path.join(get_tools_path(), "MemDumper", 'MemDumper.exe')

#memory_len: num of bytes in decimal.
def _memory_dump_convertor(chip_id, memory_addr, memory_len):

    source_name = chip_id + "_" + memory_addr + ".hex"
    dest_name = chip_id + "_" + memory_addr + ".dat"

    f_source = open(source_name, 'rb')
    f_dest = open(dest_name, 'wb')

    aa = array.array('L')
    aa.fromfile(f_source,int(memory_len)/4)
    #aa.byteswap()

    f_dest.write("1651 1 ")
    f_dest.write(memory_addr[2:])
    f_dest.write(" 0 ")
    f_dest.write(hex(int(memory_len)/4)[2:])
    f_dest.write('\r\n')
    pading_0 = "00000000"
    for i in aa:
        s_line = hex(i).rstrip("L")
        len_0 = 10 - len(s_line)
        f_dest.write(s_line[0:2])
        if len_0 != 0:
            f_dest.write(pading_0[0:len_0])
        f_dest.write(s_line[2:10].swapcase())
        f_dest.write('\r\n')

    f_source.close()
    f_dest.close()
    os.remove(source_name)

def _get_dump_hex_file(chip_id, memory_addr, memory_len):

    dump_command = "rioboot -c read -a " + memory_addr + " -n " + memory_len + " 0x" + chip_id + " > " + chip_id + "_" + memory_addr + ".hex"

    try:
        ftp = ftplib.FTP("192.168.255.1")
        ftp.login("toor4nsn", "oZPS0POrRieRtu")
    except Exception:
        print "FTP Connect to 192.168.255.1 failed"
        sys.exit(-1)

    btsConn = connections.connect_to_ssh_host('192.168.255.1', '22', 'toor4nsn', 'oZPS0POrRieRtu', '>')
    connections.switch_ssh_connection(btsConn)

    print("-----------------------------------------------------------------")
    print("Dump " + memory_len + " bytes from addr " + memory_addr + " chip 0x" + chip_id)

    connections.execute_ssh_command_without_check(dump_command)
    connections.execute_ssh_command_without_check("sync")
    ftp.voidcmd('TYPE I')
    path = chip_id + "_" + memory_addr + ".hex"
    filename = 'RETR ' + path
    local_file = open(path, 'wb')
    ftp.retrbinary(filename, local_file.write)
    local_file.close()

    connections.execute_ssh_command_without_check("rm -rf " + chip_id + "_" + memory_addr + ".hex")

def mem_dumper(dump_entry, target_dir):
    """This keyword start memory dump
    | Input Parameters  | Man. |  Description |
    | dump_entry        | Yes  |  FSP id      |
    | target_dir        | Yes  |  Directory where memdump log download to  |

    Example
    | mem dumper | ['1231:0x872479f0:400', '1231:0x9c80a480:400'] | ${TARGET LOG DIRECTORY} |
    """

    os.chdir(target_dir)

    for element in dump_entry:
        if (element[0:1] != "#" and len(element) > 14):
            CHIP_ID = element[0:4]
            MEM_ADDR = element[5:15]
            NUM_BYTES = element[16:].rstrip()
            _get_dump_hex_file(CHIP_ID, MEM_ADDR, NUM_BYTES)
            _memory_dump_convertor(CHIP_ID, MEM_ADDR, NUM_BYTES)

def mem_dumper_execute(FSP_number, Faraday_number):
    """This keyword start memory dump for specified FSP and Faraday
    | Input Parameters  | Man. |  Description |
    | FSP_number        | Yes  |  FSP id      |
    | Faraday_number    | Yes  |  Faraday id  |

    Example
    | mem dumper execute | 0x12 | 61 |
    """

    old_time = connections.set_shell_timeout("30 min")
    try:
        cpu = ['1', '2', '3', '4']
        for i in cpu:
            command = MemDumperTool + ' -s --IP_Addr=\"192.168.255.1\" --Port=\"15002\" FSPB ' + FSP_number + Faraday_number + i
            connections.execute_shell_command(command)

    finally:
        connections.set_shell_timeout(old_time)

def dump_memory_with_memdumper(DSPBoard, CPUNumber):
    """This keyword used to dump eNB memory information with memdumper.
    | Input Parameters  | Man. |  Description |
    | FSP_number        | Yes  |  FSP id      |
    | Faraday_number    | Yes  |  Faraday id  |

    Example
    | dump memory with memdumper | 0x12 | 61 |
    """
    #single dumping
    #MemDumper -s -ip <str> -port <str> -task <str> -da <str> -dl <str> <BoardType> <DSPBoard> <CPUNumber> <CoreIndex> [-file <str>]
    #MemDumper -s -ip 192.168.255.1 -port 15003 -task TASK_DSP_BROWSER -da 0x02f10000 -dl 0x50000 FSPB 0x12 1 1
    #MemDumper -s -ip <str> -port <str> -task <str> -da <str> -dl <str> <BoardType> <DSPBoard> <CPUNumber> [-file <str>]
    #MemDumper -s -ip 192.168.255.1 -port 15003 -task TASK_FOR_MEMDUMPER -da 0x02f10000 -dl 0x50000 FSMr3 0x10 1 1
    #whole dumping .Place "memorydumps.ini" (fixed filename) same as MemDumper.exe directory
    #MemDumper -s -ip <str> -port <str> -task <str> <BoardType> <DSPBoard> <CPUNumber>
    #MemDumper -s -ip 192.168.255.1 -port 15003 -task TASK_ON_FCTMCU FSPB 0x10 1
    old_time = connections.set_shell_timeout("30 min")
    command = MemDumperTool + ' -s -ip 192.168.255.1 -port 15003'
    try:
        connections.execute_shell_command(command)
    finally:
        connections.set_shell_timeout(old_time)

if __name__ == '__main__':
    connections.connect_to_host('10.69.71.113', '23', 'tdlte-tester', 'btstest')

    dump_entry = ['1231:0x872479f0:400', '1231:0x9c80a480:400', '1231:0x80080000:128', '1231:0x80080080:36096',\
                  '1241:0x80080000:128', '1241:0x80080080:36096', '1251:0x80080000:128', '1251:0x80080080:36096']

    mem_dumper(dump_entry)
    print("-----------------------------------------------------------------")
    print "MEMORY DUMP DONE"

    connections.disconnect_all_hosts()
    pass
