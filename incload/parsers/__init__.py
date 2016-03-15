"""
incload.parsers package

This package contains all neded html parsers needed to operate with incompetech.com
For example the full-list parser and the songpage parser.
"""
from .fulllist import Parser as FullListParser
from .songpage import Parser as SongPageParser