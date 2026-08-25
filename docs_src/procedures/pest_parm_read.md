---
kind: procedure
symbol: pest_parm_read
title: pest_parm_read
status: filled
source_hash: 9c423b4f66138eda
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary string used to read and discard title or separator lines from `pesticide.pes`
    during the count pass and the data pass.
  header: Temporary string used to read and discard the header line from `pesticide.pes` before
    the routine counts or loads pesticide records.
  eof: I/O status flag used with `iostat` to detect end-of-file or read failure while scanning
    and loading `pesticide.pes`.
  imax: Counts how many pesticide records are present in the file so the routine can allocate
    `pestdb` and `pestcp` with the correct bounds.
  i_exist: Logical flag set by `inquire` to decide whether the configured pesticide file exists
    before attempting to read it.
  ip: Loop counter for stepping through each pesticide record while reading `pestdb(ip)` and
    computing `pestcp(ip)`.
uses:
  basin_module: The routine uses `use basin_module`, but the context packet does not resolve
    any concrete basin symbols here, so its specific state dependency cannot be identified
    from the available evidence.
  input_file_module: '`input_file_module` provides `in_parmdb%pest`, the configured path to
    the pesticide database file. That value controls which file is checked, opened, and read.'
  maximum_data_module: '`maximum_data_module` provides `db_mx%pestparm`, the shared counter
    for how many pesticide parameter records were found. Other routines can use that count
    to size or validate pesticide-related data.'
  pesticide_data_module: '`pesticide_data_module` owns both the input database array `pestdb`
    and the calculated-parameter array `pestcp`. This routine fills the former from file data
    and derives the latter from each pesticide''s half-life fields.'
  utils: The `utils` module matters because `exp_w` safely evaluates the exponential used
    to convert half-life values into decay factors, guarding against underflow when the exponent
    is very negative.
---

<!-- facts:header -->

Reads the pesticide parameter database from `pesticide.pes` and fills pesticide lookup tables. It also converts the stored half-lives into decay factors used later by pesticide transport and fate calculations.

## Bottom Line

`pest_parm_read` reads the pesticide parameter database named by `in_parmdb%pest`, counts the records in that file, allocates `pestdb` and `pestcp` to the needed size, and then loads each pesticide definition into `pestdb(ip)`. If the configured file is missing or set to `"null"`, it still allocates one-element placeholder arrays so later code can rely on the shared pesticide tables existing.

