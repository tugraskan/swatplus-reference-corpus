---
kind: procedure
symbol: ee
title: ee
status: filled
source_hash: 5a89ff97113da786
version_label: SWAT+ 62.0.0
args:
  tk: '`tk` is the air temperature in degrees C used as the independent variable in the saturation
    vapor pressure equation; changing it changes the returned vapor pressure through both
    the numerator and denominator of the exponential expression.'
locals:
  ee: '`ee` is the function result. It starts as 0.0, then temporarily holds the logarithmic
    argument of the vapor-pressure equation before being replaced by the exponentiated saturation
    vapor pressure in kPa.'
---

<!-- facts:header -->

Returns saturation vapor pressure for a given air temperature using the SWAT water-vapor equation.

## Bottom Line

`ee` computes saturation vapor pressure from mean air temperature `tk`. It is a small climate helper used anywhere the model needs vapor pressure as an intermediate meteorological quantity.

The routine protects against the singular case `tk + 237.3 = 0` by leaving the result at zero; otherwise it evaluates the exponential form of the SWAT saturation-vapor-pressure relation.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`ee` runs as a reusable climate calculation inside routines that need vapor pressure values. `cli_rhgen` prepares a mean temperature from monthly maximum and minimum temperatures, then calls `ee` to convert dew point and mean temperature into relative humidity inputs. `et_pot` prepares air temperature `w%tave` and uses `ee` to derive actual vapor pressure, vapor pressure deficit, and the slope of the saturation vapor pressure curve that feed potential evapotranspiration calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the return value to zero. | The function starts with `ee = 0.` so a safe default is available if the temperature check fails. |
| 2. Check for the valid denominator in the saturation-vapor formula. | The guard `if (tk + 237.3 /= 0.) then` prevents division by zero before evaluating the vapor-pressure equation. |
| 3. Compute the exponential argument from temperature. | The routine forms `(16.78 * tk - 116.9) / (tk + 237.3)`, which is the logarithmic term for SWAT saturation vapor pressure. |
| 4. Convert the argument to saturation vapor pressure. | The intrinsic `Exp` turns the logarithmic term into saturation vapor pressure in kPa. |
| 5. Return the computed value. | Execution exits the function with `ee` holding either the computed vapor pressure or zero if the guard condition failed. |

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


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:2.3.2 | Saturation vapor pressure e^o | $e^o=exp[\frac{16.78*\overline T_{av}-116.9}{\overline T_{av}+237.3}]$ | ee = Exp((16.78*tk-116.9)/(tk+237.3)); the SWAT saturation-vapor-pressure relation. |
| 1:2.3.1 | Relative humidity from vapor pressures | $R_h=\frac{e}{e^o}$ | Verified against SWAT+ 62.0.0 (ee.f90). |
| 1:2.3.3 | Actual vapor pressure e = R_h*e^o | $e=R_h*e^o$ | Verified against SWAT+ 62.0.0 (ee.f90). |

## Lineage

Resolved lineage shows three changes: `df07e3f` added `ee.f90` with the saturation vapor pressure calculation; `94b6dec` preserved the same logic while importing the file from bitbucket; and `2ee1889` changed the function footer from a bare `end` to `end function ee` without altering the calculation.

- df07e3f introduced the function and its zero-initialized guarded exponential saturation-vapor calculation.
- 94b6dec kept the same behavior while carrying the file into the tracked source tree.
- 2ee1889 made only a syntactic cleanup at the function end; the computed vapor pressure logic remained unchanged.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ee' has no extracted documentation comment.
