class SongParser(object):
  def __init__(self):
    pass
  def feed(self, data):
    self.SongTitle=data["title"]
    self.Genre=data["genre"]
    self.Link = data["link"]

  def handle_starttag(self, tag, attr):
    if tag=="a":
      sid=self.getAttribute(attr, "id")
      if sid=="musicdownloadbutton":
        self.Link=self.getAttribute(attr, "href")
