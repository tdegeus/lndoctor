'''Show detailed link information.

:usage:

    lndoctor [options] <path>

:arguments:

    Path to investigate.

:options:

    -r, --realpath
        Show real path only.

    -h, --help
        Show help.

    --version
        Show version.

(c - MIT) T.W.J. de Geus | tom@geus.me | www.geus.me | github.com/tdegeus/gsbatch_topng
'''

import argparse
import os

from .. import version

def main():

    try:

        class Parser(argparse.ArgumentParser):
            def print_help(self):
                print(__doc__)

        parser = Parser()
        parser.add_argument('-r', '--realpath', required=False, action='store_true')
        parser.add_argument('-v', '--version', action='version', version=version)
        parser.add_argument('path', type=str)
        args = parser.parse_args()

        if args.realpath:
            print(os.path.realpath(args.path))

    except Exception as e:

        print(e)
        return 1


if __name__ == '__main__':

    main()
