## XML Discovery

- Root tag is 'plist'

- Root contains 1 record


## Development Notes

### Jupyter and editable packages

When functions or classes are renamed in the source package,
restart the notebook kernel before re-importing.

Reason:
Python caches imported modules for the lifetime of the kernel.


## Function Design

Keep functions as simple as possible.

- Prefer a single, readable implementation.
- Do not abstract one-line conversions into separate functions.
- Extract a private helper only when:
  - the conversion is no longer trivial,
  - the logic is reused,
  - or readability is improved.

## Dates

Dates are preserved as ISO 8601 strings.
The parser aims to preserve the original plist representation where practical. Consumers such as Pandas or analysis code are responsible for converting date strings to datetime objects when required.

Convert only when the conversion is unambiguous and universally useful. Otherwise, preserve the original representation.