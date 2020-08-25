#!/usr/bin/python

import argparse, sys, os, re, time, glob
from rpmUtils.miscutils import splitFilename

files = os.listdir(".")
for filename in files:
    (n, v, r, e, a) = splitFilename(filename)
    cmd = "mv " + filename + " " + n + ".rpm"
    print cmd
    os.system(cmd)
