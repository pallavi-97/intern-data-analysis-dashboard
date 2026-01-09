import streamlit as st
import pandas as pd

st.title("Data Analytics Intern Assignment")

# Load Excel file
df = pd.read_excel("Data Analytics Intern Assignment - Data Set.xlsx")

# Show the data
st.dataframe(df)

# Show summary statistics
st.subheader("Summary Statistics")
st.write(df.describe())
