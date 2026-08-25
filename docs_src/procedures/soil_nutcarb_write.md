---
kind: procedure
symbol: soil_nutcarb_write
title: soil_nutcarb_write
status: filled
source_hash: 46b730ad2f0a10d3
version_label: SWAT+ 62.0.0
args:
  out_freq: Selects the reporting frequency branch. The code recognizes `' d'`, `'dl'`, `'
    m'`, `'ml'`, `' y'`, `'yl'`, `' a'`, `'al'`, `' b'`, and `' e'`, and uses that choice
    to set `freq_label` and whether layer output is enabled.
locals:
  ly: Layer index used to traverse soil layers and accumulate layer-based carbon, nitrogen,
    phosphorus, and water quantities.
  const: Basin expansion factor copied from `lsu_elem(iihru)%bsn_frac` when reconstructing
    basin totals from HRU values.
  tot_lyr_n: Declared accumulator for total layer nitrogen; not assigned in the visible source
    span.
  tot_lyr_p: Declared accumulator for total layer phosphorus; not assigned in the visible
    source span.
  tot_prof_n: Declared accumulator for total profile nitrogen; not assigned in the visible
    source span.
  tot_prof_p: Declared accumulator for total profile phosphorus; not assigned in the visible
    source span.
  prf_swc: Profile soil-water content accumulator; initialized to zero but not used in the
    visible source span.
  prf_depth: Profile depth accumulator; declared but not used in the visible source span.
  frac_above_300: Fraction of a layer contributing to the 300 mm cutoff when computing `tot_300_c`
    and `seq_tot_300_c`.
  soil_prof_lig_n: Accumulator for profile lignin nitrogen across layers.
  soil_prof_nonlig_n: Accumulator for profile non-lignin nitrogen across layers.
  soil_prof_lig_p: Accumulator for profile lignin phosphorus across layers.
  soil_prof_nonlig_p: Accumulator for profile non-lignin phosphorus across layers.
  iihru: Index into `lsu_elem` used to map an HRU loop entry to its basin-weighting metadata.
  j: Primary HRU loop index used throughout the routine.
  ipl: Plant index used when summing residue and root contributions across plants in an HRU.
  iob: Object index into `ob` for the current HRU's metadata.
  profile_depth: Declared profile-depth helper; not used in the visible source span.
  freq_label: Normalized frequency label derived from `out_freq`; drives begsim/endsim handling
    and downstream emit calls.
  layer_output: Logical flag set true for layer-output variants (`dl`, `ml`, `yl`, `al`).
  root_frac_ly: Average root-fraction across plants in the current layer, used when accumulating
    `soil_prof_root_frac`.
uses:
  soil_module: Provides the soil-layer count and layer depths used to traverse each HRU profile
    and compute the 300 mm cutoff for carbon summaries.
  organic_mineral_mass_module: Provides the organic and mineral pool objects that are summed
    into HRU-level and basin-level carbon, nitrogen, and phosphorus outputs.
  hydrograph_module: Provides HRU counts, HRU-to-object indexing, and object metadata used
    to loop over HRUs and label output rows.
  calibration_data_module: Provides the basin expansion factor and object-type mapping used
    when converting HRU totals into basin totals.
  carbon_module: Holds the basin and zero-value carbon/mineral accumulators that this routine
    resets and updates.
  basin_module: Provides the print-control flags and carbon-model mode that gate which output
    families are written and how totals are computed.
  plant_module: Provides plant-community counts and layer root-fraction weights used to apportion
    residue and root mass by layer.
---

<!-- facts:header -->

Writes HRU soil carbon, nitrogen, phosphorus, plant-carbon, flux, and soil-snapshot outputs at the requested reporting frequency.

## Bottom Line

`soil_nutcarb_write` is the central HRU-level output dispatcher for soil nutrient/carbon reporting. It maps the requested frequency code to a reporting label, prepares basin-level carbon accumulators, and then emits the enabled HRU output families by calling the specialized `cb_*_emit` helpers.

