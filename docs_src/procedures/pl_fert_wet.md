---
kind: procedure
symbol: pl_fert_wet
title: pl_fert_wet
status: filled
source_hash: 14255f7c53c5bb87
version_label: SWAT+ 62.0.0
args:
  ifrt: Selects the fertilizer database record to use. The procedure reads `fertdb(ifrt)`
    to get the fertilizer’s mineral and organic N/P fractions and its NH3 share.
  frt_kg: Gives the fertilizer application rate in kg/ha. The routine multiplies this amount
    by the fertilizer fractions to update wetland stores and fertilizer summary totals.
locals:
  rtof: Fixed weighting factor for splitting organic material between fresh and stable pools
    in commented-out carbon-cycling code; it is initialized but not used in the active logic
    shown here.
  j: Local HRU index used to select the current wetland output element; it is set from `ihru`
    before the fertilizer update.
  x1: Temporary scratch variable initialized to zero; part of added but inactive/unused carbon-cycling
    bookkeeping in this source span.
  x8: Temporary scratch variable initialized to zero; part of added but inactive/unused carbon-cycling
    bookkeeping in this source span.
  x10: Temporary scratch variable initialized to zero; part of added but inactive/unused carbon-cycling
    bookkeeping in this source span.
  xxx: Temporary scratch variable initialized to zero; part of added but inactive/unused carbon-cycling
    bookkeeping in this source span.
  yy: Temporary scratch variable initialized to zero; part of added but inactive/unused carbon-cycling
    bookkeeping in this source span.
  zz: Temporary scratch variable initialized to zero; part of added but inactive/unused carbon-cycling
    bookkeeping in this source span.
  xz: Temporary scratch variable initialized to zero; part of added but inactive/unused carbon-cycling
    bookkeeping in this source span.
  yz: Temporary scratch variable initialized to zero; part of added but inactive/unused carbon-cycling
    bookkeeping in this source span.
  rln: Temporary scratch variable initialized to zero; part of added but inactive/unused carbon-cycling
    bookkeeping in this source span.
  orgc_f: Temporary scratch variable initialized to zero; part of added but inactive/unused
    carbon-cycling bookkeeping in this source span.
uses:
  mgt_operations_module: This module provides the current HRU identifier used to choose which
    wetland/output record receives the fertilizer addition.
  fertilizer_data_module: This module supplies the fertilizer composition fractions for the
    selected fertilizer type, which determine how the application rate is partitioned into
    mineral N, NH3, mineral P, organic N, and organic P.
  basin_module: '`bsn_cc%cswat` gates whether the wetland fertilizer updates run at all, so
    the basin carbon-code setting controls whether this routine changes wetland state.'
  organic_mineral_mass_module: The wetland fertilizer additions are applied through the `wet`
    hydrologic output state, so this module matters because it holds the target pools being
    incremented.
  hru_module: This module holds the global HRU fertilizer summary accumulators that are updated
    after the wetland state changes so downstream management output can report applied nutrient
    totals.
  hydrograph_module: This module provides the wetland output array and its nutrient pools;
    the routine adds the fertilizer-derived nutrients directly into `wet(j)` when standing
    water is present.
---

<!-- facts:header -->

Applies fertilizer to a wet HRU/wetland when standing water is present. It updates wetland nutrient pools and records fertilizer summary amounts for later reporting.

## Bottom Line

`pl_fert_wet` handles the wet-application branch of fertilizer management. When the basin carbon option is set to the dynamic SWAT-C mode (`bsn_cc%cswat == 2`) and the HRU has standing water, the routine adds mineral N, mineral P, organic N, and organic P to the wetland output pools for the current HRU using fertilizer database fractions.

