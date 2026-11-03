<!-- fortran-ifx-index -->
## Fortran ifx Debug

This workspace has the **Fortran ifx Debug** extension installed. For
anything involving running or debugging the compiled model, use its MCP
tools rather than editing `launch.json` or guessing symbol names -- it
resolves Intel ifx-mangled Fortran symbols that a generic C++ debugger
cannot.

| Tool | Use it to |
|---|---|
| `start_fortran_debug` | Launch a debug session against the built executable |
| `set_fortran_breakpoint` / `plan_fortran_breakpoint` | Set, or preview, a breakpoint by source location or condition |
| `clear_fortran_breakpoints` | Remove breakpoints set this way |
| `debug_continue` / `debug_step` | Resume or step the running session |
| `debug_variables` / `debug_evaluate` | Inspect scope variables, or evaluate an expression, including derived-type fields and array sections |
| `debug_output` | Read what the program printed |
| `debug_crash_report` | Name the failing subroutine when a runtime error terminates the process before the debugger traps it |
| `stop_fortran_debug` | End the session |
<!-- fortran-ifx-index -->

## SWAT+ code facts and the user-docs input tables

For questions about what the SWAT+ Fortran code does with an input field (where a value is read or set, its unit,
whether the input has any effect), use these tools **before** grepping, then read only the source lines they point
to. Run them from the repo root:

- `.swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/field_evidence.py FILE [--source NAME]`: every
  field of an input file (e.g. `hydrology.hyd`): declaration and unit, every read, everything that overwrites it,
  copies, the source comments next to each statement, and the example file's value.
- `.swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/ask.py [--source NAME] TOOL key=value [-- TOOL key=value ...]`:
  single Tamandua questions (`uses variable=`, `writers variable=`, `file_io file=`, `describe_type name=`,
  `provenance`; `--list` shows all).
- `./.venv/Scripts/python.exe agent_eval/tools/known_problems.py FILE --docs-root <docs checkout> [--source NAME]`:
  the verified docs findings for one table, and its docs pages.
- `./.venv/Scripts/swatref.exe schema --source NAME user-docs-apply|user-docs-check FILE --docs-root <docs checkout>`:
  tool-made layout fixes for a docs table, and the check.

**Versions.** The tools default to SWAT+ 62.0.1 (`--source release_62_0_1`, commit 97ca231e). For any other
version or branch, pass `--source NAME` with a source named in `swatref.toml`; the tools refuse a source that has
no Tamandua facts yet and print the one-time `swatplus-build` command that builds them (or grep that source's
checkout instead). Check `ask.py --source NAME provenance` before relying on an answer, and always say which
version an answer is for. Tamandua and its facts live in `.swatref/`, which is not in git (this machine only).

This applies to questions about the SWAT+ code and the user docs; release comparisons and other work in this repo
use their own `swatref` commands.
