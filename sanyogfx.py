import tkinter as tk
import sys
from tkinter import filedialog
import os
from os.path import dirname, basename, splitext

root = tk.Tk()
root.withdraw()

if len(sys.argv)==2:
    filePath=sys.argv[1]
else:
    filePath=filedialog.askopenfilename()

file=open(filePath,mode='rb')
size=os.path.getsize(filePath)
outDir=dirname(filePath)
BaseName=splitext(basename(filePath))[0]

Bin=file.read()

outFile=input("Enter a name prefix for output files: ")
numFiles=0

sr=iter(range(size))


# Functions vv

def writeFile(address, size, ext):
    global numFiles
    outBytes=Bin[address:address+size]
    output=open(outDir+"/%s_%s.%s" % (outFile, str(numFiles), ext), mode="xb")
    output.write(outBytes)
    output.close()
    print("Exported %s_%s.%s at address %s, size %s" % (outFile, str(numFiles), ext, hex(address), str(size)))
    numFiles+=1

# Functions ^^


print("Now searching "+basename(filePath))

for x in sr:
    if Bin[x:x+3] == b"\x49\x43\x00":
        chunkSize=int.from_bytes(Bin[x+2:x+4], "little")
        writeFile(x, chunkSize+2, "ic")
    if Bin[x:x+3] == b"\x50\x57\x00":
        chunkSize=int.from_bytes(Bin[x+2:x+4], "little")
        writeFile(x, chunkSize+2, "pw")
    if Bin[x:x+3] == b"\x43\x57\x00":
        chunkSize=int.from_bytes(Bin[x+2:x+4], "little")
        writeFile(x, chunkSize+2, "cw")
    if Bin[x:x+3] == b"\x53\x49\x00":
        chunkSize=int.from_bytes(Bin[x+2:x+4], "little")
        writeFile(x, chunkSize+2, "si")
    if Bin[x:x+3] == b"\x43\x48\x00":
        chunkSize=int.from_bytes(Bin[x+2:x+4], "little")
        writeFile(x, chunkSize+2, "ch")

print("Found %s total hits." % str(numFiles))
input("Press Enter to exit")
