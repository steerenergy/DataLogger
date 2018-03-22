import configparser
logConf = configparser.ConfigParser()
logConf.read('logConf.ini')
print(logConf.sections())
print("{time} Second(s)".format(time = logConf['Time-Settings']['time-interval']))
