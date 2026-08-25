---
kind: procedure
symbol: soil_nutcarb_init
title: soil_nutcarb_init
status: filled
source_hash: ca42a7568173a580
version_label: SWAT+ 62.0.0
args:
  isol: '`isol` identifies the soil input record context, but this routine does not use it
    for the main calculations; it is only checked in a dummy `if (isol < 0) continue` statement
    to suppress an unused-argument warning.'
locals:
  nly: Number of soil layers in the current HRU soil profile; copied from `soil(ihru)%nly`
    and used to drive all per-layer initialization loops.
  ly: Loop index for the current soil layer while initializing C, N, P, and biotillage state.
  isolt: Index of the selected soil-test initialization database entry from `sol_plt_ini(isol_pl)%nut`;
    used to fetch starting nitrate, labile P, and humus ratios.
  isol_pl: Index of the soil-plant initialization record chosen through the HRU database pointer
    `hru(ihru)%dbs%soil_plant_init`.
  wt1: Per-layer conversion weight in kg/ha, computed from bulk density and layer thickness,
    then used to convert concentration-style initial values into layer masses.
  dep_frac: Depth decay factor applied to the default or database-provided surface nitrate
    and labile phosphorus concentrations.
  frac_hum_active: Fraction of total humus assigned to the active pool in the legacy SWAT
    carbon path; sourced from soil-test defaults when needed.
  actp: Active mineral phosphorus concentration in mg/kg, derived from the active pool mass
    and used when estimating stable phosphorus in the dynamic soil P model.
  solp: Solution/labile phosphorus concentration in mg/kg, derived from the labile pool mass
    and used in dynamic PSP and SSP calculations.
  ssp: Stable soil phosphorus coefficient used in the dynamic soil P model to scale the stable
    pool from the active + labile pools.
  psp: Phosphorus sorption parameter used to split labile P into active and to choose between
    dynamic and default mineral P initialization.
  mathers_frac: Empirical fraction used in the Mathers slow-humus initialization path to estimate
    how much sequestered carbon becomes slow humus from clay+silt content.
  tot_mass: Total soil organic matter mass for the current layer, derived from thickness and
    bulk density and then used to allocate organic carbon, nitrogen, and phosphorus pools.
