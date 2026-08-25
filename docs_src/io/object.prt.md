---
kind: io
title: '`object.prt`'
status: filled
version_label: SWAT+ 62.0.0
---

**Primary target:** ob_out(:) / object_output

## Bottom Line

`object.prt` is an optional output-control file. It does not define physical model parameters. It tells SWAT+ which object-level output files to create for selected HRUs, HRU-LTE objects, routing units, reservoirs, channels, export-coefficient objects, delivery-ratio objects, outlets, or SWAT-DEG channels.

When the file exists, `object_read_output` loads each requested output row into `ob_out(:)`, resolves the requested object into the global object index, maps the requested output category into `hydno`, opens the requested output file, and writes the matching header. Later, `obj_output` uses the same `ob_out(:)` records to write data during the simulation.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Supplies `in_sim%object_prt`, whose default value is `object.prt`. |
| [sym:hydrograph_module] | Supplies `mobj_out`, `ob_out(:)`, `object_output`, `sp_ob1`, and output header objects such as `hyd_hdr_time`, `hyd_hdr`, `sol_hdr`, `plt_hdr`, and `fp_hdr`. |
| [sym:maximum_data_module] | Supplies `db_mx%object_prt`, the stored count of object-output requests. |

## File Variables

This is the input schema and the file-to-Fortran mapping. Local scratch variables are not broken out separately because the useful distinction on an IO page is whether the value comes from the file or is derived after reading.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| all | `title` | `titldum` |  |  | Title/comment line. Read and discarded. |
| all | `header` | `header` |  |  | Header line. Read and discarded. |
| 1 | `ID` | `i, ii, k` |  |  | Row id, first-pass count key, and second-pass storage index. |
| 2 | `OBJ_TYP` | `ob_out(ii)%obtyp` |  |  | Object type code used to select a `sp_ob1` offset. |
| 3 | `OBJ_TYP_NO` | `ob_out(ii)%obtypno` |  |  | Object number within the selected object type. |
| 4 | `HYD_TYP` | `ob_out(ii)%hydtyp` |  |  | Output category code mapped to `hydno`. |
| 5 | `FILENAME` | `ob_out(ii)%filename` |  |  | Output file opened on unit `unitno + i`. |

## Sample

```text
object_prt
ID  OBJ_TYP  OBJ_TYP_NO  HYD_TYP     FILENAME
1   hru      1           tot         hru_1.out
2   ru       1           tot         ru_1.out
3   cha      1           tot         channel_1.out
4   res      1           tot         reservoir_1.out
5   out      1           tot         outlet_1.out
```

## Read Pattern

```fortran
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) ii
backspace (107)
read (107,*,iostat=eof) k, ob_out(ii)%obtyp, &
  ob_out(ii)%obtypno, ob_out(ii)%hydtyp, ob_out(ii)%filename
```

## Review Notes

- `object.prt` is an output-selection file, not a physical parameter file. Its main effect is to create output files and define which object/hydrograph data are written later.
- The reader stores full rows into `ob_out(ii)`, but the subsequent `select case` blocks use `ob_out(i)`. This is equivalent only when row ids are sequential from `1` through `mobj_out`; sparse ids could leave the resolved `objno` and `hydno` on the wrong array element.
- `solnut_ly` and `solnut_pr` are mapped to `hydno` 7 and 8, and `obj_output` writes them, but `object_read_output` does not currently write headers for cases 7 or 8.
- `obj_output` has branches for `hydno` 11 and 12, but `object_read_output` does not map any `hydtyp` value to those codes.
- `object_output%name` exists in the type but is not read from `object.prt` by the current reader.
- Manual-style descriptions are included beside source-backed meanings so inferred wording does not get mistaken for Fortran comments.
