#!/usr/bin/env python3

from setuptools import setup

setup(
    name='modod',
    version='0.2.1',
    description='Regular expression optimizer',
    packages=['modod', 'parser'],
    include=['main_simplify', 'graph'],
    entry_points={
        'console_scripts': [
            'simplify = main_simplify:main'
        ]
    }
    )
