# This module grabs all CSV and Config files on the logger and saves them to /files/inbox ready to be processed

# Uses Paramiko to connect to the Pi via FTP and download the csv and config file.
import paramiko
# Import socket for error handling
import socket
# Import comms module for dealing with hostname of logger selection
import comms


# Function called to print transfers status
def printTotals(transferred, toBeTransferred):
    # Note this doesn't display properly if run in PyCharm/IDLE due to the carriage return ('/r')
    print("Transferred: {}%".format(round(transferred/toBeTransferred * 100, 2)), end="\r")


# Main download script
def init():
    try:
        # Set Directory of Remote and Local Folders
        remoteFolder = '/home/pi/Github/DataLogger/RPI/files/outbox/'
        localFolder = 'files/inbox/'

        print("\nPreparing to Download From: '{}'...".format(comms.loggerHostname.host))

        # Open a transport + import hostname
        port = 22
        transport = paramiko.Transport(comms.loggerHostname.host, port)

        # Auth
        password = "raspberry"
        username = "pi"
        transport.connect(username=username, password=password)

        # Go!
        print("Getting Config(s) and CSV(s)...")
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Get List of Files
        filesList = sftp.listdir(path=remoteFolder)

        # Remove .gitkeep file from list (we don't want to download/delete it)
        if ".gitkeep" in filesList:
            filesList.remove(".gitkeep")

        # Give warning if there are no files to download
        if len(filesList) <= 0:
            print("No Files found to Download")
        else:
            # Print Number of Files Found
            noFiles = "\n{} Files Found".format(len(filesList))
            print(noFiles)
            # Make it look pretty
            print("-"*(len(noFiles)-1))
            # Download all files in remote outbox folder and delete them after
            for fileName in filesList:
                # Download File
                remotePath = remoteFolder + fileName
                localPath = localFolder + fileName
                # Print name of file being transferred
                print("File: {}:".format(fileName))
                # Transfer the file and give status of transfer (see printTotals func at top).
                sftp.get(remotePath, localPath, callback=printTotals)
                # Print Success (note this is printed on the line above
                # due to carriage return on the above statement
                print("Transferred: 100% - Success")

            # Give option for user to delete all files on Pi
            # This means files are not deleted if the file is taken off during logging
            # Files should be deleted in all other circumstances
            option = input("Delete Files On Logger?"
                           " - IMPORTANT: Do not delete files during logger operation!\n(Y/N): ")
            if option == "Y" or option == "y":
                for fileName in filesList:
                    # Get remote path and delete
                    remotePath = remoteFolder + fileName
                    sftp.remove(remotePath)
                print("Successfully Deleted Files on Logger")
            elif option == "N" or option == "n":
                print("Files Not Deleted")
            else:
                print("Invalid Option - Files Not Deleted")
            # Print Success
            print("\nSuccess! - Files Downloaded to: '{}'"
                  "\nNOTE: You'll need to 'Convert Data' before the data can be processed\n".format(localFolder))

        # Close Connection
        sftp.close()
        transport.close()

    # If connection was unsuccessful
    except (socket.error, paramiko.SSHException) as e:
        print("ERROR: Failed To Download Files From: '{}' - "
              "Ensure you are Connected to the same Network as the Logger and Try Again"
              .format(comms.loggerHostname.host))
        # Print Error Info
        print(e)
        # Close Connection if possible
        try:
            sftp.close()
            transport.close()
        # If the above variables haven't been assigned yet, move on
        except UnboundLocalError:
            pass
