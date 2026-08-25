---
kind: procedure
symbol: calsoft_read_codes
title: calsoft_read_codes
status: filled
source_hash: 54e0dcc6e012f6ae
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer for the file title line read from `codes.sft`; it is consumed
    only to skip the title/header metadata before the actual calibration codes record.
  header: Scratch character buffer for the second text line in `codes.sft`; it is read to
    advance past file header metadata before loading `cal_codes`.
  eof: I/O status code used to detect end-of-file or read failure while stepping through `codes.sft`;
    negative values stop the read loop.
  i_exist: Logical flag set by `inquire` to indicate whether the configured `codes.sft` file
    exists; it controls whether the routine attempts to read calibration codes.
uses:
  calibration_data_module: This module owns the soft-calibration code structure and the global
    `cal_soft` switch. `calsoft_read_codes` reads the `cal_codes` record from `codes.sft`
    and updates `cal_soft` based on those flags, so the routine depends on this module for
    both the target state and the meaning of each code.
  plant_data_module: This module is imported by the subroutine, but no specific symbols from
    it are referenced in the extracted source. It matters only as a dependency in the compilation
    context, and the context packet does not show a direct use here.
  input_file_module: The routine uses `in_chg%codes_sft` to determine which file to inquire,
    open, and read. This module supplies the configured soft-calibration filename, so it controls
    where the calibration codes are loaded from.
  soil_module: The module is imported, but the extracted source does not reference any soil
    symbols inside this routine. It is part of the broader calibration dependency set rather
    than an active data source here.
  plant_module: The module is imported, but no plant symbols are used in the visible code.
    It is a dependency because soft-calibration workflows later calibrate plant-related behavior,
    even though this loader does not touch those symbols directly.
  hydrograph_module: The module is imported so the routine can participate in calibration
    setup for hydrologic processes, but the extracted source does not reference any of its
    symbols directly.
  hru_lte_module: The module is imported because one soft-calibration flag (`hyd_hrul`) targets
    HRU LTE hydrologic calibration. The routine itself only reads the flag values; later calibration
    logic uses the module's processes.
  sd_channel_module: The module is imported because channel soft-calibration flags (`chsed`,
    `chnut`) correspond to channel processes. The loader does not compute channel behavior,
    but it prepares the flags that later channel calibration code will inspect.
  organic_mineral_mass_module: This module is imported as part of the calibration dependency
    set for nutrient and sediment mass accounting, but no symbols from it are referenced in
    the visible routine body.
  mgt_operations_module: The module is imported because management operations are part of
    the broader calibration workflow that may be conditioned on the soft-calibration flags.
    No direct symbol use is shown in this routine.
  conditional_module: This module is imported because calibration setup is integrated with
    conditional logic elsewhere in the model, but the extracted source does not reference
    any conditional symbols directly.
---

<!-- facts:header -->

Reads the soft-calibration code file and loads the calibration flags into shared model state. It also marks whether any soft calibration is enabled.

## Bottom Line

`calsoft_read_codes` is a small setup routine that checks for the soft calibration code file named by `in_chg%codes_sft`, reads its title, header, and the `cal_codes` record, and then closes the file. If the file is missing or set to `"null"`, it leaves the default calibration codes unchanged.

