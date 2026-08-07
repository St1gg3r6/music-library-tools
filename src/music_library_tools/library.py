import xml.etree.ElementTree as ET
from music_library_tools.plist import plist_to_dict


def load_library(filepath: str) -> ET.Element:
    """
    Load a music library from an XML file.

    Args:
        filepath (str): The path to the XML file.

    Returns:
        Element: An xml representation of the music library.
    """

    tree = ET.parse(filepath)
    root = tree.getroot()
    assert root.tag == "plist"

    library = root[0]
    assert library.tag == "dict"

    return library


def get_library_section(library: ET.Element, section_name: str) -> ET.Element:
    """
    Get a specific section of the music library.

    Args:
        library (Element): An xml representation of the music library.
        section_name (str): The name of the section to retrieve.

    Returns:
        Element: An xml representation of the requested section.
    """

    for i in range(0, len(library), 2):
        if library[i].text == section_name:
            section = library[i + 1]
            break
    else:
        raise KeyError(f"Section '{section_name}' not found in library.")

    return section


def parse_dict_elements(section: ET.Element) -> list[dict]:
    """
        Parse a plist section whose values are <dict> elements.

        Args:
            section: A plist <dict> containing alternating <key>/<dict> children.

        Returns:
            A list of parsed Python dictionaries.
    """
    
    parsed_section = []

    for i in range(0, len(section), 2):
        element = section[i + 1]
        parsed_element, unsupported = plist_to_dict(element)

        assert not unsupported

        parsed_section.append(parsed_element)

    return parsed_section