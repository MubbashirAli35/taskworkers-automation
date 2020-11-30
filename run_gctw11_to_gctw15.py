import os
from multiprocessing import Process
import sys

def gctw11():
    os.system('python gctw11.py' + ' ' + sys.argv[1])

def gctw12():
    os.system('python gctw12.py' + ' ' + sys.argv[1])

def gctw13():
    os.system('python gctw13.py' + ' ' + sys.argv[1])

def gctw14():
    os.system('python gctw14.py' + ' ' + sys.argv[1])

def gctw15():
    os.system('python gctw15.py' + ' ' + sys.argv[1])

if __name__ == '__main__':
    worker11 = Process(target=gctw11)
    worker12 = Process(target=gctw12)
    worker13 = Process(target=gctw13)
    worker14 = Process(target=gctw14)
    worker15 = Process(target=gctw15)

    worker11.start()
    worker12.start()
    worker13.start()
    worker14.start()
    worker15.start()
