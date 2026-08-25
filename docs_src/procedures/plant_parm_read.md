---
kind: procedure
symbol: plant_parm_read
title: plant_parm_read
status: filled
source_hash: ef5be88009e91a4a
version_label: SWAT+ 62.0.0
locals:
  ic: '`ic` is the loop counter for plant records. It indexes the current plant entry while
    the routine scans `plants.plt` to count records and then rereads them into `pldb`, `pl_class`,
    and the optional partition-fraction array.'
  titldum: '`titldum` is a scratch character variable used to read and discard the file title
    line and to advance through records while counting rows. It is also used during the second
    pass when the file is rewound.'
  header: '`header` holds the database header line read from `plants.plt`. The routine reads
    it after the title on both passes so the remaining lines can be treated as data records.'
  eof: '`eof` receives the `iostat` status from each read. The routine uses it to detect end-of-file
    and stop the scan or data-loading loop cleanly.'
  imax: '`imax` counts how many plant records are present in `plants.plt`. The routine computes
    it during the first pass and then uses it to allocate the plant arrays and to set `db_mx%plantparm`.'
  mpl: '`mpl` is initialized but not used anywhere in the visible routine body. It appears
    to be a leftover counter or placeholder variable.'
  i_exist: '`i_exist` stores the result of the `inquire` check for the configured plant database
    file. It decides whether the routine should read `plants.plt` or fall back to a zero-length
    allocation path.'
uses:
  input_file_module: '`input_file_module` supplies `in_parmdb%plants_plt`, the configured
    path to the plant database file. That path controls which file this routine opens and
    whether the file is treated as present or disabled.'
  maximum_data_module: '`maximum_data_module` provides `db_mx%plantparm`, the shared record-count
    output for the plant database. This matters because other routines need the final number
    of loaded plant entries to size or iterate over plant data.'
  plant_data_module: '`plant_data_module` holds the shared arrays and derived partition-fraction
    types that this routine fills. The loaded contents of `pldb`, `pl_class`, and `cswat_1_part_fracs`
    become the plant parameter state used by later plant growth and residue/carbon calculations.'
  basin_module: '`basin_module` supplies `bsn_cc`, whose control flags decide which branch
    the routine uses after reading each plant record. `bsn_cc%cswat` selects whether lignin-based
    partition fractions are derived, and `bsn_cc%nam1` decides whether the optional `pl_class`
    field is read from the file.'
---

<!-- facts:header -->

Reads the plant parameter database from plants.plt into shared plant arrays. It also sets default or derived residue-partition fractions and records how many plant entries were loaded.

## Bottom Line

plant_parm_read loads the plant database file named by `in_parmdb%plants_plt`, counts how many plant records it contains, allocates the shared plant arrays to match, and then reads each plant record into `pldb`. While loading, it enforces a minimum maturity age of 1 year and, depending on the basin carbon setting, either derives lignin-based partition fractions or restores default residue partition fractions.

