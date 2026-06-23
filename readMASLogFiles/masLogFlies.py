import json
import glob
from datetime import date

def readMASLogFile(MasLogFileName, curentOnly='N'):
    'Output: logFileContent'

    defaultLogFileDir= '/opt/sas/viya/config/var/log/microanalyticservice/default'
    
    #set if we only want to write log output from today
    writeLine= True
    if curentOnly == 'Y':
        writeLine= False
        
    #get current date
    currDate= date.today().strftime("%Y-%m-%d")
    
    #get current log MAS log file
    logDirLst= glob.glob(defaultLogFileDir + '/*')
    masLogDir= {}
    for f in logDirLst:
        if f[len(defaultLogFileDir)+1 : len(defaultLogFileDir)+1 + len(MasLogFileName)] == MasLogFileName:
            masLogDir[f[len(defaultLogFileDir)+1 + len(MasLogFileName):len(f)-4]]= f
    logFileName= masLogDir[sorted(masLogDir.keys())[-1]]

    logFileLst= []
    with open(logFileName, 'r') as logFile:
        for line in logFile:
            if writeLine == False and line[0:10] == currDate:
                writeLine= True
            if writeLine: 
                logFileLst.append(line)
    
    logFileContent= json.dumps(logFileLst)

    return logFileContent
	
def readMASQKBLogFile(LogFileDir= ''):
    'Output: logFileContent'

    if LogFileDir == None:
        defaultLogFileDir= '/opt/sas/viya/config/var/log/microanalyticservice/default'
    elif len(LogFileDir) == 0:
        defaultLogFileDir= '/opt/sas/viya/config/var/log/microanalyticservice/default'
    else:
        defaultLogFileDir= LogFileDir
    MasLogFileName= 'masqkb.log'
    
    logFileName= defaultLogFileDir + '/' + MasLogFileName

    logFileLst= []
    try:
        with open(logFileName, 'r', encoding='utf-8-sig') as logFile:
            for line in logFile:
                logFileLst.append(line)
    except:
        logFileContent= 'File not found: ' + logFileName
        return logFileContent
        
    logFileContent= json.dumps(logFileLst)

    return logFileContent

def clearMASLogFile(MasLogFileName= ''):
    'Output: msg'

    msg= ''
    defaultLogFileDir= '/opt/sas/viya/config/var/log/microanalyticservice/default'
    
    #get current log MAS log file
    logDirLst= glob.glob(defaultLogFileDir + '/*')
    masLogDir= {}
    for f in logDirLst:
        if f[len(defaultLogFileDir)+1 : len(defaultLogFileDir)+1 + len(MasLogFileName)] == MasLogFileName:
            masLogDir[f[len(defaultLogFileDir)+1 + len(MasLogFileName):len(f)-4]]= f
    logFileName= masLogDir[sorted(masLogDir.keys())[-1]]

    try:
        logFile= open(logFileName, 'w')
    except:
        msg= 'File not found: ' + logFileName
        return msg

    logFile.close()

    msg= 'Cleared Log File: ' + logFileName
    
    return msg

def readMASQKBCfg():
    'Output: casaddress, casport, casuid, caspwd, logLevel, qkb'

    masConfFileName= '/opt/sas/viya/config/etc/sysconfig/microanalyticservice.conf'
    masQKBConfName= ''
    masQKBConfDic= {}
    casaddress= ''
    casport= -1
    casuid= ''
    caspwd= ''
    logLevel= -1
    qkb= ''
    try:
        with open(masConfFileName, 'r', encoding='utf-8-sig') as masConfFile:
            for line in masConfFile:
                if line.strip()[0:18] == 'export MASQKB_CFG=':
                    masQKBConfName= line.strip()[18:] + '/masqkb.cfg'
    except:
        print('File not found: ' + masConfFileName)

    try:
        with open(masQKBConfName, 'r', encoding='utf-8-sig') as masQKBConfFile:
            masQKBConfDic= json.loads(masQKBConfFile.read())
            casaddress= masQKBConfDic['casaddress']
            casport= masQKBConfDic['casport']
            casuid= masQKBConfDic['casuid']
            caspwd= '*****'
            logLevel= masQKBConfDic['logLevel']
            qkb= masQKBConfDic['qkb']
    except:
        casaddress= 'File not found: ' + masQKBConfName
        
    return casaddress, casport, casuid, caspwd, logLevel, qkb

def setMASQKBCfg(casaddress, casport, casuid, caspwd, logLevel, qkb):
    'Output: '

    masConfFileName= '/opt/sas/viya/config/etc/sysconfig/microanalyticservice.conf'
    masQKBConfName= ''
    masQKBConfDic= {}
    masQKBConfJson= ''
    try:
        with open(masConfFileName, 'r', encoding='utf-8-sig') as masConfFile:
            for line in masConfFile:
                if line.strip()[0:18] == 'export MASQKB_CFG=':
                    masQKBConfName= line.strip()[18:] + '/masqkb.cfg'
    except:
        print('File not found: ' + masConfFileName)

    try:
        with open(masQKBConfName, 'r', encoding='utf-8-sig') as masQKBConfFile:
            masQKBConfDic= json.loads(masQKBConfFile.read())
    except:
        casaddress= 'File not found: ' + masQKBConfName

    if casaddress != None:
        if len(casaddress) > 0:
            masQKBConfDic['casaddress']= casaddress
    if casport != None:
        if casport >= 0:
            masQKBConfDic['casport']= casport
    if casuid != None:
        if len(casuid) > 0:
            masQKBConfDic['casuid']= casuid
    if caspwd != None:
        if len(caspwd) > 0:
            masQKBConfDic['caspwd']= caspwd
    if logLevel != None:
        if logLevel >= 0:
            masQKBConfDic['logLevel']= logLevel
    if qkb != None:
        if len(qkb) > 0:
            masQKBConfDic['qkb']= qkb
    masQKBConfJson= json.dumps(masQKBConfDic)

    masConfFile= open(masQKBConfName, 'w')
    masConfFile.write(masQKBConfJson)
    masConfFile.close()
    return

def clearMASQKBCfg(LogFileDir= ''):
    'Output: msg'

    msg= ''
    if LogFileDir == None:
        defaultLogFileDir= '/opt/sas/viya/config/var/log/microanalyticservice/default'
    elif len(LogFileDir) == 0:
        defaultLogFileDir= '/opt/sas/viya/config/var/log/microanalyticservice/default'
    else:
        defaultLogFileDir= LogFileDir
    MasLogFileName= 'masqkb.log'
    
    logFileName= defaultLogFileDir + '/' + MasLogFileName

    try:
        logFile= open(logFileName, 'w')
    except:
        msg= 'File not found: ' + logFileName
        return msg

    logFile.close()
    msg= 'Cleared Log File: ' + logFileName
    
    return msg



