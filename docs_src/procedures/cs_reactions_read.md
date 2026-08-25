---
kind: procedure
symbol: cs_reactions_read
title: cs_reactions_read
status: filled
source_hash: 41bef132b460a2ae
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary 80-character title line read from the file header and discarded after
    the initial read.
  header: Temporary 80-character section header string used to advance through labeled blocks
    in `cs_reactions`.
  eof: I/O status flag for the first header read; if the file is missing or the read fails,
    it controls whether the routine proceeds.
  icount: Loop index used for reaction tables, geologic shale rows, HRU objects, and aquifer
    objects.
  igroup: Column index when reading a row of reaction-group values into `rct`.
  irct: Column index when reading the three shale reaction values into `rct_shale`.
  ishale: Index for shale formations within each HRU or aquifer object's shale-related arrays.
  group: Reaction-group selector read for each HRU or aquifer object; it chooses which row
    of `rct` applies to that object.
  hru_dum: HRU identifier read from the file and not stored here; used to consume each HRU
    object line.
  aqu_dum: Aquifer identifier read from the file and not stored here; used to consume each
    aquifer object line.
  i_exist: Logical file-existence flag set by `inquire`; it gates all later file reading and
    allocation work.
  num_rct: Count of reaction-parameter rows in the `rct` table read from file.
  num_groups: Count of reaction-group columns in the `rct` table read from file.
  shale_fractions: Scratch array holding the shale-fraction values read for each object before
    they are copied into `cs_rct_soil` or `cs_rct_aqu`.
uses:
  hydrograph_module: '`hydrograph_module` supplies `sp_ob%hru` and `sp_ob%aqu`, which determine
    how many soil and aquifer reaction records the routine allocates and fills.'
  constituent_mass_module: '`constituent_mass_module` is imported by the routine, but the
    provided source context does not resolve any directly used symbols from it; it still matters
    because it is part of the routine''s shared model-state context.'
  cs_data_module: '`cs_data_module` provides the destination arrays and types that receive
    the parsed reaction data, including the `rct` and `rct_shale` tables and the `cs_rct_soil`/`cs_rct_aqu`
    records whose fields are assigned from those tables.'
---

<!-- facts:header -->

Reads the `cs_reactions` input file and loads chemical reaction parameters for HRUs and aquifers into shared SWAT+ state.

## Bottom Line

`cs_reactions_read` is an input-loader subroutine. It checks whether the `cs_reactions` file exists, opens it, skips the title and section headers, and reads reaction tables into module arrays for soil and aquifer constituents.

