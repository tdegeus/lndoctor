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
        os.symlink(os.path.join(dirname, filename), os.path.join(dirname, "mylink"))
        path = run("lndoctor -r {0:s}".format(os.path.join(dirname, "mylink")))
        self.assertEqual(path.strip(), os.path.join(dirname, filename))
        os.remove(os.path.join(dirname, "mylink"))


if __name__ == '__main__':

    unittest.main()
