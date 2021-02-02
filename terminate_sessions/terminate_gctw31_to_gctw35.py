import os
from multiprocessing import Process
import sys

def gctw31():
    os.system('python gctw31.py' + ' ' + sys.argv[1])

def gctw32():
    os.system('python gctw32.py' + ' ' + sys.argv[1])

def gctw33():
    os.system('python gctw33.py' + ' ' + sys.argv[1])

def gctw34():
    os.system('python gctw34.py' + ' ' + sys.argv[1])

def gctw35():
    os.system('python gctw35.py' + ' ' + sys.argv[1])

if __name__ == '__main__':
    worker31 = Process(target=gctw31)
    worker32 = Process(target=gctw32)
    worker33 = Process(target=gctw33)
    worker34 = Process(target=gctw34)
    worker35 = Process(target=gctw35)

    worker31.start()
    worker32.start()
    worker33.start()
    worker34.start()
    worker35.start()
