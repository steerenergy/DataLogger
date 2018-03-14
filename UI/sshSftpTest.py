import paramiko
import time

paramiko.util.log_to_file('paramiko.log')

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('raspberrypi',username='pi',password='raspberry')

try:
    print("SSH/SFTP Test")

    #Start log
    input("Press Enter to Begin Logging...")
    #stdin, stdout and stderr and file like objects and require file methods to be used
    stdin,stdout,stderr = ssh.exec_command("python Github/DataLogger/RPI/logger.py")
    #for line in stdout:
        # Process each line in the remote output
        #print(line)
    time.sleep(0.3)
    stdin,stdout,stderr = ssh.exec_command("1")
    for line in stdout:
        # Process each line in the remote output
        print(line)

    #Stop Log
    input("Press Enter to Stop...")
    stdin,stdout,stderr = ssh.exec_command("(0x1a)")
    for line in stdout:
        # Process each line in the remote output
        print(line)


    #Grab data
    input("Press Enter to Grab Data...")
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

    # Download

    filepath = '/home/pi/Github/DataLogger/RPI/voltage.csv'
    localpath = 'C:/Users/Seb/Desktop/voltage.csv'
    sftp.get(filepath, localpath)

finally:
    # Close All
    print("Done!")
    sftp.close()
    transport.close()
    ssh.close()
