---
kind: io
source_symbols:
- aqu_read
title: '`aquifer.aqu`'
status: filled
source_hash: 14d53ad436734a0d
version_label: SWAT+ 62.0.0
---

**Primary target:** `aqudb(:)` (array of `type aquifer_database`)  
**Read by:** [sym:aqu_read]

## Bottom Line

`aquifer.aqu` defines one record per aquifer object. Each record sets the baseflow recession parameters, initial water-table depth, initial chemistry, and the recharge and revap controls used by the lumped (non-gwflow) aquifer module.

The reader `aqu_read` skips a title line and a column-header line, scans the first column to size the array, then reads each record into `aqudb` (an array of `type aquifer_database`) using the first column as the aquifer id / array index.

The file is required for aquifer simulation: if `in_aqu%aqu` is missing or set to `"null"`, `aqudb` is allocated with zero size and no aquifer properties are loaded.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Supplies `in_aqu` (`type input_aqu`); `in_aqu%aqu` holds the `aquifer.aqu` filename the reader opens on unit 107. |
| [sym:aquifer_module] | Defines `type aquifer_database` and the allocatable array `aqudb` that each record is read into. |
| [sym:basin_module] | Supplies `bsn_cc`; the reader contains `bsn_cc%gwflow = 0` to select the lumped aquifer path, though that statement sits after the loop `exit` and is unreachable as written. |
| [sym:maximum_data_module] | Supplies `db_mx`; the reader stores the number of aquifer records in `db_mx%aqudb` after the first counting pass. |

## File Variables

`aquifer.aqu` is a whitespace-delimited table with two header lines (a title line and a column-header line) followed by one record per aquifer. The first value on each record is the aquifer id, used directly as the index into `aqudb`; the remaining values populate the fields of `type aquifer_database` in declaration order. The SWAT+ editor writes column headers that differ from the source field names (e.g. `gw_flo` -> `flo`, `no3_n` -> `no3`); the list-directed read relies on column order, not the header text.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `id` | `k` | integer | none | aquifer id read from the record; used directly as the index `i` into `aqudb`. |
| 2 | `name` | `aqudb%aqunm` | character(len=16) |  | aquifer name |
| 3 | `init` | `aqudb%aqu_ini` | character(len=16) |  | initial aquifer data- points to name in initial.aqu |
| 4 | `gw_flo` | `aqudb%flo` | real | mm | flow from aquifer in current time step |
| 5 | `dep_bot` | `aqudb%dep_bot` | real | m | depth - mid-slope surface to bottom of aquifer |
| 6 | `dep_wt` | `aqudb%dep_wt` | real | m | depth - mid-slope surface to water table (initial) |
| 7 | `no3_n` | `aqudb%no3` | real | ppm NO3-N | nitrate-N concentration in aquifer (initial) |
| 8 | `sol_p` | `aqudb%minp` | real | ppm P | mineral phosphorus concentration in aquifer (initial) |
| 9 | `carbon` | `aqudb%cbn` | real | percent | organic carbon in aquifer (initial) |
| 10 | `flo_dist` | `aqudb%flo_dist` | real | m | average flow distance to stream or object |
| 11 | `bf_max` | `aqudb%bf_max` | real | mm | maximum daily baseflow - when all channels are contributing |
| 12 | `alpha_bf` | `aqudb%alpha` | real | 1/days | lag factor for groundwater recession curve |
| 13 | `revap` | `aqudb%revap_co` | real |  | revap oefficient - evap=pet*revap_co |
| 14 | `rchg_dp` | `aqudb%seep` | real | frac | fraction of recharge that seeps from aquifer |
| 15 | `spec_yld` | `aqudb%spyld` | real | m^3/m^3 | specific yield of aquifer |
| 16 | `hl_no3n` | `aqudb%hlife_n` | real | days | half-life of nitrogen in groundwater |
| 17 | `flo_min` | `aqudb%flo_min` | real | m | water table depth for return flow to occur |
| 18 | `revap_min` | `aqudb%revap_min` | real | m | water table depth for revap to occur |

## Sample

```text
refdata/Osu_1hru/aquifer.aqu:

aquifer.aqu: written by SWAT+ editor v2.2.0 on 2023-03-22 04:25 for SWAT+ rev.60.5.4
id  name         init      gw_flo   dep_bot   dep_wt    no3_n  sol_p  carbon   flo_dist  bf_max   alpha_bf  revap    rchg_dp  spec_yld  hl_no3n  flo_min  revap_min
 1  aqu011       initaqu1  0.05000  10.00000  6.00000   0.0    0.0    0.50000  50.00000  1.00000  0.95000   0.02000  0.01000  0.05000   0.0      5.00000  5.00000
 2  aqu012       initaqu1  0.05000  10.00000  6.00000   0.0    0.0    0.50000  50.00000  1.00000  0.95000   0.02000  0.01000  0.05000   0.0      5.00000  5.00000
21  aqu_deep010  initaqu1  0.00000  10.00000  20.00000  0.0    0.0    0.50000  50.00000  1.00000  0.91000   0.00000  0.00000  0.03000   0.0      0.0      0.0
```

## Read Pattern

```fortran
open (107,file=in_aqu%aqu)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
backspace (107)
read (107,*,iostat=eof) k, aqudb(i)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_aqu%aqu)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, aqudb(i)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:aqu_read] | backspace, close, open, read, rewind | Opens `aquifer.aqu` on unit 107, skips the title and column-header lines, scans the first column to count records and find the maximum id, allocates `aqudb(0:imax)`, then rewinds and reads each record into `aqudb(i)` keyed by the id column. |

## Review Notes

- The `init` column cross-walks to a `name` row in `initial.aqu`; the example value `initaqu1` must exist there.
- The SWAT+ editor header names differ from the source field names (`gw_flo`->`flo`, `no3_n`->`no3`, `sol_p`->`minp`, `carbon`->`cbn`, `alpha_bf`->`alpha`, `revap`->`revap_co`, `rchg_dp`->`seep`, `spec_yld`->`spyld`, `hl_no3n`->`hlife_n`). Only column order matters to the list-directed read.
- A deep aquifer record (e.g. `aqu_deep010`) typically has `gw_flo = 0` and zero baseflow/revap thresholds.
- `bsn_cc%gwflow = 0` appears after the loop `exit` in `aqu_read`, so it is unreachable as currently written.
- If `aquifer.aqu` is missing or set to `null`, `aqudb` is allocated with zero size.