For begsim/endsim requests it writes only the soil snapshot total file when that output is enabled. For day, month, year, and average-annual requests it loops over HRUs, assembles layer/profile totals from `soil1`, `soil`, `pcom`, and `pl_mass`, writes the enabled per-family files, and then reconstructs basin-weighted organic and mineral totals from the HRU results.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from `command` during daily, monthly, and yearly dispatch when any HRU carbon/nutrient/snapshot family is enabled; from `hru_output` at end of simulation for the begsim/endsim total snapshot; and from `output_landscape_init` to emit the begsim total snapshot when dynamic carbon mode is active. The routine depends on upstream setup of `soil`, `soil1`, `pcom`, `pl_mass`, `lsu_elem`, `pco`, and `bsn_cc`, and its outputs feed the HRU and basin carbon/nutrient documentation files used later in the model run.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Normalize output frequency | Map `out_freq` to a reporting label and layer-output flag. |
| 2. Reset basin carbon totals | Initialize basin organic and mineral carbon accumulators before any HRU processing. |
| 3. Handle begsim/endsim snapshot | If the request is a begin- or end-simulation snapshot and the snapshot family is enabled, loop over HRUs and emit the total soil snapshot rows, then return immediately. |
| 4. Loop over HRUs | Iterate through each HRU and derive the object index used for row labels and basin weighting. |
| 5. Clear HRU accumulators | Reset the HRU-level soil and profile accumulators that will be rebuilt from layer data. |
| 6. Accumulate layer pools | Traverse soil layers, sum residue, root, humus, litter, microbial, and water pools, and compute average root fraction per layer. |
| 7. Build HRU organic totals | Combine the layer accumulators into total, sequestered, and surface organic carbon summaries for the HRU. |
| 8. Compute 300 mm carbon | Compute the fraction of each layer above 300 mm and accumulate total carbon above that depth for the active carbon method. |
| 9. Populate CSWAT totals | When the static carbon method is active, derive total layer carbon from active humus, stable humus, and microbial carbon. |
| 10. Compute sequestered carbon | Accumulate sequestered carbon above 300 mm and, for the static method, populate the per-layer sequestered carbon field. |
| 11. Emit HRU output families | Call the layered carbon, N+P pool, plant-carbon, soil-snapshot, and dynamic carbon flux/pool emitters for the current HRU. |
| 12. Reconstruct basin totals | Loop over HRUs again, apply basin expansion factors, and accumulate basin organic and mineral totals from the HRU results. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(ly)%d, soil(j)%phys(ly-1)%d, soil(hru_j)%nly` |
| [sym:organic_mineral_mass_module] | `soil1, pl_mass` | `soil1(j)%tot_org, soil1(j)%seq_org, soil1(j)%surf_org, soil1(j)%hs(ly), soil1(j)%hp(ly), soil1(j)%microb(ly), soil1(j)%rsd_tot(ly), soil1(j)%root_tot(ly), soil1(j)%pl(ipl)%rsd(ly), soil1(j)%root_tot(ly)%m, pl_mass(j)%root(ipl)%m, soil1(j)%str(ly), soil1(j)%hact(ly), soil1(j)%hsta(ly), soil1(j)%man(ly), soil1(j)%meta(ly), soil1(j)%lig(ly), soil1(j)%nonlig(ly), soil1(j)%lig(ly)%n, soil1(j)%nonlig(ly)%n, soil1(j)%lig(ly)%p, soil1(j)%nonlig(ly)%p, soil1(j)%water(ly), soil1(j)%meta(1), soil1(j)%str(1), soil1(j)%microb(1), soil1(j)%hs(1), soil1(j)%man(1), soil1(j)%water(1), soil1(j)%tot_300_c, soil1(j)%hact(ly)%c, soil1(j)%hsta(ly)%c, soil1(j)%microb(ly)%c, soil1(j)%tot(ly)%c, soil1(j)%seq_tot_300_c, soil1(j)%seq(ly)%c, soil1(iihru)%tot_org, pl_mass(iihru)%tot_com, pl_mass(iihru)%rsd_tot, soil1(iihru)%tot_mn, soil1(iihru)%tot_mp, soil1(hru_j)%str(k)%n, soil1(hru_j)%meta(k)%n, soil1(hru_j)%hs(k)%n, soil1(hru_j)%hp(k)%n, soil1(hru_j)%microb(k)%n, soil1(hru_j)%water(k)%n, soil1(hru_j)%man(k)%n, soil1(hru_j)%str(k)%p, soil1(hru_j)%meta(k)%p, soil1(hru_j)%hs(k)%p, soil1(hru_j)%hp(k)%p` |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%hru, sp_ob1%hru, ob(hru_iob)%name` |
| [sym:calibration_data_module] | `lsu_elem` | `lsu_elem(j)%obtypno, lsu_elem(iihru)%bsn_frac, lsu_elem(iihru)%obtyp` |
| [sym:carbon_module] | `soil_org_z, bsn_org_soil, bsn_org_pl, bsn_org_rsd, bsn_mn, bsn_mp` | `soil_org_z, bsn_org_soil, bsn_org_pl, bsn_org_rsd, bsn_mn, bsn_mp` |
| [sym:basin_module] | `pco, bsn_cc` | `pco%cb_snap_hru%a, bsn_cc%cswat, pco%cb_cpool_hru%d, pco%cb_cpool_hru%m, pco%cb_cpool_hru%y, pco%cb_cpool_hru%a, pco%csvout, pco%cb_npool_hru%d, pco%cb_npool_hru%m, pco%cb_npool_hru%y, pco%cb_npool_hru%a` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl, pcom(j)%plg(ipl)%rtfr(ly)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bsn_org_soil` | At routine entry | Reset to `soil_org_z` before basin totals are reconstructed from HRU values. |
| `bsn_org_pl` | At routine entry | Reset to `soil_org_z` before basin totals are reconstructed from HRU values. |
| `bsn_org_rsd` | At routine entry | Reset to `soil_org_z` before basin totals are reconstructed from HRU values. |
| `soil1(j)%tot_org` | For each HRU in the main loop | Recomputed as the sum of profile organic pools across layers. |
| `soil1(j)%seq_org` | For each HRU in the main loop | Recomputed as the sum of sequestered organic pools across layers. |
| `soil1(j)%surf_org` | For each HRU in the main loop | Recomputed from layer 1 surface organic pools only. |
| `soil_prof_hact` | For each HRU in the main loop | Accumulated active humus across all layers. |
| `soil_prof_hsta` | For each HRU in the main loop | Accumulated stable humus across all layers. |
| `soil_prof_rsd` | For each HRU in the main loop | Accumulated total fresh residue across all layers. |
| `soil_prof_root` | For each HRU in the main loop | Accumulated total live root mass across all layers. |
| `soil_prof_root_frac` | For each HRU in the main loop | Accumulated average plant root fraction across layers. |
| `soil_prof_str` | For each HRU in the main loop | Accumulated structural litter across all layers. |
| `soil_prof_lig` | For each HRU in the main loop | Accumulated lignin pool across all layers. |
| `soil_prof_nonlig` | For each HRU in the main loop | Accumulated non-lignin pool across all layers. |
| `soil_prof_meta` | For each HRU in the main loop | Accumulated metabolic litter across all layers. |
| `soil_prof_man` | For each HRU in the main loop | Accumulated manure pool across all layers. |
| `soil_prof_seq_hs` | For each HRU in the main loop | Accumulated sequestered slow humus across layers greater than the surface layer. |
| `soil_prof_seq_hp` | For each HRU in the main loop | Accumulated sequestered passive humus across layers greater than the surface layer. |
| `soil_prof_seq_microb` | For each HRU in the main loop | Accumulated sequestered microbial biomass across layers greater than the surface layer. |
| `soil_prof_hs` | For each HRU in the main loop | Accumulated slow humus across all layers. |
| `soil_prof_hp` | For each HRU in the main loop | Accumulated passive humus across all layers. |
| `soil_prof_microb` | For each HRU in the main loop | Accumulated microbial biomass across all layers. |
| `soil_prof_water` | For each HRU in the main loop | Accumulated water-soluble organic pool across all layers. |
| `soil1(j)%rsd_tot(ly)` | For each HRU in the main loop | Rebuilt from plant residue pools across all plants in the HRU layer. |
| `soil1(j)%root_tot(ly)` | For each HRU in the main loop | Rebuilt from plant root fractions and root masses across all plants in the HRU layer. |
| `soil1(j)%tot_300_c` | For each HRU in the main loop | Set to the carbon total above 300 mm for the active carbon method. |
| `soil1(j)%seq_tot_300_c` | For each HRU in the main loop | Set to the sequestered carbon total above 300 mm for the active carbon method. |
| `soil1(j)%tot(ly)%c` | When `bsn_cc%cswat == 0` | Populated from active humus, stable humus, and microbial carbon for the static carbon method. |
| `soil1(j)%seq(ly)%c` | When `bsn_cc%cswat == 0` | Populated from active humus, stable humus, and microbial carbon for the static carbon method. |
| `soil1(j)%tot_300_c` | When `bsn_cc%cswat == 2` | Accumulated from `soil1(j)%tot(ly)%c` for the dynamic carbon method. |
| `soil1(j)%seq_tot_300_c` | When `bsn_cc%cswat == 2` | Accumulated from `soil1(j)%seq(ly)%c` for the dynamic carbon method. |
| `bsn_org_soil` | When basin totals are reconstructed | Accumulated from HRU soil organic totals using basin expansion factors. |
| `bsn_org_pl` | When basin totals are reconstructed | Accumulated from HRU plant community totals using basin expansion factors. |
| `bsn_org_rsd` | When basin totals are reconstructed | Accumulated from HRU residue totals and profile residue totals using basin expansion factors. |
| `bsn_mn` | When basin totals are reconstructed | Accumulated from HRU mineral nitrogen totals using basin expansion factors. |
| `bsn_mp` | When basin totals are reconstructed | Accumulated from HRU mineral phosphorus totals using basin expansion factors. |

## File I/O

<!-- facts:io -->


## Lineage

`soil_nutcarb_write.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 74 non-merge commit(s) since, most recently `dfce092` (2026-06-02, "move carbon activation to cswat = 2, reserve 1 for C-FARM"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `soil_nutcarb_write.f90` are listed.

- `dfce092` (2026-06-02) — move carbon activation to cswat = 2, reserve 1 for C-FARM
- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `07c7ea3` (2026-05-18) — Cleaned soil_nutcarb_write to make it more clear as to what it was doing in regard to writing headers one time for hru_cbn_lyrs and hru_seq_…
- `c3a99cb` (2026-05-15) — Updated code to include root_mass in hru_cpool output and in jupyter notebook code. Removed hru_rsdc graphs from jupyter notebook.
- `28c64c3` (2026-05-14) — Removed output files no longer needed. hru_soilc_stat hru_rsdc_stat, hru_soilcarb_mb_stat
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- No source-backed Git lineage evidence was available; lineage summary reflects that limitation.
- `carbon_module` had no resolved outside references in the context packet, so its state usage is described only at the module level from visible source facts.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
