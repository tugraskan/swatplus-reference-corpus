---
kind: procedure
symbol: constit_hyd_mult
title: constit_hyd_mult
status: filled
source_hash: 73e1692b33387afb
version_label: SWAT+ 62.0.0
args:
  iob: '`iob` selects which object in `obcs` is updated. The routine uses `iob` to read that
    object''s incoming hydrograph from `obcs(iob)%hin(1)` and to write the multiplied results
    into `obcs(iob)%hd(1)`.'
  idr: '`idr` selects the delivery-ratio definition to apply. The routine uses it to find
    the matching pesticide, pathogen, heavy-metal, and salt delivery-ratio arrays through
    `dr_pest_num(idr)`, `dr_path_num(idr)`, `dr_hmet_num(idr)`, and `dr_salt_num(idr)`.'
locals:
  idr_pest: Holds the delivery-ratio table index for pesticides after mapping from `dr_pest_num(idr)`,
    so the routine can read `dr_pest(idr_pest)%pest` for the pesticide multipliers.
  ipest: Loop index over pesticide constituents, running from 1 to `cs_db%num_pests` to apply
    each pesticide multiplier.
  idr_path: Holds the delivery-ratio table index for pathogens after mapping from `dr_path_num(idr)`,
    so the routine can read `dr_path(idr_path)%path`.
  ipath: Loop index over pathogen constituents, running from 1 to `cs_db%num_paths` to apply
    each pathogen multiplier.
  idr_hmet: Holds the delivery-ratio table index for heavy metals after mapping from `dr_hmet_num(idr)`,
    so the routine can read `dr_hmet(idr_hmet)%hmet`.
  ihmet: Loop index over heavy-metal constituents, running from 1 to `cs_db%num_metals` to
    apply each heavy-metal multiplier.
  idr_salt: Holds the delivery-ratio table index for salts after mapping from `dr_salt_num(idr)`,
    so the routine can read `dr_salt(idr_salt)%salt`.
  isalt: Loop index over salt constituents, running from 1 to `cs_db%num_salts` to apply each
    salt multiplier.
uses:
  constituent_mass_module: This module supplies the shared constituent database and hydrograph
    containers that the subroutine reads and updates. `cs_db` provides the loop bounds for
    each constituent class, `obcs` contains the incoming hydrograph (`hin`) and the outgoing
    hydrograph (`hd`) for the selected object, and `dr_pest`, `dr_path`, `dr_hmet`, and `dr_salt`
    provide the per-constituent delivery multipliers that are applied element by element.
  dr_module: This module maps the abstract delivery-ratio object index `idr` to the specific
    delivery-ratio records used here. Without `dr_pest_num`, `dr_path_num`, `dr_hmet_num`,
    and `dr_salt_num`, the routine would not know which pesticide, pathogen, heavy-metal,
    or salt multiplier set belongs to the current routing object.
---

<!-- facts:header -->

Applies delivery-ratio multipliers to the current object's constituent hydrographs. It scales pesticide, pathogen, heavy-metal, and salt loads from the incoming hydrograph into the outgoing hydrograph for a given object and delivery-ratio set.

## Bottom Line

`constit_hyd_mult` looks up the delivery-ratio record for the current routing object and multiplies each constituent class in `obcs(iob)%hin(1)` by the corresponding ratio array. The results are stored in `obcs(iob)%hd(1)`, so the object's outgoing hydrograph carries constituent masses adjusted by the selected delivery ratios.

