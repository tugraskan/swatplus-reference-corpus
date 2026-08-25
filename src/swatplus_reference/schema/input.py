"""Emit a version-tagged JSON schema of SWAT+ input database file layouts.

This generator reads the pinned SWAT+ Fortran source tree and, for each
name-keyed input database file, records the column layout its reader expects:
the ordered list of columns, their Fortran name and type, and whether each is
numeric. The artifact is consumed by the
``tugraskan/SWATPLUS-Authoritative-Reference-Database`` repo to validate
submitted data rows (wrong column count, text in a numeric field, a header row
that no longer matches the file).

Two SWAT+ read patterns are handled (see :mod:`swatplus_reference.parser.schema_fortran`
which already joins ``&`` continuation lines before we ever see a statement):

* **derived type** — ``read (107,*) snodb(isno)`` reads a whole derived type.
  We resolve the variable to its declaration, then to the ``type`` definition,
  and flatten its components (recursively expanding any nested derived-type
  components, exactly as Fortran list-directed I/O does).
* **field list** — ``read (107,*) manure_om(it)%name, manure_om(it)%frac_water,
  ...`` names components explicitly. We resolve each component against its type.

Decision tables (``*.dtl``) are a different shape entirely -- a header record
plus two nested, variable-length blocks of rows, each row itself followed by
a variable-length tail -- and get their own resolution path
(``build_decision_tables``) and their own ``decision_tables`` payload section,
including the closed vocabularies (``cond%var``, ``act%typ``) a row's columns
must draw from, read from the source's own ``select case`` dispatch.

The source is authoritative for arity, order, and types. The committed text
file's header row (the display names) is deliberately *not* guessed here — the
consumer reconciles the Fortran names we emit against its own header row.

Where a database file's reader cannot be located, or its filename expression
cannot be resolved, the file is reported in ``unresolved`` rather than guessed.
A wrong schema is worse than a missing one.

The schema payload is deterministic: same source tree in, byte-identical JSON
out. Keys are sorted and no timestamps appear inside per-file entries. The only
non-deterministic field, top-level ``generated_utc``, can be suppressed with
``--no-timestamp`` for reproducible builds.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json
import re

from ..parser.schema_fortran import STRING_LITERAL_RE, parse_args, split_top_level_commas
from ..parser.schema_model import (
    DerivedTypeDoc,
    IOOperation,
    ProcedureDoc,
    ProjectIndex,
    SelectCaseDoc,
    VariableRef,
)


SOURCE_REPOSITORY = "swat-model/swatplus"

# The name-keyed database files the consumer validates. Restricting the artifact
# to a curated set keeps it deterministic and focused, and lets us honestly
# report which files did not resolve. To cover a newly added upstream database
# file, add its committed filename here and regenerate.
#
# Coverage note (2026-07): the resolver can see well beyond this tuple --
# 179 filenames resolve against the pinned 62.0.0 source with no filter at
# all. The block below adds every file that is *safe* to add mechanically:
# exactly one `open` block, exactly one data read in that block, and no
# implied-do (variable-length trailing group) anywhere the field parser
# can't bind to a value already present in the record (a `record_layout`
# repeat group -- see `RepeatGroup` -- when it can; see below). Deliberately
# NOT included, despite resolving:
#   - Decision tables (`*.dtl`) -- nested, variable-length, a different shape
#     entirely (a header record, then two blocks of rows each with their own
#     variable-length tail): not a `ReadSchema`/`RepeatGroup` at all. Handled
#     by a separate mechanism instead -- see `DECISION_TABLE_FILES` and
#     `build_decision_tables` below, and the `decision_tables` payload
#     section, not this `files` one.
#   - `pest_metabolite.pes` -- a genuinely two-shape file, like a decision
#     table: a 2-field parent header line (name, count) followed by a
#     variable number of 5-field daughter records. The resolver only sees
#     the daughter shape (its one real "data read"); the parent/count
#     structure that makes the file variable-length isn't a data read at
#     all under this model, so nothing flags it as unsafe by field count.
#   - `cs_aqu.ini`, `cs_channel.ini`, `salt_channel.ini`,
#     `pest_water.ini`, and `path_water.ini` now resolve through the
#     additive `runtime_arity` payload, where their runtime-width arrays
#     are tied to count sections from `constituents.cs`.
#   - Externally-governed repeat counts: `cell_sol.gw`, `minerals.gw`,
#     `ponds.gw`, `tvheads.gw`,
#     `gwflow_canal.con`. Each has an implied-do bounded by something
#     outside the record itself -- `grid_ncol`, `time%nbyr`, or an arithmetic
#     expression (`obj_tot*3`) -- so `_find_count_field` correctly can't bind
#     it to a column already read. `res_conds.dat`, `tile.gw` are
#     the same, one level deeper (the count governs a *nested* repeat).
#     (`calibration.cal`'s main record was this case too -- now resolved, and
#     the file is fully covered, in `multi_record`; see the note below.)
# `chan-surf.lin` was this "peek read count" case and is now RESOLVED and
# added: the repeat count comes from an earlier peek read
# (`read ..., nspu` / backspace / re-read with the implied-do tail) under a
# throwaway local name, not one of the record's own fields. Because the peek
# and the full read scan the same physical line, the peek's last token sits in
# the column the full record's last fixed field occupies, so
# `_peek_bound_count_field` binds the count there (`nspu` -> `obj_tot`).
# Verified safe and added in this pass: `weather-sta.cli`, `rout_unit.rtu`,
# `outside_rcv.wal`, and `carbon.bsn` all checked out against the pinned
# source (the fields the schema reports match the actual derived-type
# components read, field for field) -- their earlier "needs review" flag
# was an artifact of comparing against LLM-authored overlay docs, which
# turned out to be wrong themselves for these four, not the schema.
#
# `recall_db.rec` was held back for a real bug: its record's last 6 columns
# are 6 sibling components of the *same* type (`constituent_file_data`:
# name/units/tstep, one per constituent category), so the flattened field
# names collided -- "name", "units", "tstep" each appeared 6 times with
# nothing to tell org_min's name from pest's. Fixed in `read_to_schema`:
# when a %chain's sibling flattening produces a name collision anywhere in
# the read, every colliding chain's fields are prefixed with that chain's
# own component name ("org_min.name", "pest.name", ...). Unambiguous reads
# (the common case, including every other file above) are untouched -- the
# prefix only fires when a real collision is detected in that read.
# (`rout_unit.def`, once excluded for the same variable-length-tail reason as
# the *.con/*.def family above, now resolves via `record_layout`.)
#
# `cells.gw` -- read as raw text and hand-parsed with `split_line`, not via a
# list-directed record -- resolves too, via a different mechanism entirely:
# `resolve_positional_extraction` collects the file's `read(fields(N),*)
# var` calls (one column per statement, against a character array split out
# of each row) into one ordered schema, the same way `record_layout` collects
# a list-directed record's fields, plus any column set by a plain assignment
# rather than a read (`cell_name(i) = trim(fields(2))`, needed for `cells.gw`
# itself). Declines -- rather than publish a wrong prefix -- when a column
# index is computed rather than literal (`fields(2+j)`, a data-dependent
# repeat group nested inside the hand-parse: `cellcon.gw`, `sw_group.gw`).
# When two reads claim the same column with different targets, that used to
# be an automatic decline too (a keyed/tagged record, where a column's
# meaning depends on an earlier column's value) -- `outputs.gw`'s
# `head_output_time`/`observation_cell`/`detail_debug_cell` rows are exactly
# this. Now resolved instead of declined: when every conflicting read sits in
# its own `case ('literal')` branch of a `select case` on another column of
# the same record, and the literals are covered by that select's own captured
# vocabulary (`ProcedureDoc.select_cases`), the column is emitted as a tagged
# column (`tag_field`/`variants` on the entry, see `ReadSchema`) rather than
# guessed at or dropped -- see `_resolve_tagged_positional_column`. Also
# added alongside `cells.gw`: `zones.gw` and
# `chancell.gw`, the same positional shape (`cells.gw` resolves fully, all
# 23 columns -- its optional trailing columns use full `if (...) then` /
# `endif` blocks, not the single-line form below). A separate, real,
# uncaptured gap: `if (cond) read(...)` on one line is invisible to
# I/O-operation detection entirely (it requires the line to *start* with the
# keyword) -- costs `chancell.gw` its last two columns (`dep_zone`, `obs`);
# see PositionalExtractionTests for specifics.
TARGET_FILES: tuple[str, ...] = (
    "cal_parms.cal",
    "plants.plt",
    "aqu_reg.def",
    "print.prt",
    "fertilizer.frt",
    "tillage.til",
    "pesticide.pes",
    "pathogens.pth",
    "urban.urb",
    "septic.sep",
    "snow.sno",
    "transplant.plt",
    "manure_db.frt",
    "manure_om.frt",
    "harv.ops",
    "graze.ops",
    "water_balance.sft",
    "irr.ops",
    "chem_app.ops",
    "fire.ops",
    "sweep.ops",
    "puddle.ops",
    "tiledrain.str",
    "septic.str",
    "filterstrip.str",
    "grassedww.str",
    "bmpuser.str",
    "soil_plant.ini",
    "cntable.lum",
    "cons_practice.lum",
    "ovn_table.lum",
    # -- added 2026-07: mechanically safe widening beyond the original 28 --
    "aqu_catunit.ele",
    "aquifer.aqu",
    "ch_sed_parms.sft",
    "channel-lte.cha",
    "channel.cha",
    "codes.bsn",
    "codes.sft",
    "delratio.del",
    "dr_om.del",
    "element.ccu",
    "exco.exc",
    "exco_om.exc",
    "fertilizer.frt_cs",
    "field.fld",
    "hru-data.hru",
    "hru-lte.hru",
    "hyd-sed-lte.cha",
    "hydrology.cha",
    "hydrology.hyd",
    "hydrology.res",
    "hydrology.wet",
    "initial.aqu",
    "initial.aqu_cs",
    "initial.cha",
    "initial.cha_cs",
    "initial.res",
    "landuse.lum",
    "ls_reg.ele",
    "ls_unit.ele",
    "manure.frt",
    "nutrients.cha",
    "nutrients.res",
    "nutrients.rte",
    "nutrients.sol",
    "object.cnt",
    "object.prt",
    "om_osrc.wal",
    "om_treat.wal",
    "om_use.wal",
    "om_water.ini",
    "parameters.bsn",
    "rec_catunit.ele",
    "res_catunit.ele",
    "reservoir.res",
    "reservoir.res_cs",
    "rout_unit.ele",
    "salt_aqu.ini",
    "salt_fertilizer.frt",
    "satbuffer.str",
    "scen_dtl.upd",
    "sed_nut.cha",
    "sediment.cha",
    "sediment.res",
    "shade_factor.shf",
    "soils_lte.sol",
    "temperature.cha",
    "time.sim",
    "topography.hyd",
    "water_tower.wal",
    "wb_parms.sft",
    "weir.res",
    "wetland.wet",
    "wetland.wet_cs",
    # -- added 2026-07: verified against source after the overlay-agreement
    # heuristic flagged these for review; the schema was correct all along --
    "carbon.bsn",
    "outside_rcv.wal",
    "rout_unit.rtu",
    "weather-sta.cli",
    # -- added 2026-07: needed the collision-prefix fix in read_to_schema --
    "recall_db.rec",
    # -- added 2026-07: plain-intrinsic record reads, unlocked by the
    # `_is_intrinsic_record_read` fallback (these name ordinary typed columns
    # but never touch a derived type, so the old gate discarded them) --
    "floodplain.gw",
    "gwflow.wetland",
    "hrucell.gw",
    "lsucell.gw",
    "phreato.gw",
    "phreato_cell.gw",
    "pond_cell.gw",
    "pumpex.gw",
    "rescell.gw",
    "solute.gw",
    # -- added 2026-07: variable-length records where the repeat count is
    # provably a value already read in this same record (a `record_layout`
    # repeat group -- see `RepeatGroup`, `resolve_variable_length_read`) --
    "aqu_catunit.def",
    "aqu_cha.lin",
    "aquifer.con",
    "ch_catunit.def",
    "ch_reg.def",
    "ch_sed_budget.sft",
    "chan-surf.lin",
    "chandeg.con",
    "channel.con",
    "delratio.con",
    "exco.con",
    "gwflow.con",
    "hru-lte.con",
    "hru.con",
    "ls_reg.def",
    "ls_unit.def",
    "outlet.con",
    "plant_gro.sft",
    "plant_parms.sft",
    "rec_catunit.def",
    "rec_reg.def",
    "recall.con",
    "res_catunit.def",
    "res_reg.def",
    "reservoir.con",
    "rout_unit.con",
    "rout_unit.def",
    # -- added 2026-07: positional hand-parsed records (resolve_positional_extraction) --
    "cells.gw",
    "chancell.gw",
    "zones.gw",
    # -- added 2026-07: tagged (keyed) positional column (_resolve_tagged_positional_column) --
    "outputs.gw",
    # -- added 2026-08: found by cross-checking every file the Fortran source
    #    actually opens against this list -- these were simply never added,
    #    not an extraction gap; each resolves with existing extractor
    #    support, no new resolver code needed. manure_allo.mnu and
    #    pest_metabolite.pes were also candidates but are deliberately left
    #    out: pest_metabolite.pes is the documented two-shape exclusion
    #    above (see test_files_excluded_for_documented_reasons_stay_out);
    #    manure_allo.mnu's demand block was flagged for a nested
    #    variable-length array (`trn(:)%withdr(isrc)`) that, on inspection,
    #    is only ever `allocate`d with `source = 0.` and never actually
    #    read from any line in manure_allocation_read.f90 - the resolved
    #    3-block schema may already be complete, but left out pending
    #    someone confirming that reading against the original caution --
    "tile.gw",
    "pest.com",
    "res_conds.dat",
    # -- added 2026-08: co2_yr.dat failed with "unknown derived type
    #    'co2_annual'" -- a real scanner gap, now fixed. co2_read.f90
    #    declares `type co2` / `type co2_annual` local to the subroutine's
    #    own specification part (the only place in the pinned source this
    #    happens; every other derived type is module-level), and the
    #    scanner only ever collected `type ... end type` declarations seen
    #    outside any procedure. Fixed in fortran.py's type-collection check
    #    to no longer gate on that (see FortranScannerTests -- the
    #    procedure-local-type case). Resolves cleanly once the type is
    #    findable: `co2_inc%co2_yr(itot)`'s two fields (iyr, co2) --
    "co2_yr.dat",
    # -- added 2026-08: manure_allo.mnu was left out of the 2026-08 batch
    #    above pending confirmation that its demand block's caution (see the
    #    header+sub-block section below) doesn't apply to THIS resolution
    #    path. Confirmed: `trn(:)%withdr(isrc)` is never read anywhere in the
    #    pinned source, so the per-open block resolution's existing 3-block
    #    schema (header / source rows / demand rows) is already complete --
    "manure_allo.mnu",
)

# Investigated 2026-08: the 8 files 5eeaf58 flagged as unresolved-even-when-
# targeted inside gwflow_read.f90 and its siblings (chan_depth.gw,
# hru_pump.gw, pond_div.gw, sw_group.gw, transit.gw, soil_lyr_depths.sol,
# carbon_layers.prt, looping.con). All 8 came back the generic "reader not
# found for filename" -- not a specific reason -- which turned out to be two
# separate things wearing the same message.
#
# A real scanner bug, now fixed: `_update_condition_stack`'s end-of-block
# check (fortran.py) only matched `end if`/`end do`/`end select` *with* a
# space. Free-form Fortran also allows the no-space spelling (`endif`/
# `enddo`/`endselect`), and gwflow_read.f90's whole family spells every
# closing statement that way, exclusively -- so inside these procedures the
# condition stack never popped: it just grew for the entire 2000+-line
# procedure body, and `_in_do_loop` (which scans that trail for a `do`) saw
# a loop opened hundreds of lines earlier as still enclosing every later
# read. Fixed to match both spellings, same as every other "end X" regex in
# fortran.py already did (see ConditionTrailUnspacedEndKeywordTests). Zero
# effect on any currently-resolved file -- byte-identical schema -- but it
# was what made every read in these procedures look suspect while
# investigating, this one included.
#
# With that noise gone, all 8 turned out to already be correctly
# unresolvable, each for a reason this schema already declines elsewhere by
# design -- not a resolver gap:
#   - sw_group.gw is already the documented cellcon.gw-style decline
#     (`fields(2+j)`, a computed column index) a few lines above and in
#     test_files_excluded_for_documented_reasons_stay_out. Not new; the
#     condition-stack bug just made it look unexplained.
#   - hru_pump.gw, transit.gw, soil_lyr_depths.sol each read their rows as a
#     single bare column inside a `do` loop (`hru_pump_ids(i)`,
#     `cell_transit`, `csld`) -- exactly the "genuinely ambiguous with a
#     record-count prescan" case `_is_intrinsic_record_read` already
#     declines by design (see its docstring's second guard).
#   - carbon_layers.prt is three lines -- title, header, one scalar integer
#     (a layer count) -- no row data at all, the same category as codes.gw.
#   - looping.con is never read anywhere in the pinned source: it's a
#     write-only diagnostic dump (hyd_connect.f90's infinite-loop guard),
#     not an input file. The open()-based gap scan that flagged it as a
#     candidate can't tell read from write; same category as the
#     gwflow-output-writer files 5eeaf58 already excluded for that reason.
#   - chan_depth.gw and pond_div.gw are opened in one procedure
#     (gwflow_chan_read.f90 / gwflow_read.f90, respectively) on a
#     module-level unit that's deliberately left open, unclosed, past that
#     procedure's return; their actual per-timestep row read lives in a
#     DIFFERENT procedure entirely (gwflow_simulate.f90 / gwflow_pond.f90)
#     that never opens anything itself. Both rows are otherwise perfectly
#     ordinary and resolvable (`year month day (div(r),r=1,gw_npond)`,
#     `dum dum (dep(j),j=1,gw_chan_ndpzn)`) -- the gap is architectural:
#     nothing in the resolver looks for a matching `open` in a SIBLING
#     procedure when a block has none of its own. A real, uncaptured gap,
#     not attempted here: the current per-procedure attribution model would
#     need a deliberately scoped cross-procedure unit search to close it,
#     and a wrong guess there (unit numbers and names get reused for
#     different files elsewhere in the same run -- `in_gw` alone opens 16
#     different files in gwflow_read.f90) would misattribute real data
#     rather than just miss it.
# None of the 8 added to TARGET_FILES above; none of them produce a schema
# today, each for a reason already covered elsewhere in this file.

# Decision tables (`*.dtl`): a genuinely different shape from everything in
# TARGET_FILES above, so they get their own resolution path
# (`build_decision_tables`) and their own payload section, not a `ReadSchema`
# entry. All four share one Fortran type (`decision_table`, in
# conditional_module.f90): a 4-field header record (name, conds, alts, acts),
# then `conds` condition rows (`conditions_var` flattened, 6 fields, plus an
# `alts`-driven implied-do tail of `alt` strings), then `acts` action rows
# (`actions_var` flattened, 8 fields, plus the same `alts`-driven tail of
# `act_outcomes` strings) -- verified identical across dtbl_lum_read.f90,
# dtbl_res_read.f90, dtbl_scen_read.f90, and dtbl_flocon_read.f90.
DECISION_TABLE_FILES: tuple[str, ...] = (
    "flo_con.dtl",
    "lum.dtl",
    "res_rel.dtl",
    "scen_lu.dtl",
)

# Multi-record files: a header record followed by one or more blocks of
# sub-records, each block sized by a column of that header (see
# `MultiRecordSchema` / `build_multi_records`). A separate shape and payload
# section, like decision tables -- not a flat `ReadSchema`.
#   - `soils.sol`     : a soil header (snam, nly, hydgrp, zmx, anion_excl,
#                       crk, texture) + `nly` layer records (14 columns each).
#   - `plant.ini`     : a plant-community header (name, plants_com,
#                       rot_yr_ini) + `plants_com` plant records (8 cols each).
#   - `weather-wgn.cli`: a station header (wgn_n, lat, long, elev, rain_yrs --
#                       spanning two roots, `wgn_n(i)` and `wgn(i)%...`) + a
#                       fixed 12 monthly-stat records (14 columns each), the
#                       block sized by the literal `do mo = 1, 12`, not a
#                       header column.
#   - `management.sch`: a schedule header (name, num_ops, num_autos) + an auto
#                       block (`num_autos` `auto_name` rows) + an operations
#                       block (`num_ops` rows, 7 columns). Two wrinkles the
#                       detector handles: the operations block is read in a
#                       called helper on the same unit (`read_mgtops`), and the
#                       auto block is keyed -- the generic-table names
#                       `pl_hv_summer1/winter1/summer2` backspace and re-read
#                       extra `auto_crop` columns -- so it is marked
#                       `variable_width` with only the guaranteed `auto_name`
#                       column, not falsely fixed at one column.
# Other header+sub-block files are deliberately NOT curated here yet, each for
# a real reason:
#   - `manure_allo.mnu` -- NOT because of a nested variable-length array (a
#     prior caution here said its demand block had one; checked directly
#     against manure_allocation_read.f90 2026-08 and found no `read` of any
#     kind touches `trn(:)%withdr(isrc)` anywhere in the pinned source --
#     it's `allocate`d with `source = 0.` and only ever written to at
#     runtime, by mallo_control.f90's demand computation. That reading is
#     safe and unrelated to this file's flat `files`/TARGET_FILES entry
#     (added, see below) -- `manure_allocation_read`'s ordinary per-open
#     block resolution already captures the demand row's real 5 columns
#     (k, ob_typ, ob_num, dtbl, right) exactly, `withdr` never among them.
#     The real reason THIS detector -- `resolve_multi_record_block`, a
#     structurally different resolution path than TARGET_FILES/`files` --
#     isn't safe for it: `num_objs`, the demand sub-block's `do` count, is
#     assigned from `mallo(imro)%src_obs` at line 56 and then REASSIGNED
#     from `mallo(imro)%trn_obs` at line 58 before the demand loop actually
#     uses it -- but `_find_count_field` returns the first matching
#     assignment in the whole procedure, not the one nearest the read, so it
#     resolves the demand block's count to `src_obs` instead of `trn_obs`.
#     Both the source sub-block (`src_obs`-counted, 19 columns) and the
#     demand sub-block end up keyed identically and collapse into one
#     `_collapse_multi_record_blocks` group, silently keeping only the
#     narrower demand columns under the WRONG count field -- not a decline,
#     a wrong answer, which is worse. See
#     StaleCountReassignmentTests in test_input_schema.py for the minimal
#     repro. Left out of MULTI_RECORD_FILES until `_find_count_field` is
#     made position-aware (nearest preceding assignment, not first match) --
#     not attempted here, since no currently-curated multi_record file
#     depends on a reassigned local count variable and a wrong guess at the
#     fix risks the files that already resolve correctly.
# The detector also structurally matches, but we do NOT curate here, these
# files (claimed internally, never output):
#   - `ch_sed_budget.sft`, `plant_gro.sft`, `plant_parms.sft` -- already
#     covered in the flat `files` section as `record_layout` (a single read
#     with an implied-do tail); their header+block reading is an alternative
#     view of the same file, so leaving them in `files` avoids listing one
#     file in two sections with two shapes.
#   - `lum.dtl` and other decision tables -- header + count-driven blocks too,
#     but with per-row implied-do tails and vocabularies the `decision_tables`
#     section captures and this one would drop; kept there.
#   - `calibration.cal` -- now fully resolved and added. Its main record is
#     itself variable-length (10 fixed fields + `num_tot` + an `elem_cnt`
#     implied-do tail, resolved via the peek-count binding
#     `_peek_bound_count_field`, the same fix that added `chan-surf.lin`) --
#     carried honestly as `header.repeat` (`MultiRecordSchema.header_repeat`)
#     rather than silently dropped, so the header doesn't look narrower than
#     it really is. Each record is then followed by an optional
#     `conds`-counted conditions block whose rows are KEYED with two
#     structurally different shapes: `if (range == "range") then` reads
#     `range, var, val1, val2`; `else` reads a full `cond` record (`var, alt,
#     targ, targc`). Resolved by `resolve_multi_record_block`'s if/else
#     pairing (see `_find_if_else_read_pairs`, and fortran.py's else/elseif
#     condition-trail tracking that makes the two branches' reads
#     distinguishable at all) -- emitted as a `tag_field` block with one
#     `TaggedRowVariant` per branch, `"range"` and the catch-all `"other"`,
#     rather than guessing one shape. `outputs.gw` is a different resolution
#     path entirely (a hand-parsed, `resolve_positional_extraction` file) and
#     isn't reached by this; it stays excluded for its own, separately
#     documented reason.
MULTI_RECORD_FILES: tuple[str, ...] = (
    "calibration.cal",
    "management.sch",
    "plant.ini",
    "soils.sol",
    "water_allocation.wro",
    "weather-wgn.cli",
)

# Multi-section files: one physical file contains more than one logical read
# section/pass, so it cannot be represented honestly as one flat row shape.
# The measured-weather station lists count data rows, reread station names, then
# reread station filenames. `constituents.cs` is a stacked count/list file: each
# constituent-category count is followed by the matching variable-width name
# list. Per-station time-series files opened later on unit 108, and the files
# whose arity is governed by `constituents.cs`, are represented separately or
# still intentionally excluded until their external count references can be
# expressed without inventing a flat shape.
MULTI_SECTION_FILES: tuple[str, ...] = (
    "constituents.cs",
    "hmd.cli",
    "pcp.cli",
    "pet.cli",
    "slr.cli",
    "tmp.cli",
    "wnd.cli",
)

_CONSTITUENTS_CS_SECTIONS: tuple[tuple[str, str, str], ...] = (
    ("pests", "num_pests", "pests"),
    ("paths", "num_paths", "paths"),
    ("metals", "num_metals", "metals"),
    ("salts", "num_salts", "salts"),
    ("cs", "num_cs", "cs"),
)

# Runtime-arity files have fields whose column count is governed by a runtime
# count defined outside the file itself. They are not flat `files` rows; keep
# them additive and explicit.
RUNTIME_ARITY_FILES: tuple[str, ...] = (
    "cs_recall.rec",
    "salt_recall.rec",
    "water_canal.wal",
    "water_pipe.wal",
    "dr_hmet.del",
    "dr_path.del",
    "dr_pest.del",
    "dr_salt.del",
    "exco_hmet.exc",
    "exco_path.exc",
    "exco_pest.exc",
    "exco_salt.exc",
    "atmodep.cli",
    "cs_atmo.cli",
    "salt_atmo.cli",
    "cs_aqu.ini",
    "cs_channel.ini",
    "cs_hru.ini",
    "hmet_hru.ini",
    "path_hru.ini",
    "path_water.ini",
    "pest_hru.ini",
    "pest_water.ini",
    "salt_hru.ini",
    "salt_channel.ini",
    "water_treat.wal",
    "water_use.wal",
    "out_src.wal",
    "cell_sol.gw",
    "minerals.gw",
    "tvheads.gw",
    "ponds.gw",
    "gwflow_canal.con",
)

# Pinned-source filename attribution fixes: SWAT+ 62.0.0 has a small number of
# readers whose `open(file=...)` expression points at the wrong sibling
# `file.cio` slot even though the surrounding control flow clearly belongs to a
# different declared filename. Keep these overrides keyed narrowly by reader,
# source line, and the mistaken resolved filename so we repair only the known
# upstream bug and do not generalize past the evidence.
_OPEN_FILENAME_OVERRIDES: dict[tuple[str, int, str], tuple[str, ...]] = {
    ("aqu_read_elements.f90", 89, "aqu_catunit.def"): ("aqu_reg.def",),
}
# Intrinsic Fortran base types the consumer treats as numeric. ``character`` (and
# anything else, e.g. ``logical``) is non-numeric; that is the check the
# consumer actually runs against a submitted value.
_NUMERIC_BASE_TYPES = frozenset({"real", "integer", "double precision"})

_DERIVED_TYPE_RE = re.compile(r"type\s*\(\s*([a-z_]\w*)", re.I)
_DIMENSION_RE = re.compile(r"dimension\s*\(([^)]*)\)", re.I)
# A read field like ``manure_om(it)%name`` or ``snodb(isno)`` or ``pldb(ic)``:
# leading identifier, optional (index), optional %component chain.
_FIELD_RE = re.compile(r"^([a-z_]\w*)\s*(?:\([^()]*\))?\s*(%.*)?$", re.I)
_LITERAL_FILE_RE = re.compile(r"^[\w.\-]+\.\w+$")
# SWAT+'s conventional names for a read target whose value is discarded: a
# title line, a column-header line, or a scratch line consumed to align the
# file position. They are never file columns in their own right.
_THROWAWAY_TARGETS = frozenset({"titldum", "header"})
_DO_LOOP_RE = re.compile(r"(?:^|>)\s*do\b", re.I)
# An implied-do read item: ``(ob(i)%obtyp_out(isp), ..., isp = 1, nout)``.
_IMPLIED_DO_RE = re.compile(r"^\(.*,\s*\w+\s*=\s*[^,]+,[^,)]+\)$")
# An internal read's unit: a character array element with a LITERAL index,
# e.g. ``split_fields(4)``. A computed index (``split_fields(2+j)``) does not
# match -- it signals a data-dependent repeat group, a different shape.
_INTERNAL_READ_UNIT_RE = re.compile(r"^([a-z_]\w*)\(\s*(\d+)\s*\)$", re.I)
_ASSIGNMENT_RE = re.compile(r"^\s*([a-z_]\w*(?:\([^()]*\))?(?:%[a-z_]\w*)?)\s*=\s*(.+?)\s*$", re.I)


@dataclass(slots=True)
class FieldSpec:
    fortran_name: str
    fortran_type: str
    numeric: bool
    units: str | None
    doc: str | None
    # Verbatim ``|range:`` token text, kept so a disputed range's parenthetical
    # survives into the artifact even though only the leading pair is parsed.
    range_text: str | None = None
    minimum: float | None = None
    maximum: float | None = None

    def to_dict(self, position: int) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "position": position,
            "fortran_name": self.fortran_name,
            "fortran_type": self.fortran_type,
            "numeric": self.numeric,
            "units": self.units,
            "doc": self.doc,
        }
        if self.range_text is not None:
            payload["range"] = self.range_text
        if self.minimum is not None:
            payload["minimum"] = self.minimum
        if self.maximum is not None:
            payload["maximum"] = self.maximum
        return payload


@dataclass(slots=True)
class RepeatGroup:
    """A variable-length record tail: ``fields`` repeated ``count_field`` times.

    ``count_field`` is the ``fortran_name`` of a column already present in the
    read's fixed prefix (see :class:`ReadSchema`) whose value at read time
    determines how many repeats follow -- e.g. ``src_tot`` for a ``.con``
    file's outflow objects, or ``nspu`` for a ``.def`` file's element list.
    """

    fields: list[FieldSpec]
    count_field: str
    count_expr: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "count_field": self.count_field,
            "count_expr": self.count_expr,
            "fields": [f.to_dict(i) for i, f in enumerate(self.fields)],
        }


@dataclass(slots=True)
class ReadSchema:
    """A resolved data read: the ordered columns plus provenance.

    ``repeat`` is set only for a record with a data-dependent tail whose
    count is provably a value already read in this same record; see
    :meth:`SchemaResolver.resolve_variable_length_read`. ``fields`` is
    always just the fixed prefix -- the repeat group's columns live in
    ``repeat.fields``, never mixed into ``fields`` itself, so a consumer
    that ignores ``repeat`` still gets an honest (if partial) schema
    instead of a misleadingly short flat one.

    ``tag_field``/``variants`` are set only for a hand-parsed (positional)
    record whose column meaning depends on another column's value -- e.g.
    ``outputs.gw``'s rows, where column 2 means one thing when column 1 is
    ``"head_output_time"`` and something else entirely for
    ``"observation_cell"``. ``tag_field`` is the source expression that
    supplies the tag (the source never assigns it to a persisted variable,
    so there is no field name to invent for it); ``variants`` is one
    :class:`TaggedRowVariant` per case the source's own ``select case``
    dispatches on (see :meth:`SchemaResolver.resolve_positional_extraction`).
    ``fields`` holds any OTHER columns the record has outside the tagged one.
    """

    fields: list[FieldSpec]
    pattern: str  # "derived_type" | "field_list" | "positional"
    base_type: str | None
    type_source: str | None
    reader_line: int
    repeat_source: str | None = None
    repeat_expr: str | None = None
    repeat: RepeatGroup | None = None
    tag_field: str | None = None
    variants: list[TaggedRowVariant] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "reader_line": self.reader_line,
            "read_pattern": self.pattern,
            "derived_type": self.base_type,
            "type_source": self.type_source,
            "fields": [f.to_dict(i) for i, f in enumerate(self.fields)],
        }
        if self.repeat is not None:
            payload["variable_arity"] = True
            payload["repeat"] = self.repeat.to_dict()
        if self.tag_field is not None:
            payload["tag_field"] = self.tag_field
            payload["variants"] = [v.to_dict() for v in self.variants]
        return payload


@dataclass(slots=True)
class DecisionTableBlock:
    """One of a decision table's two record blocks (conditions or actions).

    ``row_count_field`` names the header field (e.g. ``conds``) whose value
    at read time is how many ``row_fields`` records follow; each of those
    records ends with a trailing repeat of ``repeat_field``, run
    ``repeat_count_field`` times (e.g. ``alts``). Unlike :class:`RepeatGroup`,
    both counts live in an earlier, separate header record -- not a column
    already read in the same record -- which is exactly why decision tables
    need their own shape instead of reusing ``ReadSchema``/``RepeatGroup``.
    """

    row_count_field: str
    row_fields: list[FieldSpec]
    repeat_count_field: str
    repeat_field: FieldSpec

    def to_dict(self) -> dict[str, Any]:
        return {
            "row_count_field": self.row_count_field,
            "row": {
                "fields": [f.to_dict(i) for i, f in enumerate(self.row_fields)],
                "repeat": {
                    "count_field": self.repeat_count_field,
                    "fields": [self.repeat_field.to_dict(0)],
                },
            },
        }


@dataclass(slots=True)
class DecisionTableSchema:
    """A resolved decision-table (``*.dtl``) reader: header + two blocks.

    ``condition_vocabulary`` and ``action_vocabulary`` are the closed sets of
    string literals the file's rows may legally use for ``cond%var`` and
    ``act%typ`` respectively, captured from the source's own ``select case``
    dispatch (see ``SelectCaseDoc``) rather than guessed -- a row using any
    other value would never match a case branch at runtime. ``other_vocabularies``
    carries any further select-case dispatch found in the same reader (e.g. a
    per-action-type ``option`` sub-dispatch) that doesn't fit either slot above;
    included as-is rather than discarded, but not claimed to nest under a
    particular action type since that structural link isn't tracked.
    """

    header_fields: list[FieldSpec]
    condition_block: DecisionTableBlock
    action_block: DecisionTableBlock
    condition_vocabulary: list[str]
    action_vocabulary: list[str]
    other_vocabularies: list[tuple[str, list[str]]]
    reader: str
    reader_line: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "reader": self.reader,
            "reader_line": self.reader_line,
            "read_pattern": "decision_table",
            "header": {"fields": [f.to_dict(i) for i, f in enumerate(self.header_fields)]},
            "condition_block": self.condition_block.to_dict(),
            "action_block": self.action_block.to_dict(),
            "vocabulary": {
                "condition_var": self.condition_vocabulary,
                "action_typ": self.action_vocabulary,
                "other": [
                    {"subject": subject, "cases": cases}
                    for subject, cases in self.other_vocabularies
                ],
            },
        }


@dataclass(slots=True)
class MultiRecordBlock:
    """A block of sub-records that follows a header record.

    Distinct from :class:`RepeatGroup` (whose repeats are the tail of one
    read statement) and from :class:`DecisionTableBlock` (whose per-row tail
    and vocabulary make it a different shape): here the header and the
    sub-records are *separate* read statements -- a header line, then a
    ``do``-loop of sub-record lines.

    The block's length is given exactly one of two ways, emitted as the
    matching key: ``count_field`` -- the loop bound is (directly or through a
    traced local assignment) one of the header's own columns (soils.sol's
    ``nly``) -- or ``count`` -- the loop bound is a compile-time literal
    (weather-wgn.cli's twelve monthly-stat rows, ``do mo = 1, 12``).

    ``variable_width`` marks a *keyed* block whose rows are still all the
    *same* shape but sometimes wider: the reader reads a base row, then for
    certain first-column values backspaces and re-reads a wider row
    (management.sch's auto block, where ``pl_hv_summer1`` etc. carry extra
    crop columns). ``row_fields`` then holds only the columns guaranteed on
    every row (the common prefix); the flag tells the consumer not to reject
    a wider row as having too many columns.

    ``row_repeat`` / ``row_suffix_fields`` mark a row whose own record
    contains a nested implied-do group followed by trailing fields: a fixed
    prefix, then a repeated group counted by one of that prefix's columns, then
    a fixed suffix (water_allocation.wro's transfer rows). This is still one
    counted sub-block, but its row is richer than a plain flat field list.

    ``variants`` marks a *tagged* block whose rows are genuinely different
    shapes, not just different widths: the reader peeks the row's own leading
    value and dispatches to one of several structurally distinct field lists
    (calibration.cal's conditions block -- see :class:`TaggedRowVariant`).
    When set, ``row_fields`` is empty and ``tag_field`` names the column the
    dispatch is keyed on.
    """

    row_fields: list[FieldSpec] = field(default_factory=list)
    count_field: str | None = None
    count_literal: int | None = None
    variable_width: bool = False
    row_repeat: RepeatGroup | None = None
    row_suffix_fields: list[FieldSpec] = field(default_factory=list)
    tag_field: str | None = None
    variants: list[TaggedRowVariant] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        if self.count_field is not None:
            out["count_field"] = self.count_field
        else:
            out["count"] = self.count_literal
        if self.tag_field is not None:
            out["row"] = {"tag_field": self.tag_field, "variants": [v.to_dict() for v in self.variants]}
        else:
            out["row"] = {"fields": [f.to_dict(i) for i, f in enumerate(self.row_fields)]}
            if self.row_repeat is not None:
                out["row"]["repeat"] = self.row_repeat.to_dict()
            if self.row_suffix_fields:
                out["row"]["suffix_fields"] = [
                    f.to_dict(i) for i, f in enumerate(self.row_suffix_fields)
                ]
            if self.variable_width:
                out["variable_width"] = True
        return out


@dataclass(slots=True)
class TaggedRowVariant:
    """One shape a tagged (keyed) block's row can take.

    Selected at read time by the row's own leading value: ``tag`` is the
    literal that selects this variant (calibration.cal's ``"range"``), or the
    sentinel ``"other"`` for the catch-all ``else`` branch, which stands for
    every value that doesn't match any of the block's other tags.
    """

    tag: str
    fields: list[FieldSpec]

    def to_dict(self) -> dict[str, Any]:
        return {"tag": self.tag, "fields": [f.to_dict(i) for i, f in enumerate(self.fields)]}


@dataclass(slots=True)
class MultiRecordSchema:
    """A resolved multi-record file: a header record plus one or more blocks
    of sub-records, each block sized by a column of the header.

    E.g. ``soils.sol`` (a soil header, then ``nly`` layer records) or
    ``plant.ini`` (a plant-community header, then ``plants_com`` plant
    records). The header's columns live in ``header_fields``; each block's
    sub-record columns live in its own ``row_fields`` -- never mixed -- so a
    consumer that only understands the header still gets an honest, if
    partial, schema.

    ``header_repeat`` is set when the header record is *itself*
    variable-length -- its own trailing implied-do tail, resolved the same
    way as a flat ``ReadSchema``'s ``repeat`` (see
    :meth:`SchemaResolver.resolve_variable_length_read`; calibration.cal's
    main record reads 10 fixed fields, ``num_tot``, then an ``elem_cnt`` tail
    counted by ``num_tot``). Without this a header that has its own repeat
    tail would silently look like a plain fixed-width record.
    """

    header_fields: list[FieldSpec]
    blocks: list[MultiRecordBlock]
    reader: str
    reader_line: int
    header_repeat: RepeatGroup | None = None

    def to_dict(self) -> dict[str, Any]:
        header: dict[str, Any] = {"fields": [f.to_dict(i) for i, f in enumerate(self.header_fields)]}
        if self.header_repeat is not None:
            header["variable_arity"] = True
            header["repeat"] = self.header_repeat.to_dict()
        return {
            "reader": self.reader,
            "reader_line": self.reader_line,
            "read_pattern": "multi_record",
            "header": header,
            "blocks": [b.to_dict() for b in self.blocks],
        }


@dataclass(slots=True)
class MultiSectionSection:
    """One logical section/pass within a multi-section input file."""

    name: str
    fields: list[FieldSpec]
    count_source: str
    reader_line: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "count_source": self.count_source,
            "reader_line": self.reader_line,
            "fields": [f.to_dict(i) for i, f in enumerate(self.fields)],
        }


@dataclass(slots=True)
class MultiSectionSchema:
    """A resolved file with multiple logical read sections/passes."""

    sections: list[MultiSectionSection]
    reader: str
    reader_line: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "reader": self.reader,
            "reader_line": self.reader_line,
            "read_pattern": "multi_section",
            "sections": [s.to_dict() for s in self.sections],
        }


@dataclass(slots=True)
class RuntimeArityField:
    """A field whose width may be governed by an external runtime count."""

    field: FieldSpec
    count_source: str | None = None
    count_expr: str | None = None

    def to_dict(self, position: int) -> dict[str, Any]:
        payload = self.field.to_dict(position)
        if self.count_source is not None:
            payload["variable_arity"] = True
            payload["count_source"] = self.count_source
            payload["count_expr"] = self.count_expr
        return payload


@dataclass(slots=True)
class RuntimeAritySection:
    """One physical/logical record section in a runtime-arity file."""

    name: str
    fields: list[RuntimeArityField]
    count_source: str
    reader_line: int
    applies_when: str | None = None
    nested_file_field: str | None = None
    repeat_source: str | None = None
    repeat_expr: str | None = None
    repeat_fields: list[RuntimeArityField] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "name": self.name,
            "count_source": self.count_source,
            "reader_line": self.reader_line,
            "fields": [f.to_dict(i) for i, f in enumerate(self.fields)],
        }
        if self.applies_when is not None:
            payload["applies_when"] = self.applies_when
        if self.nested_file_field is not None:
            payload["nested_file_field"] = self.nested_file_field
        if self.repeat_source is not None:
            payload["repeat_source"] = self.repeat_source
            payload["repeat_expr"] = self.repeat_expr
            if self.repeat_fields:
                payload["repeat_fields"] = [f.to_dict(i) for i, f in enumerate(self.repeat_fields)]
        return payload


@dataclass(slots=True)
class RuntimeAritySchema:
    """A file whose row/section width depends on a runtime count source."""

    sections: list[RuntimeAritySection]
    reader: str
    reader_line: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "reader": self.reader,
            "reader_line": self.reader_line,
            "read_pattern": "runtime_arity",
            "sections": [s.to_dict() for s in self.sections],
        }


def base_type_word(vartype: str | None) -> str:
    """Normalise a declaration type to its base word: ``character (len=40)`` ->
    ``character``, ``double precision`` -> ``double precision``."""
    text = (vartype or "").strip().lower()
    if not text:
        return "unknown"
    if text.startswith("double"):
        return "double precision"
    return re.split(r"[\s(]", text, maxsplit=1)[0]


def is_numeric_type(vartype: str | None) -> bool:
    return base_type_word(vartype) in _NUMERIC_BASE_TYPES


def array_multiplicity(comp: VariableRef) -> int:
    """How many list-directed columns a component occupies.

    A fixed-size array component (``real, dimension(4) :: cn`` or ``real ::
    cn(4)``) flattens to that many columns in Fortran list-directed I/O. Returns
    1 for scalars and for symbolic/assumed-shape sizes we cannot expand.
    """
    decl = comp.declaration or ""
    match = _DIMENSION_RE.search(decl)
    dims_text: str | None = match.group(1) if match else None
    if dims_text is None:
        # Dimensions attached to the name itself, e.g. ``:: cn(4)``. Anchor on
        # the component name to avoid matching a ``character(len=..)`` kind spec.
        name_dim = re.search(rf"::[^:]*\b{re.escape(comp.name)}\s*\(([^)]*)\)", decl, re.I)
        dims_text = name_dim.group(1) if name_dim else None
    if not dims_text:
        return 1
    total = 1
    for dim in dims_text.split(","):
        dim = dim.strip()
        if re.fullmatch(r"\d+", dim):
            total *= int(dim)
        elif ":" in dim:
            lo, _, hi = dim.partition(":")
            if re.fullmatch(r"-?\d+", lo.strip()) and re.fullmatch(r"-?\d+", hi.strip()):
                total *= int(hi) - int(lo) + 1
            else:
                return 1  # assumed/allocatable shape — not a fixed column count
        else:
            return 1  # symbolic size (e.g. a named constant) — cannot expand
    return total


def derived_type_name(vartype: str | None) -> str | None:
    """Return the inner type name of a ``type (foo)`` declaration, else None."""
    if not vartype:
        return None
    match = _DERIVED_TYPE_RE.search(vartype)
    return match.group(1).lower() if match else None


# A trailing ``|range: <text>`` token on a declaration comment. The token is
# labelled rather than positional: SWAT+ comments already use one, two, and
# three pipe fields, so a range identified by pipe position could not be told
# apart from the legacy ``<oldname> |<units> |<desc>`` form.
RANGE_TOKEN_RE = re.compile(r"\|\s*range:\s*(?P<range>[^|]*?)\s*$", re.IGNORECASE)

# ``0-1``, ``0.0001-0.01``, ``-90-90``, or a lower bound only as ``>=0``.
_RANGE_PAIR_RE = re.compile(r"^\s*(-?[0-9.]+)\s*-\s*(-?[0-9.]+)\s*$")
_RANGE_MIN_RE = re.compile(r"^\s*>=\s*(-?[0-9.]+)\s*$")


def extract_range(doc: str) -> tuple[str, str | None]:
    """Split a trailing ``|range: ...`` token off a declaration comment.

    Returns the comment with the token removed and the token's text, so the
    description never absorbs the range.  Without this the existing
    "description is everything after the first pipe" rule would fold the range
    into the prose.
    """
    if not doc:
        return doc, None
    match = RANGE_TOKEN_RE.search(doc)
    if match is None:
        return doc, None
    return doc[: match.start()].rstrip(), (match.group("range").strip() or None)


def parse_range_token(text: str | None) -> tuple[float | None, float | None]:
    """Parse a range token's text into ``(minimum, maximum)``.

    A disputed range carries the source value first and the modular database's
    value in a trailing parenthetical, e.g. ``0-1 * (modular db: 10-17.5)``.
    The source range is authoritative, so the parenthetical is ignored here and
    only flagged for review.
    """
    if not text:
        return None, None
    head = text.split("*", 1)[0].strip()
    pair = _RANGE_PAIR_RE.match(head)
    if pair is not None:
        return float(pair.group(1)), float(pair.group(2))
    lower = _RANGE_MIN_RE.match(head)
    if lower is not None:
        return float(lower.group(1)), None
    return None, None


def split_units_doc(doc: str) -> tuple[str | None, str | None]:
    """Parse a SWAT+ trailing comment ``deg C  |snowfall temp`` into
    ``("deg C", "snowfall temp")``.

    Units are read from the ``<units> |<desc>`` inline comment. The units token
    is taken from the line that actually contains the ``|`` (not merely the
    first line), so a multi-line ``!!`` comment misattributed above the
    declaration cannot masquerade as units. Multi-line descriptions collapse to
    a single line. A trailing ``|range:`` token is removed first so it never
    lands in the description.
    """
    if not doc or not doc.strip():
        return None, None
    doc, _ = extract_range(doc)
    if not doc.strip():
        return None, None
    lines = doc.strip().splitlines()
    pipe_idx = next((i for i, line in enumerate(lines) if "|" in line), None)
    if pipe_idx is None:
        # No pipe: the whole comment is a description (units unknown).
        return None, re.sub(r"\s+", " ", doc.strip()).strip() or None
    units = lines[pipe_idx].split("|", 1)[0].strip() or None
    desc = re.sub(r"\s*\n\s*\|?\s*", " ", doc.split("|", 1)[1]).strip() or None
    return units, desc


# A component-access read considered for multi-record detection:
# (op, root instance names, split tokens, resolved columns, do-nesting depth).
Read = tuple[IOOperation, set[str], list[tuple[str, list[str]]], list[FieldSpec], int]
# Sentinel depth for a read imported from a called helper: always "deeper" than
# any real header, so it qualifies as a sub-block by nesting -- its correctness
# rests on the count-to-header-column linkage, not on physical location.
_IMPORTED_READ_DEPTH = 999


class SchemaResolver:
    """Resolves read statements to column schemas against a scanned project."""

    def __init__(self, project: ProjectIndex):
        self.project = project
        self.types_by_name: dict[str, DerivedTypeDoc] = {
            t.name.lower(): t for t in project.types
        }
        # Global index of module-level variables (read targets like ``snodb``,
        # ``pldb``, ``cn`` are module globals). First declaration wins.
        self.module_vars: dict[str, VariableRef] = {}
        for module in project.modules:
            for var in module.variables:
                self.module_vars.setdefault(var.name.lower(), var)
        self.instance_slot_map = self._build_instance_slot_map()
        self.call_args_by_callee = self._build_call_args_index()

    def _build_call_args_index(self) -> dict[str, list[list[str]]]:
        """Map a called procedure's name to the actual arguments at each call site.

        Resolves the indirect case where a reader's ``open`` names one of its
        own dummy arguments rather than a literal or a ``file.cio`` slot (a
        shared reader parameterized at runtime, e.g. ``hyd_read_connect(con_file,
        ...)`` called once per ``*.con`` file with a different actual filename
        argument each time).
        """
        index: dict[str, list[list[str]]] = {}
        for caller in (*self.project.procedures, *self.project.programs):
            for call in caller.calls:
                if call.kind != "subroutine":
                    continue
                callee = call.name.split("%")[0].lower()
                args = _call_actual_args(call.raw, call.name)
                if args:
                    index.setdefault(callee, []).append(args)
        return index

    def _build_instance_slot_map(self) -> dict[str, str]:
        """Map ``in_parmdb%snow`` -> ``snow.sno`` from ``file.cio`` slot types.

        Any module-level derived-type instance whose type has string-literal
        component initialisers contributes ``<instance>%<component>`` entries.
        This resolves the indirect ``file=in_parmdb%snow`` open expressions.
        """
        slot_map: dict[str, str] = {}
        for name, var in self.module_vars.items():
            type_name = derived_type_name(var.vartype)
            if not type_name:
                continue
            dtype = self.types_by_name.get(type_name)
            if not dtype:
                continue
            for comp in dtype.components:
                literal = _strip_string_literal(comp.initial)
                if literal:
                    slot_map[f"{name}%{comp.name.lower()}"] = literal
        return slot_map

    def resolve_var_type(self, base: str, proc: ProcedureDoc) -> str | None:
        """Resolve a variable's declared type, preferring proc-local decls."""
        lowered = base.lower()
        for var in proc.variables:
            if var.name.lower() == lowered:
                return var.vartype
        var = self.module_vars.get(lowered)
        return var.vartype if var else None

    def flatten_type(
        self, type_name: str, _seen: frozenset[str] = frozenset()
    ) -> list[FieldSpec] | None:
        """Flatten a derived type's components in declaration order.

        Nested derived-type components are expanded recursively (Fortran
        list-directed I/O flattens them into consecutive columns). Returns None
        if the type is unknown or a nested type is unresolvable.
        """
        dtype = self.types_by_name.get(type_name.lower())
        if dtype is None or type_name.lower() in _seen:
            return None
        seen = _seen | {type_name.lower()}
        fields: list[FieldSpec] = []
        for comp in dtype.components:
            nested = derived_type_name(comp.vartype)
            if nested:
                sub = self.flatten_type(nested, seen)
                if sub is None:
                    return None
                fields.extend(sub)
            else:
                fields.extend(self._fields_from_component(comp))
        return fields

    def _fields_from_component(
        self, comp: VariableRef, *, as_scalar: bool = False
    ) -> list[FieldSpec]:
        """One column per scalar component, or N columns for a fixed-size array.

        ``as_scalar`` forces a single column even for a fixed-size array
        component: the read subscripted it to one element (``...%tmpmx(mo)``),
        so it contributes one value per record, not the whole declared array.
        Without this a per-element read of a ``dimension(12)`` component read
        inside a ``do mo = 1, 12`` loop would wrongly expand to 12 columns.
        """
        units, doc = split_units_doc(comp.doc)
        _, range_text = extract_range(comp.doc or "")
        low, high = parse_range_token(range_text)
        base_type = base_type_word(comp.vartype)
        numeric = is_numeric_type(comp.vartype)
        multiplicity = 1 if as_scalar else array_multiplicity(comp)
        if multiplicity <= 1:
            return [FieldSpec(comp.name, base_type, numeric, units, doc, range_text, low, high)]
        return [
            FieldSpec(
                f"{comp.name}({i})", base_type, numeric, units, doc, range_text, low, high
            )
            for i in range(1, multiplicity + 1)
        ]

    def _resolve_component_chain(
        self, dtype: DerivedTypeDoc, chain: list[str], *, last_is_element: bool = False
    ) -> list[FieldSpec] | None:
        """Resolve a ``%a%b`` component chain to one or more columns.

        ``last_is_element`` marks that the read subscripted the final
        component to a single array element (``...%tmpmx(mo)``); it is passed
        through to :meth:`_fields_from_component` so a fixed-size array read
        one element at a time isn't expanded to its full declared width.
        """
        current = dtype
        for depth, comp_name in enumerate(chain):
            match = next(
                (c for c in current.components if c.name.lower() == comp_name.lower()),
                None,
            )
            if match is None:
                return None
            nested = derived_type_name(match.vartype)
            is_last = depth == len(chain) - 1
            if is_last:
                if nested:
                    return self.flatten_type(nested)
                return self._fields_from_component(match, as_scalar=last_is_element)
            if not nested:
                return None
            current = self.types_by_name.get(nested)
            if current is None:
                return None
        return None

    def _is_intrinsic_record_read(
        self,
        parsed: list[tuple[str, list[str], bool]],
        io_op: IOOperation,
        proc: ProcedureDoc,
    ) -> bool:
        """Is this a per-record read of plain intrinsic columns?

        Some input files (several ``*.gw`` grid files in particular) are read
        straight into intrinsic scalars and arrays rather than a derived-type
        record, so the derived-type test above never fires even though the
        read names a perfectly good ordered column list.

        Three guards keep this from turning bookkeeping reads into bogus
        one-column schemas -- the reason the derived-type test existed:

        * it must sit inside a ``do`` loop, i.e. read once per record, which
          excludes the title/header/count reads that precede the loop;
        * it must name at least two columns once SWAT+'s conventional
          throwaway targets are discounted, which excludes the ubiquitous
          ``do while (eof == 0); read (107,*) i`` record-counting pre-pass
          (a one-column loop read is genuinely ambiguous with a real
          one-column record, so we decline rather than guess);
        * every column must resolve to a declared intrinsic type, so a read
          we only partly understand is reported unresolved, never guessed;
        The caller additionally clears ``allow_intrinsic_record`` when any read
        in the same block carries an implied-do (``(x(i), i = 1, n)``): such a
        record is a fixed prefix plus a data-dependent number of repeats, and
        readers commonly peek at the prefix, ``backspace``, then re-read the
        whole record. Resolving the peek would publish the prefix as if it were
        the record -- wrong rather than partial -- so we decline until the
        schema can express a repeat group.
        """
        if not _in_do_loop(io_op):
            return False
        columns = [
            base for base, _chain, _el in parsed if base.lower() not in _THROWAWAY_TARGETS
        ]
        if len(columns) < 2:
            return False
        return all(
            base_type_word(self.resolve_var_type(base, proc)) != "unknown" for base in columns
        )

    def read_to_schema(
        self,
        io_op: IOOperation,
        proc: ProcedureDoc,
        *,
        allow_intrinsic_record: bool = True,
    ) -> tuple[ReadSchema | None, str | None]:
        """Turn one read statement into a column schema.

        Returns ``(schema, None)`` for a resolved data read, ``(None, None)`` for
        a non-data read (header/scalar), or ``(None, reason)`` when a read is
        clearly a data read but a type could not be resolved.

        ``allow_intrinsic_record`` lets the caller suppress the plain-intrinsic
        fallback for a block whose record is variable-length; see
        :meth:`_is_intrinsic_record_read`.
        """
        parsed: list[tuple[str, list[str], bool]] = []  # (base, chain, last_is_element)
        is_data_read = False
        for raw in io_op.fields:
            match = _FIELD_RE.match(raw.strip())
            if not match:
                return None, None
            base = match.group(1)
            chain, last_is_element = _parse_component_chain(match.group(2) or "")
            parsed.append((base, chain, last_is_element))
            type_name = derived_type_name(self.resolve_var_type(base, proc))
            if chain or (type_name and type_name in self.types_by_name):
                is_data_read = True

        if not is_data_read and allow_intrinsic_record:
            is_data_read = self._is_intrinsic_record_read(parsed, io_op, proc)

        if not is_data_read:
            return None, None

        fields: list[FieldSpec] = []
        primary_type: str | None = None
        has_component_access = False
        # (start, end, label) spans of fields expanded from one %chain into
        # more than one column -- candidates for a disambiguating prefix if
        # their plain names turn out to collide with another chain's (e.g.
        # recall_db(i)%org_min and %pest are both `type
        # constituent_file_data`, so both flatten to name/units/tstep).
        chain_groups: list[tuple[int, int, str]] = []
        for base, chain, last_is_element in parsed:
            vartype = self.resolve_var_type(base, proc)
            type_name = derived_type_name(vartype)
            if chain:
                has_component_access = True
                if not type_name:
                    return None, f"unresolved type for '{base}' in read"
                dtype = self.types_by_name.get(type_name)
                if dtype is None:
                    return None, f"unknown derived type '{type_name}'"
                primary_type = primary_type or type_name
                sub = self._resolve_component_chain(dtype, chain, last_is_element=last_is_element)
                if sub is None:
                    return None, f"unresolved component {base}%{'%'.join(chain)}"
                start = len(fields)
                fields.extend(sub)
                if len(sub) > 1:
                    chain_groups.append((start, len(fields), chain[-1]))
            elif type_name and type_name in self.types_by_name:
                primary_type = primary_type or type_name
                sub = self.flatten_type(type_name)
                if sub is None:
                    return None, f"could not flatten derived type '{type_name}'"
                fields.extend(sub)
            else:
                # An intrinsic scalar/array column mixed into a data read
                # (e.g. ``pl_class(ic)`` alongside ``pldb(ic)``).
                fields.append(
                    FieldSpec(
                        fortran_name=base,
                        fortran_type=base_type_word(vartype),
                        numeric=is_numeric_type(vartype),
                        units=None,
                        doc=None,
                    )
                )

        # Sibling %chains of the same type (recall_db(i)%org_min, %pest, ...)
        # flatten to identically-named columns -- "name"/"units"/"tstep" each
        # appearing once per sibling. Only prefix when a real collision shows
        # up, so unambiguous reads (the common case) keep their plain names.
        names = [f.fortran_name for f in fields]
        if chain_groups and len(set(names)) != len(names):
            for start, end, label in chain_groups:
                for i in range(start, end):
                    fields[i].fortran_name = f"{label}.{fields[i].fortran_name}"

        pattern = "field_list" if has_component_access else "derived_type"
        type_source = None
        if primary_type and primary_type in self.types_by_name:
            type_source = self.types_by_name[primary_type].location.label()
        return (
            ReadSchema(
                fields=fields,
                pattern=pattern,
                base_type=primary_type,
                type_source=type_source,
                reader_line=io_op.location.line,
            ),
            None,
        )

    def _resolve_field_token(
        self,
        base: str,
        chain: list[str],
        proc: ProcedureDoc,
        *,
        last_is_element: bool = False,
    ) -> tuple[list[FieldSpec], str | None, str | None]:
        """Resolve one already-split ``(base, %chain)`` field token to column(s).

        The same derived-type / flatten / plain-scalar logic as the main loop
        in :meth:`read_to_schema`, factored out so
        :meth:`resolve_variable_length_read` can apply it to both a record's
        fixed prefix and its repeat group without duplicating the resolution
        rules (only the token-splitting boilerplate around it differs).

        ``last_is_element`` marks that the read subscripted the final component
        to a single array element (see :meth:`_fields_from_component`); pass it
        when the caller knows this, so a fixed-size array read one element at a
        time isn't expanded to its full declared width.

        Returns ``(fields, type_name_or_None, error_reason_or_None)``; on
        error ``fields`` is empty.
        """
        vartype = self.resolve_var_type(base, proc)
        type_name = derived_type_name(vartype)
        if chain:
            if not type_name:
                return [], None, f"unresolved type for '{base}' in read"
            dtype = self.types_by_name.get(type_name)
            if dtype is None:
                return [], None, f"unknown derived type '{type_name}'"
            sub = self._resolve_component_chain(dtype, chain, last_is_element=last_is_element)
            if sub is None:
                return [], None, f"unresolved component {base}%{'%'.join(chain)}"
            return sub, type_name, None
        if type_name and type_name in self.types_by_name:
            sub = self.flatten_type(type_name)
            if sub is None:
                return [], None, f"could not flatten derived type '{type_name}'"
            return sub, type_name, None
        return (
            [
                FieldSpec(
                    fortran_name=base,
                    fortran_type=base_type_word(vartype),
                    numeric=is_numeric_type(vartype),
                    units=None,
                    doc=None,
                )
            ],
            None,
            None,
        )

    def _resolve_read_fields(
        self, io_op: IOOperation, proc: ProcedureDoc
    ) -> tuple[list[FieldSpec] | None, str | None, str | None]:
        """Resolve every field token of one read into a flat column list.

        Returns ``(fields, primary_type, error)``. A read that isn't a plain
        list of field tokens (an implied-do, an unparseable token) returns
        ``(None, None, None)`` -- not this shape -- rather than an error.
        """
        fields: list[FieldSpec] = []
        primary_type: str | None = None
        for raw in io_op.fields:
            match = _FIELD_RE.match(raw.strip())
            if match is None:
                return None, None, None
            base = match.group(1)
            chain, last_is_element = _parse_component_chain(match.group(2) or "")
            sub, type_name, err = self._resolve_field_token(
                base, chain, proc, last_is_element=last_is_element
            )
            if err:
                return None, None, err
            primary_type = primary_type or type_name
            fields.extend(sub)
        return fields, primary_type, None

    def resolve_multi_record_block(
        self, block: _IOBlock, proc: ProcedureDoc
    ) -> tuple[MultiRecordSchema | None, str | None]:
        """Resolve a header-record-plus-sub-blocks file to its schema.

        The shape (verified against ``soils.sol``, ``plant.ini``, and
        ``weather-wgn.cli``): inside the per-entry loop, a *header* read names
        several components of a derived-type instance
        (``soildb(isol)%s%...``), and one or more *sub-block* reads name
        components of that same instance (``soildb(isol)%ly(j)%...``) from
        inside a further ``do`` loop.

        Detected structurally, not by filename. A *sub-block* is a single-root
        component read inside a ``do`` loop; it pairs with a *header* read that
        also names that same root and sits no deeper than it, in one of two
        ways -- the block's count comes from either:

        * a **header column** -- the sub's ``do`` bound resolves (via
          :func:`_find_count_field`, directly or through a traced assignment
          like ``mlyr = soildb(isol)%s%nly``) to one of the header's columns;
          or
        * a **compile-time literal** -- the bound is an integer constant
          (``do mo = 1, 12``); here the header must be *strictly* shallower and
          earlier in source, since there's no count column tying the two
          together, only their nesting.

        The header need not be the widest read (soils.sol's 14-column layer is
        wider than its 7-column header) and may span more than one root
        instance (weather-wgn.cli's ``wgn_n(iwgn), wgn(iwgn)%lat, ...``); it is
        the richest read that supplies a count for at least one sub-block. A
        block with no such pairing is simply not this shape -- declined.

        Two further wrinkles, both verified against ``management.sch``:

        * a sub-block read may live in a *called helper* that reads the same
          open unit (``call read_mgtops(isched)``); such reads are pulled in as
          candidate sub-blocks, still gated by the same count-to-header-column
          linkage;
        * several reads may share a sub-block -- a base read plus keyed
          backspace re-reads of a wider row for certain first-column values
          (``pl_hv_summer1`` -> extra crop columns). Reads that share a header,
          root, first column, and count collapse into one block; if their
          widths disagree the block is ``variable_width`` and carries only the
          guaranteed (narrowest) columns.

        A fourth, verified against ``calibration.cal``: a sub-block whose rows
        are a genuinely *different* shape depending on the row's own leading
        value (not just wider, but different fields entirely) -- an ``if
        (<peek> == "<literal>") then`` / ``else`` pair of reads (see
        :func:`_find_if_else_read_pairs`), gated by the same count-to-header
        linkage as any other sub-block. Produces a ``tag_field`` block with two
        :class:`TaggedRowVariant`\\ s rather than a plain ``row_fields`` list.

        If the chosen header read is itself the peek half of a peek-and-
        backspace pair whose full re-read carries an implied-do tail (the
        ``chan-surf.lin`` idiom -- see
        :meth:`resolve_variable_length_read`/``_peek_bound_count_field``), the
        fuller, repeat-aware resolution is used for ``header_fields`` instead,
        and the repeat group is carried as ``header_repeat`` -- otherwise a
        header that is itself variable-length would silently look fixed-width.
        """
        reads = self._multi_record_candidate_reads(block, proc)

        # (sub_op, sub_root, sub_fields, header_read, count_field|None, count_literal|None)
        Pairing = tuple[IOOperation, str, list[FieldSpec], Read, str | None, int | None]
        pairings: list[Pairing] = []
        for sub_op, sub_roots, _sp, sub_fields, sub_depth in reads:
            component_roots = {base.lower() for base, chain in _sp if chain}
            if len(component_roots) == 1:
                root = next(iter(component_roots))
            elif len(sub_roots) == 1:
                root = next(iter(sub_roots))
            else:
                continue  # a repeated record is one instance
            bound = _innermost_do_bound(sub_op)
            if bound is None:
                continue
            is_literal = bound.strip().isdigit()
            for header in reads:
                h_op, h_roots, h_parsed, h_fields, h_depth = header
                if h_op is sub_op or root not in h_roots:
                    continue
                if is_literal:
                    if h_depth < sub_depth and h_op.location.line < sub_op.location.line:
                        pairings.append((sub_op, root, sub_fields, header, None, int(bound)))
                        break
                    continue
                if h_depth > sub_depth:
                    continue
                count_name = self._header_count_column(bound, root, h_parsed, h_fields, proc)
                if count_name is not None:
                    pairings.append((sub_op, root, sub_fields, header, count_name, None))

        # A read that's half of an if/else tag dispatch (calibration.cal's
        # else-branch read, `cal_upd(i)%cond(icond)`) can ALSO independently
        # satisfy the plain single-read pairing above -- it IS a valid
        # ordinary component read, just one that belongs to a tagged variant
        # instead. Exclude both halves from ordinary pairing up front, so a
        # tagged block's rows never also show up as a second, plain block.
        if_else_pairs = _find_if_else_read_pairs(block.reads)
        branch_op_ids = {id(op) for pair in if_else_pairs for op in pair[:2]}
        pairings = [p for p in pairings if id(p[0]) not in branch_op_ids]

        # (if_op, root, discriminator, count_field, variants, header_read)
        TaggedPairing = tuple[IOOperation, str, str, str, list[TaggedRowVariant], Read]
        tagged_pairings: list[TaggedPairing] = []
        for if_op, else_op, discriminator, literal in if_else_pairs:
            if_parsed = _split_field_tokens(if_op.fields)
            else_parsed = _split_field_tokens(else_op.fields)
            if if_parsed is None or else_parsed is None:
                continue
            if_fields, _t1, err1 = self._resolve_read_fields(if_op, proc)
            else_fields, _t2, err2 = self._resolve_read_fields(else_op, proc)
            if err1 or err2 or not if_fields or not else_fields:
                continue
            roots = {b.lower() for b, c in if_parsed if c} | {b.lower() for b, c in else_parsed if c}
            if len(roots) != 1:
                continue
            root = next(iter(roots))
            bound = _innermost_do_bound(if_op)
            if bound is None or bound.strip().isdigit():
                continue  # a literal-count tagged block is unverified; decline
            sub_depth = _do_depth(if_op)
            for header in reads:
                h_op, h_roots, h_parsed, h_fields, h_depth = header
                if root not in h_roots or h_depth > sub_depth:
                    continue
                count_name = self._header_count_column(bound, root, h_parsed, h_fields, proc)
                if count_name is not None:
                    variants = [
                        TaggedRowVariant(tag=literal, fields=if_fields),
                        TaggedRowVariant(tag="other", fields=else_fields),
                    ]
                    tagged_pairings.append((if_op, root, discriminator, count_name, variants, header))
                    break

        if not pairings and not tagged_pairings:
            return None, None

        # The header is the richest read that supplies a count for a sub.
        candidate_headers = [p[3] for p in pairings] + [t[5] for t in tagged_pairings]
        header = max(candidate_headers, key=lambda r: len(r[3]))
        header_op, _hr, _hp, header_fields, _hd = header

        blocks = self._collapse_multi_record_blocks(
            [p for p in pairings if p[3][0] is header_op], proc, block.reads
        )
        for _if_op, _root, discriminator, count_name, variants, hdr in tagged_pairings:
            if hdr[0] is header_op:
                blocks.append(
                    MultiRecordBlock(count_field=count_name, tag_field=discriminator, variants=variants)
                )
        if not blocks:
            return None, None

        header_repeat: RepeatGroup | None = None
        for sib in block.reads:
            if sib is header_op or sib.kind != "read":
                continue
            tokens = [t.strip() for t in sib.fields]
            if not tokens or _parse_implied_do(tokens[-1]) is None:
                continue
            if _do_depth(sib) != _do_depth(header_op):
                continue
            full_schema, _reason = self.resolve_variable_length_read(sib, proc, block.reads)
            if (
                full_schema is not None
                and full_schema.repeat is not None
                and len(full_schema.fields) == len(header_op.fields)
            ):
                header_fields = full_schema.fields
                header_repeat = full_schema.repeat
                break

        return (
            MultiRecordSchema(
                header_fields=header_fields,
                blocks=blocks,
                reader=proc.location.path,
                reader_line=header_op.location.line,
                header_repeat=header_repeat,
            ),
            None,
        )

    def _multi_record_candidate_reads(
        self, block: _IOBlock, proc: ProcedureDoc
    ) -> list[Read]:
        """Component-access reads of ``block`` plus those of called helpers.

        A header spans >= 1 root; a sub-record names exactly one instance root.
        Besides the block's own reads, this pulls in reads from procedures the
        block's procedure ``call``s that read the *same* open unit (e.g.
        ``read_mgtops`` reading unit 107). Imported reads get a sentinel depth
        deeper than any real header so they always qualify as sub-blocks by
        nesting; their correctness still rests on the count-to-header-column
        linkage applied later, not on where they physically live.
        """
        def collect(op: IOOperation, resolve_proc: ProcedureDoc, depth: int) -> Read | None:
            parsed = _split_field_tokens(op.fields)
            if parsed is None or not any(chain for _, chain in parsed):
                return None
            fields, _ptype, err = self._resolve_read_fields(op, resolve_proc)
            if err or not fields:
                return None
            return (op, {b.lower() for b, _ in parsed}, parsed, fields, depth)

        reads: list[Read] = []
        for op in block.reads:
            read = collect(op, proc, _do_depth(op))
            if read is not None:
                reads.append(read)

        unit = block.open.unit if block.open else None
        if unit:
            called = {c.name.split("%")[0].lower() for c in proc.calls if c.kind == "subroutine"}
            for helper in self.project.procedures:
                if helper.name.lower() not in called:
                    continue
                for op in helper.io:
                    if op.kind == "read" and op.unit == unit:
                        read = collect(op, helper, _IMPORTED_READ_DEPTH)
                        if read is not None:
                            reads.append(read)
        return reads

    def _header_count_column(
        self,
        bound: str,
        root: str,
        header_parsed: list[tuple[str, list[str]]],
        header_fields: list[FieldSpec],
        proc: ProcedureDoc,
    ) -> str | None:
        """The header column (if any) that supplies a sub-block's ``do`` count.

        Two linkages: the bound is a bare/traced local resolving to a header
        column (:func:`_find_count_field`, soils.sol's ``mlyr``), or the bound
        is itself a ``root%...%col`` chain whose leaf is a header column of that
        same root (management.sch's ``do iop = 1, sched(isched)%num_ops``).
        """
        h_names = {f.fortran_name.lower(): f.fortran_name for f in header_fields}
        count_field = _find_count_field(bound, header_parsed, proc)
        if count_field and count_field.lower() in h_names:
            return h_names[count_field.lower()]
        match = _FIELD_RE.match(bound.strip())
        if match and match.group(1).lower() == root:
            chain, _last = _parse_component_chain(match.group(2) or "")
            if chain and chain[-1].lower() in h_names:
                return h_names[chain[-1].lower()]
        return None

    def _collapse_multi_record_blocks(
        self, pairings: list, proc: ProcedureDoc, block_reads: list[IOOperation]
    ) -> list[MultiRecordBlock]:
        """Fold sub-block reads that describe the same block into one block each.

        Reads that share a root, first column, and count are the same block
        seen more than once -- a base read and its keyed backspace re-reads.
        They collapse to one block; a width disagreement among them marks the
        block ``variable_width`` and keeps only the common (narrowest) columns.
        If a sibling reread exposes a richer prefix + repeat + suffix row shape,
        prefer that over the narrow probe read.
        """
        groups: dict[tuple, list] = {}
        order: list[tuple] = []
        for sub_op, root, sub_fields, _hdr, count_name, count_lit in pairings:
            key = (root, sub_fields[0].fortran_name.lower(), count_name, count_lit)
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append((sub_op, sub_fields))
        blocks: list[MultiRecordBlock] = []
        for key in sorted(order, key=lambda k: min(op.location.line for op, _ in groups[k])):
            _root, _first, count_name, count_lit = key
            variants = groups[key]
            structured = self._find_embedded_repeat_multi_record_row(
                root=_root,
                first_field=_first,
                count_name=count_name,
                count_lit=count_lit,
                variant_ops=[op for op, _ in variants],
                proc=proc,
                block_reads=block_reads,
            )
            if structured is not None:
                prefix_fields, repeat, suffix_fields = structured
                blocks.append(
                    MultiRecordBlock(
                        row_fields=prefix_fields,
                        count_field=count_name,
                        count_literal=count_lit,
                        row_repeat=repeat,
                        row_suffix_fields=suffix_fields,
                    )
                )
                continue
            widths = {len(f) for _op, f in variants}
            narrowest = min((f for _op, f in variants), key=len)
            blocks.append(
                MultiRecordBlock(
                    row_fields=narrowest,
                    count_field=count_name,
                    count_literal=count_lit,
                    variable_width=len(widths) > 1,
                )
            )
        return blocks

    def _find_embedded_repeat_multi_record_row(
        self,
        *,
        root: str,
        first_field: str,
        count_name: str | None,
        count_lit: int | None,
        variant_ops: list[IOOperation],
        proc: ProcedureDoc,
        block_reads: list[IOOperation],
    ) -> tuple[list[FieldSpec], RepeatGroup, list[FieldSpec]] | None:
        """Find a sibling reread whose row has prefix + repeat + suffix shape."""

        depths = {_do_depth(op) for op in variant_ops}
        if len(depths) != 1:
            return None
        bounds = {_innermost_do_bound(op) for op in variant_ops}
        if len(bounds) != 1:
            return None
        target_depth = next(iter(depths))
        target_bound = next(iter(bounds))
        best: tuple[list[FieldSpec], RepeatGroup, list[FieldSpec]] | None = None
        best_width = -1
        for candidate in block_reads:
            if candidate.kind != "read":
                continue
            if _do_depth(candidate) != target_depth:
                continue
            if _innermost_do_bound(candidate) != target_bound:
                continue
            resolved = self._resolve_embedded_repeat_row(candidate, proc)
            if resolved is None:
                continue
            candidate_root, prefix_fields, repeat, suffix_fields = resolved
            if candidate_root != root or not prefix_fields:
                continue
            if prefix_fields[0].fortran_name.lower() != first_field:
                continue
            if count_lit is not None:
                pass
            if count_name is not None and repeat.count_field.lower() == count_name.lower():
                continue
            width = len(prefix_fields) + len(repeat.fields) + len(suffix_fields)
            if width > best_width:
                best = (prefix_fields, repeat, suffix_fields)
                best_width = width
        return best

    def _resolve_embedded_repeat_row(
        self, io_op: IOOperation, proc: ProcedureDoc
    ) -> tuple[str, list[FieldSpec], RepeatGroup, list[FieldSpec]] | None:
        """Resolve one read containing a mid-row implied-do plus a trailing suffix."""

        tokens = [t.strip() for t in io_op.fields]
        implied_indexes = [i for i, token in enumerate(tokens) if _IMPLIED_DO_RE.match(token)]
        if len(implied_indexes) != 1:
            return None
        repeat_index = implied_indexes[0]
        if repeat_index == 0 or repeat_index == len(tokens) - 1:
            return None

        prefix_tokens = tokens[:repeat_index]
        suffix_tokens = tokens[repeat_index + 1 :]
        prefix_parsed = _split_field_tokens(prefix_tokens)
        suffix_parsed = _split_field_tokens(suffix_tokens)
        if prefix_parsed is None or suffix_parsed is None:
            return None

        parsed_impl = _parse_implied_do(tokens[repeat_index])
        if parsed_impl is None:
            return None
        items, _loop_var, _lo, hi = parsed_impl
        repeat_parsed = _split_field_tokens(items)
        if repeat_parsed is None:
            return None

        component_roots = {
            base.lower()
            for base, chain in (prefix_parsed + repeat_parsed + suffix_parsed)
            if chain
        }
        if len(component_roots) != 1:
            return None
        root = next(iter(component_roots))

        prefix_fields: list[FieldSpec] = []
        for base, chain in prefix_parsed:
            sub, _type_name, err = self._resolve_field_token(base, chain, proc)
            if err:
                return None
            prefix_fields.extend(sub)

        count_field = _find_count_field(hi, prefix_parsed, proc)
        if count_field is None:
            return None

        repeat_fields: list[FieldSpec] = []
        for base, chain in repeat_parsed:
            sub, _type_name, err = self._resolve_field_token(base, chain, proc)
            if err:
                return None
            repeat_fields.extend(sub)
        if not repeat_fields:
            return None

        suffix_fields: list[FieldSpec] = []
        for base, chain in suffix_parsed:
            sub, _type_name, err = self._resolve_field_token(base, chain, proc)
            if err:
                return None
            suffix_fields.extend(sub)
        if not suffix_fields:
            return None

        return (
            root,
            prefix_fields,
            RepeatGroup(fields=repeat_fields, count_field=count_field, count_expr=hi),
            suffix_fields,
        )

    def resolve_variable_length_read(
        self, io_op: IOOperation, proc: ProcedureDoc, siblings: list[IOOperation] | None = None
    ) -> tuple[ReadSchema | None, str | None]:
        """Resolve a record whose last field is an implied-do repeat group.

        A record like ``k, name, area_ha, nspu, (elem_cnt(isp), isp = 1,
        nspu)`` has a fixed prefix followed by a variable number of repeats.
        This is only resolved when the repeat count is provably a value
        already read in this same record -- see :func:`_find_count_field` -- or,
        when ``siblings`` is given, provably read by an earlier peek read into
        the column that lines up with the record's last fixed field (see
        :meth:`_peek_bound_count_field`, the ``chan-surf.lin`` idiom).
        Anything else -- an externally-governed count, more than one repeat
        group, an unparseable implied-do -- is reported unresolved (or
        silently declined as "not this shape") rather than guessed, matching
        this module's rule that a wrong schema is worse than a missing one.
        """
        tokens = [t.strip() for t in io_op.fields]
        if not tokens or not _IMPLIED_DO_RE.match(tokens[-1]):
            return None, None
        if any(_IMPLIED_DO_RE.match(t) for t in tokens[:-1]):
            return None, "more than one repeat group in a single record"

        prefix_parsed = _split_field_tokens(tokens[:-1])
        if prefix_parsed is None:
            return None, None

        parsed_impl = _parse_implied_do(tokens[-1])
        if parsed_impl is None:
            return None, None
        items, _loop_var, _lo, hi = parsed_impl

        prefix_fields: list[FieldSpec] = []
        primary_type: str | None = None
        for base, chain in prefix_parsed:
            sub, type_name, err = self._resolve_field_token(base, chain, proc)
            if err:
                return None, err
            primary_type = primary_type or type_name
            prefix_fields.extend(sub)

        count_field = _find_count_field(hi, prefix_parsed, proc)
        if count_field is None and siblings is not None:
            count_field = self._peek_bound_count_field(
                hi, prefix_parsed, prefix_fields, io_op, siblings
            )
        if count_field is None:
            return None, f"repeat count '{hi}' is not a field already read in this record"

        repeat_parsed = _split_field_tokens(items)
        if repeat_parsed is None:
            return None, None

        repeat_fields: list[FieldSpec] = []
        for base, chain in repeat_parsed:
            sub, type_name, err = self._resolve_field_token(base, chain, proc)
            if err:
                return None, err
            primary_type = primary_type or type_name
            repeat_fields.extend(sub)

        if not repeat_fields:
            return None, None

        type_source = None
        if primary_type and primary_type in self.types_by_name:
            type_source = self.types_by_name[primary_type].location.label()
        return (
            ReadSchema(
                fields=prefix_fields,
                pattern="field_list",
                base_type=primary_type,
                type_source=type_source,
                reader_line=io_op.location.line,
                repeat=RepeatGroup(
                    fields=repeat_fields, count_field=count_field, count_expr=hi
                ),
            ),
            None,
        )

    def _peek_bound_count_field(
        self,
        hi: str,
        prefix_parsed: list[tuple[str, list[str]]],
        prefix_fields: list[FieldSpec],
        io_op: IOOperation,
        siblings: list[IOOperation],
    ) -> str | None:
        """Bind an implied-do count read by an earlier *peek* of the record.

        SWAT+'s ``chan-surf.lin`` / ``calibration.cal`` idiom reads a record's
        fixed prefix once to learn the repeat count (``read ... , nspu``), then
        ``backspace``es and re-reads the whole record with the implied-do tail.
        The count variable (``nspu``) is a throwaway local, so it isn't one of
        the record's own fields -- but because the peek and the full read scan
        the *same physical line*, the peek's last token sits in the very column
        the full record's last fixed field occupies (``obj_tot`` / ``num_tot``).

        So bind the count to that last prefix field when a sibling read exists
        whose columns line up with this record's fixed prefix (same scalar
        field count) and whose last token is exactly the bound variable. The
        strict length + last-token match keeps this from firing on unrelated
        reads. Returns the field name, or None.
        """
        # Only a scalar prefix has a clean column<->field alignment.
        if len(prefix_parsed) != len(prefix_fields) or not prefix_fields:
            return None
        hi_lower = hi.strip().lower()
        for sib in siblings:
            if sib is io_op:
                continue
            sib_tokens = [t.strip() for t in sib.fields]
            if len(sib_tokens) != len(prefix_fields):
                continue
            if any(_IMPLIED_DO_RE.match(t) for t in sib_tokens):
                continue
            last = _split_field_tokens([sib_tokens[-1]])
            if last is None:
                continue
            last_base, last_chain = last[0]
            last_name = (last_chain[-1] if last_chain else last_base).lower()
            if last_name == hi_lower:
                return prefix_fields[-1].fortran_name
        return None

    def resolve_positional_extraction(
        self, block: _IOBlock, proc: ProcedureDoc
    ) -> tuple[ReadSchema | None, str | None]:
        """Resolve a hand-parsed record from its column-by-column reads.

        Some input files are never read with a single list-directed
        statement at all: the reader takes each row into a text buffer
        (``read(unit,'(a)') buf``), splits it into a character array (``call
        split_line(buf, fields_array, n)``), then reads each column back out
        one at a time -- ``read(fields_array(1),*) id``,
        ``read(fields_array(2),*) name``, and so on. Each such internal read
        (unit is a parenthesized array-element expression, never a real file
        unit) names exactly one column; this collects them into one ordered
        schema. A column occasionally comes from a plain assignment instead
        of a read (SWAT+ does this for at least one string column per
        hand-parsed file, e.g. ``cell_name(i) = trim(split_fields(2))``) --
        picked up the same way, by scanning assignments in the same source
        range for the same array.

        Only resolved when every internal read in the block uses the same
        array and a literal column index, and no two reads or assignments
        claim the same column with different targets. A computed index
        (``fields_array(2+j)``) signals a data-dependent repeat group --out
        of scope here, same as :meth:`resolve_variable_length_read`'s
        implied-do case. Declined, not guessed, when that happens.

        Conflicting targets at the same column are not automatically fatal,
        though: if every conflicting read sits in its own ``case
        ('literal')`` branch of a ``select case`` whose subject is another
        column of this same record (``outputs.gw``'s rows, tagged
        ``'head_output_time'`` / ``'observation_cell'`` / etc. by column 1),
        that is a *keyed* column, not an unresolvable conflict -- see
        :meth:`_resolve_tagged_positional_column`. Anything else about the
        conflict still declines.
        """
        internal = [op for op in block.reads if op.unit and "(" in op.unit]
        if not internal:
            return None, None

        array_names: set[str] = set()
        column_reads: dict[int, list[IOOperation]] = {}
        for op in internal:
            match = _INTERNAL_READ_UNIT_RE.match(op.unit or "")
            if not match:
                return None, None
            array_names.add(match.group(1).lower())
            if len(op.fields) != 1:
                return None, None
            column_reads.setdefault(int(match.group(2)), []).append(op)

        if len(array_names) != 1:
            return None, None
        array_name = next(iter(array_names))

        columns: dict[int, str] = {}
        tagged: tuple[int, str, list[TaggedRowVariant]] | None = None
        conflict_reason: str | None = None
        for index, ops in column_reads.items():
            targets = {op.fields[0] for op in ops}
            if len(targets) == 1:
                columns[index] = ops[0].fields[0]
                continue
            resolved_tag = (
                self._resolve_tagged_positional_column(index, ops, array_name, proc)
                if tagged is None
                else None
            )
            if resolved_tag is not None:
                tagged = resolved_tag
                continue
            conflict_reason = f"column {index} has conflicting targets in the same record"
        if tagged is None and conflict_reason:
            return None, conflict_reason

        lines = [op.location.line for op in internal]
        assigned = _positional_assignment_targets(proc, array_name, min(lines), max(lines))
        for index, target in assigned.items():
            if index in columns and columns[index] != target:
                return None, f"column {index} has conflicting targets in the same record"
            columns.setdefault(index, target)

        if len(columns) < 2 and tagged is None:
            return None, None

        fields: list[FieldSpec] = []
        primary_type: str | None = None
        for index in sorted(columns):
            match = _FIELD_RE.match(columns[index].strip())
            if not match:
                return None, None
            base = match.group(1)
            chain_text = match.group(2) or ""
            chain = [
                re.sub(r"\([^()]*\)", "", part).strip()
                for part in chain_text.split("%")
                if part.strip()
            ]
            sub, type_name, err = self._resolve_field_token(base, chain, proc)
            if err:
                return None, err
            primary_type = primary_type or type_name
            fields.extend(sub)

        type_source = None
        if primary_type and primary_type in self.types_by_name:
            type_source = self.types_by_name[primary_type].location.label()
        tag_field, variants = (tagged[1], tagged[2]) if tagged else (None, [])
        return (
            ReadSchema(
                fields=fields,
                pattern="positional",
                base_type=primary_type,
                type_source=type_source,
                reader_line=internal[0].location.line,
                tag_field=tag_field,
                variants=variants,
            ),
            None,
        )

    def _resolve_tagged_positional_column(
        self, index: int, ops: list[IOOperation], array_name: str, proc: ProcedureDoc
    ) -> tuple[int, str, list[TaggedRowVariant]] | None:
        """Resolve a positional column whose target depends on another
        column's value, via the source's own ``select case`` dispatch.

        Each op in ``ops`` reads the same column into a different target;
        this resolves when every one of them sits in its own ``case
        ('literal')`` branch of a ``select case`` whose subject is
        ``<array_name>(<key_index>)`` for some *other* column of this same
        record, and the branches' literals are all real entries of that
        select's own captured vocabulary (:class:`SelectCaseDoc`, scoped by
        line proximity since a shared procedure can hold several unrelated
        selects on the same expression -- e.g. a counting pre-pass with a
        narrower vocabulary than the real read). Declines (returns None)
        rather than guess if the dispatch doesn't match this shape exactly.
        """
        subject_re = re.compile(rf"^{re.escape(array_name)}\(\s*(\d+)\s*\)$", re.I)
        by_label: dict[str, IOOperation] = {}
        key_index: int | None = None
        for op in ops:
            tail = (op.condition or "").rsplit(">", 1)[-1].strip()
            if " / " not in tail:
                return None
            select_text, case_text = tail.rsplit(" / ", 1)
            case_match = re.match(r"^case\s*\((.*)\)$", case_text.strip(), re.I)
            if case_match is None:
                return None
            literals = STRING_LITERAL_RE.findall(case_match.group(1))
            if len(literals) != 1:
                return None  # a multi-value case ('a', 'b') isn't this simple shape
            select_match = re.match(r"^select\s+case\s*\((.*)\)$", select_text.strip(), re.I)
            if select_match is None:
                return None
            subj_match = subject_re.match(_unwrap_trim_adjustl(select_match.group(1)))
            if subj_match is None:
                return None
            this_key_index = int(subj_match.group(1))
            if key_index is None:
                key_index = this_key_index
            elif key_index != this_key_index:
                return None  # different dispatch keys -- not one coherent tag
            label = literals[0]
            if label in by_label and by_label[label].fields[0] != op.fields[0]:
                return None
            by_label[label] = op
        if key_index is None or key_index == index:
            return None

        vocabulary = self._select_case_vocabulary_near(
            proc, f"{array_name}({key_index})", [op.location.line for op in ops]
        )
        if not vocabulary or not set(by_label).issubset(set(vocabulary)):
            return None

        variants: list[TaggedRowVariant] = []
        for label in vocabulary:
            op = by_label.get(label)
            if op is None:
                continue
            match = _FIELD_RE.match(op.fields[0].strip())
            if not match:
                return None
            chain, last_is_element = _parse_component_chain(match.group(2) or "")
            sub, _type_name, err = self._resolve_field_token(
                match.group(1), chain, proc, last_is_element=last_is_element
            )
            if err or len(sub) != 1:
                return None
            variants.append(TaggedRowVariant(tag=label, fields=sub))
        if not variants:
            return None
        return index, f"{array_name}({key_index})", variants

    def _select_case_vocabulary_near(
        self, proc: ProcedureDoc, subject_expr: str, near_lines: list[int]
    ) -> list[str] | None:
        """The case labels of the select-case on ``subject_expr`` closest to
        (and preceding) ``near_lines``.

        ``ProcedureDoc.select_cases`` is flat across the whole procedure, so
        a shared reader can hold more than one select on the identical
        subject text (a counting pre-pass, then the real read, each with its
        own vocabulary) -- picking by subject text alone risks the wrong
        one. The select-case statement always precedes the reads inside it,
        so the closest preceding match by line is the enclosing one.
        """
        target = subject_expr.replace(" ", "").lower()
        floor = min(near_lines)
        best: SelectCaseDoc | None = None
        for sc in proc.select_cases:
            if _unwrap_trim_adjustl(sc.subject or "").replace(" ", "").lower() != target:
                continue
            if sc.location.line > floor:
                continue
            if best is None or sc.location.line > best.location.line:
                best = sc
        return best.cases if best else None

    def resolve_decision_table_block(
        self, block: _IOBlock, proc: ProcedureDoc
    ) -> tuple[DecisionTableSchema | None, str | None]:
        """Resolve a decision-table (``*.dtl``) reader's block to its schema.

        Verified structurally, not by procedure or filename: a header read
        of exactly ``name, conds, alts, acts`` off one array variable, then
        exactly two implied-do reads off the same variable (a condition row
        + its ``alts``-driven alt tail, then an action row + its
        ``alts``-driven outcome tail, in that source order -- true in all
        four ``.dtl`` readers). Anything else about the block -- extra
        reads, a different header shape -- is simply not this pattern, so
        this declines (``None, None``) rather than guess; only a match on
        the header shape that then fails to resolve a component is reported
        as an actual error.
        """
        # Deliberately not `_IMPLIED_DO_RE` here: its bound-matching group
        # (`[^,)]+`) can't contain its own `)`, so it rejects an implied-do
        # whose bound is a %chain with an index, e.g. `dtbl_lum(i)%alts` --
        # exactly this file's shape. `_parse_implied_do` itself handles it
        # fine (it splits on top-level commas, paren-depth aware), so use
        # its success as the gate instead of the regex pre-filter.
        implied_do_ops = [
            op for op in block.reads if op.fields and _parse_implied_do(op.fields[-1].strip())
        ]
        if len(implied_do_ops) != 2:
            return None, None
        cond_op, act_op = implied_do_ops

        def _row_base(op: IOOperation) -> str | None:
            if len(op.fields) != 2:
                return None
            match = _FIELD_RE.match(op.fields[0].strip())
            return match.group(1).lower() if match else None

        cond_base, act_base = _row_base(cond_op), _row_base(act_op)
        if not cond_base or cond_base != act_base:
            return None, None
        array_name = cond_base

        header_op = next(
            (
                op
                for op in block.reads
                if op is not cond_op
                and op is not act_op
                and len(op.fields) == 4
                and all(
                    (m := _FIELD_RE.match(f.strip())) and m.group(1).lower() == array_name
                    for f in op.fields
                )
            ),
            None,
        )
        if header_op is None:
            return None, None

        header_fields: list[FieldSpec] = []
        for raw in header_op.fields:
            match = _FIELD_RE.match(raw.strip())
            chain = [
                re.sub(r"\([^()]*\)", "", part).strip()
                for part in (match.group(2) or "").split("%")
                if part.strip()
            ]
            sub, _type_name, err = self._resolve_field_token(array_name, chain, proc)
            if err:
                return None, err
            header_fields.extend(sub)
        expected = ["name", "conds", "alts", "acts"]
        if [f.fortran_name.lower() for f in header_fields] != expected:
            return None, None
        header_by_name = {f.fortran_name.lower(): f.fortran_name for f in header_fields}

        condition_block = self._resolve_decision_table_row_block(
            cond_op, array_name, header_by_name, "conds", proc
        )
        if isinstance(condition_block, str):
            return None, condition_block
        action_block = self._resolve_decision_table_row_block(
            act_op, array_name, header_by_name, "acts", proc
        )
        if isinstance(action_block, str):
            return None, action_block

        # The COND_VAR vocabulary isn't in any *.dtl reader -- it's runtime
        # dispatch, shared by every decision-table type, in the single
        # `conditions` subroutine every table-driven control routine calls
        # (hru_control, res_control, wallo_demand, ...). Scoped to that one
        # procedure by name: a pattern-only search across every procedure
        # picked up `cal_conditions`' unrelated 8-value dispatch first
        # (same %cond(..)%var subject shape, alphabetically earlier file).
        condition_vocab = self._select_case_vocabulary(
            [p for p in self.project.procedures if p.name.lower() == "conditions"],
            r"%cond\([^)]*\)%var\s*$",
        )
        reader_cases = [
            sc for sc in proc.select_cases if sc.subject and re.search(r"%act\([^)]*\)%typ\s*$", sc.subject, re.I)
        ]
        action_vocab = reader_cases[0].cases if reader_cases else []
        exclude_ids = {id(sc) for sc in reader_cases}
        other = [(sc.subject, sc.cases) for sc in proc.select_cases if id(sc) not in exclude_ids]

        return (
            DecisionTableSchema(
                header_fields=header_fields,
                condition_block=condition_block,
                action_block=action_block,
                condition_vocabulary=condition_vocab,
                action_vocabulary=action_vocab,
                other_vocabularies=other,
                reader=proc.location.path,
                reader_line=header_op.location.line,
            ),
            None,
        )

    def _resolve_decision_table_row_block(
        self,
        op: IOOperation,
        array_name: str,
        header_by_name: dict[str, str],
        row_count_name: str,
        proc: ProcedureDoc,
    ) -> DecisionTableBlock | str:
        """Resolve one implied-do read into a :class:`DecisionTableBlock`.

        Returns the block, or a ``str`` error reason (never ``None`` -- the
        caller already knows this op is meant to be a decision-table row by
        the time it gets here).
        """
        if row_count_name not in header_by_name:
            return f"decision table header has no '{row_count_name}' field"
        row_match = _FIELD_RE.match(op.fields[0].strip())
        if row_match is None:
            return f"could not parse row token '{op.fields[0]}'"
        row_chain = [
            re.sub(r"\([^()]*\)", "", part).strip()
            for part in (row_match.group(2) or "").split("%")
            if part.strip()
        ]
        row_fields, _type_name, err = self._resolve_field_token(array_name, row_chain, proc)
        if err:
            return err

        parsed_impl = _parse_implied_do(op.fields[-1].strip())
        if parsed_impl is None:
            return f"could not parse implied-do '{op.fields[-1]}'"
        items, _loop_var, _lo, hi = parsed_impl
        if len(items) != 1:
            return "decision table repeat tail names more than one variable"

        hi_match = _FIELD_RE.match(hi.strip())
        hi_chain = [
            re.sub(r"\([^()]*\)", "", part).strip()
            for part in ((hi_match.group(2) if hi_match else "") or "").split("%")
            if part.strip()
        ]
        repeat_count_name = hi_chain[-1].lower() if hi_chain else hi.strip().lower()
        if repeat_count_name not in header_by_name:
            return f"repeat count '{hi}' is not a header field"

        item_match = _FIELD_RE.match(items[0].strip())
        if item_match is None:
            return f"could not parse repeat item '{items[0]}'"
        item_chain = [
            re.sub(r"\([^()]*\)", "", part).strip()
            for part in (item_match.group(2) or "").split("%")
            if part.strip()
        ]
        repeat_fields, _repeat_type, err = self._resolve_field_token(array_name, item_chain, proc)
        if err:
            return err
        if len(repeat_fields) != 1:
            return f"repeat item '{items[0]}' did not resolve to exactly one column"

        return DecisionTableBlock(
            row_count_field=header_by_name[row_count_name],
            row_fields=row_fields,
            repeat_count_field=header_by_name[repeat_count_name],
            repeat_field=repeat_fields[0],
        )

    def _select_case_vocabulary(
        self, procedures: list[ProcedureDoc], subject_pattern: str
    ) -> list[str]:
        """The case labels of the first select-case anywhere whose subject matches."""
        pattern = re.compile(subject_pattern, re.I)
        for proc in procedures:
            for sc in proc.select_cases:
                if sc.subject and pattern.search(sc.subject):
                    return sc.cases
        return []

    def resolve_multi_section_block(
        self, block: _IOBlock, proc: ProcedureDoc
    ) -> tuple[MultiSectionSchema | None, str | None]:
        """Resolve curated files with multiple logical read sections."""
        filenames = _filenames_for_block(block, proc, self)
        if not any(name in MULTI_SECTION_FILES for name in filenames):
            return None, None
        if "constituents.cs" in filenames:
            return self._resolve_constituents_cs_block(block, proc)
        return self._resolve_station_list_block(block, proc)

    def _resolve_station_list_block(
        self, block: _IOBlock, proc: ProcedureDoc
    ) -> tuple[MultiSectionSchema | None, str | None]:
        """Resolve a measured-weather station-list ``*.cli`` file.

        SWAT+ reads these files in several passes over the same data rows: one
        pass counts rows to size arrays, one pass stores the station names, and
        one pass stores the station filenames later opened as separate physical
        time-series files. This method captures only the index file opened on
        the current block's unit.
        """
        count_op = next(
            (
                op for op in block.reads
                if len(op.fields) == 1
                and op.fields[0].strip().lower() in _THROWAWAY_TARGETS
                and re.search(r"do\s+while\s*\(\s*eof\s*==\s*0\s*\)", op.condition or "", re.I)
            ),
            None,
        )
        station_op = next(
            (
                op for op in block.reads
                if len(op.fields) == 1
                and (m := _FIELD_RE.match(op.fields[0].strip()))
                and m.group(1).lower().endswith("_n")
                and _in_do_loop(op)
            ),
            None,
        )
        filename_op = next(
            (
                op for op in block.reads
                if len(op.fields) == 1
                and (m := _FIELD_RE.match(op.fields[0].strip()))
                and [c.lower() for c in _parse_component_chain(m.group(2) or "")[0]] == ["filename"]
                and _in_do_loop(op)
            ),
            None,
        )
        if station_op is None or filename_op is None:
            return None, "multi-section station list missing station-name or filename pass"

        station_match = _FIELD_RE.match(station_op.fields[0].strip())
        station_fields, _station_type, err = self._resolve_field_token(
            station_match.group(1), [], proc
        )
        if err:
            return None, err
        filename_match = _FIELD_RE.match(filename_op.fields[0].strip())
        filename_chain, last_is_element = _parse_component_chain(filename_match.group(2) or "")
        filename_fields, _filename_type, err = self._resolve_field_token(
            filename_match.group(1), filename_chain, proc, last_is_element=last_is_element
        )
        if err:
            return None, err
        if len(station_fields) != 1 or len(filename_fields) != 1:
            return None, "multi-section station list fields did not resolve to scalar columns"

        sections: list[MultiSectionSection] = []
        if count_op is not None:
            sections.append(
                MultiSectionSection(
                    name="row_count_pass",
                    fields=[],
                    count_source="until_eof",
                    reader_line=count_op.location.line,
                )
            )
        sections.extend(
            [
                MultiSectionSection(
                    name="station_name_pass",
                    fields=station_fields,
                    count_source="row_count_pass",
                    reader_line=station_op.location.line,
                ),
                MultiSectionSection(
                    name="station_filename_pass",
                    fields=filename_fields,
                    count_source="row_count_pass",
                    reader_line=filename_op.location.line,
                ),
            ]
        )
        return (
            MultiSectionSchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=(count_op or station_op).location.line,
            ),
            None,
        )

    def _resolve_constituents_cs_block(
        self, block: _IOBlock, proc: ProcedureDoc
    ) -> tuple[MultiSectionSchema | None, str | None]:
        """Resolve ``constituents.cs`` as count lines followed by name-list lines."""
        sections: list[MultiSectionSection] = []
        for category, count_name, list_name in _CONSTITUENTS_CS_SECTIONS:
            count_op = next(
                (
                    op for op in block.reads
                    if len(op.fields) == 1
                    and _normalised_field_name(op.fields[0]) == count_name
                ),
                None,
            )
            list_op = next(
                (
                    op for op in block.reads
                    if len(op.fields) == 1
                    and (parsed := _parse_implied_do(op.fields[0])) is not None
                    and len(parsed[0]) == 1
                    and _normalised_field_name(parsed[0][0]) == list_name
                    and parsed[3].strip().lower().endswith(count_name)
                ),
                None,
            )
            if count_op is None or list_op is None:
                return None, f"constituents.cs missing {category} count/list section"

            count_fields, _count_type, err = self._resolve_field_expr(
                count_op.fields[0], proc
            )
            if err:
                return None, err
            list_items, _loop_var, _lo, _hi = _parse_implied_do(list_op.fields[0]) or (
                [],
                "",
                "",
                "",
            )
            list_fields, _list_type, err = self._resolve_field_expr(list_items[0], proc)
            if err:
                return None, err
            if len(count_fields) != 1 or len(list_fields) != 1:
                return None, (
                    f"constituents.cs {category} section did not resolve to scalar fields"
                )

            count_section_name = f"{category}_count"
            sections.append(
                MultiSectionSection(
                    name=count_section_name,
                    fields=count_fields,
                    count_source="literal_1",
                    reader_line=count_op.location.line,
                )
            )
            sections.append(
                MultiSectionSection(
                    name=f"{category}_names",
                    fields=list_fields,
                    count_source=count_section_name,
                    reader_line=list_op.location.line,
                )
            )

        return (
            MultiSectionSchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_field_expr(
        self, expr: str, proc: ProcedureDoc
    ) -> tuple[list[FieldSpec], str | None, str | None]:
        match = _FIELD_RE.match(expr.strip())
        if match is None:
            return [], None, f"could not parse field '{expr}'"
        chain, last_is_element = _parse_component_chain(match.group(2) or "")
        return self._resolve_field_token(
            match.group(1), chain, proc, last_is_element=last_is_element
        )

    def resolve_runtime_arity_block(
        self, block: _IOBlock, proc: ProcedureDoc
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        """Resolve curated runtime-arity files."""
        filenames = _filenames_for_block(block, proc, self)
        row_repeat_specs = {
            "hmet_hru.ini": ("constituents.cs:metals_count", "cs_db%num_metals"),
            "pest_hru.ini": ("constituents.cs:pests_count", "cs_db%num_pests"),
        }
        for filename, (count_source, count_expr) in row_repeat_specs.items():
            if filename in filenames:
                return self._resolve_hru_name_soil_plant_row_repeat_runtime_arity_block(
                    block,
                    proc,
                    filename=filename,
                    repeat_source=count_source,
                    repeat_expr=count_expr,
                )

        combined_array_specs = {
            "path_hru.ini": ("constituents.cs:paths_count", "cs_db%num_paths"),
        }
        for filename, (count_source, count_expr) in combined_array_specs.items():
            if filename in filenames:
                return self._resolve_hru_name_combined_soil_plant_runtime_arity_block(
                    block,
                    proc,
                    filename=filename,
                    array_count_source=count_source,
                    array_count_expr=count_expr,
                )

        atmo_specs = {
            "atmodep.cli",
            "cs_atmo.cli",
            "salt_atmo.cli",
        }
        for filename in atmo_specs:
            if filename in filenames:
                return self._resolve_atmospheric_runtime_arity_block(
                    block,
                    proc,
                    filename=filename,
                )

        recall_specs = {
            "cs_recall.rec",
            "salt_recall.rec",
        }
        for filename in recall_specs:
            if filename in filenames:
                return self._resolve_recall_runtime_arity_block(
                    block,
                    proc,
                    filename=filename,
                )

        gwflow_specs = {
            "cell_sol.gw",
            "minerals.gw",
            "tvheads.gw",
            "ponds.gw",
            "gwflow_canal.con",
        }
        for filename in gwflow_specs:
            if filename in filenames:
                return self._resolve_gwflow_runtime_arity_block(
                    block,
                    proc,
                    filename=filename,
                )
        single_array_specs = {
            "dr_hmet.del": ("delivery_ratios", "hmet", "constituents.cs:metals_count", "cs_db%num_metals"),
            "dr_path.del": ("delivery_ratios", "path", "constituents.cs:paths_count", "cs_db%num_paths"),
            "dr_pest.del": ("delivery_ratios", "pest", "constituents.cs:pests_count", "cs_db%num_pests"),
            "dr_salt.del": ("delivery_ratios", "salt", "constituents.cs:salts_count", "cs_db%num_salts"),
            "exco_hmet.exc": ("export_coefficients", "hmet", "constituents.cs:metals_count", "cs_db%num_metals"),
            "exco_path.exc": ("export_coefficients", "path", "constituents.cs:paths_count", "cs_db%num_paths"),
            "exco_pest.exc": ("export_coefficients", "pest", "constituents.cs:pests_count", "cs_db%num_pests"),
            "exco_salt.exc": ("export_coefficients", "salt", "constituents.cs:salts_count", "cs_db%num_salts"),
            "cs_aqu.ini": ("aquifer_concentrations", "aqu", "constituents.cs:cs_count", "cs_db%num_cs + cs_db%num_cs"),
            "cs_channel.ini": ("channel_concentrations", "conc", "constituents.cs:cs_count", "cs_db%num_cs"),
            "salt_channel.ini": ("channel_concentrations", "conc", "constituents.cs:salts_count", "cs_db%num_salts"),
        }
        for filename, (section_name, field_name, count_source, count_expr) in single_array_specs.items():
            if filename in filenames:
                return self._resolve_name_plus_variable_array_runtime_arity_block(
                    block,
                    proc,
                    filename=filename,
                    array_section_name=section_name,
                    array_field_name=field_name,
                    array_count_source=count_source,
                    array_count_expr=count_expr,
                )

        water_init_specs = {
            "pest_water.ini": ("constituents.cs:pests_count", "cs_db%num_pests"),
            "path_water.ini": ("constituents.cs:paths_count", "cs_db%num_paths"),
        }
        for filename, (count_source, count_expr) in water_init_specs.items():
            if filename in filenames:
                return self._resolve_water_init_runtime_arity_block(
                    block,
                    proc,
                    filename=filename,
                    array_count_source=count_source,
                    array_count_expr=count_expr,
                )

        water_nested_specs = {
            "water_canal.wal",
            "water_pipe.wal",
        }
        for filename in water_nested_specs:
            if filename in filenames:
                return self._resolve_water_nested_runtime_arity_block(
                    block,
                    proc,
                    filename=filename,
                )

        wal_specs = {
            "water_treat.wal",
            "water_use.wal",
            "out_src.wal",
        }
        for filename in wal_specs:
            if filename in filenames:
                return self._resolve_wal_constituent_runtime_arity_block(
                    block,
                    proc,
                    filename=filename,
                )

        hru_array_specs = {
            "cs_hru.ini": ("constituents.cs:cs_count", "cs_db%num_cs + cs_db%num_cs"),
            "salt_hru.ini": ("constituents.cs:salts_count", "cs_db%num_salts+5"),
        }
        for filename, (count_source, count_expr) in hru_array_specs.items():
            if filename in filenames:
                return self._resolve_hru_name_soil_plant_runtime_arity_block(
                    block,
                    proc,
                    filename=filename,
                    array_count_source=count_source,
                    array_count_expr=count_expr,
                )
        return None, None

    def _resolve_hru_name_soil_plant_row_repeat_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
        *,
        filename: str,
        repeat_source: str,
        repeat_expr: str,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1
                and op.fields[0].strip().lower() in _THROWAWAY_TARGETS
                and re.search(
                    r"do\s+while\s*\(\s*eof\s*==\s*0\s*\)",
                    op.condition or "",
                    re.I,
                )
            ),
            None,
        )
        name_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1
                and (
                    _normalised_field_name(op.fields[0]) == "name"
                    or (_normalised_field_name(op.fields[0]) or "").endswith("_name")
                )
                and (count_op is None or op.location.line > count_op.location.line)
            ),
            None,
        )
        combined_row_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 3
                and _normalised_field_name(op.fields[0]) in _THROWAWAY_TARGETS
                and _normalised_field_name(op.fields[1]) == "soil"
                and _normalised_field_name(op.fields[2]) == "plt"
                and name_op is not None
                and op.location.line > name_op.location.line
            ),
            None,
        )
        soil_row_op = None
        plant_row_op = None
        if combined_row_op is None:
            soil_row_op = next(
                (
                    op
                    for op in block.reads
                    if len(op.fields) == 2
                    and _normalised_field_name(op.fields[0]) in _THROWAWAY_TARGETS
                    and _normalised_field_name(op.fields[1]) == "soil"
                    and name_op is not None
                    and op.location.line > name_op.location.line
                ),
                None,
            )
            plant_row_op = next(
                (
                    op
                    for op in block.reads
                    if len(op.fields) == 2
                    and _normalised_field_name(op.fields[0]) in _THROWAWAY_TARGETS
                    and _normalised_field_name(op.fields[1]) == "plt"
                    and soil_row_op is not None
                    and op.location.line > soil_row_op.location.line
                ),
                None,
            )
        if name_op is None or (combined_row_op is None and (soil_row_op is None or plant_row_op is None)):
            return None, f"{filename} missing name/soil+plant row-repeat reads"

        name_fields, _name_type, err = self._resolve_field_expr(name_op.fields[0], proc)
        if err:
            return None, err
        if combined_row_op is not None:
            soil_expr = combined_row_op.fields[1]
            plant_expr = combined_row_op.fields[2]
            reader_line = combined_row_op.location.line
        else:
            soil_expr = soil_row_op.fields[1]
            plant_expr = plant_row_op.fields[1]
            reader_line = soil_row_op.location.line
        soil_fields, _soil_type, err = self._resolve_field_expr(soil_expr, proc)
        if err:
            return None, err
        plant_fields, _plant_type, err = self._resolve_field_expr(plant_expr, proc)
        if err:
            return None, err
        if len(name_fields) != 1 or len(soil_fields) != 1 or len(plant_fields) != 1:
            return None, f"{filename} runtime-arity fields did not resolve to scalar fields"

        count_section = "row_count_pass"
        sections: list[RuntimeAritySection] = []
        if count_op is not None:
            sections.append(
                RuntimeAritySection(
                    name=count_section,
                    fields=[],
                    count_source="until_eof_group",
                    reader_line=count_op.location.line,
                )
            )
        sections.extend(
            [
                RuntimeAritySection(
                    name="entry_name",
                    fields=[RuntimeArityField(name_fields[0])],
                    count_source=count_section,
                    reader_line=name_op.location.line,
                ),
                RuntimeAritySection(
                    name="soil_plant_concentration_rows",
                    fields=[RuntimeArityField(soil_fields[0]), RuntimeArityField(plant_fields[0])],
                    count_source=count_section,
                    reader_line=reader_line,
                    repeat_source=repeat_source,
                    repeat_expr=repeat_expr,
                ),
            ]
        )
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_hru_name_combined_soil_plant_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
        *,
        filename: str,
        array_count_source: str,
        array_count_expr: str,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1
                and op.fields[0].strip().lower() in _THROWAWAY_TARGETS
                and re.search(
                    r"do\s+while\s*\(\s*eof\s*==\s*0\s*\)",
                    op.condition or "",
                    re.I,
                )
            ),
            None,
        )
        name_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1
                and _normalised_field_name(op.fields[0]) == "name"
                and (count_op is None or op.location.line > count_op.location.line)
            ),
            None,
        )
        combined_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 3
                and _normalised_field_name(op.fields[0]) in _THROWAWAY_TARGETS
                and _normalised_field_name(op.fields[1]) == "soil"
                and _normalised_field_name(op.fields[2]) == "plt"
                and name_op is not None
                and op.location.line > name_op.location.line
            ),
            None,
        )
        if name_op is None or combined_op is None:
            return None, f"{filename} missing name/soil+plant runtime-arity reads"

        name_fields, _name_type, err = self._resolve_field_expr(name_op.fields[0], proc)
        if err:
            return None, err
        soil_fields, _soil_type, err = self._resolve_field_expr(combined_op.fields[1], proc)
        if err:
            return None, err
        plant_fields, _plant_type, err = self._resolve_field_expr(combined_op.fields[2], proc)
        if err:
            return None, err
        if len(name_fields) != 1 or len(soil_fields) != 1 or len(plant_fields) != 1:
            return None, f"{filename} runtime-arity fields did not resolve to scalar fields"

        count_section = "row_count_pass"
        sections: list[RuntimeAritySection] = []
        if count_op is not None:
            sections.append(
                RuntimeAritySection(
                    name=count_section,
                    fields=[],
                    count_source="until_eof_group",
                    reader_line=count_op.location.line,
                )
            )
        sections.extend(
            [
                RuntimeAritySection(
                    name="entry_name",
                    fields=[RuntimeArityField(name_fields[0])],
                    count_source=count_section,
                    reader_line=name_op.location.line,
                ),
                RuntimeAritySection(
                    name="soil_plant_concentrations",
                    fields=[
                        RuntimeArityField(
                            soil_fields[0],
                            count_source=array_count_source,
                            count_expr=array_count_expr,
                        ),
                        RuntimeArityField(
                            plant_fields[0],
                            count_source=array_count_source,
                            count_expr=array_count_expr,
                        ),
                    ],
                    count_source=count_section,
                    reader_line=combined_op.location.line,
                ),
            ]
        )
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_hru_name_soil_plant_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
        *,
        filename: str,
        array_count_source: str,
        array_count_expr: str,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1
                and op.fields[0].strip().lower() in _THROWAWAY_TARGETS
                and re.search(
                    r"do\s+while\s*\(\s*eof\s*==\s*0\s*\)",
                    op.condition or "",
                    re.I,
                )
            ),
            None,
        )
        name_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1
                and _normalised_field_name(op.fields[0]) == "name"
                and (count_op is None or op.location.line > count_op.location.line)
            ),
            None,
        )
        soil_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1
                and _normalised_field_name(op.fields[0]) == "soil"
                and name_op is not None
                and op.location.line > name_op.location.line
            ),
            None,
        )
        plant_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1
                and _normalised_field_name(op.fields[0]) == "plt"
                and soil_op is not None
                and op.location.line > soil_op.location.line
            ),
            None,
        )
        if name_op is None or soil_op is None or plant_op is None:
            return None, f"{filename} missing name/soil/plant runtime-arity reads"

        name_fields, _name_type, err = self._resolve_field_expr(name_op.fields[0], proc)
        if err:
            return None, err
        soil_fields, _soil_type, err = self._resolve_field_expr(soil_op.fields[0], proc)
        if err:
            return None, err
        plant_fields, _plant_type, err = self._resolve_field_expr(plant_op.fields[0], proc)
        if err:
            return None, err
        if len(name_fields) != 1 or len(soil_fields) != 1 or len(plant_fields) != 1:
            return None, f"{filename} runtime-arity fields did not resolve to scalar fields"

        count_section = "row_count_pass"
        sections: list[RuntimeAritySection] = []
        if count_op is not None:
            sections.append(
                RuntimeAritySection(
                    name=count_section,
                    fields=[],
                    count_source="until_eof_group",
                    reader_line=count_op.location.line,
                )
            )
        sections.extend(
            [
                RuntimeAritySection(
                    name="entry_name",
                    fields=[RuntimeArityField(name_fields[0])],
                    count_source=count_section,
                    reader_line=name_op.location.line,
                ),
                RuntimeAritySection(
                    name="soil_concentrations",
                    fields=[
                        RuntimeArityField(
                            soil_fields[0],
                            count_source=array_count_source,
                            count_expr=array_count_expr,
                        )
                    ],
                    count_source=count_section,
                    reader_line=soil_op.location.line,
                ),
                RuntimeAritySection(
                    name="plant_concentrations",
                    fields=[
                        RuntimeArityField(
                            plant_fields[0],
                            count_source=array_count_source,
                            count_expr=array_count_expr,
                        )
                    ],
                    count_source=count_section,
                    reader_line=plant_op.location.line,
                ),
            ]
        )
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_atmospheric_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
        *,
        filename: str,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        if filename == "atmodep.cli":
            return self._resolve_atmodep_cli_runtime_arity_block(block, proc)
        if filename == "cs_atmo.cli":
            return self._resolve_cs_atmo_runtime_arity_block(block, proc)
        if filename == "salt_atmo.cli":
            return self._resolve_salt_atmo_runtime_arity_block(block, proc)
        return None, None

    def _resolve_atmodep_cli_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        control_op = next(
            (
                op for op in block.reads
                if len(op.fields) == 5
                and _normalised_field_name(op.fields[0]) == "num_sta"
                and _normalised_field_name(op.fields[1]) == "timestep"
                and _normalised_field_name(op.fields[4]) == "num"
            ),
            None,
        )
        if control_op is None:
            return None, "atmodep.cli missing control header read"
        control_fields, _control_type, err = self._resolve_read_fields(control_op, proc)
        if err or control_fields is None:
            return None, err or "atmodep.cli could not resolve control header"
        station_fields = self._atmo_branch_station_fields(block, proc, array_name="atmodep")
        if station_fields is None:
            return None, "atmodep.cli missing one or more timestep branches"
        return (
            RuntimeAritySchema(
                sections=[
                    RuntimeAritySection(
                        name="control_header",
                        fields=[RuntimeArityField(f) for f in control_fields],
                        count_source="literal_1",
                        reader_line=control_op.location.line,
                    )
                ] + station_fields,
                reader=proc.location.path,
                reader_line=control_op.location.line,
            ),
            None,
        )

    def _resolve_cs_atmo_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        sections = self._constituent_atmo_sections(
            block,
            proc,
            station_field_name="station_name",
            station_doc="station name",
            repeat_source="constituents.cs:cs_count",
            repeat_expr="cs_db%num_cs",
            value_fields={"aa": [("rf", "rf"), ("dry", "dry")], "mo": [("rfmo", "rfmo"), ("drymo", "drymo")], "yr": [("rfyr", "rfyr"), ("dryyr", "dryyr")]},
            value_count_source="atmodep.cli:control_header:num",
            value_count_expr="atmodep_cont%num",
            discard_prefix=False,
        )
        if sections is None:
            return None, "cs_atmo.cli missing one or more timestep branches"
        return RuntimeAritySchema(sections=sections, reader=proc.location.path, reader_line=sections[0].reader_line), None

    def _resolve_salt_atmo_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        sections = self._constituent_atmo_sections(
            block,
            proc,
            station_field_name="station_name",
            station_doc="station name",
            repeat_source="constituents.cs:salts_count",
            repeat_expr="cs_db%num_salts",
            value_fields={"aa": [("rf", "rf"), ("dry", "dry")], "mo": [("rfmo", "rfmo"), ("drymo", "drymo")], "yr": [("rfyr", "rfyr"), ("dryyr", "dryyr")]},
            value_count_source="atmodep.cli:control_header:num",
            value_count_expr="atmodep_cont%num",
            discard_prefix=True,
        )
        if sections is None:
            return None, "salt_atmo.cli missing one or more timestep branches"
        return RuntimeAritySchema(sections=sections, reader=proc.location.path, reader_line=sections[0].reader_line), None

    def _atmo_branch_station_fields(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
        *,
        array_name: str,
    ) -> list[RuntimeAritySection] | None:
        sections: list[RuntimeAritySection] = []
        station_count_source = "control_header:num_sta"
        period_count_source = "control_header:num"
        station_name_doc = FieldSpec(
            fortran_name="station_name",
            fortran_type="character",
            numeric=False,
            units=None,
            doc="station name",
        )
        branch_specs = {
            "aa": ["nh4_rf", "no3_rf", "nh4_dry", "no3_dry"],
            "mo": ["nh4_rfmo", "no3_rfmo", "nh4_drymo", "no3_drymo"],
            "yr": ["nh4_rfyr", "no3_rfyr", "nh4_dryyr", "no3_dryyr"],
        }
        for branch, field_names in branch_specs.items():
            station_op = next((
                op for op in block.reads
                if len(op.fields) == 1
                and _normalised_field_name(op.fields[0]) == "name"
                and f'timestep == "{branch}"' in (op.condition or "")
            ), None)
            if station_op is None:
                return None
            sections.append(RuntimeAritySection(
                name=f"{branch}_station_name",
                fields=[RuntimeArityField(station_name_doc)],
                count_source=station_count_source,
                reader_line=station_op.location.line,
            ))
            for fname in field_names:
                op = next((
                    read for read in block.reads
                    if len(read.fields) == 1
                    and f'timestep == "{branch}"' in (read.condition or "")
                    and _parse_implied_do(read.fields[0].strip()) is not None
                    and self._atmo_implied_do_field_name(read.fields[0]) == fname
                ), None)
                if op is None:
                    if branch == "aa":
                        op = next((
                            read for read in block.reads
                            if len(read.fields) == 1
                            and f'timestep == "{branch}"' in (read.condition or "")
                            and _normalised_field_name(read.fields[0]) == fname
                        ), None)
                    if op is None:
                        return None
                field_expr = op.fields[0]
                implied = _parse_implied_do(field_expr.strip())
                array_expr = field_expr if implied is None else implied[0][0]
                resolved_fields, _t, err = self._resolve_field_expr(array_expr, proc)
                if err or len(resolved_fields) != 1:
                    return None
                rfield = RuntimeArityField(resolved_fields[0])
                if branch != "aa":
                    rfield = RuntimeArityField(resolved_fields[0], count_source=period_count_source, count_expr="atmodep_cont%num")
                sections.append(RuntimeAritySection(
                    name=f"{branch}_{fname}",
                    fields=[rfield],
                    count_source=station_count_source,
                    reader_line=op.location.line,
                ))
        return sections

    def _constituent_atmo_sections(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
        *,
        station_field_name: str,
        station_doc: str,
        repeat_source: str,
        repeat_expr: str,
        value_fields: dict[str, list[tuple[str, str]]],
        value_count_source: str,
        value_count_expr: str,
        discard_prefix: bool,
    ) -> list[RuntimeAritySection] | None:
        sections: list[RuntimeAritySection] = []
        station_count_source = "atmodep.cli:control_header:num_sta"
        station_field = RuntimeArityField(FieldSpec(fortran_name=station_field_name, fortran_type="character", numeric=False, units=None, doc=station_doc))
        for branch, pairs in value_fields.items():
            station_op = next((
                op for op in block.reads
                if len(op.fields) == 1
                and f'timestep == "{branch}"' in (op.condition or "")
                and (_normalised_field_name(op.fields[0]) == "station_name" or _normalised_field_name(op.fields[0]) == "name")
            ), None)
            if station_op is None:
                return None
            sections.append(RuntimeAritySection(name=f"{branch}_station_name", fields=[station_field], count_source=station_count_source, reader_line=station_op.location.line))
            for suffix, target_name in pairs:
                op = next((
                    read for read in block.reads
                    if f'timestep == "{branch}"' in (read.condition or "")
                    and len(read.fields) in (1, 2)
                    and self._atmo_value_field_name(read, discard_prefix) == target_name
                ), None)
                if op is None:
                    return None
                resolved = self._atmo_resolve_value_field(op, proc, discard_prefix)
                if resolved is None:
                    return None
                field, variable_arity = resolved
                runtime_field = RuntimeArityField(field, count_source=value_count_source, count_expr=value_count_expr) if variable_arity else RuntimeArityField(field)
                sections.append(RuntimeAritySection(
                    name=f"{branch}_{suffix}_rows",
                    fields=[runtime_field],
                    count_source=station_count_source,
                    reader_line=op.location.line,
                    repeat_source=repeat_source,
                    repeat_expr=repeat_expr,
                ))
        return sections

    def _atmo_implied_do_field_name(self, token: str) -> str | None:
        implied = _parse_implied_do(token.strip())
        if implied is None or len(implied[0]) != 1:
            return None
        return _normalised_field_name(implied[0][0])

    def _atmo_value_field_name(self, op: IOOperation, discard_prefix: bool) -> str | None:
        if not op.fields:
            return None
        field_expr = op.fields[1] if discard_prefix and len(op.fields) == 2 else op.fields[-1]
        implied = _parse_implied_do(field_expr.strip())
        if implied is not None and len(implied[0]) == 1:
            return _normalised_field_name(implied[0][0])
        return _normalised_field_name(field_expr)

    def _atmo_resolve_value_field(
        self,
        op: IOOperation,
        proc: ProcedureDoc,
        discard_prefix: bool,
    ) -> tuple[FieldSpec, bool] | None:
        field_expr = op.fields[1] if discard_prefix and len(op.fields) == 2 else op.fields[-1]
        implied = _parse_implied_do(field_expr.strip())
        variable_arity = implied is not None
        array_expr = field_expr if implied is None else implied[0][0]
        fields, _t, err = self._resolve_field_expr(array_expr, proc)
        if err or len(fields) != 1:
            return None
        return fields[0], variable_arity

    def _resolve_recall_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
        *,
        filename: str,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        if filename == "cs_recall.rec":
            return self._resolve_cs_recall_runtime_arity_block(block, proc)
        if filename == "salt_recall.rec":
            return self._resolve_salt_recall_runtime_arity_block(block, proc)
        return None, f"{filename} is not a supported recall runtime-arity file"

    def _resolve_salt_recall_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1 and _normalised_field_name(op.fields[0]) == "i"
            ),
            None,
        )
        data_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 4
                and _normalised_field_name(op.fields[0]) == "k"
                and _normalised_field_name(op.fields[1]) == "name"
                and _normalised_field_name(op.fields[2]) == "typ"
                and _normalised_field_name(op.fields[3]) == "filename"
            ),
            None,
        )
        nested_proc_block = next(
            (
                candidate
                for candidate in _procedure_io_blocks(proc)
                if candidate.open is not None
                and (candidate.open.file_expr or "").strip().lower() == "rec_salt(i)%filename"
            ),
            None,
        )
        if count_op is None or data_op is None or nested_proc_block is None:
            return None, "salt_recall.rec missing registry/nested runtime-arity reads"

        nested_years_op = next(
            (
                op
                for op in nested_proc_block.reads
                if len(op.fields) == 1 and _normalised_field_name(op.fields[0]) == "nbyr"
            ),
            None,
        )
        nested_data_op = next(
            (
                op
                for op in nested_proc_block.reads
                if len(op.fields) == 7
                and _normalised_field_name(op.fields[0]) == "jday"
                and _normalised_field_name(op.fields[1]) == "mo"
                and _normalised_field_name(op.fields[2]) == "day_mo"
                and _normalised_field_name(op.fields[3]) == "iyr"
                and _normalised_field_name(op.fields[4]) == "ob_typ"
                and _normalised_field_name(op.fields[5]) == "ob_name"
                and _parse_implied_do(op.fields[6].strip()) is not None
            ),
            None,
        )
        if nested_years_op is None or nested_data_op is None:
            return None, "salt_recall.rec missing nested count/data runtime-arity reads"

        registry_fields: list[RuntimeArityField] = []
        for field_expr in data_op.fields:
            fields, _field_type, err = self._resolve_field_expr(field_expr, proc)
            if err:
                return None, err
            if len(fields) != 1:
                return None, "salt_recall.rec registry field did not resolve to scalar field"
            registry_fields.append(RuntimeArityField(fields[0]))

        nested_year_fields, _nested_year_type, err = self._resolve_field_expr(
            nested_years_op.fields[0], proc
        )
        if err:
            return None, err
        if len(nested_year_fields) != 1:
            return None, "salt_recall.rec nested year count did not resolve to a scalar field"

        nested_row_fields: list[RuntimeArityField] = []
        for field_expr in nested_data_op.fields[:-1]:
            fields, _field_type, err = self._resolve_field_expr(field_expr, proc)
            if err:
                return None, err
            if len(fields) != 1:
                return None, "salt_recall.rec nested row field did not resolve to scalar field"
            nested_row_fields.append(RuntimeArityField(fields[0]))

        implied = _parse_implied_do(nested_data_op.fields[-1].strip())
        if implied is None or len(implied[0]) != 1:
            return None, "salt_recall.rec nested implied-do runtime-arity read had unexpected shape"
        array_fields, _array_type, err = self._resolve_field_expr(implied[0][0], proc)
        if err:
            return None, err
        if len(array_fields) != 1:
            return None, "salt_recall.rec concentration field did not resolve to scalar field"
        nested_row_fields.append(
            RuntimeArityField(
                array_fields[0],
                count_source="constituents.cs:salts_count",
                count_expr="cs_db%num_salts",
            )
        )

        sections = [
            RuntimeAritySection(
                name="row_count_pass",
                fields=[],
                count_source="until_eof_group",
                reader_line=count_op.location.line,
            ),
            RuntimeAritySection(
                name="registry_rows",
                fields=registry_fields,
                count_source="row_count_pass",
                reader_line=data_op.location.line,
            ),
            RuntimeAritySection(
                name="nested_year_count",
                fields=[RuntimeArityField(nested_year_fields[0])],
                count_source="single_record",
                reader_line=nested_years_op.location.line,
                applies_when="typ != 4",
                nested_file_field="filename",
            ),
            RuntimeAritySection(
                name="nested_daily_rows",
                fields=nested_row_fields,
                count_source="until_eof_nested_file",
                reader_line=nested_data_op.location.line,
                applies_when="typ == 1",
                nested_file_field="filename",
            ),
            RuntimeAritySection(
                name="nested_monthly_rows",
                fields=nested_row_fields,
                count_source="until_eof_nested_file",
                reader_line=nested_data_op.location.line,
                applies_when="typ == 2",
                nested_file_field="filename",
            ),
            RuntimeAritySection(
                name="nested_annual_rows",
                fields=nested_row_fields,
                count_source="until_eof_nested_file",
                reader_line=nested_data_op.location.line,
                applies_when="typ == 3",
                nested_file_field="filename",
            ),
        ]
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_cs_recall_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1 and _normalised_field_name(op.fields[0]) == "i"
            ),
            None,
        )
        data_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 4
                and _normalised_field_name(op.fields[0]) == "k"
                and _normalised_field_name(op.fields[1]) == "name"
                and _normalised_field_name(op.fields[2]) == "typ"
                and _normalised_field_name(op.fields[3]) == "filename"
            ),
            None,
        )
        nested_proc_block = next(
            (
                candidate
                for candidate in _procedure_io_blocks(proc)
                if candidate.open is not None
                and (candidate.open.file_expr or "").strip().lower() == "rec_cs(i)%filename"
            ),
            None,
        )
        if count_op is None or data_op is None or nested_proc_block is None:
            return None, "cs_recall.rec missing registry/nested runtime-arity reads"

        nested_years_op = next(
            (
                op
                for op in nested_proc_block.reads
                if len(op.fields) == 1 and _normalised_field_name(op.fields[0]) == "nbyr"
            ),
            None,
        )
        nested_data_op = next(
            (
                op
                for op in nested_proc_block.reads
                if len(op.fields) == 7
                and _normalised_field_name(op.fields[0]) == "jday"
                and _normalised_field_name(op.fields[1]) == "mo"
                and _normalised_field_name(op.fields[2]) == "day_mo"
                and _normalised_field_name(op.fields[3]) == "iyr"
                and _normalised_field_name(op.fields[4]) == "ob_typ"
                and _normalised_field_name(op.fields[5]) == "ob_name"
                and _parse_implied_do(op.fields[6].strip()) is not None
            ),
            None,
        )
        if nested_years_op is None or nested_data_op is None:
            return None, "cs_recall.rec missing nested count/data runtime-arity reads"

        registry_fields: list[RuntimeArityField] = []
        for field_expr in data_op.fields:
            fields, _field_type, err = self._resolve_field_expr(field_expr, proc)
            if err:
                return None, err
            if len(fields) != 1:
                return None, "cs_recall.rec registry field did not resolve to scalar field"
            registry_fields.append(RuntimeArityField(fields[0]))

        nested_year_fields, _nested_year_type, err = self._resolve_field_expr(
            nested_years_op.fields[0], proc
        )
        if err:
            return None, err
        if len(nested_year_fields) != 1:
            return None, "cs_recall.rec nested year count did not resolve to a scalar field"

        nested_row_fields: list[RuntimeArityField] = []
        for field_expr in nested_data_op.fields[:-1]:
            fields, _field_type, err = self._resolve_field_expr(field_expr, proc)
            if err:
                return None, err
            if len(fields) != 1:
                return None, "cs_recall.rec nested row field did not resolve to scalar field"
            nested_row_fields.append(RuntimeArityField(fields[0]))

        implied = _parse_implied_do(nested_data_op.fields[-1].strip())
        if implied is None or len(implied[0]) != 1:
            return None, "cs_recall.rec nested implied-do runtime-arity read had unexpected shape"
        array_fields, _array_type, err = self._resolve_field_expr(implied[0][0], proc)
        if err:
            return None, err
        if len(array_fields) != 1:
            return None, "cs_recall.rec concentration field did not resolve to scalar field"
        nested_row_fields.append(
            RuntimeArityField(
                array_fields[0],
                count_source="constituents.cs:cs_count",
                count_expr="cs_db%num_cs",
            )
        )

        sections = [
            RuntimeAritySection(
                name="row_count_pass",
                fields=[],
                count_source="until_eof_group",
                reader_line=count_op.location.line,
            ),
            RuntimeAritySection(
                name="registry_rows",
                fields=registry_fields,
                count_source="row_count_pass",
                reader_line=data_op.location.line,
            ),
            RuntimeAritySection(
                name="nested_year_count",
                fields=[RuntimeArityField(nested_year_fields[0])],
                count_source="single_record",
                reader_line=nested_years_op.location.line,
                applies_when="typ != 4",
                nested_file_field="filename",
            ),
            RuntimeAritySection(
                name="nested_daily_rows",
                fields=nested_row_fields,
                count_source="until_eof_nested_file",
                reader_line=nested_data_op.location.line,
                applies_when="typ == 1",
                nested_file_field="filename",
            ),
            RuntimeAritySection(
                name="nested_monthly_rows",
                fields=nested_row_fields,
                count_source="until_eof_nested_file",
                reader_line=nested_data_op.location.line,
                applies_when="typ == 2",
                nested_file_field="filename",
            ),
            RuntimeAritySection(
                name="nested_annual_rows",
                fields=nested_row_fields,
                count_source="until_eof_nested_file",
                reader_line=nested_data_op.location.line,
                applies_when="typ == 3",
                nested_file_field="filename",
            ),
        ]
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_water_nested_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
        *,
        filename: str,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        if filename == "water_canal.wal":
            return self._resolve_water_canal_runtime_arity_block(block, proc)
        if filename == "water_pipe.wal":
            return self._resolve_water_pipe_runtime_arity_block(block, proc)
        return None, f"{filename} is not a supported nested water runtime-arity file"

    def _resolve_water_pipe_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        file_count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1 and _normalised_field_name(op.fields[0]) == "imax"
            ),
            None,
        )
        peek_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 6
                and _normalised_field_name(op.fields[0]) == "i"
                and _normalised_field_name(op.fields[-1]) == "num_aqu"
            ),
            None,
        )
        data_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 7
                and _normalised_field_name(op.fields[0]) == "i"
                and _normalised_field_name(op.fields[-2]) == "num_aqu"
                and _parse_implied_do(op.fields[-1].strip()) is not None
            ),
            None,
        )
        if file_count_op is None or peek_op is None or data_op is None:
            return None, "water_pipe.wal missing file-count/peek/data runtime-arity reads"

        file_count_fields, _count_type, err = self._resolve_field_expr(file_count_op.fields[0], proc)
        if err:
            return None, err
        if len(file_count_fields) != 1:
            return None, "water_pipe.wal file count did not resolve to a scalar field"

        prefix_fields: list[RuntimeArityField] = []
        for field_expr in data_op.fields[:-1]:
            fields, _field_type, err = self._resolve_field_expr(field_expr, proc)
            if err:
                return None, err
            if len(fields) != 1:
                return None, "water_pipe.wal prefix field did not resolve to scalar field"
            prefix_fields.append(RuntimeArityField(fields[0]))

        implied = _parse_implied_do(data_op.fields[-1].strip())
        if implied is None or len(implied[0]) != 1:
            return None, "water_pipe.wal implied-do runtime-arity read had unexpected shape"
        repeat_fields, _repeat_type, err = self._resolve_field_expr(implied[0][0], proc)
        if err:
            return None, err
        if not repeat_fields:
            return None, "water_pipe.wal repeat field did not resolve"

        sections = [
            RuntimeAritySection(
                name="entry_count",
                fields=[RuntimeArityField(file_count_fields[0])],
                count_source="single_record",
                reader_line=file_count_op.location.line,
            ),
            RuntimeAritySection(
                name="pipe_rows",
                fields=prefix_fields,
                count_source="entry_count",
                reader_line=data_op.location.line,
                repeat_source="pipe_rows:num_aqu",
                repeat_expr="num_aqu",
                repeat_fields=[RuntimeArityField(field) for field in repeat_fields],
            ),
        ]
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_water_canal_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        file_count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1 and _normalised_field_name(op.fields[0]) == "imax"
            ),
            None,
        )
        peek_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 17
                and _normalised_field_name(op.fields[0]) == "i"
                and _normalised_field_name(op.fields[-1]) == "num_aqu"
            ),
            None,
        )
        data_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 18
                and _normalised_field_name(op.fields[0]) == "i"
                and _normalised_field_name(op.fields[-2]) == "num_aqu"
                and _parse_implied_do(op.fields[-1].strip()) is not None
            ),
            None,
        )
        if file_count_op is None or peek_op is None or data_op is None:
            return None, "water_canal.wal missing file-count/peek/data runtime-arity reads"

        file_count_fields, _count_type, err = self._resolve_field_expr(file_count_op.fields[0], proc)
        if err:
            return None, err
        if len(file_count_fields) != 1:
            return None, "water_canal.wal file count did not resolve to a scalar field"

        prefix_fields: list[RuntimeArityField] = []
        for field_expr in data_op.fields[:-1]:
            fields, _field_type, err = self._resolve_field_expr(field_expr, proc)
            if err:
                return None, err
            if len(fields) != 1:
                return None, "water_canal.wal prefix field did not resolve to scalar field"
            prefix_fields.append(RuntimeArityField(fields[0]))

        implied = _parse_implied_do(data_op.fields[-1].strip())
        if implied is None or len(implied[0]) != 1:
            return None, "water_canal.wal implied-do runtime-arity read had unexpected shape"
        repeat_fields, _repeat_type, err = self._resolve_field_expr(implied[0][0], proc)
        if err:
            return None, err
        if not repeat_fields:
            return None, "water_canal.wal repeat field did not resolve"

        sections = [
            RuntimeAritySection(
                name="entry_count",
                fields=[RuntimeArityField(file_count_fields[0])],
                count_source="single_record",
                reader_line=file_count_op.location.line,
            ),
            RuntimeAritySection(
                name="canal_rows",
                fields=prefix_fields,
                count_source="entry_count",
                reader_line=data_op.location.line,
                repeat_source="canal_rows:num_aqu",
                repeat_expr="num_aqu",
                repeat_fields=[RuntimeArityField(field) for field in repeat_fields],
            ),
        ]
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_gwflow_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
        *,
        filename: str,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        if filename == "cell_sol.gw":
            return self._resolve_cell_sol_runtime_arity_block(block, proc)
        if filename == "minerals.gw":
            return self._resolve_minerals_runtime_arity_block(block, proc)
        if filename == "tvheads.gw":
            return self._resolve_tvheads_runtime_arity_block(block, proc)
        if filename == "ponds.gw":
            return self._resolve_ponds_runtime_arity_block(block, proc)
        if filename == "gwflow_canal.con":
            return self._resolve_gwflow_canal_runtime_arity_block(block, proc)
        return None, f"{filename} is not a supported gwflow runtime-arity file"

    def _resolve_cell_sol_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        data_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 2
                and _normalised_field_name(op.fields[0]) == "cell_id"
                and _parse_implied_do(op.fields[1].strip()) is not None
            ),
            None,
        )
        if data_op is None:
            return None, "cell_sol.gw missing cell_id/solute runtime-arity read"

        cell_fields, _cell_type, err = self._resolve_field_expr(data_op.fields[0], proc)
        if err:
            return None, err
        implied = _parse_implied_do(data_op.fields[1].strip())
        if implied is None or len(implied[0]) != 1:
            return None, "cell_sol.gw implied-do runtime-arity read had unexpected shape"
        solute_fields, _solute_type, err = self._resolve_field_expr(implied[0][0], proc)
        if err:
            return None, err
        if len(cell_fields) != 1 or len(solute_fields) != 1:
            return None, "cell_sol.gw runtime-arity fields did not resolve to scalar fields"

        sections = [
            RuntimeAritySection(
                name="solute_rows",
                fields=[
                    RuntimeArityField(cell_fields[0]),
                    RuntimeArityField(
                        solute_fields[0],
                        count_source="gwflow:gw_nsolute",
                        count_expr="gw_nsolute",
                    ),
                ],
                count_source="gwflow:ncell",
                reader_line=data_op.location.line,
            )
        ]
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_minerals_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1 and _normalised_field_name(op.fields[0]) == "gw_nminl"
            ),
            None,
        )
        structured_mode_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1 and _normalised_field_name(op.fields[0]) == "read_type"
            ),
            None,
        )
        structured_single_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1 and _normalised_field_name(op.fields[0]) == "single_value"
            ),
            None,
        )
        structured_array_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1
                and _parse_implied_do(op.fields[0].strip()) is not None
                and "grid_val" in op.fields[0]
            ),
            None,
        )
        unstructured_data_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1
                and _parse_implied_do(op.fields[0].strip()) is not None
                and "gwsol_minl_state" in op.fields[0]
            ),
            None,
        )
        if (
            count_op is None
            or structured_mode_op is None
            or structured_single_op is None
            or structured_array_op is None
            or unstructured_data_op is None
        ):
            return None, "minerals.gw missing count/structured/unstructured runtime-arity reads"

        count_fields, _count_type, err = self._resolve_field_expr(count_op.fields[0], proc)
        if err:
            return None, err
        mode_fields, _mode_type, err = self._resolve_field_expr(structured_mode_op.fields[0], proc)
        if err:
            return None, err
        single_fields, _single_type, err = self._resolve_field_expr(structured_single_op.fields[0], proc)
        if err:
            return None, err
        if len(count_fields) != 1 or len(mode_fields) != 1 or len(single_fields) != 1:
            return None, "minerals.gw scalar control fields did not resolve to scalar fields"

        structured_implied = _parse_implied_do(structured_array_op.fields[0].strip())
        unstructured_implied = _parse_implied_do(unstructured_data_op.fields[0].strip())
        if (
            structured_implied is None
            or len(structured_implied[0]) != 1
            or unstructured_implied is None
            or len(unstructured_implied[0]) != 1
        ):
            return None, "minerals.gw implied-do runtime-arity read had unexpected shape"

        structured_array_fields, _structured_type, err = self._resolve_field_expr(
            structured_implied[0][0], proc
        )
        if err:
            return None, err
        unstructured_fields, _unstructured_type, err = self._resolve_field_expr(
            unstructured_implied[0][0], proc
        )
        if err:
            return None, err
        if len(structured_array_fields) != 1 or len(unstructured_fields) != 1:
            return None, "minerals.gw array fields did not resolve to scalar fields"

        sections = [
            RuntimeAritySection(
                name="mineral_count",
                fields=[RuntimeArityField(count_fields[0])],
                count_source="single_record",
                reader_line=count_op.location.line,
            ),
            RuntimeAritySection(
                name="structured_mineral_modes",
                fields=[RuntimeArityField(mode_fields[0])],
                count_source="gwflow:gw_nminl",
                reader_line=structured_mode_op.location.line,
                applies_when='grid_type == "structured"',
            ),
            RuntimeAritySection(
                name="structured_single_value_rows",
                fields=[RuntimeArityField(single_fields[0])],
                count_source="structured_mineral_modes:single",
                reader_line=structured_single_op.location.line,
                applies_when='grid_type == "structured" and read_type == "single"',
            ),
            RuntimeAritySection(
                name="structured_array_rows",
                fields=[
                    RuntimeArityField(
                        structured_array_fields[0],
                        count_source="gwflow:grid_ncol",
                        count_expr="grid_ncol",
                    )
                ],
                count_source="gwflow:grid_nrow",
                reader_line=structured_array_op.location.line,
                applies_when='grid_type == "structured" and read_type == "array"',
            ),
            RuntimeAritySection(
                name="unstructured_mineral_rows",
                fields=[
                    RuntimeArityField(
                        unstructured_fields[0],
                        count_source="gwflow:gw_nminl",
                        count_expr="gw_nminl",
                    )
                ],
                count_source="gwflow:ncell",
                reader_line=unstructured_data_op.location.line,
                applies_when='grid_type == "unstructured"',
            ),
        ]
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_tvheads_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1 and _normalised_field_name(op.fields[0]) == "cell_id"
            ),
            None,
        )
        data_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 2
                and _normalised_field_name(op.fields[0]) == "cell_id"
                and _parse_implied_do(op.fields[1].strip()) is not None
            ),
            None,
        )
        if count_op is None or data_op is None:
            return None, "tvheads.gw missing row-count/data runtime-arity reads"

        cell_fields, _cell_type, err = self._resolve_field_expr(data_op.fields[0], proc)
        if err:
            return None, err
        implied = _parse_implied_do(data_op.fields[1].strip())
        if implied is None or len(implied[0]) != 1:
            return None, "tvheads.gw implied-do runtime-arity read had unexpected shape"
        head_fields, _head_type, err = self._resolve_field_expr(implied[0][0], proc)
        if err:
            return None, err
        if len(cell_fields) != 1 or len(head_fields) != 1:
            return None, "tvheads.gw runtime-arity fields did not resolve to scalar fields"

        sections = [
            RuntimeAritySection(
                name="row_count_pass",
                fields=[],
                count_source="until_eof_group",
                reader_line=count_op.location.line,
            ),
            RuntimeAritySection(
                name="head_rows",
                fields=[
                    RuntimeArityField(cell_fields[0]),
                    RuntimeArityField(
                        head_fields[0],
                        count_source="time:nbyr",
                        count_expr="time%nbyr",
                    ),
                ],
                count_source="row_count_pass",
                reader_line=data_op.location.line,
            ),
        ]
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_ponds_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1 and _normalised_field_name(op.fields[0]) == "dum_id"
            ),
            None,
        )
        data_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) >= 9
                and _normalised_field_name(op.fields[0]) == "id"
                and _parse_implied_do(op.fields[-1].strip()) is not None
            ),
            None,
        )
        if count_op is None or data_op is None:
            return None, "ponds.gw missing row-count/data runtime-arity reads"

        section_fields: list[RuntimeArityField] = []
        for field_expr in data_op.fields[:-1]:
            fields, _field_type, err = self._resolve_field_expr(field_expr, proc)
            if err:
                return None, err
            if len(fields) != 1:
                return None, "ponds.gw row field did not resolve to scalar field"
            section_fields.append(RuntimeArityField(fields[0]))
        implied = _parse_implied_do(data_op.fields[-1].strip())
        if implied is None or len(implied[0]) != 1:
            return None, "ponds.gw implied-do runtime-arity read had unexpected shape"
        array_fields, _array_type, err = self._resolve_field_expr(implied[0][0], proc)
        if err:
            return None, err
        if len(array_fields) != 1:
            return None, "ponds.gw concentration field did not resolve to scalar field"
        section_fields.append(
            RuntimeArityField(
                array_fields[0],
                count_source="gwflow:gw_nsolute",
                count_expr="gw_nsolute",
            )
        )

        sections = [
            RuntimeAritySection(
                name="row_count_pass",
                fields=[],
                count_source="until_eof_group",
                reader_line=count_op.location.line,
            ),
            RuntimeAritySection(
                name="pond_rows",
                fields=section_fields,
                count_source="row_count_pass",
                reader_line=data_op.location.line,
            ),
        ]
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_gwflow_canal_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 2
                and _normalised_field_name(op.fields[0]) == "canal_id"
                and _normalised_field_name(op.fields[1]) == "obj_tot"
            ),
            None,
        )
        data_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 3
                and _normalised_field_name(op.fields[0]) == "canal_id"
                and _normalised_field_name(op.fields[1]) == "obj_tot"
                and _parse_implied_do(op.fields[2].strip()) is not None
            ),
            None,
        )
        if count_op is None or data_op is None:
            return None, "gwflow_canal.con missing row-count/data runtime-arity reads"

        prefix_fields: list[RuntimeArityField] = []
        for field_expr in data_op.fields[:2]:
            fields, _field_type, err = self._resolve_field_expr(field_expr, proc)
            if err:
                return None, err
            if len(fields) != 1:
                return None, "gwflow_canal.con prefix field did not resolve to scalar field"
            prefix_fields.append(RuntimeArityField(fields[0]))

        repeat_fields: list[RuntimeArityField] = []
        for field_name in ("cell_num", "length", "stage"):
            vartype = self.resolve_var_type(field_name, proc)
            repeat_fields.append(
                RuntimeArityField(
                    FieldSpec(
                        fortran_name=field_name,
                        fortran_type=base_type_word(vartype),
                        numeric=is_numeric_type(vartype),
                        units=None,
                        doc=None,
                    )
                )
            )

        sections = [
            RuntimeAritySection(
                name="canal_header_rows",
                fields=prefix_fields,
                count_source="until_eof_group",
                reader_line=count_op.location.line,
            ),
            RuntimeAritySection(
                name="canal_connection_rows",
                fields=prefix_fields,
                count_source="canal_header_rows",
                reader_line=data_op.location.line,
                repeat_source="canal_header_rows:obj_tot",
                repeat_expr="obj_tot",
                repeat_fields=repeat_fields,
            ),
        ]
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_name_plus_variable_array_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
        *,
        filename: str,
        array_section_name: str,
        array_field_name: str,
        array_count_source: str,
        array_count_expr: str,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1
                and op.fields[0].strip().lower() in _THROWAWAY_TARGETS
                and re.search(
                    r"do\s+while\s*\(\s*eof\s*==\s*0\s*\)",
                    op.condition or "",
                    re.I,
                )
            ),
            None,
        )
        data_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 2
                and (
                    _normalised_field_name(op.fields[0]) == "name"
                    or (_normalised_field_name(op.fields[0]) or "").endswith("_name")
                )
                and (count_op is None or op.location.line > count_op.location.line)
            ),
            None,
        )
        if data_op is None:
            return None, f"{filename} missing name/{array_field_name} runtime-arity read"

        name_fields, _name_type, err = self._resolve_field_expr(data_op.fields[0], proc)
        if err:
            return None, err

        array_token = data_op.fields[1].strip()
        implied = _parse_implied_do(array_token)
        array_expr = array_token
        if implied is not None:
            items, _ivar, _lo, _hi = implied
            if len(items) != 1:
                return None, f"{filename} implied-do runtime-arity read had unexpected shape"
            array_expr = items[0]
        if _normalised_field_name(array_expr) != array_field_name:
            return None, f"{filename} missing name/{array_field_name} runtime-arity read"

        array_fields, _array_type, err = self._resolve_field_expr(array_expr, proc)
        if err:
            return None, err
        if len(name_fields) != 1 or len(array_fields) != 1:
            return None, f"{filename} runtime-arity fields did not resolve to scalar fields"

        count_section = "row_count_pass"
        count_section = "row_count_pass"
        sections: list[RuntimeAritySection] = []
        if count_op is not None:
            sections.append(
                RuntimeAritySection(
                    name=count_section,
                    fields=[],
                    count_source="until_eof_group",
                    reader_line=count_op.location.line,
                )
            )
        sections.extend(
            [
                RuntimeAritySection(
                    name="entry_name",
                    fields=[RuntimeArityField(name_fields[0])],
                    count_source=count_section,
                    reader_line=data_op.location.line,
                ),
                RuntimeAritySection(
                    name=array_section_name,
                    fields=[
                        RuntimeArityField(
                            array_fields[0],
                            count_source=array_count_source,
                            count_expr=array_count_expr,
                        )
                    ],
                    count_source=count_section,
                    reader_line=data_op.location.line,
                ),
            ]
        )
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_water_init_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
        *,
        filename: str,
        array_count_source: str,
        array_count_expr: str,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1
                and op.fields[0].strip().lower() in _THROWAWAY_TARGETS
                and re.search(
                    r"do\s+while\s*\(\s*eof\s*==\s*0\s*\)",
                    op.condition or "",
                    re.I,
                )
            ),
            None,
        )
        name_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1
                and (
                    _normalised_field_name(op.fields[0])
                    in {"name", "pest_init_name", "path_init_name"}
                )
                and (count_op is None or op.location.line > count_op.location.line)
            ),
            None,
        )
        array_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 3
                and _normalised_field_name(op.fields[0]) in _THROWAWAY_TARGETS
                and _normalised_field_name(op.fields[1]) == "water"
                and _normalised_field_name(op.fields[2]) == "benthic"
                and name_op is not None
                and op.location.line > name_op.location.line
            ),
            None,
        )
        if name_op is None or array_op is None:
            return None, f"{filename} missing name/water/benthic runtime-arity reads"

        name_fields, _name_type, err = self._resolve_field_expr(name_op.fields[0], proc)
        if err:
            return None, err
        water_fields, _water_type, err = self._resolve_field_expr(array_op.fields[1], proc)
        if err:
            return None, err
        benthic_fields, _benthic_type, err = self._resolve_field_expr(array_op.fields[2], proc)
        if err:
            return None, err
        if len(name_fields) != 1 or len(water_fields) != 1 or len(benthic_fields) != 1:
            return None, f"{filename} runtime-arity fields did not resolve to scalar fields"

        count_section = "row_count_pass"
        sections: list[RuntimeAritySection] = []
        if count_op is not None:
            sections.append(
                RuntimeAritySection(
                    name=count_section,
                    fields=[],
                    count_source="until_eof_group",
                    reader_line=count_op.location.line,
                )
            )
        sections.extend(
            [
                RuntimeAritySection(
                    name="entry_name",
                    fields=[RuntimeArityField(name_fields[0])],
                    count_source=count_section,
                    reader_line=name_op.location.line,
                ),
                RuntimeAritySection(
                    name="water_benthic_concentrations",
                    fields=[
                        RuntimeArityField(
                            water_fields[0],
                            count_source=array_count_source,
                            count_expr=array_count_expr,
                        ),
                        RuntimeArityField(
                            benthic_fields[0],
                            count_source=array_count_source,
                            count_expr=array_count_expr,
                        ),
                    ],
                    count_source=count_section,
                    reader_line=array_op.location.line,
                ),
            ]
        )
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )

    def _resolve_wal_constituent_runtime_arity_block(
        self,
        block: _IOBlock,
        proc: ProcedureDoc,
        *,
        filename: str,
    ) -> tuple[RuntimeAritySchema | None, str | None]:
        count_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) == 1 and op.fields[0].strip().lower() == "imax"
            ),
            None,
        )
        main_op = next(
            (
                op
                for op in block.reads
                if len(op.fields) >= 5
                and op.fields[0].strip().lower() == "i"
                and any(_normalised_field_name(field) == "name" for field in op.fields[1:])
                and (count_op is None or op.location.line > count_op.location.line)
            ),
            None,
        )
        if count_op is None or main_op is None:
            return None, f"{filename} missing count/main-row reads"

        count_fields, _count_type, err = self._resolve_field_expr(count_op.fields[0], proc)
        if err:
            return None, err
        main_fields: list[RuntimeArityField] = []
        for field_expr in main_op.fields:
            fields, _field_type, err = self._resolve_field_expr(field_expr, proc)
            if err:
                return None, err
            if len(fields) != 1:
                return None, f"{filename} main-row field did not resolve to scalar field"
            main_fields.append(RuntimeArityField(fields[0]))

        def optional_array_section(
            name: str,
            field_name: str,
            count_source: str,
            count_expr: str,
        ) -> RuntimeAritySection | None:
            op = next(
                (
                    read
                    for read in block.reads
                    if len(read.fields) == 1
                    and _normalised_field_name(read.fields[0]) == field_name
                    and read.location.line > main_op.location.line
                    and count_expr.lower() in (read.condition or "").lower()
                ),
                None,
            )
            if op is None:
                return None
            fields, _field_type, err = self._resolve_field_expr(op.fields[0], proc)
            if err or len(fields) != 1:
                return None
            return RuntimeAritySection(
                name=name,
                fields=[
                    RuntimeArityField(
                        fields[0],
                        count_source=count_source,
                        count_expr=count_expr,
                    )
                ],
                count_source="main_rows",
                reader_line=op.location.line,
            )

        sections = [
            RuntimeAritySection(
                name="entry_count",
                fields=[RuntimeArityField(count_fields[0])] if count_fields else [],
                count_source="literal_1",
                reader_line=count_op.location.line,
            ),
            RuntimeAritySection(
                name="main_rows",
                fields=main_fields,
                count_source="entry_count",
                reader_line=main_op.location.line,
            ),
        ]
        for section in (
            optional_array_section(
                "pest_concentrations",
                "pest",
                "constituents.cs:pests_count",
                "cs_db%num_pests",
            ),
            optional_array_section(
                "pathogen_concentrations",
                "path",
                "constituents.cs:paths_count",
                "cs_db%num_paths",
            ),
        ):
            if section is not None:
                sections.append(section)
        if len(sections) != 4:
            return None, f"{filename} missing pest/path runtime-arity reads"
        return (
            RuntimeAritySchema(
                sections=sections,
                reader=proc.location.path,
                reader_line=sections[0].reader_line,
            ),
            None,
        )
    def resolve_filename(self, expr: str | None) -> str | None:
        """Resolve an open ``file=`` expression to a concrete filename."""
        if not expr:
            return None
        text = expr.strip().strip("`'\"")
        if "%" in text:
            return self.instance_slot_map.get(text.lower())
        if _LITERAL_FILE_RE.match(text):
            return text
        return None

    def resolve_dummy_arg_filenames(self, proc: ProcedureDoc, expr: str) -> list[str]:
        """Resolve a filename opened via one of ``proc``'s own dummy arguments.

        Each call site may pass a different filename for the same argument
        position (e.g. ``call hyd_read_connect(in_con%hru_con, ...)`` and
        ``call hyd_read_connect(in_con%aqu_con, ...)``); every filename that
        resolves shares this procedure's schema, so all are returned.
        """
        name = expr.strip()
        lowered_args = [a.lower() for a in proc.args]
        if name.lower() not in lowered_args:
            return []
        index = lowered_args.index(name.lower())
        filenames: list[str] = []
        seen: set[str] = set()
        for args in self.call_args_by_callee.get(proc.name.lower(), []):
            if index >= len(args) or "=" in args[index]:
                continue  # out of range, or a keyword argument at this position
            resolved = self.resolve_filename(args[index])
            if resolved and resolved not in seen:
                seen.add(resolved)
                filenames.append(resolved)
        return filenames


