"""
Unit tests for vdj_tracks.library.loader module
"""
from pathlib import Path

from vdj_tracks.library.crate import Crate
from .conftest import (
    MOCK_UNKNOWN_LIBRARY_NAME,
    MOCK_VALID_CONFIGURATION_SONG_COUNT,
    MOCK_VALID_LIBRARY_CRATES_COUNT,
    MOCK_VALID_LIBRARY_SONG_COUNT,
    MOCK_VALID_LIBRARY_CRATE_NAME_FOUND,
    MOCK_VALID_LIBRARY_CRATE_NAME_NOT_FOUND,
)


def test_virtualdj_application_properties(vdj) -> None:
    """
    Mock various properties of VirtualDJ application
    """
    for library in vdj.libraries:
        print(f'LIBRARY {library}')
    for crate in vdj.crates:
        print(f'CRATE {crate.path}')
    assert len(vdj.crates) == MOCK_VALID_LIBRARY_CRATES_COUNT
    assert len(vdj.songs) == MOCK_VALID_CONFIGURATION_SONG_COUNT + MOCK_VALID_LIBRARY_SONG_COUNT
    # This consists of the mocked configuration directory
    # and manually loaded library
    assert len(vdj.libraries) == 2


def test_virtualdj_application_get_crate_by_string_not_found(vdj) -> None:
    """
    Test fetching crate by crate name as string successfully
    """
    crate = vdj.crates.get_crate(MOCK_VALID_LIBRARY_CRATE_NAME_NOT_FOUND)
    assert crate is None


def test_virtualdj_application_get_crate_by_string_found(vdj) -> None:
    """
    Test fetching crate by crate name as string successfully
    """
    crate = vdj.crates.get_crate(MOCK_VALID_LIBRARY_CRATE_NAME_FOUND)
    assert isinstance(crate, Crate)
    assert crate is not None
    assert str(crate) == MOCK_VALID_LIBRARY_CRATE_NAME_FOUND


def test_virtualdj_application_get_crate_by_path_found(vdj) -> None:
    """
    Test fetching crate by crate name as string successfully
    """
    crate = vdj.crates.get_crate(vdj.crates[-1].path)
    assert isinstance(crate, Crate)
    assert crate == vdj.crates[-1]


def test_virtualdj_application_get_crate_by_path_string_found(vdj) -> None:
    """
    Test fetching crate by crate name as string successfully
    """
    crate = vdj.crates.get_crate(str(vdj.crates[-1].path))
    assert isinstance(crate, Crate)
    assert crate == vdj.crates[-1]


def test_virtualdj_application_get_library_name_not_found(vdj) -> None:
    """
    Test looking up unexpected library by name
    """
    assert vdj.libraries.get_library(MOCK_UNKNOWN_LIBRARY_NAME) is None


def test_virtualdj_application_get_library_path_not_found(tmpdir, vdj) -> None:
    """
    Test looking up unexpected library by path
    """
    assert vdj.libraries.get_library(Path(tmpdir.strpath)) is None


def test_virtualdj_application_get_library_name_found(vdj) -> None:
    """
    Test looking up known library by parent path
    """
    library = list(vdj.libraries)[-1]
    assert vdj.libraries.get_library(library.path.parent.stem) == library
