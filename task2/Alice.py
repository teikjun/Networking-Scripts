# Alice is the sender (Client)

from socket import *
import sys
import zlib
from typing import Tuple
import signal
import math
import re


def main() -> None:
    serverName = "localhost"
    serverPort = int(sys.argv[1])
    # Create a socket 
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    # Set timeout to 50ms
    clientSocket.settimeout(0.05)
    sequenceNum = 0

    # Get input message
    inputMsg: str = sys.stdin.read()
    
    msgList = [inputMsg[i:i+32] for i in range (0, len(inputMsg), 32)]

    for currMsg in msgList:
        isDone: bool = False
        while not isDone:
            try:
                message = pack(currMsg, sequenceNum)
                clientSocket.sendto(message, (serverName, serverPort))
                ackMsg, serverAddress = clientSocket.recvfrom(512)
                (ack, valid) = unpack(ackMsg)

                if valid and (ack == sequenceNum + len(currMsg)):
                    isDone = True     
            except timeout: 
                pass
        sequenceNum += len(currMsg)

# add the sequenceNum and checksum headers
def pack(payload, sequenceNum) -> bytes:
    sequenceNumBytes = intToBytes(sequenceNum)
    payloadBytes = payload.encode()
    checksum: bytes = intToBytes(zlib.crc32(payloadBytes))
    result: bytes = sequenceNumBytes + checksum + payloadBytes
    return result

# parse the received message
def unpack(data) -> Tuple[int, bool]:
    try:
        checksum = data[:4]
        sequenceNumBytes = data[4:]
        if bytesToInt(checksum) == zlib.crc32(sequenceNumBytes):
            return (int(sequenceNumBytes), True)
        return (int(sequenceNumBytes), False)
    except:
        return (0, False)

def intToBytes(x) -> bytes:
    return x.to_bytes(4, "big")

def bytesToInt(x) -> int:
    return int.from_bytes(x, "big")


if __name__ == "__main__":
    main()
