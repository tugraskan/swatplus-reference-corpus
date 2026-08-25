---
kind: procedure
symbol: flow_dur_curve
title: flow_dur_curve
status: filled
source_hash: df15899d2ab396d9
version_label: SWAT+ 62.0.0
locals:
  sum: Running accumulator used to sum daily or annual flow values before computing means.
  iyr: Year-loop index used when iterating over annual flow-duration curves and building the
    simulation-median curve.
  next: Pointer/index to the next node in the linked list while inserting or traversing sorted
    flow values.
  npts: Number of existing items already in the linked list before inserting the current daily
    or annual value.
  ipts: Loop counter used to walk through existing linked-list positions during insertion.
  iprv: Previous linked-list node index, used when splicing the current item into the sorted
    chain.
  mle: Tracks the current linked-list tail (minimum element for the descending daily list
    and last element for the annual list) so new smallest values can be appended.
  nprob: Index of the current flow-duration probability point being filled from the standard
    27-point schedule.
  iday: Day counter used when scanning daily flows to collect yearly probabilities and compute
    annual means.
  mfe: Tracks the current linked-list head (maximum element for the descending daily list
    and first element for the annual list) so new largest values can be inserted at the front.
  iyr_ch: Helper index that identifies the middle year position when taking the median annual
    curve from an odd or even number of years.
uses:
  time_module: The `time_module` flags determine when the routine should finalize a yearly
    curve (`time%end_yr`) and when it should finalize the simulation-wide median curve (`time%end_sim`).
    The current day and year counters (`time%day`, `time%yrs`, `time%nbyr`) also control which
    linked-list node is updated and which annual record receives results.
  hydrograph_module: The `hydrograph_module` holds the object-specific hydrograph and all
    flow-duration storage that this routine reads and updates. In particular, `ob(icmd)%hd(1)%flo`
    supplies the day's flow, `ob(icmd)%fdc_ll` and `ob(icmd)%fdc_lla` store the sorted daily
    and annual linked lists, `ob(icmd)%fdc` holds annual and median curve results, and `ob(icmd)%flash_idx`
    carries the flashiness-index accumulators and output value.
---

<!-- facts:header -->

Builds and summarizes flow duration curves for a channel object. It ranks daily flows within each year, then derives annual and simulation-median flow-duration statistics and a flashiness index for output.

## Bottom Line

This routine updates the flow-duration-curve data stored on the current object `ob(icmd)` as the simulation advances one day at a time. Each day it inserts the current flow (`ob(icmd)%hd(1)%flo`) into a linked list so the year-to-date flows stay sorted, which lets the model sample annual flow-duration percentiles later.

At year end it extracts the 27 standard duration-curve points, computes annual mean/max/min, and resets the yearly linked-list heads for the next year. At simulation end it sorts the annual curves across years, computes the median flow-duration curve plus overall mean/max/min, converts those flows from volume per day to m3/s, computes the flashiness index, and writes a summary line to unit 6000.

## Arguments

<!-- facts:arguments -->

## Where It Fits

