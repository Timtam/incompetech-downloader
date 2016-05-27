class SongParser(object):
  def feed(self,data):
    self.SongTitle=data['title']
    self.Genre=data['genre']
    self.Link=data['link']
