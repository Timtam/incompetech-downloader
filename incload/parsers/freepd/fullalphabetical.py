from incload import downloader
from incload.parsers import baseparser
import urllib

class FullAlphabeticalParser(baseparser.BaseParser):
  Source="http://freepd.com"
  def __init__(self):
    baseparser.BaseParser.__init__(self)
    self.__DetectionLevel=0
    self.__Genres={}
    self.__Results={}
    self.__ParseGenres=False
    self.__ParseSong=False
    self.__Genre=""
    self.__GenreLink=""
    
  def feed(self, data):
    baseparser.BaseParser.feed(self, data)
    if self.__DetectionLevel==0:
      self.__DetectionLevel=1
      for genre in sorted(self.__Genres.keys()):
        dl=downloader.Downloader(self.Source+self.__Genres[genre])
        print "Downloading page for genre '%s'"%genre
        try:
          dl.start()
          dl.wait()
        except KeyboardInterrupt:
          dl.stop()
          raise KeyboardInterrupt()
        print "Parsing page for genre '%s'"%genre
        self.__Genre=genre
        self.feed(dl.read())

  def handle_starttag(self, tag, attr):
    if self.__DetectionLevel==0:
      if self.__ParseGenres==False and tag == "div" and self.getAttribute(attr, "id")=="categories":
        self.__ParseGenres=True
      elif self.__ParseGenres==True and tag == "a":
        self.__GenreLink=self.getAttribute(attr, "href")
    elif self.__DetectionLevel==1:
      if self.__ParseSong==False and tag == "div" and self.getAttribute(attr, "class")=="title":
        self.__ParseSong=True
      elif self.__ParseSong==True and tag == "a":
        self.__Results[self.getAttribute(attr, "href")]={"title":self.getAttribute(attr, "href"), "link":self.Source+self.__Genres[self.__Genre]+"/"+urllib.quote(self.getAttribute(attr, "href"))+".mp3", "genre":self.__Genre}

  def handle_endtag(self, tag):
    if self.__DetectionLevel==0:
      if self.__ParseGenres==True and tag == "div":
        self.__ParseGenres=False
    elif self.__DetectionLevel==1:
      if self.__ParseSong==True and tag=="div":
        self.__ParseSong=False

  def handle_data(self, data):
    if self.__DetectionLevel==0:
      if self.__GenreLink and data != "download":
        self.__Genres[data]=self.__GenreLink
      self.__GenreLink=""

  @property
  def Result(self):
    ordered=sorted(self.__Results.keys())
    for i in range(len(ordered)):
      ordered[i]=self.__Results[ordered[i]]
    return ordered