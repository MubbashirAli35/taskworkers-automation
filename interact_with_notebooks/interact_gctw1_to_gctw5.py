import os
from multiprocessing import Process
import sys

def gctw01():
    os.system('python gctw01.py' + ' ' + sys.argv[1])

def gctw02():
    os.system('python gctw02.py' + ' ' + sys.argv[1])

def gctw03():
    os.system('python gctw03.py' + ' ' + sys.argv[1])

def gctw04():
    os.system('python gctw04.py' + ' ' + sys.argv[1])

def gctw05():
    os.system('python gctw05.py' + ' ' + sys.argv[1])


if __name__ == '__main__':
    worker1 = Process(target=gctw01)
    worker2 = Process(target=gctw02)
    worker3 = Process(target=gctw03)
    worker4 = Process(target=gctw04)
    worker5 = Process(target=gctw05)

    worker1.start()
    worker2.start()
    worker3.start()
    worker4.start()
    worker5.start()
