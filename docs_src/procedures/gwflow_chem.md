---
kind: procedure
symbol: gwflow_chem
title: gwflow_chem
status: filled
source_hash: 7fef3ec26d6264a0
version_label: SWAT+ 62.0.0
args:
  cell_id: '`cell_id` selects which groundwater cell''s chemistry state, solute concentrations,
    shale flags, and connectivity are used to compute reaction masses.'
  gw_vol: '`gw_vol` is the groundwater volume for the selected cell; it scales concentration-based
    reaction rates into daily mass changes.'
locals:
  s: '`s` is a solute-loop counter that is declared here but not used in the visible source;
    the 2025 lineage shows it was later removed as unused.'
  n: '`n` indexes shale entries within the current cell or a connected cell so the routine
    can test each shale source and accumulate release terms.'
  k: '`k` indexes the connected groundwater cells of `cell_id` when the routine checks adjacent
    cells for shale-driven selenium release.'
  shale_source: '`shale_source` is a flag that is set when the current cell itself contains
    shale; if it stays zero, the routine also searches neighboring cells for shale sources.'
  cell_conn: '`cell_conn` holds the id of a neighboring connected cell retrieved from `cell_con(cell_id)%cell_id(k)`
    so the routine can inspect that neighbor''s chemistry state.'
  isalt: '`isalt` counts salt-ion species while the routine loops through `cs_db%num_salts`
    and fills salt reaction masses.'
  sol_index: '`sol_index` tracks the current position in the groundwater solute list as the
    routine steps through nitrate, phosphorus, salts, and constituents.'
  rctn_rate: '`rctn_rate` temporarily holds a per-solute reaction coefficient, first for nitrate
    mass and later for selenium-species reduction rates.'
  cseo4: '`cseo4` stores the current selenate concentration in the selected cell so the routine
    can compute its reduction mass.'
  cseo3: '`cseo3` stores the current selenite concentration in the selected cell so the routine
    can compute its reduction mass.'
  cno3: '`cno3` stores the current nitrate concentration used for nitrate mass, nitrate inhibition,
    and selenium-release calculations.'
  o2: '`o2` stores the current dissolved oxygen state for the cell and drives oxygen reduction
    and selenium mobilization terms.'
  no3inhib: '`no3inhib` computes the nitrate-inhibition factor applied to selenate and selenite
    reduction, reducing those reactions when nitrate is present.'
  seo4red: '`seo4red` is the selenate reduction rate in concentration units, used to compute
    the selenate mass reaction term.'
  seo3red: '`seo3red` is the selenite reduction rate in concentration units, used to compute
    the selenite mass reaction term.'
  o2red: '`o2red` is the oxygen reduction rate produced by shale oxidation; it is used to
    estimate selenium release from shale sources.'
  no3red: '`no3red` accumulates nitrate reduction from shale sources and is used to calculate
    selenium release coupled to nitrate reduction.'
  yseo4_o2: '`yseo4_o2` is the fixed stoichiometric factor used to convert oxygen reduction
    into released selenium mass.'
  yseo4_no3: '`yseo4_no3` is the fixed stoichiometric factor used to convert nitrate reduction
    into released selenium mass.'
  se_prod_o2: '`se_prod_o2` accumulates selenium production associated with oxygen-driven
    shale oxidation.'
  se_prod_no3: '`se_prod_no3` accumulates selenium production associated with nitrate-driven
    shale oxidation.'
  ko2a: '`ko2a` holds the shale- or bedrock-specific oxygen-reduction coefficient used for
    the current shale source being evaluated.'
  kno3a: '`kno3a` holds the shale- or bedrock-specific nitrate-reduction coefficient used
    for the current shale source being evaluated.'
  sseratio: '`sseratio` holds the selenium-to-sulfur release ratio for the current shale source
    and scales selenium release from reduction rates.'
uses:
  gwflow_module: '`gwflow_module` provides the cell groundwater state and connectivity needed
    to find how many neighboring cells exist for `cell_id` and to build reaction terms against
    that cell''s solute state.'
  hydrograph_module: '`hydrograph_module` is imported by the routine even though no candidate
    reference from it was resolved in the extracted source; it is therefore relevant only
    as a compile-time dependency in this context, and the extracted evidence does not show
    a specific symbol used from it.'
  constituent_mass_module: '`constituent_mass_module` supplies `cs_db%num_salts`, which tells
    the routine how many salt-ion reaction entries to process when salt chemistry is enabled.'
---

<!-- facts:header -->

Computes groundwater chemistry reaction mass changes for one gwflow cell. It fills the groundwater reaction arrays used by the solute transport step.

## Bottom Line

`gwflow_chem` computes daily reaction masses for groundwater solutes in a single cell. It starts with first-order reactions for nitrate, phosphorus, and salt ions, then applies a special mineral-reaction hook if enabled, and finally adds constituent chemistry for selenium, oxygen, nitrate inhibition, and shale-driven selenium release.

