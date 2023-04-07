"""
Pytest unit test configuration for vdj_tracks python package
"""
from pathlib import Path
from typing import Iterator

import pytest

from sys_toolkit.tests.mock import MockCalledMethod

from vdj_tracks.library.loader import Library
from vdj_tracks import VirtualDJ

MOCK_DATA = Path(__file__).parent.joinpath('mock')

MOCK_VALID_CONFIGURATION_DIRECTORY = MOCK_DATA.joinpath('valid-configuration')
# By default has 'default' and 'sidelist' playlists
MOCK_VALID_CONFIGURATION_PLAYLISTS_COUNT = 2
MOCK_VALID_CONFIGURATION_SONG_COUNT = 2

MOCK_VALID_LIBRARY = MOCK_DATA.joinpath('valid-library/VirtualDJ')
MOCK_VALID_LIBRARY_CRATES_COUNT = 2
MOCK_VALID_LIBRARY_SONG_COUNT = 4

MOCK_UNKNOWN_LIBRARY_NAME = 'Jaskaa'

MOCK_VALID_LIBRARY_CRATE_NAME_FOUND = 'Soul'
MOCK_VALID_LIBRARY_CRATE_NAME_NOT_FOUND = 'Soul & R&B'


@pytest.fixture
def valid_configuration_directory(monkeypatch) -> Iterator[Path]:
    """
    Mock valid configuration directory and library
    """
    monkeypatch.setattr('vdj_tracks.library.loader.Libraries.mountpoints', [])
    monkeypatch.setattr(
        'vdj_tracks.configuration.constants.DEFAULT_VIRTUALDJ_DIRECTORY',
        MOCK_VALID_CONFIGURATION_DIRECTORY
    )
    yield MOCK_VALID_CONFIGURATION_DIRECTORY


# pylint: disable=redefined-outer-name,unused-argument
@pytest.fixture
def valid_library(valid_configuration_directory) -> Iterator[Library]:
    """
    Mock valid library
    """
    yield VirtualDJ().libraries.add_library(MOCK_VALID_LIBRARY)


# pylint: disable=redefined-outer-name
@pytest.fixture
def vdj(valid_library) -> Iterator[VirtualDJ]:
    """
    Mock VirtualDJ object with simple configuration and single valid library
    """
    application = valid_library.loader.application
    yield application


@pytest.fixture
def mountpoints_permission_denied(monkeypatch, tmpdir) -> Iterator[Path]:
    """
    Mock returning paths as mountpoints where accessing the directory is not allowed
    """
    restricted_path = Path(tmpdir.strpath, 'restricted-directory/subpath')
    mock_mount_data = MockCalledMethod(
        return_value=[{
            'device': '/dev/test',
            'mountpoint': str(restricted_path),
            'filesystem': 'demo',
            'options': '',
        }]
    )
    monkeypatch.setattr(
        'vdj_tracks.library.loader.Mountpoints.__get_mountpoint_data__',
        mock_mount_data
    )
    if not restricted_path.is_dir():
        restricted_path.mkdir(parents=True)
    restricted_path.parent.chmod(int('0000', 8))
    yield mock_mount_data
    restricted_path.parent.chmod(int('0755', 8))
