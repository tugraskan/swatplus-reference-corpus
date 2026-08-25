---
kind: module
symbol: pesticide_data_module
title: pesticide_data_module
status: filled
source_hash: 918e63322a479cf2
version_label: SWAT+ 62.0.0
variables:
  pestdb: Allocatable saved array of `pesticide_db` records. It holds the raw pesticide properties
    read from `pesticide.pes` or updated by calibration, including adsorption, half-lives,
    solubility, transfer velocities, benthic parameters, plant uptake, and description. Readers/writers
    seen in the packet include `pest_parm_read`, `cal_parm_select`, `pest_washp`, `pest_pl_up`,
    `pest_lch`, `ch_rtpest`, `res_pest`, `res_initial`, `read_mgtops`, and `constit_db_read`.
  pestcp: Allocatable saved array of `pesticide_cp` records. It stores calculated pesticide
    coefficients derived from `pestdb`, especially decay multipliers and daughter-metabolite
    mappings. `pest_parm_read` computes the decay factors from half-lives, and `pest_metabolite_read`
    allocates and fills the `daughter` arrays and metabolite counts.
type_components:
  pesticide_db:
    name: '|pesticide name'
    koc: (mL/g)               |soil adsorption coeff normalized for soil org carbon content
    washoff: none                 |frac of pesticide on foliage which is washed off by rainfall
      event
    foliar_hlife: days                 |half-life of pest on foliage
    soil_hlife: days                 |half-life of pest in soil
    solub: mg/L (ppm)           |solubility of chemical in water
    aq_hlife: days                 |aquatic half-life
    aq_volat: m/day                |aquatic volatilization coeff
    mol_wt: g/mol                |molecular weight - to calculate mixing velocity
    aq_resus: m/day                |aquatic resuspension velocity for pesticide sorbed to
      sediment
    aq_settle: m/day                |aquatic settling velocity for pesticide sorbed to sediment
    ben_act_dep: m                    |depth of active benthic layer
    ben_bury: m/day                |burial velocity in benthic sediment
    ben_hlife: days                 |half-life of pest in benthic sediment
    pl_uptake: none                 |fraction taken up by plant
    descrip: pesticide description
  daughter_decay_fractions:
    name: daughter pesticide name
    num: sequential pesticide number in simulation
    foliar_fr: 0-1                  |fraction of parent foilar degrading to daughter
    soil_fr: 0-1                  |fraction of parent soil degrading to daughter
    aq_fr: 0-1                  |fraction of parent aquatic degrading to daughter
    ben_fr: 0-1                  |fraction of parent benthic degrading to daughter
  pesticide_cp:
    num_metab: number of metabolites
    daughter: Allocated array of `daughter_decay_fractions` records that lists the daughter
      pesticides for this parent and the fraction routed to each daughter.
    decay_f: none                 |exp of the rate const for degradation of the pest on foliage
    decay_s: none                 |exp of the rate const for degradation of the pest in soil
    decay_a: none                 |exp of the rate const for degradation of the pest in aquatic
    decay_b: none                 |exp of the rate const for degradation of the pest in benthic
      layer
type_summaries:
  pesticide_db: One record in the pesticide parameter database. It represents a single parent
    pesticide species and its base physical/chemical properties used throughout SWAT+.
  daughter_decay_fractions: One daughter-metabolite routing record attached to a parent pesticide.
    It names a daughter pesticide, stores its basin sequence number, and gives the fraction
    of parent decay that becomes that daughter in each domain.
  pesticide_cp: Calculated pesticide-parameter record derived from the raw database entry.
    It stores first-order decay multipliers and the allocated daughter-metabolite list for
    one pesticide.
---

<!-- facts:header -->

