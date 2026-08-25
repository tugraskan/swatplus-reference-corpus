---
kind: procedure
symbol: ch_initial
title: ch_initial
status: filled
source_hash: d33425313fe4aed6
version_label: SWAT+ 62.0.0
args:
  idat: Reach index into `channel_module::ch`; the routine writes the initialized bank and
    bed composition for this specific channel reach.
  irch: Index of the channel reach being initialized from `proc_cha`; it is used to select
    `ch(irch)` for output state updates.
locals:
  ised: Local sediment-data index. It is set from `ch_dat(idat)%sed` and then used to pick
    the corresponding `ch_sed(ised)` record for particle-size and critical-shear calculations.
  bnksize: Bank median particle size in millimeters, computed from `ch_sed(ised)%bnk_d50 /
    1000.` and used to choose the bank texture class fractions.
  bedsize: Bed median particle size in millimeters, computed from `ch_sed(ised)%bed_d50 /
    1000.` and used to choose the bed texture class fractions.
  sc: Temporary shear-stress predictor. It is reset to zero, then set from the sum of silt
    and clay percentages when estimating critical shear stress.
uses:
  channel_data_module: '`channel_data_module` provides the channel-sediment lookup tables
    that connect the reach’s property record to the sediment parameter set (`ch_dat(idat)%sed`),
    and it stores the sediment inputs (`ch_sed`) that supply particle size, cover factors,
    and critical-shear fields used by this initialization.'
  channel_module: '`channel_module` holds the per-reach channel state that this routine populates.
    The bank and bed fraction members in `ch(irch)` are the outputs that later channel erosion
    and transport calculations read.'
---

<!-- facts:header -->

Initializes each channel reach’s bank and bed sediment texture fractions and default critical shear stresses from channel sediment property inputs.

## Bottom Line

`ch_initial` uses the sediment-property record linked to a channel reach to assign bank and bed texture fractions in `ch(irch)` from the median particle sizes in `ch_sed(ised)`. It also estimates critical shear stress for bank and bed if those values have not already been provided, using the reach’s silt-plus-clay percentages and the cover factors stored in the sediment data.

