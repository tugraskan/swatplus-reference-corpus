---
kind: procedure
symbol: readpcom
title: readpcom
status: filled
source_hash: 44cb0d0bb2894c4a
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary string used to read and discard the first title line from `plant.ini`
    during both the counting pass and the data-loading pass.
  header: Temporary string used to read and discard the second header line from `plant.ini`
    during both passes.
  name: Temporary plant/community name field used while scanning the file structure and skipping
    plant records during the count pass.
  eof: I/O status flag from each `read`; `0` means continue, and a negative value ends processing
    when the file reaches end-of-file.
  i_exist: Logical flag set by `inquire` to tell the routine whether the configured plant
    community file is present before trying to open it.
  mcom: Local counter initialized to zero and used only to form the default `db_mx%plantcom
    = mcom + 1` value when no file is available.
  icom: Loop counter for the community records in `pcomdb`; each iteration loads one plant
    community from `plant.ini`.
  imax: Running count of how many plant communities were discovered in the file; later used
    to size `pcomdb` and set `db_mx%plantcom`.
  numb: Number of plant records to skip for the current community while scanning the file
    during the first counting pass.
  ii: Inner-loop counter used to skip over each plant entry in a community during the first
    pass when only counting communities.
  mpcom: Number of plants in the current community, taken from `pcomdb(icom)%plants_com` and
    used to allocate and loop over `pcomdb(icom)%pl`.
  iplt: Loop counter for individual plant entries within one plant community.
  ipldb: Loop counter used to search the master plant database `pldb` for a matching plant
    name.
uses:
  input_file_module: The configured file name comes from `input_file_module`; `readpcom` uses
    `in_init%plant` to decide which community file to open, and it treats the special value
    `"null"` as a disabled/absent file case.
  maximum_data_module: 'The maximum-data module holds the plant-database sizes that bound
    this loader: `db_mx%plantparm` limits the search through the master plant table, and `db_mx%plantcom`
    is set by this routine to report how many communities were found.'
  plant_data_module: These module arrays and fields are the actual data containers `readpcom`
    fills. It allocates `pcomdb`, reads community and plant attributes into its components,
    and uses `pldb(ipldb)%plantnm` to resolve each community plant name to a master database
    index stored in `db_num`.
---

<!-- facts:header -->

Reads the plant community initialization database from `plant.ini` into `pcomdb` and links each community plant to the master plant database.

## Bottom Line

readpcom is the plant-community database loader. It checks whether the configured community file exists, counts how many communities it contains, allocates `pcomdb`, and then reads each community header and plant entry from `plant.ini`.

For every plant listed in a community, it searches `pldb` for a matching master plant name and stores the match index in `db_num`. If a plant name is not found, it writes a diagnostic to unit 9001. Downstream model setup depends on this routine because later code uses the populated community structure and database links.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database setup, after `proc_db` has already read earlier input tables and before later landuse and management readers run. Its output populates the plant-community database and the plant-name-to-database links that later model setup relies on when assembling plant communities and related initialization data.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the plant community file is available | The routine inquires on `in_init%plant`. If the file is missing or the filename is `"null"`, it allocates a minimal `pcomdb(0:0)` with one empty plant array and sets `db_mx%plantcom` to `mcom + 1`. |
| 2. Scan the file to count communities | When the file exists, the routine opens unit 113 on `in_init%plant`, reads the title and header, then loops through each community record, skipping the declared number of plant lines and incrementing `imax` for each community found. |
| 3. Allocate community storage | After the count pass, it allocates `pcomdb(0:imax)` so there is one slot per community plus the zero index. |
| 4. Rewind and reread file headers | The routine rewinds unit 113 and rereads the title and header lines so it can perform a fresh pass that loads actual data values. |
| 5. Read each plant community record | For each community index, it reads the community name, plant count, and initial rotation year, stores the plant count in `mpcom`, and allocates the community's plant array `pcomdb(icom)%pl(mpcom)`. |
| 6. Load each plant entry and resolve the master database index | Within each community, the routine reads each plant's initialization fields, searches `pldb` up to `db_mx%plantparm` for a matching `plantnm`, stores the match in `db_num`, and writes a diagnostic if no match is found. |
| 7. Record the final community count and close the file | After loading is complete, it stores the final `imax` in `db_mx%plantcom` and closes unit 113. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_init` | `in_init%plant` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plantcom, db_mx%plantparm` |
| [sym:plant_data_module] | `pcomdb, pldb` | `pcomdb(0)%pl(0:0), pcomdb(icom)%name, pcomdb(icom)%plants_com, pcomdb(icom)%rot_yr_ini, pcomdb(icom)%pl(mpcom), pcomdb(icom)%pl(iplt)%cpnm, pcomdb(icom)%pl(iplt)%igro, pcomdb(icom)%pl(iplt)%lai, pcomdb(icom)%pl(iplt)%bioms, pcomdb(icom)%pl(iplt)%phuacc, pcomdb(icom)%pl(iplt)%pop, pcomdb(icom)%pl(iplt)%fr_yrmat, pcomdb(icom)%pl(iplt)%rsdin, pldb(ipldb)%plantnm, pcomdb(icom)%pl(iplt)%db_num` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%plantcom` | After the file scan and load pass completes, or immediately with the default missing-file branch. | `db_mx%plantcom` is updated to report how many plant communities were found in `plant.ini`; if the file is absent or disabled it is set from the default minimal count, otherwise it is set to `imax` after the scan. |
| `pcomdb(icom)%pl(iplt)%db_num` | When a plant code read from `plant.ini` matches `pldb(ipldb)%plantnm` during the search loop. | `pcomdb(icom)%pl(iplt)%db_num` is set to the matching master-plant index so the community plant entry can be linked to the corresponding record in `pldb`. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed `readpcom`. The original file was added in df07e3f with the present read-and-link workflow. In 39fabde, only local variable initializations were changed: `titldum`, `header`, `name`, `eof`, `mcom`, `icom`, `imax`, `numb`, `ii`, `mpcom`, `iplt`, and `ipldb` were given explicit initial values, while the file I/O and database logic remained the same in the diff shown.

- df07e3f introduced the routine and its plant-community loading logic, including allocation of `pcomdb`, the two-pass scan of `plant.ini`, and matching each community plant against `pldb`.
- 39fabde did not change the algorithm; it only added explicit initial values to local variables used by the routine.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'readpcom' has no extracted documentation comment.
