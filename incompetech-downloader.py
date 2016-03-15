"""
imcompetech-downloader
written by Toni Barth (Timtam)
pull requests are welcome
"""

# some standard library importing stuff here
import argparse
import os
import os.path
import sys
# here we get stuff from our own source
from incload.downloader import Downloader
from incload import globals
from incload.parsers import songpage

# starting the argument command-line parsing
Parser=argparse.ArgumentParser()
Parser.add_argument("-o","--output",help="set the corresponding output directory",type=str)
Arguments=Parser.parse_args()
# output directory definition
if Arguments.output:
  globals.OutputDirectory=Arguments.output
if not os.path.exists(globals.OutputDirectory): # failure if not existing
  print "This output directory doesn't exist."
  sys.exit(1)
