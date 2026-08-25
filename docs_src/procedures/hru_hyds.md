---
kind: procedure
symbol: hru_hyds
title: hru_hyds
status: filled
source_hash: a856449f1649e136
version_label: SWAT+ 62.0.0
locals:
  j: Current HRU index used to read the active HRU state and pesticide balance arrays.
  cnv_m3: Area-based conversion factor from HRU runoff depth units to cubic meters for flow
    volumes.
  cnv_kg: Area-based conversion factor from per-area constituent loads to kilograms using
    HRU area.
  cnv_ppm: Temporary concentration conversion factor used to turn water-quality mass loads
    into concentration-like values for `cbod` and `dox`.
  iob: Local copy of the current command/object index (`icmd`) used when writing to `ob` and
    `obcs`.
  ihyd: Loop counter for summing hydrograph components into the total outflow hydrograph.
  ipest: Loop counter over pesticide constituent slots.
  ipath: Loop counter over pathogen constituent slots.
  isalt: Loop counter over salt ion constituent slots.
  ics: Loop counter over generic constituent slots.
  istep: Loop counter over subdaily hydrograph time steps and over component summations.
  istep_bak: Backward-looking subdaily index used while shifting the current-day hydrograph
    during Green-Ampt translation.
  day_cur: Current hydrograph day index copied from `ob(icmd)%day_cur`.
  day_next: Next hydrograph day index used to receive shifted flow steps, wrapping to day
    1 after `day_max`.
  tinc: Number of time steps to shift the hydrograph by, derived from travel time and the
    model time step.
  inext_step: Source subdaily step index in the current day hydrograph when copying flow into
    the next-day storage.
uses:
  hru_module: The HRU module supplies the active HRU record and the HRU-area scaling needed
    to convert per-area runoff and load values into object-level hydrograph volumes and masses.
  hydrograph_module: The hydrograph module defines the daily hydrograph containers and their
    fields, so this routine can zero, accumulate, and separate the water-quality and flow
    outputs written for the current command object.
  basin_module: The basin control code selects whether Green-Ampt routing is active, which
    changes how the subdaily hydrograph storage is shifted and filled.
  time_module: The current simulation time step and its minute length determine whether subdaily
    hydrograph shifting is needed and how many steps a runoff translation should span.
  constituent_mass_module: The constituent-mass database controls how many pesticide, pathogen,
    salt, and generic constituent slots are populated, and the constituent hydrograph arrays
    receive the loads built by this routine.
  output_landscape_module: The overlay packet shows this module as a dependency, but no specific
    imported state or type from it was resolved in the extracted references, so its role cannot
    be identified precisely from the provided evidence.
  output_ls_pesticide_module: The pesticide-balance module holds the HRU pesticide load components
    that are summed into surface runoff, percolation, lateral flow, and tile flow pesticide
    outputs.
  climate_module: The daily weather record provides average air temperature, which this routine
    uses to estimate surface runoff water temperature in the routed hydrograph.
---

<!-- facts:header -->

`hru_hyds` assembles daily and subdaily HRU runoff hydrographs for a command object. It packages water, sediment, nutrients, salts, pesticides, and other constituents into the hydrograph storage used for routing and output.

## Bottom Line

`hru_hyds` converts the current HRU’s daily water and constituent balances into the object hydrographs stored on `ob(icmd)` and `obcs(icmd)`. It separates runoff into surface, recharge, lateral, and tile components, computes the matching constituent loads, and then prepares the subdaily hydrograph arrays used for routing.

