# Source grain and review rules
This independent project uses synthetic data, not an export from SAP, TDMS or an employer.

| Sheet | Grain | Main fields | Safe interpretation |
|---|---|---|---|
| BOM_Error_Data | One logged error event; no explicit event ID | Date, Unit_ID, error type, detection stage, origin department | Count events, not unique defective units |
| Revision_Change_Log | One logged revision activity; no explicit change ID | Date, Unit_ID, Part_Number, old/new revision, reason | An unchanged revision is a review flag, not proof of an invalid release |
| KPI_Summary | One saved metric per row | Metric, Value | Compare cached values with recomputed source totals |

Required fields must be populated. Dates must parse; resolution time and scenario cost must be nonnegative; rework must be Yes/No. Exact duplicate records are flagged. Repeated Unit_ID values are permitted because units can have multiple events.

There are 67 distinct error-table units and 62 revision-table units, with zero overlapping IDs in this snapshot. Do not join the two tables for an error/revision relationship. A future linked dataset needs a defined event/change key and verified relationship.

Rework event percentage = Yes error events / all error events × 100. Average resolution time is an event-weighted mean. Estimated impact sums scenario cost values; it is not avoided cost or booked loss.

The validator compares cached workbook KPIs; openpyxl does not recalculate Excel formulas, validate every chart, or approve engineering designs.