The routine matters because `gwflow_solute` uses its outputs when assembling the net mass change for each solute. Its results combine local groundwater concentrations, groundwater volume, per-solute reaction coefficients, and cell-specific shale/mineral flags to determine how much mass is produced or consumed in that cell during the time step.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`gwflow_chem` runs inside the groundwater solute transport workflow after `gwflow_solute` has selected the active cell and initialized `mass_rct` and `mass_min`. Its output reaction masses are then used by `gwflow_solute` to compute each solute's net mass change for the transport/reaction update.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize | Set the solute index to the first solute and clear the groundwater reaction mass array before any reaction calculations. |
| 2. first-order base reactions | Compute nitrate and phosphorus reaction masses from the current cell concentration, groundwater volume, and per-solute reaction coefficient. |
| 3. salt-ion loop | If salt chemistry is enabled, step through each simulated salt ion, add one solute index per salt, compute its mass reaction, and optionally call the mineral-reaction routine for that cell. |
| 4. load constituent concentrations | If constituent chemistry is enabled, read nitrate, selenate, selenite, and oxygen concentrations for the selected cell to drive the rest of the reaction calculations. |
| 5. compute selenium reduction | Form nitrate inhibition and compute concentration-based reduction rates for selenate and selenite. |
| 6. reset selenium release accumulators | Set selenium release stoichiometry factors, clear the selenium production accumulators, and clear the shale-source flag before checking shale sources. |
| 7. check shale inside the cell | Loop through shale records in the current cell; when a shale flag is present, compute oxygen and nitrate reduction, accumulate selenium release, clear the bedrock-shale flag, and mark that the cell itself is a shale source. |
| 8. check bedrock shale | If the cell still has bedrock shale enabled, compute the same oxygen, nitrate, and selenium-release terms from the bedrock shale parameters. |
| 9. search connected cells | If the current cell was not itself a shale source, loop over connected cells and inspect their shale lists to add neighboring shale-driven selenium release contributions. |
| 10. write selenium and nitrate reactions | Convert the accumulated selenium production and reduction terms into selenate and selenite mass reactions, then subtract nitrate loss from the nitrate reaction entry. |
| 11. add boron reaction | Advance to the boron solute slot and compute its first-order reaction mass from the cell concentration, groundwater volume, and reaction coefficient. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_state` | `gw_state(cell_id)%ncon` |
| [sym:hydrograph_module] | `hydrograph_module` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mass_rct` | When the routine reaches the constituent-reaction block and computes selenate/selenite and shale-driven selenium terms. | `mass_rct` is reset to zero at the start of the routine and then filled for nitrate, phosphorus, salts, selenium species, and boron so the caller can use a complete reaction-mass vector for the cell. |
| `mass_rct(sol_index)` | When constituent chemistry is enabled and the routine updates the current selenium reaction slots. | `mass_rct(sol_index)` and the neighboring selenium entries are overwritten with the net selenium reaction mass for the selected cell, combining reduction and shale-driven production terms. |
| `gwsol_chem(cell_id)%bed_flag` | When a shale flag is found in the selected cell's shale list. | `gwsol_chem(cell_id)%bed_flag` is cleared to prevent bedrock shale from also contributing when the cell already contains shale; this forces the routine to use only the local shale source path for that cell. |
| `mass_rct(1)` | When the constituent block reaches the nitrate update after calculating shale-driven nitrate reduction. | `mass_rct(1)` is reduced by the nitrate reduction term so nitrate mass loss is reflected in the first groundwater solute reaction slot. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved five commits affecting `gwflow_chem`. The earliest resolved change added the routine from upstream bitbucket and included the full groundwater chemistry logic. Later commits mostly cleaned formatting and initialized locals, while the 2026 merge inserted an explicit purpose note, added `s`, `k`, `shale_source`, `cell_conn`, and `rctn_rate`, and made the selenium/neighbor-shale logic clearer.

- 94b6dec added the initial `gwflow_chem` implementation: first-order reaction masses, optional mineral reactions, constituent selenium chemistry, shale checks, and neighbor-cell shale sourcing.
- 39fabde initialized local counters and reaction scalars to zero and normalized formatting, reducing uninitialized-variable risk in the chemistry calculations.
- f1e61a3 made only whitespace/formatting fixes to reaction assignments and the subroutine terminator.
- 2ee1889 removed the unused `s` declaration and adjusted the end-of-subroutine formatting.
- 92db11b added documentation, reintroduced `s`, added `k`, `shale_source`, `cell_conn`, and `rctn_rate`, and rewired the selenium-source logic to separate local shale from connected-cell shale checks.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gwflow_chem' has no extracted documentation comment.
- hydrograph_module is imported, but the extracted source and candidate refs did not resolve a specific symbol usage from that module.
- algorithm_steps revised: condensed the routine into 11 source-backed steps to match the visible control flow while preserving the cited line ranges.
