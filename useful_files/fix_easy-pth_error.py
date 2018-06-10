import fileinput
import sys

prefix = sys.argv[1]
print("removing /usr/lib/python2.7 from prefix \"" + prefix + "\" easy-install.pth")

for line in fileinput.input(prefix + "/lib/python2.7/dist-packages/easy-install.pth", inplace=True):
    newline = line.replace("\n", "")
    if not '/usr/lib/python2.7' in newline:
        print(newline)

for line in fileinput.input(prefix + "/lib/python2.7/site-packages/easy-install.pth", inplace=True):
    newline = line.replace("\n", "")
    if not '/usr/lib/python2.7' in newline:
        print(newline)
