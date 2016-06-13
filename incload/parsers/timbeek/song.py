from incload.parsers import baseparser

class SongParser(baseparser.BaseParser):
  def __init__(self):
    baseparser.BaseParser.__init__(self)
    self.__ParseTitle=False
    self.__ParseGenre=0
    self.SongTitle=""
  def handle_starttag(self, tag, attr):
    if tag=="h1" and self.getAttribute(attr, "class")=="entry-title":
      self.__ParseTitle=True
    elif tag=="td" and self.getAttribute(attr, "id")=="musicData":
      self.__ParseGenre=1
    elif tag=="source" and self.getAttribute(attr, "type")=="audio/mpeg":
      self.Link=self.getAttribute(attr, "src")
  def handle_data(self, data):
    if self.__ParseTitle:
      if self.SongTitle=="":
        self.SongTitle=data
      else:
        self.SongTitle=self.SongTitle+"_"+data
    elif self.__ParseGenre==1:
      self.__ParseGenre=2
    elif self.__ParseGenre==2:
      self.Genre=data
      self.__ParseGenre=0
  def handle_endtag(self, tag):
    if self.__ParseTitle and tag=="h1":
      self.__ParseTitle=False