uses:
  hru_module: '`hru_module` provides the current HRU object, the soil-plant initialization
    pointer, and the nutrient parameter `psp`. `soil_nutcarb_init` uses those values to choose
    the correct initialization record and, when the dynamic P model is off, to fall back to
    the HRU-level phosphorus sorption setting.'
  soil_module: '`soil_module` holds the soil profile for the current HRU, including layer
    count, layer depths, bulk density, thickness, organic carbon, and texture. Those properties
    determine how many layers to initialize, how to compute mass conversion factors, how deep-decay
    concentrations are applied, and how the Mathers carbon split responds to texture.'
  soil_data_module: '`soil_data_module` supplies the soil-test database record that seeds
    starting nitrate, labile P, active-humus fraction, and humus C:N and C:P ratios. Without
    it, the routine would have to use only hard-coded fallback values.'
  basin_module: '`basin_module` supplies basin control codes that switch the soil P algorithm
    and the carbon initialization style. `sol_P_model` selects the legacy versus dynamic phosphorus
    path, and `cswat` selects the legacy SWAT humus pools versus CENTURY-style pools.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` defines the `soil1` per-HRU
    mass structure that this routine populates. Its layer-wise carbon, mineral nitrogen/phosphorus,
    humus, residue, and microbial fields are the actual outputs of the initialization.'
  carbon_module: '`carbon_module` provides the global organic-fraction controls that decide
    how sequestered carbon is split into passive, slow, and microbial pools, and whether the
    Mathers slow-humus method is used.'
  tillage_data_module: '`tillage_data_module` matters because the final part of the routine
    assigns each soil layer’s initial biotillage mixing efficiency from the tillage mixing
    depth (`bmix_depth`) and efficiency (`bmix_eff`). Those values determine the `init_bmix`
    field written into the soil profile.'
---

<!-- facts:header -->

Initializes soil nutrient and carbon pools for each HRU soil layer, then sets initial biotillage mixing efficiency by depth. It supports both the legacy SWAT nutrient/humus scheme and the CENTURY-style carbon pools.

## Bottom Line

`soil_nutcarb_init` builds the starting soil chemistry state for the current HRU. It reads the HRU’s soil profile, the selected soil-plant initialization record, basin control flags, and carbon-fraction settings, then populates layer-by-layer nitrate, mineral phosphorus, organic nitrogen/phosphorus, and carbon pools.

It also computes `conv_wt` for converting concentration units to kg/ha and assigns `init_bmix` for each soil layer from the requested biotillage mixing depth. Those initialized pools and mixing values are what later soil nutrient cycling and carbon routines operate on.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during soil/nutrient setup after the HRU has been linked to its soil database entry and soil-plant initialization record. The upstream setup must have populated `soil(ihru)`, `hru(ihru)%dbs%soil_plant_init`, `sol_plt_ini`, and the basin control codes; the results are then used by later soil carbon and nutrient cycling, phosphorus partitioning, and tillage-mixing behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Resolve the current HRU soil context and initialization record. | Read the current HRU soil layer count, choose the soil-plant initialization record from `hru(ihru)%dbs%soil_plant_init`, and obtain the soil nutrient initialization selector `sol_plt_ini(isol_pl)%nut`. |
| 2. Seed layer carbon percentages. | Loop over soil layers and assign `soil1(ihru)%cbn(ly)`, forcing the surface layer to at least 0.001 percent carbon while copying deeper-layer carbon directly from the soil profile. |
| 3. Convert layer soil properties to mass basis. | For each layer, compute `soil(ihru)%phys(ly)%conv_wt` from bulk density and thickness, then store it in `wt1` for use as the kg/ha conversion factor. |
| 4. Initialize mineral nitrogen by depth. | Use the exponential depth factor `dep_frac` with either the database nitrate concentration or the default 7 ppm fallback, then convert the result from mg/kg to kg/ha. |
| 5. Initialize labile and active phosphorus pools. | Seed labile P from the soil-test database or a 5 ppm fallback, convert it to kg/ha, then compute active and stable mineral P using either the dynamic `sol_P_model` pathway or the legacy `4 * act` rule. |
| 6. Build total soil organic matter and humus pools. | Compute total organic mass, carbon, nitrogen, and phosphorus for each layer, then, when `cswat == 0`, split that total into active and stable humus using the soil-test active fraction and humus C:N/C:P ratios. |
| 7. Build CENTURY passive and slow humus pools. | When `cswat == 2`, derive the sequestered fraction from `org_frac%frac_seq`, populate passive humus, and choose the slow-humus formula from either the default fraction path or the Mathers texture-based path. |
| 8. Build microbial and residue pools. | Populate microbial biomass, then split the non-sequestered carbon into metabolic, structural, lignin, and non-lignin residue pools with fixed stoichiometric ratios. |
| 9. Assign tillage mixing efficiency and finalize sequestered totals. | Set each layer’s `init_bmix` from the biotillage depth and efficiency, then compute the total organic pool and the sequestered organic pool for the layer. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, sol_plt_ini` | `hru(ihru)%dbs%soil_plant_init, sol_plt_ini(isol_pl)%nut, hru(ihru)%nut%psp` |
| [sym:soil_module] | `soil` | `soil(ihru)%nly, soil(ihru)%phys(ly)%cbn, soil(ihru)%phys(ly)%conv_wt, soil(ihru)%phys(ly)%bd, soil(ihru)%phys(ly)%thick, soil(ihru)%phys(ly)%d, soil(ihru)%phys(ly)%clay, soil(ihru)%phys(ly)%silt, soil(ihru)%ly(ly)%init_bmix, soil(ihru)%phys(ly-1)%d` |
| [sym:soil_data_module] | `solt_db` | `solt_db(isolt)%nitrate, solt_db(isolt)%lab_p, solt_db(isolt)%fr_hum_act, solt_db(isolt)%hum_c_n, solt_db(isolt)%hum_c_p` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%sol_P_model, bsn_cc%cswat` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(ihru)%cbn(ly), soil1(ihru)%mn(ly)%no3, soil1(ihru)%mp(ly)%lab, soil1(ihru)%mp(ly)%act, soil1(ihru)%mp(ly)%sta, soil1(ihru)%tot(ly)%m, soil1(ihru)%tot(ly)%c, soil1(ihru)%tot(ly)%n, soil1(ihru)%tot(ly)%p, soil1(ihru)%hact(ly)%m, soil1(ihru)%hact(ly)%c, soil1(ihru)%hact(ly)%n, soil1(ihru)%hact(ly)%p, soil1(ihru)%hsta(ly)%m, soil1(ihru)%hsta(ly)%c, soil1(ihru)%hsta(ly)%n, soil1(ihru)%hsta(ly)%p, soil1(ihru)%hp(ly)%m, soil1(ihru)%hp(ly)%c, soil1(ihru)%hp(ly)%n, soil1(ihru)%hp(ly)%p, soil1(ihru)%hs(ly)%m, soil1(ihru)%hs(ly)%c, soil1(ihru)%hs(ly)%n, soil1(ihru)%hs(ly)%p, soil1(ihru)%microb(ly)%m, soil1(ihru)%microb(ly)%c, soil1(ihru)%microb(ly)%n, soil1(ihru)%microb(ly)%p, soil1(ihru)%meta(ly)%m, soil1(ihru)%meta(ly)%c, soil1(ihru)%meta(ly)%n, soil1(ihru)%meta(ly)%p, soil1(ihru)%str(ly)%m, soil1(ihru)%str(ly)%c, soil1(ihru)%str(ly)%n, soil1(ihru)%str(ly)%p, soil1(ihru)%lig(ly)%m, soil1(ihru)%lig(ly)%c, soil1(ihru)%lig(ly)%n, soil1(ihru)%lig(ly)%p, soil1(ihru)%nonlig(ly)%m, soil1(ihru)%nonlig(ly)%c, soil1(ihru)%nonlig(ly)%n, soil1(ihru)%nonlig(ly)%p, soil1(ihru)%tot(ly), soil1(ihru)%str(ly), soil1(ihru)%meta(ly), soil1(ihru)%hs(ly), soil1(ihru)%hp(ly), soil1(ihru)%microb(ly), soil1(ihru)%seq(ly)` |
| [sym:carbon_module] | `org_frac` | `org_frac%frac_not_seq, org_frac%frac_seq, org_frac%frac_hum_passive, org_frac%frac_hum_slow, org_frac%mathers_method, org_frac%frac_hum_microb` |
| [sym:tillage_data_module] | `bmix_depth, bmix_eff` | `bmix_depth, bmix_eff` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil1(ihru)%cbn(ly)` | For every soil layer during the first layer loop; surface layer uses `max(0.001, soil(ihru)%phys(ly)%cbn)` and deeper layers copy `soil(ihru)%phys(ly)%cbn`. | Sets the layer’s organic carbon percentage that is later used to compute total organic mass and, in the dynamic P path, the PSP estimate. |
| `soil(ihru)%phys(ly)%conv_wt` | For every soil layer before nitrate and phosphorus concentrations are converted to kg/ha. | Stores the mass-conversion factor derived from bulk density and layer thickness, so concentration-style initial values can be expressed as layer masses. |
| `soil1(ihru)%mn(ly)%no3` | For every soil layer after selecting the nitrate source value and applying the depth factor. | Initializes the layer nitrate stock from the soil-test database or default concentration and converts it to kg/ha for the mineral-N pool. |
| `soil1(ihru)%mp(ly)%lab` | For every soil layer after the labile-P source value and depth factor are chosen. | Initializes the labile phosphorus stock for the layer, then converts it to kg/ha for the mineral-P pool. |
| `soil1(ihru)%mp(ly)%act` | When `bsn_cc%sol_P_model == 1`; otherwise `psp` comes from `hru(ihru)%nut%psp`. | Sets active mineral phosphorus as the amount implied by the chosen phosphorus sorption parameter and the initialized labile pool. |
| `soil1(ihru)%mp(ly)%sta` | When `bsn_cc%sol_P_model == 1`; otherwise the legacy `4 * act` rule is used. | Sets the stable mineral phosphorus pool using the dynamic SSP estimate or the legacy ratio to active phosphorus. |
| `soil1(ihru)%tot(ly)%m` | For every layer while building the total soil organic pool. | Stores the layer’s total soil organic matter mass, derived from bulk soil mass, carbon percentage, and the 58% carbon assumption. |
| `soil1(ihru)%tot(ly)%c` | For every layer while building the total soil organic pool. | Stores the layer’s total soil organic carbon mass, which becomes the basis for nitrogen, phosphorus, humus, and residue allocation. |
| `soil1(ihru)%tot(ly)%n` | For every layer while building the total soil organic pool. | Initializes total organic nitrogen from the carbon mass using a fixed 10:1 C:N ratio. |
| `soil1(ihru)%tot(ly)%p` | For every layer while building the total soil organic pool. | Initializes total organic phosphorus from the carbon mass using a fixed 100:1 C:P ratio. |
| `soil1(ihru)%hact(ly)%m` | Only when `bsn_cc%cswat == 0`. | Initializes the active humus mass as the selected fraction of total organic matter for the legacy SWAT carbon path. |
| `soil1(ihru)%hact(ly)%c` | Only when `bsn_cc%cswat == 0`. | Initializes the active humus carbon pool from the total organic carbon and the active humus fraction. |
| `soil1(ihru)%hact(ly)%n` | Only when `bsn_cc%cswat == 0`. | Initializes active humus nitrogen from its carbon mass and the configured humus C:N ratio. |
| `soil1(ihru)%hact(ly)%p` | Only when `bsn_cc%cswat == 0`. | Initializes active humus phosphorus from its carbon mass and the configured humus C:P ratio. |
| `soil1(ihru)%hsta(ly)%m` | Only when `bsn_cc%cswat == 0`. | Initializes the stable humus mass as the remaining fraction of total organic matter after the active pool is removed. |
| `soil1(ihru)%hsta(ly)%c` | Only when `bsn_cc%cswat == 0`. | Initializes the stable humus carbon pool from the remaining share of total organic carbon. |
| `soil1(ihru)%hsta(ly)%n` | Only when `bsn_cc%cswat == 0`. | Initializes stable humus nitrogen from its carbon mass and the configured humus C:N ratio. |
| `soil1(ihru)%hsta(ly)%p` | Only when `bsn_cc%cswat == 0`. | Initializes stable humus phosphorus from its carbon mass and the configured humus C:P ratio. |
| `org_frac%frac_not_seq` | Only when `bsn_cc%cswat == 2`; `org_frac%frac_not_seq` is set from `org_frac%frac_seq`. | Stores the non-sequestered fraction of initial carbon, used to partition residue pools from the sequestered humus pools. |
| `soil1(ihru)%hp(ly)%m` | Only when `bsn_cc%cswat == 2`. | Initializes passive humus mass as the sequestered fraction multiplied by the passive-humus share of total organic matter. |
| `soil1(ihru)%hp(ly)%c` | Only when `bsn_cc%cswat == 2`. | Initializes passive humus carbon from the sequestered carbon fraction and the passive-humus share. |
| `soil1(ihru)%hp(ly)%n` | Only when `bsn_cc%cswat == 2`. | Initializes passive humus nitrogen from passive humus carbon using a 10:1 C:N ratio. |
| `soil1(ihru)%hp(ly)%p` | Only when `bsn_cc%cswat == 2`. | Initializes passive humus phosphorus from passive humus carbon using an 80:1 C:P ratio. |
| `soil1(ihru)%hs(ly)%m` | Only when `bsn_cc%cswat == 2`. | Initializes slow humus mass using either the default slow-humus fraction or the Mathers texture-based estimate. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:1.1.1 | Initial NO3 concentration by depth | $NO3_{conc,z}=7*exp(\frac{-z}{1000})$ | dep_frac=Exp(-exp_co*depth); default no3=7.*dep_frac (mg/kg). Eq uses 7*exp(-z/1000); code uses configurable exp_co. |
| 3:1.1.2 | Initial humus organic N from organic C | $orgN_{hum,ly}=10^4*(\frac{orgC_{ly}}{14})$ | tot%n=tot%c/10 (C:N=10). Theory formula uses C:N≈14; code uses 10. Conceptual match, different constant. |
| 3:1.1.4 | Stable organic N pool (cswat=0 path) | $orgN_{sta,ly}=orgN_{hum,ly}*(1-fr_{actN})$ | hsta%n=(1-frac_hum_active)*tot%c/hum_c_n; implements orgN_sta=(1-fr_actN)*orgN_hum via C:N ratio. |
| 3:1.1.5 | Fresh organic N in surface residue | $orgN_{frsh,surf}=0.0015*rsd_{surf}$ | orgN_frsh=0.0015*rsd_surf is a residue initialization formula; not computed in soil_nutcarb_init. Likely in plant/residue init code. |
| 3:1.1.6 | Unit conversion conc_N to kg/ha | $\frac{conc_N*\rho_b*depth_{ly}}{100}=\frac{kgN}{ha}$ | conv_wt=bd*thick/100; no3(kg/ha)=no3(mg/kg)*conv_wt. Matches formula conc*rho_b*depth/100=kg/ha. |
| 3:2.1.1 | Active mineral P pool init from PSP | $minP_{act,ly}=P_{solution,ly}*\frac{1-pai}{pai}$ | mp%act=mp%lab*(1-psp)/psp; exact match for minP_act=P_solution*(1-pai)/pai with pai=psp. |
| 3:2.1.2 | Stable mineral P = 4 * active mineral P | $minP_{sta,ly}=4*minP_{act,ly}$ | mp%sta=4.*mp%act in the else branch (non-dynamic PSP). Exact match. |
| 3:2.1.3 | Humus organic P from humus organic N (C:P=80) | $orgP_{hum,ly}=0.125*orgN_{hum,ly}$ | Verified against SWAT+ 62.0.0 (soil_nutcarb_init.f90:154). hp%p = hp%c/80.` (C:P 80:1), not theory's `0.125·orgN |
| 3:2.1.4 | Fresh organic P in surface residue | $orgP_{frsh,surf}=0.0003*rsd_{surf}$ | Verified against SWAT+ 62.0.0 (soil_nutcarb_init.f90). fresh org-P from residue C:P pools, not `0.0003·rsd |

## Lineage

Three resolved commits changed `soil_nutcarb_init`. The earliest resolved change, `6d425fb`, removed hard-coded CENTURY fraction assignments and switched the code to use the imported `org_frac` defaults, also commenting out direct residue assignments so the routine could compute residue pools from the totals instead. `d504f1c` corrected the CENTURY fraction references so passive, slow, and microbial pools use the `org_frac%...` members consistently rather than bare names. `5323b15` added the non-lignin residue pool calculations from the structural residue pool. `69a6607` fixed the logical comparisons for `org_frac%mathers_method`, and `bc7755a` changed the CENTURY sequestered fraction setup so `frac_not_seq` is derived from `org_frac%frac_seq` instead of a fixed literal.

- `6d425fb` moved CENTURY initialization away from hard-coded fraction literals and residue copies, making the routine use imported organic-fraction controls and computed residue pools.
- `d504f1c` fixed the passive/slow/microbial pool formulas to read `org_frac%frac_hum_passive`, `org_frac%frac_hum_slow`, and `org_frac%frac_hum_microb` from the carbon module.
- `5323b15` added explicit non-lignin residue initialization by subtracting lignin mass, carbon, nitrogen, and phosphorus from the structural residue pool.
- `69a6607` corrected the `mathers_method` comparisons to use logical equivalence operators, ensuring the Mathers slow-humus branch is selected correctly.
- `bc7755a` changed the CENTURY non-sequestered fraction to derive from `org_frac%frac_seq`, so the residue share now follows the configured sequestered-carbon fraction.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'soil_nutcarb_init' has no extracted documentation comment.
- algorithm_steps revised: condensed the draft into nine source-backed steps matching the actual control flow and layer loops.
- Source parsing treats `soil`, `hru`, `sol_plt_ini`, `soil1`, `cbn`, `phys`, `mn`, `mp`, `hact`, `hsta`, `hp`, `hs`, `microb`, `meta`, `str`, `lig`, `nonlig`, `seq`, `max`, `Exp`, and `log` as callee-like symbols, but several are module data components or intrinsic functions rather than executable subroutines.
- `tillage_data_module` is used only for `bmix_depth` and `bmix_eff` in the final layer mixing assignment; no separate type or derived-type member was resolved from the extracted snippets.
