#-*- coding: utf-8 -*-
"""
@summary:
    
    Module to provide Rohde&Schwarz FSV signal analyzer operations.

    NI-VISA library and PyVISA module are required.

    Download NI-VISA 5.4.1
        
        Windows         http://www.ni.com/download/ni-visa-5.4.1/4627/en/
        Mac OS X        http://www.ni.com/download/ni-visa-5.4.1/4632/en/
        SUSE, RedHat    http://www.ni.com/download/ni-visa-5.4.1/4629/en/

    Download PyVisa

        https://github.com/hgrecco/pyvisa

@version:
    
    see __VERSION__

@revision history:
    
     05/08/14 - Shi, Jia (NSN - CN/Hangzhou), add key word fsv_run_commands()
     04/03/14 - Shi, Jia (NSN - CN/Hangzhou), First draft

@copyright: (c) 2014 NSN. All rights reserved.
"""

import visa
import time
import sys
import argparse
import traceback


__VERSION__ = 0.2

__all__ = ["fsv_run_commands"]


def fsv_run_commands(ip, cmds):
    """
    RF DOC NEEDS TO BE ADDED HERE
    """
    result = []

    try:
        fsv = RsFsv(ip)

        if isinstance(cmds, (str, unicode)):
            cmds = [cmds]

        for cmd in cmds:
            ret = fsv.fsv_run_command(cmd, 0)
            result.append(ret)
            print "Command: %s\nResult: %s\n" % (cmd, ret)
    except:
        raise
    else:
        return result


class MyArgPsr(argparse.ArgumentParser):

    """
    Argument parser inherit from argparse
    """

    def error(self, errMsg):
        """Override the default error handler
        """
        print "Error: %s.\n" % errMsg
        self.print_help()
        print
        raise IOError("%s.\n" % errMsg)
        sys.exit()


class Instrument(object):

    """
    Common instrument class in which included common
    operations (commands) which are described in the
    IEEE 488.2 (IEC 625-2) standard.

    These commands have the same effect and are employed
    in the same way on different devices.
    """

    ascii = 0
    single = 1
    double = 3
    big_endian = 4

    CR = '\r'
    LF = '\n'

    def __init__(self):
        """ This is a virtual constructor, all required instance
        attributes are listed but not implemented in this
        class, they shall be implemented in subclasses.
        """
        self.inst = None

    def common_calibrate(self):
        """ Initiates a calibration of the instrument and
        subsequently queries the calibration status.

        @return <str>: calibration status from the device,
                       responses > 0 indicate errors.
        """
        self.inst.write("*CAL?")
        time.sleep(25)
        return self.inst.read()

    def common_clear_statue(self):
        """
        The command clears the output buffer and error queue.

        @return: None
        """
        self.inst.write("*CLS")
        time.sleep(1)

    def common_event_status_enable(self, val):
        """
        Sets the event status enable register to the specified value.

        @val <int>: ESE register value, range 0-255

        @return: the return code from the FSV.
        """
        if int(val) not in range(0, 256):
            raise ValueError("value %s out of range 0-255" % val)
        else:
            return self.inst.write("*ESE %s" % val)

    def common_event_status_read(self):
        """
        Returns the contents of the event status register
        in decimal form and subsequently sets the register to zero.

        @return: the contents of the event status register in
                 decimal, range 0-255.
        """
        return self.inst.ask("*ESR?")

    def common_identification_query(self):
        """
        @return: the instrument identification.
        """
        self.inst.write("*IDN?")
        time.sleep(0.1)
        return self.inst.read()

    def common_individual_status_query(self):
        """
        @return: returns the contents of the IST flag in decimal form.
                 The IST flag is the status bit which is sent during
                 a parallel poll. The return value could be 0 or 1.
        """
        return self.inst.ask("*IST?")

    def common_operation_complete(self):
        """
        Sets bit 0 in the event status register when all
        preceding commands have been executed.

        This bit can be used to initiate a service request.
        The query form writes a "1" into the output buffer
        as soon as all preceding commands have been executed.
        This is used for command synchronization.
        """
        return self.inst.write("*OPC")

    def common_option_ident_query(self):
        """
        @return: a list of all installed and activated options
                 included in the instrument which are separated
                 by commas.
        """
        return self.inst.ask("*OPT?")

    def common_pass_control_back(self, addr):
        """
        Pass Control Back

        Indicates the controller address to which remote control
        is returned after termination of the triggered action.

        @addr <int>: control address, range 0-30.
        """
        return self.inst.write("*PCB %s" % addr)

    def common_ppr_enable(self, val):
        """
        Sets parallel poll enable register to the indicated value.

        @val <int>: range 0-255

        @return: returns the contents of the parallel poll
                 enable register in decimal form
        """
        print self.inst.write("*PRE %s" % val)

    def common_power_on_status_clear(self):
        """
        Determines whether the contents of the ENABle registers
        are preserved or reset when the instrument is switched on.

        Thus a service request can be triggered when the instrument is
        switched on, if the status registers ESE and SRE are suitably configured. The
        query reads out the contents of the "power-on-status-clear" flag.

        @return: 0 - the contents of the status registers are preserved
                 1 - resets the status registers
        """
        self.inst.write("*PSC")
        return self.inst.ask("*PSC?")

    def common_reset(self):
        """
        Sets the instrument to a defined default status.
        The default settings are indicated in the description of commands.

        @return: what the device returns.
        """
        self.inst.write("*RST")

    def common_service_request_enable(self, val):
        """
        Sets the service request enable register to the
        indicated value. This command determines under
        which conditions a service request is triggered.

        @val <int>: contents of the service request enable register
                    in decimal form, bit 6 (MSS mask bit) is always 0,
                    range 0-255

        @return: what the device returns.
        """
        return self.inst.write("*SRE %s" % val)

    def common_status_byte_query(self):
        """
        @return: the contents of the status byte in decimal form.
        """
        return self.inst.ask("*STB?")

    def common_trigger(self):
        """
        Triggers all actions waiting for a trigger event.
        In particular, *TRG generates a manual trigger signal
        (Manual Trigger).

        This common command complements the commands of the TRIGgersubsystem.
        *TRGcorresponds to the INITiate:IMMediatecommand.

        @return: what the device returns.
        """
        return self.inst.write("*TRG")

    def common_self_test(self):
        """
        Triggers self-tests of the instrument and returns an error code
        in decimal form (see Service Manual supplied with the instrument).

        "0" indicates no errors.

        @return: error code.
        """
        self.inst.write("*TST?")
        time.sleep(12)
        return self.inst.read()

    def common_wait_to_continue(self):
        """
        Prevents servicing of the subsequent commands until
        all preceding commands have been executed and all
        signals have settled.
        """
        self.inst.write("*WAI")
        time.sleep(5)
        return self.inst.read()


