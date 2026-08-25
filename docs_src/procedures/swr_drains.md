---
kind: procedure
symbol: swr_drains
title: swr_drains
status: filled
source_hash: e0bd6f376d513b52
version_label: SWAT+ 62.0.0
locals:
  j1: Layer index used to walk through the soil profile and apply the drain calculations layer
    by layer.
  j: Active HRU index copied from `ihru`; all HRU-, soil-, time-, and wetland-state lookups
    are made for this HRU.
  m: Small loop counter used in the Kirkham geometry sum for the `gee1` factor.
  cone: Computed effective lateral saturated conductivity for the current HRU profile, derived
    from layer conductivities and saturated thickness.
  depth: Computed depth from the soil surface to the drain-equation reference level used in
    the flux calculations.
  dg: Declared as a layer-depth placeholder, but this source span does not assign it before
    it is used in the fallback conductivity calculation; the source is therefore ambiguous
    here.
  ad: Adjusted drain depth used in the drain geometry and Kirkham-factor calculations, based
    on soil depth and configured drain depth.
  ap: Intermediate geometric correction term used in the drain-head calculation when the drain
    is shallow relative to spacing.
  hdrain: Equivalent depth from the drain water surface to the impermeable layer, used as
    the effective head in the drainage/subirrigation equations.
  gee: Final Kirkham G-factor used to scale the tile-flow equations after being bounded to
    the model’s allowed range.
  gee1: Accumulated logarithmic contribution to the Kirkham G-factor from the two-term loop
    over `m`.
  gee2: Intermediate ratio term in the Kirkham G-factor computation for one summand.
  gee3: Second intermediate ratio term in the Kirkham G-factor computation for one summand.
  pi: Approximate value of pi used in the trigonometric and logarithmic geometry formulas.
  k2: Intermediate tangent term in the Kirkham-factor computation based on drain depth and
    soil depth.
  k3: Intermediate tangent term in the Kirkham-factor computation based on drain radius and
    soil depth.
  k4: Angle-like intermediate for the first hyperbolic/trigonometric pair inside the Kirkham
    sum.
  k5: Angle-like intermediate for the drain-radius term inside the Kirkham sum.
  k6: Angle-like intermediate for the adjusted-drain-depth term inside the Kirkham sum.
  y1: Dummy depth variable derived from maximum rooting depth minus shallower water-table
    depth; it controls how much of each layer contributes to the saturated thickness.
  isdr: Stores the HRU’s tile-drain flag from `hru(j)%tiledrain`, though this source span
    does not branch on it after assignment.
  above: Tracks the top depth of the previously processed layer so the current layer’s saturated
    thickness can be clipped correctly.
  x: Upper bound for the current layer’s saturated thickness, equal to the layer thickness
    remaining below `above`.
  sum: Accumulator for the weighted effective conductivity sum used to compute `cone`.
  deep: Accumulator for the total saturated thickness used as the divisor when averaging conductivity
    into `cone`.
  xx: Intermediate ratio `k2/k3` used to decide whether the Kirkham G-factor uses the simplified
    or logarithmic form.
  hdmin: Minimum drain-head depth derived from `depth - sdr_dep`; it prevents using a drain
    head shallower than the drain depth reference.
  storro: Threshold surface storage computed as 20% of `stmaxd(j)`; ponded storage must exceed
    this before direct drainage is computed.
  stor: Current HRU surface storage or ponded water depth used to decide between drainage
    and subirrigation branches.
  dflux: Computed tile or subirrigation flux for the day; this is the value ultimately returned
    as `qtile`.
  em: Distance from drain water level to water table at midpoint; negative values indicate
    the subirrigation branch.
  ddranp: Adjusted drain-depth threshold used to suppress subirrigation when the water table
    is too shallow relative to the drain bottom.
  dot: Helper depth used in the subirrigation equation as the distance from the impermeable
    layer to the water level above the drain.
  cosh: Intrinsic hyperbolic cosine function used in the Kirkham G-factor terms.
  cos: Intrinsic cosine function used in the Kirkham G-factor terms.