After loading each pesticide record, the routine converts the four half-life fields in `pestdb` into decay multipliers in `pestcp`: foliage, soil, aquatic, and benthic. It also publishes the number of pesticide records through `db_mx%pestparm`, which lets the rest of the model know how many pesticide entries were available from `pesticide.pes`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization, after `proc_db` starts loading shared parameter tables and before later pesticide fate calculations need the database. Its outputs feed pesticide behavior throughout the model because they provide both the raw pesticide properties and the derived decay coefficients.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the pesticide database should be read | The routine checks `in_parmdb%pest` with `inquire` and also tests for the sentinel string `"null"`. If the file is absent or disabled, it skips file processing and allocates placeholder arrays `pestdb(0:0)` and `pestcp(0:0)`. |
| 2. Open the file and count data records | When the file is available, the routine opens unit 106 on `in_parmdb%pest`, reads the title and header records, then loops through the remaining lines to count entries by incrementing `imax` until end-of-file. |
| 3. Allocate storage for raw and derived pesticide data | After the first pass, the routine allocates `pestdb(0:imax)` and `pestcp(0:imax)` so the raw database records and calculated pesticide coefficients have room for every entry. |
| 4. Rewind and restart reading from the top | The routine rewinds unit 106, rereads the title and header lines, and positions the file at the first pesticide record for the second pass. |
| 5. Read each pesticide record | For each index from 1 to `imax`, the routine reads one structured record into `pestdb(ip)` and stops early if a read error or end-of-file occurs. |
| 6. Derive foliar decay from foliar half-life | If `pestdb(ip)%foliar_hlife` is positive, the routine computes `pestcp(ip)%decay_f` as `exp_w(-.693 / pestdb(ip)%foliar_hlife)`; otherwise it stores zero. |
| 7. Derive soil decay from soil half-life | If `pestdb(ip)%soil_hlife` is positive, the routine computes `pestcp(ip)%decay_s` with the same half-life-to-rate conversion; otherwise it stores zero. |
| 8. Derive aquatic decay from aquatic half-life | If `pestdb(ip)%aq_hlife` is positive, the routine computes `pestcp(ip)%decay_a` as `exp_w(-.693 / pestdb(ip)%aq_hlife)`; otherwise it stores zero. |
| 9. Derive benthic decay from benthic half-life | If `pestdb(ip)%ben_hlife` is positive, the routine computes `pestcp(ip)%decay_b` from the benthic half-life; otherwise it stores zero. |
| 10. Publish the record count and close the file | After the loop finishes, the routine leaves the read block, copies `imax` into `db_mx%pestparm`, closes unit 106, and returns. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module does not have a resolved candidate reference in the extracted packet.` |  |
| [sym:input_file_module] | `in_parmdb` | `in_parmdb%pest` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%pestparm` |
| [sym:pesticide_data_module] | `pestdb, pestcp` | `pestdb(ip)%foliar_hlife, pestcp(ip)%decay_f, pestdb(ip)%soil_hlife, pestcp(ip)%decay_s, pestdb(ip)%aq_hlife, pestcp(ip)%decay_a, pestdb(ip)%ben_hlife, pestcp(ip)%decay_b` |
| [sym:utils] | `exp_w` | `exp_w` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pestcp(ip)%decay_f` | When `pestdb(ip)%foliar_hlife > 0.` during the record-processing loop; otherwise it is set to 0. | `pestcp(ip)%decay_f` is refreshed from the foliar half-life so later pesticide calculations can use a decay multiplier instead of recomputing the rate each time. |
| `pestcp(ip)%decay_s` | When `pestdb(ip)%soil_hlife > 0.` during the record-processing loop; otherwise it is set to 0. | `pestcp(ip)%decay_s` stores the soil decay multiplier derived from the soil half-life for later use by pesticide fate logic. |
| `pestcp(ip)%decay_a` | When `pestdb(ip)%aq_hlife > 0.` during the record-processing loop; otherwise it is set to 0. | `pestcp(ip)%decay_a` stores the aquatic decay multiplier derived from the aquatic half-life for later use by pesticide fate logic. |
| `pestcp(ip)%decay_b` | When `pestdb(ip)%ben_hlife > 0.` during the record-processing loop; otherwise it is set to 0. | `pestcp(ip)%decay_b` stores the benthic decay multiplier derived from the benthic half-life for later use by pesticide fate logic. |
| `db_mx%pestparm` | After the file pass completes, using the final `imax` record count derived from `pesticide.pes`. | `db_mx%pestparm` is updated to report how many pesticide records were found, so other routines can size loops or validate database coverage. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:3.2.2 | Soil pesticide half-life to rate-constant relationship | $t_{1/2,s}=\frac{0.693}{k_{p,soil}}$ | Verified against SWAT+ 62.0.0 (pest_parm_read.f90:64). decay_s = exp_w(-.693/soil_hlife)` — soil half-life |
| 3:3.2.4 | Foliar pesticide half-life to rate-constant relationship | $t_{1/2,f}=\frac{0.693}{k_{p,foliar}}$ | Verified against SWAT+ 62.0.0 (pest_parm_read.f90:59). decay_f = exp_w(-.693/foliar_hlife)` — foliar half-life |
| 7:4.1.7 | Aqueous first-order decay constant | $k_{p,aq}=\frac{0.693}{t_{1/2,aq}}$ | Verified against SWAT+ 62.0.0 (pest_parm_read.f90:70). decay_a = exp_w(-.693/aq_hlife)` — aqueous k=0.693/hlife |
| 7:4.2.8 | Benthic pesticide degradation | $pst_{deg,sed} = k_{p,sed} *pst_{rchsed}$ | Verified against SWAT+ 62.0.0 (pest_parm_read.f90:75). |
| 7:4.2.9 | Benthic first-order decay constant | $k_{p,sed} =\frac{0.693}{t_{1/2,sed}}$ | Verified against SWAT+ 62.0.0 (pest_parm_read.f90:75). decay_b = exp_w(-.693/ben_hlife)` — benthic/sediment half-life |

## Lineage

Three source-backed commits were resolved for `pest_parm_read`. `df07e3f` added the routine with file existence checks, record counting, allocation, reading, and decay-factor derivation. `94b6dec` shows the same initial implementation as the imported upstream source. `39fabde` initialized the local variables `titldum`, `header`, `eof`, `imax`, and `ip` to explicit default values. `9b7f630` replaced the direct `Exp` calls with `exp_w` from `utils` for safer underflow handling and added `use utils` to the procedure.

- df07e3f added the full pesticide parameter reader: it inquires on `in_parmdb%pest`, allocates placeholder arrays when the file is missing, scans `pesticide.pes` to count records, allocates `pestdb` and `pestcp`, rereads each entry, computes the four decay multipliers from half-lives, and stores the count in `db_mx%pestparm`.
- 39fabde changed only local initialization in this procedure by giving `titldum`, `header`, `eof`, `imax`, and `ip` explicit default values in their declarations.
- 9b7f630 replaced the intrinsic exponential calls with `utils::exp_w` for all four decay calculations and added `use utils` so underflow-safe exponentials are used.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'pest_parm_read' has no extracted documentation comment.
- basin_module is imported but no concrete symbols from it were resolved in the packet.
- The file-reading loop uses `do`/`exit` around `open (106,file=in_parmdb%pest)`; this appears to be a single-pass guard structure rather than repeated reopening for multiple files.
- The source initializes `eof` and `imax` both in declarations and again on lines 18-19; the declaration-time defaults were added later by commit 39fabde.
- algorithm_steps revised: merged the placeholder allocation and record-counting narrative into a single scan/allocate flow, and expanded the decay derivation steps to match the source-line evidence.