@dataclass(slots=True)
class ReaderResult:
    filename: str
    reader: str
    schema: ReadSchema
    # Other genuinely distinct record shapes this same open-block also reads
    # (see ``_select_block_schemas``) -- e.g. print.prt's csvout/crop_yld/
    # objects groups, discarded before because only the single richest
    # candidate survived. Never a peek/reread of ``schema`` itself; those
    # collapse into one during selection. Empty for the overwhelming common
    # case of a block with exactly one record shape.
    extra_blocks: list[ReadSchema] = field(default_factory=list)


@dataclass(slots=True)
class DecisionTableResult:
    filename: str
    reader: str
    schema: DecisionTableSchema


@dataclass(slots=True)
class MultiRecordResult:
    filename: str
    reader: str
    schema: MultiRecordSchema


@dataclass(slots=True)
class MultiSectionResult:
    filename: str
    reader: str
    schema: MultiSectionSchema



@dataclass(slots=True)
class RuntimeArityResult:
    filename: str
    reader: str
    schema: RuntimeAritySchema

@dataclass(slots=True)
class _IOBlock:
    """One ``open`` and the reads that belong to it, in source order.

    A procedure that opens several files in sequence (e.g. ``gwflow_read``
    opening 44 files, one at a time, reusing the same unit variable for each)
    reuses the same unit number across many unrelated files. Grouping by unit
    *number* alone would merge all of them into one; a block instead resets
    every time that unit is re-opened, so each file gets its own schema.
    """

    open: IOOperation | None
    reads: list[IOOperation] = field(default_factory=list)


