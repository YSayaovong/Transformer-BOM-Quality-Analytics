"""Read-only checks for the synthetic BOM workbook; never approves a design."""
import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import openpyxl

ERROR_COLUMNS = ('Date', 'Unit_ID', 'Error_Type', 'Stage_Detected', 'Department_Origin', 'Time_to_Resolve_Hours', 'Rework_Required', 'Estimated_Impact_Cost_USD')
REVISION_COLUMNS = ('Date', 'Unit_ID', 'Part_Number', 'Old_Revision', 'New_Revision', 'Change_Reason', 'Rework_Required')

def read_rows(book, name, expected):
    values = list(book[name].values)
    if tuple(values[0]) != expected:
        raise ValueError(f'{name}: unexpected columns')
    return [dict(zip(expected, row)) for row in values[1:] if any(v is not None for v in row)]

def validate(errors, revisions):
    issues = []
    for name, rows, columns in [('BOM_Error_Data', errors, ERROR_COLUMNS), ('Revision_Change_Log', revisions, REVISION_COLUMNS)]:
        seen = set()
        for number, row in enumerate(rows, 2):
            reasons = []
            if any(row[c] is None or (isinstance(row[c], str) and not row[c].strip()) for c in columns):
                reasons.append('missing required value')
            key = tuple(row[c] for c in columns)
            if key in seen:
                reasons.append('exact duplicate record')
            seen.add(key)
            if not isinstance(row['Date'], datetime):
                reasons.append('invalid date')
            if row['Rework_Required'] not in ('Yes', 'No'):
                reasons.append('invalid rework flag')
            if name == 'BOM_Error_Data':
                for field in ('Time_to_Resolve_Hours', 'Estimated_Impact_Cost_USD'):
                    value = row[field]
                    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
                        reasons.append(f'invalid nonnegative measure: {field}')
            if reasons:
                issues.append({'sheet': name, 'excel_row': number, 'severity': 'error', 'reasons': reasons})
            if name == 'Revision_Change_Log' and row['Old_Revision'] == row['New_Revision']:
                issues.append({'sheet': name, 'excel_row': number, 'severity': 'review', 'reasons': ['unchanged revision: confirm whether administrative change was intended']})
    ec = Counter(r['Unit_ID'] for r in errors)
    rc = Counter(r['Unit_ID'] for r in revisions)
    # This is a join-risk diagnostic, not a supported business relationship.
    joined_pairs = sum(count * rc[unit] for unit, count in ec.items())
    has_errors = any(i['severity'] == 'error' for i in issues)
    metrics = None
    if errors and not has_errors:
        metrics = {
            'error_events': len(errors),
            'rework_event_count': sum(r['Rework_Required'] == 'Yes' for r in errors),
            'rework_event_pct': round(100 * sum(r['Rework_Required'] == 'Yes' for r in errors) / len(errors), 4),
            'average_resolution_hours': round(sum(r['Time_to_Resolve_Hours'] for r in errors) / len(errors), 4),
            'estimated_scenario_impact_usd': round(sum(r['Estimated_Impact_Cost_USD'] for r in errors), 2),
        }
    return {'error_rows': len(errors), 'revision_rows': len(revisions), 'error_units': len(ec), 'revision_units': len(rc), 'unit_id_inner_join_pairs': joined_pairs, 'shared_units': len(ec.keys() & rc.keys()), 'issues': issues, 'metrics': metrics}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workbook', type=Path, default=Path(__file__).resolve().parents[1] / 'Transformer_BOM_Quality_Analytics.xlsx')
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'reports' / 'validation.json')
    args = parser.parse_args()
    book = openpyxl.load_workbook(args.workbook, data_only=True)
    result = validate(read_rows(book, 'BOM_Error_Data', ERROR_COLUMNS), read_rows(book, 'Revision_Change_Log', REVISION_COLUMNS))
    result['source_sha256'] = hashlib.sha256(args.workbook.read_bytes()).hexdigest()
    result['scope'] = 'Synthetic portfolio data; event-level checks, not engineering release approval.'
    result['kpi_summary_comparison'] = []
    if result['metrics']:
        m = result['metrics']
        expected = {'Total BOM Errors': m['error_events'], 'Rework Rate (%)': m['rework_event_pct'], 'Average Resolution Time (hrs)': m['average_resolution_hours'], 'Total Estimated Cost Impact ($)': m['estimated_scenario_impact_usd']}
        for label, cached in list(book['KPI_Summary'].values)[1:]:
            calculated = expected[label]
            result['kpi_summary_comparison'].append({'metric': label, 'cached_workbook': cached, 'calculated': calculated, 'matches_to_2dp': isinstance(cached, (int, float)) and round(cached, 2) == round(calculated, 2)})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(f"{result['error_rows']} error events; {result['revision_rows']} revisions; {len(result['issues'])} review/error flags")
    if any(i['severity'] == 'error' for i in result['issues']) or any(not c['matches_to_2dp'] for c in result['kpi_summary_comparison']):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
