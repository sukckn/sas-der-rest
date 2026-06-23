###################################################################
#class saslog
#class to write log information to a file
#Crerate a saslog object to create a log file
#use method out() to write log information
#you can set a log level to pass out more or less information. 
#    The default log level is 0 to write all info to the log file
###################################################################
import sys
from datetime import datetime

class saslog:
    log= None
    logFile= None
###################################################################
#Constructor
#The constructor create the log file. 
#Parameters:
#    logLevel=0 - Control how much information is pass out.
#    logFileName=None - Logfile name. If not supplied name is 'saspy.log'.
#    logDir=None - LogFile directory. If not suppied log info will be written to 
#                  MAS logFile directory. Make sure sufficiant write permission for
#                  the directoy exists.
###################################################################
    def __init__(self, logLevel=0, logFileName=None, logDir=None):
        if logFileName == None:
            logFileName= "saspy.log"
        if logDir == None:
            logDir= "/opt/sas/viya/config/var/log/microanalyticservice/default/"
        else:
            logDir+= "/"
                
        self.logFile= logDir + logFileName
        try:
            self.log= open(self.logFile, "a")
        except Exception as err:
            print(err)
            sys.exit()
            
        self.logLevel= logLevel
        #switch to output log also to the screen
        self.screen= False
        return
###################################################################
#setLogLevel() - Set log level
#Parameters:
#    logLevel - Set log level to control output. You can change the log level 
#               after the object has been created.
###################################################################
    def setLogLevel(self, logLevel):
        self.logLevel= logLevel
        return

###################################################################
#setStdout() - output log into also to screen
#Parameters:
#    switch - Set to also output to stdout. 
###################################################################
    def setStdout(self, switch=True):
        self.screen= switch
        return
###################################################################
#getLogLevel() - Set log level
#Parameters:
###################################################################
    def getLogLevel(self):
        return self.logLevel
###################################################################
#out() - Write log information
#Parameters:
#    msg - Information to be logged
#    logLevel - At wich level should msg be passed out.
###################################################################
    def out(self, msg, logLevel=0):
        if self.logLevel >= logLevel:
            #we can also output the msg to the screen. 
            if self.screen == True:
                print(msg)
            #msg will be pass out including timestamp and log level info
            self.log.write("%s [%04d] %s\n" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f"), logLevel, msg))
            self.log.flush()
        return
###################################################################
#getLogName() - return the log file name
###################################################################
    def getLogName(self):
        return self.logFile
###################################################################
#close() - close the log file
###################################################################
    def close(self):
        if self.log != None:
            self.log.close()
        return
###################################################################
#Destructor
###################################################################
    def __del__(self):
        self.close()
        return