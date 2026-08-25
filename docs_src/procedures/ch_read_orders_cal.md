---
kind: procedure
symbol: ch_read_orders_cal
title: ch_read_orders_cal
status: filled
source_hash: e8cddfd19cdb7bfb
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer for the first title/header line read from `ch_sed_budget.sft`;
    it is only used to advance past the file's introductory text.
  header: Temporary character buffer for section header lines in `ch_sed_budget.sft`, including
    the line before each region's order block.
  eof: I/O status flag used on each `read` to detect end-of-file or read failure while scanning
    `ch_sed_budget.sft`.
  ihru: Loop index over HRUs in a channel region when transferring region membership from
    `ccu_reg` to `ccu_cal`.
  i_exist: Logical result of `inquire` used to decide whether the configured calibration file
    exists before attempting to read it.
  imax: Initialized counter placeholder; it is reset but not used in the extracted logic.
  mcal: Initialized counter placeholder; it is reset but not used in the extracted logic.
  mreg: Number of channel calibration regions read from the file and later used to size `chcal`
    and assign `db_mx%ch_reg`.
  i: Loop index over calibration regions stored in `chcal`.
  nspu: Number of spatial units listed for a region in the input record; it controls whether
    the routine expands explicit element lists or defaults to all channels.
  isp: Loop index used while reading `nspu` element numbers into `elem_cnt`.
  ielem: Counter for the expanded number of channel elements in a region and later an index
    into `chcal(i)%num`.
  ii: Loop index used to walk through the packed `elem_cnt` encoding of channel ranges and
    singletons.
  ie: Inner loop index used to expand a contiguous element range into individual channel numbers.
  ie1: Starting value of a channel index or range endpoint read from `elem_cnt`.
  ie2: Second value of a range or a look-ahead element value used to decide whether the next
    packed entry is a singleton or an encoded range.
  iord_mx: Number of order blocks for the current region; it is used to allocate `chcal(i)%ord`.
  iord: Loop index over the order records inside one calibration region.
  ich_s: Loop index over the channel numbers stored in `chcal(i)%num` when summing total channel
    length.
uses:
  input_file_module: The file path `in_chg%ch_sed_budget_sft` comes from `input_file_module`,
    so that module controls which calibration configuration file this routine opens and reads.
  maximum_data_module: '`db_mx%cha_reg` and `db_mx%ch_reg` are the channel-region maxima bookkeeping
    fields in `maximum_data_module`; this routine checks the existing channel-region count
    before filling HRU-linked channel data and then records the total number of channel calibration
    regions it read.'
  calibration_data_module: '`calibration_data_module` provides the `chcal`, `ccu_reg`, `ccu_cal`,
    and `ccu_elem` arrays that this routine populates. These types hold the channel-region
    names, channel numbers, order descriptors, HRU membership, and per-HRU area values needed
    for calibration setup.'
  hydrograph_module: '`sp_ob%chandeg` from `hydrograph_module` supplies the default count
    of SWAT-deg channels when a calibration region has no explicit `nspu` list, so it determines
    the fallback region membership size.'
  sd_channel_module: '`sd_ch(ich)%chl` from `sd_channel_module` provides each channel reach''s
    length, which this routine sums into each region/order length so the calibration record
    can carry total channel length.'
---

<!-- facts:header -->

Reads channel sediment-budget calibration orders from `ch_sed_budget.sft` and populates the channel calibration database. It also maps channel regions to HRUs and accumulates channel lengths by order region.

## Bottom Line

This subroutine loads channel soft-calibration order data from the file named by `in_chg%ch_sed_budget_sft`. It first determines how many channel calibration regions exist, then reads each region's channel list and order metadata into `chcal`, including the channel numbers to calibrate and the order-specific measurement records.

