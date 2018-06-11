# Uses Paramiko to connect to the Pi via ftp and download the csv and config file.
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
        transport.connect(username=username, password=password)
        # Go!
        print("Getting Config and CSV...")
        sftp = paramiko.SFTPClient.from_transport(transport)
        # Download all files in remote outbox folder
        for fileName in sftp.listdir(path='/home/pi/Github/DataLogger/RPI/files/outbox'):
            remotePath = '/home/pi/Github/DataLogger/RPI/files/outbox/' + fileName
            localPath = 'files/inbox/'+fileName
            sftp.get(remotePath, localPath)
        if len(sftp.listdir(path='/home/pi/Github/DataLogger/RPI/files/outbox')) > 2:
            print("\nWARNING - Multiple CSV/Config Files have been found. ")
        print("Success!")
    finally:
        sftp.close()
        transport.close()


if __name__ == "__main__":
    init()
