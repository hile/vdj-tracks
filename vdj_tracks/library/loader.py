"""
VirtualDJ libraries loader
"""
from pathlib import Path
from typing import Dict, List, TYPE_CHECKING

from fs_toolkit import Mountpoints
from sys_toolkit.collection import CachedMutableMapping

from ..constants import LIBRARY_FOLDER_NAME
from .library import Library

if TYPE_CHECKING:
    from ..application import VirtualDJ


class Libraries(CachedMutableMapping):
    """
    VirtualDJ filesystem libraries

    Library folders are detected based on filesystem folders
    """
    application: 'VirtualDJ'
    __items__: Dict[str, Library]

    def __init__(self, application: 'VirtualDJ') -> None:
        self.application = application
        self.update()

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

    def update(self) -> None:  # pylint:disable=arguments-differ
        """
        Detect list of VirtualDJ libraries automatically
        """
        self.__start_update__()
        self.__items__ = {}

        if self.application.configuration.path.is_dir():
            self.add_library(self.application.configuration.path)
        for mountpoint in self.mountpoints:
            self.add_library(mountpoint.joinpath(LIBRARY_FOLDER_NAME))
        self.__finish_update__()

    def add_library(self, path: Path) -> Library:
        """
        Add library to detected library paths
        """
        library = Library(self, path)
        self.__items__[str(library.path)] = library
        self.__loaded__ = True
        return library
