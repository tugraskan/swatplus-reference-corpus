---
kind: procedure
symbol: cs_hru_read
title: cs_hru_read
status: filled
source_hash: f05130cda330f9a2
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard title or record text while scanning
    and re-reading `cs_hru.ini`.
  header: Scratch character buffer used to skip header lines in `cs_hru.ini` before the data
    records are counted and loaded.
  ics: Loop index over constituent HRU records; used first to count records indirectly and
    then to allocate and populate each `cs_soil_ini` element.
  eof: I/O status flag from each `read`; negative values signal end-of-file or a failed read,
    and zero keeps the scan/load loops going.
  imax: Counter for the number of HRU constituent records found in `cs_hru.ini`; it becomes
    the allocation size and is stored in `db_mx%cs_ini`.
  i_exist: Logical flag set by `inquire` to indicate whether `cs_hru.ini` exists before attempting
    to open and read it.
uses:
  constituent_mass_module: This module holds the shared constituent database types and storage
    that `cs_hru_read` fills. The routine allocates `cs_soil_ini(imax)` and then populates
    each element's `name`, `soil`, and `plt` fields, while `cs_db%num_cs` determines the length
    of the soil and plant concentration arrays that are allocated for each record.
  input_file_module: This module is imported by the routine, but the extracted source does
    not resolve any directly referenced symbols from it. It still matters because the reader
    is part of the model's shared input-file workflow and may rely on module-wide input handling
    conventions even though no specific `input_file_module` symbol appears in the visible
    body.
  maximum_data_module: This module provides the shared maximum-data counters where the routine
    stores how many HRU constituent records were found. `db_mx%cs_ini` records the discovered
    record count so other code can size or validate later constituent processing.
---

<!-- facts:header -->

Reads the HRU constituent initial-condition file `cs_hru.ini` and loads soil and plant concentration arrays for each constituent entry.

## Bottom Line

`cs_hru_read` is the HRU constituent setup reader. It opens `cs_hru.ini`, counts how many constituent records are present, allocates `cs_soil_ini` to that size, and then loads each record's constituent name plus soil and plant starting concentrations.

The routine matters because it seeds the shared constituent database for later HRU simulations. Downstream routines use the populated `cs_soil_ini` entries and the stored count in `db_mx%cs_ini` to drive constituent initialization and other constituent-specific reads.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the input-reading phase, when `proc_read` calls it as part of the constituent setup sequence. It expects `cs_db%num_cs` to already be available so it can size the soil and plant arrays, and its results feed later constituent initialization and other constituent-specific readers that depend on `cs_soil_ini` and `db_mx%cs_ini`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the input file is available. | The routine uses `inquire` to test for `cs_hru.ini` and enters the read logic when the file exists, using the `i_exist` flag to control that decision. |
| 2. Open the file and skip the leading header lines. | The routine opens unit 107 on `cs_hru.ini` and reads one title line plus four header lines into scratch variables, stopping early if any read signals end-of-file. |
| 3. Count how many data records are present. | After resetting `imax` to zero, the routine loops through the file three tokens at a time, incrementing `imax` for each record-like group until a read reports end-of-file. |
| 4. Save the record count and allocate storage. | The routine stores the discovered count in `db_mx%cs_ini`, allocates `cs_soil_ini(imax)`, and then allocates each element's `soil` and `plt` arrays using `cs_db%num_cs + cs_db%num_cs` as the size. |
| 5. Rewind and skip the headers again. | The routine rewinds unit 107 to the beginning of `cs_hru.ini` and repeats the title/header reads so the file is positioned at the first data record for the actual load pass. |
| 6. Read each HRU constituent record into shared state. | For each record, the routine reads the constituent name, then the soil concentrations, then the plant concentrations into the corresponding `cs_soil_ini(ics)` element. |
| 7. Close the input file and finish. | The routine closes unit 107, exits the outer loop, and returns to the caller after the shared constituent state has been populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `cs_soil_ini, cs_db` | `cs_soil_ini(ics)%soil, cs_db%num_cs, cs_soil_ini(ics)%plt, cs_soil_ini(ics)%name` |
| [sym:input_file_module] | `input_file_module` | `input_file_module` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cs_ini` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%cs_ini` | After counting records in `cs_hru.ini` and before allocating `cs_soil_ini`. | `db_mx%cs_ini` is set to the number of HRU constituent records found in the input file so the rest of the model can know how many initial constituent entries were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved four commits that changed `cs_hru_read`. The initial addition in `df07e3f` introduced the routine to read HRU soil and plant constituent concentrations from `cs_hru.ini`. Commit `f8bb6ec` changed the `cs_soil_ini(ics)%soil` allocation to use `source = 0.` so the soil arrays are initialized on allocation. Commit `39fabde` initialized the local scalars `titldum`, `header`, `ics`, `eof`, and `imax`, and also added `source = 0.` to the `cs_soil_ini(ics)%plt` allocation. Commit `35b029c` only adjusted whitespace and the file ending without changing behavior.

- df07e3f introduced the full `cs_hru_read` workflow: open `cs_hru.ini`, count records, allocate `cs_soil_ini`, load each record, and close the file.
- f8bb6ec made the `cs_soil_ini(ics)%soil` allocation zero-initialize its values at allocation time.
- 39fabde initialized the routine's local variables and also zero-initialized `cs_soil_ini(ics)%plt` at allocation time.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- The visible source shows no resolved callee calls inside `cs_hru_read`.
- The `input_file_module` import is present, but no directly referenced symbol from that module was resolved in the extracted source.
