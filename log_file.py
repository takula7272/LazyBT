##--20180423--##
import zipfile
import os
import config

debug=config.debug

#bugreport file name block
bugreport_filename=[]
#logcat file name block
logcat_filename=[]
#asusevent file name block
asuseventlog_filename=[]

def parse_logfile_name(inputdir='.'):
    target_bugreport=False
    for dirPath, dirNames, fileNames in os.walk(inputdir):
        for f in fileNames:
            if 'bugreport' in f and 'zip' in f:
                with zipfile.ZipFile(os.path.join(dirPath, f),'r') as myzip:
                    unzippath=dirPath+'/bugreport'
                    myzip.extractall(path=unzippath)
                    myzip.close()
                bugreport_filename.clear()
                bugreport_filename.append(unzippath+'/'+f[:-3]+'txt')
                if debug: print(unzippath+'/'+f[:-3]+'txt')
                target_bugreport=True
            elif 'bugreport' in f and 'png' not in f and target_bugreport==False:
                if debug:print(os.path.join(dirPath, f))
                bugreport_filename.append(os.path.join(dirPath, f))
            elif 'logcat.txt' in f and 'asdf' not in f:
                if debug:print(os.path.join(dirPath, f))
                logcat_filename.append(os.path.join(dirPath, f))
            elif 'ASUSEvtlog' in f:
                if debug:print(os.path.join(dirPath, f))
                asuseventlog_filename.append(os.path.join(dirPath, f))

    if not (len(bugreport_filename) or len(logcat_filename) or len(asuseventlog_filename)):
        return False
    else:
        return True

def parse_logcat_file_name(inputdir='.'):
    for dirPath, dirNames, fileNames in os.walk(inputdir):
        for f in fileNames:
            if 'logcat.txt' in f and 'asdf' not in f:
                if debug:print(os.path.join(dirPath, f))
                logcat_filename.append(os.path.join(dirPath, f))

    if not len(logcat_filename):
        return False
    else:
        return True

