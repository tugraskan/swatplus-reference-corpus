---
kind: module
symbol: tillage_data_module
title: tillage_data_module
status: filled
source_hash: 10259fc01bae291b
version_label: SWAT+ 62.0.0
variables:
  bmix_idtill: '|none          |the tilldb index of the biomix tillage.'
  till_eff_days: '|none          |length of days a tillage operation will have an effect'
  bmix_eff: '|none          |biological mixing efficieny'
  bmix_depth: '|mm            |maximum potential biological mixing depth'
  dtill: '|mm            |actual biological or tillage mixing  mixing depth'
  bmix_a: '|none          !Base intercept in zz equation in mgt_tillfactor.f90 for biomixing'
  bmix_b: '|none          !slope of in zz equation in mgt_tillfactor.f90 for biomixing'
  bmix_c: '|none          !exponent multiplier in zz equation in mgt_tillfactor.f90 for biomixing'
  tillmix_a: '|none          !Base intercept in zz equation in mgt_tillfactor.f90 for tillage
    mixing'
  tillmix_b: '|none          !slope of in zz equation in mgt_tillfactor.f90 for tillage mixing'
  tillmix_c: '|none          !exponent multiplier in zz equation in mgt_tillfactor.f90 for
    tillage mixing'
  bio_consf: '|none          |biological mixing moisture consolidation factor used by `mgt_biomix`
    and set from `carbon.bsn`.'
  till_consf: '|none          |tillage mixing moisture consolidation factor used by `mgt_tillfactor`
    and set from `carbon.bsn`.'
  tilldb: Allocatable saved array of `tillage_db` records loaded from `tillage.til`; it supplies
    tillage operation names, mixing efficiency, mixing depth, roughness, and ridge properties
    to management, decision-table, and initialization routines.
type_components:
  tillage_db:
    tillnm: Tillage operation name used as the lookup key when schedules and decision tables
      crosswalk a text operation to a tillage database index.
    effmix: none               |mixing efficiency of tillage operation
    deptil: mm                 |depth of mixing caused by tillage
    ranrns: mm                 |random roughness
    ridge_ht: mm                 |ridge height
    ridge_sp: mm                 |ridge interval (or row spacing)
type_summaries:
  tillage_db: One tillage operation definition, including its name and the physical mixing/roughness
    parameters that management routines use when applying a tillage event.
---

<!-- facts:header -->

tillage_data_module owns the shared tillage and biological-mixing parameter state used across SWAT+ management, carbon, and soil-initialization routines. It also defines the `tillage_db` record type and the allocatable `tilldb` database that stores tillage operation definitions, including the special `biomix` entry that later routines use for mixing depth and efficiency.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container with no contained procedures. Its state is populated by file readers and setup routines such as `till_parm_read`, `carbon_bsn_read`, and `soil_nutcarb_init`, while management routines read the shared values later during tillage and carbon calculations.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `tilldb` | Reads the tillage database entry to print tillage diagnostics and to dispatch tillage or biomixing events through the selected operation index. |
| [sym:cal_parm_select] | `calibration parameter request` | `bio_consf, till_consf, bmix_a, bmix_b, bmix_c, tillmix_a, tillmix_b, tillmix_c` | Updates the shared tillage and biomixing calibration constants when a calibration case targets one of those parameter names. |
| [sym:carbon_bsn_read] | `carbon.bsn, _lyr.bsn` | `till_eff_days, bio_consf, till_consf, bmix_a, bmix_b, bmix_c, tillmix_a, tillmix_b, tillmix_c` | Reads basin carbon settings and loads the tillage-effect timing, consolidation factors, and tillage/biomixing curve-fit coefficients from the basin carbon file. |
| [sym:dtbl_lum_read] | `lum.dtl` | `tilldb` | Crosswalks land-use decision-table tillage actions to a numeric tillage database index by matching action names against `tilldb(idb)%tillnm`. |
| [sym:dtbl_res_read] | `res_rel.dtl` | `none` | The module is imported in the routine's interface context, but no symbol from `tillage_data_module` is referenced in the extracted source. |
| [sym:dtbl_scen_read] | `scen_lu.dtl` | `none` | The module is imported in the routine's interface context, but no visible `tillage_data_module` symbol is referenced in the extracted source. |
| [sym:hru_control] | `unit_100100` | `till_eff_days, bmix_eff` | Monitors tillage age against `till_eff_days` to clear expired tillage effects and later triggers biomixing when `bmix_eff` is active. |
| [sym:mgt_sched] | `unit_2612` | `tilldb` | Uses the tillage database name lookup to identify the schedule's tillage operation index before invoking tillage mixing routines. |
| [sym:read_mgtops] | `unit_107, unit_9001` | `tilldb` | Maps each management schedule's tillage operation text to a `tilldb` index so later execution can reference the selected tillage record. |
| [sym:soil_nutcarb_init] | `soil initialization state` | `bmix_depth, bmix_eff` | Uses the biological mixing depth and efficiency to initialize each soil layer's starting biotillage mixing factor. |
| [sym:till_parm_read] | `tillage.til` | `bmix_idtill, bmix_eff, bmix_depth, tilldb` | Loads all tillage database records, then identifies the `biomix` record and stores its index, efficiency, and depth in the shared module state. |

