---
kind: procedure
symbol: read_mgtops
title: read_mgtops
status: filled
source_hash: 8e61b68b5213dcc6
version_label: SWAT+ 62.0.0
args:
  isched: '`isched` selects which already-allocated management schedule in `sched` to read
    and populate; every read, date conversion, and database lookup is performed for that schedule
    only.'
locals:
  iyear: Tracks the current management year number while the schedule is being read. It starts
    at 1 and is incremented when an operation code of `skip` marks the end of a year.
  day: Holds the current operation day-of-month copied from `sched(isched)%mgt_ops(iop)%day`
    so it can be passed to `Jdt`.
  mon: Holds the current operation month copied from `sched(isched)%mgt_ops(iop)%mon` so it
    can be passed to `Jdt`.
  iop: Indexes the current operation within `sched(isched)%mgt_ops` during the schedule loop.
  jdt: Local external function name for the Julian-day conversion routine. It is declared
    so the routine can call `Jdt` to turn month/day into a day-of-year value.
  idb: Temporary database index used while scanning each lookup table for a matching operation
    name; when a match is found, it is stored into the operation record.
uses:
  maximum_data_module: These maximum counters define the valid bounds for every database search
    loop in this routine. `read_mgtops` uses them to know how many plant communities, plant
    parms, transplant records, harvest ops, tillage parms, irrigation ops, fertilizer parms,
    chemical application ops, manure parms, pesticide parms, grazing ops, fire ops, and sweep
    ops it must scan when crosswalking text names to indices.
  plant_data_module: These database arrays provide the text names that management operations
    are matched against. `read_mgtops` compares schedule fields such as `op_char` and `op_plant`
    to the plant community, plant, and transplant names so it can store the correct numeric
    references in the schedule record.
  mgt_operations_module: This module owns the management schedule and operation records that
    `read_mgtops` populates. The routine writes the derived date fields, database indices,
    and irrigation flag into `sched(isched)%mgt_ops(iop)` so later management logic can execute
    the schedule without repeated string matching.
  tillage_data_module: Tillage names come from the tillage database, and the `till` case resolves
    the schedule's tillage operation by comparing `op_char` against `tilldb(idb)%tillnm`.
    That lookup is what supplies the tillage operation index used later by management execution.
  fertilizer_data_module: Fertilizer and manure operations both rely on database names to
    resolve the chosen material and application type. `read_mgtops` matches schedule text
    against `fertdb` or `manure_db`, then uses `chemapp_db` to resolve the application mode
    for fertilizer, manure, and pesticide operations.
  pesticide_data_module: Pesticide operations also require a text-to-index lookup before the
    schedule can be used later. The routine compares `op_char` with `pestdb(idb)%name` to
    store the pesticide database index in the operation record.
  time_module: '`ndays` is the month-end day table passed into `Jdt` so each operation''s
    month and day can be converted into a Julian day-of-year. That derived day number is stored
    on the schedule and used later for calendar-based management timing.'
---

<!-- facts:header -->

Reads one management schedule and crosswalks each scheduled operation to the database indices and calendar fields it needs later in SWAT+.

## Bottom Line

read_mgtops walks through the operations already allocated for one schedule and fills in each record with derived dates and database pointers. It reads the raw operation fields from unit 107, converts the month/day into a Julian day, tracks the schedule year across `skip` boundaries, and matches each operation's text names against the corresponding plant, tillage, irrigation, fertilizer, manure, pesticide, harvest, grazing, fire, and street-sweep databases.

