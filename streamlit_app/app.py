import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")
st.title("📊 Data Analysis Dashboard")

# -------------------------------
# Load Excel
# -------------------------------
@st.cache_data
def load_excel():
    return pd.read_excel(
        "Data Analytics Intern Assignment - Data Set.xlsx",
        sheet_name=None,
        engine="openpyxl"
    )

workbook = load_excel()

# -------------------------------
# Dropdowns
# -------------------------------
data_view = st.selectbox("Data View", ["Orders", "Sessions", "Calls"])
time_granularity = st.selectbox("Time Granularity", ["Daily", "Weekly", "Monthly"])

# -------------------------------
# Sheet mapping (same as JS)
# -------------------------------
sheet_map = {
    "Orders": "Orders_Raw",
    "Sessions": "Sessions_Raw",
    "Calls": "Calls_Raw"
}

df = workbook[sheet_map[data_view]]

# -------------------------------
# Date & Entity mapping
# -------------------------------
if data_view == "Orders":
    date_col = "Order Date"
    entity_col = "Phone"
    value_col = "Amount"
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce").fillna(0)

elif data_view == "Sessions":
    date_col = "Session Date"
    entity_col = "Device ID"
    value_col = None

else:  # Calls
    date_col = "Call Date"
    entity_col = "Phone"
    value_col = None

# -------------------------------
# Clean & prepare
# -------------------------------
df = df[[date_col, entity_col] + ([value_col] if value_col else [])].dropna()

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df[entity_col] = df[entity_col].astype(str).str.replace(r"\D", "", regex=True)

df = df.dropna(subset=[date_col, entity_col])

# -------------------------------
# Time Granularity
# -------------------------------
if time_granularity == "Daily":
    df["TimeKey"] = df[date_col].dt.date

elif time_granularity == "Weekly":
    df["TimeKey"] = df[date_col].dt.to_period("W").astype(str)

else:  # Monthly
    df["TimeKey"] = df[date_col].dt.to_period("M").astype(str)

# -------------------------------
# Deduplicate (same logic as JS)
# -------------------------------
df = df.drop_duplicates(subset=["TimeKey", entity_col])

# -------------------------------
# Aggregate
# -------------------------------
if value_col:
    result = df.groupby("TimeKey")[value_col].sum().reset_index()
    y_label = "Total Amount"
else:
    result = df.groupby("TimeKey").size().reset_index(name="Count")
    y_label = "Count"

# -------------------------------
# Sort by time
# -------------------------------
result = result.sort_values("TimeKey")

# -------------------------------
# Plot
# -------------------------------
fig = px.bar(
    result,
    x="TimeKey",
    y=result.columns[1],
    title=f"{data_view} ({time_granularity})",
    labels={
        "TimeKey": "Date",
        result.columns[1]: y_label
    }
)

st.plotly_chart(fig, use_container_width=True)








