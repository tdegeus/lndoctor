
from setuptools import setup
from setuptools import find_packages

setup(
    name = 'lndoctor',
    license = 'MIT',
    author = 'Tom de Geus',
    author_email = 'tom@geus.me',
    description = 'Detailed information of symbolic links',
    long_description = 'Detailed information of symbolic links',
    keywords = 'symlink',
    url = 'https://github.com/tdegeus/lndoctor',
    packages = find_packages(),
    use_scm_version = {'write_to': 'lndoctor/_version.py'},
    setup_requires = ['setuptools_scm'],
    # install_requires = [],
    entry_points = {
        'console_scripts': [
            'lndoctor = lndoctor.cli.lndoctor:main',
        ]})