class RsFsv(Instrument):

    """
    The class for Rohde&Schwarz FSV Signal and Spectrum Analyzer which
    provides common operations including preset, run SCPI command, etc.
    """

    def __init__(self, ip=None):
        self.rm = visa.ResourceManager()

        if ip is not None:
            self.addr = "TCPIP::%s::INSTR" % ip
            self.inst = self.rm.get_instrument(self.addr, timeout=10)

    def fsv_connect(self, ip):
        """ in case one wants to get self.inst object (since
        the constructor is not allowed to return anything),
        this method is provided as an alternative.

        @ip <str>: FSV ip address.
        """
        self.addr = "TCPIP::%s::INSTR" % ip
        self.inst = self.rm.get_instrument(self.addr, timeout=10)

        return self.inst

    def fsv_preset(self):
        """ This command initiates an instrument reset.

        The common SCPI command *RST has the same effect as SYSTem:PRESet
        and both of those command will clear the output buffer but will
        not clear the error queue.

        @return <str>: error status message, if any.
        """
        return self.fsv_run_command("SYSTEM:PRESET", delay=0.5)

    def fsv_run_command(self, command, expRc=0, delay=0.1):
        """ Execute an SCPI commands. For SCPI commands usage,
        refer to FSV_OperatingManual.pdf, which can be download
        on R&S official website.

        @command   <str>: the SCPI commands to run.
        @[expRc]   <int>: excepted return code from executing, 0 by
                          default and None to skip error.
        @[delay] <float>: delay between write and query, defaults to 0.1s.
        @return    <str>: error message, if any.
        """
        cmd = command.strip()
        self.inst.write(command.strip())

        time.sleep(delay)

        # query processing
        if '?' in cmd:
            return self.inst.read()
        else:
            return self.__fsv_query_err_msg(expRc)

    def __fsv_query_err_msg(self, expErrCod=None):
        """ Get the error messages which are entered in the
        error/event queue of the status reporting system.

        - Error messages defined by SCPI are marked negative error codes.
        - Error messages defined by device are marked positive error codes.

        @[expErrCod] <int>: the excepted error code, None by default.
        @return      <str>: error messages, the format is as follows
                            <error code>, "<error text with queue query>;
                            <remote control command concerned>"
        """
        self.inst.write("SYSTem:ERRor?")
        time.sleep(0.1)
        errMsg = self.inst.read()

        if expErrCod is None or int(errMsg.split(',')[0]) == expErrCod:
            return errMsg
        else:
            raise Exception(errMsg)


if __name__ == "__main__":
    arg = MyArgPsr(conflict_handler='resolve')
    arg.add_argument("commands", nargs='+', help="The SCPI commands to run, commands separated by spaces.")
    arg.add_argument("--ip", default="192.168.255.1", help="Device's IP address, 192.168.255.1 by default.")
    arg.add_argument("--version", action="version", version="version %s" % __VERSION__)
    args = arg.parse_args()

    fsv = RsFsv(args.ip)
    for cmd in args.commands:
        print "Command: %s\nResult: %s\n" % (cmd, fsv.fsv_run_command(cmd))
