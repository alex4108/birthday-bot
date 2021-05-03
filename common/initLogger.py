import logging
import os

'''
Gets the log level from environment config, or falls back to defaults otherwise
'''
def getLogLevel():

    logLevel = os.environ.get("LOG_LEVEL")

    if logLevel != None and logLevel != "":

        return logLevel

    elif os.environ.get("ENV") == "LIVE" or os.environ.get("ENV") == "TEST":

        logLevel = logging.INFO
        
    else:

        logLevel = logging.INFO
    
    return logLevel

'''
    Retrieves a logger that was previously created with name, and sets the log level
'''
def init(name):
    
    try:
        
        logging.getLogger(name).setLevel(getLogLevel())

    except Exception as e:

        print("FATAL failed to initialize " + name + " logger.")

        print(str(e))

        exit(1)

'''
    Creates a logger with a given name, and sets the default log level
'''
def create(name):         
    
    if name is None:

        print("FATAL must include name with getLogger()")
    
        return 1

    name = str(name)

    try:
        
        log = logging.basicConfig(level=getLogLevel())

        log = logging.getLogger(name)

    except Exception as e:

        print("FATAL failed to create " + name + " logger.")

        print(str(e))

        exit(1)

    return log