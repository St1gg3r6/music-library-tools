# Apple Music Library Investigation – Discoveries

This document records findings established during analysis of the exported Apple Music XML library. Items are categorised as **Design Principles**, **Discoveries**, **Proven Relationships**, **Observations** and **Open Questions**.

---

# Design Principles

## DP001 – Parse to native Python types

The parser converts plist values into their most appropriate native Python types as early as possible.

| plist tag | Python type |
|-----------|-------------|
| `string` | `str` |
| `integer` | `int` |
| `true` | `bool` |
| `false` | `bool` |
| `date` | `datetime.datetime` |
| `dict` | `dict` (recursive) |
| `array` | `list` |

This ensures that all downstream analysis operates on native Python objects rather than XML elements.

---

## DP002 – Preserve source metadata

The exported XML should be treated as the authoritative source.

Data normalisation (for example, the `Comments` field) should be performed on derived data only. The original metadata should remain unchanged until any metadata restoration work has been completed.

---

# Discoveries

## D001 – Track storage structure

### Evidence

- `tracks.tag == "dict"`
- `len(tracks) == 38,060`

### Conclusion

The exported library stores **Tracks** as a plist dictionary, with each track represented as a key/value pair.

---

## D002 – Individual track structure

### Evidence

The first track contains:

- Track ID: `1704`
- XML tag: `dict`
- 68 child elements

The first key/value pairs are:

- Track ID → 1704
- Name → Hells Bells
- Artist → AC/DC
- Album → Back In Black
- Genre → Rock

### Conclusion

Each track is represented as a plist dictionary containing key/value metadata.

---

## D003 – Value types present in the library

All 19,030 tracks were parsed successfully.

Supported types:

- `string`
- `integer`
- `true`
- `date`

No unsupported plist value types remain.

---

## D004 – Effect of "Add to Library" on a Removed track

**Date observed:** 2026-08-06

### Starting state

- Track Cloud Status = Removed.
- Duplicate Waiting/Matched record already existed.
- Original record contained historical metadata.

### Action

Right-click → **Add to Library**

### Observed behaviour

- Cloud Status changed almost immediately to Matched.
- Duplicate library entry disappeared.
- Only one visible library record remained.
- Historical metadata (play count, rating, etc.) was lost.
- Music referenced the original media file.
- A duplicate physical file with a numeric suffix remained on disk.

This behaviour became one of the primary motivations for the investigation.

---

# Proven Relationships

## PR001 – Track Type and Location

```
Track Type = File
        ⇔
Location exists
```

This relationship has been verified across the entire exported library.

---

## PR002 – Boolean fields are sparse

Boolean plist fields are only exported when their value is `True`.

`False` values are omitted entirely from the XML.

Examples include:

- Matched
- Purchased
- Apple Music
- Protected
- Favorited
- Loved

---

## PR003 – Library identifiers are unique

Both of the following uniquely identify library records:

- Track ID
- Persistent ID

Neither field can be used to associate an original track with its replacement.

---

## PR004 – Downloaded tracks are file-backed

Downloaded tracks, regardless of origin, have:

- `Track Type = File`
- `Location` populated

This applies to:

- Imported tracks
- Downloaded Apple Music tracks
- Downloaded matched tracks

---

# Observations

## O001 – Kind and Matched represent different concepts

`Kind` and the boolean `Matched` field are not equivalent.

For example:

- `Kind = Matched AAC audio file` does **not** necessarily imply `Matched = True`.
- `Matched = True` may appear on tracks whose `Kind` is simply `AAC audio file`.

---

## O002 – Replacement records are new library objects

When Apple creates a replacement record it creates a new library object rather than modifying the original.

Characteristics include:

- New Track ID
- New Persistent ID
- New Date Added

The original and replacement coexist until the original is removed.

---

## O003 – Replacement records lose user metadata

Replacement records consistently lose user-generated metadata including:

- Play Count
- Play Date
- Rating
- Favorited
- Loved

while typically gaining Apple catalogue metadata such as:

- Release Date
- Artwork Count
- Sort Album Artist

---

## O004 – Download mutates a replacement record

Downloading a replacement track does **not** create another library record.

Instead, the existing replacement record is modified in place.

Observed changes include:

- Track Type: Remote → File
- Location populated
- Local media file created
- Date Modified updated

Track ID and Persistent ID remain unchanged.

---

## O005 – Downloaded replacement files are separate media files

Downloaded replacement tracks do not overwrite the original imported files.

Instead Apple creates a second local file, typically with a numeric suffix (for example, `Strength 2.m4a`).

---

## O006 – Apple may substitute a different master

Downloaded replacement files may differ from the original imported file.

Observed differences include:

- Duration
- File size
- Normalization value

This supports treating file characteristics as descriptive rather than identifying metadata.

---

# Open Questions

- Why do downloaded replacement tracks become `Purchased AAC audio file` rather than `Matched AAC audio file`?
- What exactly does the Music application's **Waiting** state represent?
- Why are Waiting tracks not downloadable?
- Can replacement records be reliably identified before user metadata is lost?
- Can historical metadata be safely transferred from an original record to its replacement?
- Which metadata fields provide the most reliable identity for matching original and replacement tracks?