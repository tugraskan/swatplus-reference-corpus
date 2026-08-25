---
kind: procedure
symbol: unit_hyd_ru_hru
title: unit_hyd_ru_hru
status: filled
source_hash: ae735a5aa04a9f4d
version_label: SWAT+ 62.0.0
locals:
  iihru: Loop counter for HRUs; it selects each HRU source hydrograph to pass through `unit_hyd`.
  iiru: Loop counter for routing units; it selects each RU source hydrograph to pass through
    `unit_hyd`.
  iob: Object index into `ob`; it identifies the receiving object whose connectivity and hydrograph
    storage are being updated.
  ihyd: Index over the incoming hydrographs on a given object; it selects which receiving
    connection is being examined.
  tc: Temporary time-of-concentration value. It is loaded from either `tconc` or `ru_tc`,
    then reduced by the square root of the incoming area fraction before calling `unit_hyd`
    for a partial inflow.
uses:
  hru_module: The HRU module supplies `tconc`, the time of concentration for each HRU. This
    routine uses those values as the input basis for building HRU unit hydrographs.
  ru_module: The RU module supplies `ru_tc`, the time of concentration for each routing unit.
    This routine uses those values to build unit hydrographs for RU inflows in the same way
    it does for HRUs.
  hydrograph_module: The hydrograph module provides the global object counts and connectivity
    tables that determine which HRUs, RUs, and receiving objects exist, how many incoming
    hydrographs each object has, whether an incoming connection is partial, and where the
    computed unit hydrograph should be stored.
  time_module: The time module provides `time%step`, which gates whether subdaily hydrograph
    construction should occur. If the model is not running with more than one step per day,
    this routine skips the subdaily hydrograph setup.
---

<!-- facts:header -->

Builds unit hydrographs for HRUs, routing units, and fractional inflow connections. It scales the hydrograph shape by the contributing area fraction before storing it on the receiving object.

## Bottom Line

This subroutine populates subdaily unit hydrographs used by the routing network. For every HRU and routing unit, it calls `unit_hyd` to build the base unit hydrograph, then stores additional unit hydrographs for any receiving object that gets only a fraction of an HRU or RU.

The fraction-based branch matters because an incoming connection that represents only part of an HRU or RU must have its time of concentration adjusted before the hydrograph is generated. The resulting hydrograph is stored in `ob(iob)%hin_uh(ihyd)%uh` for later routing behavior.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during subdaily routing setup, after `time%step` and the object connectivity tables have been initialized. The upstream object layout in `sp_ob`, `sp_ob1`, and `ob` prepares the HRU/RU and receiving-object indices, and later routing behavior depends on the unit hydrographs stored in `ob(iob)%uh` and `ob(iob)%hin_uh(ihyd)%uh`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check subdaily mode | Skip all work unless the simulation is using more than one routing time step per day, because only then does the model need subdaily unit hydrographs. |
| 2. build HRU hydrographs | Loop over every HRU, map it to the corresponding object index, and call `unit_hyd` with that HRU's `tconc` so the object's base unit hydrograph is generated. |
| 3. build RU hydrographs | Loop over every routing unit, map it to the corresponding object index, and call `unit_hyd` with that RU's `ru_tc` so the object's base unit hydrograph is generated. |
| 4. scan receiving objects | Visit each object in the network and then each of its incoming hydrograph connections so partial inflows can be identified and handled. |
| 5. select partial inflows | Only process connections whose incoming fraction is less than 1.0, because full incoming hydrographs already have their standard unit hydrograph values. |
| 6. load HRU time constant | If the incoming object type is an HRU, look up its HRU number, fetch `tconc` for that HRU, and store it in `tc`. |
| 7. load RU time constant | If the incoming object type is an RU, look up its RU number, fetch `ru_tc` for that RU, and store it in `tc`. |
| 8. scale for area fraction | Reduce the time of concentration by multiplying it by the square root of the incoming area fraction, using the assumption noted in the comment that time of concentration scales with square root of drainage area. |
| 9. build inflow hydrograph | Call `unit_hyd` with the adjusted `tc` and store the result in the receiving object's `hin_uh(ihyd)%uh` array for that incoming hydrograph. |
| 10. finish loops | Close out the partial-inflow, object, and mode loops once all eligible incoming hydrographs have been generated. |
| 11. exit routine | Return to the caller after all applicable hydrographs have been populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `tconc` |  |
| [sym:ru_module] | `ru_tc` |  |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%hru, sp_ob1%hru, sp_ob%ru, sp_ob1%ru, sp_ob%objs, ob(iob)%rcv_tot, ob(iob)%frac_in(ihyd), ob(iob)%obtyp_in(ihyd), ob(iob)%obtypno_in(ihyd), ob(iob)%hin_uh(ihyd)%uh` |
| [sym:time_module] | `time` | `time%step` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

`unit_hyd_ru_hru.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `unit_hyd_ru_hru.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'unit_hyd_ru_hru' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
