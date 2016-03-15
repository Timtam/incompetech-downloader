# downloading utilities for incload
# a wrapper which uses urllib2 (on python2) and threading module to provide a parallelly running downloading interface
# the downloaded stuff will at first be stored in a StringIO buffer object
import StringIO
# some output capabilities
import sys
# for sleeping functionalities ;)
import time
# for multi-threading purposes
import threading
# for internet access
import urllib2
# and the globals, as always
from incload import globals

class Downloader(threading.Thread):
  # constructor which also accepts an url
  def __init__(self, url):
    # parent-class constructor call
    threading.Thread.__init__(self)
    # some properties, as always
    self.__Url=url
    self.__Filesize=0
    self.__Downloaded=0
    self.__Buffer=StringIO.StringIO()
    self.__Running=False
    # some locks to prevent ... locks? :)
    self.__RetrievalLock=threading.Lock()
    # and an event to support stopping
    self.__StopEvent=threading.Event()
  # this small method will create a request for us
  def __getrequest(self):
    return urllib2.Request(self.__Url, None, {'User-Agent': globals.UserAgent})
  # used to call the corresponding page and get some information like file size and stuff
  def call(self):
    # open urllib2 object and try your best
    request=self.__getrequest()
    try:
      connection=urllib2.urlopen(request)
      self.__Filesize=int(connection.info().getheaders("Content-Length")[0])
      connection.close()
    except:
      # in this case, our best wasn't enough
      return False
    return True
  # will run the actual download process
  def run(self):
    self.__Running=True
    # get request and open the url respectively
    request=self.__getrequest()
    connection=urllib2.urlopen(request)
    # get small chunks and write them to our buffer
    # don't forget to lock up while doing this
    chunk=connection.read(globals.ChunkSize)
    while chunk:
      # if stop command is set
      if self.__StopEvent.isSet():
        self.__Buffer.close()
        self.__Running=False
        break
      self.__RetrievalLock.acquire()
      self.__Downloaded=self.__Downloaded+len(chunk)
      self.__Buffer.write(chunk)
      chunk=connection.read(globals.ChunkSize)
      self.__RetrievalLock.release()
    connection.close()
    self.__Running=False
  # we support download canceling
  def stop(self):
    self.__RetrievealLock.acquire()
    self.__StopEvent.set()
    self.__RetrievalLock.release()
  # we also support retrieval to process it further inside of python
  def read(self):
    # if the download is still running, don't do it
    if self.Running:
      return ""
    self.__Buffer.seek(0)
    return self.__Buffer.read()
  # but also writing to file directly
  def write(self, filename, binary=False):
    # if the download is still running, don't do it
    if self.Running: 
      return False
    # construct the opening mode
    mode="w"+("b" if binary else "")
    file=open(filename,mode)
    self.__Buffer.seek(0)
    file.write(self.__Buffer.read())
    return True
  # we also support some progress indicator
  # it can be called to progress the download progress while running
  # it of course doesn't run multi-threaded
  def showProgress(self):
    # if we aren't actually running, we stop this desaster
    if not self.Running: return
    # show some stuff to fill our progress line
    sys.stdout.write("")
    # the displaying loop
    while self.Running:
      percentage=self.Downloaded*100/self.FullSize
      displaying=globals.ProgressBarLength*percentage/100
      sys.stdout.write("\r%s"%("%"*displaying))
      time.sleep(1.0)
    sys.stdout.write("\n")
  # some properties to retrieve data like remaining size and stuff
  @property
  def FullSize(self):
    return self.__Filesize
  @property
  def DownloadedSize(self):
    self.__RetrievalLock.acquire()
    size=self.__Downloaded
    self.__RetrievalLock.release()
    return size
  @property
  def RemainingSize(self):
    return self.FullSize-self.DownloadedSize
  @property
  def Running(self):
    self.__RetrievalLock.acquire()
    state=self.__Running
    self.__RetrievalLock.release()
    return state