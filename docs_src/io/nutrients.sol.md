---
kind: io
source_symbols:
- solt_db_read
title: '`nutrients.sol`'
status: filled
source_hash: 071650038641bd58
version_label: SWAT+ 62.0.0
---

**Primary target:** `solt_db(:)` (array of `type soiltest_db`)  
**Read by:** [sym:solt_db_read]

## Bottom Line

The file `nutrients.sol` configures soil test parameters related to phosphorus and nitrogen content and humus characteristics in soil layers.

It is optional; if the file does not exist or is set to "null", an empty soil test database array is allocated.

The reader `solt_db_read` loads this file and populates the array `solt_db` of type `soiltest_db`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input file path variable `in_sol%nut_sol` used to locate `nutrients.sol`. |
| [sym:maximum_data_module] | provides the global variable `db_mx%soiltest` which is set to the number of soil test records read. |
| [sym:soil_data_module] | provides the derived type `soiltest_db` and the allocatable array `solt_db` where the file records are stored. |

## File Variables

The file `nutrients.sol` contains tabular soil test data records, each mapping to one element of the `solt_db` array of type `soiltest_db`. Each record includes soil test parameters such as phosphorus and nitrate concentrations, humus fractions, and related ratios.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `solt_db%name` | character(len=16) |  | soil test name or identifier |
| 3 |  | `solt_db%exp_co` | real |  | depth coefficient to adjust concentrations for depth |
| 4 |  | `solt_db%lab_p` | real | ppm | labile phosphorus concentration in soil surface |
| 5 |  | `solt_db%nitrate` | real | ppm | nitrate nitrogen concentration in soil surface |
| 6 |  | `solt_db%fr_hum_act` | real | 0-1 | fraction of soil humus that is active |
| 7 |  | `solt_db%hum_c_n` | real | ratio | humus carbon to nitrogen ratio (typical range 8-12) |
| 8 |  | `solt_db%hum_c_p` | real | ratio | humus carbon to phosphorus ratio (typical range 70-90) |
| 9 |  | `solt_db%inorgp` | real | ppm | inorganic phosphorus in soil surface (not currently used) |
| 10 |  | `solt_db%watersol_p` | real | ppm | water soluble phosphorus in soil surface (not currently used) |
| 11 |  | `solt_db%h3a_p` | real | ppm | H3A phosphorus in soil surface (not currently used) |
| 12 |  | `solt_db%mehlich_p` | real | ppm | Mehlich phosphorus in soil surface (not currently used) |
| 13 |  | `solt_db%bray_strong_p` | real | ppm | Bray phosphorus in soil surface (not currently used) |

## Sample

```text
Example record lines are not present in the source; please refer to a reference dataset such as Ames_sub1 for a real example.
```

## Read Pattern

```fortran
open (107,file=in_sol%nut_sol)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) solt_db(isolt)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_sol%nut_sol)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) solt_db(isolt)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:solt_db_read] | open, read, rewind, close | Reads the `nutrients.sol` file if it exists and is not set to "null". It counts the number of soil test records, allocates the `solt_db` array accordingly, then reads all soil test records into `solt_db`. It also enforces a maximum value of 0.005 for the `exp_co` field by resetting higher values to 0.001. If the file does not exist or is "null", it allocates an empty `solt_db` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as per the existence check and null string test in the reader.
- No example record lines are present in the source; users should consult reference datasets for sample data formatting.
