---
kind: procedure
symbol: hcsout_output
title: hcsout_output
status: filled
source_hash: 1de549725df0e32a
version_label: SWAT+ 62.0.0
locals:
  iiout: Loop index over each outgoing source connection for the current spatial object; it
    selects which `ob(iob)` outlet/hydrograph branch is being reported and accumulated.
  ipest: Loop index over pesticide constituents when writing or copying pesticide mass arrays.
  ipath: Loop index over pathogen constituent entries when writing or copying pathogen mass
    arrays.
  imetal: Loop index over heavy-metal constituent entries when writing or copying metal mass
    arrays.
  isalt: Loop index over salt constituent entries when writing or copying salt mass arrays.
  iob: Loop index over spatial objects in `sp_ob%objs`; it selects the object whose outgoing
    hydrograph constituents are being reported.
uses:
  hydrograph_module: '`hydrograph_module` provides the object inventory and routing metadata
    that determine how many objects and source links exist, which object identifiers to print,
    and which outgoing hydrograph branch fields (`obtyp_out`, `obtypno_out`, `htyp_out`, `frac_out`,
    `hin_a`) are associated with each report row.'
  time_module: '`time_module` supplies the current simulation clock and period flags that
    gate when each block of output runs, so the routine can distinguish daily, monthly, yearly,
    and end-of-simulation reporting and stamp each record with the current date fields.'
  constituent_mass_module: '`constituent_mass_module` defines the constituent counts and storage
    arrays that control whether each mass class is written and which values are accumulated
    or averaged; without `cs_db`, `hcs1`, and `obcs`, the routine would have no constituent
    dimensions or destination storage for the output records.'
---

<!-- facts:header -->

Writes hydrologic constituent output for every object/source connection at daily, monthly, yearly, and average-annual intervals. It reports pesticide, pathogen, metal, and salt masses to fixed unit files and CSV companions when enabled.

## Bottom Line

`hcsout_output` is a reporting subroutine with no arguments. It walks every spatial object and each outgoing source connection, then writes the current hydrograph constituent masses for the active time period: daily, monthly, yearly, and average-annual.

