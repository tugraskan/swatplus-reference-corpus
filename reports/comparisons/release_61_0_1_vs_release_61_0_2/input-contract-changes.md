# SWAT+ Input Contract Changes

This is the primary source-level input change report. Filenames are resolved from the same defaults used by the schema extractor. A resolved default can still be overridden by runtime configuration.

## Summary

- Added input defaults: **0**
- Removed input defaults: **0**
- Changed read contracts: **0**
- Possible renames or replacements: **0**
- Candidate open/read blocks with unresolved filenames: **28**
- Newly unresolved filename expressions in the candidate: **1**

## Added inputs

_None._

## Removed inputs

_None._

## Changed input read contracts

_None._

## Possible renames or replacements

_None._

## Unresolved opened input filenames

The candidate contains 28 unresolved runtime filename expression(s); 1 were introduced by this comparison. Only newly introduced expressions are expanded below.
### `copy_file` at `copy_file.f90`

- Reason: opened input filename could not be resolved
- Expression(s): `source`
- Procedure: `copy_file`
- Reader: `copy_file.f90`
- Match: source_input
- Source filename expression(s): `source`
- Open: line 16, file expression `source`, parser value `source`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 21 | data | `do` | `line` |
