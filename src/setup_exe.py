#!/usr/bin/env python3

import sys
from cx_Freeze import setup, Executable

setup(
    name = 'modod-sore',
    version = '0.1',
    description='SORE from word list.',
    options = {"build_exe": {'packages': ['modod', 'parser']}},
    executables = [
      Executable('dtd-inf/sore.py'),
      Executable('dtd-inf/dtd.py')
    ]
    )

