##--20180423--##
#Pattern tag
SAME_LINE='0'
TARGET='1'
LINE_START='2'
LINE_END='3'
MAC_TARGET='4'
MAC_START='5'
NAME_TARGET='6'
NAME_START='7'
NAME_END='8'

#query logpattern in bugreport
LOGPATTERN_BUGREPORT=1
#query logpattern in logcat
LOGPATTERN_LOGCAT=2
#query logpattern in asuseventlog
LOGPATTERN_ASUSEVENTLOG=3

raw_bugreport_pattern=[
{SAME_LINE:False,TARGET:'Bonded devices:\n',LINE_START:'0',LINE_END:'\n',MAC_TARGET:'strip',NAME_TARGET:']', NAME_END:'\n'}
]
raw_logcat_pattern=[
{SAME_LINE:True, TARGET:'[BT] Connected to ', NAME_TARGET:'RName:', NAME_END:'\n'},
{SAME_LINE:True, TARGET:'[BT] Disconnected from ', NAME_TARGET:'RName:', NAME_END:'\n'},
]
raw_asuseventlog_pattern=[
{SAME_LINE:True, TARGET:'[BT] Connected to ', NAME_TARGET:'RName:', NAME_END:'\n'},
{SAME_LINE:True, TARGET:'[BT] Disconnected from ', NAME_TARGET:'RName:', NAME_END:'\n'},
]

#pattern set block
pattern_set=[]

def load(log_type):
    pattern_set.clear()
    if log_type==LOGPATTERN_BUGREPORT:
        target_pattern=raw_bugreport_pattern
    elif log_type==LOGPATTERN_LOGCAT:
        target_pattern=raw_logcat_pattern
    elif log_type==LOGPATTERN_ASUSEVENTLOG:
        target_pattern=raw_asuseventlog_pattern

    for index in range(len(target_pattern)):
       mPattern=pattern()
       for a, b in target_pattern[index].items():
           if a==SAME_LINE: mPattern.same_line=b
           elif a==TARGET: mPattern.target=b
           elif a==LINE_START: mPattern.line_start=b
           elif a==LINE_END: mPattern.line_end=b
           elif a==MAC_TARGET: mPattern.mac_target=b
           elif a==MAC_START: mPattern.mac_start=b
           elif a==NAME_TARGET: mPattern.name_target=b
           elif a==NAME_START: mPattern.name_start=b
           elif a==NAME_END: mPattern.name_end=b
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

class pattern:
    same_line=True
    target='' #if same_line is true, target is mac target and mac_target is no meaning, else target is line target
    line_start=''
    line_end=''
    mac_target=''
    mac_start=''
    name_target=''
    name_start=''
    name_end=''

    def __init__(sef):
        pass
