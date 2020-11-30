import os
from multiprocessing import Process
import sys

def gctw16():
    os.system('python gctw16.py' + ' ' + sys.argv[1])

def gctw17():
    os.system('python gctw17.py' + ' ' + sys.argv[1])

def gctw18():
    os.system('python gctw18.py' + ' ' + sys.argv[1])

def gctw19():
    os.system('python gctw19.py' + ' ' + sys.argv[1])

def gctw20():
    os.system('python gctw20.py' + ' ' + sys.argv[1])

if __name__ == '__main__':
    worker16 = Process(target=gctw16)
    worker17 = Process(target=gctw17)
    worker18 = Process(target=gctw18)
    worker19 = Process(target=gctw19)
    worker20 = Process(target=gctw20)

    worker16.start()
    worker17.start()
    worker18.start()
    worker19.start()
    worker20.start()
