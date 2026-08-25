---
kind: procedure
symbol: soil_phys_init
title: soil_phys_init
status: filled
source_hash: a9f02b5fdaf4515a
version_label: SWAT+ 62.0.0
args:
  isol: Selects which soil database record in `sol` is initialized. The routine reads and
    updates `sol(isol)` and all of its layer/profile fields in place.
locals:
  j: Loop counter over soil layers within the selected soil profile. It is reset and reused
    for the per-layer defaulting and water-balance calculations.
  nly: Number of layers in `sol(isol)%s%nly`; it controls how many layers are processed in
    each loop.
  sumpor: Accumulator for profile porosity depth in millimeters, built as the sum of each
    layer's porosity times thickness.
  pormm: Per-layer porosity depth contribution in millimeters (`por * thick`), added into
    `sumpor`.
  nota: Fallback saturated hydraulic conductivity assigned when the hydrologic soil group
    is not A, B, C, or D.
  a: Default conductivity value used when the soil hydrologic group is A.
  b: Default conductivity value used when the soil hydrologic group is B.
  c: Default conductivity value used when the soil hydrologic group is C.
  d: Default conductivity value used when the soil hydrologic group is D.
  drpor: Drainable porosity for the current layer, computed as total porosity minus the upper-water-content
    threshold.
  sa: Top-soil sand fraction converted from percent to a unit fraction for detached-sediment
    calculations.
  cl: Top-soil clay fraction converted from percent to a unit fraction for detached-sediment
    calculations.
  si: Top-soil silt fraction converted from percent to a unit fraction for detached-sediment
    calculations.
  depth_prev: Depth to the bottom of the previous layer; used to derive each layer thickness
    from cumulative depth.
uses:
  soil_module: '`soil_module` defines the `sol` database and the nested soil profile, physical-layer,
    and layer-output components that this routine reads and updates. The entire procedure
    operates by initializing those fields in place, so the module provides both the target
    state and the type definitions that make the assignments possible.'
  basin_module: '`sol` is the actual soil database entry being initialized. Its nested profile
    and layer fields hold the initial conditions for conductivity, moisture storage, crack
    volume, and profile averages that this routine computes.'
  time_module: '`time%step` determines whether the routine applies the subdaily texture correction
    to the first layer''s sand fraction. That correction only matters when the model is running
    with more than one timestep per day.'
---

<!-- facts:header -->

Initializes and bounds the soil physical properties for one soil database entry. It derives layer water storage, porosity, crack behavior, and related profile totals used by later hydrology calculations.

## Bottom Line

`soil_phys_init` prepares the soil-property record `sol(isol)` for simulation use. It fills in default values when inputs are missing or out of range, computes layer- and profile-scale water storage terms, and derives texture-based detached-sediment fractions and crack-volume terms.

