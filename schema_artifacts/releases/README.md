# Schema Release Artifacts

Each release has three tracked artifacts:

- `swatplus-VERSION.json`: deterministic source-derived input schema;
- `swatplus-VERSION-ranges.json`: the same schema with safely matched ranges;
- `swatplus-VERSION.provenance.json`: requested ref and exact source commit.

Rebuild them with `swatref schema build` and `swatref schema ranges`.
