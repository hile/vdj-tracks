"""
VirtualDJ configuration directory loader
"""
from pathlib import Path
from typing import Optional, Union, TYPE_CHECKING

from ..library.library import Library

if TYPE_CHECKING:
    from ..application import VirtualDJ


# pylint: disable=too-few-public-methods
class VirtualDJConfigurationDirectory:
    """
    Configuration directory for VirtualDJ settings and playlists
    """
    application: 'VirtualDJ'
    path: Path

    def __init__(self,
                 application: 'VirtualDJ',
                 path: Optional[Union[str, Path]] = None) -> None:
        self.application = application
        path = Path(path) if path is not None else self.__get_default__path__()
        self.path = path.expanduser().resolve()

    def __repr__(self) -> str:
        return str(self.path)

    def __get_default__path__(self) -> Path:
        """
        Get default configuration path
        """
        from .constants import DEFAULT_VIRTUALDJ_DIRECTORY  # pylint: disable=import-outside-toplevel
        return Path(DEFAULT_VIRTUALDJ_DIRECTORY)

    @property
    def library(self) -> Library:
        """
        Return the configured Library object matching configuration directory
        """
        return self.application.get_library(self.path)
