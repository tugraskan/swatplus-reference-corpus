# Wire-contract fixtures

These three snapshots freeze the portable rich-parser contract that TAMANDUA and
any other external consumer reads. They are built from the checked-in demo
sources in `tests/fixtures/`, so they are small enough to review in a diff and
do not depend on a fetched SWAT+ checkout.

| File | Envelope | What it holds |
| --- | --- | --- |
| `rich-v1.snapshot.json` | `format: 1` | The pre-v2 payload: `asdict(ProjectIndex)`, no export/model/parser identifiers, and no call filtering |
| `rich-v2.snapshot.json` | `format: 2` | The original allowlisted export, before structured assignments, identities, and block nesting |
| `rich-v3.snapshot.json` | `format: 3` | The current export, produced by `RichStore.save()` |

## What they guarantee

- **v1 stays readable.** `rich-v1.snapshot.json` is the shape the producer
  wrote before `swatplus-reference-rich-v2` existed. The current reader must
  keep loading it, including the unresolved function-shaped candidates that v1
  exported and later contracts filter out. This compatibility path is tested
  rather than asserted.
- **Conversion is lossy, on purpose.** Re-saving a loaded v1 snapshot yields a
  well-formed v3 envelope, but fields v1 never recorded stay `null`: the v1
  producer discarded each assignment's target and expression, and they cannot be
  invented from the payload. Producing a complete v3 snapshot means re-scanning
  the pinned source, not converting an old one. The test asserts both halves of
  that so the limit stays documented rather than discovered.
- **v2 stays readable and v3 cannot drift silently.** The original v2 fixture
  remains unchanged and loadable. Rebuilding from `tests/fixtures/` must
  reproduce `rich-v3.snapshot.json` byte for byte. Any field added, removed,
  renamed, or reordered in the export fails that test, so a wire change is
  always a reviewed diff of this file.
- **Unsupported versions are refused.** A snapshot naming an unknown envelope
  format or an unknown export schema is rejected rather than half-read.

The v1 and original v2 files differ by exactly the call filtering: v1 carries
three call observations including two unresolved function candidates; v2
carries the one proven call. V3 then introduces the structured Phase 1 fields
under a new version instead of silently changing v2 beneath existing readers.

## Regenerating

Only regenerate when the contract change is intended and reviewed. The v3 file
is written by `RichStore.save()`; v1 and v2 are frozen historical fixtures. The
v1 file replicates the historical
producer (`asdict(index)`, `source_root` forced to `"."`, provenance under
`swatplus_reference_rich_snapshot`, `indent=2`, `sort_keys=True`, trailing
newline) with the fixed placeholder commit `cccc...cccc`. `test_contracts.py`
regenerates the v3 payload in-memory on every run, so a stale checked-in file
fails immediately.
