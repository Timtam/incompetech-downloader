# this parser parses the full list of songs available at incompetech.com
# we need to implement the HTMLParser interface
# for now it is only python 2 compatible, pull requests welcome
import HTMLParser
# regular expressions will also be needed
import re
# we need some exceptions here
from incload.exceptions import ParseError
# and the globals too
from incload import globals

class Parser(HTMLParser.HTMLParser):
  # for this class, we'll need some constructor
  def __init__(self):
    # safety first, call the parent class constructor too
    HTMLParser.HTMLParser.__init__(self)
    # now we need to declare some important variables
    self.__Link=""
    self.__OpenTag=False
    self.__ResultList=[]    
    # at least we need to compile our regular expression later used to identify relevant links
    self.__Identifier=re.compile(globals.ISRC)
  # as you should know if you're familiar with the HTMLParser concept,
  # you need to re-declare important methods so you get notified if some important stuff was found
  # so, let's do that here
  def handle_starttag(self, tag,attr):
    # for this page, only the a tags are interesting for us.
    # also, they need to contain some catalog identifier in them
    # so, we need to identify a tags, capture their links and let handle_data do the remaining work for us
    if tag=="a":
      # we need to find the href attribute, if any
      for i in range(len(attr)):
        if attr[i][0]=="href":
          self.__OpenTag=True
          self.__Link=attr[i][1]
          return
    # otherwise we will reset all data
    self.__OpenTag=False
    self.__Link=""
  def handle_data(self, data):
    # the text inside the link needs to match the ISRC identifyer regexp, so let's check that and add the link to the result list if successful
    if self.__Identifier.match(data):
      self.__ResultList.append(self.__Link)
  # finally we need some getter to retrieve the resulting list
  @property
  def Result(self):
    return self.__ResultList
