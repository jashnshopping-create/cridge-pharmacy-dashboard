import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Cridge Pharmacy Weekly KPI Dashboard",
    layout="wide"
)

st.title("💊 Cridge Pharmacy Weekly KPI Dashboard")
st.write("Enter daily data for each KPI and view summarized weekly performance.")

# -------------------------------
# User Input
# -------------------------------

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Define KPIs to track
kpis = {
    "Prescription Fulfillment Time (mins)": "numeric",
    "Error Rate (%)": "numeric",
    "Daily Workload (prescriptions)": "numeric",
    "Revenue ($)": "numeric",
    "Profit Margin (%)": "numeric",
    "Overtime Hours": "numeric",
    "Training Hours": "numeric",
    "Staff Satisfaction (1-10)": "numeric",
    "Repeat Patient Rate (%)": "numeric",
    "Customer Satisfaction (1-10)": "numeric",
    "Complaints (count)": "numeric"
}

# Create empty DataFrame to hold inputs
data = pd.DataFrame(index=days, columns=kpis.keys())

st.subheader("📊 Input Daily KPI Data")

# Input widgets for each day & KPI
for day in days:
    st.markdown(f"### {day}")
    cols = st.columns(3)  # split into 3 columns for cleaner layout
    i = 0
    for kpi in kpis.keys():
        with cols[i % 3]:
            value = st.number_input(f"{kpi} - {day}", min_value=0.0, step=1.0, key=f"{day}_{kpi}")
            data.loc[day, kpi] = value
        i += 1

# Convert numeric inputs to float
data = data.astype(float)

# -------------------------------
# Weekly Summary
# -------------------------------
st.subheader("📈 Weekly KPI Summary")

weekly_summary = data.mean().to_frame("Weekly Average")
weekly_summary["Weekly Total"] = data.sum()

st.dataframe(weekly_summary.style.format("{:.2f}"))

# -------------------------------
# Visualization
# -------------------------------

st.subheader("📊 KPI Visualizations")

# Line chart for trends across days
selected_kpi = st.selectbox("Select KPI to visualize trends", data.columns)
fig_line = px.line(data, x=data.index, y=selected_kpi, title=f"{selected_kpi} - Daily Trend")
st.plotly_chart(fig_line, use_container_width=True)

# Bar chart for weekly totals
fig_bar = px.bar(
    weekly_summary,
    x=weekly_summary.index,
    y="Weekly Total",
    title="Weekly Totals for Each KPI",
    text_auto=True
)
st.plotly_chart(fig_bar, use_container_width=True)

# Radar chart for averages (quick comparison)
fig_radar = px.line_polar(
    r=weekly_summary["Weekly Average"],
    theta=weekly_summary.index,
    line_close=True,
    title="Weekly KPI Profile (Average)"
)
fig_radar.update_traces(fill="toself")
st.plotly_chart(fig_radar, use_container_width=True)

# -------------------------------
# Insights
# -------------------------------
st.subheader("📝 Insights")

if weekly_summary.loc["Error Rate (%)", "Weekly Average"] > 5:
    st.warning("⚠️ Error rate is above 5%. Consider reviewing staff training and workload balance.")

if weekly_summary.loc["Staff Satisfaction (1-10)", "Weekly Average"] < 6:
    st.error("❌ Staff satisfaction is low. Risk of turnover is high!")

if weekly_summary.loc["Customer Satisfaction (1-10)", "Weekly Average"] < 7:
    st.warning("⚠️ Customer satisfaction is below target. Investigate complaint causes.")

if weekly_summary.loc["Overtime Hours", "Weekly Total"] > 20:
    st.info("ℹ️ High overtime detected. Staffing levels may need adjustment.")
