"""
Unit tests for vdj_tracks.library.loader module
"""
from sys_toolkit.tests.mock import MockReturnFalse, MockReturnTrue

from vdj_tracks import VirtualDJ


def test_libraries_detect_mountpoint_dirs_none(monkeypatch) -> None:
    """
    Test detecting vdj_tracks folders with mocked 'is_dir' call to force all
    mountpoints to match
    """
    monkeypatch.setattr('fs_toolkit.mounts.platform.base.Path.is_dir', MockReturnFalse())
    vdj = VirtualDJ()
    assert len(vdj.libraries) == 0


def test_libraries_detect_mountpoint_dirs_all(monkeypatch) -> None:
    """
    Test detecting vdj_tracks folders with mocked 'is_dir' call to force all
    mountpoints to match
    """
    monkeypatch.setattr('fs_toolkit.mounts.platform.base.Path.is_dir', MockReturnTrue())
    vdj = VirtualDJ()
    vdj.libraries.update()
    assert len(vdj.libraries) > 0


# pylint: disable=unused-argument
def test_libraries_detect_mountpoint_dirs_permission_denied(
        mountpoints_permission_denied) -> None:
    """
    Test detecting vdj_tracks folders with mocked 'is_dir' call to force all
    mountpoints to match
    """
    vdj = VirtualDJ()
    assert len(vdj.libraries.mountpoints) == 0