The routine matters because later soil-water and routing behavior depends on the values it sets: saturated conductivity, wilting point, field capacity, porosity, profile water totals, water-table factor, and subdaily infiltration texture corrections.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`soils_init` calls `soil_phys_init(isol)` after the soil database has been allocated and populated, once for each soil record. The results feed later HRU soil assignment and downstream hydrology because this routine establishes the physical parameters and profile water-storage totals that other soil and routing routines rely on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Bound profile-level defaults and determine layer count | Clamp albedo and anion exclusion to valid ranges, then read the selected soil profile's layer count into `nly`. |
| 2. Loop through each soil layer to fill missing inputs | For each layer, assign default conductivity by hydrologic group, constrain bulk density, AWC, and rock content, and fill missing layer pH and calcium values. |
| 3. Compute water contents and porosity by layer | Revisit the layers to compute wilting point, upper-water threshold, porosity, drainable porosity, and the variable water-table factor. |
| 4. Derive detached-sediment fractions from topsoil texture | Use the first layer's sand, clay, and silt percentages to compute detached sand, silt, clay, small-aggregate, and large-aggregate fractions, then renormalize if the large-aggregate fraction goes negative. |
| 5. Build thickness-based layer storage and saturation terms | Reset running depth, compute each layer thickness, then calculate porosity storage, upper-limit storage, field-capacity storage, saturation storage, hydraulic conductivity factor, wilting-point storage, crack depth, and crack volume for each layer. |
| 6. Finish profile totals and water-table fields | Store profile water-at-water-table values, estimate water-table depth when the initial field-capacity fraction is above 1, and compute average porosity and average bulk density for the soil profile. |
| 7. Apply subdaily sand correction when needed | If the model is running with more than one timestep per day, recompute the first layer's sand fraction from clay and silt. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:soil_module] | `sol` | `sol(isol)%s%alb, sol(isol)%s%anion_excl, sol(isol)%s%nly, sol(isol)%phys(j)%k, sol(isol)%s%hydgrp, sol(isol)%phys(j)%bd, sol(isol)%phys(j)%awc, sol(isol)%phys(j)%rock, sol(isol)%ly(j)%cal, sol(isol)%ly(j)%ph, sol(isol)%phys(j)%wp, sol(isol)%phys(j)%clay, sol(isol)%phys(j)%up, sol(isol)%phys(j)%por, sol(isol)%ly(j)%vwt, sol(isol)%phys(1)%sand, sol(isol)%phys(1)%clay, sol(isol)%phys(1)%silt, sol(isol)%s%det_san, sol(isol)%s%det_sil, sol(isol)%s%det_cla, sol(isol)%s%det_sag, sol(isol)%s%det_lag, sol(isol)%phys(j)%thick, sol(isol)%phys(j)%d, sol(isol)%phys(j)%ul, sol(isol)%s%sumul, sol(isol)%phys(j)%fc, sol(isol)%s%sumfc, sol(isol)%phys(j)%st, sol(isol)%s%ffc, sol(isol)%phys(j)%hk, sol(isol)%s%sw, sol(isol)%phys(j)%wpmm, sol(isol)%s%sumwp, sol(isol)%phys(j)%crdep, sol(isol)%s%crk, sol(isol)%ly(j)%volcr, sol(isol)%s%swpwt, sol(isol)%s%wat_tbl, sol(isol)%phys(nly)%d, sol(isol)%s%avpor, sol(isol)%s%avbd` |
| [sym:basin_module] | `sol` | `sol(isol)%s%alb, sol(isol)%s%anion_excl, sol(isol)%s%nly, sol(isol)%phys(j)%k, sol(isol)%s%hydgrp, sol(isol)%phys(j)%bd, sol(isol)%phys(j)%awc, sol(isol)%phys(j)%rock, sol(isol)%ly(j)%cal, sol(isol)%ly(j)%ph, sol(isol)%phys(j)%wp, sol(isol)%phys(j)%clay, sol(isol)%phys(j)%up, sol(isol)%phys(j)%por, sol(isol)%ly(j)%vwt, sol(isol)%phys(1)%sand, sol(isol)%phys(1)%clay, sol(isol)%phys(1)%silt, sol(isol)%s%det_san, sol(isol)%s%det_sil, sol(isol)%s%det_cla, sol(isol)%s%det_sag, sol(isol)%s%det_lag, sol(isol)%phys(j)%thick, sol(isol)%phys(j)%d, sol(isol)%phys(j)%ul, sol(isol)%s%sumul, sol(isol)%phys(j)%fc, sol(isol)%s%sumfc, sol(isol)%phys(j)%st, sol(isol)%s%ffc, sol(isol)%phys(j)%hk, sol(isol)%s%sw, sol(isol)%phys(j)%wpmm, sol(isol)%s%sumwp, sol(isol)%phys(j)%crdep, sol(isol)%s%crk, sol(isol)%ly(j)%volcr, sol(isol)%s%swpwt, sol(isol)%s%wat_tbl, sol(isol)%phys(nly)%d, sol(isol)%s%avpor, sol(isol)%s%avbd` |
| [sym:time_module] | `time` | `time%step` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sol(isol)%phys(j)%k` | When `sol(isol)%phys(j)%k <= 0.0` for a layer | The layer's saturated hydraulic conductivity is replaced with a default value based on the soil hydrologic group: A, B, C, D, or the fallback `nota`. This prevents missing or invalid conductivity from propagating into later hydrology calculations. |
| `sol(isol)%phys(j)%wp` | When `sol(isol)%phys(j)%wp <= 0.` after the wilting-point formula | The layer wilting point is raised to a small positive floor so the model has a usable lower water-content bound and can compute storage terms without nonphysical zero or negative values. |
| `sol(isol)%phys(j)%up` | After `wp` and `awc` are combined for the layer | `up` is set to the field-capacity water-content threshold, and if that value would exceed porosity it is reduced to stay below porosity. This keeps the layer's upper water bound physically feasible. |
| `sol(isol)%phys(j)%por` | After bulk density is available for the layer | Porosity is computed from bulk density using the soil particle density constant 2.65. This supplies the layer's total pore-space fraction for later storage and drainage calculations. |
| `sol(isol)%ly(j)%vwt` | For every layer in the main water-balance loop | Volumetric water stored at wilting point is computed as `wp * thick`, giving the mm water equivalent held at the lower water limit in that layer. |
| `sol(isol)%s%det_san` | After texture fractions are derived from the first layer | The profile's detached sand fraction is computed from sand and clay and may be renormalized if the aggregate balance goes negative. This profile sediment class is used by later erosion and detachment behavior. |
| `sol(isol)%s%det_sil` | After texture fractions are derived from the first layer | The profile's detached silt fraction is computed from the first-layer silt fraction and, if needed, rescaled with the other fractions during the negative-large-aggregate check. |
| `sol(isol)%s%det_cla` | After texture fractions are derived from the first layer | The profile's detached clay fraction is computed from the first-layer clay fraction and, if needed, rescaled with the other fractions during the negative-large-aggregate check. |
| `sol(isol)%s%det_sag` | After texture fractions are derived from the first layer | The profile's small-aggregate fraction is set from clay-based piecewise rules and may be rescaled if the large-aggregate fraction becomes negative. |
| `sol(isol)%s%det_lag` | If the computed large-aggregate fraction is negative | The profile's large-aggregate fraction is forced to zero and the other detached fractions are renormalized so the profile fractions remain usable. |
| `sol(isol)%phys(j)%thick` | During the per-layer thickness pass | Thickness is recomputed from cumulative depth and previous depth so the model has each layer's actual thickness rather than bottom depth. |
| `sol(isol)%phys(j)%ul` | During the per-layer thickness pass | Upper-limit storage in millimeters is computed as the pore-space above wilting point times layer thickness, giving the layer's water held above the lower bound. |
| `sol(isol)%s%sumul` | During the per-layer thickness pass | The profile saturation-water total is accumulated from each layer's `ul` value so later routines can use a profile-scale saturation storage. |
| `sol(isol)%phys(j)%fc` | During the per-layer thickness pass | Field-capacity water in millimeters is computed from the difference between the upper-water threshold and wilting point times layer thickness. |
| `sol(isol)%s%sumfc` | During the per-layer thickness pass | The profile field-capacity total is accumulated across layers for later profile-level storage calculations. |
| `sol(isol)%phys(j)%st` | During the per-layer thickness pass | Storage at the current soil state is derived from field capacity and the profile fraction `ffc`, providing the layer's initial water storage condition. |
| `sol(isol)%phys(j)%hk` | During the per-layer thickness pass | The layer hydraulic coefficient is computed from the difference between saturation and field-capacity storage divided by conductivity, with a floor of 1 to avoid unrealistically small values. |
| `sol(isol)%s%sw` | During the per-layer thickness pass | The profile's current soil-water total is accumulated from each layer's storage-at-condition value. |
| `sol(isol)%phys(j)%wpmm` | During the per-layer thickness pass | Wilting-point water in millimeters is computed as the layer wilting-point fraction times thickness. |
| `sol(isol)%s%sumwp` | During the per-layer thickness pass | The profile wilting-point total is accumulated from the layer wilting-point water amounts. |
| `sol(isol)%phys(j)%crdep` | During the per-layer thickness pass | Potential crack depth is computed from the profile crack potential, exponential depth decay, and layer thickness. |
| `sol(isol)%ly(j)%volcr` | During the per-layer thickness pass | Crack volume for the layer is computed from crack depth and the fraction of water storage between field capacity and storage-at-condition. |
| `sol(isol)%s%swpwt` | After the per-layer water-balance loop | The profile water-at-water-table state is copied from the current soil-water total so later water-table logic has a reference value. |
| `sol(isol)%s%wat_tbl` | When the initial field-capacity fraction exceeds 1 | A water-table depth is estimated from the residual between detached aggregate fraction and field-capacity storage; otherwise it is set to zero. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:3.1.1 | Bulk density relationship | $\rho _b=\frac{M_s}{V_T}$ | Bulk density is an input state used to derive porosity rather than being computed from mass and total volume inside this routine. |
| 2:3.1.2 | Total soil volume decomposition | $V_T=V_A+V_W+V_S$ | The routine uses bulk density and porosity directly; it does not explicitly decompose total volume into air, water, and solids volumes. |
| 2:3.1.3 | Soil porosity | $\phi_{soil}=1-\frac{\rho_b}{\rho_s}$ | Verified against SWAT+ 62.0.0 (soil_phys_init.f90:94). por = 1. - bd/2.65` — ρ_s hardcoded 2.65 |
| 2:3.1.4 | Available water capacity | $AWC=FC-WP$ | Verified against SWAT+ 62.0.0 (soil_phys_init.f90:93). AWC=FC−WP (rearranged `up = wp + awc`) |
| 2:3.1.5 | Wilting point | $WP_{ly}=0.40*\frac{m_c*\rho_b}{100}$ | Verified against SWAT+ 62.0.0 (soil_phys_init.f90:91). wp = 0.4*clay*bd/100.` — wilting point |
| 2:3.1.6 | Field capacity | $FC_{ly}=WP_{ly}+AWC_{ly}$ | Verified against SWAT+ 62.0.0 (soil_phys_init.f90:93). up = wp + awc` — FC = WP + AWC |
| 2:3.3.4 | Maximum crack depth by layer | $crk_{max,ly}=0.916*crk_{max}*exp\lfloor-0.0012*z_{l,ly}\rfloor*depth_{ly}$ | crdep = crk*0.916*exp(-0.0012*z)*thickness. |
| 2:3.2.4 |  | $TT_{perc}=\frac{SAT_{ly}-FC_{ly}}{K_{sat}}$ | Verified against SWAT+ 62.0.0 (soil_phys_init.f90:153). hk = (ul - fc)/k` — TT_perc, floored at 1. (:155) |
| 5:2.2.6 |  | $AWC_{ly}=FC_{ly}-WP_{ly}$ | Verified against SWAT+ 62.0.0 (soil_phys_init.f90:93). AWC=FC−WP |
| 7:2.1.1 |  | $PSA=(SAN)(1.-CLA)^{2.4}$ | Verified against SWAT+ 62.0.0 (soil_phys_init.f90:114). det_san = sa*(1-cl)**2.49` — exponent 2.49 in code vs theory's 2.4 |
| 7:2.1.2 |  | $PSI=0.13SIL$ | Verified against SWAT+ 62.0.0 (soil_phys_init.f90:115). det_sil = 0.13*si` — silt fraction |
| 7:2.1.3 |  | $PCL=0.20CLA$ | Verified against SWAT+ 62.0.0 (soil_phys_init.f90:116). det_cla = 0.20*cl` — clay fraction |
| 7:2.1.4 |  | $SAG=\begin{cases}2.0CLA & for &CLA 0.5 \end{cases}$ | Verified against SWAT+ 62.0.0 (soil_phys_init.f90:118). det_sag = 2.0*cl` (CLA<0.25 branch) |
| 7:2.1.5 |  | $LAG=1.0-PSA-PSI-PCL-SAG$ | Verified against SWAT+ 62.0.0 (soil_phys_init.f90:125). det_lag = 1.−san−sil−cla−sag |

## Lineage

Four resolved commits changed `soil_phys_init`. The latest source addition commit (`94b6dec`) brought the procedure in with its full initialization logic. Later commits mostly made behavior-preserving cleanup, but `d462a2d` simplified the nested hydrologic-group branch for saturated conductivity, `759dd36` tightened indentation while preserving the water-content logic, `39fabde` initialized local working variables to zero, and `889136d` corrected a comment typo without changing code behavior.

- `94b6dec` introduced the full soil-physics initialization logic in the source snapshot, including layer defaulting, water-content calculations, detached-sediment fractions, crack depth, and profile water-table setup.
- `39fabde` changed local declarations to initialized forms (`j`, `nly`, `sumpor`, `pormm`, `nota`, `a`, `b`, `c`, `d`, `drpor`, `sa`, `cl`, `si`, `depth_prev`), which makes the routine's scratch-state deterministic before use.
- `d462a2d` rewrote the nested hydrologic-group conductivity assignment into an `else if` chain, preserving the same conductivity choices while cleaning the control flow.
- `759dd36` only reformatted the nested `if` block around `up` and `wp` calculations; the computed values remained the same.
- `889136d` changed a comment from "wont" to "won't" and did not alter runtime behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'soil_phys_init' has no extracted documentation comment.