This routine matters because it seeds channel erosion and resistance parameters before later channel processes run. Downstream routing and erosion behavior depend on the initialized `bnk_*`, `bed_*`, `tc_bnk`, and `tc_bed` values.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during channel setup in `proc_cha`, after the reach property index `idat` has been taken from `ob(i)%props` and before overbank and landscape-link parameters are read. Its initialized texture fractions and critical shear stresses are then available to later channel sediment, erosion, and routing behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. derive sediment index | Read the sediment-property index for this reach from `ch_dat(idat)%sed`, then convert bank D50 from micrometers to millimeters as `bnksize`. |
| 2. classify bank as clayey | If `bnksize <= 0.005`, assign the bank fractions to a clayey mix: mostly clay, with lesser silt, sand, and gravel. |
| 3. classify bank as silty | If `0.005 < bnksize <= 0.05`, assign the bank fractions to a silty mix with silt dominant. |
| 4. classify bank as sandy | If `0.05 < bnksize <= 2.`, assign the bank fractions to a sandy mix with sand dominant. |
| 5. classify bank as gravelly | If `bnksize > 2.`, assign the bank fractions to a gravelly mix with gravel dominant. |
| 6. derive bed size | Convert bed D50 from micrometers to millimeters as `bedsize` from the same sediment record. |
| 7. classify bed as clayey | If `bedsize <= 0.005`, assign the bed fractions to a clayey mix. |
| 8. classify bed as silty | If `0.005 < bedsize <= 0.05`, assign the bed fractions to a silty mix with silt dominant. |
| 9. classify bed as sandy | If `0.05 < bedsize <= 2.`, assign the bed fractions to a sandy mix with sand dominant. |
| 10. classify bed as gravelly | If `bedsize > 2.`, assign the bed fractions to a gravelly mix with gravel dominant. |
| 11. initialize shear-stress helper | Reset the temporary predictor `SC` to zero before checking whether critical shear stress needs to be estimated. |
| 12. estimate bank critical shear stress if missing | When `ch_sed(ised)%tc_bnk <= 1.e-6`, compute `SC` from the bank silt-plus-clay percentage, then calculate `ch_sed(ised)%tc_bnk` with the Julian and Torres-style polynomial multiplied by `cov1`. |
| 13. estimate bed critical shear stress if missing | When `ch_sed(ised)%tc_bed <= 1.e-6`, compute `SC` from the bed silt-plus-clay percentage, then calculate `ch_sed(ised)%tc_bed` with the same polynomial multiplied by `cov2`. |
| 14. return | Finish the initialization and return the updated reach and sediment states to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:channel_data_module] | `ch_dat, ch_sed` | `ch_dat(idat)%sed, ch_sed(ised)%bnk_d50, ch_sed(ised)%bed_d50, ch_sed(ised)%tc_bnk, ch_sed(ised)%cov1, ch_sed(ised)%tc_bed, ch_sed(ised)%cov2` |
| [sym:channel_module] | `ch` | `ch(irch)%bnk_cla, ch(irch)%bnk_sil, ch(irch)%bnk_san, ch(irch)%bnk_gra, ch(irch)%bed_cla, ch(irch)%bed_sil, ch(irch)%bed_san, ch(irch)%bed_gra` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ch(irch)%bnk_cla` | When `bnksize <= 0.005` from the selected sediment record. | Sets the channel reach’s bank clay fraction to the clayey default used by this initializer, as part of choosing one texture class for the bank. |
| `ch(irch)%bnk_sil` | When `0.005 < bnksize <= 0.05` from the selected sediment record. | Sets the channel reach’s bank silt fraction to the silty default used by this initializer, as part of choosing one texture class for the bank. |
| `ch(irch)%bnk_san` | When `0.05 < bnksize <= 2.` from the selected sediment record. | Sets the channel reach’s bank sand fraction to the sandy default used by this initializer, as part of choosing one texture class for the bank. |
| `ch(irch)%bnk_gra` | When `bnksize > 2.` from the selected sediment record. | Sets the channel reach’s bank gravel fraction to the gravelly default used by this initializer, as part of choosing one texture class for the bank. |
| `ch(irch)%bed_cla` | When `bedsize <= 0.005` from the selected sediment record. | Sets the channel reach’s bed clay fraction to the clayey default used by this initializer, establishing the bed texture mix for this reach. |
| `ch(irch)%bed_sil` | When `0.005 < bedsize <= 0.05` from the selected sediment record. | Sets the channel reach’s bed silt fraction to the silty default used by this initializer, establishing the bed texture mix for this reach. |
| `ch(irch)%bed_san` | When `0.05 < bedsize <= 2.` from the selected sediment record. | Sets the channel reach’s bed sand fraction to the sandy default used by this initializer, establishing the bed texture mix for this reach. |
| `ch(irch)%bed_gra` | When `bedsize > 2.` from the selected sediment record. | Sets the channel reach’s bed gravel fraction to the gravelly default used by this initializer, establishing the bed texture mix for this reach. |
| `ch_sed(ised)%tc_bnk` | When `ch_sed(ised)%tc_bnk <= 1.e-6` after bank texture fractions have been assigned. | Writes an estimated bank critical shear stress into the sediment record only if no bank value was already supplied, using the bank silt-plus-clay content and cover factor `cov1`. |
| `ch_sed(ised)%tc_bed` | When `ch_sed(ised)%tc_bed <= 1.e-6` after bed texture fractions have been assigned. | Writes an estimated bed critical shear stress into the sediment record only if no bed value was already supplied, using the bed silt-plus-clay content and cover factor `cov2`. |

## File I/O

<!-- facts:io -->


## Lineage

`ch_initial` was introduced in df07e3f as a new initialization subroutine. The later 39fabde commit only changed local declarations by giving `ised`, `bnksize`, `bedsize`, and `sc` explicit zero initializers. The f1e61a3 commit kept the logic unchanged and only converted the indentation from tabs to spaces in the bank/bed classification blocks.

- df07e3f added the full bank/bed texture initialization and conditional critical-shear estimation logic.
- 39fabde changed only variable initialization style by assigning default zero values to the local counters and reals; behavior stayed the same.
- f1e61a3 made formatting-only indentation changes, with no algorithmic effect.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ch_initial' has no extracted documentation comment.
