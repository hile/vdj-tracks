"""
Unit tests for vdj_tracks.configuration module
"""
from vdj_tracks.library.library import Library
from vdj_tracks.library.playlist import Playlist

from ..conftest import MOCK_VALID_CONFIGURATION_PLAYLISTS_COUNT


def test_configuration_loader_properties(vdj) -> None:
    """
    Test various properties of VirtualDJ configuration directory
    """
    assert isinstance(repr(vdj.configuration), str)
    assert vdj.configuration.path.is_dir()
    assert isinstance(vdj.configuration.library, Library)

    library = vdj.libraries[str(vdj.configuration.path)]
    assert len(library.playlists) == MOCK_VALID_CONFIGURATION_PLAYLISTS_COUNT
    for playlist in library.playlists:
        assert isinstance(playlist, Playlist)
        assert isinstance(repr(playlist), str)
