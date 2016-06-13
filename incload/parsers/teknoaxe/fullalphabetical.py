from incload.parsers import baseparser
from incload import downloader

class FullAlphabeticalParser(baseparser.BaseParser):
  Source="http://teknoaxe.com/Home.php"
  def __init__(self):
    baseparser.BaseParser.__init__(self)
    self.__DetectionLevel=0
    self.__Category=""
    self.__Categories={}
    self.__Genre=""
    self.__Genres={}
    self.__Song=""
    self.__Songs={}
    self.__FooterItemCount=0
  def feed(self, data):
    baseparser.BaseParser.feed(self, data)
    if self.__DetectionLevel==0:
      self.__DetectionLevel=1
      for category in sorted(self.__Categories.keys()):
        print "Downloading genre list for category '%s'"%category
        dl=downloader.Downloader(self.__Categories[category])
        try:
          dl.start()
          dl.wait()
        except KeyboardInterrupt:
          dl.stop()
          raise KeyboardInterrupt()
        print "Parsing genre list for category '%s'"%category
        self.feed(dl.read())
      self.__DetectionLevel=2
      for self.__Genre in sorted(self.__Genres.keys()):
        print "Downloading song list for genre '%s'"%self.__Genre
        dl=downloader.Downloader(self.__Genres[self.__Genre])
        try:
          dl.start()
          dl.wait()
        except KeyboardInterrupt:
          dl.stop()
          raise KeyboardInterrupt()
        print "Parsing song list for genre '%s'"%self.__Genre
        self.feed(dl.read())

  def handle_starttag(self, tag, attr):
    if self.__DetectionLevel==0:
      if self.__FooterItemCount==2:
        if tag=="a":
          self.__Category=self.getAttribute(attr, "href")
          return
      if tag=="div":
        sclass=self.getAttribute(attr, "class")
        if sclass=="footeritem":
          self.__FooterItemCount=self.__FooterItemCount+1
    elif self.__DetectionLevel==1:
      if tag=="a":
        sclass=self.getAttribute(attr, "class")
        if sclass=="musiclink":
          self.__Genre=self.getAttribute(attr, "href")
    elif self.__DetectionLevel==2:
      if tag=="a":
        sclass=self.getAttribute(attr, "class")
        if sclass=="genre_post":
          self.__Song=self.getAttribute(attr, "href")
      elif tag=="img":
        sclass=self.getAttribute(attr, "class")
        if sclass=="genre_image":
          salt=self.getAttribute(attr, "alt")
          salt=salt.split(":")[1]
          if not salt in self.__Songs or (self.__Songs[salt]["genre"] in self.__Categories and self.__Genre not in self.__Categories):
            self.__Songs[salt]={"link":self.__Song, "title":salt, "genre":self.__Genre}
          self.__Song=""
  def handle_data(self, data):
    if self.__DetectionLevel==0 and self.__FooterItemCount==2 and self.__Category:
      if data != "Music" and data != "Commission":
        self.__Categories[data]=self.__Category
      self.__Category=""
    elif self.__DetectionLevel==1 and self.__Genre:
      self.__Genres[data]=self.__Genre
      self.__Genre=""
  @property
  def Result(self):
    ordered=sorted(self.__Songs.keys())
    l=[]
    for o in ordered:
      l.append(self.__Songs[o])
    return l