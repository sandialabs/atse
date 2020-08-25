from __future__ import print_function
from collections import defaultdict
import sys
import re
import argparse

res = {} # Given a reasons line, determine what kind it is
args = None

reason_categories = ['all', 'hardware', 'memory', 'software',
                     'filesystem', 'ignored', 'other']
# 'other' is a catchall that does not match other specific reasons
# This is a superset of res.keys()

def init_res():
    res['all'] = re.compile('')
    res['hardware'] = re.compile('(nodecheck|Nodediag|LOW_MHZ|TURBO ON)')
    res['memory'] = re.compile('MemoryErrors')
    res['software'] = re.compile('(sharpd|NTP|openibd)')
    res['filesystem'] = re.compile('(Lustre|projects|NFS)')
    res['ignored'] = re.compile('Needs Reason|\[2019-03-23T.*\] update_node: node ast[0-9]+ reason set to: performance|healthcheck:\n')

class node:
    def __init__(self):
        self.metrics = {}
        # Any kvs we wish to keep

        self.logcats = defaultdict(list)
        # key: Log category
        # Value: List of loglines

    def add_line(self, line, category):
        self.logcats[category].append(line)

nodes = defaultdict(node)

def process_update_node(line):
    line = line.strip('\n')
    hostname = line.split(' ')[3]
    nmatched = 0
    for name,test_re in res.items():
        if test_re.search(line):
            nodes[hostname].add_line(line, name)
            nmatched += 1
    if nmatched == 1: # Matched only 'all'
        nodes[hostname].add_line(line, 'other')
    elif nmatched > 2:
        print('Warning: The following line matched %s categories' % nmatched)
        print(line)
    elif nmatched == 0:
        print('Warning: The following line did not match any expressions (including empty)')
        print(line)

def read_slurm(infile):
    update_node_re = re.compile('update_node: node ast[0-9]+ reason set to:')
    for line in infile:
        if update_node_re.search(line):
            process_update_node(line)

def print_node_table(nodelist):
    for field in reason_categories:
        print(field, end=' ')

    for nodename in nodelist:
        print(nodename, end=' ')

        for field in reason_categories:
            print(len(nodes[nodename].logcats[field]), end=' ')
        print()

def print_node_summaries(nodelist):
    for nodename in nodelist:
        print(nodename)
        for field in reason_categories: #res.keys():
            logs = nodes[nodename].logcats[field]
            print('\t', field, len(logs))
            nskey = 'show_' + field
            if vars(args).get(nskey) is True:
                print('\n'.join(logs))
    pass

def parse_args():
    global args
    parser = argparse.ArgumentParser(description='Display node history and statistics from slurm logs on stdin.')
    for cat in reason_categories:
        parser.add_argument('-' + cat[0].upper(),
                            '--' + cat,
                            action='store_true',
                            dest='show_' + cat,
                            help=('Display errors of type "%s"' % cat))
    parser.add_argument('-t', '--table', action='store_true', dest='print_table_only', help='Display table with error type counts. Overrides per-category arguments.')
    parser.add_argument('nodes', type=str, nargs='*', help='Nodes to output')
    args = parser.parse_args()

def main():
    parse_args()

    init_res()
    read_slurm(sys.stdin)

    nodelist=args.nodes
    if len(nodelist) == 0:
        for i in range(1, 2593):
            nodename = 'ast' + str(i)
            nodelist.append(nodename)
    if args.print_table_only is False:
        print_node_summaries(nodelist)
    else:
        print_node_table(nodelist)


if __name__ == "__main__":
    main()
