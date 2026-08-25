---
kind: procedure
symbol: res_initial
title: res_initial
status: filled
source_hash: 44047e904a82efcf
version_label: SWAT+ 62.0.0
locals:
  ires: Loop index over reservoir objects. It identifies the current reservoir being initialized
    and indexes all reservoir-related arrays.
  lnvol: Temporary log-volume difference used when solving the surface-area exponent `br2`.
    It guards against a very small denominator in the log-ratio calculation.
  resdif: Temporary difference between emergent and principal reservoir volumes from `res_hyd`.
    It is used with the surface-area difference to decide whether the normal exponent calculation
    can be used.
  i: Index into the reservoir initial-condition table `res_init`. It is obtained from `res_dat(idat)%init`
    and then used to select the source records for organics, pesticides, pathogens, salt,
    and constituent initial values.
  idat: Index into `res_dat`, the reservoir property/data table. It is used to find which
    initialization records and external input files belong to the current reservoir.
  icon: Index of the selected external salt or constituent database record. It is loaded from
    `res_dat(idat)%salt` or `res_dat(idat)%cs` before reading initial concentrations.
  init: Index into `res_init` for the current reservoir's chosen initial-condition bundle.
    It is reused for the organics, pesticide, pathogen, salt, and constituent initial sources.
  ipest: Loop counter over simulated pesticide species. It steps through each pesticide concentration
    to initialize reservoir water and benthic masses.
  ipath: Loop counter over simulated pathogen species. It steps through each pathogen concentration
    to initialize reservoir water and benthic masses.
  isalt: Loop counter over simulated salt ions. It is used to copy initial salt concentrations
    and convert them to mass.
  ipest_db: Index into the pesticide database `pestdb`. It maps the simulation pesticide index
    to the correct database entry so the molecular weight can be used for mixing velocity.
uses:
  reservoir_module: The reservoir object array is the main target of this routine. `res_initial`
    writes the reservoir object number, geometry, weir height, lag parameters, Hanazaki memory
    fields, and aquatic mixing coefficients into `res_ob(ires)` so later reservoir routing
    has consistent starting state.
  maximum_data_module: '`maximum_data_module` matters because `sp_ob%res` controls how many
    reservoir objects exist and `sp_ob1%res` provides the first reservoir object number. Those
    values determine the loop bounds and the object-number mapping assigned to each `res_ob(ires)%ob`.'
  reservoir_data_module: This module provides the reservoir input tables that link each reservoir
    to its geometry, operational start date, and initial-condition records. `res_initial`
    uses `res_hyd` for geometry and activation timing, `res_dat` to find the right initialization
    bundles, `res_init` to choose the initial-condition datasets, and `res_sed` for sediment
    density needed in pesticide mixing velocity.
  hydrograph_module: The hydrograph state holds the mutable reservoir water-object arrays
    that this routine seeds. `res_initial` writes the starting water volume into `res(ires)`,
    copies the reset reference into `res_om_init(ires)`, and uses the resulting `res(ires)%flo`
    when converting concentration values to mass and surface area.
  constituent_mass_module: This module defines the reservoir water and benthic constituent
    arrays plus the counts of pesticides, pathogens, salts, and other constituents. `res_initial`
    needs those counts to loop over each species and the arrays to store the initial water-column
    and benthic concentrations and masses.
  pesticide_data_module: The pesticide database supplies molecular weight for each pesticide.
    `res_initial` uses `pestdb(ipest_db)%mol_wt` to compute the reservoir aquatic mixing velocity
    `aq_mix`, so pesticide transport and exchange can start from the correct reservoir-specific
    mixing value.
  water_body_module: The reservoir water-body state stores surface area. `res_initial` computes
    `res_wat_d(ires)%area_ha` from the initialized reservoir volume and shape parameters so
    later reservoir evaporation, precipitation, and water-surface calculations have the starting
    area.
  res_salt_module: The salt module holds the external salt-reservoir initial concentration
    table. `res_initial` reads `res_salt_data(icon)%c_init(isalt)` to seed reservoir salt
    concentrations when the reservoir is configured to use a salt initialization file.
  res_cs_module: The constituent-state module holds the external reservoir constituent initial
    concentrations. `res_initial` reads `res_cs_data(icon)%c_seo4`, `res_cs_data(icon)%c_seo3`,
    and `res_cs_data(icon)%c_born` to seed selenium and boron concentrations in reservoir
    water.
---

<!-- facts:header -->

