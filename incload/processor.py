# processor
# the main program which executes the full download process
# we will actually need some importings
# at first these from the standard lib
import os.path
import time
# then the ones we developed
from incload.downloader import Downloader
from incload import globals
from incload.parsers import FullListParser, SongPageParser

class Processor(object):
  # constructor not needed yet
  # anyway, execution will be needed
  def execute(self):
    # let's get started loading the full list
    downloader=Downloader(globals.Incompetech+globals.FullList)
    # we don't need call() here, since incompetech doesn't deliver Content-Length and additional information for web pages
    downloader.start()
    print "Downloading song list..."
    while downloader.Running:
      time.sleep(0.05)
    print "Parsing song list..."
    parser=FullListParser()
    parser.feed(downloader.read())
    links=parser.Result
    # we finished parsing, let's get started downloading
    print "Finished song parsing. Found %d songs to download"%len(links)
    for i in range(len(links)):
      # defining link
      link=links[i]
      # we need to download the song page first
      # doing that, we will need to construct the full link by concatenating them
      downloader=Downloader(globals.Incompetech+link)
      downloader.start()
      print "Downloading song %d"%(i+1)
      while downloader.Running:
        time.sleep(0.05)
      # and now parse the page
      print "Parsing page for song %d"%(i+1)
      parser=SongPageParser()
      parser.feed(downloader.read())
      print "Detected song:"
      print "\tTitle: %s"%parser.SongTitle
      print "\tGenre: %s"%parser.Genre
      # let's get the actually important downloader ready :)
      downloader=Downloader(globals.Incompetech+parser.Link)
      downloader.call()
      downloader.start()
      # and show some progress indicator
      downloader.showProgress()
      # and after that, save the file
      downloader.write(os.path.abspath(os.path.join(globals.OutputDirectory,parser.SongTitle+".mp3")),True)
      print "Finished!"
