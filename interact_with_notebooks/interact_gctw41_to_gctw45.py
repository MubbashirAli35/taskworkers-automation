import os
from multiprocessing import Process
import sys

def gctw41():
    os.system('python gctw41.py' + ' ' + sys.argv[1])

def gctw42():
    os.system('python gctw42.py' + ' ' + sys.argv[1])

def gctw43():
    os.system('python gctw43.py' + ' ' + sys.argv[1])

def gctw44():
    os.system('python gctw44.py' + ' ' + sys.argv[1])

def gctw45():
    os.system('python gctw45.py' + ' ' + sys.argv[1])

if __name__ == '__main__':
    worker41 = Process(target=gctw41)
    worker42 = Process(target=gctw42)
    worker43 = Process(target=gctw43)
    worker44 = Process(target=gctw44)
    worker45 = Process(target=gctw45)

    worker41.start()
    worker42.start()
    worker43.start()
    worker44.start()
    worker45.start()