uses:
  basin_module: The basin setting decides whether the Drainmod-style routine is the selected
    tile-drain method; `swr_percmain` checks `bsn_cc%tdrn` before calling `swr_drains`, so
    this module determines whether this procedure is even reached.
  hydrograph_module: The wetland hydrograph storage provides the current reservoir/wetland
    outflow volume. `swr_drains` uses `wet(j)%flo` to estimate HRU surface storage when the
    HRU is connected to a wetland rather than using rainfall and runoff terms.
  hru_module: The HRU module holds the active HRU’s tile-drain switch, drain geometry, management
    depth, surface water inputs, and the `qtile` output. `swr_drains` reads those HRU settings
    to build the geometry and writes the resulting daily tile flux back into the shared HRU
    state.
  soil_module: The soil module provides the active profile depth, layer count, layer boundaries,
    and hydraulic properties needed to compute the saturated thickness and effective lateral
    conductivity. Without `soil(j)` this routine could not determine how much of each layer
    participates in the drain calculation.
  time_module: The time module is used to detect the first simulation day so surface storage
    can be initialized to zero before flux is computed. This keeps the daily drainage logic
    from carrying over a stale storage value at startup.
  reservoir_module: The reservoir module tells the routine whether the HRU drains to a wetland/reservoir
    and supplies its surface area. That area is needed to convert `wet(j)%flo` into an equivalent
    depth when surface storage is derived from wetland water volume.
---

<!-- facts:header -->

Computes tile-drain and subirrigation flux for the active HRU using Drainmod-style equations. It also derives the profile’s effective lateral conductivity and returns the resulting daily tile flow in `qtile`.

## Bottom Line

`swr_drains` is the tile-drain/subirrigation routine used when an HRU is configured for Drainmod-style drainage. It computes an effective lateral hydraulic conductivity for the active soil profile, estimates the drain water table geometry, and then calculates daily flux as either drainage or subirrigation depending on surface storage and water-table position.

