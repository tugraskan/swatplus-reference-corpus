---
kind: procedure
symbol: gcycl
title: gcycl
status: filled
source_hash: 41cd984b67c814a7
version_label: SWAT+ 62.0.0
locals:
  xx: Temporary discard variable that receives values from Aunif during the shuffle loops
    and is not used after each draw.
  rn: Holds a uniform random fraction from Aunif so the routine can convert it into a loop
    count and derive a shuffle index.
  ii: Integer work value derived from rn; it controls how many extra Aunif draws are used
    and stores the current idg entry during shuffling.
  j: Counter for the seed-index loop and the reverse Fisher-Yates-style shuffle loop.
  k: Loop counter for repeated Aunif draws when advancing the generator, and also the swap
    index computed during idg shuffling.
  rndseed10: Working integer seed passed into Aunif so the routine can generate new seed values
    and shuffle the random stream deterministically.
  iwgn: Weather-station index used to initialize and update per-station random-number seeds
    and outputs.
  aunif: External uniform random-number generator function used to advance the seed stream
    and produce fractions for reseeding and shuffling.
uses:
  climate_module: climate_module holds the shared random-number arrays and conditional-seed
    state that this routine initializes. gcycl writes the seed matrix, the seed-location map,
    the per-station random variates, and the conditional-probability seed there so later climate
    and weather routines can reuse consistent stochastic state.
  basin_module: basin_module provides bsn_prm%igen, the basin-level switch that decides whether
    gcycl only loads default seeds or also generates a new randomized seed set. That setting
    controls whether the routine performs the extra reseeding and shuffle work.
  maximum_data_module: maximum_data_module provides db_mx%wgnsta, the number of weather stations
    over which the seed table and derived random values must be initialized. Without that
    count, gcycl would not know how many station-specific seed columns to fill.
  conditional_module: conditional_module matters because gcycl assigns rndseed_cond when it
    shuffles or refreshes the random-number stream. That seed is used by conditional probability
    logic that depends on a separate random stream from the weather-generator seeds.
---

<!-- facts:header -->

Initializes the SWAT+ random-number seed arrays for weather generation and conditional probability logic. It can optionally reshuffle the seed mapping when the basin random-generator code requests new numbers.

## Bottom Line

gcycl sets up the climate random-number state used by weather generators and related stochastic decisions. It fills the seed table for each weather station, assigns the seed mapping array idg, and derives working random values that later routines use when generating climate and sub-daily weather variability.

