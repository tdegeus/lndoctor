import unittest
import subprocess
import os
import shutil
import lndoctor


def run(cmd, verbose=False):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')


class Test_cli(unittest.TestCase):

    def test_realpath(self):

        dirname, filename = os.path.split(os.path.abspath(__file__))
        a = os.path.join(dirname, "mylink")

        for i in [a]:
            if os.path.islink(i):
                os.remove(i)
            elif os.path.exists(i):
                raise IOError("Cannot run test: '{0:s}' exists".format(i))

        os.symlink(os.path.join(dirname, filename), a)

        path = run("lndoctor -r {0:s}".format(a))
        self.assertEqual(path.strip(), os.path.join(dirname, filename))

        os.remove(a)

    def test_recursive(self):

        dirname, filename = os.path.split(os.path.abspath(__file__))
        a = os.path.join(dirname, "mylink")
        b = os.path.join(dirname, "mylink2")

        for i in [a, b]:
            if os.path.islink(i):
                os.remove(i)
            elif os.path.exists(i):
                raise IOError("Cannot run test: '{0:s}' exists".format(i))

        os.symlink(os.path.join(dirname, filename), a)
        os.symlink(a, b)

        ret = run("lndoctor --colors none {0:s}".format(os.path.join(dirname, "mylink2")))
        print('ret = ', ret)
        ret = list(filter(None, ret.splitlines()))
        ret = [i[:-1] if i[-1] == os.sep else i for i in ret]
        print('ret = ', ret)

        self.assertTrue(len(ret) == 2)
        self.assertEqual(ret[1], a)
        self.assertEqual(ret[0], b)

        os.remove(a)
        os.remove(b)


if __name__ == '__main__':

    unittest.main()
