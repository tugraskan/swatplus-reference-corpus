---
kind: procedure
symbol: structure_set_parms
title: structure_set_parms
status: filled
source_hash: a61bf22eece6e8dd
version_label: SWAT+ 62.0.0
args:
  str_name: Name of the structural practice to configure (`tiledrain`, `fstrip`, `grassww`,
    `user_def`, or `septic`); selects which branch of the dispatcher runs.
  istr: Index into the relevant operation/structure database (e.g. `sdr`, `filtstrip_db`,
    `grwaterway_db`, `bmpuser_db`) supplying the parameter values to apply.
  j: HRU number whose land-management fields are being set.
locals:
  jj: Soil-layer counter used in the tiledrain branch to find which layer contains the drain
    depth.
  tch: Time of concentration for grassed-waterway channel flow (hr), computed from waterway
    length, roughness, and slope.
  b: Trial bottom width (m) of the grassed-waterway trapezoidal channel, used to test whether
    the entered width/depth are feasible with an 8:1 side slope.
uses:
  mgt_operations_module: Supplies the structural-practice databases (`filtstrip_db`, `grwaterway_db`,
    `bmpuser_db`) whose records provide the parameter values copied onto the HRU.
  hru_module: Provides the target HRU object and management fields (`hru`, `sdr`, `tc_gwat`,
    `t_ov`, `iseptic`) that this routine writes the structural parameters into.
  soil_module: Provides the soil profile (`soil(j)%nly`, `soil(j)%phys(jj)%d`) used to locate
    which soil layer the drainage tile sits in.
---

<!-- facts:header -->

Sets structural land-management parameters on a specific HRU from a selected operation record. It handles tiledrain, filter strip, grassed waterway, user-defined BMP, and septic settings.

## Bottom Line

`structure_set_parms` copies parameter values from the operation databases into the target HRU’s management fields, then applies a few defaults and feasibility checks. For tiledrain it assigns the drainage profile and determines the soil layer and lag response; for filter strips, grassed waterways, and BMPs it transfers the operation settings into `hru(j)%lumv`, and for septic it records which septic definition applies to the HRU.

