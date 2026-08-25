---
kind: io
source_symbols:
- exco_read_om
title: '`exco_om.exc`'
status: filled
source_hash: fb7b8469d533508b
version_label: SWAT+ 62.0.0
---

**Primary target:** `exco(:)` (array of `type hyd_output`)  
**Read by:** [sym:exco_read_om]

## Bottom Line

The file `exco_om.exc` is an export coefficient input file that configures export coefficient data for hydrological output variables in the model.

It is optional and only read if the file exists and is not named "null".

The primary reader that loads this file is the `exco_read_om` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides the `type hyd_output` and the `exco` array where the export coefficient data is stored. |
| [sym:input_file_module] | Provides the `in_exco` variable which contains the filename `om` for the export coefficient file. |
| [sym:organic_mineral_mass_module] | Imported but no direct usage visible in `exco_read_om`. |
| [sym:constituent_mass_module] | Imported but no direct usage visible in `exco_read_om`. |
| [sym:maximum_data_module] | Provides `db_mx%exco_om` which stores the number of export coefficient records read from the file. |
| [sym:exco_module] | Imported but no direct usage visible in `exco_read_om`. |

## File Variables

The file consists of multiple records each representing export coefficient data for hydrological outputs. Each record is read into an element of the `exco` array of type `hyd_output`. The file contains a header section followed by lines with a name and corresponding hydrological output data fields.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `exco%flo` | real | m^3 | volume of water |
| 3 |  | `exco%sed` | real | metric tons | sediment |
| 4 |  | `exco%orgn` | real | kg N | organic N |
| 5 |  | `exco%sedp` | real | kg P | organic P |
| 6 |  | `exco%no3` | real | kg N | NO3-N |
| 7 |  | `exco%solp` | real | kg P | mineral (soluble P) |
| 8 |  | `exco%chla` | real | kg | chlorophyll-a |
| 9 |  | `exco%nh3` | real | kg N | NH3 |
| 10 |  | `exco%no2` | real | kg N | NO2 |
| 11 |  | `exco%cbod` | real | kg | carbonaceous biological oxygen demand |
| 12 |  | `exco%dox` | real | kg | dissolved oxygen |
| 13 |  | `exco%san` | real | tons | detached sand |
| 14 |  | `exco%sil` | real | tons | detached silt |
| 15 |  | `exco%cla` | real | tons | detached clay |
| 16 |  | `exco%sag` | real | tons | detached small ag |
| 17 |  | `exco%lag` | real | tons | detached large ag |
| 18 |  | `exco%grv` | real | tons | gravel |
| 19 |  | `exco%temp` | real | deg c | temperature |

## Sample

```text
Example record line format (after headers):
NameField  <flo> <sed> <orgn> <sedp> <no3> <solp> <chla> <nh3> <no2> <cbod> <dox> <san> <sil> <cla> <sag> <lag> <grv> <temp>
```

## Read Pattern

```fortran
open (107,file=in_exco%om)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) titldum
rewind (107)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) exco_om_name(ii), exco(ii)
close (107)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_exco%om)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) exco_om_name(ii), exco(ii)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:exco_read_om] | open, read, rewind, close | Reads the export coefficient file `exco_om.exc` if it exists and is not "null". It counts the number of records, allocates arrays, rewinds the file, reads header lines, then reads each record's name and hydrological output data into the arrays `exco_om_name` and `exco` respectively. |

## Review Notes

- The file `exco_om.exc` is optional and only read if it exists and is not named "null".
- The reader `exco_read_om` reads header lines before reading the data records.
- The data records contain a name and a `hyd_output` record per line.
- The commented-out code at the end of `exco_read_om` suggests intended linking of `exco` data to hydrograph objects, but this is not active in the current source.
- No sample data lines are present in the source; the sample read format is inferred from the read statement and type structure.
