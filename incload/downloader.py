# downloading utilities for incload
# a wrapper which uses urllib2 (on python2) and threading module to provide a parallelly running downloading interface
# the hard way of life
import ssl
# the downloaded stuff will at first be stored in a StringIO buffer object
import StringIO
# some output capabilities
import sys
# for sleeping functionalities ;)
import time
# for multi-threading purposes
import threading
# for internet access
import urllib
import urllib2
# and the globals, as always
from incload import globals

class Downloader(threading.Thread):
  # constructor which also accepts an url and post data
  def __init__(self, url, post=None):
    # parent-class constructor call
    threading.Thread.__init__(self)
    # some properties, as always
    self.__Url=url
    if post:
      self.__Post=urllib.urlencode(post)
    else:
      self.__Post=post
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
    return urllib2.Request(self.__Url, self.__Post, {'User-Agent': globals.UserAgent})
  # ssl contexts (needed to bypass certificate checking)
  def __getcontext(self):
    return ssl.SSLContext(ssl.PROTOCOL_TLSv1)
  # used to call the corresponding page and get some information like file size and stuff
  def call(self):
    # open urllib2 object and try your best
    try:
      request=self.__getrequest()
      connection=urllib2.urlopen(request, context=self.__getcontext())
      try:
        self.__Filesize=int(connection.info().getheaders("Content-Length")[0])
      except IndexError:
        # the download will work, but no header information containing the actual file size is available
        pass
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
    connection=urllib2.urlopen(request, context=self.__getcontext())
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
      self.__RetrievalLock.release()
      chunk=connection.read(globals.ChunkSize)
    connection.close()
    self.__Running=False
  # we support download canceling
  def stop(self):
    self.__RetrievalLock.acquire()
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
    file.close()
    return True
  # we also support some progress indicator
  # it can be called to progress the download progress while running
  # it of course doesn't run multi-threaded
  def showProgress(self):
    # while this class is actually an alive thread but download is not running yet, wait until this is the case
    while self.isAlive() and not self.Running:
      time.sleep(0.01)
    # if we aren't actually running, we stop this desaster (meaning we already finished)
    if not self.Running:
      return
    # show some stuff to fill our progress line
    sys.stdout.write("")
    # the displaying loop
    try:
      while self.Running:
        line="\rDownloading... "
        if self.FullSize:
          percentage=self.DownloadedSize*100/self.FullSize
          line=line+"%d%% finished"%percentage
        else:
          line=line+"Remaining size unknown"
        line=line+" "*(40-len(line))
        sys.stdout.write(line)
        time.sleep(1.0)
    finally:
      sys.stdout.write("\n")
  # we can wait until the downloader actually finished
  def wait(self):
    # this means we wait while the download is running or the thread is about to start the download
    while self.isAlive() or self.Running:
      time.sleep(0.01)
  # some properties to retrieve data like remaining size and stuff
  @property
  def FullSize(self):
    return self.__Filesize
  @property
  def DownloadedSize(self):
    try:
      self.__RetrievalLock.acquire()
      size=self.__Downloaded
      self.__RetrievalLock.release()
      return size
    except KeyboardInterrupt:
      self.__RetrievalLock.release()
      raise KeyboardInterrupt()
  @property
  def RemainingSize(self):
    return self.FullSize-self.DownloadedSize
  @property
  def Running(self):
    try:
      self.__RetrievalLock.acquire()
      state=self.__Running
      self.__RetrievalLock.release()
      return state
    except KeyboardInterrupt:
      self.__RetrievalLock.release()
      raise KeyboardInterrupt()