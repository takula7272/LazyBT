##--20180423--##
import config

debug=config.debug
verbose=config.verbose

ACTION='0'
KEYWORD1='1'
KEYWORD2='2'
LOGTYPE='4'
PROFILE='5'
MACINCLUDE='6'

TYPE_ALL='All'
TYPE_CONNECTION='Connection'
TYPE_AUDIO='Audio'

PROFILE_ALL='All'
PROFILE_A2DP='A2DP'
PROFILE_HFP='HFP'
PROFILE_BLE='BLE'
PROFILE_GAP='GAP'
PROFILE_HID='HID'

#query logpattern in bugreport
LOGPATTERN_BUGREPORT=1
#query logpattern in logcat
LOGPATTERN_LOGCAT=2
#query logpattern in asuseventlog
LOGPATTERN_ASUSEVENTLOG=3

raw_logcat_pattern=[
{ACTION:'Connecting...', KEYWORD1:'A2dpStateMachine: Connection state', KEYWORD2:'0->', LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_A2DP, MACINCLUDE:True},
{ACTION:'Connected', KEYWORD1:'A2dpStateMachine: Connection state', KEYWORD2:'->2', LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_A2DP, MACINCLUDE:True},
{ACTION:'Connect fail', KEYWORD1:'A2dpStateMachine: Connection state', KEYWORD2:'1->0', LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_A2DP, MACINCLUDE:True},
{ACTION:'disconnected', KEYWORD1:'A2dpStateMachine: Connection state', KEYWORD2:'2->0',LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_A2DP, MACINCLUDE:True},
{ACTION:'playing...', KEYWORD1:'A2dpStateMachine: A2DP Playing state :', KEYWORD2:'11->10',LOGTYPE:TYPE_AUDIO, PROFILE:PROFILE_A2DP, MACINCLUDE:True},
{ACTION:'suspend', KEYWORD1:'A2dpStateMachine: A2DP Playing state :', KEYWORD2:'10->11', LOGTYPE:TYPE_AUDIO, PROFILE:PROFILE_A2DP, MACINCLUDE:True},
{ACTION:'Connecting...', KEYWORD1:'HeadsetStateMachine: Connection state', KEYWORD2:'0->1', LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_HFP, MACINCLUDE:True},
{ACTION:'Connected', KEYWORD1:'HeadsetStateMachine: Connection state', KEYWORD2:'->2', LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_HFP, MACINCLUDE:True},
{ACTION:'Connect fail', KEYWORD1:'HeadsetStateMachine: Connection state', KEYWORD2:'1->0', LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_HFP, MACINCLUDE:True},
{ACTION:'disconnected', KEYWORD1:'HeadsetStateMachine: Connection state', KEYWORD2:'2->0',LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_HFP, MACINCLUDE:True},
{ACTION:'SCO connecting....', KEYWORD1:'HeadsetStateMachine: Audio state', KEYWORD2:'10->11',LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_HFP, MACINCLUDE:True},
{ACTION:'SCO connectd', KEYWORD1:'HeadsetStateMachine: Audio state', KEYWORD2:'->12',LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_HFP, MACINCLUDE:True},
{ACTION:'SCO disconnected', KEYWORD1:'HeadsetStateMachine: Audio state', KEYWORD2:'->10',LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_HFP, MACINCLUDE:True},
{ACTION:'start BLE scan', KEYWORD1:'BluetoothLeScanner: App \'', KEYWORD2:'\' startScan',LOGTYPE:TYPE_SCAN, PROFILE:PROFILE_BLE, MACINCLUDE:True},
{ACTION:'stop BLE scan', KEYWORD1:'BluetoothLeScanner: App \'', KEYWORD2:'\' stopScan', PROFILE:PROFILE_BLE},
{ACTION:'BLE turning on..', KEYWORD1:'BluetoothAdapterState: Bluetooth adapter state changed: 10-> 14', PROFILE:PROFILE_GAP},
{ACTION:'BLE only', KEYWORD1:'BluetoothAdapterState: Bluetooth adapter state changed: 14-> 15', PROFILE:PROFILE_GAP},
{ACTION:'BLE turning off', KEYWORD1:'BluetoothAdapterState: Bluetooth adapter state changed: 15-> 16', PROFILE:PROFILE_GAP},
{ACTION:'BT on', KEYWORD1:'BluetoothAdapterState: Bluetooth adapter state changed: 11-> 12', PROFILE:PROFILE_GAP},
{ACTION:'BT off', KEYWORD1:'BluetoothAdapterState: Bluetooth adapter state changed: 16-> 10', PROFILE:PROFILE_GAP},
{ACTION:'BT turning on', KEYWORD1:'BluetoothAdapterState: Bluetooth adapter state changed: 15-> 11', PROFILE:PROFILE_GAP},
{ACTION:'Connecting...', KEYWORD1:'HidService: Connection state', KEYWORD2:'0->', LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_HID, MACINCLUDE:True},
{ACTION:'Connected', KEYWORD1:'HidService: Connection state', KEYWORD2:'->2', LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_HID, MACINCLUDE:True},
{ACTION:'disconnected', KEYWORD1:'HidService: Connection state', KEYWORD2:'->0', LOGTYPE:TYPE_CONNECTION, PROFILE:PROFILE_HID, MACINCLUDE:True},
]

#pattern set block
pattern_set=[]

def load_pattern(profile, logtype):
    if verbose: print('load_pattern: profile:' + profile + ' logtype: ' + logtype)
    pattern_set.clear()
    target_pattern=raw_logcat_pattern

    for index in range(len(target_pattern)):
       if not (profile == PROFILE_ALL):
           if target_pattern[index].__contains__(PROFILE) and not (target_pattern[index][PROFILE] in profile):
               continue
       if not (logtype == TYPE_ALL):
           if target_pattern[index].__contains__(LOGTYPE) and not (target_pattern[index][LOGTYPE] in logtype):
               continue

       mPattern=pattern()
       for a, b in target_pattern[index].items():
           if a==ACTION: mPattern.action=b
           elif a==KEYWORD1: mPattern.keyword1=b
           elif a==KEYWORD2: mPattern.keyword2=b
           elif a==LOGTYPE: mPattern.logtype=b
           elif a==PROFILE: mPattern.profile=b
           elif a==MACINCLUDE: mPattern.macinclude=b
           else: print('Pattern have error type\n')
       pattern_set.append(mPattern)
       if verbose: dumpPattern(mPattern)

def dumpPattern(pattern):
    print('action:', pattern.action)
    print('keyword1:', pattern.keyword1)
    print('keyword2:', pattern.keyword2)
    print('logtype:', pattern.logtype)
    print('profile:', pattern.profile)
    print('mac included:', pattern.macinclude)

class pattern:
    action=''
    keyword1=''
    keyword2=''
    logtype=TYPE_ALL
    profile=PROFILE_A2DP
    macinclude=False

    def __init__(sef):
        pass