After updating the wetland state, it computes fertilizer summary variables (`fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `fertn`, `fertp`) so the calling management code can log or report the applied nutrient amounts.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during a fertilizer management operation after the caller has identified the fertilizer type, application rate, and surface-application setting. `actions` and `mgt_sched` prepare those inputs and call `pl_fert_wet` when the operation applies to a wet HRU with standing water. The results feed later management output/reporting through the wetland nutrient pools and the `fert*` summary variables.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. load current HRU and clear scratch variables | The routine sets `j = ihru` so it works on the current HRU’s wetland record, then initializes the temporary local variables (`X1`, `X8`, `X10`, `XXX`, `YY`, `ZZ`, `XZ`, `YZ`, `RLN`, `orgc_f`) to zero. The active fertilizer update does not use those scratch values in this source span. |
| 2. check carbon-code gate | The fertilizer-to-wetland transfer runs only when the basin carbon setting is `2`, which the basin module identifies as the dynamic CENTURY/SWAT-C mode. If the condition is false, the wetland pools are left unchanged. |
| 3. add mineral NO3 to wetland pool | The routine adds the fertilizer’s non-ammonium mineral N fraction to `wet(j)%no3`, using the application rate multiplied by `(1. - fertdb(ifrt)%fnh3n) * fertdb(ifrt)%fminn`. This represents the nitrate-like share of mineral nitrogen delivered to the wet HRU. |
| 4. add ammonium N to wetland pool | The routine adds the ammonium share of mineral N to `wet(j)%nh3`, using `frt_kg * fertdb(ifrt)%fnh3n * fertdb(ifrt)%fminn`. This routes the NH3 fraction of the fertilizer’s mineral nitrogen into the wetland state. |
| 5. add soluble P to wetland pool | The routine adds soluble phosphorus to `wet(j)%solp` by multiplying the application rate by `fertdb(ifrt)%fminp`. This updates the wetland’s mineral P pool with the fertilizer’s soluble fraction. |
| 6. add organic N to wetland pool | The routine adds organic nitrogen to `wet(j)%orgn` using `frt_kg * fertdb(ifrt)%forgn`. This stores the fertilizer’s organic N fraction in the wetland organic N pool. |
| 7. add organic/sediment P to wetland pool | The routine adds organic phosphorus to `wet(j)%sedp` using `frt_kg * fertdb(ifrt)%forgp`, then ends the gated block. This completes the wetland-state nutrient transfer for the fertilizer application. |
| 8. compute nitrate fertilizer summary | The routine computes `fertno3` as the applied rate times the fertilizer’s mineral N fraction times the non-NH3 share. This summary value records how much nitrate-equivalent mineral N was applied. |
| 9. compute ammonium fertilizer summary | The routine computes `fertnh3` as the applied rate times the fertilizer’s mineral N fraction times the NH3 share. This summary value records the ammonium portion of the fertilizer application. |
| 10. compute organic N summary | The routine computes `fertorgn` as the applied rate times the fertilizer’s organic N fraction. This records the organic nitrogen applied during the operation. |
| 11. compute soluble P summary | The routine computes `fertsolp` as the applied rate times the fertilizer’s soluble phosphorus fraction. This records the mineral phosphorus applied during the operation. |
| 12. compute organic P summary | The routine computes `fertorgp` as the applied rate times the fertilizer’s organic phosphorus fraction. This records the organic phosphorus applied during the operation. |
| 13. accumulate total fertilizer N and P | The routine increments the running HRU totals `fertn` and `fertp` by the applied mineral-plus-organic nitrogen and phosphorus, respectively. These accumulators provide the overall fertilizer nutrient totals for later management output or reporting. |
| 14. return to caller | The routine exits after updating the wetland state and the fertilizer summary variables, leaving the caller to continue with any additional management logging or related wet-operation routines. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:mgt_operations_module] | `mgt_operations_module state and types used for the current management operation context` | `ihru` |
| [sym:fertilizer_data_module] | `fertdb` | `fertdb(ifrt)%fnh3n, fertdb(ifrt)%fminn, fertdb(ifrt)%fminp, fertdb(ifrt)%forgn, fertdb(ifrt)%forgp` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%cswat` |
| [sym:organic_mineral_mass_module] | `organic_mineral_mass_module state and types used for the wetland mass accounting path` | `wet` |
| [sym:hru_module] | `ihru, fertn, fertp, fertnh3, fertno3, fertorgn, fertorgp, fertsolp` |  |
| [sym:hydrograph_module] | `wet` | `wet(j)%no3, wet(j)%nh3, wet(j)%solp, wet(j)%orgn, wet(j)%sedp` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wet(j)%no3` | Only when `bsn_cc%cswat == 2` | `wet(j)%no3` increases by the fertilizer’s non-ammonium mineral nitrogen share, so the current wetland record reflects nitrate-like mineral N added by the wet fertilizer operation. |
| `wet(j)%nh3` | Only when `bsn_cc%cswat == 2` | `wet(j)%nh3` increases by the fertilizer’s ammonium share of mineral nitrogen, storing the NH3 portion of the applied fertilizer in the wetland state. |
| `wet(j)%solp` | Only when `bsn_cc%cswat == 2` | `wet(j)%solp` increases by the fertilizer’s soluble phosphorus fraction, representing mineral P added to the wetland. |
| `wet(j)%orgn` | Only when `bsn_cc%cswat == 2` | `wet(j)%orgn` increases by the fertilizer’s organic nitrogen fraction, so wetland organic N reflects the applied material. |
| `wet(j)%sedp` | Only when `bsn_cc%cswat == 2` | `wet(j)%sedp` increases by the fertilizer’s organic phosphorus fraction, adding the organic/sediment P component of the application to the wetland state. |
| `fertno3` | Always, after the wetland update block | `fertno3` is set to the applied rate times the fertilizer’s non-ammonium mineral N fraction, providing a reportable nitrate-equivalent amount for this operation. |
| `fertnh3` | Always, after the wetland update block | `fertnh3` is set to the ammonium share of the fertilizer’s mineral N, providing a reportable NH3 amount for this operation. |
| `fertorgn` | Always, after the wetland update block | `fertorgn` is set to the fertilizer’s organic N application amount, so the management output can report organic nitrogen applied. |
| `fertsolp` | Always, after the wetland update block | `fertsolp` is set to the fertilizer’s soluble P application amount, so the management output can report mineral phosphorus applied. |
| `fertorgp` | Always, after the wetland update block | `fertorgp` is set to the fertilizer’s organic P application amount, so the management output can report organic phosphorus applied. |
| `fertn` | Always, after the wetland update block | `fertn` is incremented by the total applied nitrogen from the fertilizer’s mineral and organic fractions, maintaining the HRU-level fertilizer N total. |
| `fertp` | Always, after the wetland update block | `fertp` is incremented by the total applied phosphorus from the fertilizer’s soluble and organic fractions, maintaining the HRU-level fertilizer P total. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `pl_fert_wet`. The source was first added in 94b6dec with wet-fertilizer nutrient updates and summary bookkeeping. 39fabde initialized the local scratch variables to zero. 3f99111 changed the carbon-code condition from `cswat >= 0` to `cswat == 1`, and dfce092 changed that same guard again from `cswat == 1` to `cswat == 2` so the carbon activation is reserved for the dynamic SWAT-C path.

- 94b6dec introduced the wet-fertilizer routine that adds fertilizer-derived N and P to wetland pools and fills the `fert*` summary variables.
- 39fabde made the local scratch variables explicitly zero-initialized, reducing uninitialized-value risk without changing the fertilizer arithmetic.
- 3f99111 narrowed the carbon-code gate from all nonnegative values to `cswat == 1`, affecting when wetland fertilizer updates execute.
- dfce092 moved the same gate to `cswat == 2`, so the wetland fertilizer updates now run only under the dynamic CENTURY/SWAT-C setting.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_fert_wet' has no extracted documentation comment.
- algorithm_steps revised: expanded the algorithm from 2 nodes to 14 source-backed steps to reflect the actual wetland update and summary calculations.
- Source uncertainty note: `organic_mineral_mass_module` had no resolved candidate refs in the context packet, so its outside_state entry is described at module level only.
