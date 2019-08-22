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

        # Get List of Files
        filesList = sftp.listdir(path='/home/pi/Github/DataLogger/RPI/files/outbox')

        # Give warning if there are no files to download
        if len(filesList) <= 1:
            print("No Files found to Download")
        else:
            # Print Number of Files Found
            noFiles = "\n{} Files Found".format(len(filesList))
            print(noFiles)
            # Make it look pretty
            print("-"*(len(noFiles)-1))
            # Download all files in remote outbox folder and delete them after
            for fileName in filesList:
                # Don't download .gitkeep file or bad things happen
                if fileName != ".gitkeep":
                    # Download File
                    remotePath = '/home/pi/Github/DataLogger/RPI/files/outbox/' + fileName
                    localPath = 'files/inbox/' + fileName
                    # Print name of file being transferred
                    print("File: {}:".format(fileName))
                    # Transfer the file and give status of transfer (see printTotals func at top).
                    sftp.get(remotePath, localPath, callback=printTotals)
                    # Print Success (note this is printed on the line above
                    # due to carriage return on the above statement
                    print("Transferred: 100% - Success")

            # Give option for user to delete all files on Pi
            # This means files are not deleted if the file is taken off during logging
            option = input("Delete Files On Pi?"
                           " - IMPORTANT: Do not delete files during logger operation!\n(Y/N): ")
            if option == "Y" or option == "y":
                for fileName in filesList:
                    # Don't download .gitkeep file or bad things happen
                    if fileName != ".gitkeep":
                        # Get remote path and delete
                        remotePath = '/home/pi/Github/DataLogger/RPI/files/outbox/' + fileName
                        sftp.remove(remotePath)
                print("Successfully Deleted Files on Pi")
            elif option == "N" or option == "n":
                print("Files Not Deleted")
            else:
                print("Invalid Option - Files Not Deleted")

        # Close Connection
        sftp.close()
        transport.close()
        # Print Success
        print("\nSuccess!")

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
