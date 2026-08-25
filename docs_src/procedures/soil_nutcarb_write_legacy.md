---
kind: procedure
symbol: soil_nutcarb_write_legacy
title: soil_nutcarb_write_legacy
status: filled
source_hash: a80cb41881c21fd8
version_label: SWAT+ 62.0.0
args:
  out_freq: 'Selects which legacy output branch runs: daily, monthly, yearly, layer-by-layer
    variants, beginning-of-simulation snapshot, or end-of-simulation snapshot. The two-character
    code is mapped to a frequency label and may also enable layered output when the second
    character is `l`.'
locals:
  ly: Layer index used to walk soil layers and build per-layer writes and profile sums.
  const: Basin-area fraction used as the weighting coefficient when HRU values are accumulated
    to basin totals.
  tot_lyr_n: Temporary per-layer total organic nitrogen sum across residue, humus, and other
    organic pools for the current layer output record.
  tot_lyr_p: Temporary per-layer total organic phosphorus sum across residue, humus, and other
    organic pools for the current layer output record.
  tot_prof_n: Profile-wide total organic nitrogen sum across the soil-profile pools written
    in the profile summary records.
  tot_prof_p: Profile-wide total organic phosphorus sum across the soil-profile pools written
    in the profile summary records.
  prf_swc: Average profile soil water content computed from layer water content and profile
    thickness for the 300-mm carbon summary records.
  prf_depth: Running total of soil thickness used to normalize `prf_swc` across the full profile.
  frac_above_300: Fraction of a layer counted toward the 300-mm summary when only part of
    the layer lies above 300 mm depth.
  soil_prof_lig_n: Accumulated profile lignin nitrogen pool used in the non-layer profile
    nutrient summary.
  soil_prof_nonlig_n: Accumulated profile non-lignin nitrogen pool used in the non-layer profile
    nutrient summary.
  soil_prof_lig_p: Accumulated profile lignin phosphorus pool used in the non-layer profile
    nutrient summary.
  soil_prof_nonlig_p: Accumulated profile non-lignin phosphorus pool used in the non-layer
    profile nutrient summary.
  iihru: Basin-HRU index derived from `lsu_elem(j)%obtypno` for mapping weighted HRU values
    into basin totals.
  j: HRU loop counter used to index the current soil profile, plant community, and output
    record.
  ipl: Plant index used when iterating plant communities or plant-level residue/root pools.
  iob: Hydrograph object index for the current HRU, used to fetch GIS ID, object name, and
    type for output records.
  profile_depth: Integer depth-to-bottom of the last soil layer, used as the 300-mm cutoff
    reference.
  freq_label: Text label written into output records (`day`, `mon`, `year`, `begsim`, or `endsim`)
    after decoding `out_freq`.
  layer_output: Flag that enables layer-by-layer output when the frequency code ends in `l`.
  write_hdr: Header-write flag for legacy output streams; initialized true but not visibly
    used in the extracted body.
  root_frac_ly: Temporary per-layer root-fraction value used when constructing root-distribution
    summaries.
