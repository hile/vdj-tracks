"""
VirtualDJ libraries loader
"""
from collections.abc import MutableSequence
from pathlib import Path
from typing import List, Optional, Union, TYPE_CHECKING

from fs_toolkit import Mountpoints

from ..constants import LIBRARY_FOLDER_NAME
from .crate import Crate
from .library import Library

if TYPE_CHECKING:
    from ..application import VirtualDJ


class Crates(MutableSequence):
    """
    VirtualDJ filesystem crates
    """
    application: 'VirtualDJ'
    __items__: List[Crate]

    def __init__(self, application: 'VirtualDJ') -> None:
        self.application = application
        self.__items__ = []

    def __delitem__(self, index: int) -> None:
        self.__items__.__delitem__(index)

    def __getitem__(self, index: int) -> Crate:
        return self.__items__.__getitem__(index)

    def __len__(self) -> int:
        return len(self.__items__)

    def __setitem__(self, index: int, value: Crate) -> None:
        self.__items__.__setitem__(index, value)

    def insert(self, index: int, value: Crate) -> None:
        self.__items__.insert(index, value)

    def get_crate(self, value: Union[str, Path]) -> Optional[Crate]:
        """
        Get crate by name or path
        """
        path = Path(value).expanduser()
        for crate in self:
            if crate.path == path or crate.path.stem == value:
                return crate
        return None


class Libraries(MutableSequence):
    """
    VirtualDJ filesystem libraries

    Library folders are detected based on filesystem folders
    """
    application: 'VirtualDJ'
    __items__: List[Library]

    def __init__(self, application: 'VirtualDJ') -> None:
        self.application = application
        self.__items__ = []

    def __delitem__(self, index: int) -> None:
        self.__items__.__delitem__(index)

    def __getitem__(self, index: int) -> Library:
        return self.__items__.__getitem__(index)

    def __len__(self) -> int:
        return len(self.__items__)

    def __setitem__(self, index: int, value: Library) -> None:
        self.__items__.__setitem__(index, value)

    def insert(self, index: int, value: Library) -> None:
        self.__items__.insert(index, value)

    @property
    def mountpoints(self) -> List[Path]:
        """
        Return mountpoints with VirtualDJ subfolder
        """
        paths = []
        for item in Mountpoints():
            mountpoint = Path(item.mountpoint)
            try:
                if item.mountpoint and mountpoint.joinpath(LIBRARY_FOLDER_NAME).is_dir():
                    paths.append(mountpoint)
            except OSError:
                continue
        return paths

    def load(self) -> None:  # pylint:disable=arguments-differ
        """
        Initialize list of VirtualDJ libraries automatically
        """
        self.__items__ = []
        if self.application.configuration.path.is_dir():
            self.add_library(self.application.configuration.path)
        for mountpoint in self.mountpoints:
            self.add_library(mountpoint.joinpath(LIBRARY_FOLDER_NAME))

    def add_library(self, path: Path) -> Library:
        """
        Add library to detected library paths
        """
        library = Library(self, path)
        for crate in library.crates:
            self.application.crates.append(crate)
        self.append(library)
        return library

    def get_library(self, value: Union[str, Path]) -> Optional[Library]:
        """
        Get a library by name or path match
        """
        def match(library: Library, value: str, path: Path) -> bool:
            """
            Match library by path
            """
            if library.path.parent.stem == value:
                return True
            try:
                path.relative_to(library.path.parent)
                return True
            except ValueError:
                return False

        path = Path(value).expanduser()
        for library in self:
            if match(library, value, path):
                return library
        return None
