from incload.parsers import baseparser
from incload import downloader
import re

class SongParser(baseparser.BaseParser):
  __REGenre="View (\w+) List Page"
  def __init__(self):
    baseparser.BaseParser.__init__(self)
    self.__GenreIdentifier=re.compile(self.__REGenre)
    self.Genre=""
    self.SongTitle=""
    self.Link=""
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
    if tag=="li":
      title=self.getAttribute(attr, "title")
      if title:
        mgenre=self.__GenreIdentifier.match(title)
        if mgenre:
          self.Genre=mgenre.group(1)
    elif tag=="a":
      sclass=self.getAttribute(attr, "class")
      if sclass=="downloadblock":
        self.Link=self.getAttribute(attr, "href")
