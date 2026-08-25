---
kind: procedure
symbol: ch_rtpest
title: ch_rtpest
status: filled
source_hash: 7c63ef76804b2a11
version_label: SWAT+ 62.0.0
locals:
  ipest: Loop counter for the sequential pesticide being processed in the channel reach.
  jpst: Database index for the current pesticide; it maps the sequential simulation pesticide
    number from `cs_db%pest_num(ipest)` to the pesticide property tables.
  ipseq: Sequential basin pesticide number for a daughter or metabolite pesticide created
    from the current parent pesticide.
  ipdb: Database index for the daughter pesticide identified by `ipseq`; used to fetch molecular
    weight and other daughter/parent property ratios.
  imeta: Counter over the current pesticide's configured daughter metabolites.
  mol_wt_rto: Molecular-weight ratio used to convert parent-loss mass into equivalent daughter
    mass before storing metabolite production.
  pstin: Incoming pesticide mass delivered to the reach during the day from the upstream hydrograph.
  kd: Water-column partition coefficient built from pesticide KOC and channel carbon; it controls
    soluble versus sorbed fractions.
  depth: Channel water depth used to scale depth-dependent process rates; it is taken from
    `rcurv%dep` and floored at 0.01 m.
  chpstmass: Current pesticide mass in the water column inside the reach after inflow and
    successive water-column losses are applied.
  sedpstmass: Current pesticide mass in the active benthic sediment layer after settling,
    resuspension, diffusion, burial, and benthic reaction are applied.
  fd2: Simplified dissolved fraction for the active sediment layer, used as the sediment-side
    term in diffusion exchange.
  solmax: Mass-equivalent solubility ceiling for the current reach water volume; it is used
    to keep dissolved pesticide from exceeding solubility.
  sedcon: Suspended sediment concentration derived from suspended sediment load and water
    volume; it is used when computing the soluble/sorbed water fraction.
  tday: Fraction of a day represented by the routing/travel time; it scales process losses
    that depend on how long water stays in the reach.
  por: Bed-sediment porosity estimate derived from bulk density; it is used when computing
    the sediment dissolved fraction.
  pest_init: Mass before a reaction step; it serves as the baseline for computing reaction
    loss in water or sediment.
  pest_end: Mass remaining after a reaction step; it is the post-decay mass used to overwrite
    the current compartment mass.
  rto_out: Fraction of the remaining water-column pesticide mass routed out of the reach rather
    than retained in channel storage.
uses:
  channel_data_module: The rating-curve depth in `channel_data_module` determines the water
    depth used by the routine. That depth is needed to scale volatilization, settling, resuspension,
    diffusion, and the depth floor check.
  channel_module: '`channel_module` provides `wtrin` and `rttime`, which control whether the
    reach has enough water for in-stream processing and how strongly the time-dependent rates
    are applied. Without them, the routine could not compute flow duration or test for insignificant
    flow.'
  sd_channel_module: '`sd_channel_module` supplies reach-specific sediment properties and
    exchange coefficients that shape pesticide partitioning and sediment-water transfer. `rcurv%dep`
    feeds the depth floor, while `sd_ch(jrch)%carbon`, `sd_ch(jrch)%ch_bd`, and `sd_ch(jrch)%aq_mix(ipest)`
    determine `kd`, porosity, and diffusion strength.'
  ch_pesticide_module: '`ch_pesticide_module` holds the per-reach pesticide process results
    that this routine fills in. The `chpst` and `chpst_d` outputs record reaction, volatilization,
    settling, resuspension, diffusion, burial, and metabolite formation, while `frsol` and
    `frsrb` track the water-column soluble and sorbed fractions used by the process formulas.'
  hydrograph_module: '`hydrograph_module` provides the reach index plus inflow, outflow, and
    storage hydrograph states needed to route pesticide mass. `ht1`, `ch_stor(jrch)`, and
    `ht2` define the incoming water volume, and `jrch` selects the current reach being updated.'
  constituent_mass_module: '`constituent_mass_module` carries the channel pesticide mass arrays
    and the constituent crosswalk. `cs_db%num_pests` and `cs_db%pest_num` drive the loop and
    database lookup, while `hcs1`, `ch_water`, `ch_benthic`, and `hcs2` store incoming mass,
    retained water mass, benthic mass, and routed-out mass.'
  pesticide_data_module: '`pesticide_data_module` provides the pesticide-specific properties
    that parameterize every process rate. The routine uses database KOC, solubility, aquatic
    and benthic decay factors, volatilization, settling, resuspension, burial, active-bed
    depth, and daughter decay fractions to compute the daily mass balance and metabolite production.'
