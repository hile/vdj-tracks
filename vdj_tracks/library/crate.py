"""
VirtualDJ crate in a library
"""
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

from ..base import XMLDataFile

if TYPE_CHECKING:
    from .library import Library


# pylint: disable=too-few-public-methods
class CrateTrack:
    """
    Track in a crate with small number of attributes
    """
    crate: 'Crate'
    path: Path
    artist: str
    title: str
    idx: int
    size: int
    bpm: Optional[float]
    songlength: float
    remix: str

    def __init__(self,
                 crate: 'Crate',
                 path: str,
                 idx: str,
                 songlength: str,
                 size: str,
                 bpm: str = '',
                 artist: str = '',
                 title: str = '',
                 remix: str = '') -> None:
        self.crate = crate
        self.path = Path(path)
        self.artist = artist
        self.title = title
        self.bpm = float(bpm) if bpm else None
        self.size = int(size)
        self.idx = int(idx)
        self.songlength = float(songlength)
        self.remix = remix

    def __repr__(self) -> str:
        return str(self.path)

    @property
    def library(self) -> Optional['Library']:
        """
        Return library for crate track path

        This library may be different to playlist library when music is from an
        external drive library and it may be None when library for track is not
        attached
        """
        return self.crate.library.loader.get_library(self.path)

    @property
    def relative_path(self) -> Optional[Path]:
        """
        Return relative path to local music library
        """
        library = self.library
        return self.path.relative_to(library.path) if library is not None else None


class Crate(XMLDataFile):
    """
    Crate file in a VirtualDJ library
    """
    library: 'Library'
    path: Path

    def __init__(self, library: 'Library', path: Path) -> None:
        super().__init__(path)
        self.library = library

    def __repr__(self) -> str:
        return self.path.stem

    @property
    def tracks(self) -> List[CrateTrack]:
        """
        Return crate tracks from XML data
        """
        return [
            CrateTrack(self, **dict(element.items()))
            for element in self.xml.findall('song')
        ]
