"""
Common base classes for VirtualDJ library
"""
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Tuple

from lxml import etree


# pylint: disable=too-few-public-methods
class AttributeFormatter:
    """
    Class with method to format values in setters based on lists of attribute names
    """
    __boolean_attributes__: Tuple[str] = ()
    __float_attributes__: Tuple[str] = ()
    __integer_attributes__: Tuple[str] = ()
    __timestamp_attributes__: Tuple[str] = ()

    def __format_value__(self, attr: str, value: str) -> Any:
        """
        Format value for specified field
        """
        if value is not None:
            if attr in self.__boolean_attributes__:
                value = value in ('True', 'true', '1', True)
            if attr in self.__float_attributes__:
                value = float(value)
            if attr in self. __integer_attributes__:
                value = int(value)
            if attr in self. __timestamp_attributes__:
                value = datetime.fromtimestamp(int(value))
        return value


class XMLDataFile:
    """
    VirtualDJ data file with XML data
    """
    path: Path
    # pylint: disable=c-extension-no-member
    __element_tree__: Optional[etree.ElementTree] = None

    def __init__(self, path: Path) -> None:
        self.path = path
        self.__element_tree__ = None

    def __repr__(self) -> str:
        return str(self.path)

    @property
    def xml(self) -> etree.ElementTree:  # pylint: disable=c-extension-no-member
        """
        Return XML ElementTree for the crate file
        """
        if self.__element_tree__ is None:
            with self.path.open('rb') as handle:
                self.__element_tree__ = etree.ElementTree().parse(handle)
        return self.__element_tree__
