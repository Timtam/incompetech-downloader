# necessary hack to prevent naming breaks
glob=globals
# processor
# the main program which executes the full download process
# we will actually need some importings
# at first these from the standard lib
import os.path
import sys
# then the ones we developed
from incload.downloader import Downloader
from incload import globals

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
    # we check if we actually support the site the user wants to download from
    try:
      parsers=__import__("incload.parsers.%s"%globals.Page, glob(), locals(), ["FullAlphabeticalParser", "FullDateParser", "SongParser"], -1)
    except ImportError:
      print "Downloading from this site isn't supported yet. Check your spelling or otherwise open a ticket on GitHub so we can impplement it."
      return
    # at first we need to identify the url to use by scanning the selected sorting scheme
#    try:
    if globals.Sort==globals.SORT_ALPHABETICAL:
      parser=parsers.FullAlphabeticalParser()
    elif globals.Sort==globals.SORT_DATE:
      parser=parsers.FullDateParser()
#    except AttributeError:
#      print "We already support downloading from this site, but this site doesn't support this sorting scheme yet."
#      return
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
    print "Finished song parsing. Found %d songs to download"%len(links)
    for i in range(len(links)):
      # defining link
      link=links[i]
      # we need to download the song page first
      # doing that, we will need to construct the full link by concatenating them
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
