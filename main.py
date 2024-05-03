import os
import streamlit as st
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
from utils.b2 import B2
from data_processing import DataProcessor

REMOTE_DATA = 'healthcare-dataset-stroke-data.csv'

class DataFetcher:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Load Backblaze connection
        self.b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
                     key_id=os.environ['B2_keyID'],
                     secret_key=os.environ['B2_applicationKey'])
    
    def fetch_data(self):
        try:
            self.b2.set_bucket(os.environ['B2_BUCKETNAME'])
            df = self.b2.get_df(REMOTE_DATA)
            return df  
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return None

class StrokeRiskAnalyzer:
    def __init__(self, data):
        self.data = data
    
    def run(self):
        if self.data is not None:
            # Introduction section
            st.markdown(
                """
                <div style="background-color:#f0f0f0;padding:10px;border-radius:10px">
                    <h1 style="color:#0074D9;text-align:center;">Welcome to Stroke Risk Analysis Application</h1>
                    <p style="color:#555555;text-align:justify;">This application allows you to analyze the risk of stroke based on various factors. 
                    You can filter the data based on age, gender, hypertension, heart disease, work type, residence type, and smoking status.</p>
                    <p style="color:#555555;text-align:justify;">After selecting the filters, the application will display the filtered data, dynamic visualization, statistical analysis, and data insights.</p>
                </div>
                """, unsafe_allow_html=True
            )

            st.write("")  # Add some space
            
            st.markdown("---")  # Divider line

            try:
                # Sidebar for interactive filters
                selected_age = st.sidebar.slider("Select Age Range", int(self.data['age'].min()), int(self.data['age'].max()), (int(self.data['age'].min()), int(self.data['age'].max())))
                selected_gender = st.sidebar.selectbox("Select Gender", ['Male', 'Female', 'Other'])
                selected_hypertension = st.sidebar.selectbox("Select Hypertension", ['Yes', 'No'])
                selected_heart_disease = st.sidebar.selectbox("Select Heart Disease", ['Yes', 'No'])
                selected_work_type = st.sidebar.selectbox("Select Work Type", self.data['work_type'].unique())
                selected_residence_type = st.sidebar.selectbox("Select Residence Type", self.data['Residence_type'].unique())
                selected_smoking_status = st.sidebar.selectbox("Select Smoking Status", ['Smokes', 'Formerly Smoked', 'Never Smoked', 'Unknown'])

                # Data processing
                processor = DataProcessor(self.data)
                filtered_data = processor.filter_data(selected_age, selected_gender, selected_hypertension, selected_heart_disease, selected_work_type, selected_residence_type, selected_smoking_status)

                # Displaying filtered data or message
                if filtered_data.empty:
                    st.write("Sorry, no data exists for the given criteria")
                else:
                    st.write("Filtered Data:")
                    st.write(filtered_data)

                    # Dynamic visualization based on selected filter
                    if st.button("Show Dynamic Visualization"):
                        # Create dynamic visualization based on filtered data
                        fig, ax = plt.subplots()
                        ax.hist(filtered_data['avg_glucose_level'], bins=15, color='skyblue', edgecolor='black')
                        ax.set_title('Distribution of Average Glucose Levels')
                        ax.set_xlabel('Average Glucose Level')
                        ax.set_ylabel('Frequency')
                        ax.grid(True)
                        st.pyplot(fig)

                    # Statistical analysis
                    st.write("Statistical Analysis:")
                    st.write(processor.compute_statistics(filtered_data))

                    # Data insights
                    st.write("Data Insights:")
                    st.write("1. Average glucose levels tend to be higher among individuals with a history of stroke.")
                    st.write("2. Smoking status and age may also influence stroke risk.")

            except ValueError as ve:
                st.error(f"Invalid input: {ve}")
            except KeyError as ke:
                st.error(f"Missing data: {ke}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# Adding link to GitHub repository
            st.write("For more details, visit the GitHub repository:")
            st.markdown("[Stroke Detection Repository](https://github.com/lasyanavoor286/Stroke-Detection)")


# Instantiate classes to run the application
data_fetcher = DataFetcher()
data = data_fetcher.fetch_data()
analyzer = StrokeRiskAnalyzer(data)
analyzer.run()
