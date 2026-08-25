---
kind: module
symbol: manure_allocation_module
title: manure_allocation_module
status: filled
source_hash: bc0e96d770a66d86
version_label: SWAT+ 62.0.0
variables:
  manure_amtz: Singleton default `manure_demand_amount` record. Its fields (`mallo_obj`, `src_obj`,
    `app_t_ha`, `app_method`) are initialized to zero and used as a reset template for manure-demand
    requests before `actions` fills them from a decision table and `mallo_control` clears
    them after use.
  malloz: Singleton default `source_manure_output` record. Its fields (`stor`, `prod`, `withdr`)
    are initialized to zero and used as a reset template for allocation totals and source
    balance records in `mallo_control` and `manure_source_output`.
  mallo: Allocatable array of `manure_allocation` objects. Each element holds one manure-allocation
    object with its name, rule type, source records, demand records, and totals. It is allocated
    and populated by `manure_allocation_read` from `manure_allo.mnu` and then read and updated
    by `mallo_control`, `manure_demand_output`, `manure_source_output`, and `actions`.
  mallo_hdr: Singleton `mallo_header` label template for manure-allocation text output. It
    stores column labels such as day, month, allocation identifiers, source labels, and demand/withdrawal
    labels. Output routines use it when writing fixed-format headers.
  mallo_hdr_units: Singleton `mallo_header_units` label template for manure-allocation unit
    output. It stores the parallel header labels for unit-based output, with `m^3` labels
    on demand/withdrawal fields. Output routines use it when writing unit headers.
