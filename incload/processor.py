# necessary hack to prevent naming breaks
glob=globals
# processor
# the main program which executes the full download process
# we will actually need some importings
# at first these from the standard lib
import os.path
import sys
import types
# then the ones we developed
from incload.downloader import Downloader
from incload import globals

class Processor(object):
  # all chars forbidden in file names
  ForbiddenChars=r'<>?":|\/*'
  def __init__(self):
    # allocating some variables
    self.dlMaxCount=0
    self.dlCount=0
  # will automatically remove all forbidden characters and replace them with underscores
  def formatFilename(self,filename):
    for c in self.ForbiddenChars:
      filename=filename.replace(c, '_')
    return filename
  # anyway, execution will be needed
  def execute(self):
    # we check if we actually support the site the user wants to download from
    requiredparsers=["SongParser"]
    if globals.Sort==globals.SORT_ALPHABETICAL: requiredparsers.append("FullAlphabeticalParser")
    elif globals.Sort==globals.SORT_DATE: requiredparsers.append("FullDateParser")
    try:
      parsers=__import__("incload.parsers.%s"%globals.Page, glob(), locals(), requiredparsers, -1)
      for p in requiredparsers:
        getattr(parsers, p)
    except ImportError:
      print "This site isn't supported yet."
      return
    except AttributeError:
      print "This page doesn't support your wanted sorting scheme yet."
      return
    # at first we need to identify the url to use by scanning the selected sorting scheme
    if globals.Sort==globals.SORT_ALPHABETICAL:
      parser=parsers.FullAlphabeticalParser()
    elif globals.Sort==globals.SORT_DATE:
      parser=parsers.FullDateParser()
    # let's get started loading the list
    downloader=Downloader(parser.Source)
    # we don't need call() here, since incompetech doesn't deliver Content-Length and additional information for web pages
    try:
      downloader.start()
      print "Downloading song list..."
      downloader.wait()
    except KeyboardInterrupt:
      downloader.stop()
      raise KeyboardInterrupt()
    print "Parsing song list..."
    parser.feed(downloader.read())
    links=parser.Result
    if globals.ReverseList:
      links=links[::-1]
    # we finished parsing, let's get started downloading
    # to create some statistics
    self.dlMaxCount=len(links)
    print "Finished song parsing. Found %d songs to download"%self.dlMaxCount
    for i in range(len(links)):
      # defining link
      link=links[i]
      # we need to download the song page first
      # but only if we actually got downloadable links from the parser
      # otherwise we pass it to the parser directly
      if type(link)==types.StringType:
        downloader=Downloader(link)
        try:
          downloader.start()
          print "Downloading song %d"%(i+1)
          downloader.wait()
        except KeyboardInterrupt:
          downloader.stop()
          raise KeyboardInterrupt()
      # and now parse the page
      print "Parsing page for song %d"%(i+1)
      parser=parsers.SongParser()
      if type(link)==types.StringType:
        parser.feed(downloader.read())
      else:
        parser.feed(link)
      print "Detected song:"
      print "\tTitle: %s"%parser.SongTitle
      print "\tGenre: %s"%parser.Genre
      # time to construct the actual download target and create folders if needed
      downloadfolder=os.path.abspath(globals.OutputDirectory)
      if globals.DownloadByGenre:
        downloadfolder=os.path.join(downloadfolder,self.formatFilename(parser.Genre))
      if not os.path.exists(downloadfolder):
        # we will have to create it
        try:
          os.mkdirs(downloadfolder)
        except (OSError, IOError):
          print "An error ocurred while creating the download folder. Please fix this error and try again"
          sys.exit(1)
      downloadfile=os.path.join(downloadfolder,self.formatFilename(parser.SongTitle)+".mp3")
      if os.path.exists(downloadfile):
        print "This file already exists."
        continue
      # let's get the actually important downloader ready :)
      downloader=Downloader(parser.Link)
      downloader.call()
      try:
        downloader.start()
        # and show some progress indicator
        downloader.showProgress()
      except KeyboardInterrupt:
        downloader.stop()
        raise KeyboardInterrupt()
      # and after that, save the file
      downloader.write(downloadfile,True)
      print "Finished!"
      self.dlCount=self.dlCount+1

  # needed to display statistics at the end of the process
  def printStatistics(self):
    if self.dlMaxCount==0:
      print "No statistical information available!"
    else:
      print "Downloaded %d files out of %d files (%.02f%%)"%(self.dlCount, self.dlMaxCount, float(self.dlCount)*100/float(self.dlMaxCount))

