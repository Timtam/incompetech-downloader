# implements the parser to parse the single-song-page and retrieve relevant information
from incload.parsers import baseparser

class SongParser(baseparser.BaseParser):
  # the constructor as always
  def __init__(self):
    baseparser.BaseParser.__init__(self)
    self.__Parsing=False
    self.__ParseTitle=False
    self.__ParseGenre=False
    self.__Link=""
    self.__SongTitle=""
    self.__Genre=""
  # the usual overriding parse handlers
  def handle_starttag(self,tag,attr):
    # we need to get the relevant tbody tag and define that we want to start parsing now
    if not self.__Parsing and tag=="tbody" and self.getAttribute(attr,"class")=="filtered-song-list-body":
      self.__Parsing=True
      return
    if self.__Parsing:
      # do further parsing here
      # lets start parsing the song title
      if tag=="tr" and self.getAttribute(attr,"class")=="search-result-row expanded ":
        self.__ParseTitle=True
        return
      # continuing to parse the file link
      if tag=="a":
        # get relevant attribute
        href=self.getAttribute(attr,"href")
        if href.endswith(".mp3"):
          # it might happen that the paths are relative
          if not href.startswith("http"):
            href="http://incompetech.com%s"%href
          self.__Link=href
          return
      
  # the end tag detection will disable unnecessary parsing
  def handle_endtag(self,tag):
    # and disable it
    if tag=="tbody":
      self.__Parsing=False
  # parsing some internal data
  def handle_data(self,data):
    # if no data is specified, skipping
    if self.isEmpty(data):
      return
    # if parsing the title is allowed, we accept it as the song title
    if self.__ParseTitle:
      self.__SongTitle=data
      self.__ParseTitle=False
      return
    # continue parsing the genre
    if self.__ParseGenre:
      self.__Genre=data
      self.__ParseGenre=False
      return
    if self.__Parsing:
      if data.endswith("bpm"):
        self.__ParseGenre=True
        return
  @property
  def Link(self):
    return self.__Link
  @property
  def SongTitle(self):
    return self.__SongTitle
  @property
  def Genre(self):
    return self.__Genre