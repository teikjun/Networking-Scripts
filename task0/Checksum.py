import zlib;
import sys;

# scan input file
inputFile = sys.argv[1]

# open file in binary reader. get the entire content using read() and store into bytes object
with open(inputFile, "rb") as f:
    bytes = f.read();

# get the checksum of the bytes object and print it
checksum = zlib.crc32(bytes);
print(checksum);