The routine matters because it produces `qtile`, the tile flow used by the HRU water balance after `swr_percmain` has already established that tile drainage is active and the Drainmod option is selected. It also updates layer conductivity values in `soil(j)%ly(j1)%conk` for the current HRU profile before solving the flux equations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`swr_percmain` calls this routine after it has determined that the HRU is tiled and that the Drainmod tile option (`bsn_cc%tdrn == 1`) should be used. Before the call, `swr_percmain` has already established the active HRU context and the current water-table condition; after the call, later HRU water-balance logic depends on `qtile` as the day’s tile-flow result.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize active HRU and profile state | The routine copies `ihru` to `j`, reads the HRU tile-drain flag into `isdr`, clears the layer thickness accumulator array `wnan`, computes the water-table depth proxy `y1`, and initializes geometry constants such as `above` and `pi` before any flux equations are evaluated. |
| 2. Build saturated thickness by layer | For each soil layer, the routine determines whether the current water-table proxy reaches that layer. It stores the saturated thickness in `wnan(j1)`, clips it to the layer thickness, and updates `above` so the next layer is measured from the correct top boundary. |
| 3. Compute effective lateral conductivity | The routine converts each layer’s saturated conductivity to a lateral conductivity with `hru(j)%sdr%latksat`, then forms weighted sums of conductivity and saturated thickness. If the saturated zone is too small or the sum is too small, it falls back to using full layer thicknesses; otherwise it averages the weighted profile into `cone`. |
| 4. Derive drain geometry parameters | Using drain depth, spacing, radius, and soil depth, the routine computes `ad`, `ap`, `hdrain`, and the minimum allowable drain head `hdmin`. The head calculation uses a shallow-drain formula when the drain spacing ratio is small and otherwise uses the adjusted drain depth directly. |
| 5. Compute Kirkham G-factor | The routine evaluates the Kirkham geometry terms `k2` through `k6`, accumulates the logarithmic correction in `gee1` across two iterations of `m`, and then forms `gee`. The result is bounded to the model’s allowed range of 1 to 12. |
| 6. Prepare surface storage threshold | The routine computes the drain reference depth, calls `swr_depstor` to refresh `stmaxd(j)`, derives `storro` as 20% of that storage, initializes `stor` on the first simulation day, and then sets current surface storage either from HRU water balance terms or from wetland volume. It also enforces `hdrain >= hdmin` before the flux branch is chosen. |
| 7. Compute drainage when ponded water is sufficient | If surface storage exceeds the threshold and the water table is shallow enough, the routine computes positive tile drainage flux from the Drainmod equation using `cone`, `depth`, `hdrain`, `stor`, and `gee`. It then caps the result at the HRU drainage coefficient `hru(j)%sdr%drain_co`. |
| 8. Compute subirrigation when the water table is below the drain | When the drainage branch does not apply, the routine checks whether the water table is sufficiently below the drain to allow subirrigation. It computes `em`, `ddranp`, `dot`, and a negative flux from the subirrigation formula, then suppresses it if the water table is too shallow or limits it by the pump capacity `hru(j)%sdr%pumpcap`. |
| 9. Compute shallow-water-table drainage fallback | If the water table is not deep enough for the full subirrigation branch, the routine uses the simpler drainage equation with `em` and `hdrain`. It limits the result to the drainage coefficient and prevents negative or below-water-table drainage by forcing `dflux` to zero when needed. |
| 10. Return tile flow | The routine stores the computed daily flux in `qtile` and returns to the caller. That shared state is the procedure’s modeled tile-flow output. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module globals, including basin configuration that can control which drainage formulation is active` | `basn_cc%tdrn` |
| [sym:hydrograph_module] | `wet` | `wet(j)%flo` |
| [sym:hru_module] | `hru, wnan, stmaxd, ihru, surfq, etday, inflpcp, precip_eff, qtile, wt_shall` | `hru(j)%tiledrain, hru(j)%sdr%latksat, hru(j)%lumv%sdr_dep, hru(j)%sdr%dist, hru(j)%sdr%radius, hru(j)%sdr%drain_co, hru(j)%sdr%pumpcap` |
| [sym:soil_module] | `soil` | `soil(j)%zmx, soil(j)%nly, soil(j)%phys(j1)%d, soil(j)%ly(j1)%conk, soil(j)%phys(j1)%k, soil(j)%phys(j1)%thick` |
| [sym:time_module] | `time` | `time%yrs, time%day, time%day_start` |
| [sym:reservoir_module] | `wet_ob` | `wet_ob(j)%area_ha` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wnan` | After the loop over soil layers, when the routine builds the weighted lateral-conductivity sum for the active HRU. | `wnan` is cleared at the start of the routine so each layer’s saturated thickness can be recomputed from the current water-table depth `y1`. |
| `wnan(j1)` | Inside `do j1 = 1, soil(j)%nly` when the water table intersects the current layer. | `wnan(j1)` stores the saturated thickness contributed by that layer, clipped so it does not exceed the layer’s thickness below the previous boundary. |
| `if(wnan(j1)>x)wnan(j1)` | Still inside the layer loop, after `wnan(j1)` is computed and `x` is available as the maximum remaining thickness. | This clipping prevents the computed saturated thickness from extending past the current layer’s remaining thickness, keeping the profile geometry consistent. |
| `soil(j)%ly(j1)%conk` | During the conductivity accumulation loop after `hru(j)%sdr%latksat` is known. | Each layer’s lateral conductivity is overwritten with the HRU-specific lateral factor times the layer’s saturated conductivity, producing the effective profile conductivity used by the drainage equations. |
| `qtile` | At the end of the main flux branch after `dflux` has been computed. | `qtile` receives the final daily tile/subirrigation flux so downstream HRU water-balance logic can use the result. |

## File I/O

<!-- facts:io -->


## Lineage

`swr_drains.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `swr_drains.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'swr_drains' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into source-backed steps and cited only visible line ranges from swr_drains.f90.
- Source ambiguity: `dg` is declared and then used in the fallback thickness loop, but this source span does not show an assignment before `deep = deep + dg`.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
