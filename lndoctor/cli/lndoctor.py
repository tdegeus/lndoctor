'''Show detailed link information.

:usage:

    lndoctor [options] <path>

:arguments:

    Path to investigate.

:options:

    -r, --realpath
        Show real path only.

    --colors=arg
        Select print color scheme from: none, dark. [default: dark]

    -h, --help
        Show help.

    --version
        Show version.

(c - MIT) T.W.J. de Geus | tom@geus.me | www.geus.me | github.com/tdegeus/gsbatch_topng
'''

import argparse
import os
import collections.abc

from .. import version


def diff_theme(theme=None):
    r'''
Return dictionary of colors.

.. code-block:: python

    {
        'equal' : '...',
        'insert' : '...',
        'delete': '...',
        'replace' : '...',
    }

:param str theme: Select color-theme.

:rtype: dict
    '''

    if theme == 'dark':
        return \
        {
            'equal' : '',
            'insert' : '1;32',
            'delete': '1;31',
            'replace' : '1;37',
        }

    return \
    {
        'equal' : '',
        'insert' : '',
        'delete': '',
        'replace' : '',
    }


def theme(theme=None):
    r'''
Return dictionary of colors.

.. code-block:: python

    {
        'new' : '...',
        'overwrite' : '...',
        'skip' : '...',
        'bright' : '...',
    }

:param str theme: Select color-theme.

:rtype: dict
    '''

    if theme == 'dark':
        return \
        {
            'new' : '1;32',
            'overwrite': '1;31',
            'skip' : '1;30',
            'bright' : '1;37',
        }

    return \
    {
        'new' : '',
        'overwrite': '',
        'skip' : '',
        'bright' : '',
    }


class String:
    r'''
Rich string.

.. note::

    All options are attributes, that can be modified at all times.

.. note::

    Available methods:

    *   ``A.format()`` :  Formatted string.
    *   ``str(A)`` : Unformatted string.
    *   ``A.isnumeric()`` : Return if the "data" is numeric.
    *   ``int(A)`` : Dummy integer.
    *   ``float(A)`` : Dummy float.

:type data: str, None
:param data: The data.

:type width: None, int
:param width: Print width (formatted print only).

:type color: None, str
:param color: Print color, e.g. "1;32" for bold green (formatted print only).

:type align: ``'<'``, ``'>'``
:param align: Print alignment (formatted print only).

:type dummy: 0, int, float
:param dummy: Dummy numerical value.

:methods:


    '''

    def __init__(self, data, width=None, align='<', color=None, dummy=0):

        self.data  = data
        self.width = width
        self.color = color
        self.align = align
        self.dummy = dummy

    def format(self):
        r'''
Return formatted string: align/width/color are applied.
        '''

        if self.width and self.color:
            fmt = '\x1b[{color:s}m{{0:{align:s}{width:d}.{width:d}s}}\x1b[0m'.format(**self.__dict__)
        elif self.width:
            fmt = '{{0:{align:s}{width:d}.{width:d}s}}'.format(**self.__dict__)
        elif self.color:
            fmt = '\x1b[{color:s}m{{0:{align:s}s}}\x1b[0m'.format(**self.__dict__)
        else:
            fmt = '{{0:{align:s}s}}'.format(**self.__dict__)

        return fmt.format(str(self))

    def isnumeric(self):
        r'''
Return if the "data" is numeric : always zero for this class.
        '''
        return False

    def __str__(self):
        return str(self.data)

    def __int__(self):
        return int(self.dummy)

    def __float__(self):
        return float(self.dummy)

    def __repr__(self):
        return str(self)

    def __lt__(self,other):
        return str(self) < str(other)


def _flatten_detail(lst):
    r'''
Detail of :py:fun:`Flatten`.
Not part of public API.

See https://stackoverflow.com/a/17485785/2646505
    '''

    for item in lst:
        if isinstance(item, collections.abc.Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


def flatten(lst):
    r'''
Flatten a nested list to a one dimensional list.
    '''
    return list(_flatten_detail(lst))



def replacelink(path_list):
    r'''
Iterative path backwards from the end of the list:
once a link is encountered it is replaced by its target and the function quits.

:oaram list path_list:
    Path, separated in components
    (e.g. "path/to/link" should be supplied as ["path", "to", "link"]).

:return: path_list, index
    Thereby the link at ``index`` is replaced by its target (also as list of path components).
    If no link is found ``index = None``.
    '''

    path = [p for p in path_list]
    n = len(path)

    for i in range(n):

        p = (os.sep).join(path[:n - i])

        if os.path.islink(p):
            path[n - i - 1] = os.readlink(p).split(os.sep)
            return path, n - i - 1

    return path, None


def verbose(path, theme_name='none'):
    r'''
Recursively replace links by targets, and print these replacement (in color).

:param str path: A file path to investigate.
:param str theme_name: The name of the color-theme. See :py:mod:`mv_regex.theme`.
    '''

    assert os.path.exists(path)
    color = theme(theme_name.lower())
    path = path.split(os.sep)
    inc = 0

    while True:

        dev, i = replacelink(path)

        if i is None:
            break

        if len(dev[i][0]) > 0:
            a = (os.sep).join(path[:i])
            b = path[i]
        else:
            a = ''
            b = (os.sep).join(path[:i + 1])

        n = (os.sep).join(dev[i])
        c = (os.sep).join(path[i + 1:])

        if len(a) > 0:
            o = (os.sep).join([a, String(b, color=color['bright']).format(), c])
            d = (os.sep).join([a, String(n, color=color['new']).format(), c])
        else:
            o = (os.sep).join([String(b, color=color['bright']).format(), c])
            d = (os.sep).join([String(n, color=color['new']).format(), c])

        if inc > 0:
            print('')

        print(o)
        print(d)

        inc += 1

        if len(dev[i][0]) == 0:
            break

        path = flatten(dev)


def main():

    try:

        class Parser(argparse.ArgumentParser):
            def print_help(self):
                print(__doc__)

        parser = Parser()
        parser.add_argument('-r', '--realpath', required=False, action='store_true')
        parser.add_argument(      '--colors', required=False, default='dark')
        parser.add_argument('-v', '--version', action='version', version=version)
        parser.add_argument('path', type=str)
        args = parser.parse_args()

        if args.realpath:
            print(os.path.realpath(args.path))
            return 0

        verbose(path=args.path, theme_name=args.colors)

    except Exception as e:

        print(e)
        return 1


if __name__ == '__main__':

    main()
