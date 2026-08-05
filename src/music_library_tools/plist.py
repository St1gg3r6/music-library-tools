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

    print("Function has been called")

    if element.tag != PLIST_DICT_TAG:
        raise ValueError("Expected a plist <dict> element.")

    result: dict[str, Any] = {}

    # Iterate over the children of the <dict> element in pairs (key, value)
    for i in range(0, len(element), 2):
        key = element[i]
        value = element[i + 1]

        assert key.tag == "key"
        assert value.tag != "key"

        key_text = key.text

        assert key_text is not None

        if value.tag == 'string':
            result[key_text] = value.text

    return result
