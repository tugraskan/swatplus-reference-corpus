---
kind: procedure
symbol: smp_bmpfixed
title: smp_bmpfixed
status: filled
source_hash: 4ae501ba67383a78
version_label: SWAT+ 62.0.0
locals:
  j: Loop/index scratch variable for the active HRU. It is initialized to 0, then assigned
    `ihru` so the routine can use `j` as the array subscript for the current HRU’s state values.
uses:
  hru_module: This module holds both the active HRU index and the pollutant state arrays that
    the routine modifies, plus the HRU landuse metadata (`hru(j)%lumv`) that contains the
    BMP removal fractions. Without `hru_module`, the routine would have no current HRU record
    to look up and no state variables to update.
---

<!-- facts:header -->

Applies fixed BMP removal efficiencies to an HRU's sediment and nutrient loads. It scales the day’s pollutant loads down using the HRU’s BMP parameters.

## Bottom Line

smp_bmpfixed is a small adjustment routine that reduces the current HRU’s sediment and nutrient loads by fixed BMP removal fractions stored on the HRU landuse object. It does not change surface runoff, which the inline note says is left alone to protect the water balance.

The routine reads the active HRU index from `ihru`, uses `hru(j)%lumv%bmp_*` efficiencies to scale sediment, phosphorus, and nitrogen state variables in place, and then returns. The updated loads are the values later model code carries forward for routing and accounting.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `hru_control` after other in-field pollutant-reduction logic, specifically when `hru(j)%lumv%bmp_flag == 1` at line 618. `hru_control` prepares the call by setting the current HRU context through `ihru`/`j` and by operating on the shared HRU state arrays. The results matter for the remainder of HRU processing because the reduced sediment and nutrient loads are the values that downstream routing and output accounting use for that HRU day.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Set the working HRU index from `ihru`. | Copies the active HRU number into local variable `j` so every array update targets the current HRU record. |
| 2. Reduce sediment yield by the BMP sediment removal fraction. | Multiplies `sedyld(j)` by `1. - hru(j)%lumv%bmp_sed`, lowering the sediment load according to the fixed BMP efficiency. |
| 3. Reduce particulate phosphorus pools by the BMP particulate-P fraction. | Scales `sedminpa(j)`, `sedminps(j)`, and `sedorgp(j)` by `1. - hru(j)%lumv%bmp_pp` so all sediment-associated phosphorus pools are reduced together. |
| 4. Reduce soluble phosphorus in surface runoff by the BMP soluble-P fraction. | Multiplies `surqsolp(j)` by `1. - hru(j)%lumv%bmp_sp` to apply the fixed removal to dissolved phosphorus. |
| 5. Reduce particulate nitrogen by the BMP particulate-N fraction. | Scales `sedorgn(j)` by `1. - hru(j)%lumv%bmp_pn`, lowering the sediment-bound organic nitrogen load. |
| 6. Reduce soluble nitrogen pools by the BMP soluble-N fraction. | Multiplies `surqno3(j)` and `latno3(j)` by `1. - hru(j)%lumv%bmp_sn`, applying the fixed BMP removal to nitrate in both surface and lateral flow. |
| 7. Return to the caller. | Ends the subroutine after updating the shared HRU state arrays in place. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `sedyld, hru, sedminpa, sedminps, sedorgp, surqsolp, sedorgn, surqno3, latno3, ihru` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sedyld(j)` | When `hru(j)%lumv%bmp_flag == 1` and the routine is called for the current `ihru`. | `sedyld(j)` is overwritten with a reduced value equal to the prior sediment yield times `1 - bmp_sed`, representing fixed BMP sediment removal for that HRU day. |
| `sedminpa(j)` | When the routine processes the current HRU and applies the particulate phosphorus reduction block. | `sedminpa(j)` is overwritten with a reduced active-mineral phosphorus load, so the HRU’s sediment-associated P is lower after BMP adjustment. |
| `sedminps(j)` | When the routine processes the current HRU and applies the particulate phosphorus reduction block. | `sedminps(j)` is overwritten with a reduced stable-mineral phosphorus load, so the HRU’s sediment-associated P is lower after BMP adjustment. |
| `sedorgp(j)` | When the routine processes the current HRU and applies the particulate phosphorus reduction block. | `sedorgp(j)` is overwritten with a reduced organic phosphorus load, representing fixed BMP removal of sediment-bound P. |
| `surqsolp(j)` | When the routine processes the current HRU and applies the soluble phosphorus reduction block. | `surqsolp(j)` is overwritten with a reduced soluble phosphorus load in surface runoff, leaving runoff volume unchanged. |
| `sedorgn(j)` | When the routine processes the current HRU and applies the particulate nitrogen reduction block. | `sedorgn(j)` is overwritten with a reduced organic nitrogen load, representing BMP removal of sediment-bound N. |
| `surqno3(j)` | When the routine processes the current HRU and applies the soluble nitrogen reduction block. | `surqno3(j)` is overwritten with a reduced nitrate load in surface runoff, reflecting fixed BMP removal of dissolved N. |
| `latno3(j)` | When the routine processes the current HRU and applies the soluble nitrogen reduction block. | `latno3(j)` is overwritten with a reduced nitrate load in lateral flow, so soluble nitrogen leaving the HRU is lowered consistently across flow paths. |

## File I/O

<!-- facts:io -->


## Lineage

`smp_bmpfixed` was introduced in df07e3f with its fixed-BMP removal logic and inline purpose/input/output comments. Commit 39fabde only initialized the local index variable `j` to 0, and f1e61a3 made whitespace-only tab-to-space edits without changing behavior.

- df07e3f added the routine and its in-place load reductions for sediment, phosphorus, and nitrogen using the HRU BMP fractions.
- 39fabde changed only the local declaration `integer :: j` to `integer :: j = 0`, an initialization change with no documented algorithmic effect.
- f1e61a3 adjusted indentation on the assignment lines but left the mathematical updates unchanged.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'smp_bmpfixed' has no extracted documentation comment.