Declares the shared pesticide database (`pestdb`) and calculated pesticide-parameter table (`pestcp`) used by SWAT+ pesticide initialization, calibration, and fate/transport routines. The module itself only owns the data types and allocatable state; startup readers such as `pest_parm_read` and `pest_metabolite_read` populate the arrays, and later processes read them for decay, wash-off, uptake, routing, and reservoir/channel mixing calculations.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only. It does not contain initialization routines itself, but its allocatable arrays are populated by external readers such as `pest_parm_read` and `pest_metabolite_read`, and then consumed by downstream calibration, initialization, and fate routines.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:cal_parm_select] | `calibration parameter selection data` | `pestdb, pestcp` | Applies `pst_*` calibration branches by updating pesticide database fields such as KOC, wash-off, half-lives, solubility, volatilization, settling, and resuspension coefficients. |
| [sym:ch_read] | `channel.cha` | `pestdb, pestcp` | Imported alongside the module, but the extracted body does not show resolved pesticide-data symbol use. The packet does not support a direct read of `pestdb` or `pestcp` here. |
| [sym:constit_db_read] | `constituents.cs` | `pestdb, pestcp` | Uses `pestdb(ipestdb)%name` to match constituent pesticide names to pesticide database indices during constituent database loading. |
| [sym:cs_hru_init] | `HRU constituent initialization data` | `pestdb, pestcp` | Imported, but no resolved pesticide-data symbols are visible in the extracted body. The packet does not show a direct population of `pestdb` or `pestcp` here. |
| [sym:dtbl_lum_read] | `lum.dtl` | `pestdb, pestcp` | The source imports the module, but the visible routine body crosswalks pesticide actions through constituent and management tables rather than resolved pesticide-database symbols. |
| [sym:hydro_init] | `hydrology initialization data` | `pestdb, pestcp` | Imported, but no resolved pesticide-data symbols are visible in the extracted body. The packet does not show a direct population of `pestdb` or `pestcp` here. |
| [sym:pest_metabolite_read] | `pest_metabolite.pes` | `pestdb, pestcp` | Reads parent pesticide names, allocates each parent's `daughter` array in `pestcp`, stores metabolite names and decay fractions, and crosswalks daughter names to basin pesticide numbers. |
| [sym:pest_parm_read] | `pesticide.pes` | `pestdb, pestcp` | Reads the pesticide parameter database into `pestdb` and derives the calculated decay multipliers in `pestcp` from the half-life fields. |
| [sym:pesticide_init] | `HRU pesticide initialization data` | `pestdb, pestcp` | Imported, but the extracted body does not show resolved pesticide-data symbols. The packet does not support a direct read of `pestdb` or `pestcp` here. |
| [sym:read_mgtops] | `unit_107, unit_9001` | `pestdb, pestcp` | Matches management-operation pesticide names against `pestdb(idb)%name` to store the pesticide database index in each schedule record. |
| [sym:res_initial] | `unit_105` | `pestdb, pestcp` | Uses `pestdb(ipest_db)%mol_wt` when computing reservoir pesticide mixing velocity during reservoir startup. |
| [sym:res_read] | `reservoir.res` | `pestdb, pestcp` | Imported for reservoir startup context, but the extracted body does not show a resolved pesticide-data symbol use from this module. |

## Key Consumers

