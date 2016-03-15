"""
imcompetech-downloader
written by Toni Barth (Timtam)
pull requests are welcome
"""

# this program will just call some internals to parse stuff and process the actual download
# but we'll need imports anyway
from incload.argumentparser import ArgumentParser
from incload.processor import Processor

# we kick off creating an ArgumentParser instance and executing it
parser=ArgumentParser()
parser.execute()
# these two lines executed the whole command-line processing and put parameters into place
# creating and executing the processor now will be everything we need
# but we will also handle some exceptions which would be problematical to handle inside the processor
processor=Processor()
try:
  processor.execute()
except KeyboardInterrupt:
  print "User interruption encountered."
print "Finished downloading. Have fun!"