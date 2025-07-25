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
tab1, tab2, tab3 = st.tabs(["Statistics", "Visualization", "Data Analysis"])

 # Load data
df = clean_data(load_data())

 # Filters
with st.sidebar:
    st.header("🔍 Filters")
    area_options = ['All'] + sorted(df['Area'].unique())
    area = st.selectbox("Select Area", options=area_options)
    vehicle_options = sorted(df['Vehicle'].unique())
    vehicle = st.multiselect("Vehicle Type", options=vehicle_options, default=vehicle_options)

 # Apply filters
if area == 'All':
    filtered_df = df[df['Vehicle'].isin(vehicle)]
else:
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

        
        st.metric("🚗 Number of Vehicles Types Used", f"{filtered_df['Vehicle'].nunique()}")

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

     # Scatter plot for all stores and drops (X=Longitude, Y=Latitude)
    st.markdown("### 🗺️ Store and Drop Locations")
    store_points = filtered_df[['Store_Longitude', 'Store_Latitude']].drop_duplicates().copy()
    store_points = store_points.rename(columns={'Store_Longitude': 'Longitude', 'Store_Latitude': 'Latitude'})
    store_points['Type'] = 'Store'
    drop_points = filtered_df[['Drop_Longitude', 'Drop_Latitude']].drop_duplicates().copy()
    drop_points = drop_points.rename(columns={'Drop_Longitude': 'Longitude', 'Drop_Latitude': 'Latitude'})
    drop_points['Type'] = 'Drop'
    all_points = pd.concat([store_points, drop_points], ignore_index=True)
    scatter = alt.Chart(all_points).mark_circle(size=80).encode(
        x=alt.X('Longitude', title='Longitude'),
        y=alt.Y('Latitude', title='Latitude'),
        color=alt.Color('Type', scale=alt.Scale(domain=['Store', 'Drop'], range=['blue', 'red'])),
        tooltip=['Type', 'Latitude', 'Longitude']
    ).properties(width=700, height=400)
    st.altair_chart(scatter, use_container_width=True)


 # Data Analysis tab (placeholder)
