"""
VirtualDJ playlist in a library
"""
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from sys_toolkit.collection import CachedMutableSequence
from sys_toolkit.textfile import LineTextFile

if TYPE_CHECKING:
    from .library import Library


@dataclass
class PlaylistTrack:
    """
    Track in VirtualDJ library playlist
    """
    playlist: 'Playlist'
    path: Path

    def __repr__(self) -> str:
        return str(self.path)


# pylint: disable=too-few-public-methods
class Playlist(CachedMutableSequence):
    """
    Playlist files in VirtualDJ extended .m3u format

    This class currently ignores custom XML-like VirtualDJ metadata comments
    """
    library: 'Library'
    path: Path

    def __init__(self, library: 'Library', path: Path) -> None:
        self.library = library
        self.path = Path(path).expanduser().resolve()

    def __repr__(self) -> str:
        return self.path.stem

    def update(self) -> None:
        """
        Load m3u playlist in VirtualDJ .m3u format, ignoring extra metadata comments
        """
        self.clear()
        self.__start_update__()
        for line in LineTextFile(self.path):
            self.__items__.append(PlaylistTrack(self, Path(line)))
        self.__finish_update__()
