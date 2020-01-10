from socket import *

serverPort= 2105
serverSocket= socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('Server is ready to receive message')

while True:
    connectionSocket, clientAddr = serverSocket.accept()
    message = connectionSocket.recv(2048)
    modifiedMessage = message.upper()
    connectionSocket.send(modifiedMessage)
    connectionSocket.close()