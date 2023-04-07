"""
Song in VirtualDJ XML database
"""
import re

from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterator, Optional, TYPE_CHECKING

from inflection import underscore
from lxml.etree import _Element    # pylint: disable=no-name-in-module

from ..base import AttributeFormatter

if TYPE_CHECKING:
    from .loader import Database

RE_DRIVE_LETTER_PREFIX = r'^[A-Z]:/'

ELEMENT_SCAN_ATTRIBUTES = (
    'Version',
    'Bpm',
    'AltBpm',
    'Volume',
    'Key',
    'Flag',
)
ELEMENT_SONG_INFO_ATTRIBUTES = (
    'Bitrate',
    'Cover',
    'FirstSeen',
    'LastModified',
    'SongLength',
)

SONG_BOOLEAN_ATTRIBUTES = (
    'cover',
)
SONG_FLOAT_ATTRIBUTES = (
    'song_length',
)
SONG_INTEGER_ATTRIBUTES = (
    'bitrate',
    'file_size',
)
SONG_TIMESTAMP_ATTRIBUTES = (
    'first_seen',
    'last_modified',
)

SCAN_FLOAT_ATTRIBUTES = (
    'bpm',
    'alt_bpm',
    'volume',
)
SCAN_INT_ATTRIBUTES = (
    'flag',
    'version',
)


class Tags(Mapping, AttributeFormatter):
    """
    Tags in VirtualDJ XML database song
    """
    __items__ = Dict[str, str]

    def __init__(self, song, element: _Element) -> None:
        self.song = song
        self.__items__ = {}
        for key, value in element.items():
            attr = underscore(key)
            self.__items__[attr] = self.__format_value__(attr, value)

    def __getitem__(self, key: str) -> str:
        return self.__items__[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.__items__)

    def __len__(self) -> int:
        return len(self.__items__)


# pylint: disable=too-few-public-methods
class Scan(AttributeFormatter):
    """
    Track analysis scan data
    """
    __float_attributes__ = SCAN_FLOAT_ATTRIBUTES
    __integer_attributes__ = SCAN_INT_ATTRIBUTES

    alt_bpm: float
    bpm: float
    flag: int
    key: str
    version: int
    volume: float

    def __init__(self, song, element: _Element) -> None:
        self.song = song
        for xml_attr in ELEMENT_SCAN_ATTRIBUTES:
            attr = underscore(xml_attr)
            setattr(self, attr, self.__format_value__(attr, element.get(xml_attr)))


class Song(AttributeFormatter):
    """
    Song entry in VirtualDJ XML database
    """
    __boolean_attributes__ = SONG_BOOLEAN_ATTRIBUTES
    __float_attributes__ = SONG_FLOAT_ATTRIBUTES
    __integer_attributes__ = SONG_INTEGER_ATTRIBUTES
    __timestamp_attributes__ = SONG_TIMESTAMP_ATTRIBUTES

    database: 'Database'
    file_path: Path
    file_size: Optional[int] = None
    first_seen: Optional[datetime] = None
    last_modified: Optional[datetime] = None
    song_length: Optional[float] = None

    scan: Optional[Scan] = None
    tags: Optional[Tags] = None

    def __init__(self,
                 database: 'Database',
                 file_path: Path,
                 file_size: Optional[int] = None,
                 first_seen: Optional[datetime] = None,
                 last_modified: Optional[datetime] = None,
                 song_length: Optional[float] = None) -> None:
        self.database = database
        self.file_path = Path(file_path)
        self.file_size = self.__format_value__('file_size', file_size)
        self.first_seen = self.__format_value__('first_seen', first_seen)
        self.last_modified = self.__format_value__('last_modified', last_modified)
        self.song_length = self.__format_value__('song_length', song_length)
        self.scan = None
        self.tags = None

    def __repr__(self) -> str:
        return str(self.file_path)

    @property
    def path(self) -> Path:
        """
        Get fully qualified library file path
        """
        return self.database.library.path.parent.joinpath(self.file_path)

    def __load_element_scan__(self, element: _Element) -> None:
        """
        Load Scan object data from XML element
        """
        scan_element = element.find('Scan')
        if scan_element is None:
            return
        self.scan = Scan(self, scan_element)

    def __load_element_tags__(self, element: _Element) -> None:
        """
        Load Tags object from XML element
        """
        tag_element = element.find('Tags')
        if tag_element is None:
            return
        self.tags = Tags(self, tag_element)

    @classmethod
    def from_element(cls, database: 'Database', element: _Element) -> 'Song':
        """
        Initialize Song object from XML element
        """
        song = cls(
            database,
            file_path=re.sub(RE_DRIVE_LETTER_PREFIX, '', element.get('FilePath')),
            file_size=element.get('FileSize'),
        )
        info = element.find('Infos')
        if info is not None:
            for info_attr in ELEMENT_SONG_INFO_ATTRIBUTES:
                attr = underscore(info_attr)
                setattr(song, attr, song.__format_value__(attr, info.get(info_attr)))

        song.__load_element_scan__(element)
        song.__load_element_tags__(element)

        return song
