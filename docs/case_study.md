# BOM data-quality review
## Decision
Which records need review before using the workbook for manufacturing reporting?

## Approach
Inspect event grain, required values, duplicates, valid measures, revision consistency, cross-table keys and summary reconciliation. Run `python scripts/validate_bom.py` and the four tests before using the saved report.

## Results from the included synthetic workbook
- 120 error events; 100 revision entries.
- 25 unchanged-revision entries flagged for review; zero exact duplicate or missing-required-field errors under these checks.
- Error and revision Unit_ID sets do not overlap. A direct joined analysis is unsupported.
- 62/120 error events indicate rework (51.6667%); average resolution is 3.0915 hours.
- All four saved summary KPIs match recomputation to two decimal places.
- $164,235.38 is summed scenario impact, not savings.

## Recommended action
Review unchanged revisions with the data owner; confirm whether administrative changes are intentional. Establish a shared key before analyzing error-to-revision relationships. Keep event counts distinct from affected-unit counts.

## Career relevance
This portfolio exercise applies manufacturing/BOM context to analyst work: data checks, metric definitions, exception reporting and clear documentation. The scripts and tests were added with AI assistance and should be understood and rerun before being discussed in an interview. They do not establish Python automation performed in employment.
