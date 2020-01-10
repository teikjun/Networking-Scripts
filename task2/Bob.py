# Bob is the receiver (Server)

from socket import *
import sys
import zlib
from typing import Tuple

def main() -> None:
    # Read port number from command line
    serverPort = int(sys.argv[1])
    # Create a socket
    serverSocket = socket(AF_INET, SOCK_DGRAM) 
    # Bind socket to port number
    serverSocket.bind(("", serverPort))

    expectedSequenceNum = 0

    while True:
        data, clientAddress = serverSocket.recvfrom(512)
        (message, sequenceNum, valid) = unpack(data)
        if (sequenceNum != expectedSequenceNum):
            ackMsg = pack(str(expectedSequenceNum))
            serverSocket.sendto(ackMsg, clientAddress)
            continue
        if valid:
            print(message, end="", flush=True)
            expectedSequenceNum += len(message)
        ackMsg = pack(str(expectedSequenceNum));
        serverSocket.sendto(ackMsg, clientAddress)

# add the sequenceNum and checksum headers
def pack(sequenceNum) -> bytes:
    sequenceNumBytes = sequenceNum.encode()
    checksum: bytes = intToBytes(zlib.crc32(sequenceNumBytes))
    result: bytes = checksum + sequenceNumBytes
    return result

# parse the received message into (message, sequenceNum, valid)
def unpack(data) -> Tuple[str, int, bool]:
    try:
        sequenceNum = bytesToInt(data[:4])
        checksum = bytesToInt(data[4:8])
        messageBytes = data[8:]
        newChecksum = zlib.crc32(messageBytes)
        message: str = messageBytes.decode()
        if newChecksum == checksum:
            return (message, sequenceNum, True)
        return (message, sequenceNum, False)
    except:
        return ("", 0, False)

def intToBytes(x) -> bytes:
    return x.to_bytes(4, "big")

def bytesToInt(x) -> int:
    return int.from_bytes(x, "big")        

if __name__ == "__main__":
    main()