When basin_prm%igen is nonzero, the routine advances the generator to create a fresh seed set and a shuffled seed-order mapping, including the separate rndseed_cond value used by conditional probability handling. Those initialized seeds are then consumed by weather and precipitation generation logic that depends on repeatable but configurable randomness.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during weather-gage initialization, before weather or climate generation begins. cli_wgnread allocates the climate arrays and then calls gcycl to populate them; afterward, later weather-generation behavior depends on the seeded arrays rndseed, rnd2, rnd3, rnd8, rnd9, idg, and rndseed_cond being ready.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize seed locator | Set idg to the base process order 1 through 9 so the routine has a known starting mapping for the random-number streams. |
| 2. load default station seeds | For every weather station, assign fixed baseline seeds to rndseed(1:9,iwgn) and set the working seed rndseed10 used for later random draws. |
| 3. test reseeding flag | Check bsn_prm%igen to decide whether the model should keep the default seed set or generate a new randomized one for this run. |
| 4. generate new seeds | If reseeding is enabled, draw a fraction from Aunif, convert it to a repeat count, advance the generator that many times, and store the resulting seed back into rndseed(j,1) for each of the nine process streams. |
| 5. save conditional seed | Copy the refreshed working seed into rndseed_cond so conditional-probability code can use a separate seed stream. |
| 6. shuffle stream order | Use a reverse-order shuffle to permute idg with Aunif-generated indices, changing which seed slot feeds each climate process. |
| 7. copy rainfall seed | For each station, copy the seed selected by idg(6) into rndseed(10,iwgn) for sub-daily rainfall generation. |
| 8. draw working random values | For each station, generate current uniform random numbers for the idg-selected process streams and store them in rnd2, rnd3, rnd8, and rnd9. |
| 9. return | Exit after all shared random-number state has been initialized for later weather and conditional logic. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `rndseed, idg, rnd2, rnd3, rnd8, rnd9, rndseed_cond` |  |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%igen` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wgnsta` |
| [sym:conditional_module] | `conditional_module` | `rndseed_cond` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `idg` | Always, before the optional reseeding branch. | idg is initialized to the default process order 1 through 9, establishing the baseline mapping from random streams to climate processes. |
| `rndseed(1,iwgn)` | When bsn_prm%igen /= 0 and j iterates from 1 to 9. | rndseed(1,iwgn) is replaced by the current working seed for station iwgn after advancing Aunif, so stream 1 can vary between simulation runs. |
| `rndseed(2,iwgn)` | When bsn_prm%igen /= 0 and j iterates from 1 to 9. | rndseed(2,iwgn) is replaced by the current working seed for station iwgn after advancing Aunif, so stream 2 can vary between simulation runs. |
| `rndseed(3,iwgn)` | When bsn_prm%igen /= 0 and j iterates from 1 to 9. | rndseed(3,iwgn) is replaced by the current working seed for station iwgn after advancing Aunif, so stream 3 can vary between simulation runs. |
| `rndseed(4,iwgn)` | When bsn_prm%igen /= 0 and j iterates from 1 to 9. | rndseed(4,iwgn) is replaced by the current working seed for station iwgn after advancing Aunif, so stream 4 can vary between simulation runs. |
| `rndseed(5,iwgn)` | When bsn_prm%igen /= 0 and j iterates from 1 to 9. | rndseed(5,iwgn) is replaced by the current working seed for station iwgn after advancing Aunif, so stream 5 can vary between simulation runs. |
| `rndseed(6,iwgn)` | When bsn_prm%igen /= 0 and j iterates from 1 to 9. | rndseed(6,iwgn) is replaced by the current working seed for station iwgn after advancing Aunif, so stream 6 can vary between simulation runs. |
| `rndseed(7,iwgn)` | When bsn_prm%igen /= 0 and j iterates from 1 to 9. | rndseed(7,iwgn) is replaced by the current working seed for station iwgn after advancing Aunif, so stream 7 can vary between simulation runs. |
| `rndseed(8,iwgn)` | When bsn_prm%igen /= 0 and j iterates from 1 to 9. | rndseed(8,iwgn) is replaced by the current working seed for station iwgn after advancing Aunif, so stream 8 can vary between simulation runs. |
| `rndseed(9,iwgn)` | When bsn_prm%igen /= 0 and j iterates from 1 to 9. | rndseed(9,iwgn) is replaced by the current working seed for station iwgn after advancing Aunif, so stream 9 can vary between simulation runs. |
| `rndseed(j,1)` | When bsn_prm%igen /= 0, inside the reseeding loop for j = 1..9. | rndseed(j,1) stores the updated seed value produced for each of the nine process streams in the first station slot, providing the new base seed set for later use. |
| `rndseed_cond` | When bsn_prm%igen /= 0, after the new seed set is generated. | rndseed_cond is set to the final working seed so conditional-probability logic can use the same refreshed random sequence state. |
| `idg(j)` | When bsn_prm%igen /= 0, during the reverse shuffle loop for j = 9..1. | idg(j) is temporarily read to hold the current element before swapping, allowing the stream-order permutation to proceed safely. |
| `idg(k)` | When bsn_prm%igen /= 0, during the reverse shuffle loop for j = 9..1. | idg(k) receives the element moved from position j, completing the swap that permutes which seed index drives each process. |
| `rndseed(10,iwgn)` | After the optional reseeding branch and for each weather station iwgn. | rndseed(10,iwgn) becomes a copy of the seed selected by idg(6), reserving the rainfall-related seed stream for sub-daily precipitation generation. |
| `rnd2(iwgn)` | For each weather station iwgn, after the seed order has been established. | rnd2(iwgn) is refreshed with a new uniform random value from the seed selected by idg(2), supporting later stochastic climate calculations. |
| `rnd3(iwgn)` | For each weather station iwgn, after the seed order has been established. | rnd3(iwgn) is refreshed with a new uniform random value from the seed selected by idg(3), supporting later stochastic climate calculations. |
| `rnd8(iwgn)` | For each weather station iwgn, after the seed order has been established. | rnd8(iwgn) is refreshed with a new uniform random value from the seed selected by idg(8), supporting later stochastic climate calculations. |
| `rnd9(iwgn)` | For each weather station iwgn, after the seed order has been established. | rnd9(iwgn) is refreshed with a new uniform random value from the seed selected by idg(9), supporting later stochastic climate calculations. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows gcycl was added in df07e3f with the initial random-seed initialization logic and documentation comments. 94b6dec later updated the same source without changing the algorithm, mainly keeping the file in sync with upstream source and clarifying the external declaration for aunif, while 39fabde added default initial values to local variables and 889136d only fixed a comment typo.

- df07e3f introduced the subroutine and its seed-initialization behavior, including the default seed table, optional reseeding branch, idg shuffle, and derived random draws.
- 39fabde changed only local-variable initialization style in gcycl, setting xx, rn, ii, j, k, rndseed10, and iwgn to zero without altering the algorithm.
- 889136d made a documentation-only typo fix in the comment for conditional probability and did not change runtime behavior.
- bd18ad4 changed the external declaration of aunif to an explicit external procedure declaration, which affects compilation/interface clarity but not the seed-generation algorithm.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'gcycl' has no extracted documentation comment.
