"""
VirtualDJ library based on filesystem mountpoint
"""
from pathlib import Path
from typing import List, Optional, Union, TYPE_CHECKING

from ..constants import LIBRARY_CRATES_PATH, LIBRARY_PLAYLISTS_PATH
from ..database.database import Database
from .crate import Crate
from .playlist import Playlist

if TYPE_CHECKING:
    from .loader import Libraries


# pylint: disable=too-few-public-methods
class Library:
    """
    VirtualDJ music folder with VirtualDJ data folder
    """
    loader: 'Libraries'
    database: Database
    __crates__: Optional[List[Crate]] = None
    __playlists__: Optional[List[Crate]] = None

    def __init__(self, loader: 'Libraries', path: Union[str, Path]) -> None:
        self.loader = loader
        self.__crates__ = None
        self.__playlists__ = None
        self.path = Path(path).expanduser().resolve()
        self.database = Database(self)

    def __repr__(self):
        return str(self.path)

    @property
    def crates(self):
        """
        Return files matching glob pattern for crates .vdjfolder files in library
        """
        if self.__crates__ is None:
            self.__crates__ = [
                Crate(self, path)
                for path in self.path.joinpath(*LIBRARY_CRATES_PATH).glob('**/*.vdjfolder')
            ]
        return self.__crates__

    @property
    def playlists(self):
        """
        Return files matching glob pattern for crates .vdjfolder files in library
        """
        if self.__playlists__ is None:
            self.__playlists__ = [
                Playlist(self, path)
                for path in self.path.joinpath(*LIBRARY_PLAYLISTS_PATH).glob('**/*.m3u')
            ]
        return self.__playlists__
