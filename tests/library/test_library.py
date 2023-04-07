"""
Unit tests for vdj_tracks.library.loader module
"""
from vdj_tracks.database.database import Database


def test_library_properties(valid_library) -> None:
    """
    Test basic properties of Libraries loader object
    """
    assert isinstance(repr(valid_library), str)
    assert isinstance(valid_library.database, Database)
