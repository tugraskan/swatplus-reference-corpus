---
kind: procedure
symbol: basin_sw_init
title: basin_sw_init
status: filled
source_hash: 94b83354f7c55ecd
version_label: SWAT+ 62.0.0
locals:
  ihru: Loop counter used to walk through HRU and HRU_LTE object indexes while copying and
    summing initial water states.
  iihru: Temporary landscape-element index fetched from `lsu_elem(ihru)%obtypno` so the routine
    can look up the basin-fraction and object type for the current mapped element.
  ilsu: Loop counter over landscape-unit output regions in `lsu_out` when building RU-level
    initial water-balance totals.
  ielem: Loop counter over the members of each landscape-unit output group, used to retrieve
    each HRU index from `lsu_out(ilsu)%num`.
  const: Temporary weighting factor set to the basin fraction or RU fraction for the current
    element and used to scale each contribution into the aggregated totals.
uses:
  time_module: The routine is invoked from the simulation time-control path, and `time%yrs`
    is checked there to decide whether initialization should occur during the current run
    before daily stepping begins.
  hydrograph_module: '`sp_ob` supplies the object counts that bound the HRU and HRU_LTE initialization
    loops, so the routine knows how many elements to seed before aggregation.'
  calibration_data_module: These arrays provide the mapping and weighting metadata that tell
    the routine which HRU or HRU_LTE contributes to basin and RU totals, how much it contributes,
    and whether the mapped object is an HRU or an HRU_LTE.
  output_landscape_module: These water-balance records are the destination for the initial
    soil-water and snow-water values that the rest of the output system will compare against
    during daily, monthly, yearly, and annual reporting.
  basin_module: '`basin_module` is imported by the routine, so basin-level shared state may
    be available or expected during initialization even though no specific symbol was extracted
    in the context packet.'
  maximum_data_module: '`db_mx%lsu_out` gives the upper bound for the RU aggregation loop,
    allowing the routine to walk every configured landscape output region.'
  soil_module: The current soil-profile water content is copied from `soil(ihru)%sw` into
    the HRU water-balance outputs, making soil state the source of the initial basin water
    balance.
  hru_module: The current snowpack water equivalent in each HRU is copied from `hru(ihru)%sno_mm`
    so the initial snow balance can be recorded alongside soil water.
---

<!-- facts:header -->

Initializes basin-, RU-, and HRU-level starting soil-water and snow-water balance values for output checking. It copies current soil and snow states into daily, monthly, yearly, and annual water-balance structures before simulation time stepping begins.

## Bottom Line

`basin_sw_init` seeds the model’s water-balance output structures with the starting soil water and snow water for each HRU and HRU_LTE object. It then aggregates those initialized values to basin and landscape-unit totals so later water-balance reporting can compare model changes against a known starting state.

