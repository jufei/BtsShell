import struct

#003CB49a -- 003CB4A3

start = int('003CB49a', 16)
stop = int('003CB4A3', 16)

def _find_tag_position(tagname, binfile):
    target_pos = ''
    try:
        myfile = None
        myfile = open(binfile, 'rb+')
        
        pos = 0
        while 1:
            try:
                content = myfile.read(1)
                pos += 1
                c = struct.unpack('c', content)[0]
            except:
                print "end of file"
                break

            #find tag start <
            if c == '<':
                tag = ''

                #find the right >
                while 1:
                    try:
                        content = myfile.read(1)
                        pos += 1
                        c = struct.unpack('c', content)[0]
                    except:
                        print "end of file"
                        break
                    
                    
                    if c == '>':
                        break
                    tag += c
                    
                # check tag name    
                if str(tag) == str(tagname):
                    print "find tag '%s' at 'pos': %s" % (tagname, pos)
                    target_pos = pos
                    break

        # get tag value
        value = ''
        while 1:
            try:
                content = myfile.read(1)
                pos += 1
                c = struct.unpack('c', content)[0]
                
            except:
                print "end of file"
                break

            if c != '<':
                value += c
            else:
                break

        print "tag %s value: %s" % (tagname, value)
        return target_pos, value
    except Exception, err:
        raise Exception, err
        
    finally:
        if myfile:
            myfile.close()

def _write_bin_file(pos, strvalue, binfile):
    try:
        myfile = open(binfile, 'rb+')        
        myfile.seek(pos) 
        ss = struct.pack("%ss" % len(strvalue), str(strvalue))
        myfile.write(ss)

        return True
    except Exception, err:
        print err
        return False
    finally:
        myfile.close()
        
def read_bin_file(binfile, tagname):
    """read_bin_file to read bin file with tagname.

    | Input Paramaters   | Man. | Description |
    | binfile     | yes  | Absolute path of bin file |
    | tagname     | yes  | tag name in bin file <xxx> |

    Example
    | ${value}  | read_bin_file | d:\\xxx.bin | SwVersion |
    """
    pos, value = _find_tag_position(tagname, binfile)
    return  value
    
def modify_bin_file(binfile, tagname, newvalue):
    """modify_bin_file to modify bin file with tagname, but the new value need to have same length with old value.

    | Input Paramaters   | Man. | Description |
    | binfile     | yes  | Absolute path of bin file |
    | tagname     | yes  | tag name in bin file <xxx> |
    | newvalue    | yes   | new value length should be same with old one|

    Example:    
    | modify_bin_file | d:\\xxx.bin | SwVersion | 5912128 | #old value as 5912129 |
    """
    pos, value = _find_tag_position(tagname, binfile)

    if newvalue == value:
        print "needn't change, value is same"
        return True

    elif len(newvalue) == len(value):
        ret = _write_bin_file(pos, newvalue, binfile)
        print"Modify tag '%s' as '%s' successfully!" % (tagname, newvalue)
        return ret

    else:
        raise "the new value length is diff with exsited value"
        return False
    
    
if __name__ == '__main__':         
    modify_bin_file('D:\\work\\xml\\modify bin file\\LT-N1-DL8DSP_HD406900.BIN', 'Crc32','0x6765e815' )
    print read_bin_file('D:\\work\\xml\\modify bin file\\FCT-CCSSA2-BW_13043100.bin', 'SwVersion')