def _procedure_io_blocks(proc: ProcedureDoc) -> list[_IOBlock]:
    """Split a procedure's I/O into one block per ``open`` (in source order).

    Reads are attached to the most recent ``open`` on the same unit. A read
    on a unit with no preceding ``open`` in this procedure (rare -- e.g. a
    unit opened by a caller) lands in a trailing block with no ``open``,
    which falls back to trying every open in the procedure when resolving a
    filename, matching the old whole-procedure fallback behaviour.

    Internal reads -- ``read(a_character_variable(n), *) target``, parsing a
    value already split out of some other record -- never match a unit at
    all (their "unit" is a parenthesized expression, never a plain
    identifier or literal like a real file unit is -- checked against the
    whole pinned source: zero exceptions). They belong to whichever file is
    currently being processed, so they attach to the most recently opened
    block regardless of unit, rather than either matching per-unit (they
    never would) or falling into the shared orphan bucket, where a "try any
    open in the procedure" filename fallback would attribute them -- wrongly
    -- to whichever file the procedure happens to open first.
    """
    blocks: list[_IOBlock] = []
    current_by_unit: dict[str, _IOBlock] = {}
    current: _IOBlock | None = None
    orphan: _IOBlock | None = None
    for op in proc.io:
        if op.kind == "open":
            block = _IOBlock(open=op)
            blocks.append(block)
            current = block
            if op.unit:
                current_by_unit[op.unit] = block
        elif op.kind == "read":
            if op.unit and "(" in op.unit:
                if current is not None:
                    current.reads.append(op)
                continue
            block = current_by_unit.get(op.unit) if op.unit else None
            if block is None:
                if orphan is None:
                    orphan = _IOBlock(open=None)
                    blocks.append(orphan)
                block = orphan
            block.reads.append(op)
    return blocks


