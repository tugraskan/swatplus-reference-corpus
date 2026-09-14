# Phase 1 budgets

The plan asks Phase 1 to decide how the portable snapshot is stored and to set
size, time, and memory budgets from the Phase 0 measurements, before the model
grows. These are those decisions and the evidence behind them.

## Storage: keep plain JSON

The snapshot is tracked as plain, pretty-printed JSON. It is neither compressed
nor moved to Git LFS, and nothing is trimmed out of it for size alone.

The headline size is misleading. Measured on this branch:

| Measure | Value |
| --- | --- |
| Snapshot, raw with LF endings | 50.0 MiB (52,437,338 bytes, Phase 2) |
| Snapshot with Phase 4 call paths | 56.0 MiB (58,690,186 bytes, parser v5) |
| The same bytes under `gzip -6` | 2.1 MiB (4.8%) |
| Whole-repository pack, holding **seven** snapshot versions (~335 MB of raw content) | **6.89 MiB** |

Measured directly rather than estimated. Immediately before a `git gc` the repo
held 5.88 MiB of pack plus 21.37 MiB of loose objects; the `gc` collapsed those
loose objects into 1.01 MiB of additional pack, covering two further snapshot
versions and the rest of the Phase 1 changes. Git spends roughly **0.25 MiB per
snapshot version**, because consecutive versions of this file are nearly
identical and delta-compress against each other almost completely.

That number is what decides the question, and it decides it against every
alternative:

- **Compressing the tracked file makes storage worse, not better.** A gzipped
  blob does not delta against its predecessor -- a small change to the input
  scrambles the whole compressed output -- so each version would cost its full
  standalone ~2.1 MiB instead of ~0.25 MiB. That is roughly 8x more, in exchange
  for a snapshot diff nobody can read and a decompression step for every
  consumer.
- **Git LFS** would add setup to CI and to every consumer clone, plus quota, to
  relocate a history that costs 6.89 MiB in total.
- **Trimming the export** is the largest lever on the file itself (`metadata` is
  20.5% of it, mostly outside-state references), but it is a breaking change for
  TAMANDUA and should be driven by what that consumer actually reads, not by
  size.

Revisit this if the pack cost per re-baseline stops being small, or if a
consumer asks for a different shape. Note that pack cost is only observable
after a `git gc`; loose objects are compressed individually and will always look
several times worse than the settled figure.

## Size budget: 64 MiB, enforced

`baseline_failures()` fails the Phase 0 gate if the exported snapshot exceeds
**64 MiB** raw. At 50.0 MiB -- after the Phase 1 assignment and control-nesting
fields and the Phase 2 statement recovery -- that leaves roughly 22% headroom,
which is the room Phase 3 has to add structured records before the storage
decision above has to be reopened. Phase 1 spent about half the headroom it
started with, so each phase should measure before it adds. Phase 2 cost
52,239,056 -> 52,437,338 bytes, about 194 KiB, so headroom moved only from
22.1% to 21.9%. It is a tripwire against a model change that blows the
shape up, not a storage workaround.

Phase 4's exact-identity call paths add 6,252,848 bytes (about 6.0 MiB),
leaving 8,418,678 bytes (about 8.0 MiB, or 12.5%) below the enforced gate.
That is enough for this representation, but it is now close enough that every
later exported relationship must be measured before the wire contract grows.

### Accepted risk: call-path growth is not bounded by the model

`derive_project_call_paths()` enumerates every maximal simple path from every
procedure. That is worst-case exponential in the call graph, and nothing in the
code caps path count, path length, or recursion depth -- the 64 MiB gate is the
only backstop, and it fails the build rather than degrading.

The pinned tree's distribution shows the shape plainly:

| Measure | Value |
|---|---|
| Procedures | 734 |
| Procedures contributing no path at all | 536 (median count is 0) |
| Total paths | 16,671 |
| Total identity strings across those paths | 107,289 |
| Longest path | 12 |
| `calsoft_control` alone | 5,395 paths (32.4%) |
| `calsoft_control` + `calsoft_hyd_bfr` | 8,391 paths (50.3%) |
| Top five procedures | 10,191 paths (61.1%) |

