---
kind: procedure
symbol: nut_np_flow
title: nut_np_flow
status: filled
source_hash: 1724f3f9b8a6ecdf
version_label: SWAT+ 62.0.0
args:
  c_a: C_A is the amount of carbon available in pool A at the start of the timestep; it sets
    the scale for proportional nutrient transfer and also gates the calculation if the pool
    is essentially empty.
  e_a: E_A is the amount of nutrient E in pool A at the start of the timestep; it supplies
    the nutrient mass that is proportionally moved and is also checked for near-zero values
    before any transfer is computed.
  cetob: CEtoB is the C:E ratio required or allowed by pool B; it is the target used to decide
    whether the transferred material needs immobilization or can release excess nutrient as
    mineralization.
  c_atob: C_AtoB is the carbon flow from pool A to pool B; it determines the size of the transfer
    and is the main driver for both the nutrient flow and the ratio check.
  co2froma: CO2fromA is the CO2 emitted during decomposition of pool A; it controls whether
    any extra nutrient is associated with respiration losses and added to mineralization.
  e_atob: E_AtoB is the routine's computed nutrient flow from pool A to pool B; the caller
    receives this value after it may be reduced for mineralization adjustments.
  imm_atob: IMM_AtoB is the amount of nutrient immobilized to raise the transferred material
    to the C:E ratio required by pool B when the initial transfer is too nutrient-poor.
  mnr_atob: MNR_AtoB is the amount of nutrient mineralized away from the A-to-B transfer when
    the transfer already meets or exceeds pool B's C:E requirement, plus any nutrient released
    with CO2 loss.
locals:
  efromco2: Holds the nutrient amount associated with CO2 respiration from pool A decomposition;
    it is accumulated into mineralization at the end, although the assignment later uses the
    uppercase symbol EFCO2 in the source and that appears inconsistent with the lowercase
    local declaration.
  efco2: Declared as the same respiration-linked nutrient adjustment as EfromCO2, but the
    visible source never assigns or uses this lowercase variable; the code instead references
    EFCO2 at line 61, so the exact intended variable naming is uncertain.
---

<!-- facts:header -->

Computes nitrogen or phosphorus transfers tied to carbon flow from pool A to pool B, including immobilization or mineralization needed to match the receiving pool's C:E ratio.

## Bottom Line

nut_np_flow takes a carbon pool balance for pool A, the amount of nutrient E in that pool, the carbon flow from A to B, the target C:E ratio for pool B, and any CO2 loss from pool A. It returns the nutrient flow to pool B plus any immobilization or mineralization adjustments required to keep the transferred material consistent with the receiving pool's C:E constraint.

The routine is a small mass-balance helper used during humus and microbial pool transformations. It first scales nutrient transfer with carbon transfer, then corrects that transfer based on whether the A-to-B material is too nutrient-poor or nutrient-rich relative to CEtoB, and finally adds any nutrient released with CO2 respiration.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the carbon/nutrient transformation workflow after cbn_zhang2 has already computed pool carbon flows and CO2 losses for a specific source-to-destination transfer. Its outputs feed the downstream accounting of nutrient movement, immobilization, and mineralization for that pool transition, which in turn affects the updated pool state and nutrient balance.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize outputs | Set the nutrient transfer, immobilization, mineralization, and respiration-linked adjustment variables to zero before any case-specific logic runs. |
| 2. skip empty transfers | If pool A has essentially no nutrient, no carbon flow to B, or no carbon in pool A, exit immediately because there is no meaningful transfer to compute. |
| 3. scale nutrient with carbon | Compute the base nutrient flow to pool B by assuming nutrient moves in proportion to the carbon flow from pool A to pool B. |
| 4. handle CO2-linked nutrient | If CO2fromA is negative, do not add any respiration-linked nutrient; otherwise compute nutrient released with CO2 loss as the same fraction of E_A as the CO2 loss is of C_A. |
| 5. test recipient ratio | Compare the transferred material's C:E ratio with the ratio allowed by pool B; if it is too high, compute immobilization as the extra nutrient needed to satisfy CEtoB. |
| 6. mineralize excess nutrient | When the transferred material already contains enough nutrient for pool B, compute the surplus nutrient as mineralization and subtract that surplus from the A-to-B nutrient flow. |
| 7. add respiration-linked mineralization | Add the nutrient released with CO2 respiration to the mineralization total so the caller gets the full nutrient loss associated with the transformation. |
| 8. return results | Return the adjusted nutrient transfer and the immobilization/mineralization totals to the caller. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

The routine was introduced in df07e3f as a new helper for calculating nutrient flow from pool A to pool B along with immobilization and mineralization. 94b6dec carried the same algorithm into the later source snapshot without changing behavior, 39fabde initialized the two local respiration-adjustment variables to zero on declaration, and 889136d made only comment fixes while leaving the computation unchanged.

- df07e3f added the full nut_np_flow subroutine: proportional nutrient transfer, the CO2-linked nutrient adjustment, the CEtoB ratio test, and the immobilization/mineralization branch.
- 39fabde changed the local declarations so EfromCO2 and efco2 start at 0. instead of being uninitialized.
- 889136d only corrected typos in comments; the executable logic stayed the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- The source appears to contain a naming inconsistency at line 61: the local declarations use EfromCO2 and efco2, but the final accumulation references EFCO2. The intended variable is uncertain from the visible lines alone.
