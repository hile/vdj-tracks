"""
VirtualDJ application
"""
from itertools import chain
from pathlib import Path
from typing import List, Optional, Union

from .configuration.loader import VirtualDJConfigurationDirectory
from .database.song import Song
from .library.loader import Crates, Libraries


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
        self.crates = Crates(self)
        self.libraries = Libraries(self)
        self.libraries.load()

    @property
    def songs(self) -> List[Song]:
        """
        Return songs in all libraries
        """
        return list(chain(*[library.database.songs for library in self.libraries]))
