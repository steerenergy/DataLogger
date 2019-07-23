# This module grabs all CSV and Config files on the Pi's outbox folder and placing them in the UI's inbox folder.

# Uses Paramiko to connect to the Pi via ftp and download the csv and config file.
import paramiko
# Import socket for error handling
import socket


# Function called to print transfers status
def printTotals(transferred, toBeTransferred):
    # Note this doesn't display properly if run in PyCharm/Idle due to the carriage return ('/r')
    print("Transferred: {}%".format(round(transferred/toBeTransferred * 100, 2)), end="\r")


# Main download script
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
        print("Getting Config(s) and CSV(s)...")
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Give warning if there are no files to download
        if len(sftp.listdir(path='/home/pi/Github/DataLogger/RPI/files/outbox')) <= 1:
            print("No Files found to Download")
        else:
            # Download all files in remote outbox folder and delete them after
            for fileName in sftp.listdir(path='/home/pi/Github/DataLogger/RPI/files/outbox'):
                if fileName != ".gitkeep":
                    # Download File
                    remotePath = '/home/pi/Github/DataLogger/RPI/files/outbox/' + fileName
                    localPath = 'files/inbox/'+fileName
                    # Print name of file being transferred
                    print("\nTransferring: {}...".format(fileName))
                    # Transfer the file and give status of transfer (see printTotals func at top).
                    sftp.get(remotePath, localPath, callback=printTotals)
                    # Print Success
                    print("Successfully Downloaded: {}".format(fileName))
                    # Delete File if user wants to
                    # This means file is not deleted if the file is taken off during logging
                    option = input("Delete File Remotely?"
                                   "IMPORTANT: Do not delete files during logger operation!\n(Y/N): ")
                    if option == "Y" or option == "y":
                        sftp.remove(remotePath)
                        print("Successfully Deleted: {}".format(fileName))
                    elif option == "N" or option == "n":
                        print("File Not Deleted")
                    else:
                        print("Invalid Option - File Not Deleted")

        # Close Connection
        sftp.close()
        transport.close()
        # Print Success
        print("Success!")

    # If connection was unsuccessful
    except socket.error:
        print("\nERROR: Transfer Failed - "
              "Ensure you are Connected to the same Network as the Raspberry Pi and Try Again")
        # Close Connection if possible
        try:
            sftp.close()
            transport.close()
        # If the above variables haven't been assigned yet, move on
        except UnboundLocalError:
            pass
