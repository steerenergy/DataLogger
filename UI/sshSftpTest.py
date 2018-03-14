import paramiko
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('raspberrypi',username='pi',password='raspberry')

try:
    print("SSH/SFTP Test")
    input("Press Enter to Begin Logging...")

    #stdin, stdout and stderr and file like objects and require file methods to be used
    stdin,stdout,stderr = ssh.exec_command("python Github/DataLogger/RPI/logger.py")
    print(stdout.readlines())

    input("Press Enter to Stop...")
    stdin,stdout,stderr = ssh.exec_command("(0x1a)")
    print(stdout.readlines())

finally:
    ssh.close()
