---
kind: procedure
symbol: pl_nup
title: pl_nup
status: filled
source_hash: e3cfb2d2bf32efef
version_label: SWAT+ 62.0.0
locals:
  j: '`j` is the current HRU index. The routine copies `ihru` into `j` and then uses it to
    select the active soil profile, plant community, plant mass pools, and nitrogen-balance
    output for the HRU being processed.'
  l: '`l` is the soil-layer loop counter. It is used first to locate the layer containing
    the root zone and then to walk the root-occupied layers while transferring nitrate from
    each layer into plant uptake.'
  uno3l: '`uno3l` holds the nitrogen taken from the current soil layer on the current pass.
    It is the layer-level uptake amount that is added to `nplnt(j)` and subtracted from `soil1(j)%mn(l)%no3`.'
  idp: '`idp` is the plant database index for the current plant species. The routine sets
    it from `pcom(j)%plcur(ipl)%idplt` so it can read plant-specific parameters such as `pldb(idp)%nfix_co`.'
  root_depth: '`root_depth` tracks the effective rooting depth used in the uptake curve. It
    starts from `pcom(j)%plg(ipl)%root_dep`, is forced to at least 10.1 mm, and may be adjusted
    to the first layer boundary that contains the root zone.'
  unmx: '`unmx` is the cumulative maximum plant nitrogen that can be removed from the soil
    profile by a given depth. It is computed from `uno3d(ipl)`, `rto_no3`, `bsn_prm%n_updis`,
    layer depth, and root depth, and then used to limit uptake from each layer.'
  soil_depth: '`soil_depth` stores the current layer bottom depth as the routine scans the
    soil profile. It is used to decide whether the roots extend into the layer and to evaluate
    the depth-based nitrogen uptake equation.'
  xx: '`xx` is a temporary ratio used in the post-uptake stress calculation. It is set to
    `nplnt(j) / uno3d(ipl)` when available, or to 1 when `uno3d(ipl)` is tiny, and then combined
    with the stress returned by `nuts`.'
  max: '`max` is the intrinsic `Max` function name, not a user-defined variable. The declaration
    line is written as `integer :: max`, but the code uses `max(...)` as a function call when
    initializing `root_depth`, so this declaration is suspicious in the extracted source.'