type_components:
  manure_demand_amount:
    mallo_obj: Manure-allocation object index that owns this demand request.
    src_obj: Source-object number selected for the demand request.
    app_t_ha: Requested application amount in tons per hectare.
    app_method: Application method code chosen from the decision table.
  source_manure_output:
    stor: current manure stored - tons
    prod: mannure produced - tons
    withdr: manure withdrawal from all demand objects - tons
  manure_source_objects:
    num: source object number
    mois_typ: wet or dry
    manure_typ: points to fertilizer.frt
    lat: latitude
    long: longitude
    stor_init: initial storage - tons
    stor_max: maximum storage - tons
    prod_mon: average monthly manure produced - tons/month
    fertdb: fertilizer database number (fertilizer.frt)
    bal_d: daily amount - storage, produced, withdrawn from the source - tons
    bal_m: monthly amount - storage, produced, withdrawn from the source - tons
    bal_y: yearly amount - storage, produced, withdrawn from the source - tons
    bal_a: ave annual amount - storage, produced, withdrawn from the source - tons
  manure_demand_objects:
    num: demand object number
    ob_typ: hru (for application) or muni (treatmentb) or divert (interbasin diversion)
    ob_num: number of the object type
    dtbl: decision table name for manure/fert application
    right: manure right (sr -senior or jr - junior right
    dtbl_num: Decision-table index matched during reading so later allocation logic can call
      the right manure transfer table quickly.
    manure_amt: Embedded demand request record holding the selected manure-allocation object,
      source object, application rate, and application method.
    withdr: daily amount withdrawn from each source
    withdr_m: amount withdrawn from each source
    withdr_y: amount withdrawn from each source
    withdr_a: amount withdrawn from each source
  manure_allocation:
    name: name of the water allocation object
    rule_typ: rule type to allocate water
    src_obs: number of source objects
    trn_obs: number of demand objects
    tot: total demand, withdrawal and unmet for entire allocation object
    src: dimension by source objects
    trn: dimension by demand objects
  mallo_header:
    day: Day-of-year label used in output headers.
    mo: Month label used in output headers.
    day_mo: Day-in-month label used in output headers.
    yrc: Year label used in output headers.
    itrn: Iteration or unit label used in output headers.
    trn_typ: Demand-transaction type label.
    trn_num: Demand-transaction number label.
    src1_obj: Source object label for source 1.
    src1_typ: Source type label for source 1.
    src1_num: Source number label for source 1.
    trn1: ha-m     |demand - muni or irrigation
    s1out: ha-m     |withdrawal from source 1
    s1un: ha-m     |unmet from source 1
    src2_typ: Source type label for source 2.
    src2_num: Source number label for source 2.
    trn2: ha-m     |demand - muni or irrigation
    s2out: ha-m     |withdrawal from source 2
    s2un: ha-m     |unmet from source 2
    src3_typ: Source type label for source 3.
    src3_num: Source number label for source 3.
    trn3: ha-m     |demand - muni or irrigation
    s3out: ha-m     |withdrawal from source 3
    s3un: ha-m     |unmet from source 3
  mallo_header_units:
    day: Blank day column header slot for unit output.
    mo: Blank month column header slot for unit output.
    day_mo: Blank day-in-month column header slot for unit output.
    yrc: Blank year column header slot for unit output.
    itrn: Blank iteration or unit column header slot for unit output.
    trn_typ: Blank transaction-type column header slot for unit output.
    trn_num: Blank transaction-number column header slot for unit output.
    src1_obj: Blank source-object column header slot for source 1.
    src1_typ: Blank source-type column header slot for source 1.
    src1_num: Blank source-number column header slot for source 1.
    trn1: ha-m     |demand - muni or irrigation
    s1out: ha-m     |withdrawal from source 1
    s1un: ha-m     |unmet from source 1
    src2_typ: Blank source-type column header slot for source 2.
    src2_num: Blank source-number column header slot for source 2.
    trn2: ha-m     |demand - muni or irrigation
    s2out: ha-m     |withdrawal from source 2
    s2un: ha-m     |unmet from source 2
    src3_typ: Blank source-type column header slot for source 3.
    src3_num: Blank source-number column header slot for source 3.
    trn3: ha-m     |demand - muni or irrigation
    s3out: ha-m     |withdrawal from source 3
    s3un: ha-m     |unmet from source 3
type_summaries:
  manure_demand_amount: manure demand source and amount
  source_manure_output: manure source balance - storage, produced, withdrawan of the allocation
    object
  manure_source_objects: manure source objects
  manure_demand_objects: manure demand objects
  manure_allocation: manure allocation object
  mallo_header: Fixed text labels for manure-allocation output columns.
  mallo_header_units: Fixed unit labels for manure-allocation output columns.
---

<!-- facts:header -->

Defines the shared manure-allocation data model and its report headers. The module owns the singleton template records (`manure_amtz`, `malloz`, `mallo_hdr`, `mallo_hdr_units`) and the allocatable allocation database `mallo`, which stores manure source objects, demand objects, and totals for each manure-allocation object. It is consumed by the manure-allocation driver, configuration reader, output routines, and the general `actions` routine that populates manure-demand requests.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration-and-utility container. It does not contain startup logic; its module variables are initialized directly by declaration defaults and then populated by importer routines such as `manure_allocation_read`, `actions`, and `mallo_control`.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `manure_amtz, malloz, mallo, mallo_hdr, mallo_hdr_units` | Reads the shared manure-allocation state to stage a demand record: it copies `manure_amtz` into the selected demand object and fills `manure_amtz` fields from the current action table entry before later manure allocation uses them. |
| [sym:mallo_control] | `unit_2612` | `manure_amtz, malloz, mallo, mallo_hdr, mallo_hdr_units` | Uses `malloz` and `manure_amtz` as reset templates and reads `mallo` to execute daily manure allocation for one allocation object. |
| [sym:manure_allocation_read] | `manure_allo.mnu` | `manure_amtz, malloz, mallo, mallo_hdr, mallo_hdr_units` | Allocates and populates `mallo` from the manure-allocation input file; the singleton templates and header records remain available for later use by the writer and control routines. |
| [sym:manure_demand_output] | `unit_3210, unit_3211, unit_3212, unit_3213, unit_3214, unit_3215, unit_3216, unit_3217` | `manure_amtz, malloz, mallo, mallo_hdr, mallo_hdr_units` | Reads `mallo` to report demand-side withdrawals and uses the header templates when writing fixed-format daily, monthly, yearly, and average-annual output. |
| [sym:manure_source_output] | `unit_3200, unit_3201, unit_3202, unit_3203, unit_3204, unit_3205, unit_3206, unit_3207` | `manure_amtz, malloz, mallo, mallo_hdr, mallo_hdr_units` | Reads `mallo` and `malloz` to report source-side balance totals and to clear daily and monthly balance records after printing. |

## Key Consumers

The module is used by the manure-allocation driver and its paired read/write routines, plus the general `actions` dispatcher that constructs manure-demand requests.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:mallo_control] | manure_allocation_module | Resets each allocation object's totals from `malloz`, advances source storage from monthly production, evaluates demand decision tables, and clears the demand template after an application is executed. |
| [sym:manure_allocation_read] | manure_allocation_module | Builds the in-memory manure-allocation database by allocating `mallo`, loading source and demand records from `manure_allo.mnu`, and crosswalking decision tables and fertilizer references into numeric indices. |
| [sym:manure_demand_output] | manure_allocation_module | Reports demand-side withdrawals for each transaction in `mallo`, accumulates daily values into monthly, yearly, and average-annual totals, and clears the daily withdrawal array after writing. |
| [sym:manure_source_output] | manure_allocation_module | Reports source-side storage, production, and withdrawal balances for each source in `mallo`, rolls balances forward across reporting periods, and resets daily or monthly balance records with `malloz`. |
| [sym:actions] | manure_allocation_module | Populates manure-demand requests by copying the zeroed `manure_amtz` template into the selected demand record and then filling the allocation object, source object, application rate, and application method from the action table. |

## Lineage

`manure_allocation_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `914f365` (2025-10-30, "Changes to the manure allocation module. Mainly changed the demand object names"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `manure_allocation_module.f90` are listed.

- `914f365` (2025-10-30) — Changes to the manure allocation module. Mainly changed the demand object names
- `b095cf8` (2024-10-08) — truncation fixes
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `manure_allocation_module` has no extracted module-level documentation comment.
- The file provides utility operators `mallout_add` and `mallo_div_const`, but this page focuses on the shared allocation state they operate on.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
