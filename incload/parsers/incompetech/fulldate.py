# this parser uses exactly the same engine as the fullalphabeitcal does, so we import and overwrite some important attributes
from .fullalphabetical import FullAlphabeticalParser

class FullDateParser(FullAlphabeticalParser):
  # we just need to set the new path
  Source="http://incompetech.com/music/royalty-free/isrc_to_name.php"