def _schema_rank(schema: ReadSchema) -> tuple[bool, int]:
    """Order candidate schemas for the same block: a repeat group or a set of
    tagged variants always beats a plain prefix of equal or greater length
    (either describes strictly more of the record), and otherwise more
    columns beats fewer."""
    repeat_len = len(schema.repeat.fields) if schema.repeat else 0
    variant_len = sum(len(v.fields) for v in schema.variants)
    structured = schema.repeat is not None or bool(schema.variants)
    return (structured, len(schema.fields) + repeat_len + variant_len)


def _field_signature(schema: ReadSchema) -> tuple[tuple[str, str], ...]:
    """The plain (fixed-prefix) field name/type sequence, ignoring any
    variable-length repeat or tagged-variant tail.

    This is the only signal available for telling "two reads of the same
    record" apart from "two reads of different records" once a repeat tail is
    stripped out: two reads of literally the same record (a peek, then the
    full backspace+reread) always share a field-name-identical prefix, while
    two genuinely different parts of a file's layout never do -- SWAT+
    component names are effectively unique per record across the whole pinned
    source tree, zero exceptions found.
    """
    return tuple((f.fortran_name, f.fortran_type) for f in schema.fields)


def _same_record(a: ReadSchema, b: ReadSchema) -> bool:
    """Do ``a`` and ``b`` describe two reads of the SAME record (one a
    positional prefix -- a peek -- of the other, or identical), rather than
    two independent parts of the file's layout?

    Gated on the plain field signature (see ``_field_signature``); an empty
    signature never counts as a "prefix" of anything (a schema with no plain
    fields -- e.g. an all-tagged/variant record) since an empty tuple is
    trivially a prefix of every sequence, which would otherwise collapse it
    into whichever other candidate happens to be compared first.
    """
    sig_a, sig_b = _field_signature(a), _field_signature(b)
    if not sig_a or not sig_b:
        return sig_a == sig_b
    shorter, longer = (sig_a, sig_b) if len(sig_a) <= len(sig_b) else (sig_b, sig_a)
    return longer[: len(shorter)] == shorter


