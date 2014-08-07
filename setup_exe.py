#!/usr/bin/env python3

import sys
from cx_Freeze import setup, Executable

setup(
    name = 'modod-sore',
    version = '0.2',
    description='SORE from word list.',
    options = {"build_exe": {'packages': ['modod', 'parser'], 'path': ['src'] + sys.path}},
    executables = [
      Executable('src/dtd-inf/sore.py'),
      Executable('src/dtd-inf/dtd.py'),
      Executable('src/simplify.py')
    ]
    )

