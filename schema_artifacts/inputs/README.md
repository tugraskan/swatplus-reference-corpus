# Schema Artifact Inputs

`modular_database_rev_61_0_nbs.csv` is the tracked CSV export of the
`Rev_61_0_nbs` worksheet used by the range and field-map builders. It is an
input, not a generated report, and is kept because the minimum/maximum ranges
are not derivable from the Fortran source alone.

The builders preserve rows that cannot be matched or safely applied. See the
range and field-map reports under `schema_artifacts/reports/`.
