import fileinput
import sys
import os.path

prefix = sys.argv[1]

filename = prefix + "/lib/python2.7/dist-packages/easy-install.pth"
filename = filename.replace("//", "/")

if os.path.isfile(filename):
    print("removing /usr/lib/python2.7 from " + filename)
    for line in fileinput.input(filename, inplace=True):
        newline = line.replace("\n", "")
        if not '/usr/lib/python2.7' in newline:
            print(newline)

filename = prefix + "/lib/python2.7/site-packages/easy-install.pth"
filename = filename.replace("//", "/")

if os.path.isfile(filename):
    print("removing /usr/lib/python2.7 from " + filename)
    for line in fileinput.input(filename, inplace=True):
        newline = line.replace("\n", "")
        if not '/usr/lib/python2.7' in newline:
            print(newline)
