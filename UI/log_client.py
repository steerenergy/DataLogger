#Requries server application to be open in order to work.
import paramiko
import configparser
import uuid
import socket
import time

#User Questions
timeInterval = input("What time Interval?\n")

#Write Config Stage
print("Writing Config...")
logConf = configparser.ConfigParser()

logConf['General'] = {'language':'English','unique id': uuid.uuid4()}
#Temp Test Data
logConf['Pin-Config'] = {'0A0': '20', '0A1':'ETC'}
#Important Bit
logConf['Time-Settings'] = {'Time-Interval':timeInterval}
with open('logConf.ini', 'w') as configfile:
    logConf.write(configfile)

#Upload File stage
print("Uploading Config File...")
try:
    # Open a transport
    host = "raspberrypi"
    port = 22
    transport = paramiko.Transport((host, port))
    # Auth
    password = "raspberry"
    username = "pi"
    transport.connect(username = username, password = password)
    # Go!
    sftp = paramiko.SFTPClient.from_transport(transport)
    # Upload
    remotePath = '/home/pi/Github/DataLogger/RPI/logConf.ini'
    localPath = 'logConf.ini'
    sftp.put(localPath, remotePath)
    sftp.close()
    transport.close()


    #Logging Trigger Stage
    print("Triggering Logging...")
    TCP_IP = 'raspberrypi'
    TCP_PORT = 5005
    BUFFER_SIZE = 1024
    MESSAGE = "Read-Config"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE.encode())

    time.sleep(5)
    data = s.recv(BUFFER_SIZE)
    print(data.decode())

finally:
    # Close All
    sftp.close()
    transport.close()
    s.close()
