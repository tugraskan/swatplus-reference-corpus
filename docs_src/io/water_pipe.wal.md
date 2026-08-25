---
kind: io
source_symbols:
- water_pipe_read
title: '`water_pipe.wal`'
status: filled
source_hash: 979bea218ab0bba0
version_label: SWAT+ 62.0.0
---

**Primary target:** `pipe(:)` (array of `type water_transfer_data`)  
**Read by:** [sym:water_pipe_read]

## Bottom Line

The file `water_pipe.wal` configures water transfer infrastructure such as water towers or pipes, specifying their storage capacity, drawdown characteristics, treatment losses, and associated aquifer losses.

This file is optional; if it does not exist or is named "null", the `pipe` array is allocated with zero length.

The reader subroutine `water_pipe_read` loads this file and populates the `pipe` array accordingly.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides file existence inquiry and possibly input file handling utilities used by `water_pipe_read`. |
| [sym:water_allocation_module] | Defines the `type water_transfer_data` and related types such as `aquifer_loss` used to store the data read from `water_pipe.wal`. |
| [sym:mgt_operations_module] | Imported but no direct evidence of usage in `water_pipe_read` from the provided source lines. |
| [sym:maximum_data_module] | Provides the global maximum counts such as `db_mx%pipe` which is set to the number of pipes read from the file. |
| [sym:hydrograph_module] | Imported but no direct evidence of usage in `water_pipe_read` from the provided source lines. |
| [sym:constituent_mass_module] | Imported but no direct evidence of usage in `water_pipe_read` from the provided source lines. |

## File Variables

The file `water_pipe.wal` contains records describing water transfer units such as pipes or towers. Each record includes identifying names, storage parameters, treatment loss fractions, and aquifer loss details. The file is read sequentially and mapped into an array of `type water_transfer_data` named `pipe`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `pipe%name` | character (len=25) |  | name of the water tower or pipe |
| 3 |  | `pipe%init` | character (len=25) |  | name of the intitial concentrations |
| 4 |  | `pipe%stor_mx` | real |  | m3 !maximum storage in plant |
| 5 |  | `pipe%ddown_days` | real |  | days !days to drawdown the storage to zero |
| 6 |  | `pipe%loss_fr` | real |  | water loss during treament |
| 7 |  | `pipe%num_aqu` | integer |  | number of aquifers |
| 8 |  | `pipe%aqu_loss` | type (aquifer_loss) |  | Array of aquifer loss data for each aquifer |

## Sample

```text
Example record block from `water_pipe.wal` (format inferred from read statements):
1) Title line (character*80)
2) Integer: number of pipes (imax)
3) Header line (character*80)
4) For each pipe (1 to imax):
   a) Header line (character*80)
   b) Record line: integer id, pipe name (char*25), stor_mx (real), ddown_days (real), loss_fr (real), num_aqu (integer)
   c) Record line: integer id, pipe name (char*25), stor_mx (real), ddown_days (real), loss_fr (real), num_aqu (integer), followed by aqu_loss array entries
```

## Read Pattern

```fortran
open (107,file='water_pipe.wal')
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) imax
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i, pipe(ipipe)%name, pipe(ipipe)%stor_mx, pipe(ipipe)%ddown_days, pipe(ipipe)%loss_fr, num_aqu
read (107,*,iostat=eof) i, pipe(ipipe)%name, pipe(ipipe)%stor_mx, pipe(ipipe)%ddown_days, pipe(ipipe)%loss_fr, pipe(ipipe)%num_aqu, (pipe(ipipe)%aqu_loss(iaq), iaq = 1, num_aqu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file='water_pipe.wal')` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) imax` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i, pipe(ipipe)%name, pipe(ipipe)%stor_mx, pipe(ipipe)%ddown_days, pipe(ipipe)%loss_fr, num_aqu` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i, pipe(ipipe)%name, pipe(ipipe)%stor_mx, pipe(ipipe)%ddown_days, pipe(ipipe)%loss_fr, pipe(ipipe)%num_aqu, (pipe(ipipe)%aqu_loss(iaq), iaq = 1, num_aqu)` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:water_pipe_read] | close, open, read | Reads the `water_pipe.wal` file to populate the `pipe` array of water transfer data structures, including storage and aquifer loss parameters. It handles file existence checking and allocates the `pipe` array accordingly. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The modules `mgt_operations_module`, `hydrograph_module`, and `constituent_mass_module` are imported but not evidently used in `water_pipe_read` based on the provided source lines.
- The `aqu_loss` field is an array of `type aquifer_loss` whose detailed structure is not shown here; its meaning is inferred as aquifer-specific water loss parameters associated with each pipe.
