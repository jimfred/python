'''
Start 3 processes using a function 'f()' as the entry point.
Start 3 instances and wait for completion.
'''

import os
from multiprocessing import Process
from time import sleep


def f(args):
    print(os.getpid(), '-' * args, "Start")
    for i in range(5):
        print(os.getpid(), '-' * args, i)
        sleep(0.001)


print(os.getpid(), "Start")
p1 = Process(target=f, args=[1])
p2 = Process(target=f, args=[2])
p3 = Process(target=f, args=[3])
p1.start()
p2.start()
p3.start()
print(os.getpid(), "Wait")
p1.join()
p2.join()
p3.join()
print(os.getpid(), "Done")