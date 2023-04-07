"""
VirtualDJ XML database for a music directory
"""
from operator import attrgetter
from typing import List, Optional, TYPE_CHECKING

from ..base import XMLDataFile
from .song import Song

if TYPE_CHECKING:
    from ..library.loader import Library

DATABASE_FILENAME = 'database.xml'


class Database(XMLDataFile):
    """
    VirtualDJ XML database in a music library
    """
    library: 'Library'
    __songs__: Optional[List[Song]] = None

    def __init__(self, library: 'Library') -> None:
        super().__init__(library.path.joinpath(DATABASE_FILENAME))
        self.library = library
        self.__songs__ = None

    @property
    def songs(self) -> List[Song]:
        """
        Return XML ElementTree for the database XMLs file
        """
        if self.__songs__ is None:
            elements = self.xml.findall('Song')
            self.__songs__ = [Song.from_element(self, element) for element in elements]
            self.__songs__.sort(key=attrgetter('file_path'))
        return self.__songs__
