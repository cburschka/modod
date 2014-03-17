#!/usr/bin/env python3

from setuptools import setup

setup(
    name='modod',
    version='0.2.1',
    description='Regular expression optimizer',
    packages=['modod', 'parser'],
    package_dir={'': 'src'},
    include=['main_simplify', 'graph'],
    entry_points={
        'console_scripts': [
            'simplify = main_simplify:main'
        ]
    },
    scripts=[
      'src/dtd-inf/dtd.py',
      'src/dtd-inf/sore.py',
      'dtd.py',
      'sore.py'
    ]
    )
