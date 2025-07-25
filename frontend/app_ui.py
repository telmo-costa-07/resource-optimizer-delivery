import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import altair as alt

from app.main import load_data, clean_data

st.set_page_config(page_title="Amazon Delivery Optimizer", layout="wide")

st.title("🚚 Amazon Delivery Resource Optimizer")

 # Navigation tabs
tab1, tab2, tab3 = st.tabs(["Statistics", "Visualization", "Recommendations"])

 # Load data
df = clean_data(load_data())

 # Filters
with st.sidebar:
    st.header("🔍 Filters")
    area = st.selectbox("Select Area", options=df['Area'].unique())
    vehicle = st.multiselect("Vehicle Type", options=df['Vehicle'].unique(), default=df['Vehicle'].unique())

 # Apply filters
filtered_df = df[(df['Area'] == area) & (df['Vehicle'].isin(vehicle))]

 # Visual feedback for applied filters
st.markdown(f"<span style='background-color:#1a73e8; color:white; border-radius:8px; padding:6px 16px; font-size:1em; margin-bottom:10px; display:inline-block;'>Applied filters: <b>Area</b> = {area} | <b>Vehicles</b> = {', '.join(vehicle) if vehicle else 'None'}</span>", unsafe_allow_html=True)


 # Statistics
with tab1:
    # Summary KPIs
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric("⏱️ Average Delivery Time", f"{filtered_df['Delivery_Time'].mean():.2f} min")
    with kpi2:
        st.metric("📦 Number of Deliveries", f"{len(filtered_df)}")
    with kpi3:
        st.metric("🚗 Vehicles Used", f"{filtered_df['Vehicle'].nunique()}")

    # Split table and descriptive statistics into columns
    col_data, col_stats = st.columns([2, 1])
    with col_data:
        st.subheader(f"📊 Delivery Data for Area: {area}")
        st.dataframe(filtered_df)
    with col_stats:
        st.markdown("### 📈 Delivery Time Stats")
        st.write(filtered_df['Delivery_Time'].describe())

 # Visualization
with tab2:
    col_hist, col_vehicle = st.columns(2)
    with col_hist:
        st.markdown("### 🕒 Delivery Time Distribution")
        hist = alt.Chart(filtered_df).mark_bar().encode(
            alt.X('Delivery_Time', bin=alt.Bin(maxbins=30), title='Delivery Time (min)'),
            alt.Y('count()', title='Number of Deliveries'),
            tooltip=['count()']
        ).properties(width=350, height=300)
        st.altair_chart(hist, use_container_width=True)

    with col_vehicle:
        st.markdown("### 🚗 Vehicle Type Distribution")
        vehicle_chart = alt.Chart(filtered_df).mark_bar().encode(
            alt.X('Vehicle', title='Vehicle Type'),
            alt.Y('count()', title='Number of Deliveries'),
            color='Vehicle',
            tooltip=['Vehicle', 'count()']
        ).properties(width=350, height=300)
        st.altair_chart(vehicle_chart, use_container_width=True)

 # Recommendations (placeholder)
with tab3:
    st.markdown("### 💡 Recommendations")
    st.info("Recommendation feature coming soon!")