The routine handles four constituent groups separately: pesticides, pathogens, heavy metals, and salts. It matters because later routing and export behavior uses the updated `obcs(iob)%hd(1)` values rather than the unadjusted incoming hydrograph.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs in the delivery-ratio branch of `command`, after `command` has already identified the current object and its delivery-ratio selector. It prepares the outgoing constituent hydrograph for that object, and later routing/export logic depends on `obcs(iob)%hd(1)` carrying the multiplied values instead of the unscaled incoming masses.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. resolve pesticide delivery set | Map the input delivery-ratio ID to the pesticide delivery-ratio table with `dr_pest_num(idr)`, then multiply each pesticide mass in the incoming hydrograph by the corresponding factor and store it in the outgoing hydrograph. |
| 2. resolve pathogen delivery set | Map the input delivery-ratio ID to the pathogen delivery-ratio table with `dr_path_num(idr)`, then multiply each pathogen mass in the incoming hydrograph by the corresponding factor and store it in the outgoing hydrograph. |
| 3. resolve heavy-metal delivery set | Map the input delivery-ratio ID to the heavy-metal delivery-ratio table with `dr_hmet_num(idr)`, then multiply each heavy-metal mass in the incoming hydrograph by the corresponding factor and store it in the outgoing hydrograph. |
| 4. resolve salt delivery set | Map the input delivery-ratio ID to the salt delivery-ratio table with `dr_salt_num(idr)`, then multiply each salt mass in the incoming hydrograph by the corresponding factor and store it in the outgoing hydrograph. |
| 5. return | Exit the subroutine after all outgoing constituent hydrograph values have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `cs_db, obcs, dr_pest, dr_path, dr_hmet, dr_salt` | `cs_db%num_pests, obcs(iob)%hd(1)%pest(ipest), obcs(iob)%hin(1)%pest(ipest), dr_pest(idr_pest)%pest(ipest), cs_db%num_paths, obcs(iob)%hd(1)%path(ipath), obcs(iob)%hin(1)%path(ipath), dr_path(idr_path)%path(ipath), cs_db%num_metals, obcs(iob)%hd(1)%hmet(ihmet), obcs(iob)%hin(1)%hmet(ihmet), dr_hmet(idr_hmet)%hmet(ihmet), cs_db%num_salts, obcs(iob)%hd(1)%salt(isalt), obcs(iob)%hin(1)%salt(isalt), dr_salt(idr_salt)%salt(isalt)` |
| [sym:dr_module] | `dr_pest_num, dr_path_num, dr_hmet_num, dr_salt_num` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `obcs(iob)%hd(1)%pest(ipest)` | For each pesticide index `ipest` from 1 to `cs_db%num_pests`. | `obcs(iob)%hd(1)%pest(ipest)` is replaced with the incoming pesticide mass times the selected pesticide delivery ratio. This updates the outgoing hydrograph so the routed pesticide load reflects the current delivery setting. |
| `obcs(iob)%hd(1)%path(ipath)` | For each pathogen index `ipath` from 1 to `cs_db%num_paths`. | `obcs(iob)%hd(1)%path(ipath)` is replaced with the incoming pathogen mass times the selected pathogen delivery ratio. This updates the outgoing hydrograph so the routed pathogen load reflects the current delivery setting. |
| `obcs(iob)%hd(1)%hmet(ihmet)` | For each heavy-metal index `ihmet` from 1 to `cs_db%num_metals`. | `obcs(iob)%hd(1)%hmet(ihmet)` is replaced with the incoming heavy-metal mass times the selected heavy-metal delivery ratio. This updates the outgoing hydrograph so the routed heavy-metal load reflects the current delivery setting. |
| `obcs(iob)%hd(1)%salt(isalt)` | For each salt index `isalt` from 1 to `cs_db%num_salts`. | `obcs(iob)%hd(1)%salt(isalt)` is replaced with the incoming salt mass times the selected salt delivery ratio. This updates the outgoing hydrograph so the routed salt load reflects the current delivery setting. |

## File I/O

<!-- facts:io -->


## Lineage

`constit_hyd_mult` was added in commit df07e3f with the full delivery-ratio scaling logic for pesticides, pathogens, heavy metals, and salts. Commit c7c8e22 carried the same routine forward without changing the code in the extracted diff, and commit 39fabde only initialized the local loop/index variables to zero.

- df07e3f introduced the subroutine and its four constituent-class scaling loops, creating `constit_hyd_mult` as a delivery-ratio multiplier for `obcs(iob)%hd(1)`.
- 39fabde changed only the local integer declarations by assigning initial values of 0 to `idr_pest`, `ipest`, `idr_path`, `ipath`, `idr_hmet`, `ihmet`, `idr_salt`, and `isalt`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'constit_hyd_mult' has no extracted documentation comment.
