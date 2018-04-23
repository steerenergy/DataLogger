import sys
sys.path.append("..")
import common
import paramiko

def init():
    try:
        print("\nPreparing to Transfer...")
        # Open a transport
        host = "raspberrypi"
        port = 22
        transport = paramiko.Transport((host, port))
        # Auth
        password = "raspberry"
        username = "pi"
        transport.connect(username = username, password = password)
        # Go!
        print("Getting Config and CSV...")
        sftp = paramiko.SFTPClient.from_transport(transport)
        # Upload
        remotePath = '/home/pi/Github/DataLogger/RPI/raw.csv'
        localPath = 'raw.csv'
        sftp.get(remotePath, localPath)
        remotePath = '/home/pi/Github/DataLogger/RPI/logConf.ini'
        localPath = 'logConf.ini'
        sftp.get(remotePath, localPath)
        print("Success")
    finally:
        sftp.close()
        transport.close()

if __name__ == "__main__":
    init()