import unittest
from datetime import datetime
from validate_bom import validate

class ValidationTests(unittest.TestCase):
    def error(self):
        return dict(Date=datetime(2025, 1, 1), Unit_ID='U1', Error_Type='Missing Part', Stage_Detected='Review', Department_Origin='Engineering', Time_to_Resolve_Hours=2, Rework_Required='Yes', Estimated_Impact_Cost_USD=10)

    def revision(self):
        return dict(Date=datetime(2025, 1, 1), Unit_ID='U1', Part_Number='P1', Old_Revision='A', New_Revision='B', Change_Reason='Update', Rework_Required='No')

    def test_duplicate_event_blocks_kpi(self):
        r = validate([self.error(), self.error()], [])
        self.assertIsNone(r['metrics'])
        self.assertIn('exact duplicate record', r['issues'][0]['reasons'])

    def test_negative_measure_blocks_kpi(self):
        row = self.error(); row['Time_to_Resolve_Hours'] = -1
        self.assertIsNone(validate([row], [])['metrics'])

    def test_unchanged_revision_needs_review_not_rejection(self):
        row = self.revision(); row['New_Revision'] = 'A'
        r = validate([self.error()], [row])
        self.assertEqual(r['issues'][0]['severity'], 'review')
        self.assertEqual(r['metrics']['error_events'], 1)

    def test_repeated_unit_is_not_duplicate_event(self):
        row = self.error(); row['Error_Type'] = 'Wrong Revision'
        r = validate([self.error(), row], [self.revision()])
        self.assertEqual(r['issues'], [])
        self.assertEqual(r['unit_id_inner_join_pairs'], 2)
        self.assertEqual(r['error_units'], 1)

if __name__ == '__main__':
    unittest.main()
