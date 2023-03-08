
import socket
from threading import Thread


class Server:
    def __init__(self,servername,port,) :
     self.serverport= port
     self.servername =servername
     #creat a tcp welcoming socket 
     self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     self.server.bind((self.servername,self.serverport))
     #server become listning
     self.server.listen(5)
     print ">The server is on ."
     self.clients={}
     self.channels={}
     print ">Starting receiver..."
     self.receive()

    def broadcast(self,channel,message):
        for client in self.channels[channel]:
                    self.channels[channel][client].send(message)

    def receive(self):

        while True:
            cs,addr = self.server.accept()
            client_connected = cs.recv(200).decode()
            print 'A new client was connect with username : '+ client_connected +'\n'
            cs.send(('Hello '+ client_connected + ',we are very happy to count you with us !! ').encode())
            self.clients[client_connected]=cs
            # we iniatialize the threat and run it by telling him to execute the handleConnection function and giv
            # #and the argument given to the thread were the connection with the client and the value we incriment 
            t = Thread(target = self.handleConnection, args = (cs,str(client_connected)))
            #we start the thhread 
            t.start()

    def handleConnection(self,client,username):
     currentChannel=None
     inAChanel=False
     client.send("(Server) Make sure to use space between command and channel".encode())
     while True:
        answer = client.recv(200).decode()
        print (username+">New message from " +" : "+answer)
        var = answer.split(" ")
        first = (var[0])[0]
        SERVER_CLIENT_LEFT_CHANNEL = "{0} has left".format(username) 
        if(var[0] == "/join" ):
            SERVER_JOIN_REQUIRES_ARGUMENT = "/join command must be followed by the name of a channel to join."
            if(len(answer)<6):
                client.send((SERVER_JOIN_REQUIRES_ARGUMENT).encode())
            join_Chanel = var[1] 
            SERVER_CLIENT_JOINED_CHANNEL = "{0} has joined".format(username)
            SERVER_NO_CHANNEL_EXISTS = "No channel named {0} exists. Try '/create {0}'?".format(join_Chanel)
            
            

            if(join_Chanel in self.channels):
                if currentChannel!='' and not(currentChannel is None) and currentChannel !=join_Chanel:
                    print('>removing (Remove First to add after) '+username + ' from channel :'+str(currentChannel))
                    self.channels[currentChannel].pop(username)
                    inAChanel=False
                    currentChannel=''
                    self.broadcast(currentChannel,SERVER_CLIENT_LEFT_CHANNEL)
                elif currentChannel !=join_Chanel:
                    print('>adding '+username + ' to channel :'+join_Chanel)
                    self.channels[join_Chanel][username]=self.clients[username]
                    currentChannel=join_Chanel
                    inAChanel=True
                    print('>Added '+username + ' to channel :'+join_Chanel)
                    self.broadcast(currentChannel,SERVER_CLIENT_JOINED_CHANNEL)
            else:
                client.send((SERVER_NO_CHANNEL_EXISTS).encode())
                

                

        elif(var[0] == "/create"):
            SERVER_CREATE_REQUIRES_ARGUMENT ="/create command must be followed by the name of a channel to create"
            if(len(answer)<9):
                client.send((SERVER_CREATE_REQUIRES_ARGUMENT).encode())
            creat_chanel= var[1] 
            SERVER_CHANNEL_EXISTS = "Room {0} already exists, so cannot be created.".format(currentChannel)
            
            
            if (creat_chanel in self.channels):
                client.send((SERVER_CHANNEL_EXISTS).encode())
            else :
                #we check if the client is connected to another chanel 
                if currentChannel!='' and not(currentChannel is None):
                    print('>removing '+username + ' from channel :'+str(currentChannel))
                    self.channels[currentChannel].pop(username)
                    inAChanel=False
                    currentChannel=''
                    self.broadcast(currentChannel,SERVER_CLIENT_LEFT_CHANNEL)

                print('>adding '+username + ' to channel :'+creat_chanel)
                self.channels[creat_chanel]={}
                self.channels[creat_chanel][username]=self.clients[username]
                inAChanel=True
                currentChannel=creat_chanel
                print('>Added '+username + ' to channel :'+creat_chanel)



        elif ( var[0] == "/list"):
            channels=''
            for ch in self.channels:
                channels+='>'+ch+'\n'
            client.send(('>The current channel that are available are : '+str(channels)).encode())
        
        
        elif (first == "/" and var[0] != "/list" and var[0] != "/creat" and var[0] != "/join"):
            SERVER_INVALID_CONTROL_MESSAGE = "{} is not a valid control message. Valid messages are /create, /list, and /join.".format(answer)
            client.send((SERVER_INVALID_CONTROL_MESSAGE).encode())

       
        
        elif  inAChanel:
            print '====='
            self.broadcast(currentChannel,answer)
        #print(inAChanel)
        
        elif not (inAChanel):
            SERVER_CLIENT_NOT_IN_CHANNEL ="Not currently in any channel. Must join a channel before sending messages."
            client.send((SERVER_CLIENT_NOT_IN_CHANNEL).encode())


            




serv=Server('0.0.0.0',5555)




