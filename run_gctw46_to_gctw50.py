import os
from multiprocessing import Process
import sys

def gctw46():
    os.system('python gctw46.py' + ' ' + sys.argv[1])

def gctw47():
    os.system('python gctw47.py' + ' ' + sys.argv[1])

def gctw48():
    os.system('python gctw48.py' + ' ' + sys.argv[1])

def gctw49():
    os.system('python gctw49.py' + ' ' + sys.argv[1])

def gctw50():
    os.system('python gctw50.py' + ' ' + sys.argv[1])

if __name__ == '__main__':
    worker46 = Process(target=gctw46)
    worker47 = Process(target=gctw47)
    worker48 = Process(target=gctw48)
    worker49 = Process(target=gctw49)
    worker50 = Process(target=gctw50)

    worker46.start()
    worker47.start()
    worker48.start()
    worker49.start()
    worker50.start()
