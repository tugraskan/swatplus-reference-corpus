---
kind: procedure
symbol: ionic_strength
title: ionic_strength
status: filled
source_hash: 255e3958fc6acc9a
version_label: SWAT+ 62.0.0
args:
  is_temp: Output slot for the computed ionic strength; the routine overwrites `IS_temp` with
    the 0.5 charge-weighted sum of the seven concentrations.
  a: Calcium concentration term used in the ionic-strength sum; it is multiplied by a charge-squared
    weight of 4.
  b: Sulfate concentration term used in the ionic-strength sum; it is multiplied by a charge-squared
    weight of 4.
  c: Carbonate concentration term used in the ionic-strength sum; it is multiplied by a charge-squared
    weight of 1.
  d: Bicarbonate concentration term used in the ionic-strength sum; it is multiplied by a
    charge-squared weight of 1.
  e: Magnesium concentration term used in the ionic-strength sum; it is multiplied by a charge-squared
    weight of 4.
  f: Sodium concentration term used in the ionic-strength sum; it is multiplied by a charge-squared
    weight of 1.
  g: Potassium concentration term used in the ionic-strength sum; it is multiplied by a charge-squared
    weight of 1.
locals:
  charbal: 'Seven-element charge array holding the ion valences used to square the charge
    term for each input concentration: 2, -2, -2, -1, 2, 1, and 1.'
uses:
  salt_data_module: The module is part of the routine's declared dependencies, so it may provide
    shared salt-chemistry data or constants used by the surrounding file even though this
    subroutine's extracted lines do not reference a named member directly.
---

<!-- facts:header -->

Computes ionic strength from seven ion concentrations using fixed charge weights for the salt chemistry routines.

## Bottom Line

Ionic_Strength calculates a single ionic-strength value from the supplied ion concentrations. It applies the standard 0.5 sum of concentration times squared charge, using fixed charge factors for calcium, sulfate, carbonate, bicarbonate, magnesium, sodium, and potassium.

The result is written back through `IS_temp`, and the calling salt chemistry routines then copy that value into `IonStr` and `I_Prep_in` to drive later activity-coefficient calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs immediately after the caller routines convert dissolved-ion amounts into concentration terms. `salt_chem_aqu`, `salt_chem_hru`, and `salt_chem_soil_single` each prepare calcium, sulfate, carbonate, bicarbonate, magnesium, sodium, and potassium concentrations, then call `Ionic_Strength` before copying the returned value into `IonStr` and `I_Prep_in` for later activity-coefficient and equilibrium chemistry calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Declare the local charge array. | Defines `CharBal(7)` and initializes it with the fixed ion charges 2, -2, -2, -1, 2, 1, and 1. |
| 2. Compute ionic strength. | Calculates `IS_temp` as 0.5 times the sum of each input concentration multiplied by the square of its corresponding charge factor. |
| 3. Return to the caller. | Exits the subroutine after leaving the computed ionic strength in `IS_temp` for the caller to use. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:salt_data_module] | `module `salt_data_module`` | `Imported via `use salt_data_module`, but no specific symbols from the module are referenced in the extracted source lines.` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows one behavior-changing commit for this source span. The initial import commit `df07e3f` added `Ionic_Strength` as part of the new salt chemistry file, and later `2ee1889` did not change the formula itself but only modernized the terminator to `end subroutine Ionic_Strength` along with similar cleanup elsewhere in the file. `39fabde` only reformatted/initialized unrelated declarations in the same file and did not alter this routine's logic.

- `df07e3f` introduced the routine in `salt_chem_hru.f90` with the current 0.5 charge-squared concentration sum.
- `2ee1889` changed only the subroutine-ending syntax for `Ionic_Strength`; the calculation lines remained the same.

## Review Notes

- No direct file I/O was extracted for this procedure.
- info: weak_doc: Procedure 'Ionic_Strength' documentation is very short.
- The extracted source lines show `use salt_data_module`, but no named symbol from that module appears in the routine body.
