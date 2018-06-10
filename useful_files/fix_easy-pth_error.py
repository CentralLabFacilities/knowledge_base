import fileinput
import sys

prefix = sys.argv[1]

for line in fileinput.input(prefix + "/lib/python2.7/dist-packages/easy-install.pth", inplace=True):
    newline = line.replace("\n", "")
    if not '/usr' in newline:
        print(newline)
for line in fileinput.input(prefix + "/lib/python2.7/site-packages/easy-install.pth", inplace=True):
    newline = line.replace("\n", "")
    if not '/usr' in newline:
        print(newline)
