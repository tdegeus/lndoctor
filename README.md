# lndoctor

[![CI](https://github.com/tdegeus/lndoctor/workflows/CI/badge.svg)](https://github.com/tdegeus/lndoctor/actions)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/lndoctor.svg)](https://anaconda.org/conda-forge/lndoctor)
[![PyPi release](https://img.shields.io/pypi/v/lndoctor.svg)](https://pypi.org/project/lndoctor/)

# Overview

*lndoctor* allows you to analyse symbolic links in different level of detail:

## Real path

```bash
lndoctor -r /path/to/mylink
``` 

Shows the real path of the link. 
Examples of functionality:

### Show the real path of the current directory

```bash
lndoctor -r `pwd`
```

### Go to the real path of the current directory

```bash
cd `lndoctor -r "$PWD"`
```

# Getting lndoctor

## Using conda

```bash
conda install -c conda-forge lndoctor
```

This will also download and install all necessary dependencies.

## Using PyPi

```bash
pip install lndoctor
```

This will also download and install the necessary Python modules.

## From source

```bash
# Download lndoctor
git checkout https://github.com/tdegeus/lndoctor.git
cd lndoctor

# Install
python -m pip install .
```

This will also download and install the necessary Python modules.