The main consumers are pesticide database loaders and parameter readers, calibration and management crosswalk routines, and the process modules that simulate pesticide decay, wash-off, uptake, routing, and reservoir/channel exchange. Some importers use only `pestdb`, while others use both `pestdb` and `pestcp` for decay and metabolite routing.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:cal_parm_select] | pesticide_data_module | Applies pesticide calibration updates directly to `pestdb` fields so later fate, transport, and decay routines run with the adjusted pesticide parameters. |
| [sym:constit_db_read] | pesticide_data_module | Uses `pestdb(ipestdb)%name` to resolve each constituent pesticide name into the pesticide database index stored in `cs_db%pest_num`. |
| [sym:pest_metabolite_read] | pesticide_data_module | Populates `pestcp` daughter arrays and metabolite counts from the metabolite file so parent-to-daughter routing is available to later pesticide process routines. |
| [sym:pest_parm_read] | pesticide_data_module | Loads pesticide records into `pestdb` and computes the derived decay multipliers in `pestcp` from the stored half-lives. |
| [sym:read_mgtops] | pesticide_data_module | Matches scheduled pesticide operation names against `pestdb(idb)%name` and stores the resolved database index for later management execution. |
| [sym:res_initial] | pesticide_data_module | Uses `pestdb(ipest_db)%mol_wt` to compute reservoir pesticide mixing velocity during reservoir initialization. |
| [sym:sd_hydsed_init] | pesticide_data_module | Uses pesticide initial-condition tables and `pestdb` properties when converting channel pesticide concentrations into stored masses and mixing coefficients. |
| [sym:ch_read] | pesticide_data_module | The module is imported in the channel reader, but the extracted body does not expose a resolved pesticide-data symbol use from this packet. |
| [sym:cs_hru_init] | pesticide_data_module | The module is imported, but the extracted body does not show any resolved pesticide-data symbols, so the exact role is not identifiable from this packet. |
| [sym:dtbl_lum_read] | pesticide_data_module | The module is imported, but the visible routine body crosswalks pesticide actions through constituent and management tables rather than resolved pesticide-database symbols. |
| [sym:pesticide_init] | pesticide_data_module | The module is imported, but the extracted body does not show a resolved pesticide-data symbol use from this packet. |
| [sym:res_read] | pesticide_data_module | The module is imported during reservoir loading, but the extracted body does not show a resolved pesticide-data symbol use from this packet. |
| [sym:salt_hru_init] | pesticide_data_module | The module is imported, but no resolved pesticide-data symbols are shown in the extracted body, so its specific contribution is not visible here. |
| [sym:sd_channel_read] | pesticide_data_module | The module is imported, but the extracted references do not show a pesticide-database symbol; channel pesticide setup is present elsewhere in the routine. |
| [sym:wet_read] | pesticide_data_module | The module is imported while wetland definitions are loaded, supporting later reservoir-linked pesticide accounting even though no direct symbol reference is visible in the extracted body. |
| [sym:aqu_1d_control] | pesticide_data_module | Reads `pestcp` decay factors and daughter mappings, then uses `pestdb` molecular weight to split aquifer pesticide decay into metabolite storage. |
| [sym:ch_rtpest] | pesticide_data_module | Uses `pestdb` and `pestcp` to parameterize channel pesticide reaction, volatilization, settling, resuspension, burial, and metabolite production. |
| [sym:pest_decay] | pesticide_data_module | Uses `pestcp` decay multipliers and daughter arrays with `pestdb` molecular weights to move decayed pesticide mass into daughter metabolites in soil and foliage. |
| [sym:pest_pl_up] | pesticide_data_module | Uses `pestdb(ipest_db)%pl_uptake` as the coefficient that controls pesticide transfer from soil layers into plant pools. |
| [sym:pest_washp] | pesticide_data_module | Uses `pestdb(ipest_db)%washoff` to move pesticide mass from plant foliage into the top soil layer. |
| [sym:res_pest] | pesticide_data_module | Uses `pestdb` and `pestcp` to compute reservoir pesticide reaction, volatilization, settling, resuspension, diffusion, burial, and daughter-metabolite routing. |
| [sym:pest_soil_tot] | pesticide_data_module | The module is listed as a dependency, but no specific symbols were resolved in the extracted references, so the exact effect is not visible here. |
| [sym:hydro_init] | pesticide_data_module | The module is imported, but the extracted evidence does not show a resolved pesticide-data symbol, so the exact effect is not visible here. |
| [sym:pest_lch] | pesticide_data_module | Uses `pestdb` to evaluate pesticide sorption and solubility limits when computing lateral and surface runoff loss from soil layers. |

## Lineage

`pesticide_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `889136d` (2025-02-03, "Fix typos"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pesticide_data_module.f90` are listed.

- `889136d` (2025-02-03) — Fix typos
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module-level documentation comment is absent in the extracted source.
- The reader list is representative of the initialization and lookup routines visible in the packet, not a guaranteed exhaustive population list beyond the extracted evidence.
- Some imported procedures in the evidence list do not show resolved pesticide-data symbol use in the visible excerpts; their exact role is therefore uncertain from this packet alone.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