def _select_block_schemas(candidates: list[ReadSchema]) -> list[ReadSchema]:
    """Reduce a block's per-read candidate schemas to the distinct record
    shapes it actually contains, in source order.

    A block that does several unrelated sequential reads after one ``open``
    (print.prt's csvout/crop_yld/objects groups, each its own ``read``
    statement) has one genuinely distinct candidate per group; a block that
    peeks a record's prefix then backspaces and rereads it in full has two
    candidates for the SAME record. ``_same_record`` tells them apart by
    field-name prefix, so this keeps every distinct record shape but
    collapses each same-record group down to its single richest candidate
    (by ``_schema_rank`` -- unchanged from the prior global selection, just
    scoped to candidates that are actually reads of one another instead of
    applied across the whole block).
    """
    kept: list[ReadSchema] = []
    for schema in candidates:
        for index, existing in enumerate(kept):
            if _same_record(schema, existing):
                if _schema_rank(schema) > _schema_rank(existing):
                    kept[index] = schema
                break
        else:
            kept.append(schema)
    return kept


def analyze_procedure(
    proc: ProcedureDoc, resolver: SchemaResolver
) -> tuple[list[ReaderResult], str | None]:
    """Find the file(s) a procedure reads and their column schemas.

    A procedure may open and read more than one file in sequence (a shared
    unit reopened for each), so this pairs each ``open`` with the reads that
    follow it -- rather than picking one "best" schema for the whole
    procedure -- and returns one result per file. A procedure whose ``open``
    names one of its own dummy arguments (a reader shared across several
    input files, parameterized by its caller) likewise resolves to one
    result per distinct filename supplied at a call site, all sharing that
    block's schema.

    Returns ``(results, None)`` when at least one file+schema resolved.
    Returns ``([], reason)`` when a data read was found but no file or schema
    resolved, or ``([], None)`` when the procedure reads no database rows.
    """
    blocks = [b for b in _procedure_io_blocks(proc) if b.reads]
    if not blocks:
        return [], None

    results: list[ReaderResult] = []
    unresolved_reason: str | None = None
    for block in blocks:
        candidates: list[ReadSchema] = []
        block_reason: str | None = None
        # A record with a data-dependent tail is often peeked at first (read
        # the fixed prefix, backspace, re-read the whole record). The peek on
        # its own looks like an ordinary intrinsic record read, so suppress
        # that fallback for the whole block rather than publish a prefix as if
        # it were the record.
        variable_length = any(
            _IMPLIED_DO_RE.match(raw.strip()) for op in block.reads for raw in op.fields
        )
        for op in block.reads:
            # An internal read (from a character array element, e.g.
            # `read(split_fields(N),*) var`) targets one column of a
            # hand-parsed record; evaluated alone it looks like an ordinary
            # one-field data read via the normal chain-resolution path, which
            # would publish a misleading single-column schema for what is
            # really a many-column record. Skip it here -- the block-level
            # positional-extraction attempt below is the only way these
            # contribute a candidate, and only once collected together.
            if op.unit and "(" in op.unit:
                continue
            # The read carrying the implied-do gets a shot at the richer
            # prefix+repeat resolution; every other read (including the
            # earlier peek at just the prefix, if the reader backspaces and
            # re-reads) goes through the normal path with the intrinsic
            # fallback suppressed for the whole block, per the comment above.
            if variable_length and any(_IMPLIED_DO_RE.match(t.strip()) for t in op.fields):
                schema, reason = resolver.resolve_variable_length_read(op, proc, block.reads)
            else:
                schema, reason = resolver.read_to_schema(
                    op, proc, allow_intrinsic_record=not variable_length
                )
            if schema:
                candidates.append(schema)
            if reason and block_reason is None:
                block_reason = reason

        if any(op.unit and "(" in op.unit for op in block.reads):
            schema, reason = resolver.resolve_positional_extraction(block, proc)
            if schema:
                candidates.append(schema)
            if reason and block_reason is None:
                block_reason = reason

        # A block that does several unrelated sequential reads after one
        # `open` (print.prt's csvout/crop_yld/objects groups, each its own
        # `read` statement) has one real candidate per group; picking a
        # single "best" here -- as this used to -- silently threw the rest
        # away. `_select_block_schemas` keeps every distinct record shape,
        # collapsing only actual peek/reread pairs of the SAME record down to
        # their richest candidate.
        block_schemas = _select_block_schemas(candidates)
        if not block_schemas:
            if block_reason and unresolved_reason is None:
                unresolved_reason = block_reason
            continue

        filenames = _filenames_for_block(block, proc, resolver)
        if not filenames:
            if unresolved_reason is None:
                expr = (block.open.file_expr or block.open.file_resolved) if block.open else None
                unresolved_reason = f"could not resolve filename expression '{expr}'"
            continue

        # The richest block stays the primary schema (identical to the old
        # single-`best` selection for every file that only ever had one
        # candidate), any others ride along as `extra_blocks`.
        primary = max(block_schemas, key=_schema_rank)
        extra_blocks = [schema for schema in block_schemas if schema is not primary]
        results.extend(
            ReaderResult(
                filename=name, reader=proc.location.path, schema=primary, extra_blocks=extra_blocks
            )
            for name in filenames
        )

    if not results:
        return ([], unresolved_reason) if unresolved_reason else ([], None)
    return results, None


