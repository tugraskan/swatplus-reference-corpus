# Schema reports

The Editor schema report is a tracked input to the other two report families.
The field map connects spreadsheet, Editor, and Fortran names. The range
crosswalk records every applied, drifted, quarantined, review-needed, and
non-applicable range row.

JSON is intended for tools; Markdown is the readable review form. Rebuild the
field and range reports with `swatref schema field-map` and
`swatref schema ranges`.
