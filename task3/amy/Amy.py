###############################################
# This skeleton program is prepared for weak  #
# and average students.                       #
# If you are very strong in programming. DIY! #
# Feel free to modify this program.           #
###############################################

# Final Submission
# Amy receives Bryan's public key
# Amy sends Bryan's session (AES) key
# Amy receives messages from Bryan, decrypts and saves them to file

import socket
import sys
import pickle
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import MD5

from AESCipher import AESCipher

# Check if the number of command line argument is 2
if len(sys.argv) != 2:
    exit("Usage: python3 Alice.py <port>")
else:
    name, port = sys.argv


def main() -> None:
    # create socket
    serverName = 'localhost'
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, int(port)))
    # verify signature
    pub_key = receive_public_key(clientSocket)
    # break if the public key received is invalid
    if pub_key is None:
        return None

    # generate AES key using the supplied AESCipher class
    # by providing a 32-byte random string as the password (key)
    key = generate_random_key()

    # encrypt session key using RSA PKCS1_OAEP
    # because RSA can only encode strings and numbers
    # we only need to encode and send the 32-byte random password
    rsaCipher = PKCS1_OAEP.new(pub_key)
    sessionKey = rsaCipher.encrypt(key)

    # clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # clientSocket.connect(int(port));

    # send the session key
    send_session_key(clientSocket, sessionKey)

    # receive the messages
    receive_messages(clientSocket, key)

def receive_public_key(clientSocket):
    fileObj = clientSocket.makefile(mode="b")
    pub_key = pickle.load(fileObj)
    signature = pickle.load(fileObj)
    
    berisignKey = read_berisign_key()
    md5 = MD5.new()
    md5.update("bryan".encode())
    md5.update(pub_key)
    signer = PKCS1_PSS.new(berisignKey)
    try:
        signer.verify(md5, signature)
    except ValueError:
        print("Does not match")
        return None
    return RSA.importKey(pub_key)

def read_berisign_key():
    # read private key from file
    with open("berisign-python.pub", "r") as f:
        berisignKey = RSA.importKey(f.read())
    return berisignKey

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
