import paramiko
paramiko.util.log_to_file('paramiko.log')

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

filepath = 'Github/DataLogger/RPI/voltage.csv'
localpath = 'voltage.csv'
sftp.get(filepath, localpath)

# Upload

#filepath = '/home/foo.jpg'
#localpath = '/home/pony.jpg'
#sftp.put(localpath, filepath)

# Close

sftp.close()
transport.close()

print("Done")
