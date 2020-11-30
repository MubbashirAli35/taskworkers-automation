import os
from multiprocessing import Process
import sys

def gctw06():
    os.system('python gctw06.py' + ' ' + sys.argv[1])

def gctw07():
    os.system('python gctw07.py' + ' ' + sys.argv[1])

def gctw08():
    os.system('python gctw08.py' + ' ' + sys.argv[1])

def gctw09():
    os.system('python gctw09.py' + ' ' + sys.argv[1])

def gctw10():
    os.system('python gctw10.py' + ' ' + sys.argv[1])

if __name__ == '__main__':
    worker6 = Process(target=gctw06)
    worker7 = Process(target=gctw07)
    worker8 = Process(target=gctw08)
    worker9 = Process(target=gctw09)
    worker10 = Process(target=gctw10)

    worker6.start()
    worker7.start()
    worker8.start()
    worker9.start()
    worker10.start()
