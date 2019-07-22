##--20180423--##
import sys
import getopt
import config
import device
import A2DP

debug=config.debug

A2DP_PROFILE='A2DP'

target_device_set={}

def prasing(profile):
    if profile==A2DP_PROFILE:
        if debug: print('A2DP')
        A2DP.allaction(target_device_set)
    else:
        print('Not support')

def main (argv):
    opts, args=getopt.getopt(argv,"m:n:rd:t:")
    dump_type=device.DUMP_ALL
    target=''
    profile=A2DP_PROFILE
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
        elif op=="-t":
            profile=value

    device.get_device(dump_type, target, target_device_set)

    for a, b in target_device_set.items():
        if debug: print("{0} - {1}".format(a, b))

    prasing(profile)

if __name__ == "__main__":
    main(sys.argv[1:])
