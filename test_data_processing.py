import unittest
import pandas as pd
from data_processing import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'age': [30, 40, 50],
            'gender': ['Male', 'Female', 'Male'],
            'hypertension': ['Yes', 'No', 'Yes'],
            'heart_disease': ['No', 'Yes', 'Yes'],
            'work_type': ['Private', 'Govt_job', 'Private'],
            'Residence_type': ['Urban', 'Rural', 'Urban'],
            'smoking_status': ['Smokes', 'Never Smoked', 'Formerly Smoked']
        })

    def test_filter_data(self):
        processor = DataProcessor(self.data)
        filtered_data = processor.filter_data((30, 50), 'Male', 'Yes', 'No', 'Private', 'Urban', 'Smokes')
        self.assertEqual(len(filtered_data), 1)

    def test_compute_statistics(self):
        processor = DataProcessor(self.data)
        filtered_data = processor.filter_data((30, 50), 'Male', 'Yes', 'No', 'Private', 'Urban', 'Smokes')
        stats = processor.compute_statistics(filtered_data)
        self.assertIsNotNone(stats)

if __name__ == '__main__':
    unittest.main()
