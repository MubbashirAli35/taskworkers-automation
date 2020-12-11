import os
from multiprocessing import Process
import sys

def gctw21():
    os.system('python gctw21.py' + ' ' + sys.argv[1])

def gctw22():
    os.system('python gctw22.py' + ' ' + sys.argv[1])

def gctw23():
    os.system('python gctw23.py' + ' ' + sys.argv[1])

def gctw24():
    os.system('python gctw24.py' + ' ' + sys.argv[1])

def gctw25():
    os.system('python gctw25.py' + ' ' + sys.argv[1])

if __name__ == '__main__':
    worker21 = Process(target=gctw21)
    worker22 = Process(target=gctw22)
    worker23 = Process(target=gctw23)
    worker24 = Process(target=gctw24)
    worker25 = Process(target=gctw25)

    # worker21.start()
    worker22.start()
    worker23.start()
    worker24.start()
    worker25.start()
