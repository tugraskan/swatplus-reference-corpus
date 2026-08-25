---
kind: procedure
symbol: obj_output
title: obj_output
status: filled
source_hash: c874d7d35da46a90
version_label: SWAT+ 62.0.0
locals:
  ihd: Hydrograph index chosen from `ob_out(itot)%hydno` and used to select the daily hydrograph
    record `ob(iob)%hd(ihd)` when writing non-subdaily hydro output.
  iob: Current object number pulled from `ob_out(itot)%objno`; it determines which spatial
    object’s state is written and whether the branch uses the all-HRU path (`iob == 0`) or
    a specific object.
  iunit: Base output unit number taken from `ob_out(itot)%unitno`; the routine writes to `iunit+itot`
    for each configured output object.
  itot: Loop counter over `mobj_out`; it indexes the output-object descriptor array `ob_out`
    and is added to `iunit` to form the actual write unit.
  nly: Loop index over soil layers when writing layer-by-layer soil water, soil nutrients,
    and carbon diagnostics.
  ly: Loop index over soil layers for profile-level nutrient and residue summations.
  j: Working HRU/object index used in branches that iterate over all HRUs or reassign `j =
    iob` for a single-object write.
  ii: Subdaily time-step index used when `time%step` > 0 and the routine writes subdaily hydrograph
    flow values.
  ipl: Plant index used to sum residue or status values over the plant community for a given
    object/HRU.
  linefmt: Format suffix appended to the plant-status `write` statement so the routine can
    print repeating plant fields with the desired mixed character/real layout.
uses:
  time_module: The current date and simulation step come from `time`; every output record
    is timestamped with `time%day`, `time%mo`, `time%day_mo`, and `time%yrc`, and the subdaily
    hydrograph branch also depends on `time%step` to decide how many flow records to emit.
  hydrograph_module: The hydrograph module provides the object-selection table (`ob_out`),
    the object counts in `sp_ob`, and the connectivity/output fields in `ob` that tell this
    routine which object to write, which hydrograph or flow array to use, and which names/types
    to print with the record.
  soil_module: Soil-layer water output uses `soil(j)%phys(nly)%st` and `soil(iob)%phys(nly)%st`
    to print per-layer soil water storage, and `soil% nly` defines how many layer records
    each object contributes.
  hru_module: The `ihru` index identifies the active HRU for branches that need a basin-wide
    HRU reference, especially the residue summation logic that seeds `soil1(ihru)%rsd_tot(nly)`
    and the `j = ihru` initialization used by the routine.
  organic_mineral_mass_module: The organic-mass module supplies the carbon, nitrogen, phosphorus,
    residue, humus, and microbial pools that are written in the nutrient and carbon diagnostics;
    the routine also updates profile residue and summary pools such as `soil_prof_microb`
    and `soil_prof_somc` from these states.
  plant_module: 'Plant community state is needed to print plant status output: the routine
    loops over `pcom(j)%npl` and writes each plant’s name, growth/dormancy flags, canopy metrics,
    and accumulated heat units from `pcom` and its nested components.'
---

<!-- facts:header -->

Writes a set of object-based daily diagnostic outputs for hydrology, soil water, soil nutrients, plant status, channel water balance, and carbon summaries.

## Bottom Line

obj_output is a dispatcher that walks the configured output objects in `ob_out`, selects the requested output type for each one, and writes the current simulation date plus the matching object state to the object’s output unit. The routine does not take arguments; it relies entirely on module state from the time, hydrograph, soil, HRU, organic-mass, and plant modules.

Its main purpose is to generate the simulation’s object-level text outputs. Depending on the selected hydrograph code, it writes subdaily or daily hydrographs, soil water by layer, soil nutrient profiles, plant status tables, channel/floodplain water balance, and two special carbon-diagnostic formats. Several branches also accumulate or reset profile summary variables before writing them.

## Arguments

<!-- facts:arguments -->

## Where It Fits

