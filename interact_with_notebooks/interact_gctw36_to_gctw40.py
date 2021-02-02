import os
from multiprocessing import Process
import sys

def gctw36():
    os.system('python gctw36.py' + ' ' + sys.argv[1])

def gctw37():
    os.system('python gctw37.py' + ' ' + sys.argv[1])

def gctw38():
    os.system('python gctw38.py' + ' ' + sys.argv[1])

def gctw39():
    os.system('python gctw39.py' + ' ' + sys.argv[1])

def gctw40():
    os.system('python gctw40.py' + ' ' + sys.argv[1])

if __name__ == '__main__':
    worker36 = Process(target=gctw36)
    worker37 = Process(target=gctw37)
    worker38 = Process(target=gctw38)
    worker39 = Process(target=gctw39)
    worker40 = Process(target=gctw40)

    worker36.start()
    worker37.start()
    worker38.start()
    worker39.start()
    worker40.start()