def _filenames_for_block(
    block: _IOBlock, proc: ProcedureDoc, resolver: SchemaResolver
) -> list[str]:
    """The file(s) this block's data belongs to."""
    if block.open is not None:
        return _resolve_open_filenames(block.open, proc, resolver)
    # No open for this block specifically -- fall back to any resolvable open
    # in the procedure, as when there was no per-block attribution at all.
    # If a block has its own open but that filename is runtime/unresolvable,
    # do not borrow a sibling open's filename.
    for op in proc.io:
        if op.kind == "open":
            names = _resolve_open_filenames(op, proc, resolver)
            if names:
                return names
    return []


def _resolve_open_filenames(
    op: IOOperation, proc: ProcedureDoc, resolver: SchemaResolver
) -> list[str]:
    expr = op.file_expr or op.file_resolved
    name = resolver.resolve_filename(expr)
    if name:
        override = _OPEN_FILENAME_OVERRIDES.get(
            (proc.location.path.lower(), op.location.line, name.lower())
        )
        if override:
            return list(override)
        return [name]
    if expr:
        return resolver.resolve_dummy_arg_filenames(proc, expr)
    return []


def _open_file_expr(proc: ProcedureDoc) -> str | None:
    for op in proc.io:
        if op.kind == "open" and (op.file_expr or op.file_resolved):
            return op.file_expr or op.file_resolved
    return None


