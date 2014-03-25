#!/usr/bin/env python3

# This file provides a simple way of running simplify
# without building or installing the software.

import os
import sys

src_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'src', '')
sys.path = [src_path] + sys.path

import main_simplify

main_simplify.main()