The routine matters because later calibration logic depends on the `chcal` structures it fills: region membership, order count, measurement descriptors, and total channel length. It also derives channel-region HRU mappings from `ccu_reg`/`ccu_elem`, and it stores the total number of channel calibration regions in `db_mx%ch_reg`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during calibration setup inside `proc_cal`, after the other element-definition readers have run and before calibration allocation initialization. Its output is used later by the calibration system to know which channel regions and orders exist, how they map to channels and HRUs, and what total channel length belongs to each order.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local counters and check the configured file name | Reset working counters, inquire whether `in_chg%ch_sed_budget_sft` exists, and branch to a no-data allocation if the file is missing or set to `null`. |
| 2. Open the soft calibration file and read its prologue | Open unit 107 on the calibration file, read the title line, read the region count `mreg`, read a header line, and allocate `chcal(mreg)`. |
| 3. Read each channel calibration region record | Loop over the `mreg` regions, read each region's name, order count, and `nspu`, and if the record includes explicit spatial units, backspace and reread the full record with the `elem_cnt` list. |
| 4. Expand packed channel-element lists into explicit channel numbers | Interpret the `elem_cnt` encoding as either single channels or channel ranges, count the total number of channels, allocate `chcal(i)%num`, store `num_tot`, and fill the explicit channel-number list. |
| 5. Fall back to all SWAT-deg channels when no explicit region list exists | If `nspu` is not positive, allocate one slot per channel in `sp_ob%chandeg`, set `chcal(i)%num_tot` to that count, and populate the region with every channel index from 1 through `sp_ob%chandeg`. |
| 6. Read the order header and allocate order slots | Read the next header line, and when `chcal(i)%ord_num > 0`, store that count in `iord_mx` and allocate the `ord` array for the region. |
| 7. Load each order measurement definition | Read each order's `meas` descriptor from the file into `chcal(i)%ord(iord)%meas`. |
| 8. Map region HRUs and compute their areas when channel-region bookkeeping is enabled | If `db_mx%cha_reg > 0`, loop over `ccu_reg(i)` HRUs, translate each element number to an object number in `ccu_elem`, and store the HRU type and area in `ccu_cal(i)`. |
| 9. Sum channel lengths across the region's member channels | Loop through every stored channel number in `chcal(i)%num`, fetch each channel's length from `sd_ch(ich)%chl`, and add it to `chcal(i)%ord(iord)%length`. |
| 10. Finish the file scan and store the region count | Exit the file-processing loop and save the final region count in `db_mx%ch_reg` before returning. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_chg` | `in_chg%ch_sed_budget_sft` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cha_reg, db_mx%ch_reg` |
| [sym:calibration_data_module] | `chcal, ccu_reg, ccu_cal, ccu_elem` | `chcal(i)%name, chcal(i)%ord_num, chcal(i)%num(ielem), chcal(i)%num_tot, chcal(i)%num, chcal(i)%num(ich), chcal(i)%ord(iord_mx), chcal(i)%ord(iord)%meas, ccu_reg(i)%num_tot, ccu_reg(i)%num(ihru), ccu_cal(i)%num(ihru), ccu_elem(ielem)%obtypno, ccu_cal(i)%hru_ha(ihru), ccu_elem(ielem)%ru_frac, ccu_cal(i)%area_ha, chcal(i)%num(ich_s), chcal(i)%ord(iord)%length` |
| [sym:hydrograph_module] | `sp_ob, elem_cnt, ich` | `sp_ob%chandeg` |
| [sym:sd_channel_module] | `sd_ch` | `sd_ch(ich)%chl` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `chcal(i)%num_tot` | When a region record is read and its `nspu` value is positive, after the code counts the expanded channel entries for that region. | `chcal(i)%num_tot` is set to the total number of explicit channel numbers represented by the packed `elem_cnt` list for that calibration region. |
| `chcal(i)%num(ielem)` | When `nspu > 0` and the packed region list has been expanded into explicit channel numbers. | `chcal(i)%num(ielem)` stores each individual channel number belonging to the region after range expansion. |
| `chcal(i)%num(ich)` | When `nspu <= 0`, meaning no explicit channel list was provided for the region. | `chcal(i)%num(ich)` is filled with every channel index from 1 to `sp_ob%chandeg` to represent all SWAT-deg channels in the region. |
| `ccu_cal(i)%num(ihru)` | When `db_mx%cha_reg > 0` and the routine is filling channel-region HRU bookkeeping from `ccu_reg(i)`. | `ccu_cal(i)%num(ihru)` is updated from each region element's object type number so the channel calibration record knows the HRU/object mapping. |
| `ccu_cal(i)%hru_ha(ihru)` | When `db_mx%cha_reg > 0` and a region HRU entry has been resolved to `ccu_elem(ielem)`. | `ccu_cal(i)%hru_ha(ihru)` is set to the HRU's area in hectares, computed as `ccu_elem(ielem)%ru_frac * ccu_cal(i)%area_ha`. |
| `ich` | When a region is populated with explicit channels or when the default-all-channels branch assigns members. | `ich` is used as the current channel index while the routine stores and later sums channel membership and lengths. |
| `chcal(i)%ord(iord)%length` | For each order entry after its measurement descriptor has been read and while summing member channel lengths. | `chcal(i)%ord(iord)%length` accumulates the total length of all channels in the region for that order record. |
| `db_mx%ch_reg` | After the file scan completes successfully and just before return. | `db_mx%ch_reg` is updated to the number of channel calibration regions read from the file, making that maximum/actual count available to later routines. |

## File I/O

<!-- facts:io -->


## Lineage

Four source-backed commits were resolved for `ch_read_orders_cal`. The initial commit `df07e3f` introduced the routine with file scanning, region expansion, HRU mapping, and channel-length accumulation. `39fabde` mainly added explicit initialization of local scalars and preserved the same overall logic. `10e5ddc` changed the channel-length accumulation block by commenting out the `if (chcal(i)%ord(iord)%meas%name == sd_ch(ich)%order)` guard and leaving the unconditional sum commented as well. `29e2d36` then made that unconditional channel-length addition active again by uncommenting the `chcal(i)%ord(iord)%length = chcal(i)%ord(iord)%length + sd_ch(ich)%chl` line.

- df07e3f added the routine and its core behavior: reading `ch_sed_budget.sft`, building `chcal`, mapping HRUs, and summing channel lengths.
- 39fabde added default initial values for the local scalars (`titldum`, `header`, `eof`, `ihru`, `imax`, `mcal`, `mreg`, `i`, `nspu`, `isp`, `ielem`, `ii`, `ie`, `ie1`, `ie2`, `iord_mx`, `iord`, `ich_s`) without changing the algorithm.
- 10e5ddc removed the active measurement-name test in the channel-length accumulation block by commenting out the `if`/`end if` guard and the addition line.
- 29e2d36 re-enabled the channel-length accumulation line so each member channel's `sd_ch(ich)%chl` is added unconditionally to `chcal(i)%ord(iord)%length`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ch_read_orders_cal' has no extracted documentation comment.
