###############################################
# This skeleton program is prepared for weak  #
# and average students.                       #
# If you are very strong in programming. DIY! #
# Feel free to modify this program.           #
###############################################

# Final Submission
# Alice knows Bob's public key
# Alice sends Bob session (AES) key
# Alice receives messages from Bob, decrypts and saves them to file

import socket
import sys
import pickle
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random

from AESCipher import AESCipher

# Check if the number of command line argument is 2
if len(sys.argv) != 2:
    exit("Usage: python3 Alice.py <port>")
else:
    name, port = sys.argv


def main() -> None:
    # read Bob's public key from file
    # key is stored using RSA.exportKey and must
    # be read with the respective counterpart
    pub_key = read_public_key()

    # generate AES key using the supplied AESCipher class
    # by providing a 32-byte random string as the password (key)
    key = generate_random_key()

    # encrypt session key using RSA PKCS1_OAEP
    # because RSA can only encode strings and numbers
    # we only need to encode and send the 32-byte random password
    rsaCipher = PKCS1_OAEP.new(pub_key)
    sessionKey = rsaCipher.encrypt(key)

    # create socket
    serverName = 'localhost'
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect( (serverName, int(port)) )

    #clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #clientSocket.connect(int(port));
    
    # send the session key
    send_session_key(clientSocket, sessionKey)

    # receive the messages
    receive_messages(clientSocket, key)


def read_public_key():
    # read private key from file
    with open("bob-python.pub", "r") as f:
        pub_key = RSA.importKey(f.read())
    return pub_key


def generate_random_key():
    # generate a password aka key
    key = Random.get_random_bytes(32)
    return key


def send_session_key(clientSocket, sessionKey):
    pickledSessionKey = pickle.dumps(sessionKey)
    clientSocket.send(pickledSessionKey)

def receive_messages(clientSocket, key) -> None:
    # because each line is sent by pickling
    # it might be better to read from the socket
    # as a stream and let pickle do its job
    cipher = AESCipher(key)
    
    fileObj = clientSocket.makefile(mode="b")

    with open('msgs.txt', 'wb') as outFile:
        for i in range(0, 10):
            decryptedMessage = decryptMessage(cipher, fileObj)
            outFile.write(decryptedMessage)

def decryptMessage(cipher, message):
    message = pickle.load(message)
    decryptedMessage = cipher.decrypt(message)
    return decryptedMessage

main()
