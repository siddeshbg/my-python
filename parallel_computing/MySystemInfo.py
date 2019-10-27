#!/usr/bin/env python

import multiprocessing
import os
from cpu_cores import CPUCoresCounter


class SystemInfo:
    def get_info(self):
        print("Your system got %s cpu(s)" % multiprocessing.cpu_count())
        # print(os.cpu_count())

        # We build an instance for the current operating system
        instance = CPUCoresCounter.factory()

        # Get the number of total real cpu cores
        print("Total number of real cpu cores: %s" % instance.get_physical_cores_count())

        # Get the number of total physical processors
        print("Total number of physical processors: %s" % instance.get_physical_processors_count())


if __name__ == '__main__':
    info = SystemInfo()
    info.get_info()