The routine runs from `command` when flow-duration output is enabled and the current object is a channel (`pco%fdcout == "y"` and `ob(icmd)%typ == "chandeg"`). `command` provides the current object state and daily hydrograph flow before the call; afterward, later channel output logic can use the updated `ob(icmd)%fdc` and `ob(icmd)%flash_idx` values, and the summary line written to unit 6000 records the final statistics.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Insert today’s flow into the yearly sorted linked list | Store the current day’s flow in `ob(icmd)%fdc_ll(time%day)%val`, walk the existing daily linked list, and splice the new node into the proper descending position. If the new value becomes the first or last node, update `ob(icmd)%fdc%mfe` or `ob(icmd)%fdc%mle` accordingly. |
| 2. Capture annual probability points at year end | When `time%end_yr == 1`, traverse the daily linked list in the standard `fdc_days` order, copy the 27 percentile values into `ob(icmd)%fdc%yr(time%yrs)%p`, compute the yearly mean, and record the yearly max and min from the linked-list head and tail. |
| 3. Reset yearly list heads for the next year | After storing the annual curve statistics, reset `ob(icmd)%fdc%mfe` and `ob(icmd)%fdc%mle` to 1 so the next year starts with a fresh linked-list head and tail. |
| 4. Sort annual curves across years at simulation end | When `time%end_sim == 1`, loop over the 27 probability points and, for each point, insert the annual value for each year into `ob(icmd)%fdc_lla` as a linked list sorted by annual percentile value. This prepares an ordered year ranking for median selection. |
| 5. Compute simulation-wide mean, max, and min of annual curves | Accumulate yearly means into `sum`, track the largest yearly max with `Max`, and track the smallest yearly min with `amin1`, then store the simulation-average annual mean in `ob(icmd)%fdc%p_md%mean`. |
| 6. Select the median annual value for each probability point | Traverse the sorted annual linked list to find the middle year(s). For an odd number of years, copy the middle year’s percentile value into `ob(icmd)%fdc%p_md%p(nprob)`; for an even number of years, average the two middle yearly values. |
| 7. Convert stored flow statistics to m3/s | Divide the median mean, percentile array, maximum, and minimum by 86400 to convert from daily volume units to discharge units. |
| 8. Compute the flashiness index | If enough cumulative flow has been accumulated, compute `ob(icmd)%flash_idx%index` as `sum_q_q1 / sum_q`. |
| 9. Write the summary output record | Write the object type, property number, area, flashiness index, and median flow-duration statistics to unit 6000 for downstream reporting. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:time_module] | `time` | `time%day, time%end_yr, time%yrs, time%end_sim, time%nbyr` |
| [sym:hydrograph_module] | `ob, hd, fdc_days, icmd, fdc_npts` | `ob(icmd)%fdc_ll, ob(icmd)%hd(1)%flo, ob(icmd)%fdc%mfe, ob(icmd)%fdc_ll(next)%val, ob(icmd)%fdc_ll(iprv)%next, ob(icmd)%fdc_ll(next)%next, ob(icmd)%fdc%mle, ob(icmd)%fdc_ll(mle)%next, ob(icmd)%fdc%yr, ob(icmd)%fdc_ll(iday)%val, ob(icmd)%fdc_ll(mfe)%val, ob(icmd)%fdc_ll(mle)%val, ob(icmd)%fdc_lla(iyr)%val, ob(icmd)%fdc%yr(iyr)%p(nprob), ob(icmd)%fdc_lla(next)%val, ob(icmd)%fdc_lla(iyr)%next, ob(icmd)%fdc_lla(iprv)%next, ob(icmd)%fdc_lla(next)%next, ob(icmd)%fdc_lla(mle)%next, ob(icmd)%fdc%yr(iyr)%mean, ob(icmd)%fdc%p_md%max, ob(icmd)%fdc%yr(iyr)%max, ob(icmd)%fdc%p_md%min, ob(icmd)%fdc%yr(iyr)%min, ob(icmd)%fdc%p_md%mean, ob(icmd)%fdc%p_md%p(nprob), ob(icmd)%fdc%yr(next)%p(nprob), ob(icmd)%fdc%yr(iprv)%p(nprob), ob(icmd)%fdc%p_md%p, ob(icmd)%flash_idx%sum_q, ob(icmd)%flash_idx%index, ob(icmd)%flash_idx%sum_q_q1, ob(icmd)%typ, ob(icmd)%props, ob(icmd)%area_ha` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ob(icmd)%fdc_ll(time%day)%val` | Each call when the routine processes the current simulation day. | `ob(icmd)%fdc_ll(time%day)%val` is set to the current daily flow from `ob(icmd)%hd(1)%flo`, making the new day available for linked-list sorting. |
| `ob(icmd)%fdc_ll(time%day)%next` | When the current daily flow is inserted into the sorted daily linked list. | `ob(icmd)%fdc_ll(time%day)%next` is assigned to the node that follows the newly inserted day in descending order, so the daily list remains linked after insertion. |
| `ob(icmd)%fdc%mfe` | When the new daily flow becomes the first element in the yearly daily list. | `ob(icmd)%fdc%mfe` is updated to `time%day` so the list head points to the largest daily flow seen so far. |
| `ob(icmd)%fdc_ll(iprv)%next` | When the new daily flow is inserted somewhere after the first position in the yearly daily list. | `ob(icmd)%fdc_ll(iprv)%next` is redirected to `time%day`, linking the previous node to the newly inserted daily value. |
| `ob(icmd)%fdc_ll(mle)%next` | When the new daily flow is appended to the end of the yearly daily list. | `ob(icmd)%fdc_ll(mle)%next` is set to `time%day` so the tail points to the new smallest daily flow. |
| `ob(icmd)%fdc%mle` | When the new daily flow becomes the last element in the yearly daily list. | `ob(icmd)%fdc%mle` is updated to `time%day`, marking the current day as the tail of the daily list. |
| `ob(icmd)%fdc%yr(time%yrs)%p(nprob)` | At year end, while copying the standard 27 percentile points from the sorted daily list. | `ob(icmd)%fdc%yr(time%yrs)%p(nprob)` receives the daily flow value at the current duration probability for this year. |
| `ob(icmd)%fdc%yr(time%yrs)%mean` | At year end, after summing all daily linked-list values for the current year. | `ob(icmd)%fdc%yr(time%yrs)%mean` becomes the yearly mean flow, computed from the sum of daily values divided by the number of days processed. |
| `ob(icmd)%fdc%yr(time%yrs)%max` | At year end, after locating the yearly list head. | `ob(icmd)%fdc%yr(time%yrs)%max` stores the maximum daily flow for the year. |
| `ob(icmd)%fdc%yr(time%yrs)%min` | At year end, after locating the yearly list tail. | `ob(icmd)%fdc%yr(time%yrs)%min` stores the minimum daily flow for the year. |
| `ob(icmd)%fdc_lla(iyr)%val` | During simulation-end sorting, for each probability point and each year. | `ob(icmd)%fdc_lla(iyr)%val` is loaded with the yearly curve value at the current probability so annual values can be sorted across years. |
| `ob(icmd)%fdc_lla(iyr)%next` | During simulation-end sorting, after setting the annual value for the current year. | `ob(icmd)%fdc_lla(iyr)%next` is assigned the next year in sorted order among annual values for the current probability point. |
| `ob(icmd)%fdc_lla(iprv)%next` | During simulation-end sorting, when the annual value is inserted after a previous year in the linked list. | `ob(icmd)%fdc_lla(iprv)%next` is updated to point to the current year, preserving the sorted annual chain. |
| `ob(icmd)%fdc_lla(mle)%next` | During simulation-end sorting, when the annual value becomes the new tail of the annual list. | `ob(icmd)%fdc_lla(mle)%next` is set to the current year so the annual tail points to the last-ranked year. |
| `ob(icmd)%fdc%p_md%max` | During the simulation-end reduction over annual years. | `ob(icmd)%fdc%p_md%max` is updated to the largest yearly maximum among all years. |
| `ob(icmd)%fdc%p_md%min` | During the simulation-end reduction over annual years. | `ob(icmd)%fdc%p_md%min` is updated to the smallest yearly minimum among all years. |
| `ob(icmd)%fdc%p_md%mean` | After the annual reduction loop finishes. | `ob(icmd)%fdc%p_md%mean` is set to the average of yearly mean flows across the simulation. |
| `ob(icmd)%fdc%p_md%p(nprob)` | During the median-year selection for each probability point. | `ob(icmd)%fdc%p_md%p(nprob)` is assigned the median annual percentile value for the current probability point. |
| `ob(icmd)%fdc%p_md%p` | After all median percentile values and summary statistics are collected. | `ob(icmd)%fdc%p_md%p` is converted from daily volume units to m3/s by dividing the whole array by 86400. |
| `ob(icmd)%flash_idx%index` | At simulation end, when enough cumulative flow has been accumulated to compute flashiness. | `ob(icmd)%flash_idx%index` is calculated as the ratio of cumulative day-to-day flow change to total flow. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits touched `flow_dur_curve`. The file was introduced in df07e3f with the complete subroutine body. 35b029c made a formatting-only change to the `end subroutine flow_dur_curve` line. 94b6dec added the same source body as a new file from the upstream import. 39fabde initialized all local variables (`sum`, `iyr`, `next`, `npts`, `ipts`, `iprv`, `mle`, `nprob`, `iday`, `mfe`, `iyr_ch`) to zero, leaving the algorithm otherwise unchanged.

- df07e3f created `flow_dur_curve.f90` with the daily/annual linked-list algorithm, yearly percentile extraction, simulation-median calculation, flashiness computation, and unit-6000 output.
- 35b029c only changed the `end subroutine flow_dur_curve` spacing; it did not alter runtime behavior.
- 94b6dec imported the same subroutine body into the source tree as part of the upstream code drop.
- 39fabde initialized the subroutine’s local scalars to zero to avoid undefined values during list insertion and annual-median processing.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'flow_dur_curve' has no extracted documentation comment.
