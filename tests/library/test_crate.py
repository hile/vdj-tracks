"""
Unit tests for vdj_tracks.library.crate module
"""
from vdj_tracks.library.crate import Crate, CrateTrack

from ..conftest import MOCK_VALID_LIBRARY_CRATES_COUNT


def test_library_properties(valid_library) -> None:
    """
    Test basic properties of Libraries loader object
    """
    assert isinstance(repr(valid_library), str)
    assert len(valid_library.crates) == MOCK_VALID_LIBRARY_CRATES_COUNT
    for crate in valid_library.crates:
        assert isinstance(crate, Crate)
        assert isinstance(repr(crate), str)
        assert len(crate.tracks) > 0
        for track in crate.tracks:
            assert isinstance(track, CrateTrack)
            assert isinstance(repr(track), str)