def _in_do_loop(io_op: IOOperation) -> bool:
    """Is this read nested inside a ``do`` loop (i.e. run once per record)?

    The scanner records the enclosing ``if`` / ``select case`` / ``do``
    constructs on each I/O operation as a ``>``-joined trail.
    """
    return any(_DO_LOOP_RE.match(part.strip()) for part in (io_op.condition or "").split(">"))


def _normalised_field_name(expr: str) -> str | None:
    match = _FIELD_RE.match(expr.strip())
    if match is None:
        return None
    chain, _last_is_element = _parse_component_chain(match.group(2) or "")
    return (chain[-1] if chain else match.group(1)).lower()


def _parse_component_chain(chain_text: str) -> tuple[list[str], bool]:
    """Split a ``%a%b(k)`` chain into ``(component_names, last_is_element)``.

    Subscripts are stripped from the names so they match component
    declarations, but whether the *final* component carried an explicit index
    in the read is returned separately: ``x%arr(k)`` reads one element of a
    fixed-size array ``arr``, not the whole array, and the caller must not
    array-expand it. An intermediate subscript (``x%ly(j)%z``) is just
    array-of-derived-type indexing and doesn't affect the final scalar.
    """
    parts = [part for part in chain_text.split("%") if part.strip()]
    names = [re.sub(r"\([^()]*\)", "", part).strip() for part in parts]
    last_is_element = bool(parts) and "(" in parts[-1]
    return names, last_is_element