---

<!-- facts:header -->

Computes the daily pesticide balance for each simulated channel pesticide, splitting mass between water, bed sediment, and routed outflow while applying reaction, settling, resuspension, diffusion, burial, and daughter-product formation.

## Bottom Line

`ch_rtpest` updates in-stream pesticide mass for every pesticide in `cs_db%num_pests`. It starts from incoming pesticide mass plus existing channel storage, then applies water-column and benthic processes using channel hydraulics, channel sediment properties, and pesticide database parameters.

The routine also accumulates daughter-metabolite production into `chpst_d`, refreshes channel water and benthic pesticide storage, and separates the final water-column mass into routed outflow (`hcs2`) and retained channel storage (`ch_water`).

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during channel routing after `sd_channel_control3` has completed sediment routing and Muskingum/variable-storage flow routing and confirmed that pesticides are being simulated (`cs_db%num_pests > 0`). Its results feed later channel-output behavior, especially `obcs(icmd)%hd(1)%pest = hcs2%pest`, which passes routed pesticide mass downstream.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Clear the per-reach pesticide process output. | Initializes `chpst_d(jrch)` to the zeroed template `chpstz` so the reach starts with no accumulated pesticide process output for the day. |
| 2. Set the working water depth and enforce a minimum depth. | Reads channel depth from `rcurv%dep` and floors it at 0.01 m to avoid extremely small denominators in depth-dependent process rates. |
| 3. Loop over every simulated pesticide. | Iterates from `1` to `cs_db%num_pests` and maps each sequential pesticide number to its database index through `cs_db%pest_num(ipest)`. |
| 4. Build the current reach mass state. | Computes incoming water volume, incoming pesticide mass, current water-column pesticide mass, and current bed-sediment pesticide mass for the active reach and pesticide. |
| 5. Skip empty pesticide states. | If the combined water and benthic mass is negligible, zeros the stored water and benthic masses and skips the rest of the loop body for that pesticide. |
| 6. Compute suspended-sediment concentration, partitioning, and sediment porosity terms when flow is meaningful. | Uses reach sediment load and water volume to form `sedcon`, then computes `kd` from pesticide KOC and channel carbon, derives soluble and sorbed fractions (`frsol`, `frsrb`), and forms the active-sediment dissolved fraction `fd2` from porosity and `kd`. |
| 7. Compute the flow-duration scaling factor. | Converts reach travel time `rttime` to a day fraction and caps it at 1.0 so process losses cannot exceed a full-day exposure window. |
| 8. Apply water-column reaction and create daughter metabolites. | Applies aqueous decay using `pestcp(jpst)%decay_a ** tday`, stores the reacted mass in `chpst%pest(ipest)%react`, and distributes that loss to daughter pesticides using daughter fractions and molecular-weight ratios in `chpst_d` and `hcs1`. |
| 9. Remove pesticide by volatilization, settling, and resuspension. | Computes volatilization from the dissolved fraction, then settles sorbed pesticide to the bed, then resuspends bed pesticide back to the water column, clamping each loss so it cannot exceed the available compartment mass. |
| 10. Exchange pesticide by diffusion and apply burial. | Computes diffusion between water and bed using `sd_ch(jrch)%aq_mix(ipest)` and the sediment-water concentration difference, then removes additional bed mass by burial using `pestdb(jpst)%ben_bury` and `pestdb(jpst)%ben_act_dep`. |
| 11. Enforce the water-solubility ceiling. | Compares dissolved mass against solubility-based capacity and shifts any excess back into the sediment pool so the dissolved concentration does not exceed the database solubility limit. |
| 12. If flow is insignificant, move mass into sediment storage. | When the reach has essentially no flow, it bypasses the in-stream exchange calculations and transfers the entire pesticide mass into the benthic store. |
| 13. Apply benthic reaction and metabolite production. | Uses `pestcp(jpst)%decay_b` to reduce active sediment pesticide, stores benthic reaction loss in `chpst%pest(ipest)%react_bot`, and routes daughter mass to `chpst_d(jrch)%pest(ipseq)%metab_bot` and `ch_benthic(jrch)%pest(ipseq)`. |
| 14. Write final water-column storage and routed outflow. | Stores the final water-column mass in `hcs1%pest(ipest)` when water exists, always stores the final bed mass in `ch_benthic(jrch)%pest(ipest)`, and splits remaining water mass into routed outflow `hcs2%pest(ipest)` and retained channel storage `ch_water(jrch)%pest(ipest)` using `rto_out`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:channel_data_module] | `rcurv%dep` | `rcurv%dep` |
| [sym:channel_module] | `wtrin, rttime` |  |
| [sym:sd_channel_module] | `rcurv, sd_ch` | `rcurv%dep, sd_ch(jrch)%carbon, sd_ch(jrch)%ch_bd, sd_ch(jrch)%aq_mix(ipest)` |
| [sym:ch_pesticide_module] | `chpst, chpst_d, chpstz, frsol, frsrb` | `chpst%pest(ipest)%react, chpst_d(jrch)%pest(ipseq)%metab, chpst%pest(ipest)%volat, chpst%pest(ipest)%settle, chpst%pest(ipest)%resus, chpst%pest(ipest)%difus, chpst%pest(ipest)%bury, chpst%pest(ipest)%react_bot, chpst_d(jrch)%pest(ipseq)%metab_bot` |
| [sym:hydrograph_module] | `ht1, ch_stor, ht2, jrch` | `ht1%flo, ch_stor(jrch)%flo, ht1%sed, ht2%flo` |
| [sym:constituent_mass_module] | `cs_db, hcs1, ch_water, ch_benthic, hcs2` | `cs_db%num_pests, cs_db%pest_num(ipest), hcs1%pest(ipest), ch_water(jrch)%pest(ipest), ch_benthic(jrch)%pest(ipest), cs_db%pest_num(ipseq), hcs1%pest(ipseq), ch_benthic(jrch)%pest(ipseq), hcs2%pest(ipest)` |
| [sym:pesticide_data_module] | `pestdb, pestcp` | `pestdb(jpst)%koc, pestcp(jpst)%decay_a, pestcp(jpst)%num_metab, pestcp(jpst)%daughter(imeta)%num, pestdb(ipdb)%mol_wt, pestdb(jpst)%mol_wt, pestcp(jpst)%daughter(imeta)%aq_fr, pestdb(jpst)%aq_volat, pestdb(jpst)%aq_settle, pestdb(jpst)%aq_resus, pestdb(jpst)%ben_bury, pestdb(jpst)%ben_act_dep, pestdb(jpst)%solub, pestcp(jpst)%decay_b, pestcp(jpst)%daughter(imeta)%ben_fr` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `chpst_d(jrch)` | After benthic reaction when `pestcp(jpst)%num_metab > 0`, during the loop over `imeta` for each daughter pesticide. | `chpst_d(jrch)` accumulates daughter-pesticide mass created by decay of the parent pesticide in this reach; it is updated whenever a parent reaction or benthic reaction produces metabolite mass for a daughter pesticide. |
| `wtrin` | When the current reach has essentially no flow or when the combined pesticide mass is negligible and the routine zeros the stored water and benthic masses. | `wtrin` is computed from `ht1%flo + ch_stor(jrch)%flo` and is not itself written, but it governs whether in-stream processing is applied. If `wtrin` is too small, the routine bypasses water-column exchange and moves pesticide mass to sediment storage instead. |
| `ch_water(jrch)%pest(ipest)` | When the current reach has meaningful flow and after each process step changes the water-column pesticide mass. | `ch_water(jrch)%pest(ipest)` is overwritten at the end of the routine with the retained water-column mass, which is the post-process mass remaining after routing outflow is removed. |
| `ch_benthic(jrch)%pest(ipest)` | After settling, resuspension, diffusion, burial, and no-flow handling have determined the final bed mass for the current pesticide. | `ch_benthic(jrch)%pest(ipest)` is updated to the final active-benthic pesticide mass remaining in the reach after bed-water exchange and burial, or receives the whole mass when flow is insignificant. |
| `frsol` | When `wtrin / 86400. > 1.e-9`, before the reaction, volatilization, settling, and exchange calculations. | `frsol` is recalculated from `kd` and `sedcon` to represent the fraction of pesticide that stays dissolved in the water column for the current reach conditions. |
| `frsrb` | When `wtrin / 86400. > 1.e-9`, immediately after `frsol` is computed. | `frsrb` is set to the complementary sorbed fraction in water and is then used to scale settling losses from the sorbed pool. |
| `chpst%pest(ipest)%react` | When `pest_init > 1.e-12` during the water-column reaction step. | `chpst%pest(ipest)%react` records the amount lost from the water column by aqueous reaction; that value is the source mass for daughter metabolite production. |
| `chpst_d(jrch)%pest(ipseq)%metab` | When `pest_init > 1.e-12` and the current parent pesticide has configured daughter metabolites. | `chpst_d(jrch)%pest(ipseq)%metab` accumulates water-column daughter mass produced from the parent's reaction loss and is added into the basin daughter hydrograph state. |
| `hcs1%pest(ipseq)` | Within the water-column reaction block, for each daughter metabolite of the current parent pesticide. | `hcs1%pest(ipseq)` is incremented by the new daughter mass so the metabolite becomes part of the incoming basin constituent mass record. |
| `chpst%pest(ipest)%volat` | When the reach has meaningful flow and after the water-column reaction step. | `chpst%pest(ipest)%volat` stores the volatilized mass removed from dissolved pesticide in the water column for the current pesticide and reach. |
| `chpst%pest(ipest)%settle` | When the reach has meaningful flow and after volatilization. | `chpst%pest(ipest)%settle` stores the mass transferred from sorbed water-column pesticide into the active sediment layer. |
| `chpst%pest(ipest)%resus` | When the reach has meaningful flow and after settling has updated the sediment store. | `chpst%pest(ipest)%resus` stores the mass resuspended from the bed sediment back into the water column. |
| `chpst%pest(ipest)%difus` | When the reach has meaningful flow and the diffusion term is evaluated. | `chpst%pest(ipest)%difus` stores the signed diffusive exchange between bed sediment and water, clamped so it cannot remove more mass than is available in either compartment. |
| `chpst%pest(ipest)%bury` | When the reach has meaningful flow and the burial calculation is performed. | `chpst%pest(ipest)%bury` stores the mass removed from the active sediment layer by burial into deeper bed material. |
| `chpst%pest(ipest)%react_bot` | When `pest_init > 1.e-12` for the benthic reaction step. | `chpst%pest(ipest)%react_bot` records the pesticide loss from benthic reaction before daughter products are distributed. |
| `chpst_d(jrch)%pest(ipseq)%metab_bot` | When `pest_init > 1.e-12` in the benthic reaction loop over daughter metabolites. | `chpst_d(jrch)%pest(ipseq)%metab_bot` accumulates daughter mass created from benthic decay of the parent pesticide. |
| `ch_benthic(jrch)%pest(ipseq)` | After benthic reaction, or immediately when the reach has insignificant flow and the routine transfers all mass to sediment storage. | `ch_benthic(jrch)%pest(ipseq)` receives the updated daughter mass in the benthic compartment so the metabolite persists in the bed sediment state. |
| `hcs1%pest(ipest)` | After all water-column and bed processes are complete and `wtrin > 1.e-6`. | `hcs1%pest(ipest)` is overwritten with the final water-column pesticide mass remaining in the reach after internal process losses. |
| `hcs2%pest(ipest)` | At the end of the loop, after `rto_out` is computed from `ht2%flo` and `ch_stor(jrch)%flo`. | `hcs2%pest(ipest)` stores the routed-out pesticide mass that leaves the reach and is passed downstream. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 7:4.1.1 | Dissolved pesticide fraction in water | $F_d=\frac{1}{1+K_d*conc_{sed}}$ | Verified against SWAT+ 62.0.0 (ch_rtpest.f90:81). frsol = 1./(1.+kd*sedcon)` — F_d exactly |
| 7:4.1.2 | Sorbed pesticide fraction in water | $F_p=\frac{K_d*conc_{sed}}{1+ K_d*conc_{sed}}=1-F_d$ | Verified against SWAT+ 62.0.0 (ch_rtpest.f90:82). frsrb = 1. - frsol` — F_p = 1−F_d |
| 7:4.1.3 | Water-column partition coefficient | $K_d=3.085*10^{-8}*K_{ow}$ | Verified against SWAT+ 62.0.0 (ch_rtpest.f90:78). kd = koc·carbon/100` (Koc·foc); theory's `Kd=3.085e-8·Kow` conversion offline |
| 7:4.1.4 | Kow from solubility | $log(K_{ow})=5.00-0.670*log(pst'_{sol})$ | The routine never derives K_ow from solubility; it reads KOC from the pesticide database and multiplies by channel carbon. |
| 7:4.1.5 | Molar solubility conversion | $pst'_{sol}=\frac{pst_{sol}}{MW}*10^3$ | Code checks a mass-based solubility ceiling using pestdb%solub * wtrin but does not form the printed pst'_sol molar-conversion equation. |
| 7:4.1.6 | Water-column pesticide degradation | $pst_{deg,wtr}= k_{p,aq}*pst_{rchwtr}*TT$ | Degradation uses chpstmass * decay_a**tday, which is equivalent to first-order decay but with a precomputed database decay factor rather than the printed k_p,aq form. |
| 7:4.1.8 | Water-column volatilization loss | $pst_{vol,wtr}=\frac{v_v}{depth}*F_d*pst_{rchwtr}*TT$ | volat = aq_volat * frsol * chpstmass * tday / depth matches the theory structure but collapses the transfer-velocity derivation into a stored aq_volat parameter. |
| 7:4.1.9 | Volatilization transfer velocity | $v_v=K_l*\frac{H_e}{H_e+R*T_K*(K_l/K_g)}$ | The code uses a precomputed aq_volat coefficient and does not explicitly evaluate the Henry-law transfer-velocity formula. |
| 7:4.1.10 | Gas and liquid film transfer coefficients | $K_l=\sqrt{r_l*D_l}$ | K_g and K_l are not computed in this routine; their effect is folded into the aq_volat parameter. |
| 7:4.1.11 | Liquid-film renewal rate | $r_l=\frac{86400*v_c}{depth}$ | The routine does not calculate r_l = 86400*v_c/depth explicitly; volatilization uses the precomputed aq_volat term. |
| 7:4.1.12 | Pesticide settling from water column | $pst_{stl,wtr}=\frac{v_s}{depth}*F_p*pst_{rchwtr}*TT$ | settle = aq_settle * frsrb * chpstmass * tday / depth matches the theory structure but uses a stored settling coefficient aq_settle. |
| 7:4.1.13 | Dissolved pesticide outflow | $pst_{sol,o}=Q*\frac{F_d*pst_{rchwtr}}{V}$ | Outflow is removed by multiplying the post-process water-column mass by the routed outflow ratio; dissolved and sorbed fractions are not split into separate explicit Q*F_d/V equations at export time. |
| 7:4.1.14 | Sorbed pesticide outflow | $pst_{sorb,o}=Q*\frac{F_p*pst_{rchwtr}}{V}$ | The same routed outflow ratio removes total water-column pesticide mass after soluble/sorbed partitioning has already controlled volatilization and settling losses. |
| 7:4.2.1 | Active-sediment concentration basis | $conc^*_{sed}=\frac{M_{sed}}{V_{tot}}$ | Verified against SWAT+ 62.0.0 (ch_rtpest.f90:75). sedcon = sed/wtrin*1.e6` — sediment conc |
| 7:4.2.2 | Sediment porosity | $\phi=\frac{V_{wtr}}{V_{tot}}$ | Verified against SWAT+ 62.0.0 (ch_rtpest.f90:85). por = 1. - ch_bd/2.65` — φ |
| 7:4.2.3 | Sediment solids fraction | $1-\phi=\frac{V_{sed}}{V_{tot}}$ | Verified against SWAT+ 62.0.0 (ch_rtpest.f90:85). (1−φ) complement, same line |
| 7:4.2.5 | Bulk sediment concentration relation | $conc^*_{sed}=(1-\phi)*\rho_s$ | Verified against SWAT+ 62.0.0 (ch_rtpest.f90:85). conc*=(1−φ)·ρ_s identity |
| 7:4.2.6 | Dissolved fraction in active sediment layer | $F_{d,sed}=\frac{1}{\phi +(1- \phi)*\rho_s *K_d}$ | Verified against SWAT+ 62.0.0 (ch_rtpest.f90:86). fd2 = 1./(por + kd)` — benthic F_d,sed |
| 7:4.2.7 | Sorbed fraction in active sediment layer | $F_{p,sed}=1-F_{d,sed}$ | Verified against SWAT+ 62.0.0 (ch_rtpest.f90:86). F_p,sed = 1−F_d,sed complement |
| 7:4.2.10 | Resuspension from bed sediment | $pst_{rsp,wtr}=\frac{v_r}{depth}*pst_{rchsed}*TT$ | resus = aq_resus * sedpstmass * tday / depth matches the theory structure but uses a stored resuspension coefficient aq_resus. |
| 7:4.2.11 | Diffusion between bed sediment and water | $pst_{dif}=\mid\frac{v_d}{depth}*(F_{d,sed}*pst_{rchsed}-F_d*pst_{rchwtr})*TT\mid$ | difus = aq_mix * (fd2*sedpstmass - frsol*chpstmass) * tday / depth matches the signed concentration-difference structure, with exchange strength folded into aq_mix. |
| 7:4.2.12 | Diffusion velocity parameter | $v_d=\frac{69.35}{365}*\phi*MW^{-2/3}$ | The printed v_d formula is not evaluated directly; sd_ch(jrch)%aq_mix(ipest) acts as the calibrated sediment-water exchange coefficient. |
| 7:4.2.13 | Burial from active bed layer | $pst_{bur}=\frac{v_b}{D_{sed}}*pst_{rchsed}$ | Verified against SWAT+ 62.0.0 (ch_rtpest.f90). |
| 7:4.3.2 | Benthic pesticide mass balance | $\Delta pst_{rchsed}=-pst_{deg,sed}+pst_{stl,wtr}-pst_{rsp,wtr}-pst_{bur}\pm pst_{dif}$ | The bed-sediment mass balance is distributed across settling, resuspension, diffusion, burial, reaction, and outflow/storage updates rather than one explicit delta equation. |

## Lineage

Four resolved commits changed `ch_rtpest`. The 2024-10-08 commit corrected the water-column decay update from a linear multiply to exponentiation (`decay_a ** tday`). The 2025-08-21 refactor switched depth handling to `rcurv%dep` with a 0.01 m floor. The 2025-08-20 refactor also changed the same depth logic from `rchdep` to `rcurv%dep`. The 2025-10-29 update removed a redundant depth comment, kept the `rcurv%dep` depth source, and changed the decay expression formatting while preserving the exponentiation behavior.

- 2024-10-08: water-column reaction now uses `pestcp(jpst)%decay_a ** tday`, which changes daily decay from a simple scale factor to a time-exponentiated form.
- 2025-08-21: depth sourcing and the minimum-depth guard were standardized to `rcurv%dep` with a 0.01 m floor, affecting every depth-scaled process rate.
- 2025-08-20: the routine was refactored to use `rcurv%dep` instead of `rchdep` for pesticide calculations, aligning depth input with the rating-curve state.
- 2025-10-29: documentation/comment cleanup removed an old depth note and retained the `rcurv%dep`-based depth logic without changing the algorithm.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ch_rtpest' has no extracted documentation comment.
