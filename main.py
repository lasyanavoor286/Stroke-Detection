import os
import streamlit as st
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
from utils.b2 import B2
from data_processing import DataProcessor

REMOTE_DATA = 'healthcare-dataset-stroke-data.csv'

class StrokeRiskAnalyzer:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Load Backblaze connection
        self.b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
                     key_id=os.environ['B2_keyID'],
                     secret_key=os.environ['B2_applicationKey'])
        
        # Fetch data
        self.df = self.get_data()

        if self.df is not None:
            # Title of the web app
            st.title("Stroke Risk Analysis")

            # Sidebar for interactive filters
            self.selected_age = st.sidebar.slider("Select Age Range", int(self.df['age'].min()), int(self.df['age'].max()), (int(self.df['age'].min()), int(self.df['age'].max())))
            self.selected_gender = st.sidebar.selectbox("Select Gender", ['Male', 'Female', 'Other'])
            self.selected_hypertension = st.sidebar.selectbox("Select Hypertension", ['Yes', 'No'])
            self.selected_heart_disease = st.sidebar.selectbox("Select Heart Disease", ['Yes', 'No'])
            self.selected_work_type = st.sidebar.selectbox("Select Work Type", self.df['work_type'].unique())
            self.selected_residence_type = st.sidebar.selectbox("Select Residence Type", self.df['Residence_type'].unique())
            self.selected_smoking_status = st.sidebar.selectbox("Select Smoking Status", ['Smokes', 'Formerly Smoked', 'Never Smoked', 'Unknown'])

            # Data processing
            self.processor = DataProcessor(self.df)
            self.filtered_data = self.processor.filter_data(self.selected_age, self.selected_gender, self.selected_hypertension, self.selected_heart_disease, self.selected_work_type, self.selected_residence_type, self.selected_smoking_status)

            # Displaying filtered data
            st.write("Filtered Data:")
            st.write(self.filtered_data)

            # Dynamic visualization based on selected filter
            if st.button("Show Dynamic Visualization"):
                # Create dynamic visualization based on filtered data
                fig, ax = plt.subplots()
                ax.hist(self.filtered_data['avg_glucose_level'], bins=15, color='skyblue', edgecolor='black')
                ax.set_title('Distribution of Average Glucose Levels')
                ax.set_xlabel('Average Glucose Level')
                ax.set_ylabel('Frequency')
                ax.grid(True)
                st.pyplot(fig)

            # Statistical analysis
            st.write("Statistical Analysis:")
            st.write(self.processor.compute_statistics(self.filtered_data))

            # Data insights
            st.write("Data Insights:")
            st.write("1. Average glucose levels tend to be higher among individuals with a history of stroke.")
            st.write("2. Smoking status and age may also influence stroke risk.")

    # Adding link to GitHub repository
            st.write("For more details, visit the GitHub repository:")
            st.markdown("[Stroke Detection Repository](https://github.com/lasyanavoor286/Stroke-Detection)")

    def get_data(self):
        try:
            self.b2.set_bucket(os.environ['B2_BUCKETNAME'])
            df = self.b2.get_df(REMOTE_DATA)
            return df  
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return None

# Instantiate the StrokeRiskAnalyzer class to run the application
StrokeRiskAnalyzer()