obj_output runs near the end of the `command` workflow, after the command driver has finished processing the simulation command sequence and set up the current object/time state. Its outputs are used immediately as simulation diagnostics, so later postprocessing and printed output files depend on it, not on any returned value.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize and map the active HRU reference | Sets the plant-format string and assigns `j = ihru`, establishing the default HRU index used by several branches before any object-specific overrides. |
| 2. Iterate over all configured output objects | Loops over `itot = 1, mobj_out` and pulls the current output-object descriptor fields from `ob_out(itot)`: object number, hydrograph code, and output unit number. |
| 3. Skip objects outside the spatial range | Only processes entries whose object index is within `sp_ob%objs`, then dispatches on `ob_out(itot)%hydno` to select the output family. |
| 4. Write hydrograph outputs | For hydrograph codes 1–5, writes either subdaily flow records over `time%step` or a single daily hydrograph record using `ob(iob)%hd(ihd)`. |
| 5. Write soil-water layer outputs | For soil-water output, writes either all HRU soil layers or the selected object’s soil layers by printing `soil%phys(nly)%st` values. |
| 6. Sum and write soil-layer nutrients | For soil nutrient output, accumulates residue totals into `soil1(%rsd_tot)`, then writes mineral and organic N/P pools for each layer and each selected HRU/object. |
| 7. Accumulate and emit profile nutrient summaries | Builds profile totals for mineral N/P and humus pools across all layers, recomputes residue totals with plant residue contributions, writes the summed profile line, and then zeros the accumulators for the next object. |
| 8. Write plant-status tables | For plant-status output, prints the date and object identifiers and then formats one repeating plant record per plant in `pcom(j)%npl` using `lineFmt` and the plant growth/status/mass arrays. |
| 9. Write channel water-balance output | For channel/floodplain water balance, writes one record per channel degree of freedom or the selected channel record using `ch_fp_wb(jrch)`. |
| 10. Emit special carbon-diagnostic headers and rows | On the hard-coded diagnostic days, writes carbon headers and then prints either HRU-wide layer carbon tables or a single-object carbon summary derived from humus, microbial, and residue pools. |
| 11. Exit the dispatch loop and return | Ends the `select case`, finishes the output-object loop, exits the outer `do`, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%step, time%day, time%mo, time%day_mo, time%yrc` |
| [sym:hydrograph_module] | `ob_out, sp_ob, ob, hd` | `ob_out(itot)%objno, ob_out(itot)%hydno, ob_out(itot)%unitno, sp_ob%objs, ob_out(itot)%hydtyp, ob(iob)%typ, ob(iob)%name, ob(iob)%hyd_flo(1,ii), ob(iob)%hd(ihd), sp_ob%hru, ob(j)%name, ob(j)%typ, sp_ob%chandeg, ob(iob)%sp_ob_no` |
| [sym:soil_module] | `soil` | `soil(j)%phys(nly)%st, soil(j)%nly, soil(iob)%phys(nly)%st, soil(iob)%nly` |
| [sym:hru_module] | `ihru` | `ihru` |
| [sym:organic_mineral_mass_module] | `soil1, pl_mass, soil_prof_microb, soil_org_z, soil_prof_somc` | `soil1(ihru)%rsd_tot(nly), soil1(ihru)%pl(ipl)%rsd(nly), soil1(j)%mn(nly), soil1(j)%hact(nly)%n, soil1(j)%hsta(nly)%n, soil1(j)%hs(nly)%n, soil1(j)%hp(nly)%n, soil1(j)%rsd_tot(nly)%n, soil1(j)%mp(nly), soil1(j)%hact(nly)%p, soil1(j)%hsta(nly)%p, soil1(j)%hs(nly)%p, soil1(j)%hp(nly)%p, soil1(j)%rsd_tot(nly)%p, soil1(j)%rsd_tot(nly), soil1(j)%pl(ipl)%rsd(nly), soil1(j)%mn(ly), soil1(j)%mp(ly), soil1(j)%hact(ly), soil1(j)%hsta(ly), soil1(j)%hs(ly), soil1(j)%hp(ly), soil1(j)%rsd_tot(ly), soil1(j)%pl(ipl)%rsd(ly), pl_mass(j)%tot(ipl)%m, pl_mass(j)%ab_gr(ipl)%m, pl_mass(j)%leaf(ipl)%m, pl_mass(j)%root(ipl)%m, pl_mass(j)%stem(ipl)%m, pl_mass(j)%seed(ipl)%m, soil_prof_microb%c, soil_org_z%c, soil1(j)%tot_org%c, soil_prof_somc%c, soil1(j)%hact(nly)%c, soil1(j)%hsta(nly)%c, soil1(j)%microb(nly)%c, soil1(iob)%tot_org%c, soil1(iob)%hact(nly)%c, soil1(iob)%hsta(nly)%c, soil1(iob)%microb(nly)%c` |
| [sym:plant_module] | `pcom` | `pcom(ihru)%npl, pcom(j)%npl, pcom(j)%pl(ipl), pcom(j)%plcur(ipl)%gro, pcom(j)%plcur(ipl)%idorm, pcom(j)%plg(ipl)%lai, pcom(j)%plg(ipl)%cht, pcom(j)%plg(ipl)%root_dep, pcom(j)%plcur(ipl)%phuacc` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil1(ihru)%rsd_tot(nly)` | When processing soil-nutrient or carbon branches that recompute layer residue totals from `soil1(%pl(ipl)%rsd(nly))`. | `soil1(ihru)%rsd_tot(nly)` is overwritten with a zeroed organic mass and then rebuilt as the sum of plant-residue carbon, nitrogen, and phosphorus for the active HRU layer before being written out. |
| `soil1(j)%rsd_tot(nly)` | When processing soil-nutrient or carbon branches for a selected object `j` or `iob`. | `soil1(j)%rsd_tot(nly)` is rebuilt from plant residue pools for that object and then used in the layer nutrient and profile outputs. |
| `soil_prof_mn` | Inside the soil-profile nutrient branches as each soil layer is accumulated. | `soil_prof_mn` grows by adding each layer’s mineral nitrogen pool, so the final value is the profile-total mineral N printed for the object. |
| `soil_prof_mp` | Inside the soil-profile nutrient branches as each soil layer is accumulated. | `soil_prof_mp` grows by adding each layer’s mineral phosphorus pool, producing the profile-total mineral P reported in the output. |
| `soil_prof_hact` | Inside the soil-profile nutrient branches as each soil layer is accumulated. | `soil_prof_hact` is incremented by each layer’s active humus mass so the printed value is the whole-profile active humus total. |
| `soil_prof_hsta` | Inside the soil-profile nutrient branches as each soil layer is accumulated. | `soil_prof_hsta` is incremented by each layer’s stable humus mass so the printed value is the whole-profile stable humus total. |
| `soil_prof_hs` | Inside the soil-profile nutrient branches as each soil layer is accumulated. | `soil_prof_hs` is incremented by each layer’s slow humus mass so the printed value is the whole-profile slow humus total. |
| `soil_prof_hp` | Inside the soil-profile nutrient branches as each soil layer is accumulated. | `soil_prof_hp` is incremented by each layer’s passive humus mass so the printed value is the whole-profile passive humus total. |
| `soil1(j)%rsd_tot(ly)` | When computing soil nutrient output for a specific layer of a selected object or HRU. | `soil1(j)%rsd_tot(ly)` is rebuilt from plant residue pools for that layer and then used in the layer-level nutrient output. |
| `soil_prof_rsd` | Inside the soil-profile nutrient branches after all layers have been summed. | `soil_prof_rsd` accumulates the layer residue totals, so it becomes the profile-wide fresh residue pool written to the summary line. |
| `jrch` | When the channel water-balance branch is selected and the routine iterates channels or maps the selected object to its spatial channel number. | `jrch` is assigned the current channel degree-of-freedom index used to select `ch_fp_wb(jrch)` for output. |
| `soil_prof_microb%c` | When running the special carbon-diagnostic branch for each HRU and each layer. | `soil_prof_microb%c` is zeroed for each HRU and then accumulated across layers to report the running microbial carbon pool used in the carbon table. |
| `soil1(j)%tot_org%c` | When building the carbon-diagnostic layer output for each HRU or selected object. | `soil1(j)%tot_org%c` is set to active humus plus stable humus plus microbial carbon for the current layer, producing the layer total organic carbon value written to the file. |
| `soil_prof_somc%c` | When building the carbon-diagnostic layer output for each HRU or selected object. | `soil_prof_somc%c` is reset and then built from active humus, stable humus, and accumulated microbial carbon so the routine can print a profile SOM-carbon value. |
| `soil1(iob)%tot_org%c` | When the HRU-level carbon diagnostic branch runs for the selected object `iob`. | `soil1(iob)%tot_org%c` is overwritten with the current layer’s active humus plus stable humus plus microbial carbon and then written as the HRU carbon summary. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `obj_output`. In 1807dbb, the soil-water and soil-nutrient branches were expanded so the profile output includes the current date/object identifiers, the soil-profile branch writes then resets profile accumulators, and the layer soil-water loop was wrapped explicitly. In 39fabde, several local variables were initialized to zero and `lineFmt` was initialized to an empty string. In 72206bc, residue totals were renamed from `rsd` to `rsd_tot` in the soil nutrient/profile outputs and those totals were recomputed from plant residue pools before writing; the diff also updated the corresponding carbon-diagnostic residue references.

- 1807dbb changed the soil-water and soil-profile nutrient outputs to include date/object fields and added explicit zeroing of the profile accumulators after each write.
- 39fabde initialized the routine’s local counters (`ihd`, `iob`, `iunit`, `itot`, `nly`, `ly`, `j`, `ii`, `ipl`) and `lineFmt`, removing uninitialized-state dependence.
- 72206bc replaced direct use of `soil1(%rsd)` with computed `soil1(%rsd_tot)` values built from plant residue pools and updated the nutrient/carbon write records to use the new residue-total field.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'obj_output' has no extracted documentation comment.
