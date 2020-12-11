import os
from multiprocessing import Process
import sys

def gctw26():
    os.system('python gctw26.py' + ' ' + sys.argv[1])

def gctw27():
    os.system('python gctw27.py' + ' ' + sys.argv[1])

def gctw28():
    os.system('python gctw28.py' + ' ' + sys.argv[1])

def gctw29():
    os.system('python gctw29.py' + ' ' + sys.argv[1])

def gctw30():
    os.system('python gctw30.py' + ' ' + sys.argv[1])

if __name__ == '__main__':
    worker26 = Process(target=gctw26)
    worker27 = Process(target=gctw27)
    # worker28 = Process(target=gctw28)
    # worker29 = Process(target=gctw29)
    # worker30 = Process(target=gctw30)

    worker26.start()
    worker27.start()
    # worker28.start()
    # worker29.start()
    # worker30.start()
