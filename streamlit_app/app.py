import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

st.title("Orders Over Time Dashboard")

# --- Load Excel file ---
df = pd.read_excel("Data Analytics Intern Assignment - Data Set.xlsx", engine='openpyxl')

# --- Detect numeric columns ---
numeric_columns = df.select_dtypes(include='number').columns.tolist()
data_column = st.selectbox("Select numeric column:", numeric_columns)

# --- Detect date column ---
date_column = None
for col in df.columns:
    if 'date' in col.lower():  # simple detection
        date_column = col
        break

if date_column is None:
    st.error("No date column found in dataset!")
    st.stop()

# Convert date column to datetime
df[date_column] = pd.to_datetime(df[date_column])

# --- Optional: choose aggregation ---
granularity = st.selectbox("Select time granularity:", ["Daily", "Weekly", "Monthly"])

# Aggregate data by date
if granularity == "Daily":
    df_grouped = df.groupby(df[date_column].dt.date)[data_column].sum().reset_index()
elif granularity == "Weekly":
    df_grouped = df.groupby(df[date_column].dt.to_period("W")).sum()[[data_column]].reset_index()
    df_grouped[date_column] = df_grouped[date_column].dt.start_time
else:  # Monthly
    df_grouped = df.groupby(df[date_column].dt.to_period("M")).sum()[[data_column]].reset_index()
    df_grouped[date_column] = df_grouped[date_column].dt.start_time

# --- Plotly chart ---
st.subheader(f"Plotly: {data_column} over time ({granularity})")
fig = px.line(df_grouped, x=date_column, y=data_column, markers=True)
st.plotly_chart(fig, use_container_width=True)

# --- Altair chart ---
st.subheader(f"Altair: {data_column} over time ({granularity})")
alt_chart = alt.Chart(df_grouped).mark_line(point=True).encode(
    x=date_column,
    y=data_column
).interactive()
st.altair_chart(alt_chart, use_container_width=True)







