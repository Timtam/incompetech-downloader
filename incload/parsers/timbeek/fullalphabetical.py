from .fulldate import FullDateParser

class FullAlphabeticalParser(FullDateParser):
  @property
  def Result(self):
    idict={}
    for i in range(len(self._Results)):
      idict[self._Results[i]["title"]]=i
    l=[]
    for t in sorted(idict.keys()):
      l.append(self._Results[idict[t]]["link"])
    return l