uses:
  plant_data_module: '`plant_data_module` supplies `pldb(idp)%nfix_co`, the species-level
    nitrogen-fixation coefficient. `pl_nup` uses that coefficient to decide whether the plant
    is a legume and whether it should call `pl_nfix` and force nitrogen stress to 1.'
  basin_module: '`basin_module` supplies `bsn_prm%n_updis`, the basin nitrogen-uptake distribution
    parameter. `pl_nup` inserts it into the cumulative uptake equation that shapes how nitrogen
    demand increases with soil depth.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` holds the soil nitrate pool
    and the plant nitrogen mass pools that `pl_nup` changes. The routine removes nitrate from
    `soil1(j)%mn(l)%no3` and adds the resulting uptake to `pl_mass(j)%tot(ipl)%n`, `pl_mass(j)%ab_gr(ipl)%n`,
    `pl_mass(j)%root(ipl)%n`, and `pl_mass_up%n`.'
  hru_module: '`hru_module` provides the HRU-scoped variables that control and record the
    calculation. `uno3d`, `nplnt`, `un2`, `fixn`, `ihru`, `ipl`, `rto_no3`, and `uptake%n_norm`
    determine plant demand, uptake limits, fixation addition, and the plant nitrogen stress
    update for the current HRU/plant pair.'
  soil_module: '`soil_module` provides the soil-layer geometry used to stop uptake below the
    rooting zone. `soil(j)%nly` sets the loop bounds and `soil(j)%phys(l)%d` provides each
    layer''s bottom depth for the root-depth comparisons.'
  plant_module: '`plant_module` supplies the current plant identity, stress state, and root
    allocation fraction. `pcom(j)%plcur(ipl)%idplt` selects the species database record, `pcom(j)%plstr(ipl)%strsn`
    receives the resulting nitrogen stress factor, and `pcom(j)%plg(ipl)%root_dep` defines
    the plant root depth used by the uptake curve.'
  output_landscape_module: '`output_landscape_module` contains the HRU nitrogen-balance accumulator.
    `pl_nup` adds the day’s plant nitrogen uptake to `hnb_d(j)%nuptake` so landscape output
    can report plant N removal.'
---

<!-- facts:header -->

Computes daily plant nitrogen uptake for the current HRU and plant, including optional nitrogen fixation for legumes and the resulting nitrogen stress factor.

## Bottom Line

`pl_nup` computes daily plant nitrogen uptake for the current HRU by distributing plant N demand through the rooted soil layers, removing nitrate from `soil1(j)%mn(l)%no3`, and accumulating the uptake into `nplnt(j)`.

If the crop is a legume, it also calls `pl_nfix` to add fixed nitrogen. The routine then updates plant nitrogen mass bookkeeping, records HRU nitrogen uptake in `hnb_d(j)%nuptake`, and sets plant nitrogen stress in `pcom(j)%plstr(ipl)%strsn`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`pl_nup` runs during the plant biomass growth workflow after `pl_biomass_gro` has updated `uno3d(ipl)` and related uptake-demand variables for the current HRU. Its results feed the rest of the day’s plant mass bookkeeping and nitrogen-stress response, which downstream growth and balance logic use.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize HRU and plant state | Copies the current HRU index from `ihru`, resolves the current plant database id from `pcom(j)%plcur(ipl)%idplt`, resets plant nitrogen stress to 1, clears the HRU nitrogen-uptake output, and returns immediately if `uno3d(ipl)` is effectively zero. |
| 2. find effective rooting depth | Starts from the plant root depth, enforces a minimum depth of 10.1 mm, scans soil layers until the root zone reaches into a layer, and snaps `root_depth` to that layer boundary. |
| 3. accumulate uptake by soil layer | Loops through soil layers in the rooting zone, computes the maximum removable nitrogen `unmx` from the current plant demand, basin uptake distribution, and depth fraction, limits layer uptake by the remaining demand and the layer nitrate pool, then adds uptake to `nplnt(j)` and subtracts it from `soil1(j)%mn(l)%no3`. |
| 4. prevent negative plant uptake | Clamps `nplnt(j)` to zero if roundoff or prior calculations leave it negative. |
| 5. add legume fixation when enabled | Checks the crop fixation coefficient and, when it is nonzero, calls `pl_nfix` to calculate daily fixed nitrogen in `fixn` for the current plant. |
| 6. update plant nitrogen masses | Adds fixed N to `nplnt(j)`, then adds the resulting nitrogen uptake to total plant N, above-ground N, root N, and the daily plant uptake summary `pl_mass_up%n`. |
| 7. record HRU nitrogen uptake | Adds the day's plant nitrogen uptake to `hnb_d(j)%nuptake` for landscape nitrogen balance output. |
| 8. compute nitrogen stress | Leaves legume stress at 1. For non-legumes, calls `nuts` to compute stress from total plant N and ideal N, compares it with the uptake ratio `nplnt(j)/uno3d(ipl)` when available, takes the larger value, and caps the stress factor at 1. |
| 9. return to caller | Ends the subroutine after soil, plant, and HRU nitrogen states have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%nfix_co` |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%n_updis` |
| [sym:organic_mineral_mass_module] | `soil1, pl_mass, pl_mass_up` | `soil1(j)%mn(l)%no3, pl_mass(j)%tot(ipl)%n, pl_mass(j)%ab_gr(ipl)%n, pl_mass(j)%root(ipl)%n, pl_mass_up%n` |
| [sym:hru_module] | `uptake, nplnt, un2, uno3d, fixn, ihru, ipl, rto_no3` | `uptake%n_norm` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(l)%d` |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plstr(ipl)%strsn, pcom(j)%plg(ipl)%root_dep` |
| [sym:output_landscape_module] | `hnb_d` | `hnb_d(j)%nuptake` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcom(j)%plstr(ipl)%strsn` | Always at entry; then set to 1.0 for legumes or to the maximum of nutrient-stress and uptake-ratio calculations for non-legumes. | Stores the current plant nitrogen stress factor used by later growth calculations. This routine resets it before computing today's stress, then leaves legumes unstressed and bounds non-legume stress to the range 0 to 1. |
| `hnb_d(j)%nuptake` | Always initialized to 0 at entry, then incremented by today's plant nitrogen uptake after soil uptake and any fixation are applied. | Accumulates the HRU-scale plant nitrogen uptake reported in landscape nitrogen balance output. |
| `nplnt(j)` | Changed inside the rooting-zone loop whenever nitrate is available in a soil layer and the plant still has unmet uptake capacity. | Tracks the day's total nitrogen taken up by the current plant from soil nitrate, plus any fixed N added later. The updated value is reused for plant mass bookkeeping and stress calculations. |
| `soil1(j)%mn(l)%no3` | Changed for each rooted soil layer when layer uptake is taken from that layer. | Represents layer nitrate remaining after plant uptake removes part of the mineral N pool. |
| `pl_mass(j)%tot(ipl)%n` | Updated after soil uptake and fixation, always by adding `nplnt(j)` to the existing plant total nitrogen pool. | Stores total plant nitrogen mass for the current plant in the community; this value is later used by `nuts` and by plant mass bookkeeping. |
| `pl_mass(j)%ab_gr(ipl)%n` | Updated after soil uptake and fixation, always by adding the above-ground share of `nplnt(j)` based on root fraction. | Stores above-ground plant nitrogen mass for the current plant, which is part of the plant biomass nitrogen accounting used later in the simulation. |
| `pl_mass(j)%root(ipl)%n` | Updated after soil uptake and fixation, always by adding the root share of `nplnt(j)` based on root fraction. | Stores root nitrogen mass for the current plant, keeping the plant root N pool consistent with today's uptake. |
| `pl_mass_up%n` | Set after uptake and fixation are finalized for the current plant. | Holds the day's plant nitrogen uptake amount for biomass and nutrient-updates reporting. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:2.3.6 | Cumulative nitrogen uptake by depth | $N_{up,z}=\frac{N_{up}}{[1-exp(-\beta_n)]}*[1-exp(-\beta_n*\frac{z}{z_{root}})]$ | Verified against SWAT+ 62.0.0 (pl_nup.f90:81). unmx = uno3d*rto_no3*(1.-Exp(-n_updis*z/root_dep))/n_norm` — N uptake depth dist |
| 5:2.3.7 | Layer nitrogen uptake potential | $N_{up,ly}=N_{up,zl}-N_{up,zu}$ | Layer uptake is recovered from the cumulative depth curve through the running plant total nplnt rather than by an explicit Nup,zl - Nup,zu difference variable. |
| 5:2.3.8 | Actual layer nitrogen uptake | $N_{actualup,ly}=min\lfloor N_{up,ly} +N_{demand},NO3_{ly}\rfloor$ | Actual layer uptake is min(unmx - nplnt, layer NO3). The page's separate demand-addition term is folded into the cumulative-demand formulation. |

## Lineage

`pl_nup.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pl_nup.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `9c706fd` (2025-02-03) — Made a correction to case 3 in the cbn_zhang2.f90 to reset the till_eff to 1.0 after 30 days.
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_nup' has no extracted documentation comment.
- algorithm_steps revised: replaced placeholder steps with a 9-step model flow matching the visible source lines and merged the soil-uptake and bookkeeping blocks.
- The declaration `integer :: max` appears inconsistent with the use of `max(...)` as an intrinsic function; source behavior follows the code as written, but the declaration may be a parsing artifact or source issue.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
