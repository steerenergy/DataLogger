import paramiko
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('raspberrypi',username='pi',password='raspberry')

#stdin, stdout and stderr and file like objects and require file methods to be used
stdin,stdout,stderr = ssh.exec_command("ls /")
print(stdout.readlines())
ssh.close()
