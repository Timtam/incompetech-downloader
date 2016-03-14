# globals.py
# stores everything which needs to be publically known for more than one module
# should be seen as a more or less constant namespace
# here everything important should be declared, so that everything just needs this module to operate effectively
# by importing this including it's namespace it's possible to see and change everything another module did in here

# the path to the full list of incompetech
FullList="http://incompetech.com/music/royalty-free/full_list.php"
# needed to identify the catalog number in some submodules
# it's a regexp
ISRC="USUAN\d+"
OutputDirectory=""