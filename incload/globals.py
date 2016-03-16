# globals.py
# stores everything which needs to be publically known for more than one module
# should be seen as a more or less constant namespace
# here everything important should be declared, so that everything just needs this module to operate effectively
# by importing this including it's namespace it's possible to see and change everything another module did in here

# the amount of bytes to download at once
ChunkSize=128*1024
# sort the downloaded files into the specific genre folders?
DownloadByGenre=False
# the path to the full list of incompetech
FullList="/music/royalty-free/full_list.php"
# the incompetech base url
Incompetech="http://incompetech.com"
# needed to identify the catalog number in some submodules
# it's a regexp
ISRC="USUAN\d+"
# contains the path to the ISRC list on incompetech
# contains all the music sorted by date
ISRCList="/music/royalty-free/isrc_to_name.php"
# self-explanatory
OutputDirectory="./"
# reversing the download list can be activated here
ReverseList=False
# the sorting flags
SORT_ALPHABETICAL="alphabetical"
SORT_DATE="date"
# the sort status
Sort=SORT_ALPHABETICAL
# the web user-agent to be used while connecting to incompetech
# will be used by the downloading interface
UserAgent="Incompetech Downloader"