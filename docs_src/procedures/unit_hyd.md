---
kind: procedure
symbol: unit_hyd
title: unit_hyd
status: filled
source_hash: 0d4a2444f07b9345
version_label: SWAT+ 62.0.0
args:
  tc: '`tc` is the time of concentration for the current subbasin or routing unit. The routine
    uses it to derive the unit-hydrograph base time `tb`, peak time `tp`, and the sampling
    interval needed to build `uh`.'
  uh: '`uh` is the output hydrograph table filled by this routine. It receives the computed
    unit-hydrograph ordinates for each day-lag row and each routing time step, then is normalized
    before returning.'
locals:
  ql: Stores the previous hydrograph ordinate so the trapezoidal accumulation can average
    the current and previous `q` values when building and summing `uh`.
  sumq: Accumulates the total area under the unnormalized unit hydrograph. It is used at the
    end to divide every `uh(i,istep)` by the total and make the hydrograph sum to 1.
  tb: Holds the unit-hydrograph base time in hours, computed from `tc` plus the basin adjustment
    `bsn_prm%tb_adj` and capped at 48 hours.
  tp: Holds the hydrograph peak time in hours, set as a fixed fraction of `tb` and used as
    the split between rising and falling limbs.
  i: Counts the subdaily increments used to refine the hydrograph calculation within each
    routing time step.
  q: Stores the current hydrograph ordinate at the current `t_tot` sample, before it is averaged
    into `uh` and added to `sumq`.
  max: Provides the lower-bound clamp for `q` through the intrinsic `max` call, ensuring negative
    tail values are reset to zero.
  istep: Indexes the model routing time steps across which the unit hydrograph is built and
    stored.
  iday: Indexes the day-lag rows of `uh`, letting the routine fill up to two days of hydrograph
    values.
  t_inc: Sets how many subdaily increments are evaluated inside each model time step, increasing
    resolution near the peak of the hydrograph.
  ts_base: Stores the number of model time steps represented across the hydrograph base time
    `tb`, used to scale subdaily sampling density.
  t_inc_hr: Holds the hours represented by each subincrement inside a routing time step, derived
    from `time%dtm` and `t_inc`.
  t_tot: Tracks cumulative elapsed hydrograph time in hours as the routine steps through each
    subincrement and time step.
uses:
  basin_module: The basin module supplies the control flag and parameters that shape the hydrograph.
    `bsn_cc%uhyd` selects triangular versus gamma form, `bsn_prm%tb_adj` shifts the base time,
    and `bsn_prm%uhalpha` controls the gamma-curve sharpness.
  time_module: The time module defines the routing resolution this routine must honor. `time%dtm`
    determines the subincrement size in hours, and `time%step` sets how many routing steps
    are filled in each hydrograph row.
---

<!-- facts:header -->

Builds a subdaily unit hydrograph from watershed time of concentration. It supports either a triangular or gamma-shaped hydrograph and normalizes the result for later routing.

## Bottom Line

unit_hyd constructs a unit hydrograph array `uh` for a given time of concentration `tc`. It derives the hydrograph base time and peak time from basin parameters, then evaluates either a triangular curve or a gamma-function curve at subdaily increments controlled by the model time step.

The routine accumulates and normalizes the ordinates so downstream routing code can distribute direct runoff through the chosen unit-hydrograph shape. Its behavior is switched by `bsn_cc%uhyd`, and the gamma option uses `bsn_prm%uhalpha` while the base time is adjusted by `bsn_prm%tb_adj`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during routing setup when `time%step > 1`. It is called by `unit_hyd_ru_hru`, which supplies the per-HRU or per-RU time of concentration, and its normalized `uh` output is then used by later runoff-routing behavior that distributes flow through the unit hydrograph.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize and derive base timing | Zeroes the accumulation variables, clears the output array, computes the hydrograph base time `tb` from `tc` plus the basin adjustment, caps `tb` at 48 hours, derives peak time `tp`, estimates a base-step count from `tb` and `time%dtm`, enforces a minimum of one step, then computes the subincrement duration `t_inc_hr`. |
| 2. sweep hydrograph days and routing steps | Loops over two day-lag rows and all routing time steps so the routine can fill the hydrograph table across the full output window. |
| 3. refine each step with subincrements | Subdivides each routing step into `t_inc` pieces, advances `t_tot` by `t_inc_hr` each time, and uses those finer samples to evaluate the hydrograph near its peak. |
| 4. compute a triangular hydrograph when enabled | If `bsn_cc%uhyd == 0`, computes `q` from a triangular unit hydrograph: rising limb before `tp` and falling limb after `tp`. |
| 5. compute a gamma hydrograph when enabled | If `bsn_cc%uhyd == 1`, computes `q` from the gamma-function form using `bsn_prm%uhalpha` and `exp`. |
| 6. clamp and accumulate the sampled ordinate | Clamps `q` to zero or greater, adds the trapezoidal average of `q` and `ql` into `uh(iday,istep)`, accumulates the same contribution into `sumq`, and saves `q` in `ql` for the next subincrement. |
| 7. stop early after the tail decays | Exits the inner time-step loop once `q` falls below `1.e-4`, because the hydrograph tail has become negligible. |
| 8. normalize the hydrograph | Divides each stored hydrograph ordinate by `sumq` so the final `uh` array is normalized to unit area. |
| 9. return to caller | Returns the normalized hydrograph to the caller and ends the subroutine. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_prm, bsn_cc` | `bsn_prm%tb_adj, bsn_cc%uhyd, bsn_prm%uhalpha` |
| [sym:time_module] | `time` | `time%dtm, time%step` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `unit_hyd`. df07e3f introduced the subroutine with its triangular and gamma unit-hydrograph logic, the basin and time module dependencies, and the normalization loop. 94b6dec preserved that implementation while adding the source file to the imported codebase. 39fabde initialized the local scalars and counters, and 2ee1889 removed unused locals (`xi`, `itb`) and an obsolete `hru_module` comment during cleanup.

- df07e3f added the full `unit_hyd` implementation, including timing setup from `tc`, the `bsn_cc%uhyd` branch for triangular versus gamma hydrographs, accumulation into `uh`, and final normalization by `sumq`.
- 94b6dec imported the same routine into the repository without changing the algorithm shown in the diff.
- 39fabde initialized local variables such as `ql`, `sumq`, `tb`, `tp`, `i`, `q`, `istep`, `iday`, `t_inc`, `ts_base`, `t_inc_hr`, and `t_tot`, and adjusted the `tb` line formatting; these changes reduced uninitialized-state risk.
- 2ee1889 removed unused locals `xi` and `itb` and deleted the stale `!use hru_module, only : itb` comment.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'unit_hyd' has no extracted documentation comment.
- algorithm_steps revised: merged the initialization and time-setup statements into a single step and split the hydrograph evaluation into explicit branch/accumulate/normalize steps for readability.
- Callee `uh` is source-parsing uncertain because the extracted call graph lists it as a callee even though the source shows `uh` as the output argument being assigned.
