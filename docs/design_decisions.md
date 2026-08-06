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