Two procedures out of 734 produce half the output, and nearly three quarters of
all procedures produce none. The cost is not spread across the model; it is one
densely connected `calsoft_*` cluster, and it grows with the branching factor
inside that cluster rather than with the size of SWAT+ overall.

**Decision: accept this for now, unbounded, and do not cap it.** The
representation is exact and the current cost fits. The risk being accepted is
that the failure is abrupt -- new edges inside the calibration cluster consume
headroom far faster than edges anywhere else, and crossing 64 MiB stops the
build instead of shrinking the output.

Revisit when any of these becomes true, rather than on a schedule:

- The snapshot passes roughly 60 MiB, leaving under 4 MiB of margin.
- The top-five share of paths rises above today's 61%, meaning the hub cluster
  is getting denser rather than the model getting broader.
- The longest path exceeds about 40, which is where the unguarded recursion in
  `visit()` starts to matter as well as the size.

The alternatives, if that happens, are to cap path length or count and label the
result as truncated, or to export only the resolved direct edges -- already on
`CallRef.resolved_target` -- and let consumers walk them. Both are contract
changes, which is why neither is being taken pre-emptively.

The gate deliberately watches the raw file rather than the pack cost. Pack cost
is the better measure of what the repository actually pays, but it is only
observable after a `git gc`, it depends on how similar the new version happens
to be to the last one, and it cannot be computed while building the snapshot
that would go into it. Raw size is available at the moment the check runs and
moves in the same direction, so it is the practical proxy.

The composition below is where that headroom would go:

| Section | Share of file |
| --- | --- |
| `metadata` (outside-state references) | 20.5% |
| `control_steps` | 9.3% |
| `assignments` | 7.9% |
| `io` | 5.8% |
| `io_files` | 6.1% |
| `types` | 3.5% |
| `variables` | 2.8% |

## Time and memory: observational, not gates

Parse time and peak memory vary by machine and by concurrent load, so they are
recorded rather than compared. `PERFORMANCE.md` is regenerated in full by
`swatref docs baseline --write`, so it only ever holds the most recent run and
cannot accumulate this history; this table is the record. Observed full parses
of the pinned source, across machines and runs:

| Run | Python | Elapsed | Peak process memory |
| --- | --- | --- | --- |
| Phase 0, first | 3.12.14 | 304.60 s | 449.46 MiB |
| Phase 0, second | 3.12.14 | 448.35 s | 449.93 MiB |
| Phase 1 verification | 3.12.14 | 121.01 s | 493.14 MiB |
| Phase 2, initial `v3` baseline | 3.11.9 | 306.90 s | 499.01 MiB |
| Phase 2 review, clean clone | 3.13.12 | 41.98 s | 461.44 MiB |
| Phase 2 review, after the `inline_doc_from_raw` fix | 3.13.12 | 107.69 s | 463.10 MiB |
| Phase 2 follow-up, tracked `v4` baseline | 3.13.12 | 49.24 s | 463.00 MiB |
| Phase 4 slice 2, tracked `v5` baseline | 3.13.12 | 45.56 s | 472.36 MiB |

The last two rows are full uncached parses of the same pinned commit on one
Windows AMD64 machine, taken minutes apart under different load. The 2.6x
spread between them is the clearest evidence that elapsed time is an
observation and not a gate.

Peak memory is stable near 450-500 MiB across every run; elapsed time is not.
Treat a full parse above **900 seconds** or a peak above **1 GiB** as a signal
that something regressed rather than that the machine was busy, and investigate
before re-baselining.

A no-change run should not reparse at all: with a current `facts.json` and
`rich.json` whose recorded fparser diagnostics agree, `get_store()` returns the
cached store without touching the scanner. That behaviour is covered by the
cache tests rather than by a timing budget.
