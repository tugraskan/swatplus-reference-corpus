---
kind: procedure
symbol: salt_fert
title: salt_fert
status: filled
source_hash: f63d9116284fa944
version_label: SWAT+ 62.0.0
args:
  jj: HRU index whose soil profile and salt-balance arrays receive the fertilizer salt additions.
  ifrt: Index into the fertilizer salt database; it selects the fertilizer composition used
    to compute the salt-ion loads.
  frt_kg: Applied fertilizer mass in kg/ha; this scales every salt-ion increment added to
    soil and salt-balance state.
  fertop: Chemical-application operation index; it supplies `chemapp_db(fertop)%surf_frac`,
    which controls how the load is split between the top two soil layers.
locals:
  fert_type: Holds the fertilizer name from `fertdb(ifrt)%fertnm` so the routine can decide
    whether the load is a salt amendment (`'a'` prefix) or regular fertilizer.
  xx: 'Stores the fraction of the applied fertilizer assigned to the current soil layer: surface
    fraction for layer 1, and the remainder for layer 2.'
  l: Loop counter for the two soil layers that receive the applied salt mass.
uses:
  mgt_operations_module: '`chemapp_db(fertop)%surf_frac` provides the surface-application
    fraction for the chemical operation, which determines how much of the fertilizer salt
    load goes into the upper versus lower of the two treated soil layers.'
  salt_module: '`fert_salt(ifrt)` holds the per-kg salt composition for the selected fertilizer,
    and `hsaltb_d(jj)` records how much of each ion was added as amendment or fertilizer for
    the HRU.'
  constituent_mass_module: '`cs_db%num_salts` gates whether salt simulation is active, and
    `cs_soil(jj)%ly(l)%salt(1:8)` are the per-layer salt pools that receive the applied mass.'
  fertilizer_data_module: '`fertdb(ifrt)%fertnm` supplies the fertilizer name used to classify
    the application as a salt amendment or regular fertilizer before updating the balance
    arrays.'
---

<!-- facts:header -->

Adds fertilizer-associated salt ions to the soil profile for a selected HRU. It partitions the applied mass between the top two layers and records the addition in the salt balance arrays.

## Bottom Line

salt_fert applies a fertilizer or manure salt load to the top two soil layers of a specific HRU. It uses the chemical-application surface fraction to split the applied mass between the surface layer and the layer below, then adds eight salt ions from the fertilizer-salt database into the soil salt pools.

