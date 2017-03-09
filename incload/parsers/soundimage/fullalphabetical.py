import re

from incload.parsers import baseparser
from incload import downloader

class FullAlphabeticalParser(baseparser.BaseParser):
  Source="http://soundimage.org"
  def __init__(self):
    baseparser.BaseParser.__init__(self)
    self.__CurrentGenre=""
    self.__DetectionLevel=0
    self.__GenreLink=""
    self.__Genres={}
    self.__GenreTitle=""
    self.__InvalidGenres=["About","Home","ALBUMS","Virtual Cinema"]
    self.__ParseGenres=False
    self.__SongLink=""
    self.__Songs={}
    self.__SongTitle = ""

  def feed(self, data):
    baseparser.BaseParser.feed(self, data)
    if self.__DetectionLevel == 0:
      self.__DetectionLevel = 1
      for genre in sorted(self.__Genres.keys()):
        print "Downloading genre '%s'"%genre
        dl=downloader.Downloader(self.__Genres[genre])
        try:
          dl.start()
          dl.wait()
        except KeyboardInterrupt:
          dl.stop()
          raise KeyboardInterrupt()
        print "Parsing genre '%s'"%genre
        self.__CurrentGenre=re.sub(r"(\D+)\s+\d+", r"\1", genre)
        data=dl.read()
        data = data.decode("UTF-8")
        self.feed(data)

  def handle_starttag(self, tag, attr):
    if self.__DetectionLevel == 0:
      if tag == "nav" and self.getAttribute(attr, "role") == "navigation" and self.getAttribute(attr, "id") == "access" and self.__ParseGenres == False:
        self.__ParseGenres = True
        return

      if self.__ParseGenres == True and tag == "a":
        self.__GenreLink = self.getAttribute(attr, "href")

    elif self.__DetectionLevel == 1:
      if tag == "a" and self.getAttribute(attr, "href").startswith("http://soundimage.org/wp-content/uploads/"):
        self.__SongLink = self.getAttribute(attr, "href")

  def handle_endtag(self, tag):
    if self.__DetectionLevel == 0:
      if tag == "a" and self.__ParseGenres == True:
        if self.__GenreTitle not in self.__InvalidGenres:
          self.__Genres[self.__GenreTitle]=self.__GenreLink
        self.__GenreLink = ""
        self.__GenreTitle = ""
        return
      if self.__ParseGenres == True and tag == "div":
        self.__ParseGenres = False
    elif self.__DetectionLevel == 1:
      if tag == "a":
        self.__Songs[self.__SongTitle]={"title":self.__SongTitle, "link": self.__SongLink, "genre":self.__CurrentGenre}
        self.__SongLink = ""
        self.__SongTitle = ""

  def handle_data(self, data):
    if self.__DetectionLevel == 0:
      if self.__GenreLink != "":
        self.__GenreTitle += data
    elif self.__DetectionLevel == 1:
      if self.__SongLink != "":
        self.__SongTitle += data

  @property
  def Result(self):
    ordered=sorted(self.__Songs.keys())
    l=[]
    for o in ordered:
      l.append(self.__Songs[o])
    return l