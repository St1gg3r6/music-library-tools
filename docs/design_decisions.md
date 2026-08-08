# Design Decisions

## DD001 - Parser Responsibility

The parser deserialises Apple Music XML into native Python objects.
It does not perform application-level transformations.

## DD002 - Date Handling

Date values are preserved as ISO 8601 strings.

Reasons:
- Lossless representation.
- Directly compatible with SQLite.
- Readily converted by Pandas.
- Avoids premature interpretation of timezone semantics.

## DD003 - Unsupported Types

During parser development, unsupported plist value types are
reported rather than raising an exception, allowing discovery
of the complete XML schema.

Once parser development is complete, unsupported types should
be considered exceptional.


## Matching Principle 001

Candidate track identity should be based on stable musical metadata (Name, Artist, Album) rather than file-specific metadata (Location, Persistent ID, Track ID) or potentially mutable metadata (Total Time).

A matching algorithm should prioritise stable musical metadata (Name, Artist, Album) and treat file-specific properties such as duration, file size and bitrate as descriptive rather than identifying.