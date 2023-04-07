"""
Unit tests for vdj_tracks.base module
"""
from vdj_tracks.base import AttributeFormatter


def test_attribute_formatter_properties() -> None:
    """
    Test properties of uninitialized AttributeFormatter object
    """
    obj = AttributeFormatter()
    assert obj.__boolean_attributes__ == ()
    assert obj.__float_attributes__ == ()
    assert obj.__integer_attributes__ == ()
    assert obj.__timestamp_attributes__ == ()
