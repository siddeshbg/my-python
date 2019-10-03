#!/usr/bin/env python3
import json
from argparse import ArgumentParser
import sys
import operator
import os


class Trace:
    def __init__(self, category, name, duration):
        self.category = category
        self.name = name
        self.duration = duration

    def get_name(self):
        return self.name

    def get_duration(self):
        return self.duration

    def category(self):
        return self.category


class BazelTraceParser:
    def __init__(self, trace_file):
        self.trace_file = trace_file

    def get_traces(self):
        with open(self.trace_file) as f:
            data = json.load(f)

        return [Trace(line['cat'], line['name'], line['dur']) for line in data if 'cat' in line and 'dur' in line]

    def get_categories(self, traces):
        return set(tr.category for tr in traces)

    def get_traces_sorted(self, traces):
        return sorted(traces, key=operator.attrgetter('duration'))


class CompareTraces:
    def __init__(self, trace1, trace2):
        self.trace1 = trace1
        self.trace2 = trace2

    def compare_traces(self, file_name1, file_name2):
        short_filename1 = os.path.basename(file_name1)
        short_filename2 = os.path.basename(file_name2)
        output_filename = short_filename1 + "_" + short_filename2 + ".csv"
        print(output_filename)
        f = open(output_filename, 'w')
        f.write("name, category, %s, %s, diff, n times more/less\n" % (short_filename1, short_filename2))

        x_total = 0
        y_total= 0
        count = 0
        for x in self.trace1:
            if x.category not in ["general information", "skyframe evaluator"]:
                for y in self.trace2:
                    if x.category == y.category and x.name == y.name:
                        #print("%s, %s, %d, %d, %d" % (x.name, x.category, x.duration, y.duration, x.duration - y.duration))
                        sanitize_category = x.category.replace(",", "")
                        sanitize_name = x.name.replace(",", "")
                        f.write("%s, %s, %d, %d, %d, %.2f\n" % (sanitize_name, sanitize_category, x.duration, y.duration,
                                                          x.duration - y.duration, (x.duration - y.duration)/x.duration))
                        x_total += x.duration
                        y_total += y.duration
                        count += 1
        x_average = x_total/count
        y_average = y_total/count
        diff_average = x_average - y_average
        f.write("%s, %s, %.2f, %.2f, %d, %s\n" % ("Average", "", x_average, y_average, diff_average, diff_average/x_average))
        f.close()


def main():
    arg_parser = ArgumentParser(description="Script to parse Bazel Trace file")
    arg_parser.add_argument("-f", "--file", help='Trace file', required=True)
    arg_parser.add_argument("--file2", help='Trace file 2')

    if len(sys.argv) == 1:
        arg_parser.print_help(sys.stderr)
        sys.exit(1)

    args = arg_parser.parse_args()
    trace_file = args.file
    trace_file2 = args.file2

    trace_parser = BazelTraceParser(trace_file)
    traces = trace_parser.get_traces()
    sorted_traces = trace_parser.get_traces_sorted(traces)
    '''
    for tr in sorted_traces:
        print(tr.category, tr.name, tr.duration)
    '''

    for i in range(len(sorted_traces) - 1, len(sorted_traces) - 11, -1):
        print(sorted_traces[i].category, sorted_traces[i].name, sorted_traces[i].duration)

    parser2 = BazelTraceParser(trace_file2)
    traces2 = parser2.get_traces()
    sorted_traces2 = parser2.get_traces_sorted(traces2)

    print("#"*100)
    for i in range(len(sorted_traces2) - 1, len(sorted_traces2) - 11, -1):
        print(sorted_traces2[i].category, sorted_traces2[i].name, sorted_traces2[i].duration)

    comp = CompareTraces(sorted_traces, sorted_traces2)
    comp.compare_traces(trace_file, trace_file2)
    print(trace_parser.get_categories(traces))


if __name__ == '__main__':
    main()
