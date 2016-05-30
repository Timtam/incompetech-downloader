from incload import downloader
from incload.parsers import baseparser

class FullAlphabeticalParser(baseparser.BaseParser):
  Source="http://audionautix.com"
  def __init__(self):
    baseparser.BaseParser.__init__(self)
    self.__DetectionLevel=0
    self.__Genres={}
    self.__Results={}
    self.__ParsingSongs=False
    self.__ParsingTitle=False
    self.__ParsingGenre=False
    self.__Title=""
    self.__Genre=""
  def feed(self, data):
    baseparser.BaseParser.feed(self, data)
    if self.__DetectionLevel==0:
      self.__DetectionLevel=1
      for genre in sorted(self.__Genres.keys()):
        dl=downloader.Downloader(self.Source, {"action":"search", "hptrack": "", "submit": " Find Music ", "genre": self.__Genres[genre]})
        print "Downloading page for genre '%s'"%genre
        try:
          dl.start()
          dl.wait()
        except KeyboardInterrupt:
          dl.stop()
          raise KeyboardInterrupt()
        print "Parsing page for genre '%s'"%genre
        self.feed(dl.read())
  def handle_starttag(self, tag, attr):
    if self.__DetectionLevel==0:
      if tag=="input":
        stype=self.getAttribute(attr, "type")
        sname=self.getAttribute(attr, "name")
        if stype=="radio" and sname=="genre":
          sid=self.getAttribute(attr, "id")
          svalue=self.getAttribute(attr, "value")
          if not sid in self.__Genres:
            self.__Genres[sid]=svalue
    else:
      if not self.__ParsingSongs:
        if tag=="ul":
          sclass=self.getAttribute(attr, "class")
          if sclass=="search-result pull-left":
            self.__ParsingSongs=True
      else:
        if tag=="h2":
          self.__ParsingTitle=True
        elif tag=="a":
          sclass=self.getAttribute(attr, "class")
          if sclass=="download":
            nsong={}
            nsong['genre']=self.__Genre
            nsong['title']=self.__Title
            nsong['link']="%s%s"%(self.Source, self.getAttribute(attr, "href"))
            self.__Results[self.__Title]=nsong
  def handle_endtag(self, tag):
    if self.__ParsingSongs and tag=="ul":
      self.__ParsingSongs=False

  def handle_data(self, data):
    if self.__ParsingSongs:
      if self.__ParsingTitle:
        self.__Title=data
        self.__ParsingTitle=False
        return
      if data=="Genre:" and not self.__ParsingGenre:
        self.__ParsingGenre=True
        return
      if self.__ParsingGenre:
        self.__Genre=data.strip()
        self.__ParsingGenre=False

  @property
  def Result(self):
    ordered=sorted(self.__Results.keys())
    l=[]
    for o in ordered:
      l.append(self.__Results[o])
    return l