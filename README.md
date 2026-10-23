# Transformer BOM Quality Analytics
## Project scope
Independent Excel portfolio case study using synthetic manufacturing data to explore BOM errors, revisions, resolution time and estimated rework impact. It is separate from employer systems and is not a claim of measured workplace savings.

## Included files
- `Engineering_Analytics_Dashboard.xlsx`: primary workbook.
- `assets/`: saved dashboard, KPI, calculations and source-table screenshots.
- No Python/SQL validation pipeline is currently included.

## Data and questions
The documented example has 120 BOM error events and 100 revision log entries for H1 2025. Error records and revision records have different grains; repeating Unit_ID values do not establish a unique join.

The workbook explores error categories, detection stage, originating department, resolution time and estimated impact. Cost values are scenario estimates, not booked financial losses or realized savings.

## Review the workbook
Download and open the XLSX in a compatible spreadsheet application. Inspect the source tables and calculation formulas before interpreting charts. Compare KPI totals with source records, check blanks and duplicates, and verify which rows are included in each denominator. These checks are a review checklist, not a claim of completed automated tests.

![Dashboard](assets/dashboard.png)
![Source BOM example](assets/bom_error.png)
![Revision log](assets/revision_change_log.png)
![Calculations](assets/calculations.png)

## Limitations and next steps
Screenshots are saved outputs and can become stale. Recalculation, cross-application compatibility and all numerical findings require independent verification. Add a data dictionary, explicit validation report and reproducible calculation checks before treating the project as a validated analytical pipeline. Correlations and category differences do not establish root cause.
