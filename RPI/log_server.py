import socket
import configparser
import time


#TCP_IP line represents which network interface on the pi to use. It is not for restricting incoming messages
TCP_IP = ''
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

print("Server Start \n")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print('Connection address:', addr)

    
    while True:
        data = conn.recv(BUFFER_SIZE)
        print("received data:", data.decode())
        if data.decode() == "Read-Config":
            print("Reading Config")
            conn.sendall("Reading Config File".encode())
            logConf = configparser.ConfigParser()
            logConf.read('logConf.ini')
            conn.sendall("Time Interval is {} seconds".format(logConf['Time-Settings']['time-interval']).encode())
            #time.sleep(0.5)
            conn.sendall("Done".encode())
            data = "".encode()
        if data.decode() == "Stop-Log":
            print("Stopping")
            conn.sendall("Stopping".encode())
            time.sleep(0.5)
            conn.sendall("Done".encode())
            data = "".encode()
        if data.decode() == "Close":
            break
        else:
            pass
        time.sleep(0)

finally:
    conn.close()
    print("Closed")
