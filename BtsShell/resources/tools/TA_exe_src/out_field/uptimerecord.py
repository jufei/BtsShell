from __future__ import with_statement
import csv
import os
import time


def file_read(FileFullPath, ReadMode = 'r'):
    if not os.path.isfile(FileFullPath):
        print "File %s does not exists" % (FileFullPath)
        return []
    try:
        with open(FileFullPath, ReadMode) as p_FileObj:
            return p_FileObj.readlines()
    except IOError:
        print "Open %s failed!" % (FileFullPath)
        return []
    
def record_local_time():
    """ record_local_time
    """
    ret = ''
    for value in time.localtime()[3:6]:
        temp = str(value)
        ret = ret + ":" + temp
    local_time = "local" + ret
    
    return local_time
    
def read_output_and_analyze(output_file_path):

    Result = {}
    flag = 0
    try:
        output_content = file_read(output_file_path)
        print "read content from output.txt successfully!"
    except:
        raise Exception, "read content from output.txt failed!"
    for line in output_content:
        if 'command :uptime   return is ->' in line and 'load average:' in line and 'failed' not in line:
            Result[str(line.split(':')[0])] = str(line.split('up')[-1].split('load average:')[0]).replace(",", " ").replace(' ', '')
            if flag == 0:
                Result['bbuip'] = str(line.split('up')[-2].split('return is ->')[-1]).replace(' ', '')
                flag = 1
                
                
        if 'failed!' in line:
            Result[str(line.split(':')[0])] = 'failed'
            
    if flag == 0:
        Result['bbuip'] = record_local_time()
   
    return Result

def judge_csv_exist(csv_file_path):
    try:
        if not os.path.exists(csv_file_path):
            try:
                with open(csv_file_path, 'wb') as csvfile:
                    sp = csv.writer(csvfile, dialect = 'excel')
                    sp.writerow(['bbuip'])
                    print "create new uptime.csv file successfully!"
            except Exception, s:
                print s
                raise Exception,"Create new uptime.csv file error!try again!"
    except Exception, e:
        print e
        raise Exception, "Judge if csv file is existed error!please check"

def read_write_csv(csv_file_path, content):

    try:
        judge_csv_exist(csv_file_path)      # judge if csv file is existed
        with open(csv_file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile, dialect = 'excel')
            line_list = [ln for ln in reader]
    except Exception, s:
        print s
        raise Exception,"Read content from uptime.csv file error!try again!"
    
    row = len(line_list)
    first_list = line_list[0]
    column = len(first_list)
    last_line = []
    for i in range(column):
        last_line.append('')

    for ip in content.keys():
        if ip in first_list:
            index = first_list.index(ip)
            last_line[index] = content[ip]
        else:
            first_list.append(ip)
            last_line.append(content[ip])
            
  #  update_time = str(time.strftime('%Y_%m_%d %H:%m:%S'))
    last_line[0] = content['bbuip']
    line_list.append(last_line)

    try:
        with open(csv_file_path, 'wb') as csvfile:
            sp = csv.writer(csvfile, dialect = 'excel')
            for con in line_list:
                sp.writerow(con)
            print "Write content to uptime.csv successfully!"
            
    except Exception, s:
        print s
        raise Exception,"Write content to uptime.csv file error!try again!"

def uptime_record(output_file_name, uptime_csv_name):

    current_dir = os.path.abspath(os.curdir)
    output_file_path = os.path.join(current_dir, output_file_name)
    csv_file_path = os.path.join(current_dir, uptime_csv_name)
    read_write_csv(csv_file_path, read_output_and_analyze(output_file_path))

    
if __name__ == '__main__':

    try:
        uptime_record("output.txt", "uptime.csv")
        time.sleep(1)
        print "@action done@"
    except Exception, e:
        print e
    
    pass
