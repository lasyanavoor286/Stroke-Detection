import pandas as pd

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def filter_data(self, age_range, gender, hypertension, heart_disease, work_type, residence_type, smoking_status):
        filtered_data = self.data[(self.data['age'].between(age_range[0], age_range[1])) &
                                  (self.data['gender'] == gender) &
                                  (self.data['hypertension'] == (hypertension == 'Yes')) &
                                  (self.data['heart_disease'] == (heart_disease == 'Yes')) &
                                  (self.data['work_type'] == work_type) &
                                  (self.data['Residence_type'] == residence_type) &
                                  (self.data['smoking_status'].str.lower() == smoking_status.lower())]
        return filtered_data

    def compute_statistics(self, filtered_data):
        return filtered_data.describe()
