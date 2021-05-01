'''
Start 3 processes using a function 'f()' as the entry point.
Start 3 instances and wait for completion.
Print activity showing overlapping execution of all processes.
'''

import multiprocessing
import time


def log(proc, msg):
    print(' ' * 2 * proc, "Parent" if 0 == proc else proc, msg)


def f(args):
    log(args, "start")
    for i in range(5):
        log(args, "tick{0}".format(i))
        time.sleep(0.01)
    log(args, "done")


if __name__ == '__main__':
    log(0, "start")
    p1 = multiprocessing.Process(target=f, args=[1])
    p2 = multiprocessing.Process(target=f, args=[2])
    p3 = multiprocessing.Process(target=f, args=[3])
    p1.start()
    p2.start()
    p3.start()
    log(0, "wait")
    p1.join()
    p2.join()
    p3.join()
    log(0, "done")

