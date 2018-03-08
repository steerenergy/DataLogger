from paramiko.client import SSHClient

client = SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(AutoAddPolicy())
client.connect('192.168.1.106', username='pi', password='raspberry')