def _split_field_tokens(tokens: list[str]) -> list[tuple[str, list[str]]] | None:
    """Split each read-field token into ``(base, %component_chain)``.

    Returns ``None`` if any token isn't a plain field reference (e.g. it's
    itself an implied-do, which the caller must peel off first).
    """
    parsed: list[tuple[str, list[str]]] = []
    for raw in tokens:
        match = _FIELD_RE.match(raw.strip())
        if not match:
            return None
        base = match.group(1)
        chain, _last_is_element = _parse_component_chain(match.group(2) or "")
        parsed.append((base, chain))
    return parsed


def _do_depth(io_op: IOOperation) -> int:
    """How many ``do`` loops enclose a read, from its condition trail.

    Counts every ``do`` segment (counted or ``do while``) in the ``>``-joined
    trail. Absolute value is uninteresting; the relative depth is what tells a
    header record from the more deeply nested sub-records that follow it.
    """
    return sum(
        1 for part in (io_op.condition or "").split(">") if re.match(r"do\b", part.strip(), re.I)
    )


def _innermost_do_bound(io_op: IOOperation) -> str | None:
    """The upper bound of the innermost ``do <v> = <lo>, <hi>`` enclosing a read.

    The scanner records the enclosing constructs on each I/O operation as a
    ``>``-joined trail; this returns ``hi`` of the last counted ``do`` in that
    trail (``mlyr`` for ``... > do j = 1, mlyr``), or None if the innermost
    loop isn't a counted do-loop (a ``do while``, or no loop at all).
    """
    for part in reversed((io_op.condition or "").split(">")):
        segment = part.strip()
        match = re.match(r"do\s+[a-z_]\w*\s*=\s*[^,]+,\s*(.+)$", segment, re.I)
        if match:
            return match.group(1).strip()
        if re.match(r"do\b", segment, re.I):
            return None  # innermost loop is a do-while / unbounded do -- not this
    return None


# `if (<expr> == "<literal>") then` -- the only condition shape
# _find_if_else_read_pairs recognizes as a tag dispatch. An `elseif` chain or
# a non-equality condition is out of scope and simply won't match.
_TAG_IF_RE = re.compile(r'^if\s*\(\s*(.+?)\s*==\s*["\'](.*)["\']\s*\)\s*then$', re.I)


def _find_if_else_read_pairs(
    reads: list[IOOperation],
) -> list[tuple[IOOperation, IOOperation, str, str]]:
    """Pair reads that are the two branches of one ``if/else`` tag dispatch.

    Relies on the scanner's else/elseif tracking (``_update_condition_stack``
    in fortran.py): two reads at the same nesting level get condition trails
    that are identical except for the last segment, which for the ``if``
    branch is ``if (<expr> == "<lit>") then`` and for the ``else`` branch is
    that same text plus `` / else`` (nothing more -- an ``elseif`` in between,
    or more than one read per branch, is declined rather than guessed).

    Returns ``(if_read, else_read, discriminator_expr, literal)`` for every
    such pair found.
    """
    by_branch_root: dict[tuple[tuple[str, ...], str], list[tuple[IOOperation, str, str, str]]] = {}
    for op in reads:
        if op.kind != "read":
            continue
        trail = [s.strip() for s in (op.condition or "").split(">") if s.strip()]
        if not trail:
            continue
        *outer, last = trail
        if " / " not in last:
            root_text, branch = last, "if"
        else:
            head, tail = last.split(" / ", 1)
            if tail.strip().lower() != "else":
                continue
            root_text, branch = head.strip(), "else"
        match = _TAG_IF_RE.match(root_text)
        if not match:
            continue
        key = (tuple(outer), root_text.lower())
        by_branch_root.setdefault(key, []).append(
            (op, branch, match.group(1).strip(), match.group(2))
        )
    pairs: list[tuple[IOOperation, IOOperation, str, str]] = []
    for entries in by_branch_root.values():
        ifs = [e for e in entries if e[1] == "if"]
        elses = [e for e in entries if e[1] == "else"]
        if len(ifs) == 1 and len(elses) == 1:
            if_op, _b1, discriminator, literal = ifs[0]
            else_op, _b2, _d2, _l2 = elses[0]
            pairs.append((if_op, else_op, discriminator, literal))
    return pairs


def _parse_implied_do(token: str) -> tuple[list[str], str, str, str] | None:
    """Parse ``(item1, item2, ..., var = lo, hi)`` into ``(items, var, lo, hi)``."""
    token = token.strip()
    if not (token.startswith("(") and token.endswith(")")):
        return None
    parts = split_top_level_commas(token[1:-1])
    if len(parts) < 3:
        return None
    hi = parts[-1].strip()
    var_lo = parts[-2].strip()
    match = re.match(r"^([a-z_]\w*)\s*=\s*(.+)$", var_lo, re.I)
    if not match:
        return None
    var, lo = match.group(1), match.group(2).strip()
    items = [p.strip() for p in parts[:-2]]
    return (items, var, lo, hi) if items else None


def _find_count_field(
    hi: str, prefix_parsed: list[tuple[str, list[str]]], proc: ProcedureDoc
) -> str | None:
    """The prefix column, if any, that supplies an implied-do's repeat count.

    Direct: the bound is itself one of the prefix's bare (no %chain) targets
    (``nspu`` in ``k, name, area_ha, nspu``). Indirect: the bound is a local
    variable assigned earlier in the procedure from one of the prefix's
    %chain targets (SWAT+'s ``nout = ob(i)%src_tot`` idiom for ``.con``
    files). Anything else -- an externally-governed count such as a
    constituent-database size -- is not found here, by design.
    """
    hi_lower = hi.strip().lower()
    for base, chain in prefix_parsed:
        if not chain and base.lower() == hi_lower:
            return base
    assign_re = re.compile(rf"^\s*{re.escape(hi)}\s*=\s*(.+)$", re.I)
    for assignment in proc.assignments:
        match = assign_re.match(assignment.raw or "")
        if not match:
            continue
        rhs_match = _FIELD_RE.match(match.group(1).strip())
        if not rhs_match:
            continue
        rhs_chain_text = rhs_match.group(2) or ""
        rhs_chain = [
            re.sub(r"\([^()]*\)", "", part).strip()
            for part in rhs_chain_text.split("%")
            if part.strip()
        ]
        if not rhs_chain:
            continue
        for base, chain in prefix_parsed:
            if chain and chain[-1].lower() == rhs_chain[-1].lower():
                return chain[-1]
    return None


def _unwrap_trim_adjustl(expr: str) -> str:
    """Strip any number of enclosing ``trim(...)`` / ``adjustl(...)`` calls."""
    expr = expr.strip()
    while True:
        match = re.match(r"^(?:trim|adjustl)\s*\((.*)\)$", expr, re.I)
        if not match:
            return expr
        expr = match.group(1).strip()


def _positional_assignment_targets(
    proc: ProcedureDoc, array_name: str, line_lo: int, line_hi: int
) -> dict[int, str]:
    """Columns copied via ``VAR = trim(fields_array(N))`` rather than a read.

    Scoped to a line range (a block's own reads span) so an assignment from
    an unrelated, later use of the same array elsewhere in a long shared
    procedure like ``gwflow_read`` can't be picked up by mistake.
    """
    out: dict[int, str] = {}
    for assignment in proc.assignments:
        line = assignment.location.line
        if not (line_lo <= line <= line_hi):
            continue
        match = _ASSIGNMENT_RE.match(assignment.raw or "")
        if not match:
            continue
        target, rhs = match.group(1), _unwrap_trim_adjustl(match.group(2))
        index_match = re.match(rf"^{re.escape(array_name)}\(\s*(\d+)\s*\)$", rhs, re.I)
        if index_match:
            out[int(index_match.group(1))] = target
    return out


def _strip_string_literal(text: str | None) -> str | None:
    if not text:
        return None
    stripped = text.strip()
    if len(stripped) >= 2 and stripped[0] in {"'", '"'} and stripped[-1] == stripped[0]:
        inner = stripped[1:-1]
        return inner if inner.strip() else None
    return None


def _call_actual_args(raw: str, call_name: str) -> list[str]:
    """Extract the actual-argument list from a ``call <call_name>(...)`` statement."""
    match = re.search(rf"\bcall\s+{re.escape(call_name)}\b", raw, re.I)
    if not match:
        return []
    rest = raw[match.end():].lstrip()
    if not rest.startswith("("):
        return []
    depth = 0
    quote: str | None = None
    for i, char in enumerate(rest):
        if quote:
            if char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return parse_args(rest[1:i])
    return []


def analyze_decision_tables(
    project: ProjectIndex, resolver: SchemaResolver
) -> tuple[list[DecisionTableResult], dict[str, str]]:
    """Find every decision-table (``*.dtl``) reader and its resolved schema.

    Tries every I/O block in every procedure -- mirroring how
    :func:`analyze_procedure` walks blocks for the ordinary per-file schemas
    -- but only via :meth:`SchemaResolver.resolve_decision_table_block`,
    which declines (``None, None``) any block that isn't this specific
    shape. A block that *does* look like a decision table's header but then
    fails to resolve a component is attributed to whichever target filename
    its ``open`` names, same as the ordinary-schema unresolved-reason path.
    """
    results: list[DecisionTableResult] = []
    unresolved_reasons: dict[str, str] = {}
    for proc in project.procedures:
        for block in _procedure_io_blocks(proc):
            if not block.reads:
                continue
            schema, reason = resolver.resolve_decision_table_block(block, proc)
            if schema is None:
                if reason:
                    for name in _filenames_for_block(block, proc, resolver):
                        if name in DECISION_TABLE_FILES:
                            unresolved_reasons.setdefault(name, reason)
                continue
            for name in _filenames_for_block(block, proc, resolver):
                results.append(
                    DecisionTableResult(filename=name, reader=proc.location.path, schema=schema)
                )
    return results, unresolved_reasons


def build_decision_tables(
    project: ProjectIndex,
    resolver: SchemaResolver,
    *,
    targets: tuple[str, ...] = DECISION_TABLE_FILES,
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """Build the ``decision_tables`` / ``decision_tables_unresolved`` payload sections."""
    results, unresolved_reasons = analyze_decision_tables(project, resolver)
    resolved: dict[str, DecisionTableResult] = {}
    for result in results:
        resolved.setdefault(result.filename, result)  # first (sorted-order) reader wins

    files: dict[str, Any] = {}
    unresolved: list[dict[str, str]] = []
    for filename in targets:
        result = resolved.get(filename)
        if result is None:
            reason = unresolved_reasons.get(filename, "reader not found for filename")
            unresolved.append({"file": filename, "reason": reason})
            continue
        files[filename] = result.schema.to_dict()
    return dict(sorted(files.items())), sorted(unresolved, key=lambda e: e["file"])


def analyze_multi_records(
    project: ProjectIndex, resolver: SchemaResolver
) -> tuple[list[MultiRecordResult], dict[str, str]]:
    """Find every header-plus-sub-blocks reader and its resolved schema.

    Same walk as :func:`analyze_decision_tables`, via
    :meth:`SchemaResolver.resolve_multi_record_block`, which declines any
    block that isn't the header+sub-block shape.
    """
    results: list[MultiRecordResult] = []
    unresolved_reasons: dict[str, str] = {}
    for proc in project.procedures:
        for block in _procedure_io_blocks(proc):
            if not block.reads:
                continue
            schema, reason = resolver.resolve_multi_record_block(block, proc)
            if schema is None:
                if reason:
                    for name in _filenames_for_block(block, proc, resolver):
                        if name in MULTI_RECORD_FILES:
                            unresolved_reasons.setdefault(name, reason)
                continue
            for name in _filenames_for_block(block, proc, resolver):
                results.append(
                    MultiRecordResult(filename=name, reader=proc.location.path, schema=schema)
                )
    return results, unresolved_reasons


def build_multi_records(
    project: ProjectIndex,
    resolver: SchemaResolver,
    *,
    targets: tuple[str, ...] = MULTI_RECORD_FILES,
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """Build the ``multi_record`` / ``multi_record_unresolved`` payload sections."""
    results, unresolved_reasons = analyze_multi_records(project, resolver)
    resolved: dict[str, MultiRecordResult] = {}
    for result in results:
        resolved.setdefault(result.filename, result)  # first (sorted-order) reader wins

    files: dict[str, Any] = {}
    unresolved: list[dict[str, str]] = []
    for filename in targets:
        result = resolved.get(filename)
        if result is None:
            reason = unresolved_reasons.get(filename, "reader not found for filename")
            unresolved.append({"file": filename, "reason": reason})
            continue
        files[filename] = result.schema.to_dict()
    return dict(sorted(files.items())), sorted(unresolved, key=lambda e: e["file"])


def analyze_multi_sections(
    project: ProjectIndex, resolver: SchemaResolver
) -> tuple[list[MultiSectionResult], dict[str, str]]:
    """Find multi-section station-list readers and their resolved schemas."""
    results: list[MultiSectionResult] = []
    unresolved_reasons: dict[str, str] = {}
    for proc in project.procedures:
        for block in _procedure_io_blocks(proc):
            if not block.reads:
                continue
            schema, reason = resolver.resolve_multi_section_block(block, proc)
            if schema is None:
                if reason:
                    for name in _filenames_for_block(block, proc, resolver):
                        if name in MULTI_SECTION_FILES:
                            unresolved_reasons.setdefault(name, reason)
                continue
            for name in _filenames_for_block(block, proc, resolver):
                results.append(
                    MultiSectionResult(filename=name, reader=proc.location.path, schema=schema)
                )
    return results, unresolved_reasons


def build_multi_sections(
    project: ProjectIndex,
    resolver: SchemaResolver,
    *,
    targets: tuple[str, ...] = MULTI_SECTION_FILES,
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """Build the ``multi_section`` / ``multi_section_unresolved`` payload sections."""
    results, unresolved_reasons = analyze_multi_sections(project, resolver)
    resolved: dict[str, MultiSectionResult] = {}
    for result in results:
        resolved.setdefault(result.filename, result)

    files: dict[str, Any] = {}
    unresolved: list[dict[str, str]] = []
    for filename in targets:
        result = resolved.get(filename)
        if result is None:
            reason = unresolved_reasons.get(filename, "reader not found for filename")
            unresolved.append({"file": filename, "reason": reason})
            continue
        files[filename] = result.schema.to_dict()
    return dict(sorted(files.items())), sorted(unresolved, key=lambda e: e["file"])



def analyze_runtime_arity(
    project: ProjectIndex, resolver: SchemaResolver
) -> tuple[list[RuntimeArityResult], dict[str, str]]:
    """Find curated runtime-arity readers and their resolved schemas."""
    results: list[RuntimeArityResult] = []
    unresolved_reasons: dict[str, str] = {}
    for proc in project.procedures:
        for block in _procedure_io_blocks(proc):
            if not block.reads:
                continue
            schema, reason = resolver.resolve_runtime_arity_block(block, proc)
            if schema is None:
                if reason:
                    for name in _filenames_for_block(block, proc, resolver):
                        if name in RUNTIME_ARITY_FILES:
                            unresolved_reasons.setdefault(name, reason)
                continue
            for name in _filenames_for_block(block, proc, resolver):
                if name in RUNTIME_ARITY_FILES:
                    results.append(
                        RuntimeArityResult(
                            filename=name, reader=proc.location.path, schema=schema
                        )
                    )
    return results, unresolved_reasons


def build_runtime_arity(
    project: ProjectIndex,
    resolver: SchemaResolver,
    *,
    targets: tuple[str, ...] = RUNTIME_ARITY_FILES,
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """Build the ``runtime_arity`` / ``runtime_arity_unresolved`` payload sections."""
    results, unresolved_reasons = analyze_runtime_arity(project, resolver)
    resolved: dict[str, RuntimeArityResult] = {}
    for result in results:
        resolved.setdefault(result.filename, result)

    files: dict[str, Any] = {}
    unresolved: list[dict[str, str]] = []
    for filename in targets:
        result = resolved.get(filename)
        if result is None:
            reason = unresolved_reasons.get(filename, "reader not found for filename")
            unresolved.append({"file": filename, "reason": reason})
            continue
        files[filename] = result.schema.to_dict()
    return dict(sorted(files.items())), sorted(unresolved, key=lambda e: e["file"])

def build_schema(
    project: ProjectIndex,
    *,
    swatplus_version: str,
    source_ref: str,
    generator: str,
    source_repository: str = SOURCE_REPOSITORY,
    targets: tuple[str, ...] = TARGET_FILES,
    generated_utc: str | None = None,
) -> dict[str, Any]:
    """Build the deterministic schema payload for the scanned project.

    ``generated_utc`` is the only non-deterministic field; pass None to omit it
    (byte-identical output). Everything else is a pure function of the source.
    """
    resolver = SchemaResolver(project)

    resolved: dict[str, ReaderResult] = {}
    unresolved_reasons: dict[str, str] = {}
    for proc in project.procedures:
        results, reason = analyze_procedure(proc, resolver)
        if results:
            # First reader to claim a filename wins (deterministic: procedures
            # are scanned in sorted file order).
            for result in results:
                resolved.setdefault(result.filename, result)
        elif reason is not None:
            # Attribute a reason to any target filename this proc references.
            name = resolver.resolve_filename(_open_file_expr(proc))
            if name and name in targets:
                unresolved_reasons.setdefault(name, reason)

    files: dict[str, Any] = {}
    unresolved: list[dict[str, str]] = []
    for filename in targets:
        result = resolved.get(filename)
        if result is None:
            reason = unresolved_reasons.get(
                filename, "reader not found for filename"
            )
            unresolved.append({"file": filename, "reason": reason})
            continue
        schema = result.schema
        entry: dict[str, Any] = {"reader": result.reader, **schema.to_dict()}
        if result.extra_blocks:
            # The block genuinely reads more than one distinct record shape
            # (print.prt's csvout/crop_yld/objects groups, each its own
            # `read` statement after the same `open`) -- every shape lives
            # here, in source order, `schema` included, so a consumer that
            # understands `blocks` gets the full layout. The top-level keys
            # above stay exactly what they were before this ever produced
            # more than one block, so a consumer that only reads `fields`
            # still gets an honest (if partial) schema instead of a key it
            # doesn't expect changing shape underneath it.
            entry["blocks"] = [s.to_dict() for s in (schema, *result.extra_blocks)]
        files[filename] = entry

    decision_tables, decision_tables_unresolved = build_decision_tables(project, resolver)
    multi_record, multi_record_unresolved = build_multi_records(project, resolver)
    multi_section, multi_section_unresolved = build_multi_sections(project, resolver)


    runtime_arity, runtime_arity_unresolved = build_runtime_arity(project, resolver)
    payload: dict[str, Any] = {
        "swatplus_version": swatplus_version,
        "source_repository": source_repository,
        "source_ref": source_ref,
        "generator": generator,
        "files": dict(sorted(files.items())),
        "unresolved": sorted(unresolved, key=lambda e: e["file"]),
        # A decision table's rows aren't a flat column list -- see
        # `DecisionTableSchema` -- so it gets its own section rather than an
        # entry in `files` above. Additive: a consumer that only reads
        # `files`/`unresolved` sees no change.
        "decision_tables": decision_tables,
        "decision_tables_unresolved": decision_tables_unresolved,
        # A multi-record file (header + count-driven sub-blocks -- see
        # `MultiRecordSchema`) likewise isn't a flat column list. Its own
        # section, same additive contract.
        "multi_record": multi_record,
        "multi_record_unresolved": multi_record_unresolved,
        # Multi-section files stack or reread distinct logical sections in one
        # physical file; keep them additive for consumers that only understand
        # flat files, decision tables, or header+block multi-record files.
        "multi_section": multi_section,
        "multi_section_unresolved": multi_section_unresolved,
        # Runtime-arity files contain fields whose width is governed by counts
        # defined at runtime outside the file, e.g. `constituents.cs`.
        "runtime_arity": runtime_arity,
        "runtime_arity_unresolved": runtime_arity_unresolved,
    }
    if generated_utc is not None:
        payload["generated_utc"] = generated_utc
    return payload


def dumps(payload: dict[str, Any]) -> str:
    """Serialise a schema payload deterministically (sorted keys, trailing NL)."""
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    """Delegate the module entry point to the configured public command."""
    import sys

    from swatplus_reference.cli import main as cli_main

    forwarded = list(argv) if argv is not None else sys.argv[1:]
    return cli_main(["schema", "build", *forwarded])


if __name__ == "__main__":
    raise SystemExit(main())
