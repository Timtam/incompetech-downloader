from incload.parsers import baseparser
import re

class FullDateParser(baseparser.BaseParser):
  Source="http://timbeek.com/royalty-free-music/isrc/"
  __ISRC="NL-A5R-\d{2}-\d+"
  def __init__(self):
    baseparser.BaseParser.__init__(self)
    self.__REISRC=re.compile(self.__ISRC)
    self._Results=[]
    self.__Link=""
    self.__ParseTitle=False
  def handle_starttag(self, tag, attr):
    if tag == "a":
      self.__Link=self.getAttribute(attr, "href")
      self.__ParseTitle=False
  def handle_data(self, data):
    if self.isEmpty(data): return
    if self.__ParseTitle:
      self._Results.append({"title":data.strip(), "link":self.__Link})
      self.__Link=""
      self.__ParseTitle=False
      return
    if self.__Link:
      m=self.__REISRC.match(data)
      if m:
        self.__ParseTitle=True
  @property
  def Result(self):
    return [i["link"] for i in self._Results]
