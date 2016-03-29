"""This file is used to control squans dongle by send AT command,
And this file should be put in the Dongle Control PC which installed
Python ENV.
"""

import serial
import re
import sys
from optparse import OptionParser

class SequansControl():
    def __init__(self, com_port="COM1"):
        self.port = com_port
        print "Sequans Dongle started:", self.port

    def __excute_at_command(self, at_command):
        ser_obj = serial.Serial(port='%s' % (self.port),\
                        baudrate=9600, bytesize=8,\
                        parity='N', stopbits=1,\
                        timeout=10)

        ret = ""
        try:
            ser_obj.write(at_command)
            ser_obj.write("\r")
            ret = ser_obj.read(512)
            print ret
        finally:
            ser_obj.close()
            return ret

    def ue_attach(self, freq="2.6G", imsi=""):
        set_freq_cmd = "AT!=addInitCellSelectFreq 38 38000"
        if freq == "2.3G":
            set_freq_cmd = "AT!=addInitCellSelectFreq 40 39150"

        if imsi == "":
            # send "AT!=setusimMode useFakeUsim=0" when using USIM card
            ret = self.__excute_at_command("AT!=setusimMode useFakeUsim=0")
        else:
            # set imsi=262030020001226 if imsi is assigned for each team by lab team
            set_imsi_cmd = "AT!=set imsi=%s" % (imsi)
            ret = self.__excute_at_command(set_imsi_cmd)
        if "Ok" not in ret:
            print "Set IMSI mode failed"
        ret = self.__excute_at_command("AT!=removeallInitCellSelectFreq")
        if "Ok" not in ret:
            print "Remove initial selected cell failed"
        ret = self.__excute_at_command(set_freq_cmd)
        if "Ok" not in ret:
            print "Force cell and PCI failed"
        ret = self.__excute_at_command("AT!=poweron")
        if "Ok" not in ret:
            print "PowerOn failed"

    def ue_detach(self):
        ret = self.__excute_at_command("AT!=poweroff")
        if "Ok" not in ret:
            print "Set IOT mode failed"

    def check_ue_attach_status(self):
        ret = self.__excute_at_command("AT+CEREG=?")

        match = re.search("(\d,\d,\d)", ret)
        if match:
            attach_info = match.group()
            reg_list = attach_info.split(",")
            if reg_list[0] is "0":
                print "UE is on disable status"
                return False
            elif reg_list[0] is "1" or "2":
                print "UE attached successfully"
                return True
            else:
                return False
        else:
            return False

    def get_ue_ip_address(self):
        ip_pattern = "([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5]).*"

        ret = self.__excute_at_command("AT+CGCONTRDP=1")
        match = re.search(ip_pattern, ret)
        if match:
            ue_ip = match.group(0)
            if re.search("\"", ue_ip):
                ue_ip = re.sub("\"", "", ue_ip)
            return ue_ip
        else:
            raise Exception, "The information returned do not contain any correct ip address"

    def set_cqi_ri(self, cqi="", ri=""):
        if cqi:
            ret = self.__excute_at_command("AT!=setUlParams cqi-value=%s" % (cqi))
            if "Ok" not in ret:
                print "Set CQI value failed"
        if ri:
            ret = self.__excute_at_command("AT!=setUlParams ri-value=%s" % (ri))
            if "Ok" not in ret:
                print "Set RI value failed"

    def start_sqn4logger(self, logger_path, logger_file, log_saved):
        """This keyword used to catch text type log information, and you should know the
        logger tool path, logger file path and path for logs to be saved, all these paths
        should be based on the Dongle Control PC.

        Example
        | start_sqn4logger | C:\sqn4glogger.exe | C:\sqn4glogger.conf | C:\sequans_log.txt |
        """
        # logger_file could be "sqn4glogger.conf"
        # log_saved could be "C:\sequans_log.txt"
        cmd = '%s -c "sqn4glogger.conf" -o %s --dc localhost@7771' % (logger_path, logger_file, log_saved)
        ret = os.system(cmd)
        return ret

def main():
    """This keyword used for parsing arguments input.

    Example
    | python sequans_control.py --port com1 -o attach --freq 2.3G |
    """
    parser = OptionParser()
    parser.add_option("--port", action="store", type="string", dest="port")
    parser.add_option("-o", "--operation", action="store", type="string", dest="operation")
    parser.add_option("--freq", action="store", type="string", dest="frequency")
    parser.add_option("--imsi", action="store", type="string", dest="imsi")
    parser.add_option("--cqi", action="store", type="string", dest="cqi")
    parser.add_option("--ri", action="store", type="string", dest="ri")
    (options, args) = parser.parse_args()

    if options.port:
        sequans_control = SequansControl(options.port)
    else:
        raise Exception, "Please input correct com port"

    if options.operation == "attach":
        if options.imsi:
            sequans_control.ue_attach(options.frequency, options.imsi)
        else:
            sequans_control.ue_attach(options.frequency)
    elif options.operation == 'detach':
        sequans_control.ue_detach()
    elif options.operation == 'checkstatus':
        sequans_control.check_ue_attach_status()
    elif options.operation == 'getip':
        sequans_control.get_ue_ip_address()
    elif options.operation == 'setcqiri':
        sequans_control.set_cqi_ri(options.cqi, options.ri)
    else:
        raise Exception, "The operation \"%s\" do not support now" % (options.operation)

main()

if __name__ == "__main__":
    pass
