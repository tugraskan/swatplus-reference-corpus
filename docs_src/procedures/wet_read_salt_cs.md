---
kind: procedure
symbol: wet_read_salt_cs
title: wet_read_salt_cs
status: filled
source_hash: 5b12406ecc6571af
version_label: SWAT+ 62.0.0
locals:
  i: Scratch integer used to read the first value from each wetland record only to test whether
    another data line remains before rereading the same record with the full derived-type
    input.
  header: Temporary 80-character buffer that receives and discards the two header/title lines
    at the top of `wetland.wet_cs`.
  eof: I/O status flag for the record reads; negative status is used to detect end-of-file
    and stop the loop.
  imax: Initialized but not used in the shown routine body; it appears to be a leftover counter
    placeholder for maximum record count.
  i_exist: Logical flag set by `inquire` to decide whether `wetland.wet_cs` exists and the
    rest of the routine should run.
  iwet: Loop counter for the wetland entry being read and mapped from the input file into
    the shared wetland arrays.
  k: First field read from each wetland record before the full derived-type record is reread;
    it is not otherwise used in the shown code.
  isalt: Loop counter used to search the reservoir salt master table for a name match.
  ics: Loop counter used to search the reservoir constituent-species master table for a name
    match.
uses:
  maximum_data_module: 'The maximum-count fields set the allocation and search bounds for
    this reader: `db_mx%wet_dat` determines how many wetland records to allocate/read, while
    `db_mx%res_salt` and `db_mx%res_cs` bound the lookup loops that translate names to indices.'
  reservoir_data_module: These shared arrays hold both the raw string inputs and the resolved
    integer references for wetland salt and constituent-species links. This routine fills
    `wet_dat_c_cs` from the file and writes the matched indices into `wet_dat`.
  constituent_mass_module: The routine compares each file-provided salt name against `res_salt_data(isalt)%name`
    to find which salt definition the wetland record should point to.
  reservoir_module: This module owns the wetland reservoir records that receive the resolved
    integer links, so the routine updates `wet_dat(iwet)%salt` and `wet_dat(iwet)%cs` in place.
  res_salt_module: The constituent-species module provides the master name list used to resolve
    each wetland record’s `cs` string into the corresponding integer index.
  res_cs_module: The cs master table is searched by name so the wetland input can be converted
    from a string reference into the numeric identifier stored in `wet_dat(iwet)%cs`.
---

<!-- facts:header -->

Reads the wetland salt and constituent-species lookup file and translates its string names into integer indices.

## Bottom Line

wet_read_salt_cs opens `wetland.wet_cs`, skips the two header lines, and reads each wetland record into `wet_dat_c_cs`. It then matches the file’s salt and constituent-species names against the master lists in `res_salt_data` and `res_cs_data`, storing the resolved indices in `wet_dat(iwet)%salt` and `wet_dat(iwet)%cs`.

The routine matters because later reservoir/wetland processing uses those integer cross-references instead of the raw names from the input file. If the file is missing, it simply leaves the shared wetland mapping state unchanged.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This reader runs during model/input setup after `wetland.wet_cs` is available in the working directory. It prepares the wetland-to-reservoir salt and constituent-species references that downstream wetland and reservoir routines rely on when they need integer links instead of text names.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check for the input file | The routine clears local status variables, inquires whether `wetland.wet_cs` exists, and only continues if the file is present. |
| 2. Open the file and skip the two header records | It opens `wetland.wet_cs` on unit 105 and reads two header lines into the temporary `header` buffer to move the file position to the first data record. |
| 3. Allocate wetland character-input storage | It allocates `wet_dat_c_cs` to the size of `db_mx%wet_dat` so each wetland entry can store the raw salt and cs names from the file. |
| 4. Loop over wetland records with end-of-file detection | For each wetland slot, it peeks at the next record using a one-field read into `i`; if the end of file is reached, it exits. Otherwise it backspaces and rereads the same record as `k, wet_dat_c_cs(iwet)`. |
| 5. Resolve the salt name to a salt index | It scans `res_salt_data` for a matching `name` and stores the matching position in `wet_dat(iwet)%salt`. |
| 6. Resolve the cs name to a cs index | It scans `res_cs_data` for a matching `name` and stores the matching position in `wet_dat(iwet)%cs`. |
| 7. Close the file and return | After all records are processed, it closes unit 105 and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wet_dat, db_mx%res_salt, db_mx%res_cs` |
| [sym:reservoir_data_module] | `wet_dat_c_cs, wet_dat` | `wet_dat_c_cs(iwet)%salt, wet_dat(iwet)%salt, wet_dat_c_cs(iwet)%cs, wet_dat(iwet)%cs` |
| [sym:constituent_mass_module] | `res_salt_data` | `res_salt_data(isalt), res_salt_data(isalt)%name` |
| [sym:reservoir_module] | `wet_dat` | `wet_dat(iwet), wet_dat(iwet)%salt, wet_dat(iwet)%cs` |
| [sym:res_salt_module] | `res_salt_data` | `res_salt_data(isalt)%name` |
| [sym:res_cs_module] | `res_cs_data` | `res_cs_data(ics)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wet_dat(iwet)%salt` | When a record’s `salt` string matches `res_salt_data(isalt)%name` inside the `do isalt = 1, db_mx%res_salt` search. | The wetland record’s salt reference is converted from a text name to the corresponding salt-table index so later routines can use numeric lookups. |
| `wet_dat(iwet)%cs` | When a record’s `cs` string matches `res_cs_data(ics)%name` inside the `do ics = 1, db_mx%res_cs` search. | The wetland record’s constituent-species reference is converted from a text name to the matching cs-table index for downstream use. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in df07e3f with the full `wetland.wet_cs` reader, including header skipping, record lookahead/backspace logic, and name-to-index mapping for salt and cs. 35b029c made only a formatting/end-of-file cleanup at the end of the subroutine, and 39fabde initialized the local counters and header buffer without changing the read or mapping logic.

- df07e3f added the complete `wet_read_salt_cs` subroutine and its file-reading/name-resolution behavior.
- 35b029c only adjusted the trailing `return`/`end subroutine` formatting and removed an extra blank line.
- 39fabde initialized `i`, `header`, `eof`, `imax`, `iwet`, `k`, `isalt`, and `ics` to default values but did not change the algorithm.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'wet_read_salt_cs' has no extracted documentation comment.
- constituent_mass_module and reservoir_module are imported in the source, but no resolved symbols from those modules were identified in the extracted evidence for this routine.
