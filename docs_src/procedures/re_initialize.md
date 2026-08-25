---
kind: procedure
symbol: re_initialize
title: re_initialize
status: filled
source_hash: f56bd2962adc587f
version_label: SWAT+ 62.0.0
uses:
  hru_module: This module holds the HRU objects that represent the basin units being reset,
    along with hru_init as the saved baseline copy and bss as basin-scale storage that must
    be cleared before the next rerun.
  soil_module: This module provides soil profile state and its initialization copy; re_initialize
    restores the live soil profiles so soil-layer conditions match the baseline calibration
    start state.
  plant_module: This module contains plant community state and the saved pcom_init copy; re_initialize
    restores plant parameters and community structure before plant-related calibration loops
    continue.
  organic_mineral_mass_module: This module owns the organic/mineral mass versions of soil
    and plant state, including the live and saved copies that must be restored so residue,
    soil mass, and plant biomass pools are consistent for the next run.
  mgt_operations_module: This management-operations module contributes the control flag that
    tells the model whether basin soil water should be initialized; re_initialize sets it
    to disable that initialization for the rerun path.
  hydrograph_module: This module provides the spatial object counters that gate each reset
    block, plus the hydrologic storage structures for wetlands, channel storage, floodplain
    storage, reservoirs, and aquifers. re_initialize only copies these structures when the
    corresponding object type exists in the current setup.
  hru_lte_module: This module holds the HRU-LTE dynamic state and its initialization copy;
    re_initialize restores those parameters when HRU-LTE objects are present so specialized
    HRU simulations start from baseline values.
  sd_channel_module: This module holds SWAT-DEG channel dynamic state and its saved initialization
    copy; re_initialize restores channel-deg storage and dimensions before another sediment/hydrology
    trial.
  aquifer_module: This module owns aquifer initialization state that must be preserved and
    reused so groundwater-related storage is reset consistently across reruns.
---

<!-- facts:header -->

Resets shared SWAT+ object state back to its saved initialization copies before another calibration or rerun cycle. It clears or restores HRU, channel, reservoir, aquifer, and related management state only when those object types exist.

## Bottom Line

re_initialize is a central reset routine used before rerunning a calibration or soft-adjustment pass. It turns off basin soil-water initialization and restores model objects from their *_init snapshots so the next simulation starts from the same baseline state.

