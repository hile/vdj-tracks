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


def test_library_playlist_track_missing_library(vdj, tmpdir) -> None:
    """
    Test basic properties of playlists in VirtualDJ library
    """
    playlist = Playlist(vdj.configuration.library, Path(tmpdir.strpath, 'missing-playlists.m3u'))
    track = PlaylistTrack(playlist, Path(tmpdir.strpath, 'test.m4a'))
    assert track.library is None
    assert track.relative_path is None


def test_library_playlist_track_relative_path_found(vdj, tmpdir) -> None:
    """
    Test basic properties of playlists in VirtualDJ library
    """
    playlist = Playlist(vdj.configuration.library, Path(tmpdir.strpath, 'missing-playlists.m3u'))
    track = PlaylistTrack(playlist, Path(vdj.configuration.library.path, 'test.m4a'))
    assert track.library is not None
    assert track.relative_path is not None
