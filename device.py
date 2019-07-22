##--20180423--##
import sys
import getopt
import os
import device_log_pattern
import log_file
import config

#debug on/off
debug=config.debug

## constant ##
#BT Mac length
MAC_LENGTH=17
#dump all device
DUMP_ALL=1
#query device by name
DUMP_BY_NAME=2
#query device by mac
DUMP_BY_MAC=3

#device set block
device_set={}

#intial input dir to root dir
inputdir=config.inputdir
#default get device information from file
force_parsing=config.force_parsing

def get_device_from_file():
    f=open(os.path.join(inputdir,config.Device_File), 'r')
    line=f.readline();
    while line:
        device_set[line[:MAC_LENGTH]]=line[MAC_LENGTH+3:].replace('\n','')
        line=f.readline()

    f.close()

def set_device_to_file():
    f=open(os.path.join(inputdir,config.Device_File), 'w')
    for a, b in device_set.items():
        f.write("{0} - {1}\n".format(a, b))
    f.close()

def parsemac(pattern, line, target):
    mMac_target=target
    if 'strip' in target:
        line=line.strip()
        return line[:MAC_LENGTH].upper()
    else:
        start_point=line.index(target)+len(target)
        end_point=start_point+MAC_LENGTH
    return line[start_point:end_point].upper()

def parsename(pattern, line):
    if pattern.name_target not in line:
        return ''
    if debug: print(line)
    if debug: dumpPattern(pattern)
    start_point=line.index(pattern.name_target)+len(pattern.name_target)
    if '\n' in pattern.name_end:
       return line[start_point:].replace('\n','').strip()

def get_device_from_log():
    device_log_pattern.load(device_log_pattern.LOGPATTERN_BUGREPORT)
    for filename in log_file.bugreport_filename:
        f=open(filename,'r', encoding='ISO-8859-1')
        line=f.readline()
        while line:
            for index in range(len(device_log_pattern.pattern_set)):
                if device_log_pattern.pattern_set[index].target in line:
                    if device_log_pattern.pattern_set[index].same_line==False:
                        line=f.readline()
                        while not (line==device_log_pattern.pattern_set[index].line_end):
                            mac=parsemac(device_log_pattern.pattern_set[index], line, device_log_pattern.pattern_set[index].mac_target)
                            name=parsename(device_log_pattern.pattern_set[index], line)
                            device_set[mac]=name
                            line=f.readline()
            line=f.readline()
        f.close()

    device_log_pattern.load(device_log_pattern.LOGPATTERN_LOGCAT)
    for filename in log_file.logcat_filename:
        if debug: print('Log:' + filename)
        f=open(filename,'r', encoding='ISO-8859-1')
        line=f.readline()
        while line:
            for index in range(len(device_log_pattern.pattern_set)):
                if device_log_pattern.pattern_set[index].target in line:
                    if device_log_pattern.pattern_set[index].same_line==True:
                        mac=parsemac(device_log_pattern.pattern_set[index], line, device_log_pattern.pattern_set[index].target)
                        name=parsename(device_log_pattern.pattern_set[index], line)
                        if not device_set.__contains__(mac) or device_set[mac].strip() == '':
                            device_set[mac]=name
            line=f.readline()
        f.close()

    device_log_pattern.load(device_log_pattern.LOGPATTERN_ASUSEVENTLOG)
    for filename in log_file.asuseventlog_filename:
        if debug: print('Log:' + filename)
        f=open(filename,'r')
        line=f.readline()
        while line:
            for index in range(len(device_log_pattern.pattern_set)):
                if device_log_pattern.pattern_set[index].target in line:
                    if device_log_pattern.pattern_set[index].same_line==True:
                        mac=parsemac(device_log_pattern.pattern_set[index], line, device_log_pattern.pattern_set[index].target)
                        name=parsename(device_log_pattern.pattern_set[index], line)
                        if not device_set.__contains__(mac) or device_set[mac].strip() == '':
                            device_set[mac]=name
            line=f.readline()
        f.close()

    set_device_to_file()

def dump_device(dump_type, value):
    if dump_type==DUMP_ALL:
        for a, b in device_set.items():
            print("{0} - {1}".format(a, b))
    elif dump_type==DUMP_BY_NAME:
        for a, b in device_set.items():
            if str(value) in b: print("{0} - {1}".format(a, b))
    elif dump_type==DUMP_BY_MAC:
        for a, b in device_set.items():
            if str(value) in a: print("{0} - {1}".format(a, b))

def catch_device():
    global inputdir, force_parsing
    if os.path.exists(os.path.join(inputdir,config.Device_File)) and not force_parsing:
        get_device_from_file()
    else:
        if not log_file.parse_logfile_name(inputdir):
            print("No related file\n")
            return
        get_device_from_log()

def main(argv):
    opts, args=getopt.getopt(argv,"n:m:d:r")
    global inputdir, force_parsing
    dump_type=DUMP_ALL
    for op, value in opts:
        if op =="-d":
            inputdir=value
        elif op=="-n":
            dump_type=DUMP_BY_NAME
        elif op=="-m":
            dump_type=DUMP_BY_MAC
        elif op=="-r":
            force_parsing=True

    catch_device()
    dump_device(dump_type, value)

if __name__ == "__main__":
    main(sys.argv[1:])

def get_device(dump_type, value, target_device_set):
    catch_device()

    target_device_set.clear()
    if dump_type==DUMP_ALL:
        for a, b in device_set.items():
            target_device_set[a]=b
    elif dump_type==DUMP_BY_NAME:
        for a, b in device_set.items():
            if str(value) in b:
                target_device_set[a]=b
    elif dump_type==DUMP_BY_MAC:
        for a, b in device_set.items():
                target_device_set[a]=b







