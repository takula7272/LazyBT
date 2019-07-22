##--20180423--##
import sys
import getopt
import config
import device
import log_file
import log_pattern

debug=config.debug

target_device_set={}

def parsing(profile, logtype):
    log_file.parse_logfile_name(device.inputdir,device.force_parsing)

    log_pattern.load_pattern(profile, logtype)

    if len(log_file.logcat_filename):
        for filename in log_file.logcat_filename:
            if debug: print('Log:' + filename)
            f=open(filename,'r', encoding='ISO-8859-1')
            line=f.readline()
            while line:
                for index in range(len(log_pattern.pattern_set)):
                    if (log_pattern.pattern_set[index].profile==log_pattern.PROFILE_A2DP) or (log_pattern.pattern_set[index].profile==log_pattern.PROFILE_HFP) or (log_pattern.pattern_set[index].profile==log_pattern.PROFILE_HID):
                        if not log_pattern.pattern_set[index].keyword1 in line:
                            continue
                        if not log_pattern.pattern_set[index].keyword2 in line:
                            continue

                        if log_pattern.pattern_set[index].macinclude == True:
                            for a, b in target_device_set.items():
                                if a in line:
                                    print('Device ' + b + ' ' + log_pattern.pattern_set[index].action)
                                    print(line.replace('\n',''))
                                    break
                    elif log_pattern.pattern_set[index].profile==log_pattern.PROFILE_BLE:
                        if not log_pattern.pattern_set[index].keyword1 in line:
                            continue
                        if not log_pattern.pattern_set[index].keyword2 in line:
                            continue

                        mStart=line.index(log_pattern.pattern_set[index].keyword1)+len(log_pattern.pattern_set[index].keyword1)
                        mEnd=line.index(log_pattern.pattern_set[index].keyword2)
                        BLEapp=line[mStart:mEnd].strip()
                        print(BLEapp + ' ' + log_pattern.pattern_set[index].action)
                        print(line.replace('\n',''))
                    elif log_pattern.pattern_set[index].profile==log_pattern.PROFILE_GAP:
                        if not log_pattern.pattern_set[index].keyword1 in line:
                            continue

                        print(log_pattern.pattern_set[index].action)
                        print(line.replace('\n',''))

                line=f.readline()

            f.close()

def main (argv):
    opts, args=getopt.getopt(argv,"m:n:rd:p:t:")
    dump_type=device.DUMP_ALL
    target=''
    profile=log_pattern.PROFILE_ALL
    logtype=log_pattern.TYPE_ALL
    for op, value in opts:
        if op =="-d":
            device.inputdir=value
        elif op =="-m":
            target=value
            dump_type=device.DUMP_BY_MAC
        elif op=="-n":
            target=value
            dump_type=device.DUMP_BY_NAME
        elif op=="-r":
            device.force_parsing=True
        elif op=="-p":
            profile=value
        elif op=="-t":
            logtype=value

    device.get_device(dump_type, target, target_device_set)

    for a, b in target_device_set.items():
        if debug: print("{0} - {1}".format(a, b))

    parsing(profile, logtype)

if __name__ == "__main__":
    main(sys.argv[1:])