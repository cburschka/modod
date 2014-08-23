#!/usr/bin/env python3

from setuptools import setup

setup(
    name='modod',
    version='0.2.1',
    description='Regular expression optimizer',
    packages=['modod', 'parser', 'graph'],
    package_dir={'': 'src'},
    include=['main_simplify'],
    entry_points={
        'console_scripts': [
            'simplify = main_simplify:main'
        ]
    },
    scripts=[
      'src/dtd-inf/dtd.py',
      'src/dtd-inf/sore.py',
      'src/simplify.py',
      'src/main_simplify.py',
      'simplify.py',
      'dtd.py',
      'sore.py'
    ]
    )