After reading the record, it turns on `cal_soft` when any soft-calibration option is active. That flag tells later calibration workflow whether the model should proceed with soft calibration steps for hydrology, plant growth, sediment, nutrients, channels, or reservoirs.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`proc_cal` calls this routine after plant calibration preparation and before the later soft-calibration readers such as `lcu_read_softcal`, `ls_read_lsparms_cal`, `aqu_read_elements`, `ch_read_elements`, and `res_read_elements`. Its results determine whether `cal_soft` is set to `y`, which later calibration logic uses to decide if soft calibration pathways should be active.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check file existence | Checks whether the configured soft-calibration file exists and is not marked as `null`. If the file is absent, the routine skips loading codes and leaves default calibration settings in place. |
| 2. skip missing-file branch | Bypasses the read loop when no usable file is available. The comment shows the old allocation idea was not used here. |
| 3. begin read loop | Enters a one-pass loop used to read the calibration file records in sequence. |
| 4. open codes file | Opens `codes.sft` on unit 107 so the routine can read the calibration metadata and code record. |
| 5. read title line | Reads the first line of the file into `titldum`, consuming the title or label record. |
| 6. stop on read failure | Exits the loop immediately if the title read hits end-of-file or another negative I/O status. |
| 7. read header line | Reads the header line into `header`, advancing to the data record that contains the calibration codes. |
| 8. stop on read failure | Exits the loop if the header read fails with end-of-file or a negative status. |
| 9. read calibration codes | Reads the soft-calibration flags directly into `cal_codes`, loading the per-process activation codes from the file. |
| 10. stop on read failure | Exits the loop if the calibration-code read fails, preventing use of incomplete input. |
| 11. evaluate soft calibration need | Tests the loaded codes and sets `cal_soft` to `y` when any supported soft-calibration option is active: hydrology (`hyd_hru` or `hyd_hrul`), plant growth, sediment, nutrient, channel sediment, channel nutrient, or reservoir calibration. |
| 12. close input file | Closes unit 107 after the file has been read or skipped, ending the `codes.sft` session. |
| 13. return to caller | Returns control to `proc_cal` after the calibration code state has been loaded or left at defaults. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:calibration_data_module] | `cal_codes, cal_soft` | `cal_codes%hyd_hru, cal_codes%hyd_hrul, cal_codes%plt, cal_codes%sed, cal_codes%nut, cal_codes%chsed, cal_codes%chnut, cal_codes%res` |
| [sym:plant_data_module] | `none resolved` | `none resolved` |
| [sym:input_file_module] | `in_chg` | `in_chg%codes_sft` |
| [sym:soil_module] | `none resolved` | `none resolved` |
| [sym:plant_module] | `none resolved` | `none resolved` |
| [sym:hydrograph_module] | `none resolved` | `none resolved` |
| [sym:hru_lte_module] | `none resolved` | `none resolved` |
| [sym:sd_channel_module] | `none resolved` | `none resolved` |
| [sym:organic_mineral_mass_module] | `none resolved` | `none resolved` |
| [sym:mgt_operations_module] | `none resolved` | `none resolved` |
| [sym:conditional_module] | `none resolved` | `none resolved` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cal_codes%plt` | When any of `cal_codes%hyd_hru`, `cal_codes%hyd_hrul`, `cal_codes%plt`, `cal_codes%sed`, `cal_codes%nut`, `cal_codes%chsed`, `cal_codes%chnut`, or `cal_codes%res` indicates soft calibration is active. | `cal_codes%plt` is populated from `codes.sft` and may remain `"n"` or become an active flag such as `"y"`; it contributes to deciding whether overall soft calibration should be enabled. |
| `cal_codes%nut` | When any of `cal_codes%hyd_hru`, `cal_codes%hyd_hrul`, `cal_codes%plt`, `cal_codes%sed`, `cal_codes%nut`, `cal_codes%chsed`, `cal_codes%chnut`, or `cal_codes%res` indicates soft calibration is active. | `cal_codes%nut` is populated from `codes.sft` and reflects whether nutrient calibration is requested; if it is `"y"`, it helps turn on `cal_soft`. |
| `cal_codes%chnut` | When any of `cal_codes%hyd_hru`, `cal_codes%hyd_hrul`, `cal_codes%plt`, `cal_codes%sed`, `cal_codes%nut`, `cal_codes%chsed`, `cal_codes%chnut`, or `cal_codes%res` indicates soft calibration is active. | `cal_codes%chnut` is loaded from `codes.sft` and flags channel nutrient calibration; a `"y"` value contributes to setting the global soft-calibration switch. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `calsoft_read_codes`. The initial add commit `df07e3f` introduced the routine, its module uses, the file read sequence, and the `cal_soft` activation test. Commit `c7c8e22` carried the same logic forward from the Bitbucket import without changing behavior. Commit `39fabde` made small cleanup changes: it initialized `titldum`, `header`, and `eof`, removed trailing whitespace, and normalized indentation, but did not alter the file-reading algorithm or the soft-calibration decision.

- `df07e3f` added the procedure with its `codes.sft` read flow and the `cal_soft` activation logic for the supported calibration flags.
- `39fabde` initialized local variables and cleaned formatting; behavior stayed the same, but the routine now starts with explicit default values for the scratch strings and `eof`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'calsoft_read_codes' has no extracted documentation comment.
- algorithm_steps revised: condensed the branch/loop actions into a clearer 13-step sequence while keeping all source-line citations.
- plant_data_module, soil_module, plant_module, hydrograph_module, hru_lte_module, sd_channel_module, organic_mineral_mass_module, mgt_operations_module, and conditional_module are imported but not directly referenced in the extracted body; their roles are inferred only from the procedure's calibration context.
- The source shows `close(107)` outside the file-existence branch, so the routine closes unit 107 even when the file was not opened; this is visible in the extracted code and may be intentional in the original model style.
