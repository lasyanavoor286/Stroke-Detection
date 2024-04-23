import os

import pandas as pd

import matplotlib.pyplot as plt


import streamlit as st
from dotenv import load_dotenv

from utils.b2 import B2
from utils.modeling import *

REMOTE_DATA = 'healthcare-dataset-stroke-data.csv'


load_dotenv()

# load Backblaze connection
b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        key_id=os.environ['B2_keyID'],
        secret_key=os.environ['B2_applicationkey'])

def get_data():
    b2.set_bucket(os.environ['B2_BUCKETNAME'])
    df = b2.get_df(REMOTE_DATA)
    return df  


df = get_data()

st.title("What is the distribution of average glucose levels among individuals who have had a stroke?")

# Filtering data for individuals who have had a stroke
avg_glucose_levels_stroke = df[df['stroke'] == 1]['avg_glucose_level']

# Creating a histogram
fig = plt.figure(figsize=(10, 6))
plt.hist(avg_glucose_levels_stroke, bins=15, color='skyblue', edgecolor='black')
plt.title('Distribution of Average Glucose Levels among Individuals with Stroke')
plt.xlabel('Average Glucose Level')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

st.pyplot(fig)

st.dataframe(df.head(30))

