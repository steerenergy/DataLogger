import configparser

#Initial Import
def init():
    global config
    config = configparser.ConfigParser()
    config.read('logConf.ini')
    generalImport()
    inputImport():

#Import General Settings - for now as Global variables
def generalImport():
    global generalSettings
    generalSettings = {}
    for key in config['General']:
        generalSettings[key] = config['General'][key]
    
#Import Input Settings
def inputImport():
        for key in config['General']:
        generalSettings[key] = config['General'][key]
            for key in config['General']:
                generalSettings[key] = config['General'][key]  

#Temp testing Code

if __name__ == "__main__":
    init()
