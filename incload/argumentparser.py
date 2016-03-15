# argumentparser
# suitable to parse all arguments needed to run this program properly
# so let's get started importing some standard stuff
import argparse
import os.path
import sys
# we also need some stuff from our project
from incload import globals

class ArgumentParser(object):
  # the constructor will initialize the parser and add all arguments to it
  def __init__(self):
    self.__Parser=argparse.ArgumentParser()
    self.__Parser.add_argument("-o","--output",help="set the corresponding output directory",type=str)
  # the execute method will execute the parsing and invoke all following stuff
  def execute(self):
    args=self.__Parser.parse_args()
    # output directory definition
    if args.output:
      globals.OutputDirectory=args.output
    if not os.path.exists(globals.OutputDirectory): # failure if not existing
      print "This output directory doesn't exist."
      sys.exit(1)