The routine matters because later SWAT+ code uses the loaded plant database, class labels, and partition fractions to drive plant growth, residue behavior, and carbon-related calculations. It also stores the final record count in `db_mx%plantparm` so other routines know the size of the plant parameter database.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization, when `proc_db` is building the shared parameter databases used across the model. `proc_db` calls `plant_parm_read` before `plantparm_init` and other database readers, and later plant growth, residue, and carbon routines depend on the arrays and counts it loads.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and test file presence | The routine resets `eof`, `imax`, and `mpl`, then checks whether the configured plant database file exists and is not set to the disabled sentinel string. This decides whether it can read `plants.plt` or must fall back to an empty allocation path. |
| 2. Allocate empty storage when no file is available | If the file is missing or disabled, the routine allocates one-element-zero arrays for `pldb`, `plcp`, and `pl_class`. It also allocates `cswat_1_part_fracs` only when the carbon code branch requires it. |
| 3. Open the database and count data records | When the file is present, the routine opens `plants.plt`, reads the title and header, and then loops through the remaining lines to count how many plant records exist. Each successful read increments `imax` until end-of-file is reached. |
| 4. Allocate arrays sized to the file contents | After counting, the routine allocates `pldb`, `plcp`, and `pl_class` from index 0 through `imax`, and it allocates `cswat_1_part_fracs` when the carbon branch requires derived partition fractions. |
| 5. Rewind and skip the file title and header again | The routine rewinds `plants.plt` and rereads the title and header so the second pass starts at the first plant record. This prepares the file for actual data loading. |
| 6. Read each plant record and normalize maturity years | For each plant entry, the routine reads either `pldb(ic)` alone or `pldb(ic)` plus `pl_class(ic)` depending on `bsn_cc%nam1`, then forces `pldb(ic)%mat_yrs` to be at least 1 year. This populates the shared plant database records from the file. |
| 7. Fill carbon partition fractions or defaults | If `bsn_cc%cswat == 2`, the routine derives above-ground and below-ground lignin, structural, and metabolic fractions from the loaded residue partition values. Otherwise it restores the default residue partition fractions in `pldb(ic)%res_part_fracs`. |
| 8. Finish the record loop | The routine finishes the per-record loop and exits the surrounding `do` block after processing the file. This ends the file-reading pass once all records have been handled. |
| 9. Publish the loaded record count and close the file | The routine stores `imax` in `db_mx%plantparm`, closes unit 104, and returns to the caller. This leaves the plant database count available to the rest of the model. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_parmdb` | `in_parmdb%plants_plt` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plantparm` |
| [sym:plant_data_module] | `pldb, cswat_1_part_fracs, plcp, pl_class` | `pldb(ic)%mat_yrs, cswat_1_part_fracs(ic)%lig_frac_blg, pldb(ic)%res_part_fracs%lig_frac, cswat_1_part_fracs(ic)%lig_frac_abg, pldb(ic)%res_part_fracs%str_frac, cswat_1_part_fracs(ic)%str_frac_blg, cswat_1_part_fracs(ic)%str_frac_abg, cswat_1_part_fracs(ic)%meta_frac_blg, cswat_1_part_fracs(ic)%meta_frac_abg, pldb(ic)%res_part_fracs%meta_frac` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%cswat, bsn_cc%nam1` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pldb(ic)%mat_yrs` | When a plant record is read and `pldb(ic)%mat_yrs` is less than 1. | `pldb(ic)%mat_yrs` is forced up to at least 1 year so later model code never sees a nonpositive maturity age for a plant entry. |
| `cswat_1_part_fracs(ic)%lig_frac_blg` | When `bsn_cc%cswat == 2` for the current plant record. | `cswat_1_part_fracs(ic)%lig_frac_blg` is copied from the plant's below-ground residue lignin fraction so the carbon model can use a separate below-ground partitioning set. |
| `cswat_1_part_fracs(ic)%lig_frac_abg` | When `bsn_cc%cswat == 2` for the current plant record. | `cswat_1_part_fracs(ic)%lig_frac_abg` is copied from the plant's above-ground residue structural fraction and used as the above-ground lignin-based partition value in this routine's carbon branch. |
| `cswat_1_part_fracs(ic)%str_frac_blg` | When `bsn_cc%cswat == 2` for the current plant record. | `cswat_1_part_fracs(ic)%str_frac_blg` is computed from the below-ground lignin fraction divided by 0.80 to derive the below-ground structural fraction. |
| `cswat_1_part_fracs(ic)%str_frac_abg` | When `bsn_cc%cswat == 2` for the current plant record. | `cswat_1_part_fracs(ic)%str_frac_abg` is computed from the above-ground lignin fraction divided by 0.80 to derive the above-ground structural fraction. |
| `cswat_1_part_fracs(ic)%meta_frac_blg` | When `bsn_cc%cswat == 2` for the current plant record. | `cswat_1_part_fracs(ic)%meta_frac_blg` is set to the remainder after subtracting the below-ground structural fraction from 1.0, giving the below-ground metabolic fraction. |
| `cswat_1_part_fracs(ic)%meta_frac_abg` | When `bsn_cc%cswat == 2` for the current plant record. | `cswat_1_part_fracs(ic)%meta_frac_abg` is set to the remainder after subtracting the above-ground structural fraction from 1.0, giving the above-ground metabolic fraction. |
| `pldb(ic)%res_part_fracs%meta_frac` | When `bsn_cc%cswat` is not 2 for the current plant record. | `pldb(ic)%res_part_fracs%meta_frac` is reset to the default metabolic residue fraction of 0.85. |
| `pldb(ic)%res_part_fracs%str_frac` | When `bsn_cc%cswat` is not 2 for the current plant record. | `pldb(ic)%res_part_fracs%str_frac` is reset to the default structural residue fraction of 0.15. |
| `pldb(ic)%res_part_fracs%lig_frac` | When `bsn_cc%cswat` is not 2 for the current plant record. | `pldb(ic)%res_part_fracs%lig_frac` is reset to the default lignin residue fraction of 0.12. |
| `db_mx%plantparm` | After the routine finishes scanning or loading the plant database. | `db_mx%plantparm` is set to the number of loaded plant records so the shared maximum-data state reflects the size of `plants.plt`. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `plant_parm_read`. In 39fabde, the local counters were initialized in place, turning `ic`, `titldum`, `header`, `eof`, and `imax` into zeroed or blanked variables. In 3bb22ed, the routine gained the `pl_class` variable and the ability to allocate and read it when the file format includes class labels, plus the `backspace` fix was still absent at that point. In e22cb49, the misplaced `backspace (105)` was corrected to `backspace (104)`, fixing the file unit used when rereading the plant database. In 5e0b0b1, the routine added carbon-branch handling: it allocates `cswat_3_part_fracs` when `bsn_cc%cswat == 3`, derives above- and below-ground partition fractions from the loaded plant residue data, and otherwise restores default residue fractions. In c66dc79, the carbon-branch formulas were simplified so metabolic fractions are computed as `1.0 - structural_fraction` instead of subtracting both structural and lignin terms.

- 39fabde made the routine self-initializing by zeroing counters and blanking scratch strings before file handling begins.
- 3bb22ed extended file-format handling with the `pl_class` field and conditional reads based on `bsn_cc%nam1`.
- e22cb49 fixed the file-control bug so the routine backspaces unit 104, not unit 105, before rereading plant data.
- 5e0b0b1 added `bsn_cc%cswat == 3` branching, allocation of `cswat_3_part_fracs`, and derivation of lignin-based above- and below-ground partition fractions.
- c66dc79 changed the `cswat_3_part_fracs` metabolic-fraction formulas to use only `1.0 - structural_fraction`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'plant_parm_read' has no extracted documentation comment.
- algorithm_steps revised: split the original scan/load behavior into separate count, allocate, rewind, load, and finalize steps to match the visible control flow.
- Source shows `bsn_cc%cswat == 2` in the current span, while lineage evidence discusses a later `cswat == 3` branch; current overlay reflects the source span, and the historical notes describe the diffs as written.
