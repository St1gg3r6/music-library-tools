# Discovery 001

The XML export represents Tracks as a dictionary.

Evidence

tracks.tag == 'dict'

tracks child count == 38,060

Interpretation

Each track is likely represented as a key/value pair within the dictionary.


# Discovery 004 - Track Structure

Evidence

The first track in the Tracks dictionary has:

Track ID: 1704

Tag: dict

Child Elements: 68

The first five key/value pairs are:

Track ID -> 1704
Name     -> Hells Bells
Artist   -> AC/DC
Album     -> Back In Black
Genre     -> Rock

Conclusion

Individual tracks are represented as plist dictionaries containing
key/value pairs describing the track metadata.


# Design Principle 001

The parser converts plist values into their most appropriate native Python types as early as possible.

That means:
XML Tag	Python Type
string	str
integer	int
true	bool
false	bool
date	datetime.datetime
dict	dict (recursive)
array	list (eventually)


## Discovery 006 – Track Value Types

Parsed all 19,030 track dictionaries.

Supported types:
- string
- integer
- true

The only unsupported scalar value type encountered was `date`.

Occurrences:
- date: 19,030

This indicates every track contains exactly one date value in the exported XML.

## Discovery 007 – Effect of "Add to Library" on a Removed Track

Date observed: 2026-08-06

Starting state:
- Track had Cloud Status = Removed.
- A duplicate "Waiting" or "Matched" instance of the track already existed.
- Original track contained historical metadata (play count, rating, etc.).

Action:
- Right-clicked the Removed track.
- Selected "Add to Library".

Observed behaviour:
- Cloud Status changed almost immediately to Matched.
- The duplicate library entry disappeared.
- Only one track remained in the Music app.
- Historical metadata (play count, rating, etc.) was lost.
- Music references the original media file.
- A duplicate physical file with a "1" suffix remains on disk.

Questions:
- Was the original library entry replaced by the duplicate?
- Did Apple retain the original Persistent ID?
- Does the library XML still contain the historical metadata?