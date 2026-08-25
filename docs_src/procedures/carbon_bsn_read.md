---
kind: procedure
symbol: carbon_bsn_read
title: carbon_bsn_read
status: filled
source_hash: 7d96e0bdd4b14d48
version_label: SWAT+ 62.0.0
locals:
  titldum: Holds the first title/comment line read from each carbon input file; it is consumed
    only to advance past the optional header line and its contents are not otherwise used.
  header: Holds the second title/column-header line from each carbon input file; it is read
    and discarded as a header placeholder before the data records are parsed.
  eof: I/O status flag used by `read`, `open`, and `inquire` operations to detect missing
    files, open failures, end-of-file, and parse errors.
  i_exist: Logical flag set by `inquire` to tell whether the expected input file exists before
    attempting to open it.
  layer_id: Layer-group index read from each `carbon_lyr` record; it selects which `carbdb(:)`
    and `org_allo(:)` element to fill.
  max_lyr: Number of per-layer slots available in `carbdb`; used as the upper bound for valid
    `layer_id` values and for the final completeness check.
  rows_read: Counts how many valid per-layer rows were successfully loaded; compared against
    `max_lyr` to detect missing layer records.
  carbon_lyr: Holds the derived per-layer file name built from `in_basin%carbon_bsn` by appending
    `_lyr` before the `.bsn` extension, or `_lyr.bsn` if no extension is present.
  idot: Position of the last `.` in `in_basin%carbon_bsn`; used to split the basename from
    its extension when constructing `carbon_lyr`.
  r_hp_rate: Temporary scalar for the passive-humus transformation rate read from a `carbon_lyr`
    row before storing it in `carbdb(layer_id)%hp_rate`.
  r_hs_rate: Temporary scalar for the slow-humus transformation rate read from a `carbon_lyr`
    row before storing it in `carbdb(layer_id)%hs_rate`.
  r_microb_rate: Temporary scalar for the microbial biomass transformation rate read from
    a `carbon_lyr` row before storing it in `carbdb(layer_id)%microb_rate`.
  r_meta_rate: Temporary scalar for the metabolic litter transformation rate read from a `carbon_lyr`
    row before storing it in `carbdb(layer_id)%meta_rate`.
  r_str_rate: Temporary scalar for the structural litter transformation rate read from a `carbon_lyr`
    row before storing it in `carbdb(layer_id)%str_rate`.
  r_microb_top_rate: Temporary scalar for the top-soil microbial activity coefficient read
    from a `carbon_lyr` row before storing it in `carbdb(layer_id)%microb_top_rate`.
  r_hs_hp: Temporary scalar for the slow-to-passive humus allocation coefficient read from
    a `carbon_lyr` row before storing it in `carbdb(layer_id)%hs_hp`.
  r_a1co2: Temporary scalar for the allocation of decomposed metabolic/passive carbon to CO2
    before storing it in `org_allo(layer_id)%a1co2`.
  r_asco2: Temporary scalar for the allocation of decomposed slow humus to CO2 before storing
    it in `org_allo(layer_id)%asco2`.
  r_apco2: Temporary scalar for the allocation of decomposed passive humus to CO2 before storing
    it in `org_allo(layer_id)%apco2`.
  r_abco2: Temporary scalar for the allocation of decomposed microbial biomass to CO2 before
    storing it in `org_allo(layer_id)%abco2`.
  mathers_int: Integer flag read from `carbon.bsn` and converted to `org_frac%mathers_method`;
    `1` enables the Mathers humus-slow initialization method, other values leave it false.
uses:
  carbon_module: '`carbon_module` holds every carbon parameter this reader populates: basin-wide
    residue-decomposition tunables, organic fraction controls, per-layer carbon inputs, and
    organic CO2 allocation fractions. Without those module variables, the routine would have
    nowhere to store the parsed file contents and later carbon initialization code would not
    see the configured values.'
  basin_module: '`basin_module` provides `bsn_cc%cswat`, the switch that decides whether this
    reader should run at all. It also supplies the basin state namespace used elsewhere in
    the basin setup sequence, so this routine only executes when carbon mode 2 is enabled.'
  tillage_data_module: '`tillage_data_module` supplies the basin carbon parameters that are
    read from `carbon.bsn` and reused by tillage and biomixing calculations, including the
    days/effects and mixing coefficients. Loading them here makes those later disturbance
    calculations use the file-driven carbon settings.'
  plant_data_module: '`plant_data_module` provides `photo_degrade_factor`, which is one of
    the basin-wide carbon scalars read from `carbon.bsn`. It matters here because the routine
    initializes that residue-photo degradation control before plant and residue processes
    use it.'
  input_file_module: '`input_file_module` provides `in_basin%carbon_bsn`, the configured basin
    carbon filename. This routine reads that path to open the scalar file and derives the
    companion per-layer filename from it, so the input-file module controls which records
    are loaded.'
