---
kind: module
symbol: soil_nutcarb_module
title: soil_nutcarb_module
status: filled
source_hash: 7461ab919bdea6bd
version_label: SWAT+ 62.0.0
variables:
  orgc_hdr: Module-owned instance of `organic_carbon_header`. It holds the column labels for
    the HRU organic-carbon output table and is written by `header_snutc` to `hru_orgc.txt`.
  totc_hdr: Module-owned instance of `total_carbon_header`. It holds the column labels for
    the HRU and basin total-carbon output tables and is written by `header_snutc` to `hru_totc.txt`
    and `basin_totc.txt`.
  orgc_units: Module-owned instance of `organic_carbon_units`. It holds the unit labels for
    the HRU organic-carbon output table and is written by `header_snutc` alongside `orgc_hdr`.
  totc_units: Module-owned instance of `total_carbon_units`. It holds the unit labels for
    the HRU and basin total-carbon output tables and is written by `header_snutc` alongside
    `totc_hdr`.
type_components:
  organic_carbon_header:
    day_mo: Header label for the day-of-month/day field used in the organic-carbon summary.
    yrc: Header label for the year field.
    hru: Header label for the HRU or unit identifier column.
    str_c: Header label for structural carbon.
    lig_c: Header label for lignin carbon.
    meta_c: Header label for metabolic carbon.
    man_c: Header label for manure carbon.
    hum_c: Header label for humic carbon.
    phum_c: Header label for passive humic carbon.
    mb_c: Header label for microbial biomass carbon.
  total_carbon_header:
    day: Header label for the day-of-year field.
    yrc: Header label for the year field.
    isd: Header label for the unit or basin identifier column.
    soil_org_c: Header label for total soil organic carbon.
    plm_com_c: Header label for total plant carbon.
    rsd_com_c: Header label for total residue carbon.
  organic_carbon_units:
    day: Unit placeholder for the day field.
    yrc: Unit placeholder for the year field.
    isd: Unit placeholder for the unit identifier field.
    str_c: Units for structural carbon, expressed as kilograms per hectare.
    lig_c: Units for lignin carbon, expressed as kilograms per hectare.
    meta_c: Units for metabolic carbon, expressed as kilograms per hectare.
    man_c: Units for manure carbon, expressed as kilograms per hectare.
    hum_c: Units for humic carbon, expressed as kilograms per hectare.
    phum_c: Units for passive humic carbon, expressed as kilograms per hectare.
    mb_c: Units for microbial biomass carbon, expressed as kilograms per hectare.
  total_carbon_units:
    day: Unit placeholder for the day field.
    yrc: Unit placeholder for the year field.
    isd: Unit placeholder for the unit or basin identifier field.
    soil_org_c: Units for total soil organic carbon, expressed as kilograms per hectare.
    plm_com_c: Units for total plant carbon, expressed as kilograms per hectare.
    rsd_com_c: Units for total residue carbon, expressed as kilograms per hectare.
type_summaries:
  organic_carbon_header: Character label record for the HRU organic-carbon output header row.
  total_carbon_header: Character label record for the HRU and basin total-carbon output header
    row.
  organic_carbon_units: Character unit record for the HRU organic-carbon output table.
  total_carbon_units: Character unit record for the HRU and basin total-carbon output tables.
---

<!-- facts:header -->

Declares the reusable header and units records for SWAT+ soil carbon output tables. It owns the title strings and unit strings for HRU organic carbon, HRU total carbon, and basin total carbon summaries; `header_snutc` imports these records and writes them to the carbon output files.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only. It defines four public derived-type instances with default string values; the `header_snutc` routine reads and writes those values when producing the carbon output file headers.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:header_snutc] | `unit_2610, unit_9000, unit_2611, unit_2613` | `orgc_hdr, totc_hdr, orgc_units, totc_units` | Reads the module's header and unit records and writes them to the HRU organic-carbon, HRU total-carbon, and basin total-carbon output files. |

## Key Consumers

The only extracted importer is the carbon-header writer. It uses this module as a shared source of printable labels and units for the three soil-carbon output streams.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:header_snutc] | soil_nutcarb_module | When HRU output is enabled, `header_snutc` opens the carbon output files and writes `orgc_hdr`, `orgc_units`, `totc_hdr`, and `totc_units` to emit the column names and units for the HRU organic carbon, HRU total carbon, and basin total carbon summaries. |

## Lineage

`soil_nutcarb_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `soil_nutcarb_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `soil_nutcarb_module` has no extracted module-level documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
