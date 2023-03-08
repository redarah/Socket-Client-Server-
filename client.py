
import socket
import sys
from threading import Thread


# creat a socket for the client 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#creat the authentifaction to connect with the serverv
try:
    servername = sys.argv[2]
    tcp_port = int(sys.argv[3])
    name = sys.argv[1]
except Exception as e:

    print(e)
    input()
    print('>Wrong input  please enter : [client.py username] [IP] [PORT]')
#tcp_port = 5555

#create TCP connection socket for server and port  
try:
    client_socket.connect((servername, tcp_port))
    #client_socket.send(name)
    client_socket.send(str(name).encode())
except:
    CLIENT_CANNOT_CONNECT = "Unable to connect to {0}:{1}".format(servername,tcp_port)
    print CLIENT_CANNOT_CONNECT 
    exit(0)


def receive():
    while 1:
        try:
            message = client_socket.recv(200).decode()
            print message
        except:
            CLIENT_SERVER_DISCONNECTED = "Server at {0}:{1} has disconnected".format(servername,tcp_port)
            print CLIENT_SERVER_DISCONNECTED
            
            client_socket.close()
            exit(0)

        CLIENT_WIPE_ME = "\r    "
        #we use strip to remove the blank space 
        print (CLIENT_WIPE_ME +"\r"+message.decode().strip())
        

        
       


def write():
    while 1 :        
        #mess = raw_input("[Me]: ")
        CLIENT_MESSAGE_PREFIX = "[Me] "
        mess = '{}'.format( raw_input(CLIENT_MESSAGE_PREFIX))
        client_socket.send(str(mess).encode())
        


receive_thread = Thread(target = receive)
receive_thread.start()

write_thread = Thread(target = write)
write_thread.start()