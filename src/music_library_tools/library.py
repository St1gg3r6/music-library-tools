import xml.etree.ElementTree as ET
from music_library_tools.plist import plist_to_dict
import pandas as pd


IDENTITY_FIELDS = [
    "Artist",
    "Album",
    "Track Number",
    "Name",
]

CLOUD_STATUS_PLAYLISTS = {
    'apple_music': 'Cloud Status - Apple Music',
    'duplicate': 'Cloud Status - Duplicate',
    'error': 'Cloud Status - Error',
    'ineligible': 'Cloud Status - Ineligible',
    'matched': 'Cloud Status - Matched',
    'no_longer_available': 'Cloud Status - No Longer Available',
    'not_uploaded': 'Cloud Status - Not Uploaded',
    'purchased': 'Cloud Status - Purchased',
    'removed': 'Cloud Status - Removed',
    'uploaded': 'Cloud Status - Uploaded',
    'waiting': 'Cloud Status - Waiting'
}


def load_library(filepath: str) -> ET.Element:
    """
    Load a music library from an XML file.

    Args:
        filepath (str): The path to the XML export file.

    Returns:
        Element: The root <dict> element of the music library.
    """

    tree = ET.parse(filepath)
    root = tree.getroot()
    assert root.tag == "plist"

    library = root[0]
    assert library.tag == "dict"

    return library


def get_library_section(library: ET.Element, section_name: str) -> ET.Element:
    """
    Get a named, top-level section of the library.

    Args:
        library (Element): The library <dict> element.
        section_name (str): The name of the section to retrieve.

    Returns:
        Element: An xml representation of the requested section.
    """

    for i in range(0, len(library), 2):
        if library[i].text == section_name:
            return library[i + 1]

    raise KeyError(f"Section '{section_name}' not found in library.")


def _parse_dict_sequence(elements: list[ET.Element]) -> list[dict]:
    """
    Parse a sequence of plist <dict> elements.
    
    Args:
        elements: A list of <dict> elements.
        
    Returns:
        A list of Python dictionaries.
    """

    parsed = []
    unsupported_types = []

    for element in elements:

        assert element.tag == 'dict'

        parsed_element, unsupported = plist_to_dict(element)

        # assert not unsupported
        # unsupported_types.append(unsupported)
        parsed.append(parsed_element)

    return parsed #, unsupported_types


def parse_dict_elements(section: ET.Element) -> list[dict]:
    """
        Parse a plist <dict> whose values are <dict> elements.

        Args:
            section: A plist <dict> containing alternating <key>/<dict> children.

        Returns:
            A list of parsed Python dictionaries.
    """

    assert section.tag == 'dict'

    elements = [section[i + 1] for i in range(0, len(section), 2)]

    return _parse_dict_sequence(elements)


def parse_array_elements(section: ET.Element) -> list[dict]:
    """
    Parse a plist <array> whose children are <dict> elements.

    Args:
        section: A plist <array>

    Returns:
        A list of parsed Python dictionaries.
    """

    assert section.tag == 'array'

    return _parse_dict_sequence(list(section))


def library_export_to_dataframe(filepath: str) -> pd.DataFrame:
    """
    Load a music library from an XML file and convert the Tracks elements to a pandas DataFrame.

    Args:
        filepath (str): The path to the XML file.

    Returns:
        DataFrame: A pandas DataFrame containing the music library data.
    """

    library = load_library(filepath)
    tracks = parse_dict_elements(get_library_section(library, "Tracks"))

    df = pd.DataFrame(tracks).sort_values(by='Track ID')
    df = df[df['Playlist Only'].fillna(False) == False]  # Exclude playlist-only tracks
    
    df['Identity Count'] = df.groupby(IDENTITY_FIELDS)['Track ID'].transform('count')
    df['Max Track ID'] = df.groupby(IDENTITY_FIELDS)['Track ID'].transform('max')
    df['Min Track ID'] = df.groupby(IDENTITY_FIELDS)['Track ID'].transform('min')

    return df


def get_playlist(playlists: list[dict], name: str) -> dict | None:
    """
    Return the first playlist with the given name.

    Args:
        playlists: Parsed playlist collection.
        name: Name of the playlist to find.

    Returns:
        The first playlist dictionary with the given name, or None if not found.
    """

    for playlist in playlists:
        if playlist['Name'] == name:
            return playlist

    return None


def get_playlist_track_ids(playlist: dict) -> list[int]:
    """
    Return the track IDs from a playlist.

    Args:
        playlist: Parsed playlist dictionary.

    Returns:
        A list of track IDs from the playlist.
    """

    return [item['Track ID'] for item in playlist.get('Playlist Items', [])]


def get_track_by_id(df: pd.DataFrame, track_id: int) -> pd.Series | None:
    """
    Return the track with the given Track ID.

    Args:
        df: DataFrame containing the music library data.
        track_id: The Track ID to find.

    Returns:
        A pandas Series representing the track, or None if not found.
    """

    track = df.loc[df['Track ID'] == track_id]

    if not track.empty:
        return track.iloc[0]

    return None