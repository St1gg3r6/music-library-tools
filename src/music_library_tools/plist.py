"""
Utilities for working with Apple plist XML structures.
"""

from xml.etree.ElementTree import Element
from typing import Any


PLIST_DICT_TAG = "dict"


def plist_to_dict(element: Element) -> dict[str, Any]:
    """
    Convert a plist <dict> element into a Python dictionary.

    Parameters
    ----------
    element
        XML Element representing a plist dictionary.

    Returns
    -------
    dict
        Dictionary containing the plist key/value pairs.

    Raises
    ------
    ValueError
        If the supplied element is not a plist dictionary.
    """

    if element.tag != PLIST_DICT_TAG:
        raise ValueError("Expected a plist <dict> element.")

    result: dict[str, Any] = {}
    unsupported_types: set[str] = set()

    # Iterate over the children of the <dict> element in pairs (key, value)
    for i in range(0, len(element), 2):
        key = element[i]
        value = element[i + 1]

        assert key.tag == "key"
        assert value.tag != "key"

        key_text = key.text

        assert key_text is not None

        unsupported,converted = _convert_value(value)

        if unsupported is not None:
            unsupported_types.add(unsupported)
        else:
            result[key_text] = converted

    return result, unsupported_types


def _convert_value(element: Element) -> tuple[str | None, Any]:
    """
    Convert a plist value element into an appropriate Python value
    """

    match element.tag:
        case 'string':
            return None, element.text
        case 'integer':
            assert element.text is not None
            return None, int(element.text)
        case 'true':
            return None, True
        case 'date':
            assert element.text is not None
            return None, element.text  # Return the date string as-is
        
    return element.tag, None  # Return the tag name for unsupported types
    