"""
HexByteConversion

Convert a byte string to it's hex representation for output or visa versa.

_ByteToHex converts byte string "\xFF\xFE\x00\x01" to the string "FF FE 00 01"
_HexToByte converts string "FF FE 00 01" to the byte string "\xFF\xFE\x00\x01"
"""

import socket
import sys
import os
import time


def _ByteToHex( byteStr ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """

    # Uses list comprehension which is a fractionally faster implementation than
    # the alternative, more readable, implementation below
    #
    #    hex = []
    #    for aChar in byteStr:
    #        hex.append( "%02X " % ord( aChar ) )
    #
    #    return ''.join( hex ).strip()

    return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

def _HexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    # The list comprehension implementation is fractionally slower in this case
    #
    #    hexStr = ''.join( hexStr.split(" ") )
    #    return ''.join( ["%c" % chr( int ( hexStr[i:i+2],16 ) ) \
    #                                   for i in range(0, len( hexStr ), 2) ] )

    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

    return ''.join( bytes )

def getCpuVersions(fsp_number):
    #create an INET, STREAMing socket
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("192.168.255.1", 15003))
    except:
        print "connect failed: maybe connection is currently used by LTEBrowser"
        return

    print
    print "Get CPU Versions for all CPUs on all FSPCs. Inc 18: ENV_17_..."
    print
    print "FSP"
    print "| NYQUIST"
    print "| | CORE"
    print "-----------------------------------------------------------------------"
    for fsp in range(0,int(fsp_number)):
        for nyquist in range(6):
            for core in range(4):
                print "%d %d %d\r\n" % (fsp+1, nyquist+1, core+1),
                cmd = "00 00 1B 25 %00d %00d 12 00 00 00 00 00 00 14 00 00 00 00 00 00" % (12+fsp, 30+10*nyquist+core+1)
                data = _HexToByte(cmd)

                try:
                    s.send(data)
                except:
                    print "send failed: maybe connection is currently used by LTEBrowser"
                    s.close()
                    return

                s.settimeout(1)
                try:
                    chunk = s.recv(1024)
                except:
                    print "No answer"
                    return str(fsp+12)+str(nyquist+1)+str(core+1)

    s.close()

if __name__ == '__main__':
    print getCpuVersions('1')
    pass
