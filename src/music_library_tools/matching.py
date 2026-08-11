import pandas as pd
from music_library_tools.library import IDENTITY_FIELDS


def find_candidate_originals(track: pd.Series, search_df: pd.DataFrame,) -> pd.DataFrame:
    """
    Find candidate original tracks for a given track.

    Searches a DataFrame for tracks that share the same musical identity
    as the supplied track. Candidate matches are identified using a small
    set of stable metadata fields rather than library-specific identifiers.

    This function performs candidate selection only. It does not attempt
    to determine which candidate, if any, is the correct match.

    Args:
        track (pd.Series):
            The track for which candidate original tracks are to be found.

        search_df (pd.DataFrame):
            The DataFrame to search for candidate matches.

    Returns:
        pd.DataFrame:
            A DataFrame containing all candidate matching tracks. The
            returned DataFrame may contain zero, one or multiple rows.
    """

    # Define the metadata fields to use for candidate selection
    identity_fields = IDENTITY_FIELDS

    # Create a boolean mask for candidate matches
    mask = pd.Series(True, index=search_df.index)
    for field in identity_fields:
        if field in track and field in search_df:
            mask &= search_df[field] == track[field]

    # Return the subset of the DataFrame that matches the mask
    return search_df[mask & (search_df.index != track.name)]