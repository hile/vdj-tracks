"""
VirtualDJ application
"""
from itertools import chain
from pathlib import Path
from typing import List, Optional, Union

from .configuration.loader import VirtualDJConfigurationDirectory
from .library.crate import Crate
from .library.library import Library
from .library.loader import Libraries


# pylint: disable=too-few-public-methods
class VirtualDJ:
    """
    VirtualDJ application loader
    """
    libraries: Libraries

    def __init__(self, configuration: Optional[Union[str, Path]] = None) -> None:
        self.configuration = VirtualDJConfigurationDirectory(
            self,
            configuration
        )
        self.libraries = Libraries(self)

    @property
    def crates(self) -> List[Crate]:
        """
        Return crates in all libraries
        """
        return list(chain(*[library.crates for library in self.libraries.values()]))

    @property
    def songs(self) -> List[Crate]:
        """
        Return songs in all libraries
        """
        return list(chain(*[library.database.songs for library in self.libraries.values()]))

    def get_crate(self, value: Union[str, Path]) -> Optional[Crate]:
        """
        Get crate by name or path
        """
        path = Path(value)
        for crate in self.crates:
            if crate.path == path or crate.path.stem == value:
                return crate
        return None

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

        path = Path(value)
        for library in self.libraries.values():
            if match(library, value, path):
                return library
        return None
