#!/usr/bin/env python
import multiprocessing
import os
import time
def print_cube(num):
    print("Cube: {}".format(num * num * num))

def print_square(num):
    print("Square: {}".format(num * num))
    print(os.getpid())


def main():
    jobs = []
    for i in range(1, os.cpu_count()):
        # create process
        p = multiprocessing.Process(target=print_square, args=(i, ))
        # q = multiprocessing.Process(target=print_cube, args=(i, ))
        jobs.append(p)

        #start process
        p.start()
        # q.start()

    for job in jobs:
        job.join()

    print("Done")


if __name__ == '__main__':
    main()
