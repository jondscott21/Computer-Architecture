#!/usr/bin/env python3

"""Main."""

import sys
import os
from cpu import *


# if len(sys.argv) != 2:
os.path.join('ls8/examples')
# from examples import mult
print(sys.argv)
if len(sys.argv) != 2:
    print("Usage: file.py filename", file=sys.stderr)
    sys.exit(1)

cpu = CPU()

cpu.load(sys.argv[1])
cpu.run()
cpu.trace()