This routine matters because downstream routing and reporting read the daily hydrograph records and subdaily storage it fills, including `ob(icmd)%hd(1:5)`, `ob(icmd)%hdsep%flo_surq`, `ob(icmd)%hdsep%flo_satexsw`, `ob(icmd)%peakrate`, and `ob(icmd)%hyd_flo`. It is called from `hru_control` after HRU balances such as runoff, sediment, nutrients, salts, and pesticide losses have already been computed.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hru_control` finishes assembling the HRU water and constituent fluxes, then calls `hru_hyds` to package those values into the command object's hydrograph storage. The results feed later routing and reporting, including daily hydrograph totals, subdaily `hyd_flo` storage, and the output.landscape-style hydrograph records used by downstream model components.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the current HRU and compute area-based conversion factors. | The routine copies `ihru` into `j` and derives `cnv_m3` and `cnv_kg` from `hru(j)%area_ha` so runoff volumes and constituent masses can be written on an object basis. |
| 2. Clear the daily hydrograph storage for the active command object. | It sets `iob = icmd`, resets `ob(icmd)%hd(1:5)` to `hz`, and, when `cs_db%num_tot > 0`, resets `obcs(icmd)%hd(1:5)` to `hin_csz`. |
| 3. Fill the surface runoff hydrograph and its separation fields. | The routine writes surface runoff, saturation-excess runoff, peak rate, water temperature, sediment, nutrient, chlorophyll-a, oxygen demand, and oxygen into `ob(icmd)%hd(3)` and `ob(icmd)%hdsep` using daily HRU state and the conversion factors. |
| 4. Add surface constituent loads. | It loops over pesticides, pathogens, salts, and generic constituents to populate `obcs(icmd)%hd(3)` from the HRU balance arrays and the configured constituent counts in `cs_db`. |
| 5. Fill the recharge hydrograph and its constituent loads. | The routine writes recharge flow and nitrate to `ob(icmd)%hd(2)` and fills the recharge constituent slots from percolation and leaching balances. |
| 6. Fill the lateral soil-flow hydrograph and its constituent loads. | It writes lateral flow and nitrate to `ob(icmd)%hd(4)`, stores lateral flow separation in `ob(icmd)%hdsep%flo_latq`, and fills the lateral constituent slots. |
| 7. Fill the tile-flow hydrograph and its constituent loads. | It writes tile flow and nitrate to `ob(icmd)%hd(5)`, then fills tile pesticide, salt, and generic constituent loads. The water-temperature logic for this branch is left commented out. |
| 8. Build the total outflow hydrograph and constituent totals. | The routine sums hydrograph slots 3 through 5 into `ob(icmd)%hd(1)` and then sums the matching constituent loads into `obcs(icmd)%hd(1)`. |
| 9. Prepare the current and next subdaily day indices. | It copies `ob(icmd)%day_cur` into `day_cur`, computes `day_next`, and wraps `day_next` to 1 when it exceeds `ob(icmd)%day_max`. |
| 10. Route or translate subdaily flows when the model is running subdaily. | For `time%step > 1`, the routine either applies Green-Ampt translation by adding `hhsurfq` into the current-day hydrograph and shifting steps into the next day, or it calls `flow_hyd_ru_hru` to build the subdaily hydrograph from daily surface, lateral, and tile flows. |
| 11. Store the daily total when the run is daily only. | When `time%step <= 1`, it copies the total runoff flow into `ob(icmd)%hyd_flo(day_cur,1)` so later command-level summation can use it. |
| 12. Return to the caller. | The subroutine exits after populating the hydrograph arrays. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, surqsolp` | `hru(j)%area_ha` |
| [sym:hydrograph_module] | `ob` | `ob(icmd)%hd(1), ob(icmd)%hd(2), ob(icmd)%hd(3), ob(icmd)%hd(4), ob(icmd)%hd(5), ob(icmd)%hdsep%flo_surq, ob(icmd)%hdsep%flo_satexsw, ob(icmd)%peakrate, ob(icmd)%hd(3)%temp, ob(icmd)%hd(3)%flo, ob(icmd)%hd(3)%sed, ob(icmd)%hd(3)%orgn, ob(icmd)%hd(3)%sedp, ob(icmd)%hd(3)%no3, ob(icmd)%hd(3)%solp, ob(icmd)%hd(3)%chla, ob(icmd)%hd(3)%nh3, ob(icmd)%hd(3)%no2, ob(icmd)%hd(3)%cbod, ob(icmd)%hd(3)%dox, ob(icmd)%hd(3)%san, ob(icmd)%hd(3)%sil, ob(icmd)%hd(3)%cla, ob(icmd)%hd(3)%sag, ob(icmd)%hd(3)%lag, ob(icmd)%hd(2)%flo, ob(icmd)%hd(2)%no3, ob(icmd)%hd(4)%flo, ob(icmd)%hdsep%flo_latq, ob(icmd)%hd(4)%no3, ob(icmd)%hd(5)%flo, ob(icmd)%hd(5)%no3, ob(icmd)%hd(ihyd), ob(icmd)%day_cur, ob(icmd)%day_max, ob(icmd)%hyd_flo(day_cur,:), ob(icmd)%hyd_flo(day_next,:), ob(icmd)%hyd_flo(day_next,istep), ob(icmd)%hyd_flo(day_cur,inext_step)` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gampt` |
| [sym:time_module] | `time` | `time%step, time%dtm` |
| [sym:constituent_mass_module] | `cs_db, obcs` | `cs_db%num_tot, obcs(icmd)%hd(1), obcs(icmd)%hd(2), obcs(icmd)%hd(3), obcs(icmd)%hd(4), obcs(icmd)%hd(5), cs_db%num_pests, obcs(icmd)%hd(3)%pest(ipest), cs_db%num_paths, obcs(icmd)%hd(3)%path(ipath), cs_db%num_salts, obcs(icmd)%hd(3)%salt(isalt), cs_db%num_cs, obcs(icmd)%hd(3)%cs(ics), obcs(icmd)%hd(2)%pest(ipest), obcs(icmd)%hd(2)%path(ipath), obcs(icmd)%hd(2)%salt(isalt), obcs(icmd)%hd(2)%cs(ics), obcs(icmd)%hd(4)%pest(ipest), obcs(icmd)%hd(4)%path(ipath), obcs(icmd)%hd(4)%salt(isalt), obcs(icmd)%hd(4)%cs(ics), obcs(icmd)%hd(5)%pest(ipest), obcs(icmd)%hd(5)%path(ipath), obcs(icmd)%hd(5)%salt(isalt), obcs(icmd)%hd(5)%cs(ics), obcs(icmd)%hd(1)%pest(ipest), obcs(icmd)%hd(1)%path(ipath), obcs(icmd)%hd(1)%salt(isalt), obcs(icmd)%hd(1)%cs(ics)` |
| [sym:output_landscape_module] | `hpestb_d` |  |
| [sym:output_ls_pesticide_module] | `hpestb_d` | `hpestb_d(j)%pest(ipest)%surq, hpestb_d(j)%pest(ipest)%sed, hpestb_d(j)%pest(ipest)%perc, hpestb_d(j)%pest(ipest)%latq, hpestb_d(j)%pest(ipest)%tileq` |
| [sym:climate_module] | `w` | `w%tave` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ob(icmd)%hd(1)` | Always, after surface and other hydrograph components are computed. | `ob(icmd)%hd(1)` is cleared and then rebuilt as the sum of the surface, recharge, and lateral/tile hydrograph records. It represents the total object outflow hydrograph used for later routing and subdaily storage initialization. |
| `ob(icmd)%hd(2)` | Always, during the recharge hydrograph step. | `ob(icmd)%hd(2)` is set from recharge/percolation terms: flow from `sepbtm(j)` and nitrate from `percn(j)`. This record carries the recharge component of the object hydrograph for later routing. |
| `ob(icmd)%hd(3)` | Always, during the surface runoff hydrograph step. | `ob(icmd)%hd(3)` is populated with surface runoff flow and associated sediment, nutrients, chlorophyll-a, oxygen demand, oxygen, detached sediment fractions, and water temperature. It is the main surface outflow record used by routing and water-quality calculations. |
| `ob(icmd)%hd(4)` | Always, during the lateral soil-flow step. | `ob(icmd)%hd(4)` is set from lateral flow and nitrate so the model can route the lateral component separately from the surface and tile components. |
| `ob(icmd)%hd(5)` | Always, during the tile-flow step. | `ob(icmd)%hd(5)` is set from tile drainage flow and nitrate so tile outflow can be routed and combined into the total object hydrograph. |
| `obcs(icmd)%hd(1)` | Always, after `ob(icmd)%hd(1)` is formed. | `obcs(icmd)%hd(1)` is filled as the total constituent load across surface runoff, lateral flow, and tile flow. It is the total constituent hydrograph counterpart to `ob(icmd)%hd(1)`. |
| `obcs(icmd)%hd(2)` | Always, during the recharge constituent step. | `obcs(icmd)%hd(2)` records recharge-associated constituent loads, including pesticide leaching, salts, and other constituents. |
| `obcs(icmd)%hd(3)` | Always, during the surface constituent step. | `obcs(icmd)%hd(3)` records surface constituent loads from runoff, sediment attachment, and surface/sediment-associated transport. |
| `obcs(icmd)%hd(4)` | Always, during the lateral constituent step. | `obcs(icmd)%hd(4)` records constituent loads transported by lateral soil flow. |
| `obcs(icmd)%hd(5)` | Always, during the tile constituent step. | `obcs(icmd)%hd(5)` records constituent loads transported by tile drainage flow. |
| `ob(icmd)%hdsep%flo_surq` | Always, when surface runoff is computed. | `ob(icmd)%hdsep%flo_surq` stores the surface-runoff portion of the hydrograph separation, converted to object flow units. |
| `ob(icmd)%hdsep%flo_satexsw` | Always, when saturation-excess runoff is computed. | `ob(icmd)%hdsep%flo_satexsw` stores the saturation-excess runoff component, converted to object flow units. |
| `ob(icmd)%peakrate` | Always, when surface runoff is computed. | `ob(icmd)%peakrate` stores the peak flow rate for the current time step so routing and reporting can use the event maximum. |
| `ob(icmd)%hd(3)%temp` | Always, when surface runoff is computed. | `ob(icmd)%hd(3)%temp` is set from `w%tave` to give the surface hydrograph a water temperature estimate. |
| `ob(icmd)%hd(3)%flo` | Always, when surface runoff is computed. | `ob(icmd)%hd(3)%flo` stores the surface runoff volume for the current HRU/object after unit conversion. |
| `ob(icmd)%hd(3)%sed` | Always, when surface runoff is computed. | `ob(icmd)%hd(3)%sed` stores the sediment load associated with surface runoff. |
| `ob(icmd)%hd(3)%orgn` | Always, when surface runoff is computed. | `ob(icmd)%hd(3)%orgn` stores organic nitrogen associated with sediment yield. |
| `ob(icmd)%hd(3)%sedp` | Always, when surface runoff is computed. | `ob(icmd)%hd(3)%sedp` stores sediment-associated phosphorus from organic and mineral sediment P terms. |
| `ob(icmd)%hd(3)%no3` | Always, when surface runoff is computed. | `ob(icmd)%hd(3)%no3` stores nitrate associated with surface runoff and other surface pathways. |
| `ob(icmd)%hd(3)%solp` | Always, when surface runoff is computed. | `ob(icmd)%hd(3)%solp` stores soluble phosphorus from surface runoff and tile-labile P terms. |
| `ob(icmd)%hd(3)%chla` | Always, when surface runoff is computed. | `ob(icmd)%hd(3)%chla` stores chlorophyll-a load for the surface hydrograph. |
| `ob(icmd)%hd(3)%nh3` | Always, when surface runoff is computed. | `ob(icmd)%hd(3)%nh3` is explicitly set to zero for the surface hydrograph in this routine. |
| `ob(icmd)%hd(3)%no2` | Always, when surface runoff is computed. | `ob(icmd)%hd(3)%no2` is explicitly set to zero for the surface hydrograph in this routine. |
| `ob(icmd)%hd(3)%cbod` | Always, when surface runoff is computed and `ob(icmd)%hd(3)%flo > 0.01` determines a concentration conversion is available. | `ob(icmd)%hd(3)%cbod` stores carbonaceous biological oxygen demand as a concentration-scaled load for the surface hydrograph. |

## File I/O

<!-- facts:io -->


## Lineage

`hru_hyds.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 8 non-merge commit(s) since, most recently `b9df6cf` (2026-04-01, "gwflow re-merge: host file guards, ch_temp component mixing restoration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hru_hyds.f90` are listed.

- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `78b295f` (2026-02-05) — Updated hydrological calculations to include time step adjustments for flow conversions in hru_hyds and ru_control subroutines.
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `54a9d44` (2024-08-12) — NP_flow.f90 - Subroutine NP_FLOW REMOVED
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'hru_hyds' has no extracted documentation comment.
- summary_variables completed locally from hru_hyds.f90 (lines 48-189); each ob/obcs hydrograph and hd(3) loading component is cited to its source assignment line.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