The routine matters because later management execution uses the resolved indices and flags stored in `sched(isched)%mgt_ops(iop)` instead of the raw text names. It also reports an error to unit 9001 when a planting operation name cannot be found in `plants.plt`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after `mgt_read_mgtops` has read the schedule metadata, counted `num_ops`, allocated `sched(isched)%mgt_ops`, and positioned the shared management input stream at the operation records. Its results feed later management simulation because downstream code depends on the resolved indices, `jday`, `year`, and irrigation flag stored here.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over every allocated operation in the selected schedule | Initializes the year counter and iterates through `sched(isched)%mgt_ops` from 1 to `sched(isched)%num_ops`, processing one schedule record at a time. |
| 2. Read the raw operation record | Reads the operation code, month, day, heat-unit threshold, operation text, plant text, and override amount from unit 107 into the current management operation entry. |
| 3. Derive date fields for the current operation | Copies the month and day into local variables, converts them to a Julian day with `Jdt(ndays,day,mon)`, stores the current management year, and increments the year counter after a `skip` operation. |
| 4. Match plant-community operations | For `pcom`, scans the plant community database until `op_char` matches `pcomdb(idb)%name`, then stores that database index in `op1`. |
| 5. Match planting and transplant operations | For `plnt`, finds the plant database index from `pldb(idb)%plantnm`, writes an error to unit 9001 if no plant is found, and crosswalks the transplant name in `op_plant` to `transpl(idb)%name` for `op4`. |
| 6. Match harvest and kill-harvest operations | For `harv` and `hvkl`, scans the harvest-operation database and stores the matching harvest operation index in `op1` using the `op_plant` text field. |
| 7. Match tillage operations | For `till`, scans `tilldb` for a matching tillage name and stores the tillage database index in `op1`. |
| 8. Match irrigation operations and flag the schedule | For `irrm` and `irrp`, sets the schedule irrigation flag to 1 and resolves the irrigation operation name against `irrop_db`, storing the matching index in `op1`. |
| 9. Match fertilizer operations | For `fert`, resolves the fertilizer material name against `fertdb` into `op1` and the chemical application type against `chemapp_db` into `op4`. |
| 10. Match manure operations | For `manu`, resolves the manure database entry against `manure_db` into `op1` and the application type against `chemapp_db` into `op4`. |
| 11. Match pesticide operations | For `pest`, resolves the pesticide database entry against `pestdb` into `op1` and the application type against `chemapp_db` into `op4`. |
| 12. Match grazing operations | For `graz`, scans the grazing-operation database and stores the matching grazing operation index in `op1`. |
| 13. Match fire operations | For `burn`, scans the fire-operation database and stores the matching fire operation index in `op1`. |
| 14. Match street-sweep operations | For `swep`, scans the street-sweep database and stores the matching sweep operation index in `op1` before ending the case block and continuing to the next scheduled operation. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plantcom, db_mx%plantparm, db_mx%transplant, db_mx%harvop_db, db_mx%tillparm, db_mx%irrop_db, db_mx%fertparm, db_mx%chemapp_db, db_mx%manureparm, db_mx%pestparm, db_mx%grazeop_db, db_mx%fireop_db, db_mx%sweepop_db` |
| [sym:plant_data_module] | `pcomdb, pldb, transpl` | `pcomdb(idb)%name, pldb(idb)%plantnm, transpl(idb)%name` |
| [sym:mgt_operations_module] | `sched, harvop_db, irrop_db, chemapp_db, grazeop_db, fire_db, sweepop_db, mgt` | `sched(isched)%num_ops, sched(isched)%mgt_ops(iop)%op, sched(isched)%mgt_ops(iop)%mon, sched(isched)%mgt_ops(iop)%day, sched(isched)%mgt_ops(iop)%husc, sched(isched)%mgt_ops(iop)%op_char, sched(isched)%mgt_ops(iop)%op_plant, sched(isched)%mgt_ops(iop)%op3, sched(isched)%mgt_ops(iop)%jday, sched(isched)%mgt_ops(iop)%year, sched(isched)%mgt_ops(iop)%op1, sched(isched)%mgt_ops(iop)%op4, harvop_db(idb)%name, sched(isched)%irr, irrop_db(idb)%name, chemapp_db(idb)%name, grazeop_db(idb)%name, fire_db(idb)%name, sweepop_db(idb)%name` |
| [sym:tillage_data_module] | `tilldb` | `tilldb(idb)%tillnm` |
| [sym:fertilizer_data_module] | `fertdb, manure_db` | `fertdb(idb)%fertnm, manure_db(idb)%name` |
| [sym:pesticide_data_module] | `pestdb` | `pestdb(idb)%name` |
| [sym:time_module] | `ndays` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sched(isched)%mgt_ops(iop)%jday` | For every operation after `day` and `mon` are read from unit 107. | `sched(isched)%mgt_ops(iop)%jday` is set to the Julian day-of-year returned by `Jdt(ndays,day,mon)`, so the schedule has a calendar day number that downstream management timing can use. |
| `sched(isched)%mgt_ops(iop)%year` | For every operation after the current year counter `iyear` is assigned. | `sched(isched)%mgt_ops(iop)%year` stores the management year number for this record. It starts at 1 for the schedule and increments after any operation whose code is `skip`, marking the next year's operations. |
| `sched(isched)%mgt_ops(iop)%op1` | When the operation code is one of the database-mapped cases and the matching name is found in the relevant lookup table. | `sched(isched)%mgt_ops(iop)%op1` changes from its default zero value to the resolved database index for the selected plant community, plant, harvest, tillage, irrigation, fertilizer, manure, pesticide, grazing, fire, or sweep operation. |
| `sched(isched)%mgt_ops(iop)%op4` | Only for fertilizer, manure, and pesticide operations after matching the application type in `chemapp_db`. | `sched(isched)%mgt_ops(iop)%op4` stores the chemical application operation index that describes how the material is applied, so later management code can use the application mode along with the material lookup. |
| `sched(isched)%irr` | When the current operation code is `irrm` or `irrp`. | `sched(isched)%irr` is set to 1 to mark that the selected schedule contains irrigation operations. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved four behavior-changing commits plus one formatting/termination update. The procedure was created in df07e3f with the full operation-read and lookup logic; 94b6dec added an explicit `search, jdt` external declaration and changed the final `end` to `end subroutine read_mgtops`; 88ac4f1 added the `manu` case with manure and chemical-application crosswalks; 561bc28 changed that manure case to use `db_mx%manureparm` and `manure_db` instead of the fertilizer database; 39fabde initialized the local counters to zero.

- df07e3f introduced `read_mgtops` with the operation loop, date conversion, and database crosswalks for plant, harvest, tillage, irrigation, fertilizer, pesticide, grazing, fire, and sweep operations.
- 94b6dec added the `external :: search, jdt` declaration and made the program unit end explicit with `end subroutine read_mgtops`.
- 88ac4f1 added manure-operation support by crosswalking manure names and application types into `op1` and `op4`.
- 561bc28 corrected the manure-operation lookup to use `manure_db` and `db_mx%manureparm` rather than the fertilizer database.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'read_mgtops' has no extracted documentation comment.
