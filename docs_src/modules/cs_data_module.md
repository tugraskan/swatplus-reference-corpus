---
kind: module
symbol: cs_data_module
title: cs_data_module
status: filled
source_hash: c68476a07f001966
version_label: SWAT+ 62.0.0
variables:
  cs_rct_soil: allocatable array of `constituent_rct` records, one per HRU, holding soil reaction
    parameters loaded from `cs_reactions`
  cs_rct_aqu: allocatable array of `constituent_rct` records, one per aquifer, holding aquifer
    reaction parameters loaded from `cs_reactions`
  rct: allocatable 2-D reaction table read from `cs_reactions`; used to assign group-specific
    constituent parameters
  rct_shale: allocatable shale-parameter table read from `cs_reactions`; used to assign shale-layer
    parameters
  num_geol_shale: number of geologic formations with shale, read from `cs_reactions` and used
    to size shale arrays and loop bounds
  bor_tol_sim: flag read from `cs_plants_boron` to enable or disable simulation of boron effects
    on plant growth
  bor_stress_a: allocatable per-plant boron relative-yield coefficient array read from `cs_plants_boron`
  bor_stress_b: allocatable per-plant boron relative-yield coefficient array read from `cs_plants_boron`
type_components:
  constituent_rct:
    kd_seo4: sorption partition coefficient for seo4
    kd_seo3: sorption partition coefficient for seo3
    kd_born: sorption partition coefficient for boron
    kseo4: first-order rate constant for seo4 reduction to seo3
    kseo3: first-order rate constant for seo3 reduction to elemental se
    se_ino3: selenium reduction inhibition factor
    oxy_soil: oxygen concentration in soil water
    oxy_aqu: oxygen concentration in groundwater
    shale: fraction of object area occupied by shale formations, source of se
    sseratio: sulfur/se ratio in shale material
    ko2a: first-order rate constant for autotrophic reduction of dissolved oxygen
    kno3a: first-order rate constant for autotrophic reduction of no3
type_summaries:
  constituent_rct: Reaction-property record for constituent sorption and kinetics in soils
    or aquifers.
---

<!-- facts:header -->

Shared constituent-chemistry data container for SWAT+; it owns the soil and aquifer reaction records, reaction lookup tables, shale reaction tables, the shale-count control flag, and plant boron stress settings that downstream readers and chemistry routines populate and consume.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a shared declaration container; its variables are initialized by reader routines, especially `cs_plant_read`, `cs_reactions_read`, and `gwflow_read`, rather than by contained procedures here.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:cs_plant_read] | `cs_plants_boron` | `bor_tol_sim, bor_stress_a, bor_stress_b` | Reads the boron simulation flag and allocates/fills the per-plant boron stress coefficient arrays. |
| [sym:cs_reactions_read] | `cs_reactions` | `cs_rct_soil, cs_rct_aqu, rct, rct_shale, num_geol_shale` | Allocates the soil and aquifer reaction records, reads the reaction-group tables, reads the shale table, and loads the per-HRU and per-aquifer reaction properties. |
| [sym:gwflow_read] | `gwflow and related groundwater input files` | `rct, rct_shale, num_geol_shale` | Uses the reaction tables and shale count while building groundwater constituent chemistry state and assigning reaction-group values to groundwater cells. |

## Key Consumers

Imported by the plant boron reader, the reaction-table reader, groundwater setup, sorption routines, selenium reaction routines, reservoir constituent balance, and wetland constituent balance.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:cs_plant_read] | cs_data_module | Populates the shared boron-simulation flag and per-plant boron stress coefficients that later plant-growth and stress calculations use. |
| [sym:cs_reactions_read] | cs_data_module | Allocates and fills the shared HRU and aquifer reaction records plus the reaction and shale lookup tables that later chemistry routines read. |
| [sym:gwflow_read] | cs_data_module | Provides the reaction lookup tables and shale-count state used while assigning groundwater constituent chemistry and solute settings during gwflow initialization. |
| [sym:cs_sorb_aqu] | cs_data_module | Supplies aquifer Kd values so the routine can recompute dissolved-versus-sorbed selenium and boron masses at equilibrium. |
| [sym:cs_sorb_hru] | cs_data_module | Supplies HRU Kd values so the routine can repartition selenium and boron between soil water and sorbed mass in each layer. |
| [sym:se_reactions_aquifer] | cs_data_module | Provides aquifer reaction parameters and the shale-unit count needed to compute selenium redox reaction rates in aquifer water. |
| [sym:se_reactions_soil] | cs_data_module | Provides HRU reaction parameters and the shale-unit count needed to compute selenium redox reaction rates in soil layers. |
| [sym:cs_rctn_aqu] | cs_data_module | The aquifer reaction update runs only when the constituent database indicates constituent reactions are active, so this module governs whether the groundwater chemistry step executes. |
| [sym:cs_rctn_hru] | cs_data_module | The HRU reaction update is gated by the constituent-database state, so this module controls whether the soil selenium reaction step executes. |
| [sym:res_cs] | cs_data_module | Provides the constituent-database context used by the reservoir constituent mass-balance routine. |
| [sym:wet_cs] | cs_data_module | Provides the constituent state used by the wetland mass-balance routine to update wetland and soil constituent storage. |

## Lineage

`cs_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cs_data_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No line-specific lineage commits were resolved for this module in the provided Git Lineage Evidence.
- The source shows `gwflow_read` uses `rct` and `rct_shale`; the broader groundwater chemistry import is inferred from completed procedure evidence rather than from this module file alone.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
