from socket import *

serverName= 'localhost'
serverPort= 8080

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
while True:
    message = input('Enter a message:')
    clientSocket.send(message.encode())
    receivedMsg= clientSocket.recv(4096)
    print('from server:', receivedMsg.decode())    
    if message == "close":
       clientSocket.close()
       break