The routine does not compute new hydrology; it copies and accumulates existing constituent hydrograph state into `obcs(iob)%hcsout_m`, `hcsout_y`, and `hcsout_a`, divides the average-annual hydrograph by `time%yrs_prt` at simulation end, and emits the values to a set of fixed output units for pests, pathogens, metals, and salts.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hcsout_output` runs as part of the simulation output phase after object connectivity and constituent hydrograph storage have been prepared elsewhere. It depends on routing/setup state in `hydrograph_module`, current calendar flags in `time_module`, and constituent counts plus zero-to-accumulate hydrograph arrays in `constituent_mass_module`; later reporting files and any downstream postprocessing depend on the records it writes.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over spatial objects and outgoing source links. | The routine iterates over every spatial object (`iob = 1, sp_ob%objs`) and each of that object's source outputs (`iiout = 1, ob(iob)%src_tot`) so that each outgoing hydrograph branch can be reported separately. |
| 2. Emit daily constituent outputs when daily printing is enabled. | If `pco%day_print` matches the current interval and hydrologic daily output is enabled (`pco%hyd%d == 'y'`), the routine writes daily pesticide, pathogen, metal, and salt records. Each block checks the relevant constituent count in `cs_db` before writing the corresponding `hcs1` values and optional CSV output. |
| 3. Accumulate daily constituent masses into the monthly storage. | After daily reporting, the routine adds the current `hcs1` mass state into `obcs(iob)%hcsout_m(iiout)`, building the monthly running total for each output branch. |
| 4. Emit monthly outputs at end-of-month and accumulate into annual storage. | When `time%end_mo == 1` and monthly hydrologic output is enabled (`pco%hyd%m == 'y'`), the routine writes monthly pesticide, pathogen, metal, and salt records from `obcs(iob)%hcsout_m(iiout)`, again with optional CSV writes. This block reports the month-total masses for the branch. |
| 5. Roll monthly totals into yearly storage. | The monthly total for the branch is added to `obcs(iob)%hcsout_y(iiout)` so yearly reporting can use the accumulated monthly values. |
| 6. Emit yearly outputs at end-of-year. | When `time%end_yr == 1` and yearly hydrologic output is enabled (`pco%hyd%y == 'y'`), the routine writes yearly pesticide, pathogen, metal, and salt records from `obcs(iob)%hcsout_y(iiout)` with optional CSV copies. |
| 7. Roll yearly totals into average-annual storage. | The yearly total for the branch is added to `obcs(iob)%hcsout_a(iiout)` so average-annual output can be formed at simulation end. |
| 8. Finalize and emit average-annual outputs at simulation end. | When `time%end_sim == 1` and average-annual hydrologic output is enabled (`pco%hyd%a == 'y'`), the routine scales `ob(iob)%hin_a(iiout)` by `time%yrs_prt` and writes average-annual pesticide, pathogen, metal, and salt records from `obcs(iob)%hcsout_a(iiout)` with optional CSV copies. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, ob` | `sp_ob%objs, ob(iob)%src_tot, ob(iob)%typ, ob(iob)%num, ob(iob)%obtyp_out(iiout), ob(iob)%obtypno_out(iiout), ob(iob)%htyp_out(iiout), ob(iob)%frac_out(iiout), ob(iob)%hin_a(iiout)` |
| [sym:time_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc, time%end_mo, time%end_yr, time%end_sim, time%yrs_prt` |
| [sym:constituent_mass_module] | `cs_db, hcs1, obcs` | `cs_db%num_pests, hcs1%pest(ipest), cs_db%num_paths, hcs1%path(ipath), cs_db%num_metals, hcs1%hmet(imetal), cs_db%num_salts, hcs1%salt(isalt), obcs(iob)%hcsout_m(iiout), obcs(iob)%hcsout_m(iiout)%pest(ipest), obcs(iob)%hcsout_m(iiout)%path(ipath), obcs(iob)%hcsout_m(iiout)%hmet(imetal), obcs(iob)%hcsout_m(iiout)%salt(isalt), obcs(iob)%hcsout_y(iiout), obcs(iob)%hcsout_y(iiout)%pest(ipest), obcs(iob)%hcsout_y(iiout)%path(ipath), obcs(iob)%hcsout_y(iiout)%hmet(imetal), obcs(iob)%hcsout_y(iiout)%salt(isalt), obcs(iob)%hcsout_a(iiout), obcs(iob)%hcsout_a(iiout)%pest(ipest), obcs(iob)%hcsout_a(iiout)%path(ipath), obcs(iob)%hcsout_a(iiout)%hmet(imetal), obcs(iob)%hcsout_a(iiout)%salt(isalt)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `obcs(iob)%hcsout_m(iiout)` | During the daily-output block when `pco%day_print == 'y'`, `pco%int_day_cur == pco%int_day`, and `pco%hyd%d == 'y'` after any daily writes | It is incremented by the current constituent hydrograph `hcs1`, so it becomes the running monthly total for that object/source branch. |
| `obcs(iob)%hcsout_y(iiout)` | At the monthly accumulation point after the daily block, every loop pass | It is incremented by `obcs(iob)%hcsout_m(iiout)`, turning the monthly total into a running yearly total for that branch. |
| `obcs(iob)%hcsout_a(iiout)` | At the yearly accumulation point after the monthly block, every loop pass | It is incremented by `obcs(iob)%hcsout_y(iiout)`, so it stores the running total needed for average-annual reporting. |
| `ob(iob)%hin_a(iiout)` | When `time%end_sim == 1` and `pco%hyd%a == 'y'` | It is divided by `time%yrs_prt` to convert the accumulated average-annual hydrograph input to a per-year mean before final output. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved four commits affecting `hcsout_output`. The file was introduced in `df07e3f` with the full daily/monthly/yearly/average-annual write structure and running-total updates. `39fabde` initialized the loop counters (`iiout`, `ipest`, `ipath`, `imetal`, `isalt`, `iob`) to zero. `f1e61a3` kept the same logic but removed tab indentation and aligned continuation lines. `2fe89fd` changed the CSV-formatted writes from `G0.3` to `G0.6` precision on all CSV companion units in this routine.

- Introduced the entire `hcsout_output` reporting routine with its nested loops, conditional period checks, accumulation into `obcs(...).hcsout_m/y/a`, and all unit writes.
- Initialized the local loop counters to zero before entering the object/source loops.
- Adjusted only formatting/indentation, with no behavioral change to the output logic.
- Increased CSV numeric precision from `G0.3` to `G0.6` for all CSV companion writes in this routine.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hcsout_output' has no extracted documentation comment.
