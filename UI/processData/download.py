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
        print("Getting Config(s) and CSV(s) ...")
        sftp = paramiko.SFTPClient.from_transport(transport)
        # Download all files in remote outbox folder and delete them after
        for fileName in sftp.listdir(path='/home/pi/Github/DataLogger/RPI/files/outbox'):
            if fileName != ".gitkeep":
                # Download File
                remotePath = '/home/pi/Github/DataLogger/RPI/files/outbox/' + fileName
                localPath = 'files/inbox/'+fileName
                sftp.get(remotePath, localPath)
                print("Successfully Downloaded: {}".format(fileName))
                # Delete File
                sftp.remove(remotePath)

        if len(sftp.listdir(path='/home/pi/Github/DataLogger/RPI/files/outbox')) >= 3:
            print("WARNING - Multiple CSV/Config Files have been found. "
                  "\nPlease navigate /files/inbox and ensure there is only one CSV and Config File")
        # Close Connection
        sftp.close()
        transport.close()
    except:
        print("\n ERROR: Transfer Failed - "
              "Ensure you are Connected to the same Network as the Raspberry Pi and Try Again")


if __name__ == "__main__":
    init()
