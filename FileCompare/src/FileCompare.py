#!/usr/bin/env python3
from argparse import ArgumentParser
import sys

class FileCompare:
    def __init__(self, src_file, dest_file):
        self.src_file = src_file
        self.dest_file = dest_file

    def compare(self):
        found = []
        not_found = []
        with open(self.src_file) as src, open(self.dest_file) as dest:
            src_list = src.read().splitlines()
            dest_list = dest.read().splitlines()

            for data in src_list:
                if data not in dest_list:
                    not_found.append(data)
                else:
                    found.append(data)

        print("*" * 30)
        print("\t\tStatistics")
        print("*" * 30)
        print("Total items in source: %d" % len(src_list))
        print("Total items in destination: %d" % len(dest_list))
        print("Missing in destination: %d" % len(not_found))
        print(not_found)

        return {'found': found, 'not_found': not_found}


def main():
    parser = ArgumentParser(description='Script to look for items found in source file, but missing in destination')
    parser.add_argument("-s", "--src", help='Source file', required=True)
    parser.add_argument("-d", "--dest", help='Destination file', required=True)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    src = args.src
    dest = args.dest
    agent = FileCompare(src, dest)
    agent.compare()


if __name__ == '__main__':
    main()
