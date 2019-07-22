##--20180423--##
import log_file
import device
import A2DP_log_pattern
import config

debug=config.debug

target_device_set={}

def allaction(mTarget):
    target_device_set=mTarget
    if not len(log_file.logcat_filename) and not log_file.parse_logcat_file_name(device.inputdir):
        print('No logcat file')
        return

    log_file.logcat_filename.sort()
    log_file.logcat_filename.reverse()
    A2DP_log_pattern.load(A2DP_log_pattern.LOGPATTERN_LOGCAT)
    for filename in log_file.logcat_filename:
        if debug: print('Log:' + filename)
        f=open(filename,'r', encoding='ISO-8859-1')
        line=f.readline()
        while line:
            for index in range(len(A2DP_log_pattern.pattern_set)):
                if not A2DP_log_pattern.pattern_set[index].keyword1 in line:
                    continue
                if not A2DP_log_pattern.pattern_set[index].keyword2 in line:
                    continue

                for a, b in target_device_set.items():
                    if not a in line:
                        continue

                    print('Device ' + b + ' ' + A2DP_log_pattern.pattern_set[index].action)
                    print(line.replace('\n',''))
            line=f.readline()

        f.close()
