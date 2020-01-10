import sys;

data = []
spaceIndex = -1;
bIndex = -1;

i = 0;
while (True): 
    newData = sys.stdin.buffer.read(1);
    if (len(newData) == 0):
        break;
    elif (len(newData) == 1):
        data.append(newData);
        if (newData == b' '):
            spaceIndex = i;
        elif (newData == b'B'): 
            numString = "";
            bIndex = i;
            
            #find numerical value
            byteArray = data[spaceIndex + 1: bIndex];
            
            for b in byteArray:
               numString += bytes.decode(b);
            
            numInt = int(numString, 10);
            payloadData = sys.stdin.buffer.read(numInt);

            # payload
            sys.stdout.buffer.write(payloadData); 
            sys.stdout.buffer.flush();
    i += 1;
    

    
    

'''
while (True):
    i = 0; 
    if (len(data[i]) == i + 1):
        if data[i] == b" ":
            spaceIndex = i;
        elif data[i] == b"B":
            bIndex = i;
            data = sys.stdin.buffer.read1()
            part1 = data[spaceIndex + 1: bIndex];
            part2 = data[bIndex + 1:endIndex + 1];
            sys.stdout.buffer.write(part2); 
            sys.stdout.buffer.flush();
    if (len(data) == i)):
        break;
    i += 1;
'''


'''
while (True): 
    i = 0;
    data = sys.stdin.buffer.read1(1);
    if (len(data) == 1):
        if data[0] == b" ":
            spaceIndex = i;
        elif data[0] == b"B":
            bIndex = i;
            data = sys.stdin.buffer.read1()
            part1 = data[spaceIndex + 1: bIndex];
            part2 = data[bIndex + 1:endIndex + 1];
            sys.stdout.buffer.write(part2); 
            sys.stdout.buffer.flush();
    if (len(data) == 0):
        break;
    i += 1;
'''


'''
for i in range(0, 10**6):
    data = sys.stdin.buffer.read1(1);
    
    spaceIndex = -1;
    bIndex = -1;
    endIndex = -1;
    if (data[i] == b" "):
        spaceIndex = i;
    elif (data[i] == b"B"):
        bIndex = i;
    elif (data[i] == b""):
        endIndex = i;
        part1 = data[spaceIndex: bIndex];
        part2 = data[bIndex + 1: endIndex + 1];
        # write data to stdout and flush immediately
        sys.stdout.buffer.write(part2); 
        sys.stdout.buffer.flush();
        break;
'''
            


''' return index of B
    posSpace = data.find(b" ");
    posB = data.find(b"B");
    data = sys.stdin.buffer.read1(5);
    if data.length = 0 
    if pos >= 0:
        part1 = data[0:posSpace + 1];
        part2 = data[posSpace + 1:posB + 1];
        part3 = data[posB + 1:]
        # write data to stdout and flush immediately
        sys.stdout.buffer.write(part2); 
        sys.stdout.buffer.flush();
'''