The routine does not advance hydrology itself; it prepares summary state used by output and checking logic. In particular, it fills daily, monthly, yearly, and annual initial values in `hwb_*`, `bwb_*`, `hltwb_*`, and `ruwb_*` so the first time-step outputs have a consistent baseline.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during time-control setup, after the model has built its spatial object maps and before the first daily loop begins. `time_control` calls it when the water-balance initialization flag has not yet been set, so the current soil and snow states are captured once and then used by later water-balance output and checking logic throughout the simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop over HRUs | For each HRU index from 1 to `sp_ob%hru`, copy the current soil water from `soil(ihru)%sw` into the daily, monthly, yearly, and annual HRU water-balance records, and copy snow water from `hru(ihru)%sno_mm` into the matching `sno_init` fields. |
| 2. zero basin totals | Reset the basin daily initial soil-water and snow-water totals to zero before any weighted accumulation begins. |
| 3. scan HRUs for basin sum | Walk the HRU list again, map each HRU to its landscape-element record through `lsu_elem(ihru)%obtypno`, and only continue when the basin fraction is significant. |
| 4. weight basin HRU values | When the mapped element is an HRU, use `lsu_elem(iihru)%bsn_frac` as the weight and add the HRU's initialized soil-water and snow-water values into the basin daily totals. |
| 5. copy basin totals to longer periods | After the basin daily totals are complete, copy them directly into the monthly, yearly, and annual basin water-balance records so all periods start from the same baseline. |
| 6. scan HRU_LTE objects | Loop through HRU_LTE objects and use the same basin-fraction test to find routed or unrouted landscape elements that should contribute to basin initialization. |
| 7. add unrouted HRU_LTE basin values | For mapped elements whose type is `hlt`, add the initialized HRU_LTE soil-water and snow-water values from `hltwb_d(iihru)` into the basin daily totals using the basin fraction weight. |
| 8. loop over landscape-unit outputs | For each landscape output region up to `db_mx%lsu_out`, visit all member HRU indices listed in `lsu_out(ilsu)%num` and use their RU fractions as weights. |
| 9. sum RU contributions | For each member HRU, add the initialized HRU or HRU_LTE water-balance values into `ruwb_d(ilsu)` when the object type matches, using `lsu_elem(ihru)%ru_frac` as the scaling factor. |
| 10. duplicate RU daily totals to other periods | After the RU daily totals are built, copy them unchanged into the monthly, yearly, and annual RU water-balance records for both soil water and snow water. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%yrs, time%day_start, time%day_end_yr` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru, sp_ob%hru_lte` |
| [sym:calibration_data_module] | `lsu_elem, lsu_out` | `lsu_elem(ihru)%obtypno, lsu_elem(iihru)%bsn_frac, lsu_elem(iihru)%obtyp, lsu_out(ilsu)%num_tot, lsu_out(ilsu)%num(ielem), lsu_elem(ihru)%ru_frac, lsu_elem(ihru)%obtyp` |
| [sym:output_landscape_module] | `hwb_d, hwb_m, hwb_y, hwb_a, bwb_d, bwb_m, bwb_y, bwb_a, hltwb_d, ruwb_d, ruwb_m, ruwb_y, ruwb_a` | `hwb_d(ihru)%sw_init, hwb_m(ihru)%sw_init, hwb_y(ihru)%sw_init, hwb_a(ihru)%sw_init, hwb_d(ihru)%sno_init, hwb_m(ihru)%sno_init, hwb_y(ihru)%sno_init, hwb_a(ihru)%sno_init, bwb_d%sw_init, bwb_d%sno_init, hwb_d(iihru)%sw_init, hwb_d(iihru)%sno_init, bwb_m%sw_init, bwb_m%sno_init, bwb_y%sw_init, bwb_y%sno_init, bwb_a%sw_init, bwb_a%sno_init, hltwb_d(iihru)%sw_init, hltwb_d(iihru)%sno_init, ruwb_d(ilsu)%sw_init, ruwb_d(ilsu)%sno_init, hltwb_d(ihru)%sw_init, hltwb_d(ihru)%sno_init, ruwb_m(ilsu)%sw_init, ruwb_m(ilsu)%sno_init, ruwb_y(ilsu)%sw_init, ruwb_y(ilsu)%sno_init, ruwb_a(ilsu)%sw_init, ruwb_a(ilsu)%sno_init` |
| [sym:basin_module] | `basin` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_out` |
| [sym:soil_module] | `soil` | `soil(ihru)%sw` |
| [sym:hru_module] | `hru` | `hru(ihru)%sno_mm` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hwb_d(ihru)%sw_init` | During the first HRU loop for every `ihru` from 1 to `sp_ob%hru`. | Stores the current soil-water content of each HRU in the daily HRU output so later water-balance checks can compare simulated changes against the starting profile water. |
| `hwb_m(ihru)%sw_init` | During the first HRU loop for every `ihru` from 1 to `sp_ob%hru`. | Stores the current soil-water content of each HRU in the monthly HRU output at the start of the run. |
| `hwb_y(ihru)%sw_init` | During the first HRU loop for every `ihru` from 1 to `sp_ob%hru`. | Stores the current soil-water content of each HRU in the yearly HRU output at the start of the run. |
| `hwb_a(ihru)%sw_init` | During the first HRU loop for every `ihru` from 1 to `sp_ob%hru`. | Stores the current soil-water content of each HRU in the annual HRU output at the start of the run. |
| `hwb_d(ihru)%sno_init` | During the first HRU loop for every `ihru` from 1 to `sp_ob%hru`. | Stores the current snowpack water equivalent of each HRU in the daily HRU output. |
| `hwb_m(ihru)%sno_init` | During the first HRU loop for every `ihru` from 1 to `sp_ob%hru`. | Stores the current snowpack water equivalent of each HRU in the monthly HRU output. |
| `hwb_y(ihru)%sno_init` | During the first HRU loop for every `ihru` from 1 to `sp_ob%hru`. | Stores the current snowpack water equivalent of each HRU in the yearly HRU output. |
| `hwb_a(ihru)%sno_init` | During the first HRU loop for every `ihru` from 1 to `sp_ob%hru`. | Stores the current snowpack water equivalent of each HRU in the annual HRU output. |
| `bwb_d%sw_init` | After basin totals are cleared and the HRU scan begins. | Starts the basin daily initial soil-water total at zero so weighted HRU contributions can be accumulated from scratch. |
| `bwb_d%sno_init` | After basin totals are cleared and the HRU scan begins. | Starts the basin daily initial snow-water total at zero so weighted HRU contributions can be accumulated from scratch. |
| `bwb_m%sw_init` | After the basin HRU accumulation is complete. | Copies the basin daily initial soil-water total into the monthly basin record so all time scales start from the same baseline. |
| `bwb_m%sno_init` | After the basin HRU accumulation is complete. | Copies the basin daily initial snow-water total into the monthly basin record so all time scales start from the same baseline. |
| `bwb_y%sw_init` | After the basin HRU accumulation is complete. | Copies the basin daily initial soil-water total into the yearly basin record so all time scales start from the same baseline. |
| `bwb_y%sno_init` | After the basin HRU accumulation is complete. | Copies the basin daily initial snow-water total into the yearly basin record so all time scales start from the same baseline. |
| `bwb_a%sw_init` | After the basin HRU accumulation is complete. | Copies the basin daily initial soil-water total into the annual basin record so all time scales start from the same baseline. |
| `bwb_a%sno_init` | After the basin HRU accumulation is complete. | Copies the basin daily initial snow-water total into the annual basin record so all time scales start from the same baseline. |
| `ruwb_d(ilsu)%sw_init` | For each HRU_LTE candidate with `lsu_elem(iihru)%bsn_frac > 1.e-12` and `lsu_elem(iihru)%obtyp == "hlt"`. | Adds the initialized HRU_LTE soil-water contribution into the basin daily total using the basin fraction as the weight. |
| `ruwb_d(ilsu)%sno_init` | For each HRU_LTE candidate with `lsu_elem(iihru)%bsn_frac > 1.e-12` and `lsu_elem(iihru)%obtyp == "hlt"`. | Adds the initialized HRU_LTE snow-water contribution into the basin daily total using the basin fraction as the weight. |
| `ruwb_m(ilsu)%sw_init` | For each landscape unit `ilsu` and each member `ielem` with `lsu_elem(ihru)%ru_frac > 1.e-9` and `lsu_elem(ihru)%obtyp == "hru"`. | Adds the member HRU soil-water initialization into the RU daily total using the RU fraction weight. |
| `ruwb_m(ilsu)%sno_init` | For each landscape unit `ilsu` and each member `ielem` with `lsu_elem(ihru)%ru_frac > 1.e-9` and `lsu_elem(ihru)%obtyp == "hru"`. | Adds the member HRU snow-water initialization into the RU daily total using the RU fraction weight. |
| `ruwb_y(ilsu)%sw_init` | For each landscape unit `ilsu` and each member `ielem` with `lsu_elem(ihru)%ru_frac > 1.e-9` and `lsu_elem(ihru)%obtyp == "hlt"`. | Adds the member HRU_LTE soil-water initialization into the RU daily total using the RU fraction weight. |
| `ruwb_y(ilsu)%sno_init` | For each landscape unit `ilsu` and each member `ielem` with `lsu_elem(ihru)%ru_frac > 1.e-9` and `lsu_elem(ihru)%obtyp == "hlt"`. | Adds the member HRU_LTE snow-water initialization into the RU daily total using the RU fraction weight. |
| `ruwb_a(ilsu)%sw_init` | After the RU daily total is built for each `ilsu`. | Copies the RU daily soil-water total into the monthly RU output record so the region starts with the same initial value. |
| `ruwb_a(ilsu)%sno_init` | After the RU daily total is built for each `ilsu`. | Copies the RU daily snow-water total into the monthly RU output record so the region starts with the same initial value. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed `basin_sw_init`. The file was introduced in `df07e3f`, and `39fabde` only initialized the local counters/constant at declaration time; the later diff did not change the routine's water-balance logic.

- `df07e3f` added the full `basin_sw_init` implementation: HRU snow/soil initialization, basin aggregation, HRU_LTE basin addition, and RU aggregation/copy-out logic.
- `39fabde` changed only the local declarations so `ihru`, `iihru`, `ilsu`, `ielem`, and `const` start at zero; the accumulation algorithm remained the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'basin_sw_init' has no extracted documentation comment.