It matters because later model code can use the populated `cs_rct_soil` and `cs_rct_aqu` records to supply per-object reaction coefficients, shale fractions, and related kinetic/sorption parameters.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the model input-reading phase, called from `proc_read` after other constituent input readers and before later readers such as `cs_urban_read`, `topo_read`, and `hydrol_read`. Its results populate shared reaction-parameter state that later model calculations can use for HRU and aquifer constituent behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize locals and check for the input file | The routine zeroes its counters, declares scratch storage, and uses `inquire(file="cs_reactions", exist=i_exist)` to decide whether the reactions file is present before doing any allocation or reads. |
| 2. Open the reactions file and consume the title line | If the file exists, it opens unit 107 on `cs_reactions` and reads the first line into `titldum`, capturing the file title and initial read status. |
| 3. Allocate soil and aquifer reaction containers | The routine allocates `cs_rct_soil` for each HRU and `cs_rct_aqu` for each aquifer using `sp_ob%hru` and `sp_ob%aqu` from `hydrograph_module`. |
| 4. Read the reaction-parameter table | It reads a header, the row and column counts, allocates `rct(num_rct,num_groups)`, then reads every row of the reaction table into `rct`. |
| 5. Read geologic shale parameters | The routine reads another header, the number of shale formations, allocates `rct_shale(num_geol_shale,3)`, and fills the three shale coefficients for each formation. |
| 6. Populate HRU reaction records | For each HRU, it allocates shale-related arrays, reads the HRU identifier, selected reaction group, and shale fractions, then copies the chosen reaction-row values and shale-table values into `cs_rct_soil(icount)`. |
| 7. Populate aquifer reaction records when aquifers exist | If `sp_ob%aqu > 0`, it reads the aquifer section header and fills each `cs_rct_aqu(icount)` record with the same pattern used for HRUs, but using the aquifer-specific `oxy_aqu` and `kseo4` assignments. |
| 8. Close the file and return | After all sections are processed, it closes unit 107 and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru, sp_ob%aqu` |
| [sym:constituent_mass_module] | `constituent_mass_module` | `none resolved` |
| [sym:cs_data_module] | `cs_rct_soil, cs_rct_aqu, rct, rct_shale, num_geol_shale` | `cs_rct_soil(icount)%shale(num_geol_shale), cs_rct_soil(icount)%sseratio(num_geol_shale), cs_rct_soil(icount)%ko2a(num_geol_shale), cs_rct_soil(icount)%kno3a(num_geol_shale), cs_rct_soil(icount)%se_ino3, cs_rct_soil(icount)%oxy_soil, cs_rct_soil(icount)%kd_seo4, cs_rct_soil(icount)%kd_seo3, cs_rct_soil(icount)%kd_born, cs_rct_soil(icount)%kseo4, cs_rct_soil(icount)%shale(ishale), cs_rct_soil(icount)%sseratio(ishale), cs_rct_soil(icount)%ko2a(ishale), cs_rct_soil(icount)%kno3a(ishale), cs_rct_aqu(icount)%shale(num_geol_shale), cs_rct_aqu(icount)%sseratio(num_geol_shale), cs_rct_aqu(icount)%ko2a(num_geol_shale), cs_rct_aqu(icount)%kno3a(num_geol_shale), cs_rct_aqu(icount)%se_ino3, cs_rct_aqu(icount)%oxy_aqu, cs_rct_aqu(icount)%kd_seo4, cs_rct_aqu(icount)%kd_seo3, cs_rct_aqu(icount)%kd_born, cs_rct_aqu(icount)%kseo4, cs_rct_aqu(icount)%shale(ishale), cs_rct_aqu(icount)%sseratio(ishale), cs_rct_aqu(icount)%ko2a(ishale), cs_rct_aqu(icount)%kno3a(ishale)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_rct_soil(icount)%se_ino3` | For each HRU object line read from `cs_reactions` (inside `do icount=1,sp_ob%hru`). | Stores the reaction-row value selected by `group` into the HRU's selenium-inhibition factor, replacing the default zero value with the file-supplied parameter. |
| `cs_rct_soil(icount)%oxy_soil` | For each HRU object line read from `cs_reactions` (inside `do icount=1,sp_ob%hru`). | Stores the reaction-row value selected by `group` into the HRU's soil-water oxygen concentration field. |
| `cs_rct_soil(icount)%kd_seo4` | For each HRU object line read from `cs_reactions` (inside `do icount=1,sp_ob%hru`). | Stores the shared reaction-row sorption coefficient for selenium oxyanion in soil records. |
| `cs_rct_soil(icount)%kd_seo3` | For each HRU object line read from `cs_reactions` (inside `do icount=1,sp_ob%hru`). | Stores the shared reaction-row sorption coefficient for selenium oxyanion in soil records. |
| `cs_rct_soil(icount)%kd_born` | For each HRU object line read from `cs_reactions` (inside `do icount=1,sp_ob%hru`). | Stores the boron sorption coefficient selected from the reaction table for the current HRU. |
| `cs_rct_soil(icount)%kseo4` | For each HRU object line read from `cs_reactions` (inside `do icount=1,sp_ob%hru`). | Stores the selenium reduction rate constant selected from the reaction table for the current HRU. |
| `cs_rct_soil(icount)%shale(ishale)` | For each shale fraction read for an HRU, after `shale_fractions(ishale)` has been read from file. | Copies the per-shale fraction read from `cs_reactions` into the HRU's shale-fraction array. |
| `cs_rct_soil(icount)%sseratio(ishale)` | For each shale fraction read for an HRU, after `rct_shale` has been loaded. | Copies the shale sulfur/se ratio for each geologic unit into the HRU's shale parameter array. |
| `cs_rct_soil(icount)%ko2a(ishale)` | For each shale fraction read for an HRU, after `rct_shale` has been loaded. | Copies the shale autotrophic oxygen-reduction coefficient for each geologic unit into the HRU's shale parameter array. |
| `cs_rct_soil(icount)%kno3a(ishale)` | For each shale fraction read for an HRU, after `rct_shale` has been loaded. | Copies the shale autotrophic nitrate-reduction coefficient for each geologic unit into the HRU's shale parameter array. |
| `cs_rct_aqu(icount)%se_ino3` | For each aquifer object line read from `cs_reactions` when `sp_ob%aqu > 0`. | Stores the reaction-row value selected by `group` into the aquifer's selenium-inhibition factor. |
| `cs_rct_aqu(icount)%oxy_aqu` | For each aquifer object line read from `cs_reactions` when `sp_ob%aqu > 0`. | Stores the reaction-row oxygen concentration value for groundwater into the aquifer reaction record. |
| `cs_rct_aqu(icount)%kd_seo4` | For each aquifer object line read from `cs_reactions` when `sp_ob%aqu > 0`. | Stores the selenium oxyanion sorption coefficient for the aquifer reaction record. |
| `cs_rct_aqu(icount)%kd_seo3` | For each aquifer object line read from `cs_reactions` when `sp_ob%aqu > 0`. | Stores the selenium oxyanion sorption coefficient for the aquifer reaction record. |
| `cs_rct_aqu(icount)%kd_born` | For each aquifer object line read from `cs_reactions` when `sp_ob%aqu > 0`. | Stores the boron sorption coefficient selected from the reaction table for the aquifer. |
| `cs_rct_aqu(icount)%kseo4` | For each aquifer object line read from `cs_reactions` when `sp_ob%aqu > 0`. | Stores the selenium reduction rate constant selected from the reaction table for the aquifer. |
| `cs_rct_aqu(icount)%shale(ishale)` | For each shale fraction read for an aquifer, after `shale_fractions(ishale)` has been read from file. | Copies the per-shale fraction read from `cs_reactions` into the aquifer's shale-fraction array. |
| `cs_rct_aqu(icount)%sseratio(ishale)` | For each shale fraction read for an aquifer, after `rct_shale` has been loaded. | Copies the shale sulfur/se ratio for each geologic unit into the aquifer's shale parameter array. |
| `cs_rct_aqu(icount)%ko2a(ishale)` | For each shale fraction read for an aquifer, after `rct_shale` has been loaded. | Copies the shale autotrophic oxygen-reduction coefficient for each geologic unit into the aquifer's shale parameter array. |
| `cs_rct_aqu(icount)%kno3a(ishale)` | For each shale fraction read for an aquifer, after `rct_shale` has been loaded. | Copies the shale autotrophic nitrate-reduction coefficient for each geologic unit into the aquifer's shale parameter array. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows the routine was introduced in 94b6dec/df07e3f as a new file that reads `cs_reactions`, allocates `cs_rct_soil` and `cs_rct_aqu`, and fills `rct` and `rct_shale`. 39fabde initialized local scalars, changed `rct`/`rct_shale` and per-object shale arrays to zero-initialized allocations, and 2ee1889 changed only the final program unit syntax from `end` to `end subroutine cs_reactions_read`.

- 94b6dec/df07e3f established the routine's file-reading workflow and data loading into reaction arrays and per-object records.
- 39fabde added explicit initialization for local scalars and zero-filled allocations for the reaction tables and shale arrays.
- 2ee1889 made a non-behavioral source cleanup by replacing the generic end statement with `end subroutine cs_reactions_read`.
- 35b029c preserved the same reader logic and file structure, with no behavioral change visible in the diff beyond formatting/comments.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- constituent_mass_module is imported, but no directly resolved symbols from it were available in the provided context; documentation should treat its use as unresolved unless a fuller source scan is added.
- algorithm_steps revised: compressed the draft into 8 source-backed steps that match the visible control flow and reads/allocations in the source.