This matters because later HRU initialization and land-phase simulation logic depend on these fields being populated before routing, drainage, and BMP behavior are calculated. In particular, the grassed-waterway branch also computes a channel time-of-concentration term and calls `ttcoef_wway` to finish waterway coefficient setup.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Runs during HRU/structure initialization and from scheduled management actions (`structure_init`, `proc_hru`, `actions`). It translates a structural-practice database record into concrete HRU management fields before the land-phase simulation uses them. Tile-drain, filter-strip, grassed-waterway, user BMP, and septic settings written here are later read by drainage, surface-runoff/filter, waterway routing, BMP removal, and septic routines.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Dispatch on structure type | Enters a `select case (str_name)` that routes to one of five structural-practice branches: `tiledrain`, `fstrip`, `grassww`, `user_def`, or `septic`. |
| 2. Tile drain setup | Copies the `sdr(istr)` tile-drain record onto the HRU, finds the soil layer containing the drain depth (`ldrain`), and sets the tile travel time `tile_ttime = 1. - Exp(-24./lag)` when a drain layer and positive lag exist (else 0). |
| 3. Filter strip setup | Copies filter-strip parameters from `filtstrip_db(istr)` and clamps them to valid ranges (vfsratio 0-300, vfscon 0.1-0.95, vfsch 0-0.95). |
| 4. Grassed waterway setup | For a valid `istr`, sets the grassed-waterway flag and copies geometry from `grwaterway_db(istr)`, applies defaults (e.g. Manning's n 0.35, length, depth, slope, sediment coefficient), computes the waterway time of concentration `tc_gwat(j) = tch + t_ov(j)`, checks channel feasibility for an 8:1 trapezoidal section, and calls `ttcoef_wway(j)`. |
| 5. User BMP setup | Sets the user-BMP flag and copies the sediment, particulate/soluble P, particulate/soluble N, and bacteria removal fractions from `bmpuser_db(istr)`. |
| 6. Septic setup | Stores the septic operation index on the HRU: `iseptic(j) = istr`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:mgt_operations_module] | `filtstrip_db, grwaterway_db, bmpuser_db` | `filtstrip_db(istr)%vfsi, filtstrip_db(istr)%vfsratio, filtstrip_db(istr)%vfscon, filtstrip_db(istr)%vfsch, grwaterway_db(istr)%grwat_n, grwaterway_db(istr)%grwat_spcon, grwaterway_db(istr)%grwat_d, grwaterway_db(istr)%grwat_w, grwaterway_db(istr)%grwat_l, grwaterway_db(istr)%grwat_s, bmpuser_db(istr)%bmp_sed, bmpuser_db(istr)%bmp_pp, bmpuser_db(istr)%bmp_sp, bmpuser_db(istr)%bmp_pn, bmpuser_db(istr)%bmp_sn, bmpuser_db(istr)%bmp_bac` |
| [sym:hru_module] | `hru, sdr, tc_gwat, t_ov, iseptic` | `hru(j)%sdr, hru(j)%lumv%sdr_dep, sdr(istr)%depth, hru(j)%lumv%ldrain, sdr(istr)%lag, hru(j)%lumv%tile_ttime, hru(j)%lumv%vfsi, hru(j)%lumv%vfsratio, hru(j)%lumv%vfscon, hru(j)%lumv%vfsch, hru(j)%lumv%ngrwat, hru(j)%lumv%grwat_i, hru(j)%lumv%grwat_n, hru(j)%lumv%grwat_spcon, hru(j)%lumv%grwat_d, hru(j)%lumv%grwat_w, hru(j)%lumv%grwat_l, hru(j)%lumv%grwat_s, hru(j)%km, hru(j)%topo%slope, hru(j)%lumv%bmp_flag, hru(j)%lumv%bmp_sed, hru(j)%lumv%bmp_pp, hru(j)%lumv%bmp_sp, hru(j)%lumv%bmp_pn, hru(j)%lumv%bmp_sn, hru(j)%lumv%bmp_bac` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(jj)%d` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hru(j)%sdr` | In the `tiledrain` branch (`str_name == "tiledrain"`). | Copies the entire tile-drain parameter set `sdr(istr)` onto the HRU. |
| `hru(j)%lumv%sdr_dep` | In the `tiledrain` branch (`str_name == "tiledrain"`). | Sets the tile-drain installation depth from the drain record. |
| `hru(j)%lumv%ldrain` | In the `tiledrain` branch (`str_name == "tiledrain"`). Loops soil layers when `sdr_dep > 0`, else set to 0. | Identifies the soil layer that contains the tile-drain depth (the deepest layer shallower than `sdr_dep`), or 0 when there is no drain. |
| `hru(j)%lumv%tile_ttime` | In the `tiledrain` branch (`str_name == "tiledrain"`). When `ldrain > 0` and `sdr(istr)%lag > 0.01`, else 0. | Tile-drain travel-time release fraction derived from the drain lag. |
| `hru(j)%lumv%vfsi` | In the `fstrip` (filter strip) branch (`str_name == "fstrip"`). | Copies the filter-strip indicator/flag from `filtstrip_db(istr)`. |
| `hru(j)%lumv%vfsratio` | In the `fstrip` (filter strip) branch (`str_name == "fstrip"`). Clamped to 0-300. | Copies the ratio of field area to filter-strip area from `filtstrip_db(istr)`. Clamped to 0-300. |
| `hru(j)%lumv%vfscon` | In the `fstrip` (filter strip) branch (`str_name == "fstrip"`). Clamped to 0.1-0.95. | Copies the fraction of flow through the most concentrated 10% of the strip from `filtstrip_db(istr)`. Clamped to 0.1-0.95. |
| `hru(j)%lumv%vfsch` | In the `fstrip` (filter strip) branch (`str_name == "fstrip"`). Clamped to 0-0.95. | Copies the fraction of flow that is channelized (bypasses the strip) from `filtstrip_db(istr)`. Clamped to 0-0.95. |
| `hru(j)%lumv%ngrwat` | In the `grassww` branch (set before the `istr > 0` guard). | Stores the grassed-waterway structure index on the HRU. |
| `hru(j)%lumv%grwat_i` | In the `grassww` (grassed waterway) branch, when `istr > 0`. | Sets the grassed-waterway active flag to 1. |
| `hru(j)%lumv%grwat_n` | In the `grassww` (grassed waterway) branch, when `istr > 0`. Defaults to 0.35 if not positive. | Copies the Manning's roughness n from `grwaterway_db(istr)`. Defaults to 0.35 if not positive. |
| `hru(j)%lumv%grwat_spcon` | In the `grassww` (grassed waterway) branch, when `istr > 0`. Defaults to 0.005 if not positive. | Copies the sediment transport coefficient from `grwaterway_db(istr)`. Defaults to 0.005 if not positive. |
| `hru(j)%lumv%grwat_d` | In the `grassww` (grassed waterway) branch, when `istr > 0`. Defaults to 3/64 of width if not positive (or if 8:1 geometry is infeasible). | Copies the channel depth from `grwaterway_db(istr)`. Defaults to 3/64 of width if not positive (or if 8:1 geometry is infeasible). |
| `hru(j)%lumv%grwat_w` | In the `grassww` (grassed waterway) branch, when `istr > 0`. | Copies the channel width from `grwaterway_db(istr)`. |
| `hru(j)%lumv%grwat_l` | In the `grassww` (grassed waterway) branch, when `istr > 0`. Defaults to sqrt(HRU area in km2) if not positive. | Copies the waterway length from `grwaterway_db(istr)`. Defaults to sqrt(HRU area in km2) if not positive. |
| `hru(j)%lumv%grwat_s` | In the `grassww` (grassed waterway) branch, when `istr > 0`. Defaults to 0.75 x HRU slope if not positive. | Copies the waterway slope from `grwaterway_db(istr)`. Defaults to 0.75 x HRU slope if not positive. |
| `tc_gwat(j)` | In the `grassww` (grassed waterway) branch, when `istr > 0`. | Grassed-waterway time of concentration: channel travel time plus overland-flow time. |
| `hru(j)%lumv%bmp_flag` | In the `user_def` branch (`str_name == "user_def"`). | Sets the user-BMP active flag to 1. |
| `hru(j)%lumv%bmp_sed` | In the `user_def` branch (`str_name == "user_def"`). | Copies the sediment removal efficiency from `bmpuser_db(istr)`. |
| `hru(j)%lumv%bmp_pp` | In the `user_def` branch (`str_name == "user_def"`). | Copies the particulate phosphorus removal efficiency from `bmpuser_db(istr)`. |
| `hru(j)%lumv%bmp_sp` | In the `user_def` branch (`str_name == "user_def"`). | Copies the soluble phosphorus removal efficiency from `bmpuser_db(istr)`. |
| `hru(j)%lumv%bmp_pn` | In the `user_def` branch (`str_name == "user_def"`). | Copies the particulate nitrogen removal efficiency from `bmpuser_db(istr)`. |
| `hru(j)%lumv%bmp_sn` | In the `user_def` branch (`str_name == "user_def"`). | Copies the soluble nitrogen removal efficiency from `bmpuser_db(istr)`. |
| `hru(j)%lumv%bmp_bac` | In the `user_def` branch (`str_name == "user_def"`). | Copies the bacteria removal efficiency from `bmpuser_db(istr)`. |

## File I/O

<!-- facts:io -->


## Lineage

`structure_set_parms.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `structure_set_parms.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'structure_set_parms' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
