import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")
st.title("📊 Data Analysis Dashboard")

# --- Load Excel file ---
try:
    df = pd.read_excel("Data Analytics Intern Assignment - Data Set.xlsx", engine='openpyxl')
except FileNotFoundError:
    st.error("Excel file not found! Make sure 'Data Analytics Intern Assignment - Data Set.xlsx' is in your repo.")
    st.stop()

# Show the first few rows
st.subheader("Dataset Preview")
st.dataframe(df.head())

# --- Numeric columns for visualization ---
numeric_columns = df.select_dtypes(include='number').columns.tolist()
if not numeric_columns:
    st.error("No numeric columns found in the dataset to plot.")
    st.stop()

# --- Dropdown to select column to visualize ---
data_view = st.selectbox("Select Column to Visualize:", numeric_columns)

# --- Optional: Date-based filtering ---
date_column = None
for col in df.columns:
    if 'date' in col.lower():  # simple check for date column
        date_column = col
        break

time_granularity = st.selectbox("Time Granularity:", ["Daily", "Weekly", "Monthly"])

# If a date column exists, we can resample
if date_column:
    df[date_column] = pd.to_datetime(df[date_column])
    if time_granularity == "Daily":
        df_plot = df.set_index(date_column).resample("D").sum()
    elif time_granularity == "Weekly":
        df_plot = df.set_index(date_column).resample("W").sum()
    else:  # Monthly
        df_plot = df.set_index(date_column).resample("M").sum()
else:
    df_plot = df.copy()

# --- Display charts ---

# Plotly Bar Chart
st.subheader(f"Plotly Bar Chart: {data_view}")
fig = px.bar(df_plot, x=df_plot.index, y=data_view, labels={'x':'Date/Index', 'y':data_view})
st.plotly_chart(fig, use_container_width=True)

# Altair Chart
st.subheader(f"Altair Line Chart: {data_view}")
alt_chart = alt.Chart(df_plot.reset_index()).mark_line(point=True).encode(
    x='index',
    y=data_view
).interactive()

st.altair_chart(alt_chart, use_container_width=True)

# Optional: show summary statistics
st.subheader("Summary Statistics")
st.dataframe(df[numeric_columns].describe())


