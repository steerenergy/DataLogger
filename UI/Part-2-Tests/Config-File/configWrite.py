import configparser
import uuid
logConf = configparser.ConfigParser()
timeInterval = input("What time Interval?\n")
logConf['General'] = {'language':'English','unique id': uuid.uuid4()}
logConf['Pin-Config'] = {'0A0': '20', '0A1':'ETC'}
logConf['Time-Settings'] = {'Time-Interval':timeInterval}
with open('logConf.ini', 'w') as configfile:
    logConf.write(configfile)
