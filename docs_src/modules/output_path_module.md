---
kind: module
symbol: output_path_module
title: output_path_module
status: filled
source_hash: 8ff0372bddd53e1a
version_label: SWAT+ 62.0.0
variables:
  out_path: Shared output-path prefix for all output files; set by `init_output_path`, appended
    by `get_output_filename`, and used by `open_output_file` when opening report files.
---

<!-- facts:header -->

Owns the shared output-directory state for SWAT+ file creation. `out_path` stores the configured prefix for generated output files, `init_output_path` normalizes and validates the requested directory and creates it if needed, `get_output_filename` builds a full file path from the shared prefix, and `open_output_file` centralizes opening results files on the resolved path. Startup code and many report/header routines depend on this module so output files land in the configured output directory rather than the working directory.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration-and-helper container rather than a passive constant store. `readcio_read` passes the output-path text from `file.cio` into `init_output_path`, which validates the path, creates the directory if needed, and stores the normalized prefix in `out_path` for later file opens.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:carbon_legacy_module::carbon_legacy_open] | `unit_8348, unit_9000, unit_8349, unit_8358, unit_8359, unit_8382, unit_8383, unit_8386, unit_8387, unit_8384, unit_8385, unit_8360, unit_8363, unit_8367, unit_8368, unit_8372, unit_8373, unit_8374, unit_8375, unit_8376, unit_8377, unit_8378, unit_8379, unit_8380, unit_8381, unit_8366` | `out_path` | Uses `open_output_file` to open carbon-legacy output units on the resolved output path before writing legacy carbon and soil-nutrition output records. |
| [sym:co2_read] | `unit_2222, co2_yr.dat` | `out_path` | Uses `open_output_file` to create `co2.out` in the configured output directory before reading annual CO2 data and expanding it into the simulation series. |
| [sym:header_aquifer] | `unit_2520, unit_9000, unit_2524, unit_2521, unit_2525, unit_2522, unit_2526, unit_2523, unit_2527` | `out_path` | Uses `open_output_file` to open the aquifer header files on the resolved output path before writing daily, monthly, yearly, and average-annual headers. |
| [sym:header_channel] | `unit_2480, unit_9000, unit_2484, unit_2481, unit_2485, unit_2482, unit_2486, unit_2483, unit_2487` | `out_path` | Uses `open_output_file` to open channel output files in the configured output directory before writing the channel header records. |
| [sym:header_const] | `unit_6080, unit_6082, unit_6084, unit_6086, unit_6021, unit_6022, unit_6023, unit_6024, unit_6025, unit_6026, unit_6027, unit_6028, unit_6060, unit_6061, unit_6062, unit_6063, unit_6064, unit_6065, unit_6066, unit_6067, unit_6030, unit_6031, unit_6032, unit_6033, unit_6034, unit_6035, unit_6036, unit_6037, unit_6040, unit_6041, unit_6042, unit_6043, unit_6044, unit_6045, unit_6046, unit_6047, unit_6070, unit_6071, unit_6072, unit_6073, unit_6074, unit_6075, unit_6076, unit_6077, unit_6090, unit_6091, unit_6092, unit_6093, unit_6094, unit_6095, unit_6096, unit_6097` | `out_path` | Uses `open_output_file` to create the constituent output files on the resolved output path so the file locations and record lengths are handled consistently. |
| [sym:header_cs] | `unit_9000, unit_2708, unit_2724, unit_2712, unit_2728, unit_2716, unit_2732, unit_2720, unit_2736, unit_2709, unit_2725, unit_2713, unit_2729, unit_2717, unit_2733, unit_2721, unit_2737, unit_2710, unit_2726, unit_2714, unit_2730, unit_2718, unit_2722, unit_2738, unit_2711, unit_2727, unit_2715, unit_2731, unit_2719, unit_2735, unit_2723, unit_2739, unit_2740, unit_2756, unit_2744, unit_2760, unit_2748, unit_2764, unit_2752, unit_2768, unit_2741, unit_2757, unit_2745, unit_2761, unit_2749, unit_2765, unit_2753, unit_2769, unit_2742, unit_2758, unit_2746, unit_2762, unit_2750, unit_2766, unit_2754, unit_2770, unit_2743, unit_2759, unit_2747, unit_2763, unit_2751, unit_2767, unit_2755, unit_2771` | `out_path` | Uses `open_output_file` to create the hydrology constituent output files on the SWAT+ output path before writing the basin/program and constituent headers. |
| [sym:header_hyd] | `unit_9000, unit_2580, unit_2584, unit_2581, unit_2585, unit_2582, unit_2586, unit_2583, unit_2587, unit_2560, unit_2564, unit_2561, unit_2565, unit_2562, unit_2566, unit_2563, unit_2567, unit_2700, unit_2704, unit_2701, unit_2705, unit_2702, unit_2706, unit_2703, unit_2707` | `out_path` | Uses `open_output_file` for every enabled hydrology output so the files are opened on the resolved destination path before header records and registry entries are written. |
| [sym:header_lu_change] | `unit_3612, unit_9000` | `out_path` | Uses `open_output_file` to open the land-use-change output file at unit 3612 on the configured output path before writing the header text. |
| [sym:header_mgt] | `unit_2612, unit_9000` | `out_path` | Uses `open_output_file` to open the management output file in the configured output directory before writing the basin/program and column header lines. |
| [sym:header_path] | `unit_2790, unit_9000, unit_2794, unit_2791, unit_2795, unit_2792, unit_2796, unit_2793, unit_2797` | `out_path` | Uses `open_output_file` to create the HRU-pathogen output files on the resolved output path before writing header records. |
| [sym:header_pest] | `unit_2800, unit_9000, unit_2804, unit_2801, unit_2805, unit_2802, unit_2806, unit_2803, unit_2807, unit_2808, unit_2812, unit_2809, unit_2813, unit_2810, unit_2814, unit_2811, unit_2815, unit_2816, unit_2820, unit_2817, unit_2821, unit_2818, unit_2822, unit_2819, unit_2823, unit_3000, unit_3004, unit_3001, unit_3005, unit_3002, unit_3006, unit_3003, unit_3007, unit_3008, unit_3012, unit_3009, unit_3013, unit_3010, unit_3014, unit_3011, unit_3015, unit_2832, unit_2836, unit_2833, unit_2837, unit_2834, unit_2838, unit_2835, unit_2839, unit_2848, unit_2852, unit_2849, unit_2853, unit_2850, unit_2854, unit_2851, unit_2855, unit_2864, unit_2868, unit_2865, unit_2869, unit_2866, unit_2870, unit_2867, unit_2871` | `out_path` | Uses `open_output_file` to resolve each relative pesticide output name into a full path before opening the file and writing the pesticide headers. |
| [sym:header_reservoir] | `unit_2540, unit_9000, unit_2544, unit_2541, unit_2545, unit_2542, unit_2546, unit_2543, unit_2547` | `out_path` | Uses `open_output_file` to open reservoir output files on the resolved output path before the reservoir header rows are written. |

