import sys;

inputString = sys.argv[1];
subStringA = inputString[0:8];
subStringB = inputString[8:16];
subStringC = inputString[16:24];
subStringD = inputString[24:32];

myList = [subStringA, subStringB, subStringC, subStringD];

for i in range(0, 4):
    myList[i] = int(myList[i] , 2);

for j in range(0, 4):
    if (j < 3):
        print(str(myList[j]) + ".", end =  "");
    else:
        print(myList[j]);