with tab3:
    st.markdown("### 📊 Data Analysis")

     # Correlation matrix heatmap
    st.markdown("#### Correlation Matrix")
    corr = filtered_df.select_dtypes(include=['number']).corr()
    corr_matrix = corr.stack().reset_index()
    corr_matrix.columns = ['Variable1', 'Variable2', 'Correlation']
    heatmap = alt.Chart(corr_matrix).mark_rect().encode(
        x=alt.X('Variable1', title=None),
        y=alt.Y('Variable2', title=None),
        color=alt.Color('Correlation', scale=alt.Scale(scheme='redblue', domain=[-1,1])),
        tooltip=['Variable1', 'Variable2', 'Correlation']
    ).properties(width=500, height=500)

    text = alt.Chart(corr_matrix).mark_text(size=14, fontWeight='bold').encode(
        x='Variable1',
        y='Variable2',
        text=alt.Text('Correlation', format='.2f'),
        color=alt.condition(
            "abs(datum.Correlation) > 0.5", alt.value('white'), alt.value('black')
        )
    )

    st.altair_chart(heatmap + text, use_container_width=True)

     # Pie chart and Bar chart for Category side by side
    cat_counts = filtered_df['Category'].value_counts().reset_index()
    cat_counts.columns = ['Category', 'Count']
    col_bar, col_pie = st.columns(2)
    with col_bar:
        st.markdown("#### Category Distribution (Bar Chart)")
        bar = alt.Chart(cat_counts).mark_bar().encode(
            x=alt.X('Category', title='Category'),
            y=alt.Y('Count', title='Number of Deliveries'),
            color='Category',
            tooltip=['Category', 'Count']
        ).properties(width=350, height=350)
        st.altair_chart(bar, use_container_width=True)
    with col_pie:
        st.markdown("#### Category Distribution (Pie Chart)")
        cat_counts['Percent'] = cat_counts['Count'] / cat_counts['Count'].sum() * 100
        pie = alt.Chart(cat_counts).mark_arc(innerRadius=60).encode(
            theta=alt.Theta('Count', type='quantitative'),
            color=alt.Color('Category', legend=None),
            tooltip=['Category', 'Count', alt.Tooltip('Percent', format='.1f')]
        ).properties(width=350, height=350)
        pie_text = alt.Chart(cat_counts).mark_text(radiusOffset=20, size=14, fontWeight='bold').encode(
            theta=alt.Theta('Count', type='quantitative'),
            color=alt.Color('Category', legend=None)
        )
        st.altair_chart(pie + pie_text, use_container_width=True)

     # Histograms for Agent_Age, Agent_Rating, Delivery_Time
    st.markdown("#### Histograms and Boxplots")
    col_age, col_rating, col_time = st.columns(3)

    # Agent Age
    with col_age:
        st.markdown("**Agent Age**")
        # Histogram with KDE
        age_hist = alt.Chart(filtered_df).mark_bar(opacity=0.6).encode(
            alt.X('Agent_Age', bin=alt.Bin(maxbins=30), title='Agent Age'),
            alt.Y('count()', title='Count'),
            tooltip=['count()']
        ).properties(width=250, height=180)
        age_kde = alt.Chart(filtered_df).transform_density(
            'Agent_Age',
            as_=['Agent_Age', 'density']
        ).mark_line(color='blue', size=2).encode(
            x='Agent_Age:Q',
            y=alt.Y('density:Q', axis=None)
        )
        st.altair_chart(age_hist + age_kde, use_container_width=True)
        # Boxplot
        age_box = alt.Chart(filtered_df).mark_boxplot(extent='min-max').encode(
            x=alt.X('Agent_Age:Q', title='Agent Age')
        ).properties(width=250, height=100)
        st.altair_chart(age_box, use_container_width=True)

    # Agent Rating
    with col_rating:
        st.markdown("**Agent Rating**")
        rating_hist = alt.Chart(filtered_df).mark_bar(opacity=0.6).encode(
            alt.X('Agent_Rating', bin=alt.Bin(maxbins=30), title='Agent Rating'),
            alt.Y('count()', title='Count'),
            tooltip=['count()']
        ).properties(width=250, height=180)
        rating_kde = alt.Chart(filtered_df).transform_density(
            'Agent_Rating',
            as_=['Agent_Rating', 'density']
        ).mark_line(color='blue', size=2).encode(
            x='Agent_Rating:Q',
            y=alt.Y('density:Q', axis=None)
        )
        st.altair_chart(rating_hist + rating_kde, use_container_width=True)
        rating_box = alt.Chart(filtered_df).mark_boxplot(extent='min-max').encode(
            x=alt.X('Agent_Rating:Q', title='Agent Rating')
        ).properties(width=250, height=100)
        st.altair_chart(rating_box, use_container_width=True)

    # Delivery Time
    with col_time:
        st.markdown("**Delivery Time**")
        time_hist = alt.Chart(filtered_df).mark_bar(opacity=0.6).encode(
            alt.X('Delivery_Time', bin=alt.Bin(maxbins=30), title='Delivery Time'),
            alt.Y('count()', title='Count'),
            tooltip=['count()']
        ).properties(width=250, height=180)
        time_kde = alt.Chart(filtered_df).transform_density(
            'Delivery_Time',
            as_=['Delivery_Time', 'density']
        ).mark_line(color='blue', size=2).encode(
            x='Delivery_Time:Q',
            y=alt.Y('density:Q', axis=None)
        )
        st.altair_chart(time_hist + time_kde, use_container_width=True)
        time_box = alt.Chart(filtered_df).mark_boxplot(extent='min-max').encode(
            x=alt.X('Delivery_Time:Q', title='Delivery Time')
        ).properties(width=250, height=100)
        st.altair_chart(time_box, use_container_width=True)

     # Bar chart: Average Delivery Time by Category
    st.markdown("#### Average Delivery Time by Category (Bar Chart)")
    avg_delivery_by_cat = filtered_df.groupby('Category')['Delivery_Time'].mean().reset_index()
    cat_bar = alt.Chart(avg_delivery_by_cat).mark_bar().encode(
        x=alt.X('Category', title='Category'),
        y=alt.Y('Delivery_Time', title='Average Delivery Time (min)'),
        color=alt.Color('Category', legend=None),
        tooltip=['Category', alt.Tooltip('Delivery_Time', format='.2f')]
    ).properties(width=400, height=300)
    cat_text = alt.Chart(avg_delivery_by_cat).mark_text(dy=-10, size=14, fontWeight='bold').encode(
        x='Category',
        y='Delivery_Time',
        text=alt.Text('Delivery_Time', format='.2f'),
        color=alt.value('white')
    )
    st.altair_chart(cat_bar + cat_text, use_container_width=True)

     # Display the last four bar charts in four columns
    col_traffic, col_weather, col_vehicle, col_area = st.columns(4)

    with col_traffic:
        st.markdown("**Average Delivery Time by Traffic**")
        avg_delivery_by_traffic = filtered_df.groupby('Traffic')['Delivery_Time'].mean().reset_index()
        traffic_bar = alt.Chart(avg_delivery_by_traffic).mark_bar().encode(
            x=alt.X('Traffic', title='Traffic'),
            y=alt.Y('Delivery_Time', title='Average Delivery Time (min)'),
            color=alt.Color('Traffic', legend=None),
            tooltip=['Traffic', alt.Tooltip('Delivery_Time', format='.2f')]
        ).properties(width=200, height=250)
        traffic_text = alt.Chart(avg_delivery_by_traffic).mark_text(dy=-10, size=14, fontWeight='bold').encode(
            x='Traffic',
            y='Delivery_Time',
            text=alt.Text('Delivery_Time', format='.2f'),
            color=alt.value('white')
        )
        st.altair_chart(traffic_bar + traffic_text, use_container_width=True)

    with col_weather:
        st.markdown("**Average Delivery Time by Weather**")
        avg_delivery_by_weather = filtered_df.groupby('Weather')['Delivery_Time'].mean().reset_index()
        weather_bar = alt.Chart(avg_delivery_by_weather).mark_bar().encode(
            x=alt.X('Weather', title='Weather'),
            y=alt.Y('Delivery_Time', title='Average Delivery Time (min)'),
            color=alt.Color('Weather', legend=None),
            tooltip=['Weather', alt.Tooltip('Delivery_Time', format='.2f')]
        ).properties(width=200, height=250)
        weather_text = alt.Chart(avg_delivery_by_weather).mark_text(dy=-10, size=14, fontWeight='bold').encode(
            x='Weather',
            y='Delivery_Time',
            text=alt.Text('Delivery_Time', format='.2f'),
            color=alt.value('white')
        )
        st.altair_chart(weather_bar + weather_text, use_container_width=True)

    with col_vehicle:
        st.markdown("**Average Delivery Time by Vehicle**")
        avg_delivery_by_vehicle = filtered_df.groupby('Vehicle')['Delivery_Time'].mean().reset_index()
        vehicle_bar = alt.Chart(avg_delivery_by_vehicle).mark_bar().encode(
            x=alt.X('Vehicle', title='Vehicle'),
            y=alt.Y('Delivery_Time', title='Average Delivery Time (min)'),
            color=alt.Color('Vehicle', legend=None),
            tooltip=['Vehicle', alt.Tooltip('Delivery_Time', format='.2f')]
        ).properties(width=200, height=250)
        vehicle_text = alt.Chart(avg_delivery_by_vehicle).mark_text(dy=-10, size=14, fontWeight='bold').encode(
            x='Vehicle',
            y='Delivery_Time',
            text=alt.Text('Delivery_Time', format='.2f'),
            color=alt.value('white')
        )
        st.altair_chart(vehicle_bar + vehicle_text, use_container_width=True)

    with col_area:
        st.markdown("**Average Delivery Time by Area**")
        avg_delivery_by_area = filtered_df.groupby('Area')['Delivery_Time'].mean().reset_index()
        area_bar = alt.Chart(avg_delivery_by_area).mark_bar().encode(
            x=alt.X('Area', title='Area'),
            y=alt.Y('Delivery_Time', title='Average Delivery Time (min)'),
            color=alt.Color('Area', legend=None),
            tooltip=['Area', alt.Tooltip('Delivery_Time', format='.2f')]
        ).properties(width=200, height=250)
        area_text = alt.Chart(avg_delivery_by_area).mark_text(dy=-10, size=14, fontWeight='bold').encode(
            x='Area',
            y='Delivery_Time',
            text=alt.Text('Delivery_Time', format='.2f'),
            color=alt.value('white')
        )
        st.altair_chart(area_bar + area_text, use_container_width=True)

     # Bar chart and Pie chart for count of Traffic, Weather, Vehicle, and Area
    st.markdown("#### Count Distribution by Traffic, Weather, Vehicle, and Area")
    col_traffic, col_weather, col_vehicle, col_area = st.columns(4)

     # Traffic
    with col_traffic:
        traffic_counts = filtered_df['Traffic'].value_counts().reset_index()
        traffic_counts.columns = ['Traffic', 'Count']
        st.markdown("**Traffic (Bar Chart)**")
        traffic_bar = alt.Chart(traffic_counts).mark_bar().encode(
            x=alt.X('Traffic', title='Traffic'),
            y=alt.Y('Count', title='Count'),
            color=alt.Color('Traffic', legend=None),
            tooltip=['Traffic', 'Count']
        ).properties(width=200, height=180)
        st.altair_chart(traffic_bar, use_container_width=True)
        st.markdown("**Traffic (Pie Chart)**")
        traffic_counts['Percent'] = traffic_counts['Count'] / traffic_counts['Count'].sum() * 100
        traffic_pie = alt.Chart(traffic_counts).mark_arc(innerRadius=40).encode(
            theta=alt.Theta('Count', type='quantitative'),
            color=alt.Color('Traffic', legend=None),
            tooltip=['Traffic', 'Count', alt.Tooltip('Percent', format='.1f')]
        ).properties(width=200, height=180)
        pie_text = alt.Chart(traffic_counts).mark_text(radiusOffset=20, size=12, fontWeight='bold').encode(
            theta=alt.Theta('Count', type='quantitative'),
            color=alt.Color('Traffic', legend=None)
        )
        st.altair_chart(traffic_pie + pie_text, use_container_width=True)

     # Weather
    with col_weather:
        weather_counts = filtered_df['Weather'].value_counts().reset_index()
        weather_counts.columns = ['Weather', 'Count']
        st.markdown("**Weather (Bar Chart)**")
        weather_bar = alt.Chart(weather_counts).mark_bar().encode(
            x=alt.X('Weather', title='Weather'),
            y=alt.Y('Count', title='Count'),
            color=alt.Color('Weather', legend=None),
            tooltip=['Weather', 'Count']
        ).properties(width=200, height=180)
        st.altair_chart(weather_bar, use_container_width=True)
        st.markdown("**Weather (Pie Chart)**")
        weather_counts['Percent'] = weather_counts['Count'] / weather_counts['Count'].sum() * 100
        weather_pie = alt.Chart(weather_counts).mark_arc(innerRadius=40).encode(
            theta=alt.Theta('Count', type='quantitative'),
            color=alt.Color('Weather', legend=None),
            tooltip=['Weather', 'Count', alt.Tooltip('Percent', format='.1f')]
        ).properties(width=200, height=180)
        pie_text = alt.Chart(weather_counts).mark_text(radiusOffset=20, size=12, fontWeight='bold').encode(
            theta=alt.Theta('Count', type='quantitative'),
            color=alt.Color('Weather', legend=None)
        )
        st.altair_chart(weather_pie + pie_text, use_container_width=True)

     # Vehicle
    with col_vehicle:
        vehicle_counts = filtered_df['Vehicle'].value_counts().reset_index()
        vehicle_counts.columns = ['Vehicle', 'Count']
        st.markdown("**Vehicle (Bar Chart)**")
        vehicle_bar = alt.Chart(vehicle_counts).mark_bar().encode(
            x=alt.X('Vehicle', title='Vehicle'),
            y=alt.Y('Count', title='Count'),
            color=alt.Color('Vehicle', legend=None),
            tooltip=['Vehicle', 'Count']
        ).properties(width=200, height=180)
        st.altair_chart(vehicle_bar, use_container_width=True)
        st.markdown("**Vehicle (Pie Chart)**")
        vehicle_counts['Percent'] = vehicle_counts['Count'] / vehicle_counts['Count'].sum() * 100
        vehicle_pie = alt.Chart(vehicle_counts).mark_arc(innerRadius=40).encode(
            theta=alt.Theta('Count', type='quantitative'),
            color=alt.Color('Vehicle', legend=None),
            tooltip=['Vehicle', 'Count', alt.Tooltip('Percent', format='.1f')]
        ).properties(width=200, height=180)
        pie_text = alt.Chart(vehicle_counts).mark_text(radiusOffset=20, size=12, fontWeight='bold').encode(
            theta=alt.Theta('Count', type='quantitative'),
            color=alt.Color('Vehicle', legend=None)
        )
        st.altair_chart(vehicle_pie + pie_text, use_container_width=True)

     # Area
    with col_area:
        area_counts = filtered_df['Area'].value_counts().reset_index()
        area_counts.columns = ['Area', 'Count']
        st.markdown("**Area (Bar Chart)**")
        area_bar = alt.Chart(area_counts).mark_bar().encode(
            x=alt.X('Area', title='Area'),
            y=alt.Y('Count', title='Count'),
            color=alt.Color('Area', legend=None),
            tooltip=['Area', 'Count']
        ).properties(width=200, height=180)
        st.altair_chart(area_bar, use_container_width=True)
        st.markdown("**Area (Pie Chart)**")
        area_counts['Percent'] = area_counts['Count'] / area_counts['Count'].sum() * 100
        area_pie = alt.Chart(area_counts).mark_arc(innerRadius=40).encode(
            theta=alt.Theta('Count', type='quantitative'),
            color=alt.Color('Area', legend=None),
            tooltip=['Area', 'Count', alt.Tooltip('Percent', format='.1f')]
        ).properties(width=200, height=180)
        pie_text = alt.Chart(area_counts).mark_text(radiusOffset=20, size=12, fontWeight='bold').encode(
            theta=alt.Theta('Count', type='quantitative'),
            color=alt.Color('Area', legend=None)
        )
        st.altair_chart(area_pie + pie_text, use_container_width=True)