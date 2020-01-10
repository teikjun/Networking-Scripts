from socket import *;
#from typing import List;
import sys;
#import time;
import struct;
#import cProfile

# Server should:
# 1. bind() to the input port in command argument
# 2. listen() to the socket and accept() a new connection
# 3. Parse and respond to client request(s) sequentially, by using recv() and send() for socket I/O
# 4. Go back to 2 after client disconnects 

# bind() welcoming socket to input port
serverPort: int = int(sys.argv[1]);
serverSocket = socket(AF_INET, SOCK_STREAM);
serverSocket.bind(("", serverPort));
# listen() to the socket
serverSocket.listen(1);
# initialize variables needed for response
httpMethod: str = ""; 
path: str = "";
contentHeader: str = "";
contentLen: str = ""; 
content: bytes = b"";
contentBA: bytearray = bytearray(b"");
complete: bool = False; 
stage: int = 0;
contentCount = 0;
messageCount = 0;
upperMethod = "";
contentList = [];
intContentLen = 0;

# dictionary 
keyValueStore = {};

def main():    
    global complete, messageCount;
    while True:
        #start = time.time();
        #print("Server is ready to receive message");
        # accept() a new connection
        connectionSocket, clientAddr = serverSocket.accept();    
        #print("connectionSocket accepted");
        # persist connection until client disconnects 

        while True:
            # parse client message
            byteMessage = connectionSocket.recv(524288);
            messageLen = len(byteMessage);
            #print("message length", messageLen); 
            #print(byteMessage);
            # close connection if message length is 0
            if messageLen == 0:     
                #print("no message, closing this connectionSocket now");
                connectionSocket.close();
                break;
            # parse the message one letter at a time, send a response as soon as a request is done
            byteList = struct.unpack(str(messageLen) + "c", byteMessage);  
            for currentElement in byteList:
                parseOne(currentElement);
                if complete == True:
                    #printAll();
                    # response with status and status description, and value (if needed)
                    response: bytes = responseHandler();
                    #print("response:", response);
                    # respond to client
                    connectionSocket.send(response);
                    # reset variables after each response to a complete request
                    reset();
                    #end = time.time();
                    #print("time", time.time() - start);
            #printAll();
            #print("time", time.time() - start);
            
def isComplete(stage: int) -> bool:
    return (stage == 3 and (upperMethod == "GET" or upperMethod == "DELETE")) or (stage == 5 and int(contentLen) == 0);

def parseOne(currentElement: bytes):
    global stage, httpMethod, path, complete, contentHeader, upperMethod, contentList, intContentLen;
    #print(currentElement);
    if currentElement == b" " and stage != 5:
        stage += 1;
        #print("stage: " + str(stage));
        #print("method", httpMethod);
        if isComplete(stage):
            complete = True;
        if stage == 1:
            upperMethod = httpMethod.upper();
        # after finishing buffering contentHeader, check if we got the correct header field
        # if not, empty the contentHeader and skip the next header field
        if stage == 3:
            contentHeader = "".join(contentList);
            if contentHeader.upper() != "CONTENT-LENGTH":
                contentHeader = "";
                contentList = [];
                stage = 10; 
        if stage == 4:
            intContentLen = int(contentLen);
        # after skipping the next header field, go back to buffering contentHeader
        elif stage == 11:
            stage = 2;
        # after skipping the next two header field, go back to stage 4. 
        # Proceed to stage 5 only when next token is a whitespace (double whitespace)
        elif stage == 14: 
            stage = 4;
    else:
        if stage == 0: 
            httpMethod += currentElement.decode();
        elif stage == 1:
            path += currentElement.decode();
        elif upperMethod== "POST":
            postParser(currentElement);
            #elif httpMethod.upper() == "GET" or httpMethod.upper() == "DELETE":
            #    if stage != 2:
            #        print("Error: This stage is invalid for method GET or DELETE");
            #else: 
            #    print("Error: httpMethod is invalid: " + httpMethod);

def postParser(currentElement: bytes): 
    global stage, contentHeader, contentLen, intContentLen, content, contentCount, complete, contentBA, contentList, intContentLen;
    if stage == 2: 
        contentList.append(currentElement.decode());
    elif stage == 3:    
        contentLen += currentElement.decode();
    elif stage == 4:
        # expected whitespace, but now parsing useless header which will be followed by another useless header
        # use stage 12 and 13 to skip the 2 useless headers
        stage = 12;
    elif stage == 5:
        if contentCount < intContentLen: 
            contentBA += currentElement;
            contentCount += 1;
            if contentCount == intContentLen:
                content = bytes(contentBA);
                complete = True;
    #elif stage == 10 or stage == 12 or stage == 13: 
    #    pass;
    #elif stage == 6:
    #    print("Error: This stage is invalid for method POST");

def responseHandler() -> bytes: 
    #prefix: str = path[:5];
    key: str = path[5:];
    if upperMethod == "POST":
        return postHandler(key);
    elif upperMethod == "GET":
        return getHandler(key);
    elif upperMethod == "DELETE":
        return deleteHandler(key);
    else:
        #print("Error: invalid httpMethod");
        return b"";
        
def postHandler(key) -> bytes:
    keyValueStore[key] = content;
    return b"200 OK  ";

def getHandler(key) -> bytes:
    value = keyValueStore.get(key);
    if value == None:
        return b"404 NotFound  ";
    elif isinstance(value, bytes):
        valueLen = str(len(value)).encode();
        result = bytearray(b"200 OK Content-Length ")
        result.extend(valueLen);
        result.extend(b"  ");
        result.extend(value);
        return bytes(result);
    else:
        return b"";

def deleteHandler(key) -> bytes:
    value = keyValueStore.pop(key, None);
    if value == None:
        return b"404 NotFound  ";
    elif isinstance(value, bytes):
        valueLen = str(len(value)).encode();
        result = bytearray(b"200 OK Content-Length ")
        result.extend(valueLen);
        result.extend(b"  ");
        result.extend(value);
        return bytes(result);
    else:
        return b"";
        
def reset():
    global httpMethod, path, contentHeader, contentLen, content, complete, stage, contentCount, contentBA, contentList, intContentLen;
    httpMethod = ""; 
    path = "";
    contentHeader = "";
    contentLen = ""; 
    content = b"";
    contentBA = bytearray(b"");
    complete = False; 
    stage = 0;
    contentCount = 0;   
    upperMethod = "";
    contentList = [];
    intContentLen = 0;

#def printAll():
#    print("     httpMethod: " + httpMethod);
#    print("     path: " + path);
#    if (httpMethod.upper() == "POST"):
#        print("     contentHeader: " + contentHeader);
#        print("     contentLen: " + contentLen);
#        print(b"     content: " + content);
   
main();


#cProfile.run('main()')
   

# stage 
# 0: add to httpMethod
# 1: add to path
# if method is POST           
# 2: add to contentHeader      
# 3: add to contentLen          
# 4: do nothing (should receive an empty space)
# 5: add to content
# 6: set complete to True  
# if method is GET
# 2: set complete to True

# if method is POST           
# 2: add to contentHeader      
# 3: add to contentLen          
# 4: do nothing (should receive an empty space)
# 5: add to content
# 6: set complete to True 

# if method is GET
# 2: set complete to True
#def simpleParser(currentElement: str):
#    if stage == 2:
#        complete = True;

#def isComplete(stage: int) -> bool:
#    return (stage == 3 and (httpMethod == "GET" or httpMethod == "DELETE")) or (stage == 7 and httpMethod == "POST")