## Key Consumers

The main importers fall into three groups: parameter readers that load or calibrate tillage state, management routines that apply tillage or biomixing during execution, and initialization/carbon routines that consume the stored coefficients and thresholds later in the model.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:cal_parm_select] | tillage_data_module | Updates the shared tillage and biomixing calibration constants so later tillage and biomix calculations use the selected calibration values. |
| [sym:carbon_bsn_read] | tillage_data_module | Loads the basin carbon file values into the module so later carbon and disturbance routines use the file-driven tillage timing and mixing coefficients. |
| [sym:dtbl_lum_read] | tillage_data_module | Provides the tillage name database used to resolve a land-use decision-table tillage action into the numeric operation index stored in the decision table. |
| [sym:read_mgtops] | tillage_data_module | Supplies the tillage operation names that let the schedule reader translate each scheduled tillage action into a `tilldb` index for later execution. |
| [sym:soil_nutcarb_init] | tillage_data_module | Provides the biological mixing depth and efficiency used to seed each soil layer's initial biotillage state in the soil profile. |
| [sym:till_parm_read] | tillage_data_module | Allocates and fills the tillage database, then stores the biomix record index, efficiency, and depth for later tillage and biomixing routines. |
| [sym:dtbl_res_read] | tillage_data_module | Imported by the routine, but no extracted source line shows a reference to any `tillage_data_module` symbol. |
| [sym:dtbl_scen_read] | tillage_data_module | Imported by the routine, but no extracted source line shows a reference to any `tillage_data_module` symbol. |
| [sym:cbn_zhang2] | tillage_data_module | Provides the tillage-effect age threshold used when the DSSAT tillage branch applies disturbance effects in the soil carbon routine. |
| [sym:mgt_biomix] | tillage_data_module | Supplies the biological mixing depth and efficiency, plus the consolidation factor, that control how much biomixing occurs in the HRU soil profile. |
| [sym:mgt_newtillmix_cswat0] | tillage_data_module | Supplies the selected tillage record's efficiency and depth so the routine can apply the proper soil mixing for a tillage event. |
| [sym:mgt_newtillmix_cswat1] | tillage_data_module | Supplies the selected tillage record's efficiency and depth so the routine can apply the proper soil mixing for a tillage event and record the tillage depth state. |
| [sym:mgt_newtillmix_wet] | tillage_data_module | Supplies the selected tillage record's efficiency and depth so wet tillage can mix the ponded water and wetted soil column to the correct depth. |
| [sym:mgt_sched] | tillage_data_module | Uses the tillage database name lookup to route a scheduled tillage operation to the correct tillage-mixing routine. |
| [sym:mgt_tillfactor] | tillage_data_module | Supplies the empirical coefficients and consolidation constant used to compute daily layer mixing factors for biomixing and tillage. |
| [sym:actions] | tillage_data_module | Uses the tillage database to print the active tillage name and efficiency and to dispatch the matching tillage or biomixing action. |
| [sym:hru_control] | tillage_data_module | Uses the tillage age threshold to expire tillage effects and the biomix efficiency to decide when to run biological mixing. |

## Lineage

`tillage_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 10 non-merge commit(s) since, most recently `bc7755a` (2026-05-27, "Refactor carbon subsystem: file-based inputs, per-family outputs, calibration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `tillage_data_module.f90` are listed.

- `bc7755a` (2026-05-27) — Refactor carbon subsystem: file-based inputs, per-family outputs, calibration
- `1d2922d` (2026-05-06) — added bio_consf and till_consf to tillage_data_module
- `08d78c9` (2026-04-15) — Changes to use surface temperature of soil to determine when surface residue decomposition occurs. Removed unnecessary code from cbn_zhang2…
- `df18587` (2026-03-26) — Added variables coefs for bio and tillage mixing.
- `2ee1889` (2025-11-17) — Cleanup of sine warnings.
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No extracted module-level documentation comment is present in the source.
- No commits were resolved for this source span in the provided Git lineage evidence.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
