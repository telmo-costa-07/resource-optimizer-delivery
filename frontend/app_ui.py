import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import load_data, clean_data

st.set_page_config(page_title="Amazon Delivery Optimizer", layout="wide")

st.title("🚚 Amazon Delivery Resource Optimizer")

# Load data
df = clean_data(load_data())

# Filtros
with st.sidebar:
    st.header("🔍 Filters")
    area = st.selectbox("Select Area", options=df['Area'].unique())
    vehicle = st.multiselect("Vehicle Type", options=df['Vehicle'].unique(), default=df['Vehicle'].unique())

# Apply filters
filtered_df = df[(df['Area'] == area) & (df['Vehicle'].isin(vehicle))]

# Display data
st.subheader(f"📊 Delivery Data for Area: {area}")
st.dataframe(filtered_df)

# Statistics
st.markdown("### 📈 Delivery Time Stats")
st.write(filtered_df['Delivery_Time'].describe())
