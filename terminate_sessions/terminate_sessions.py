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

if __name__=='__main__':
    worker1 = Process(target=gctw01)
    worker2 = Process(target=gctw02)
    worker3 = Process(target=gctw03)
    worker4 = Process(target=gctw04)
    worker5 = Process(target=gctw05)
    worker6 = Process(target=gctw06)
    worker7 = Process(target=gctw07)
    worker8 = Process(target=gctw08)
    worker9 = Process(target=gctw09)
    worker10 = Process(target=gctw10)
    worker11 = Process(target=gctw11)
    worker12 = Process(target=gctw12)
    worker13 = Process(target=gctw13)
    worker14 = Process(target=gctw14)
    worker15 = Process(target=gctw15)
    worker16 = Process(target=gctw16)
    worker17 = Process(target=gctw17)
    worker18 = Process(target=gctw18)
    # worker19 = Process(target=gctw19)
    worker20 = Process(target=gctw20)

    worker1.start()
    worker2.start()
    worker3.start()
    worker4.start()
    worker5.start()
    worker6.start()
    worker7.start()
    worker8.start()
    worker9.start()
    worker10.start()
    worker11.start()
    worker12.start()
    worker13.start()
    worker14.start()
    worker15.start()
    worker16.start()
    worker17.start()
    worker18.start()
    # worker19.start()
    worker20.start()