uses:
  soil_module: '`soil_module` provides the HRU soil profile metadata and layer properties
    that this routine prints, including layer count, soil series name, layer depths, and physical
    properties such as bulk density, water capacity, carbon content, texture, and surface-layer
    attributes. Those values define the per-HRU soil snapshot records and the depth basis
    for the layered and profile summaries.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` supplies the per-HRU carbon,
    nitrogen, phosphorus, residue, root, humus, microbial, and flux pools that this routine
    aggregates and writes. Without these shared mass objects, the routine could not form the
    layer and profile totals for soil, plant, residue, and organic-flux output.'
  hydrograph_module: '`hydrograph_module` provides the HRU object counts and identifiers needed
    to locate the current object and label each output line with the correct GIS ID, object
    name, and object type. That mapping is what lets the routine connect internal HRU indices
    to exported reporting records.'
  calibration_data_module: '`calibration_data_module` matters because this routine is only
    one piece of the legacy reporting path and uses control data that determine whether CSV
    variants of the output are emitted. The extracted routine body checks `pco%csvout`, so
    the module’s imported print-control state governs whether the text-only or CSV streams
    are written.'
  carbon_module: '`carbon_module` matters because the routine resets and accumulates the basin
    and profile carbon/organic summary objects before writing them out. Those shared carbon-state
    variables hold the summary pools that are exported at the end of the routine and therefore
    must be available from the carbon model state.'
  basin_module: '`basin_module` provides the basin carbon control code and CSV print flag
    that gate this legacy output path. `bsn_cc%cswat` switches between static and dynamic
    carbon behavior, and `pco%csvout` decides whether the `.csv` companion records are written
    alongside the text files.'
  plant_module: '`plant_module` supplies the plant-community structure and root-fraction arrays
    needed to write plant carbon summaries and distribute root mass by layer. The routine
    reads community count and layer root fractions from `pcom` so it can report plant totals
    and layer root contributions for each HRU.'
---

<!-- facts:header -->

Writes legacy CSU/SWAT-C soil carbon, residue, plant, and soil-property outputs for HRUs and basin totals at the requested frequency.

## Bottom Line

`soil_nutcarb_write_legacy` is a legacy output routine that prints soil-profile properties, carbon and nutrient pool summaries, plant carbon summaries, and organic-flux diagnostics for each HRU. The output pattern depends on the requested frequency code in `out_freq`, whether CSV output is enabled, and whether the basin carbon mode `bsn_cc%cswat` is set to 2.

It is also responsible for accumulating basin-level organic soil, plant, and residue totals from HRU results and writing a final basin summary line. The routine is gated by `print.prt` control flags through `pco%cb_hru` and `pco%csvout`, and it is called from the main command flow and opening/setup code when legacy carbon outputs are requested.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when the driver or output subsystem requests the legacy CSU carbon outputs for HRUs, typically from `command` for daily/monthly/yearly/average-annual cases or from setup code for begin-simulation snapshots. The opening/setup path prepares the initial begin-simulation call, and later the same routine’s basin totals and summary writes feed the legacy carbon reporting files used by the end-of-step output process.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Decode the requested legacy frequency | The routine maps the two-character `out_freq` code to a human-readable label and, for the `l` variants, turns on layered output so both layer and profile records can be written. |
| 2. Reset basin organic totals | Before doing any HRU reporting, the routine zeros the basin organic-soil, plant, and residue totals using the shared carbon zero state. |
| 3. Handle begin/end simulation snapshots | If the frequency label is `begsim` or `endsim` and carbon diagnostics are enabled, the routine loops over HRUs and writes soil-property snapshots for each layer; `begsim` goes to the begin-sim soil-property files, while `endsim` goes to the end-sim soil-property files and CSV companions when enabled. |
| 4. Build HRU organic pools and layer summaries | For normal reporting frequencies, the routine loops over HRUs, resets per-HRU summary objects, and accumulates layer-by-layer organic pools for soil, residue, humus, roots, and related nitrogen and phosphorus totals. |
| 5. Emit layer and profile nutrient summaries | The routine writes per-layer and profile nitrogen/phosphorus summary lines to the legacy text and CSV files, using `-1, -1` as the profile marker and `tot_lyr_*` / `tot_prof_*` values to summarize the pools. |
| 6. Emit plant carbon summaries | When carbon diagnostics are enabled, the routine writes plant-community carbon totals and, if CSV output is requested, the CSV companion record. |
| 7. Emit organic-flux diagnostics for cswat=2 | If the basin carbon mode is dynamic (`bsn_cc%cswat == 2`), the routine writes layer and profile organic-flux outputs for the HRU, including CSV copies when requested. |
| 8. Compute 300-mm carbon summaries | The routine computes profile depth, average profile soil water content, and 300-mm carbon totals, then writes layer and profile carbon-and-water summary records for the HRU. |
| 9. Accumulate basin-weighted organic totals | After the HRU loop, the routine maps HRUs through `lsu_elem`, applies basin fractions, and adds weighted soil, plant, residue, mineral nitrogen, and mineral phosphorus contributions into the basin summary state. |
| 10. Write the final basin summary | The routine writes the final basin organic summary line to the basin output unit, reporting day, year, and basin-level organic soil, plant, and residue carbon. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%snam, soil(j)%phys(ly)%bd, soil(j)%phys(ly)%awc, soil(j)%phys(ly)%k, soil(j)%phys(ly)%cbn, soil(j)%phys(ly)%clay, soil(j)%phys(ly)%silt, soil(j)%phys(ly)%sand, soil(j)%phys(ly)%rock, soil(j)%ly(ly)%alb, soil(j)%ly(ly)%usle_k, soil(j)%ly(ly)%ec, soil(j)%ly(ly)%cal, soil(j)%ly(ly)%ph, soil(j)%phys(ly)%d, soil(j)%phys(ly-1)%d` |
| [sym:organic_mineral_mass_module] | `soil1, pl_mass` | `soil1(j)%tot(ly)%c, soil1(j)%tot_org, soil1(j)%seq_org, soil1(j)%surf_org, soil1(j)%hs(ly), soil1(j)%hp(ly), soil1(j)%microb(ly), soil1(j)%rsd_tot(ly), soil1(j)%root_tot(ly), soil1(j)%pl(ipl)%rsd(ly), soil1(j)%root_tot(ly)%m, pl_mass(j)%root(ipl)%m, soil1(j)%str(ly), soil1(j)%hact(ly), soil1(j)%hsta(ly), soil1(j)%man(ly), soil1(j)%meta(ly), soil1(j)%lig(ly), soil1(j)%nonlig(ly), soil1(j)%lig(ly)%n, soil1(j)%nonlig(ly)%n, soil1(j)%lig(ly)%p, soil1(j)%nonlig(ly)%p, soil1(j)%water(ly), soil1(j)%meta(1), soil1(j)%str(1), soil1(j)%microb(1), soil1(j)%hs(1), soil1(j)%man(1), soil1(j)%water(1), soil1(j)%tot_300_c, soil1(j)%hact(ly)%c, soil1(j)%hsta(ly)%c, soil1(j)%microb(ly)%c, soil1(j)%seq_tot_300_c, soil1(j)%seq(ly)%c, soil1(j)%rsd_tot(ly)%n, soil1(j)%str(ly)%n, soil1(j)%meta(ly)%n, soil1(j)%hs(ly)%n, soil1(j)%hp(ly)%n, soil1(j)%microb(ly)%n, soil1(j)%water(ly)%n, soil1(j)%man(ly)%n, soil1(j)%rsd_tot(ly)%p, soil1(j)%str(ly)%p, soil1(j)%meta(ly)%p, soil1(j)%hs(ly)%p, soil1(j)%hp(ly)%p, soil1(j)%microb(ly)%p` |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%hru, sp_ob1%hru, ob(iob)%name, ob(iob)%typ` |
| [sym:calibration_data_module] | `pco` | `pco%csvout` |
| [sym:carbon_module] | `soil_org_z, soil_prof_hact, soil_prof_hsta, soil_prof_rsd, soil_prof_root, soil_prof_root_frac, soil_prof_str, soil_prof_lig, soil_prof_nonlig, soil_prof_meta, soil_prof_man, soil_prof_seq_hs, soil_prof_seq_hp, soil_prof_seq_microb, soil_prof_water` | `soil_org_z, soil_prof_hact, soil_prof_hsta, soil_prof_rsd, soil_prof_root, soil_prof_root_frac, soil_prof_str, soil_prof_lig, soil_prof_nonlig, soil_prof_meta, soil_prof_man, soil_prof_seq_hs, soil_prof_seq_hp, soil_prof_seq_microb, soil_prof_water` |
| [sym:basin_module] | `pco, bsn_cc` | `pco%csvout, bsn_cc%cswat` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl, pcom(j)%plg(ipl)%rtfr(ly)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `bsn_org_soil` | When the routine starts, before any HRU processing. | `bsn_org_soil` is reset to the zero organic state so basin soil-organic carbon can be rebuilt from the current HRU contributions. |
| `bsn_org_pl` | When the routine starts, before any HRU processing. | `bsn_org_pl` is reset to the zero organic state so basin plant carbon can be rebuilt from the current HRU contributions. |
| `bsn_org_rsd` | When the routine starts, before any HRU processing. | `bsn_org_rsd` is reset to the zero organic state so basin residue carbon can be rebuilt from the current HRU contributions. |
| `soil1(j)%tot_org` | Inside the HRU loop while building the current HRU’s soil summary. | `soil1(j)%tot_org` is set to the zero organic state and then filled from the layer totals so it represents the HRU’s total soil organic pool. |
| `soil1(j)%seq_org` | Inside the HRU loop while building the current HRU’s soil summary. | `soil1(j)%seq_org` is set to the zero organic state and then filled from the layer sequence-carbon pools so it represents the HRU’s sequestered-organic pool. |
| `soil1(j)%surf_org` | Inside the HRU loop while building the current HRU’s soil summary. | `soil1(j)%surf_org` is set to the zero organic state and then filled from surface-layer organic pools so it represents the HRU’s surface organic pool. |
| `soil_prof_hact` | During the layer accumulation loop for each HRU. | `soil_prof_hact` is updated from the active-humus layer pool so the profile active-humus summary reflects the current HRU’s layer totals. |
| `soil_prof_hsta` | During the layer accumulation loop for each HRU. | `soil_prof_hsta` is updated from the stable-humus layer pool so the profile stable-humus summary reflects the current HRU’s layer totals. |
| `soil_prof_rsd` | During the layer accumulation loop for each HRU. | `soil_prof_rsd` is updated from the residue layer pools so the profile residue summary reflects the current HRU’s layer totals. |
| `soil_prof_root` | During the layer accumulation loop for each HRU. | `soil_prof_root` is updated from the live-root layer pools so the profile root summary reflects the current HRU’s layer totals. |
| `soil_prof_root_frac` | During the layer accumulation loop for each HRU. | `soil_prof_root_frac` is updated from the plant root-fraction data so the routine can report root distribution by layer. |
| `soil_prof_str` | During the layer accumulation loop for each HRU. | `soil_prof_str` is updated from the structural-litter layer pool so the profile structural-litter summary reflects the current HRU’s layer totals. |
| `soil_prof_lig` | During the layer accumulation loop for each HRU. | `soil_prof_lig` is updated from the lignin pool so the profile lignin summary reflects the current HRU’s layer totals. |
| `soil_prof_nonlig` | During the layer accumulation loop for each HRU. | `soil_prof_nonlig` is updated from the non-lignin pool so the profile non-lignin summary reflects the current HRU’s layer totals. |
| `soil_prof_meta` | During the layer accumulation loop for each HRU. | `soil_prof_meta` is updated from the metabolic-litter pool so the profile metabolic summary reflects the current HRU’s layer totals. |
| `soil_prof_man` | During the layer accumulation loop for each HRU. | `soil_prof_man` is updated from the manure pool so the profile manure summary reflects the current HRU’s layer totals. |
| `soil_prof_seq_hs` | During the layer accumulation loop for each HRU. | `soil_prof_seq_hs` is updated from the sequestered-humus component so the profile sequence-carbon summary captures slow humus contributions. |
| `soil_prof_seq_hp` | During the layer accumulation loop for each HRU. | `soil_prof_seq_hp` is updated from the sequestered-passive-humus component so the profile sequence-carbon summary captures passive humus contributions. |
| `soil_prof_seq_microb` | During the layer accumulation loop for each HRU. | `soil_prof_seq_microb` is updated from the sequestered-microbial component so the profile sequence-carbon summary captures microbial contributions. |
| `soil_prof_hs` | During the layer accumulation loop for each HRU. | `soil_prof_hs` is updated from the slow-humus pool so the profile carbon summary captures the slow-humus mass. |
| `soil_prof_hp` | During the layer accumulation loop for each HRU. | `soil_prof_hp` is updated from the passive-humus pool so the profile carbon summary captures the passive-humus mass. |
| `soil_prof_microb` | During the layer accumulation loop for each HRU. | `soil_prof_microb` is updated from the microbial biomass pool so the profile carbon summary captures microbial mass. |
| `soil_prof_water` | During the profile-water calculation for each HRU. | `soil_prof_water` is updated from layer water pools so the profile summary can report total water-associated organic mass or water content as written in the summary record. |
| `soil1(j)%rsd_tot(ly)` | During the per-layer residue accounting loop. | `soil1(j)%rsd_tot(ly)` is filled from the current layer’s residue pools so residue carbon, nitrogen, and phosphorus can be printed in the layer and profile summary records. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The procedure was introduced in commit 821a63e with legacy CSU carbon output logic for begin/end simulation snapshots, layer/profile soil-carbon and nutrient reporting, plant carbon reporting, organic-flux output, 300-mm carbon summaries, basin weighting, and the final basin summary write. Commit dfce092 later changed the carbon-mode gating from `bsn_cc%cswat == 1` to `bsn_cc%cswat == 2` in the soil-carbon accumulation, sequence-carbon accumulation, and `cswat == 2` output branch, and updated the nearby comment to say the `cswat == 2` files are written.

- 821a63e introduced the legacy soil carbon reporting routine, including all major text/CSV output streams, basin-weighted accumulation, and the final basin summary write.
- dfce092 changed the dynamic-carbon branch from `bsn_cc%cswat == 1` to `bsn_cc%cswat == 2`, so the legacy outputs now follow the revised CSWAT mode numbering and the corresponding comment was updated.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'soil_nutcarb_write_legacy' has no extracted documentation comment.
- calibration_data_module and carbon_module have no resolved candidate outside refs in the packet; their "outside" fields were inferred only from the available module lists and nearby state usage.
- algorithm_steps revised: merged the draft's scattered case labels into ten source-backed steps that follow the actual execution path and cite only visible source lines.
- Some summary-variable names in the draft are broader than the visible source excerpts; where the extracted body did not show a direct assignment, the description states the inferred role from the surrounding writes and accumulations.
