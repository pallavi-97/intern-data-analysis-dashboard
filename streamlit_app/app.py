import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.title("Data Analysis Dashboard")

# Load Excel file
df = pd.read_excel("Data Analytics Intern Assignment - Data Set.xlsx", engine='openpyxl')

# Numeric columns
numeric_columns = df.select_dtypes(include='number').columns.tolist()
data_view = st.selectbox("Select Column:", numeric_columns)

# Plotly chart
fig = px.bar(df, x=df.index, y=data_view, labels={'x':'Index', 'y':data_view})
st.plotly_chart(fig, use_container_width=True)

# Altair chart
df_alt = df.reset_index().rename(columns={'index':'Row'})
alt_chart = alt.Chart(df_alt).mark_line(point=True).encode(
    x='Row',
    y=data_view
).interactive()
st.subheader(f"Altair Chart: {data_view}")
st.altair_chart(alt_chart, use_container_width=True)




