---
kind: procedure
symbol: res_rel_conds
title: res_rel_conds
status: filled
source_hash: 23c9a7e7ea27b320
version_label: SWAT+ 62.0.0
args:
  ictbl: Selects which reservoir condition table in ctbl to evaluate.
  stor: Current reservoir storage value tested against table conditions named stor.
  inflo: Current inflow value tested against table conditions named inflo.
  pdsi: Current PDSI value tested against table conditions named pdsi.
locals:
  icon: Loop index for the top-level condition set and later for the selected module's subconditions;
    it tracks which condition block is being tested.
  modu: Module selector derived from the matched top-level condition action; it chooses which
    module-specific condition list to evaluate next.
  iscon: Inner-loop index over the individual subconditions within the current condition block.
uses:
  reservoir_conditions_module: reservoir_conditions_module supplies the shared decision-table
    storage and the result variables this routine reads and writes. res_rel_conds depends
    on ctbl to fetch condition clauses and action values, updates the shared hit flag while
    testing each clause, reads the shared day value for date-based rules, and writes release
    when no top-level rule matches.
  time_module: time_module matters because the routine evaluates table conditions on the current
    model day, and day is the integer state passed into cond_integer_c for day-based rule
    matching.
  hydrograph_module: hydrograph_module matters because this routine writes the selected release
    into ht2%flo. That shared hydrograph output is the value returned to the reservoir routing
    workflow as the computed outflow.
---

<!-- facts:header -->

Selects a reservoir release amount by testing table-defined conditions against storage, inflow, PDSI, and day.

## Bottom Line

res_rel_conds walks the reservoir condition table for the selected table index and looks for the first matching release rule. It checks the table's top-level conditions against the current storage, inflow, PDSI, and day, then uses the matched rule's action field to choose a module-specific subtable.

If no top-level condition matches, it forces release to zero and returns. If a module is selected but none of that module's subconditions match, it sets ht2%flo to zero; otherwise ht2%flo is loaded from the matched action value, which later reservoir routing uses as the release flow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

res_control calls res_rel_conds after it has selected the reservoir release table index in ictbl from res_dat(idat)%release. This routine then evaluates the applicable release conditions and sets the resulting outflow, either by forcing release to zero or by placing the chosen action into ht2%flo for later reservoir water-balance and routing steps.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the module selector and scan the top-level condition table. | The routine starts with modu set to zero, then loops over each top-level condition block in ctbl(ictbl)%conds. This is the first pass that decides which release rule, if any, applies to the current reservoir state. |
| 2. Assume a potential hit and test each clause in the current condition block. | For each condition block, hit is initialized to 'y' and each subcondition is evaluated by variable name. stor, inflo, and pdsi are checked with cond_real_c, while day is checked with cond_integer_c. Each call can invalidate the current block by changing hit. |
| 3. Stop at the first block that still hits. | If hit remains 'y' after all subconditions are tested, the routine exits the top-level loop immediately. That leaves icon pointing to the matching condition block. |
| 4. Return zero release when no top-level condition matched. | If icon advanced past the end of the top-level condition list, no rule matched, so release is set to 0. and the subroutine returns at once. |
| 5. Derive the module index from the matched action. | The matched condition block's action value is converted to an integer module selector, then incremented by one. This maps the condition-table action to the corresponding entry in ctbl(ictbl)%mods. |
| 6. Scan the selected module's subconditions. | The routine loops over the selected module's condition blocks, resets hit to 'y' for each one, and tests the module-specific clauses. Only inflo and stor are checked in this second stage, again through cond_real_c. |
| 7. Stop at the first module block that still hits. | If a module subcondition block stays matched after all of its tests, the loop exits and icon identifies the chosen module release action. |
| 8. Write the release flow or zero it out. | If no module block matched, ht2%flo is set to 0.; otherwise ht2%flo is assigned the matched action value from the module table. That value becomes the release flow output for downstream reservoir calculations. |
| 9. Return to the caller. | After the release flow is determined, the routine returns control to res_control. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_conditions_module] | `ctbl, hit, day, release` | `ctbl(ictbl)%num_conds, ctbl(ictbl)%conds(icon)%num_conds, ctbl(ictbl)%conds(icon)%scon(iscon)%var, ctbl(ictbl)%conds(icon)%scon(iscon)%op, ctbl(ictbl)%conds(icon)%scon(iscon)%val, ctbl(ictbl)%conds(icon)%action, ctbl(ictbl)%mods(modu)%num_conds, ctbl(ictbl)%mods(modu)%con(icon)%num_conds, ctbl(ictbl)%mods(modu)%con(icon)%scon(iscon)%var, ctbl(ictbl)%mods(modu)%con(icon)%scon(iscon)%op, ctbl(ictbl)%mods(modu)%con(icon)%scon(iscon)%val, ctbl(ictbl)%mods(modu)%con(icon)%action` |
| [sym:time_module] | `day` | `day` |
| [sym:hydrograph_module] | `ht2` | `ht2%flo` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hit` | When a top-level condition block fails to match any rule, or when the routine is still within a candidate block and a test disqualifies it, hit is reset/left as the shared match flag used by the condition-check helpers. | hit records whether the current set of conditions is still satisfied. cond_real_c and cond_integer_c use it as the shared pass/fail flag while res_rel_conds scans the condition table. |
| `release` | If icon advances past ctbl(ictbl)%num_conds after scanning the top-level condition blocks, meaning no block matched. | release is forced to 0. so the reservoir has no allowed release for the current state. |
| `ht2%flo` | If no module-specific condition block matches after scanning ctbl(ictbl)%mods(modu)%con(icon)%num_conds. | ht2%flo is set to 0. to suppress release when the selected module's subconditions are not satisfied. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 8:1.1.9 | Uncontrolled release V_flowout=V-V_pr when V-V_pr < q_rel*86400 | $V_{flowout}=V-V_{pr}$ | res_rel_conds.f90 uses condition-table lookup (ht2%flo=table value) â€” no explicit V-V_pr formula. V-V_pr < q_rel*86400 condition and release value encoded in input condition table. |
| 8:1.1.10 | Uncontrolled release V_flowout=q_rel*86400 when V-V_pr > q_rel*86400 | $V_{flowout}=q_{rel}*86400$ | Cap q_rel*86400 is a table-driven value; no explicit formula line. |
| 8:1.1.11 | Uncontrolled release condition V_em-V_pr < q_rel*86400 | $V_{em}-V_{pr}<q_{rel}*86400$ | Condition tested by input table; no explicit formula. |
| 8:1.1.12 | Uncontrolled release condition V_em-V_pr > q_rel*86400 | $V_{em}-V_{pr}>q_{rel}*86400$ | Condition tested by input table; no explicit formula. |

## Lineage

`res_rel_conds.f90` was introduced in `2405a68` (2024-07-16, "Fixing for Compiling") and has been changed in 3 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `res_rel_conds.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `c639a8c` (2024-07-24) — Revert "Some Fixes to get pesticides running."
- `2405a68` (2024-07-16) — Fixing for Compiling

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'res_rel_conds' has no extracted documentation comment.
- The provided Git Lineage Evidence reported no resolved commits for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