It conditionally resets HRU, HRU-LTE, SWAT-DEG channel, reservoir, and aquifer storage structures based on the object counts in sp_ob. It also clears basin-baseflow storage bss to zero, so later runs do not carry over residual state from the previous trial.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs at the start of a calibration rerun or other repeat simulation step, after the calling calibration routine has finished adjusting parameters for the current trial. The caller prepares the new parameter values and then invokes re_initialize so the next time_control-driven run begins from a clean baseline, with later hydrology, plant, sediment, and storage calculations depending on the restored state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. disable basin soil-water reinitialization | Sets pco%sw_init to "n", turning off the basin soil-water initialization flag so the next rerun does not reapply the default soil-water startup sequence. |
| 2. reset HRU-linked state when HRUs exist | If the model contains any HRUs, copies the live HRU, soil, soil1, plant community, plant mass, and wetland objects from their saved *_init versions and clears basin baseflow storage bss to zero. |
| 3. reset HRU-LTE dynamic state when present | If HRU-LTE objects exist, restores hlt from hlt_init so HRU-LTE-specific dynamics start the next run from their saved baseline values. |
| 4. reset SWAT-DEG channel storages when present | If SWAT-DEG channels exist, restores sd_ch from sdch_init and resets channel and floodplain storage states from the saved hydrologic initialization copies. |
| 5. reset reservoir storage when present | If reservoirs exist, restores reservoir hydrologic storage from res_om_init so reservoir state matches the saved initial condition for the next run. |
| 6. leave aquifer initialization state unchanged | If aquifers exist, the routine executes a self-assignment of aqu_om_init, which leaves the saved aquifer initialization state unchanged; this branch does not change model state in the extracted source. |
| 7. return to caller | Returns immediately after the conditional reset blocks, handing control back to the calibration or rerun routine that requested the state reset. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, hru_init, bss` |  |
| [sym:soil_module] | `soil, soil_init` |  |
| [sym:plant_module] | `pcom, pcom_init` |  |
| [sym:organic_mineral_mass_module] | `soil1, soil1_init, pl_mass, pl_mass_init` |  |
| [sym:mgt_operations_module] | `pco%sw_init` | `pco%sw_init` |
| [sym:hydrograph_module] | `sp_ob, wet, wet_om_init, ch_stor, ch_om_water_init, fp_stor, fp_om_water_init, res, res_om_init` | `sp_ob%hru, sp_ob%hru_lte, sp_ob%chandeg, sp_ob%res, sp_ob%aqu` |
| [sym:hru_lte_module] | `hlt, hlt_init` |  |
| [sym:sd_channel_module] | `sd_ch, sdch_init` |  |
| [sym:aquifer_module] | `aqu_om_init` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pco%sw_init` | Always, before any object-count checks. | pco%sw_init is set to "n" to disable basin soil-water initialization for the next rerun. |
| `hru` | Only when sp_ob%hru > 0. | The live HRU array is replaced with hru_init so HRU-level state returns to its saved baseline. |
| `soil` | Only when sp_ob%hru > 0. | The live soil profile array is replaced with soil_init to restore baseline soil conditions for all HRUs. |
| `soil1` | Only when sp_ob%hru > 0. | The live soil1 mass profile array is replaced with soil1_init so organic/mineral soil mass state resets with the rest of the HRU state. |
| `pcom` | Only when sp_ob%hru > 0. | The plant community array pcom is restored from pcom_init so plant parameter and community structure state is reset. |
| `pl_mass` | Only when sp_ob%hru > 0. | The plant mass array pl_mass is restored from pl_mass_init to reset biomass and related mass state. |
| `wet` | Only when sp_ob%hru > 0. | The wetland hydrologic output array wet is restored from wet_om_init to reset wetland storage/state tied to HRUs. |
| `bss` | Only when sp_ob%hru > 0. | bss is set to 0. so basin baseflow storage starts the new run empty. |
| `hlt` | Only when sp_ob%hru_lte > 0. | The HRU-LTE state array hlt is restored from hlt_init. |
| `sd_ch` | Only when sp_ob%chandeg > 0. | The SWAT-DEG channel dynamic array sd_ch is restored from sdch_init. |
| `ch_stor` | Only when sp_ob%chandeg > 0. | Channel storage ch_stor is restored from ch_om_water_init to reset channel water state. |
| `fp_stor` | Only when sp_ob%chandeg > 0. | Floodplain storage fp_stor is restored from fp_om_water_init so floodplain water state matches the saved baseline. |
| `res` | Only when sp_ob%res > 0. | Reservoir state res is restored from res_om_init. |
| `aqu_om_init` | Only when sp_ob%aqu > 0. | The aquifer initialization array aqu_om_init is assigned to itself, so the extracted code shows no effective aquifer state change. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in df07e3f as a new reset subroutine that restores HRU, soil, plant, channel, reservoir, and aquifer-related state from saved initialization arrays and clears bss. In eb22103, the only behavioral change in this file was removal of the rsd1 = rsd1_init reset line; the current source no longer resets rsd1 here.

- df07e3f added re_initialize.f90 with full reset logic for pco%sw_init, hru, soil, soil1, pcom, pl_mass, wet, bss, hlt, sd_ch, ch_stor, fp_stor, res, and aqu_om_init.
- eb22103 removed the rsd1 = rsd1_init assignment from the HRU reset block, so residue state is no longer reset by this routine.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 're_initialize' has no extracted documentation comment.
- Source line 48 is a self-assignment (aqu_om_init = aqu_om_init), so the aquifer branch appears to be a no-op in the extracted code.
