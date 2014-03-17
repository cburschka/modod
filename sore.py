#!/usr/bin/python3

# This file provides a simple way of running sore.py
# without building or installing the software.

import os
import sys

src_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'src', '')
sys.path = [src_path, os.path.join(src_path, 'dtd-inf')] + sys.path

import sore
