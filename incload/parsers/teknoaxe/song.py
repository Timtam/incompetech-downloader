from incload.parsers import baseparser
from incload import downloader
from incload.exceptions import SongParseError
import re

class SongParser(baseparser.BaseParser):
  __REGenre="More (\w+)"
  def __init__(self):
    baseparser.BaseParser.__init__(self)
    self.__GenreIdentifier=re.compile(self.__REGenre)
    self.Genre=""
    self.SongTitle=""
    self.Link=""
    self.__ParseGenre=False
  def feed(self, data):
    self.SongTitle=data["title"]
    dl=downloader.Downloader(data["link"])
    try:
      dl.start()
      dl.wait()
    except KeyboardInterrupt:
      dl.stop()
      raise KeyboardInterrupt()
    baseparser.BaseParser.feed(self, dl.read())

  def handle_starttag(self, tag, attr):
    if tag=="p":
      sclass=self.getAttribute(attr, "class")
      if sclass=="c2a":
        self.__ParseGenre=True
    elif tag=="a":
      sid=self.getAttribute(attr, "id")
      if sid=="musicdownloadbutton":
        self.Link=self.getAttribute(attr, "href")
  def handle_data(self, data):
    if self.__ParseGenre==True:
      mgenre=self.__GenreIdentifier.match(data)
      if mgenre:
        self.Genre=mgenre.group(1)
      self.__ParseGenre=False
