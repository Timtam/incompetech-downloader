# processor
# the main program which executes the full download process
# we will actually need some importings
# at first these from the standard lib
import os.path
import sys
# then the ones we developed
from incload.downloader import Downloader
from incload import globals
from incload.parsers import FullListParser, SongPageParser

class Processor(object):
  # all chars forbidden in file names
  ForbiddenChars=r'<>?":|\/*'
  # constructor not needed yet
  # will automatically remove all forbidden characters and replace them with underscores
  def formatFilename(self,filename):
    for c in self.ForbiddenChars:
      filename=filename.replace(c, '_')
    return filename
  # anyway, execution will be needed
  def execute(self):
    # at first we need to identify the url to use by scanning the selected sorting scheme
    if globals.Sort==globals.SORT_ALPHABETICAL:
      link=globals.FullList
    elif globals.Sort==globals.SORT_DATE:
      link=globals.ISRCList
    # let's get started loading the list
    downloader=Downloader(globals.Incompetech+link)
    # we don't need call() here, since incompetech doesn't deliver Content-Length and additional information for web pages
    try:
      downloader.start()
      print "Downloading song list..."
      downloader.wait()
    except KeyboardInterrupt:
      downloader.stop()
      raise KeyboardInterrupt()
    print "Parsing song list..."
    parser=FullListParser()
    parser.feed(downloader.read())
    links=parser.Result
    if globals.ReverseList:
      links=links[::-1]
    # we finished parsing, let's get started downloading
    print "Finished song parsing. Found %d songs to download"%len(links)
    for i in range(len(links)):
      # defining link
      link=links[i]
      # we need to download the song page first
      # doing that, we will need to construct the full link by concatenating them
      downloader=Downloader(globals.Incompetech+link)
      try:
        downloader.start()
        print "Downloading song %d"%(i+1)
        downloader.wait()
      except KeyboardInterrupt:
        downloader.stop()
        raise KeyboardInterrupt()
      # and now parse the page
      print "Parsing page for song %d"%(i+1)
      parser=SongPageParser()
      parser.feed(downloader.read())
      print "Detected song:"
      print "\tTitle: %s"%parser.SongTitle
      print "\tGenre: %s"%parser.Genre
      # time to construct the actual download target and create folders if needed
      downloadfolder=os.path.abspath(globals.OutputDirectory)
      if globals.DownloadByGenre:
        downloadfolder=os.path.join(downloadfolder,parser.Genre)
      if not os.path.exists(downloadfolder):
        # we will have to create it
        try:
          os.mkdir(downloadfolder)
        except (OSError, IOError):
          print "An error ocurred while creating the download folder. Please fix this error and try again"
          sys.exit(1)
      downloadfile=os.path.join(downloadfolder,self.formatFilename(parser.SongTitle)+".mp3")
      if os.path.exists(downloadfile):
        print "This file already exists."
        continue
      # let's get the actually important downloader ready :)
      downloader=Downloader(globals.Incompetech+parser.Link)
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
