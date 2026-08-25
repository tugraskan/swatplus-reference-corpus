---
kind: procedure
symbol: hru_urb_bmp
title: hru_urb_bmp
status: filled
source_hash: 35d46da4cfbd1983
version_label: SWAT+ 62.0.0
locals:
  j: '`j` is the active HRU index. The routine copies `ihru` into `j` and then uses `j` to
    read and update the current HRU’s runoff, concentration limits, and load variables.'
  xx: '`xx` is the conversion factor from runoff depth in mm to a concentration scaling term
    (`100. / qdr(j)`). It is reused to translate between concentration limits in ppm and the
    mass-per-area quantities stored in the HRU state.'
  sedppm: '`sedppm` holds the computed sediment concentration for the current HRU runoff event,
    in ppm, based on `sedyld(j)`, `qdr(j)`, and `hru(j)%area_ha`.'
  solnppm: '`solnppm` holds the total dissolved inorganic nitrogen concentration for the runoff
    event, computed from `surqno3(j) + latno3(j)` and the runoff scaling factor.'
  solpppm: '`solpppm` holds the soluble phosphorus concentration in runoff, computed from
    `surqsolp(j)` and the runoff scaling factor.'
  sednppm: '`sednppm` holds the organic nitrogen concentration associated with sediment, computed
    from `sedorgn(j)` and the runoff scaling factor.'
  sedpppm: '`sedpppm` holds the phosphorus concentration associated with sediment and mineral
    sediment-bound phosphorus, computed from `sedorgp(j) + sedminpa(j) + sedminps(j)` and
    the runoff scaling factor.'
uses:
  hru_module: The `hru_module` state supplies the current HRU index, runoff depth, HRU area,
    urban BMP concentration limits, and the sediment/nutrient loads that this routine tests
    and potentially reduces. Without those module arrays and the `hru(j)%area_ha` geometry,
    `hru_urb_bmp` cannot convert between event concentrations and mass-based HRU loads.
---

<!-- facts:header -->

Checks urban HRU runoff concentrations against BMP targets and caps sediment and nutrient loads when they exceed those limits.

## Bottom Line

This subroutine is a load-limiting filter for the current HRU. It converts the HRU’s water depth to a ppm scaling factor, compares sediment and nutrient concentrations against the urban BMP thresholds stored in `hru_module`, and reduces the corresponding exported loads when they are too high.

It only acts when runoff depth is large enough to matter (`qdr(j) > 0.1`) and uses the current HRU index (`ihru`) to update the active HRU’s sediment yield, surface nitrate, lateral nitrate, surface soluble phosphorus, organic nitrogen, and mineral phosphorus pools. Those adjusted values then flow back into later HRU routing and output calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `hru_control` after runoff-related load variables have been assembled for the current HRU. `hru_control` first computes the combined concentration check value (`sed_con + soln_con + solp_con + orgn_con + orgp_con`) and then calls `hru_urb_bmp` when that total is nontrivial; the updated loads then affect later HRU routing and outflow behavior in the same control step.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check runoff depth | The routine only proceeds when runoff depth for the active HRU is greater than 0.1 mm. If runoff is too small, it skips all concentration checks and returns without changing the HRU loads. |
| 2. convert runoff to scaling factor | It computes `xx = 100. / qdr(j)`, which serves as the ppm-to-load conversion factor for the current runoff event. |
| 3. compute sediment concentration | It converts the current sediment yield into a runoff concentration using the HRU area and stores the result in `sedppm`. |
| 4. compute nutrient concentrations | It computes event concentrations for dissolved inorganic nitrogen, soluble phosphorus, organic nitrogen, and sediment-associated phosphorus from the current HRU load variables. |
| 5. cap sediment yield if needed | If the sediment concentration exceeds the BMP limit `sed_con(j)`, it reduces `sedyld(j)` so the event concentration matches the limit. |
| 6. cap nitrate loads if needed | If dissolved inorganic nitrogen exceeds `soln_con(j)`, it reduces both surface nitrate and lateral nitrate to the same capped concentration. |
| 7. cap soluble phosphorus if needed | If soluble phosphorus exceeds `solp_con(j)`, it lowers `surqsolp(j)` to the limit-based load. |
| 8. cap organic nitrogen if needed | If sediment-associated organic nitrogen exceeds `orgn_con(j)`, it reduces `sedorgn(j)` to the limit-based load. |
| 9. cap sediment phosphorus pools if needed | If sediment-associated phosphorus exceeds `orgp_con(j)`, it reduces the sediment organic nitrogen and both mineral phosphorus pools to the same capped concentration-based load. |
| 10. return | The subroutine ends after the HRU state has been conditionally adjusted for urban BMP concentration limits. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `sedyld, qdr, hru, surqno3, latno3, surqsolp, sedorgn, sedorgp, sedminpa, sedminps, sed_con, soln_con, solp_con, orgn_con, orgp_con, ihru` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sedyld(j)` | Only when `qdr(j) > 0.1` and `sedppm > sed_con(j)`. | `sedyld(j)` is reduced so the event sediment concentration does not exceed the urban BMP threshold. This keeps the HRU’s sediment export consistent with the allowed concentration limit. |
| `surqno3(j)` | Only when `qdr(j) > 0.1` and `solnppm > soln_con(j)`. | `surqno3(j)` is lowered to the same capped concentration as `latno3(j)` so the combined dissolved inorganic nitrogen export meets the BMP limit. |
| `latno3(j)` | Only when `qdr(j) > 0.1` and `solnppm > soln_con(j)`. | `latno3(j)` is lowered together with surface nitrate because the routine treats the total dissolved inorganic nitrogen load as one capped concentration target. |
| `surqsolp(j)` | Only when `qdr(j) > 0.1` and `solpppm > solp_con(j)`. | `surqsolp(j)` is reduced so surface soluble phosphorus export does not exceed the BMP concentration threshold. |
| `sedorgn(j)` | Only when `qdr(j) > 0.1` and `sednppm > orgn_con(j)`. | `sedorgn(j)` is reduced so sediment-associated organic nitrogen meets the BMP limit. |
| `sedminpa(j)` | Only when `qdr(j) > 0.1` and `sedpppm > orgp_con(j)`. | `sedminpa(j)` is reduced with the other sediment phosphorus pools so the total sediment-linked phosphorus concentration is capped. |
| `sedminps(j)` | Only when `qdr(j) > 0.1` and `sedpppm > orgp_con(j)`. | `sedminps(j)` is reduced with the other sediment phosphorus pools so the total sediment-linked phosphorus concentration is capped. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was added in df07e3f as a new urban BMP limiter. Commit 39fabde initialized the local working variables to zero at declaration, and f1e61a3 only reformatted indentation and spacing without changing the routine’s logic; the latest resolved diff still shows the same runoff gate and concentration-capping behavior.

- df07e3f introduced the full `hru_urb_bmp` subroutine, including the runoff-depth gate, ppm conversions, and all sediment/nutrient capping assignments.
- 39fabde changed the local variable declarations to initialize `j`, `xx`, and the concentration variables at declaration time.
- f1e61a3 made whitespace-only edits and did not alter the routine’s behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'hru_urb_bmp' has no extracted documentation comment.
