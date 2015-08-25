# -*- encoding: utf-8 -*-

__author__ = 'Mohanson'

import getopt
import sys

import saika.path.clean


usage = """
Usage:
    saika.path.clean [options] [dirs]

Options:
    -h, --help                  Show help.
    -t, --type                  List contain 'python'
"""


def main():
    options = dict()

    shortargs = 'ht:'
    longargs = ['help', 'type=']
    opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)
    for opt in opts:
        if opt[0] in ['-h', '--help']:
            print(usage)
        if opt[0] in ['-t', '--type']:
            options['type'] = opt[1]

    for folder_path in args:
        if 'type' in options:
            saika.path.clean.clean(folder_path, options['type'])
        else:
            saika.path.clean.auto_clean(folder_path)


if __name__ == '__main__':
    main()