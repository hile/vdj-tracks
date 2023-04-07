"""
Unit tests for vdj_tracks.database.loader module
"""


def test_database_properties(valid_library) -> None:
    """
    Test basic properties of library database objects
    """
    database = valid_library.database
    assert isinstance(repr(database), str)

    # Check lazy loading
    songs = database.songs
    assert songs == database.songs