Initializes reservoir object metadata, geometry, and starting water-quality state. It also derives the reservoir surface-area shape coefficients used later in routing.

## Bottom Line

res_initial walks every reservoir object and fills the reservoir-side state needed before simulation begins. It copies geometry and operational setup from the read-in reservoir data, allocates and zeros the Hanazaki memory arrays, and computes the surface-area curve parameters `br1` and `br2` from the principal and emergency spillway values.

For reservoirs that are operational at the current simulation start date, it also seeds the initial organic-mineral hydrology object, pesticide/pathogen/salt/constituent concentrations, and initial surface area. Those values become the starting conditions used by later reservoir routing and water-quality calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during reservoir setup after `proc_res` has allocated reservoir structures, built reservoir objects, and read reservoir and salt/constituent input data. Its results feed all later reservoir routing and water-quality behavior because they define the starting geometry, operation timing, volumes, surface area, and initial chemical/biological state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over each reservoir object | For every reservoir, assign its object number, convert principal and emergency volumes from ha-m to m3, copy principal and emergency surface areas, and compute the initial weir height from principal volume and area. |
| 2. Initialize Hanazaki-style reservoir memory fields | Set the annual inflow and irrigation-demand summary variables to zero, fix the memory length at five years, allocate the monthly and daily history arrays, zero them, and clear irrigation tracking state. |
| 3. Load lag parameters and compute surface-area coefficients | Copy the input lag parameters into `lag_up` and `lag_down`, then derive `br2` from the log ratio of emergency and principal surface areas to volumes when the reservoir geometry is valid. Cap `br2` at 0.9 and compute `br1` from the corresponding surface-area relation, or fall back to the capped/default branch when the geometry is not suitable. |
| 4. Process only reservoirs that are operational at simulation start | For each reservoir, test whether the current simulation time is at or after the reservoir operational start year and month. Only those reservoirs receive initial water and constituent states; otherwise the reservoir is left at zero-volume startup conditions. |
| 5. Initialize organic-mineral water state and convert it to mass | Select the reservoir's initialization record, copy the organic-mineral water state from `om_init_water(init)` into `res(ires)`, convert it with `res_convert_mass` using the reservoir principal volume, and save the converted state in `res_om_init(ires)` for later reset or calibration use. |
| 6. Initialize pesticide water and benthic concentrations | Loop over the configured pesticide species, map each one to the pesticide database, copy initial water and benthic concentrations from `pest_water_ini(init)`, and compute aquatic mixing velocity from molecular weight and sediment bulk density. |
| 7. Initialize pathogen water and benthic concentrations | Loop over pathogen species and copy initial water-column and benthic concentrations from `path_water_ini(init)` into the reservoir water and benthic state arrays. |
| 8. Compute initial reservoir surface area from volume and shape | Use the just-computed shape parameters and the initialized reservoir flow/volume state to calculate the starting surface area in hectares and store it in `res_wat_d(ires)%area_ha`. |
| 9. Initialize salts when salt data are enabled | If salts are configured, select the salt database record for the reservoir and either copy each initial salt concentration from `res_salt_data(icon)%c_init` and convert it to mass, or set both concentration and mass to zero when no valid salt dataset is available. |
| 10. Initialize other constituents when constituent data are enabled | If other constituents are configured, select the constituent database record and either copy selenate, selenite, and boron initial concentrations from `res_cs_data(icon)` and convert them to mass, or clear the concentrations and masses to zero when no valid dataset is available. |
| 11. Close the reservoir file stream and return | Close file unit 105 after initialization work is finished, then return to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_module] | `res_ob` | `res_ob(ires)%ob, res_ob(ires)%evol, res_ob(ires)%pvol, res_ob(ires)%esa, res_ob(ires)%psa, res_ob(ires)%weir_hgt, res_ob(ires)%I_mean, res_ob(ires)%S_ini, res_ob(ires)%N_memory, res_ob(ires)%I_mon_past, res_ob(ires)%daily_inflow_array, res_ob(ires)%c_ratio, res_ob(ires)%d_mean, res_ob(ires)%d_mon_past, res_ob(ires)%daily_demand_array, res_ob(ires)%d_irrig_day, res_ob(ires)%irrig_track, res_ob(ires)%lag_up, res_ob(ires)%lag_down, res_ob(ires)%br2, res_ob(ires)%br1, res_ob(ires)%props, res_ob(ires)%aq_mix(ipest)` |
| [sym:maximum_data_module] | `sp_ob, sp_ob1` | `sp_ob%res, sp_ob1%res` |
| [sym:reservoir_data_module] | `res_hyd, res_dat, res_init, res_sed` | `res_hyd(ires)%evol, res_hyd(ires)%pvol, res_hyd(ires)%esa, res_hyd(ires)%psa, res_hyd(ires)%br1, res_hyd(ires)%br2, res_hyd(ires)%iyres, res_hyd(ires)%mores, res_dat(idat)%init, res_init(i)%org_min, res_init(i)%pest, res_sed(ires)%bd, res_init(i)%path, res_dat(idat)%salt, res_dat(idat)%cs` |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, res, om_init_water, res_om_init` | `sp_ob%res, sp_ob1%res, res(ires)%flo` |
| [sym:constituent_mass_module] | `cs_db, res_water, pest_water_ini, res_benthic, path_water_ini` | `cs_db%num_pests, cs_db%pest_num(ipest), res_water(ires)%pest(ipest), pest_water_ini(init)%water(ipest), res_benthic(ires)%pest(ipest), pest_water_ini(init)%benthic(ipest), cs_db%num_paths, res_water(ires)%path(ipath), path_water_ini(init)%water(ipath), res_benthic(ires)%path(ipath), path_water_ini(init)%benthic(ipath), cs_db%num_salts, res_water(ires)%saltc(isalt), res_water(ires)%salt(isalt), cs_db%num_cs, res_water(ires)%csc(1), res_water(ires)%cs(1), res_water(ires)%csc(2), res_water(ires)%cs(2), res_water(ires)%csc(3), res_water(ires)%cs(3)` |
| [sym:pesticide_data_module] | `pestdb` | `pestdb(ipest_db)%mol_wt` |
| [sym:water_body_module] | `res_wat_d` | `res_wat_d(ires)%area_ha` |
| [sym:res_salt_module] | `res_salt_data` | `res_salt_data(icon)%c_init(isalt)` |
| [sym:res_cs_module] | `res_cs_data` | `res_cs_data(icon)%c_seo4, res_cs_data(icon)%c_seo3, res_cs_data(icon)%c_born` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `res_ob(ires)%ob` | Always, inside the first reservoir loop. | `res_ob(ires)%ob` is assigned the reservoir object number `sp_ob1%res + ires - 1`, mapping the loop index to the actual reservoir object id used elsewhere in the model. |
| `res_ob(ires)%evol` | Always, inside the first reservoir loop. | `res_ob(ires)%evol` stores the emergency spillway volume converted from ha-m to m3, so later reservoir geometry and shape calculations use model volume units. |
| `res_ob(ires)%pvol` | Always, inside the first reservoir loop. | `res_ob(ires)%pvol` stores the principal spillway volume converted from ha-m to m3, which is then used to compute weir height and the area-volume curve. |
| `res_ob(ires)%esa` | Always, inside the first reservoir loop. | `res_ob(ires)%esa` is copied from the reservoir hydrology table and becomes the emergency spillway surface area used in shape-parameter calculations. |
| `res_ob(ires)%psa` | Always, inside the first reservoir loop. | `res_ob(ires)%psa` is copied from the reservoir hydrology table and becomes the principal spillway surface area used in shape-parameter calculations. |
| `res_ob(ires)%weir_hgt` | Always, inside the first reservoir loop, after principal volume and surface area are available. | `res_ob(ires)%weir_hgt` is computed as principal volume divided by principal area converted to meters, giving the starting weir height above the reservoir bottom. |
| `res_ob(ires)%I_mean` | Always, during Hanazaki-state initialization in the first loop. | `res_ob(ires)%I_mean` is reset to zero so the reservoir starts with no accumulated annual inflow history. |
| `res_ob(ires)%S_ini` | Always, during Hanazaki-state initialization in the first loop. | `res_ob(ires)%S_ini` is set to the larger of emergency and principal volume, which serves as the initial storage baseline for the operational-year calculations. |
| `res_ob(ires)%N_memory` | Always, during Hanazaki-state initialization in the first loop. | `res_ob(ires)%N_memory` is fixed at 5 years, determining the length of the rolling inflow and irrigation history arrays. |
| `res_ob(ires)%I_mon_past` | Always, after allocating the inflow history array. | `res_ob(ires)%I_mon_past` is allocated to 12 times the memory length and filled with zeros so the reservoir starts with no prior monthly inflow history. |
| `res_ob(ires)%daily_inflow_array` | Always, after allocating the daily inflow array. | `res_ob(ires)%daily_inflow_array` is allocated with one element and initialized to zero, creating the current-month inflow storage used by later updates. |
| `res_ob(ires)%c_ratio` | Always, during Hanazaki-state initialization in the first loop. | `res_ob(ires)%c_ratio` is set to the default 0.51 capacity ratio used by the reservoir operational method. |
| `res_ob(ires)%d_mean` | Always, during irrigation-state initialization in the first loop. | `res_ob(ires)%d_mean` is reset to zero so the reservoir starts with no annual irrigation-demand average. |
| `res_ob(ires)%d_mon_past` | Always, after allocating the irrigation-demand history array. | `res_ob(ires)%d_mon_past` is allocated and zeroed to hold the rolling monthly irrigation-demand history. |
| `res_ob(ires)%daily_demand_array` | Always, after allocating the daily irrigation-demand array. | `res_ob(ires)%daily_demand_array` is allocated with one element and set to zero for the current-month demand history. |
| `res_ob(ires)%d_irrig_day` | Always, during irrigation-state initialization in the first loop. | `res_ob(ires)%d_irrig_day` is reset to zero so no daily irrigation demand carries into the start of simulation. |
| `res_ob(ires)%irrig_track` | Always, during irrigation-state initialization in the first loop. | `res_ob(ires)%irrig_track` is reset to zero to clear any prior irrigation tracking state. |
| `res_ob(ires)%lag_up` | Always, during the first loop. | `res_ob(ires)%lag_up` is copied from `res_hyd(ires)%br1`, using the input reservoir coefficient as the upstream lag parameter. |
| `res_ob(ires)%lag_down` | Always, during the first loop. | `res_ob(ires)%lag_down` is copied from `res_hyd(ires)%br2`, using the input reservoir coefficient as the downstream lag parameter. |
| `res_ob(ires)%br2` | When the reservoir geometry is valid and the log-volume ratio can be used, or when the routine falls back to the default branch. | `res_ob(ires)%br2` is computed from the log ratio of surface areas and volumes, but capped at 0.9; if the geometry is invalid it is set directly to 0.9. |
| `res_ob(ires)%br1` | After `br2` is computed or capped. | `res_ob(ires)%br1` is derived from the surface-area/volume relation using either the computed exponent or the capped 0.9 branch, providing the coefficient for the area-volume curve. |
| `res(ires)` | Only when the current simulation time is at or after the reservoir operational start date. | `res(ires)` receives the initial organic-mineral water state and is converted to mass units, so the reservoir starts with a fully initialized water-quality state rather than a zero-volume placeholder. |
| `res_om_init(ires)` | Only when the current simulation time is at or after the reservoir operational start date. | `res_om_init(ires)` stores a copy of the initial organic-mineral reservoir state as a reset/reference value for later soft calibration or reinitialization. |
| `res_water(ires)%pest(ipest)` | Only when the reservoir has pesticide initialization enabled and a valid pesticide initialization table is available. | `res_water(ires)%pest(ipest)` is filled with the starting pesticide concentration for each simulated pesticide species, establishing the initial reservoir-water pesticide mass state after later conversion. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 8:1.1.3 | Reservoir SA-V exponent expsa | $expsa=\frac{log_{10}(SA_{em})-log_{10}(SA_{pr})}{log_{10}(V_{em})-log_{10}(V_{pr})}$ | br2=(Log10(esa)-Log10(psa))/(Log10(evol)-Log10(pvol)); exact match for expsa=(log10(SA_em)-log10(SA_pr))/(log10(V_em)-log10(V_pr)). Capped at 0.9 (line 72-74). |
| 8:1.1.4 | Reservoir SA-V coefficient beta_sa | $\beta_{sa}=(\frac{SA_{em}}{V_{em}})^{expsa}$ | br1=(esa/evol)**br2 (line 76) or (psa/pvol)**0.9 when br2 capped (line 74). Matches beta_sa=(SA_em/V_em)^expsa; alternate form when exponent hits 0.9 cap. |

## Lineage

`res_initial.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `d3c291b` (2026-01-31, "integrate new reservoir routines"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `res_initial.f90` are listed.

- `d3c291b` (2026-01-31) — integrate new reservoir routines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `96c2bfb` (2024-03-24) — Mar 21 status
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_initial' has no extracted documentation comment.
- lineage unavailable: no commits were resolved for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
