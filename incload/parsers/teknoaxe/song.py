from incload.parsers import baseparser
from incload import downloader
from incload.exceptions import SongParseError

class SongParser(baseparser.BaseParser):
  def __init__(self):
    baseparser.BaseParser.__init__(self)
    self.Genre=""
    self.SongTitle=""
    self.Link=""
  def feed(self, data):
    self.SongTitle=data["title"]
    self.Genre=data["genre"]
    dl=downloader.Downloader(data["link"])
    try:
      dl.start()
      dl.wait()
    except KeyboardInterrupt:
      dl.stop()
      raise KeyboardInterrupt()
    baseparser.BaseParser.feed(self, dl.read())

  def handle_starttag(self, tag, attr):
    if tag=="a":
      sid=self.getAttribute(attr, "id")
      if sid=="musicdownloadbutton":
        self.Link=self.getAttribute(attr, "href")
