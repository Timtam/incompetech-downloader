# the joshwoodward.com full alphabetical parser
import json

class FullAlphabeticalParser(object):
  Source="https://www.joshwoodward.com/mod/song/view-artist-2/ajax/get-songs.php"
  def __init__(self):
    self.__Results={}
  def feed(self, data):
    songs=json.loads(data)
    for song in songs.values():
      nsong={}
      nsong['genre']=song['genre']
      nsong['title']=song['name']
      nsong['link']="https://joshwoodward.com/mod/song/force-download.php?file=%s"%song['mp3']
      self.__Results[song['name']]=nsong
      if song['instrumental_mp3']:
        nsong={}
        nsong['genre']=song['genre']
        nsong['title']="%s (instrumental)"%song['name']
        nsong['link']="https://joshwoodward.com/mod/song/force-download.php?file=%s"%song['instrumental_mp3']
        self.__Results["%s (instrumental)"%(song['name'])]=nsong
  @property
  def Result(self):
    order=sorted(self.__Results.keys())
    l=[]
    for o in order:
      l.append(self.__Results[o])
    return l