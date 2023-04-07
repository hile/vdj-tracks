"""
Unit tests for vdj_tracks.library.playlist module
"""
from pathlib import Path
from vdj_tracks.library.playlist import Playlist, PlaylistTrack


def test_library_playlist_properties(vdj) -> None:
    """
    Test basic properties of playlists in VirtualDJ library
    """
    library = vdj.configuration.library
    assert len(library.playlists) > 0
    for playlist in library.playlists:
        assert isinstance(playlist, Playlist)
        for track in playlist:
            assert isinstance(track, PlaylistTrack)
            assert isinstance(track.path, Path)
            assert isinstance(repr(track), str)