---

<!-- facts:header -->

Reads basin-wide carbon settings from `carbon.bsn` and per-layer carbon coefficients from the matching `_lyr.bsn` file. It validates the files, loads shared carbon parameters into module state, and stops with an error if required data are missing or malformed.

## Bottom Line

`carbon_bsn_read` is the basin-level carbon configuration reader used when `bsn_cc%cswat == 2`. It first reads scalar carbon controls from `in_basin%carbon_bsn`, then derives the per-layer filename from that basename, reads layer-specific coefficients into `carbdb(:)` and `org_allo(:)`, and rejects missing, unopened, malformed, or incomplete input with error messages and `error stop`.

The routine matters because later carbon calculations depend on the module state it fills: residue decomposition tunables, temperature/water controls, Mathers-method selection, and per-layer transformation/allocation coefficients. If these values are not loaded correctly, downstream carbon initialization and soil/carbon routines will use defaults or fail to reflect the basin file contents.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during basin setup inside `proc_bsn`, after the basin parameters, basin print codes, and CO2 inputs are read and before `carbon_layers_read` is called. Its results populate the carbon-module state that later carbon initialization and soil carbon routines depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Exit immediately when carbon mode 2 is not active | Checks `bsn_cc%cswat` and returns without doing any work unless carbon mode 2 is enabled. |
| 2. Verify the basin carbon file exists | Uses `inquire` on `in_basin%carbon_bsn`; if the file is missing, writes an error to the console and log and stops the model. |
| 3. Open and read the basin carbon scalars | Opens `carbon.bsn`, skips the optional title and header lines with character reads, then reads the basin-wide carbon coefficients and the Mathers-method flag into module state. |
| 4. Close the basin carbon file | Closes unit 107 after the basin scalar row has been processed. |
| 5. Derive the per-layer filename from `carbon.bsn` | Uses the last dot in `in_basin%carbon_bsn` to build `carbon_lyr`; if an extension exists it inserts `_lyr` before it, otherwise it appends `_lyr.bsn`. |
| 6. Verify and open the per-layer carbon file | Checks that `carbon_lyr` exists, reports and stops if not, then opens it on unit 107 for reading. |
| 7. Skip the per-layer title and header lines | Reads two character records from the per-layer file to consume the optional title and column header. |
| 8. Set the expected number of layer groups | Stores `size(carbdb)` in `max_lyr` so the routine knows how many valid layer-group rows should be present. |
| 9. Read each layer-group record until end-of-file | Loops over the remaining records, reading a layer id and 11 coefficients each time. Rows with invalid `layer_id` values are reported and skipped; valid rows are copied into `carbdb(layer_id)` and `org_allo(layer_id)`, and `rows_read` is incremented. |
| 10. Check that all expected layer rows were read | Compares `rows_read` to `max_lyr`; if any layer rows are missing, it writes an error message, closes the file, and stops. |
| 11. Close the per-layer file and return | Closes unit 107 after successful completion and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:carbon_module] | `org_frac, cb_wtr_coef, man_coef, org_con, carbdb, org_allo, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref` | `org_frac%frac_seq, org_frac%frac_hum_microb, org_frac%frac_hum_slow, org_frac%frac_hum_passive, cb_wtr_coef%prmt_21, cb_wtr_coef%prmt_44, man_coef%rtof, org_con%tmpf, org_con%watf, org_con%tn, org_con%top, org_con%tx, org_frac%mathers_method, carbdb(layer_id)%hp_rate, carbdb(layer_id)%hs_rate, carbdb(layer_id)%microb_rate, carbdb(layer_id)%meta_rate, carbdb(layer_id)%str_rate, carbdb(layer_id)%microb_top_rate, carbdb(layer_id)%hs_hp, org_allo(layer_id)%a1co2, org_allo(layer_id)%asco2, org_allo(layer_id)%apco2, org_allo(layer_id)%abco2` |
| [sym:basin_module] | `bsn_cc, bsn` | `bsn_cc%cswat` |
| [sym:tillage_data_module] | `till_eff_days, bio_consf, till_consf, bmix_a, bmix_b, bmix_c, tillmix_a, tillmix_b, tillmix_c` |  |
| [sym:plant_data_module] | `photo_degrade_factor` |  |
| [sym:input_file_module] | `in_basin` | `in_basin%carbon_bsn, in_basin%carbon_bsn(1:idot-1), in_basin%carbon_bsn(idot:)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `org_frac%mathers_method` | When `bsn_cc%cswat == 2` and the basin data row has been read successfully, `mathers_int` is converted with `org_frac%mathers_method = (mathers_int == 1)`. | This sets whether the Mathers humus-slow initialization method is enabled for later soil carbon initialization. |
| `carbdb(layer_id)%hp_rate` | For each valid per-layer record where `1 <= layer_id <= max_lyr`, the read value `r_hp_rate` is copied into `carbdb(layer_id)%hp_rate`. | This stores the passive-humus transformation rate for that layer group so later carbon routines can use the file-driven coefficient. |
| `carbdb(layer_id)%hs_rate` | For each valid per-layer record where `1 <= layer_id <= max_lyr`, the read value `r_hs_rate` is copied into `carbdb(layer_id)%hs_rate`. | This stores the slow-humus transformation rate for later carbon calculations. |
| `carbdb(layer_id)%microb_rate` | For each valid per-layer record where `1 <= layer_id <= max_lyr`, the read value `r_microb_rate` is copied into `carbdb(layer_id)%microb_rate`. | This stores the microbial biomass transformation rate for later carbon calculations. |
| `carbdb(layer_id)%meta_rate` | For each valid per-layer record where `1 <= layer_id <= max_lyr`, the read value `r_meta_rate` is copied into `carbdb(layer_id)%meta_rate`. | This stores the metabolic litter transformation rate for later carbon calculations. |
| `carbdb(layer_id)%str_rate` | For each valid per-layer record where `1 <= layer_id <= max_lyr`, the read value `r_str_rate` is copied into `carbdb(layer_id)%str_rate`. | This stores the structural litter transformation rate for later carbon calculations. |
| `carbdb(layer_id)%microb_top_rate` | For each valid per-layer record where `1 <= layer_id <= max_lyr`, the read value `r_microb_top_rate` is copied into `carbdb(layer_id)%microb_top_rate`. | This stores the top-soil microbial activity coefficient used by later carbon routines. |
| `carbdb(layer_id)%hs_hp` | For each valid per-layer record where `1 <= layer_id <= max_lyr`, the read value `r_hs_hp` is copied into `carbdb(layer_id)%hs_hp`. | This stores the slow-to-passive humus allocation coefficient for later carbon calculations. |
| `org_allo(layer_id)%a1co2` | For each valid per-layer record where `1 <= layer_id <= max_lyr`, the read value `r_a1co2` is copied into `org_allo(layer_id)%a1co2`. | This sets the fraction of decomposed metabolic/passive carbon routed to CO2 for that layer group. |
| `org_allo(layer_id)%asco2` | For each valid per-layer record where `1 <= layer_id <= max_lyr`, the read value `r_asco2` is copied into `org_allo(layer_id)%asco2`. | This sets the fraction of decomposed slow humus routed to CO2 for that layer group. |
| `org_allo(layer_id)%apco2` | For each valid per-layer record where `1 <= layer_id <= max_lyr`, the read value `r_apco2` is copied into `org_allo(layer_id)%apco2`. | This sets the fraction of decomposed passive humus routed to CO2 for that layer group. |
| `org_allo(layer_id)%abco2` | For each valid per-layer record where `1 <= layer_id <= max_lyr`, the read value `r_abco2` is copied into `org_allo(layer_id)%abco2`. | This sets the fraction of decomposed microbial biomass routed to CO2 for that layer group. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `carbon_bsn_read`: `bc7755a` introduced the subroutine to read `carbon.bsn` and the per-layer carbon file; `821a63e` added the derived `carbon_lyr` filename, `idot`, out-of-range row warnings, and the final row-count validation; `dfce092` switched the activation gate and error text from carbon code 1 to code 2. `6329ff2` then changed the header reading to use `'(a)'` for optional blank title/header lines and updated parse-failure messaging to say the data/values line may be missing or malformed.

- Introduced the carbon basin reader, including the basin scalar file read, per-layer table read, and the module assignments for carbon coefficients and allocation fractions.
- Added dynamic construction of the per-layer filename from `in_basin%carbon_bsn`, plus per-row layer-id validation, incomplete-table detection, and the final row-count check.
- Changed the carbon activation gate and related error messages from code 1 to code 2 so the routine only runs for the current carbon mode.
- Made the title and header reads tolerant of blank lines by using character reads, and broadened the parse-error text to cover missing or malformed data/value lines.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'carbon_bsn_read' has no extracted documentation comment.