## Key Consumers

Most importers are startup or report-header routines. Some are initialization routines that call `init_output_path` to establish the shared directory prefix, while many others are output setup routines that call `open_output_file` so their report files are created in the configured SWAT+ output directory.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:co2_read] | output_path_module | Creates `co2.out` through the shared output-path helper before the CO2 series is read and written to the output file. |
| [sym:header_aquifer] | output_path_module | Opens aquifer output files in the configured output directory, then writes the aquifer header records. |
| [sym:header_channel] | output_path_module | Opens channel output files on the resolved SWAT+ output path before header records are written. |
| [sym:header_const] | output_path_module | Opens the constituent output files consistently on the configured output path before their header blocks are written. |
| [sym:header_cs] | output_path_module | Opens hydrology constituent output files in the model's output directory and writes their header records. |
| [sym:header_hyd] | output_path_module | Opens hydrology-related output files on the resolved output path and then writes standard header and registry records. |
| [sym:header_lu_change] | output_path_module | Opens the land-use-change report file at unit 3612 in the configured output directory before writing its header. |
| [sym:header_mgt] | output_path_module | Opens the management output file in the configured output directory, then writes the basin/program header lines. |
| [sym:header_path] | output_path_module | Opens HRU-pathogen output files on the resolved output path before writing file headers and file registry entries. |
| [sym:header_pest] | output_path_module | Opens pesticide output files in the configured output directory before the pesticide header rows are written. |
| [sym:header_reservoir] | output_path_module | Opens reservoir output files on the resolved output path before reservoir headers are written. |
| [sym:header_salt] | output_path_module | Opens salt output files on the resolved path before the salt file header rows are written. |
| [sym:header_sd_channel] | output_path_module | Opens SWAT-DEG channel output files on the resolved output path before channel header records are written. |
| [sym:header_snutc] | output_path_module | Opens the soil-carbon output files and writes the basin/program banner line for each file. |
| [sym:header_water_allocation] | output_path_module | Opens water-allocation report files on the configured output path before header rows are written. |
| [sym:header_wetland] | output_path_module | Opens wetland/reservoir output files on the resolved output path before their header rows are written. |
| [sym:header_write] | output_path_module | Provides the path-resolution helper used to open the many basin and calibration output files that `header_write` seeds during initialization. |
| [sym:header_yield] | output_path_module | Opens yield output files with the shared output-path helper before writing yield header information. |
| [sym:proc_bsn] | output_path_module | Opens basin-level output units through the shared output-path helper during basin initialization. |
| [sym:proc_hru] | output_path_module | Opens HRU output or diagnostic files through the shared output-path helper during HRU initialization. |
| [sym:readcio_read] | output_path_module | Parses the output-path text from `file.cio` and initializes the shared `out_path` state used by later output-file construction. |
| [sym:carbon_legacy_module::carbon_legacy_open] | output_path_module | Opens legacy carbon and soil-nutrition output units through the shared output-path helper before those legacy records are written. |
| [sym:output_landscape_init] | output_path_module | Uses the shared output-path state while setting up landscape-related output units during initialization. |

## Lineage

Source-backed lineage shows one resolved commit for this module: `9299ca5` (2025-12-04) added `output_path_module.f90` as a new file to allow specifying an output directory. The diff introduces the module with shared `out_path` state plus `init_output_path`, `get_output_filename`, and `open_output_file`; no later source changes were resolved in the provided lineage evidence.

- {'commit': '9299ca5', 'summary': 'Added a new output-path module that stores a shared output directory prefix, validates and creates the directory when initialized, and provides helper routines to build full filenames and open output files on that path.', 'impact': 'This change enabled SWAT+ output files to be routed to a user-specified directory instead of relying on the working directory.'}

## Review Notes

- Module `output_path_module` has no extracted module-level documentation comment beyond the variable and procedure comments in the source.
- No derived types were extracted for this module.
- The reader list is representative of the importers table and mirrors the parser output; use `all_importers` for the full importer appendix.
- lineage evidence resolved only the initial addition commit for this module.
