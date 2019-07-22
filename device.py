##-- 20180420 --##
import sys
import getopt
import os
import zipfile
import log_pattern

#debug on/off
debug=False

## constant ##
#BT Mac length
MAC_LENGTH=17
#dump all device
DUMP_ALL=1
#query device by name
DUMP_BY_NAME=2
#query device by mac
DUMP_BY_MAC=3
#query logpattern in bugreport
LOGPATTERN_BUGREPORT=1
#query logpattern in logcat
LOGPATTERN_LOGCAT=2

#device set block
device_set={}
#pattern set block
pattern_set=[]
#bugreport file name block
bugreport_filename=[]
#logcat file name block
logcat_filename=[]
#device set record file name
Device_File="alldevice.txt"

#intial input dir to root dir
inputdir="."
#default get device information from file
force_parsing=False

def parse_logfile_name():
    global inputdir
    target_bugreport=False
    for dirPath, dirNames, fileNames in os.walk(inputdir):
        for f in fileNames:
            if 'bugreport' and 'zip' in f:
                with zipfile.ZipFile(os.path.join(dirPath, f),'r') as myzip:
                    unzippath=dirPath+'/bugreport'
                    myzip.extractall(path=unzippath)
                    myzip.close()
                bugreport_filename.clear()
                bugreport_filename.append(unzippath+'/'+f[:-3]+'txt')
                if debug: print(unzippath+'/'+f[:-3]+'txt')
                target_bugreport=True
            elif 'bugreport' in f and target_bugreport==False:
                if debug:print(os.path.join(dirPath, f))
                bugreport_filename.append(os.path.join(dirPath, f))
            elif 'logcat.txt' in f and 'asdf' not in f:
                if debug:print(os.path.join(dirPath, f))
                logcat_filename.append(os.path.join(dirPath, f))

    if not (len(bugreport_filename) or len(logcat_filename)):
        return False
    else:
        return True

def get_device_from_file():
    f=open(os.path.join(inputdir,Device_File), 'r')
    line=f.readline();
    while line:
        device_set[line[:MAC_LENGTH]]=line[MAC_LENGTH+3:].replace('\n','')
        line=f.readline()

    f.close()

def set_device_to_file():
    f=open(os.path.join(inputdir,Device_File), 'w')
    for a, b in device_set.items():
        f.write("{0} - {1}\n".format(a, b))
    f.close()

def load_log_pattern(log_type):
    pattern_set.clear()
    if log_type==LOGPATTERN_BUGREPORT:
        target_pattern=log_pattern.raw_bugreport_pattern
    elif log_type==LOGPATTERN_LOGCAT:
        target_pattern=log_pattern.raw_logcat_pattern

    for index in range(len(target_pattern)):
       mPattern=log_pattern.pattern()
       for a, b in target_pattern[index].items():
           if a==log_pattern.SAME_LINE: mPattern.same_line=b
           elif a==log_pattern.TARGET: mPattern.target=b
           elif a==log_pattern.LINE_START: mPattern.line_start=b
           elif a==log_pattern.LINE_END: mPattern.line_end=b
           elif a==log_pattern.MAC_TARGET: mPattern.mac_target=b
           elif a==log_pattern.MAC_START: mPattern.mac_start=b
           elif a==log_pattern.NAME_TARGET: mPattern.name_target=b
           elif a==log_pattern.NAME_START: mPattern.name_start=b
           elif a==log_pattern.NAME_END: mPattern.name_end=b
           else: print('Pattern have error type\n')
       pattern_set.append(mPattern)

def dumpPattern(pattern):
    print('same_line:', pattern.same_line)
    print('target:', pattern.target)
    print('line_start:', pattern.line_start)
    print('line_end:', pattern.line_end)
    print('mac_target:', pattern.mac_target)
    print('mac_start:', pattern.mac_start)
    print('name_target:', pattern.name_target)
    print('name_start:', pattern.name_start)
    print('name_end:', pattern.name_end)

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
    start_point=line.index(pattern.name_target)+len(pattern.name_target)
    if debug: dumpPattern(pattern)
    if '\n' in pattern.name_end:
       return line[start_point:].replace('\n','').strip()

def catch_device():
    global Device_File, inputdir, force_parsing
    if os.path.exists(os.path.join(inputdir,Device_File)) and (not (force_parsing == True)):
        get_device_from_file()
        return

    load_log_pattern(LOGPATTERN_BUGREPORT)
    for filename in bugreport_filename:
        f=open(filename,'r')
        line=f.readline()
        while line:
            for index in range(len(pattern_set)):
                if pattern_set[index].target in line:
                    if pattern_set[index].same_line==False:
                        line=f.readline()
                        while not (line==pattern_set[index].line_end):
                            mac=parsemac(pattern_set[index], line, pattern_set[index].mac_target)
                            name=parsename(pattern_set[index], line)
                            device_set[mac]=name
                            line=f.readline()
            line=f.readline()
        f.close()

    load_log_pattern(LOGPATTERN_LOGCAT)
    for filename in logcat_filename:
        if debug: print('Log:' + filename)
        f=open(filename,'r', encoding='ISO-8859-1')
        line=f.readline()
        while line:
            for index in range(len(pattern_set)):
                if pattern_set[index].target in line:
                    if pattern_set[index].same_line==True:
                        mac=parsemac(pattern_set[index], line,pattern_set[index].target)
                        name=parsename(pattern_set[index], line)
                        if not device_set.__contains__(mac) or device_set[mac].strip() == '':
                            device_set[mac]=name
            line=f.readline()
        f.close()
    set_device_to_file()

def dump_device(dump_type):
    if dump_type==DUMP_ALL:
        for a, b in device_set.items():
            print("{0} - {1}".format(a, b))
    elif dump_type==DUMP_BY_NAME:
        for a, b in device_set.items():
            if str(value) in b: print("{0} - {1}".format(a, b))
    elif dump_type==DUMP_BY_MAC:
        for a, b in device_set.items():
            if str(value) in a: print("{0} - {1}".format(a, b))

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

    if (parse_logfile_name()==False):
        print("No related file\n")
        return

    catch_device()
    dump_device(dump_type)

if __name__ == "__main__":
    main(sys.argv[1:])



