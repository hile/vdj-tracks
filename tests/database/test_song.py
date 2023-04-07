"""
Unit tests for vdj_tracks.database.song module
"""
from pathlib import Path
from vdj_tracks.database.song import Song

from ..conftest import MOCK_VALID_LIBRARY_SONG_COUNT


def test_database_song_properties(valid_library) -> None:
    """
    Test basic properties of library database song objects
    """
    database = valid_library.database
    assert len(database.songs) == MOCK_VALID_LIBRARY_SONG_COUNT
    for song in database.songs:
        assert isinstance(song, Song)
        assert isinstance(repr(song), str)
        assert isinstance(song.path, Path)
        if song.tags:
            for tag in song.tags:
                assert isinstance(tag, str)
                assert isinstance(song.tags[tag], str)
