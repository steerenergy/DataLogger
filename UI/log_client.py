#Requries server application to be open in order to work.
import paramiko
import ConfigParser
import uuid
import socket

#Write Config Stage
logConf = configparser.ConfigParser()
timeInterval = input("What time Interval?\n")
logConf['General'] = {'language':'English','unique id': uuid.uuid4()}
#Temp Test Data
logConf['Pin-Config'] = {'0A0': '20', '0A1':'ETC'}
#Important Bit
logConf['Time-Settings'] = {'Time-Interval':timeInterval}
with open('logConf.ini', 'w') as configfile:
    logConf.write(configfile)

#Upload File stage
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
    filepath = '/home/pi/Github/DataLogger/RPI/logConf.ini'
    localpath = 'C:/Users/Seb/Desktop/logConf.ini'
    sftp.put(localpath, filepath)
    sftp.close()
    transport.close()

#Logging Trigger Stage

TCP_IP = 'raspberrypi'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Read-Config"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE.encode())
data = s.recv(BUFFER_SIZE)
print("received data:", data.decode())





finally:
    # Close All
    print("Done!")
    sftp.close()
    transport.close()
    s.close()
