##--20180423--##
import config

debug=config.debug

ACTION='0'
KEYWORD1='1'
KEYWORD2='2'

#query logpattern in logcat
LOGPATTERN_LOGCAT=2

raw_logcat_pattern=[
{ACTION:'Connecting...', KEYWORD1:'A2dpStateMachine: Connection state', KEYWORD2:'0->'},
{ACTION:'Connected', KEYWORD1:'A2dpStateMachine: Connection state', KEYWORD2:'->2'},
{ACTION:'Connect fail', KEYWORD1:'A2dpStateMachine: Connection state', KEYWORD2:'1->0'},
{ACTION:'disconnected', KEYWORD1:'A2dpStateMachine: Connection state', KEYWORD2:'2->0'},
{ACTION:'playing...', KEYWORD1:'A2dpStateMachine: A2DP Playing state :', KEYWORD2:'11->10'},
{ACTION:'suspend', KEYWORD1:'A2dpStateMachine: A2DP Playing state :', KEYWORD2:'10->11'},
]

#pattern set block
pattern_set=[]

def load(log_type):
    pattern_set.clear()
    if log_type==LOGPATTERN_LOGCAT:
        target_pattern=raw_logcat_pattern

    for index in range(len(target_pattern)):
       mPattern=pattern()
       for a, b in target_pattern[index].items():
           if a==ACTION: mPattern.action=b
           elif a==KEYWORD1: mPattern.keyword1=b
           elif a==KEYWORD2: mPattern.keyword2=b
           else: print('Pattern have error type\n')
       pattern_set.append(mPattern)

def dumpPattern(pattern):
    print('action:', pattern.action)
    print('keyword1:', pattern.keyword1)
    print('keyword2:', pattern.keyword2)

class pattern:
    action=''
    keyword1=''
    keyword2=''

    def __init__(sef):
        pass