When salt simulation is enabled and the fertilizer ID is valid, the routine also updates the HRU salt-balance bookkeeping. It classifies the application by the fertilizer name: names starting with `a` are treated as salt amendments and are accumulated in `%amnd`, while all other fertilizers are accumulated in `%fert` for the eight tracked ions.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during management/operations processing after the caller has selected a fertilizer type, application mass, and chemical-application setting. `actions` and `mgt_sched` prepare those inputs, and later salt-budget accounting depends on the updated `cs_soil` and `hsaltb_d` values.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check salt simulation gate | Proceeds only when salts are simulated for the model and the fertilizer-salt flag is enabled. |
| 2. validate fertilizer ID | Skips the application unless the fertilizer type index is positive and can index the fertilizer-salt database. |
| 3. loop over top two layers | Processes only layers 1 and 2 so the applied salt is split between the surface and the layer beneath it. |
| 4. reset layer fraction | Initializes the application fraction for the current layer before assigning the layer-specific share. |
| 5. assign surface or remainder | Uses `chemapp_db(fertop)%surf_frac` for layer 1 and `1. - chemapp_db(fertop)%surf_frac` for layer 2. |
| 6. add salts to soil pools | Adds the eight fertilizer salt-ion masses to `cs_soil(jj)%ly(l)%salt(1:8)` using the layer fraction and applied mass. |
| 7. load fertilizer name | Copies the fertilizer name from the fertilizer database so the routine can classify the application. |
| 8. classify amendment | Tests the first character of the fertilizer name; names beginning with `a` are treated as salt amendments. |
| 9. book amendment load | Accumulates the applied salt masses into `hsaltb_d(jj)%salt(1:8)%amnd` for amendment-type applications. |
| 10. book fertilizer load | Accumulates the applied salt masses into `hsaltb_d(jj)%salt(1:8)%fert` for regular fertilizer applications. |
| 11. finish layer loop | Ends the two-layer split after both layer shares have been processed. |
| 12. return | Returns to the caller after the soil salt pools and HRU salt-balance arrays have been updated or skipped by the gates. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:mgt_operations_module] | `chemapp_db` | `chemapp_db(fertop)%surf_frac` |
| [sym:salt_module] | `fert_salt, hsaltb_d, fert_salt_flag` | `fert_salt(ifrt)%so4, fert_salt(ifrt)%ca, fert_salt(ifrt)%mg, fert_salt(ifrt)%na, fert_salt(ifrt)%k, fert_salt(ifrt)%cl, fert_salt(ifrt)%co3, fert_salt(ifrt)%hco3, hsaltb_d(jj)%salt(1)%amnd, hsaltb_d(jj)%salt(2)%amnd, hsaltb_d(jj)%salt(3)%amnd, hsaltb_d(jj)%salt(4)%amnd, hsaltb_d(jj)%salt(5)%amnd, hsaltb_d(jj)%salt(6)%amnd, hsaltb_d(jj)%salt(7)%amnd, hsaltb_d(jj)%salt(8)%amnd, hsaltb_d(jj)%salt(1)%fert, hsaltb_d(jj)%salt(2)%fert, hsaltb_d(jj)%salt(3)%fert, hsaltb_d(jj)%salt(4)%fert, hsaltb_d(jj)%salt(5)%fert, hsaltb_d(jj)%salt(6)%fert, hsaltb_d(jj)%salt(7)%fert, hsaltb_d(jj)%salt(8)%fert` |
| [sym:constituent_mass_module] | `cs_db, cs_soil` | `cs_db%num_salts, cs_soil(jj)%ly(l)%salt(1), cs_soil(jj)%ly(l)%salt(2), cs_soil(jj)%ly(l)%salt(3), cs_soil(jj)%ly(l)%salt(4), cs_soil(jj)%ly(l)%salt(5), cs_soil(jj)%ly(l)%salt(6), cs_soil(jj)%ly(l)%salt(7), cs_soil(jj)%ly(l)%salt(8)` |
| [sym:fertilizer_data_module] | `fertdb` | `fertdb(ifrt)%fertnm` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_soil(jj)%ly(l)%salt(1)` | When `cs_db%num_salts > 0`, `fert_salt_flag == 1`, `ifrt > 0`, and the current layer is being processed. | Adds the fraction of the applied fertilizer salt mass belonging to sulfate (`so4`) into the selected soil layer's salt(1) pool. |
| `cs_soil(jj)%ly(l)%salt(2)` | When `cs_db%num_salts > 0`, `fert_salt_flag == 1`, `ifrt > 0`, and the current layer is being processed. | Adds the fraction of the applied fertilizer salt mass belonging to calcium (`ca`) into the selected soil layer's salt(2) pool. |
| `cs_soil(jj)%ly(l)%salt(3)` | When `cs_db%num_salts > 0`, `fert_salt_flag == 1`, `ifrt > 0`, and the current layer is being processed. | Adds the fraction of the applied fertilizer salt mass belonging to magnesium (`mg`) into the selected soil layer's salt(3) pool. |
| `cs_soil(jj)%ly(l)%salt(4)` | When `cs_db%num_salts > 0`, `fert_salt_flag == 1`, `ifrt > 0`, and the current layer is being processed. | Adds the fraction of the applied fertilizer salt mass belonging to sodium (`na`) into the selected soil layer's salt(4) pool. |
| `cs_soil(jj)%ly(l)%salt(5)` | When `cs_db%num_salts > 0`, `fert_salt_flag == 1`, `ifrt > 0`, and the current layer is being processed. | Adds the fraction of the applied fertilizer salt mass belonging to potassium (`k`) into the selected soil layer's salt(5) pool. |
| `cs_soil(jj)%ly(l)%salt(6)` | When `cs_db%num_salts > 0`, `fert_salt_flag == 1`, `ifrt > 0`, and the current layer is being processed. | Adds the fraction of the applied fertilizer salt mass belonging to chloride (`cl`) into the selected soil layer's salt(6) pool. |
| `cs_soil(jj)%ly(l)%salt(7)` | When `cs_db%num_salts > 0`, `fert_salt_flag == 1`, `ifrt > 0`, and the current layer is being processed. | Adds the fraction of the applied fertilizer salt mass belonging to carbonate (`co3`) into the selected soil layer's salt(7) pool. |
| `cs_soil(jj)%ly(l)%salt(8)` | When `cs_db%num_salts > 0`, `fert_salt_flag == 1`, `ifrt > 0`, and the current layer is being processed. | Adds the fraction of the applied fertilizer salt mass belonging to bicarbonate (`hco3`) into the selected soil layer's salt(8) pool. |
| `hsaltb_d(jj)%salt(1)%amnd` | When the fertilizer name starts with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's sulfate contribution into the amendment salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(2)%amnd` | When the fertilizer name starts with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's calcium contribution into the amendment salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(3)%amnd` | When the fertilizer name starts with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's magnesium contribution into the amendment salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(4)%amnd` | When the fertilizer name starts with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's sodium contribution into the amendment salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(5)%amnd` | When the fertilizer name starts with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's potassium contribution into the amendment salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(6)%amnd` | When the fertilizer name starts with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's chloride contribution into the amendment salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(7)%amnd` | When the fertilizer name starts with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's carbonate contribution into the amendment salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(8)%amnd` | When the fertilizer name starts with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's bicarbonate contribution into the amendment salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(1)%fert` | When the fertilizer name does not start with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's sulfate contribution into the regular fertilizer salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(2)%fert` | When the fertilizer name does not start with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's calcium contribution into the regular fertilizer salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(3)%fert` | When the fertilizer name does not start with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's magnesium contribution into the regular fertilizer salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(4)%fert` | When the fertilizer name does not start with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's sodium contribution into the regular fertilizer salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(5)%fert` | When the fertilizer name does not start with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's potassium contribution into the regular fertilizer salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(6)%fert` | When the fertilizer name does not start with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's chloride contribution into the regular fertilizer salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(7)%fert` | When the fertilizer name does not start with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's carbonate contribution into the regular fertilizer salt-balance total for HRU `jj`. |
| `hsaltb_d(jj)%salt(8)%fert` | When the fertilizer name does not start with `a` after the soil-layer update has been computed for the current layer. | Accumulates the layer's bicarbonate contribution into the regular fertilizer salt-balance total for HRU `jj`. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved for six commits. df07e3f introduced `salt_fert` as a new subroutine that adds fertilizer salt to the soil profile and records amendment/fertilizer balances. 35b029c only adjusted the end-of-subroutine line formatting. 16e54aa changed the salt-flag test from `.eq.1` to `== 1`. 2ee1889 removed the unused local `isalt` declaration. 39fabde initialized `fert_type`, `xx`, `isalt`, and `l` with default values. 94b6dec imported the routine from earlier source, retaining the same core behavior of splitting the load across the top two layers and updating soil and balance arrays.

- df07e3f: added the full salt fertilizer application routine, including the two-layer split, soil salt updates, fertilizer-name classification, and amendment versus fertilizer bookkeeping.
- 16e54aa: changed the salt-simulation guard from `.eq.1` to `== 1` without changing the control flow.
- 39fabde: initialized local variables `fert_type`, `xx`, `isalt`, and `l` to safe defaults.
- 2ee1889: removed the unused local variable `isalt` while leaving the algorithm unchanged.
- 35b029c: adjusted only the trailing `end subroutine` formatting; no behavior change.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'salt_fert' has no extracted documentation comment.
