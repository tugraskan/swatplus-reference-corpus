# Phase 0 parser performance reference

This is an observational baseline, not a byte-reproducibility gate. CI verifies the deterministic facts and artifacts instead.

- Platform: `Linux x86_64`
- Python: `3.11.15`
- Workload: one complete rich scan, fparser2 diagnostic pass, and documentation projection
- Elapsed time: **96.86 seconds**
- Peak process resident memory at parse completion: **487.17 MiB**
- Measurement: OS peak working set/RSS, including interpreter overhead; no allocation tracing is enabled
- Source: pinned SWAT+ commit recorded in the JSON baseline
