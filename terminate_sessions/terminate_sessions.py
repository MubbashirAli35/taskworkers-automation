import os
from multiprocessing import Process

def gctw01():
    os.system('python gctw01.py')

def gctw02():
    os.system('python gctw02.py')

def gctw03():
    os.system('python gctw03.py')

def gctw04():
    os.system('python gctw04.py')

def gctw05():
    os.system('python gctw05.py')

def gctw06():
    os.system('python gctw06.py')

def gctw07():
    os.system('python gctw07.py')

def gctw08():
    os.system('python gctw08.py')

def gctw09():
    os.system('python gctw09.py')

def gctw10():
    os.system('python gctw10.py')

def gctw11():
    os.system('python gctw11.py')

def gctw12():
    os.system('python gctw12.py')

def gctw13():
    os.system('python gctw13.py')

def gctw14():
    os.system('python gctw14.py')

def gctw15():
    os.system('python gctw15.py')

def gctw16():
    os.system('python gctw16.py')

def gctw17():
    os.system('python gctw17.py')

def gctw18():
    os.system('python gctw18.py')

def gctw19():
    os.system('python gctw19.py')

def gctw20():
    os.system('python gctw20.py')

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