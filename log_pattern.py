##--20180420--##
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

raw_bugreport_pattern=[
{SAME_LINE:False,TARGET:'Bonded devices:\n',LINE_START:'0',LINE_END:'\n',MAC_TARGET:'strip',NAME_TARGET:']', NAME_END:'\n'}
]
raw_logcat_pattern=[
{SAME_LINE:True, TARGET:'[BT] Connected to ', NAME_TARGET:'RName:', NAME_END:'\n'},
{SAME_LINE:True, TARGET:'[BT] Disconnected from ', NAME_TARGET:'RName:', NAME_END:'\n'},
]

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
