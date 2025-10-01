import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

# -----------------------------------------------------
# APP CONFIGURATION
# -----------------------------------------------------
st.set_page_config(
    page_title="Cridge Pharmacy KPI Dashboard",
    page_icon="💊",
    layout="wide"
)

st.title("💊 Cridge Pharmacy KPI Dashboard")
st.markdown("Enter your pharmacy performance data below to generate insights.")

# -----------------------------------------------------
# SIDEBAR - DATA ENTRY
# -----------------------------------------------------
st.sidebar.header("📊 Enter KPI Data")

# Operations data
st.sidebar.subheader("Operations")
presc_time = st.sidebar.number_input("Average prescription fulfillment time (minutes)", min_value=0.0, value=12.0)
error_rate = st.sidebar.number_input("Error rate (%)", min_value=0.0, max_value=100.0, value=2.0)
daily_workload = st.sidebar.slider("Average daily prescriptions filled", min_value=0, max_value=500, value=250)

# Financial data
st.sidebar.subheader("Financials")
revenue_per_rx = st.sidebar.number_input("Revenue per prescription ($)", min_value=0.0, value=75.0)
profit_margin = st.sidebar.slider("Profit margin (%)", min_value=0, max_value=100, value=20)
total_revenue = st.sidebar.number_input("Total revenue ($)", min_value=0.0, value=50000.0)

# Staff data
st.sidebar.subheader("Staff")
turnover = st.sidebar.slider("Annual staff turnover (%)", min_value=0, max_value=100, value=15)
overtime = st.sidebar.number_input("Average monthly overtime hours per staff", min_value=0.0, value=10.0)
training = st.sidebar.number_input("Training hours per staff annually", min_value=0.0, value=20.0)
satisfaction = st.sidebar.slider("Staff satisfaction (%)", min_value=0, max_value=100, value=70)

# Customer data
st.sidebar.subheader("Customers")
repeat_rate = st.sidebar.slider("Repeat patient rate (%)", min_value=0, max_value=100, value=60)
cust_satisfaction = st.sidebar.slider("Customer satisfaction (%)", min_value=0, max_value=100, value=80)
complaints = st.sidebar.number_input("Complaints per 100 prescriptions", min_value=0.0, value=1.5)

# -----------------------------------------------------
# MAIN DASHBOARD - VISUALIZATIONS
# -----------------------------------------------------
st.subheader("📈 Key Performance Indicators Overview")

# Create summary dataframe
kpi_data = {
    "KPI": [
        "Prescription Time (min)", "Error Rate (%)", "Daily Workload",
        "Revenue/Prescription ($)", "Profit Margin (%)", "Total Revenue ($)",
        "Turnover (%)", "Overtime Hours", "Training Hours", "Staff Satisfaction (%)",
        "Repeat Patient Rate (%)", "Customer Satisfaction (%)", "Complaints per 100 Rx"
    ],
    "Value": [
        presc_time, error_rate, daily_workload,
        revenue_per_rx, profit_margin, total_revenue,
        turnover, overtime, training, satisfaction,
        repeat_rate, cust_satisfaction, complaints
    ]
}

df = pd.DataFrame(kpi_data)

# Display in a table
st.dataframe(df, use_container_width=True)

# -----------------------------------------------------
# CHARTS
# -----------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    # Staff Satisfaction Gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=satisfaction,
        title={'text': "Staff Satisfaction"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "green" if satisfaction >= 70 else "red"}}
    ))
    st.plotly_chart(fig, use_container_width=True)

    # Revenue Pie
    fig_pie = px.pie(
        names=["Profit", "Other Costs"],
        values=[profit_margin, 100 - profit_margin],
        title="Profit Margin Breakdown"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Error Rate Bar
    fig_bar = px.bar(
        x=["Error Rate", "Complaints"],
        y=[error_rate, complaints],
        color=["Error Rate", "Complaints"],
        title="Error & Complaints"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Customer Satisfaction vs Repeat Patients
    fig_scatter = px.scatter(
        x=[cust_satisfaction],
        y=[repeat_rate],
        size=[total_revenue/1000],
        title="Customer Satisfaction vs Repeat Rate",
        labels={"x": "Customer Satisfaction (%)", "y": "Repeat Patient Rate (%)"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------------------------------
# INSIGHTS
# -----------------------------------------------------
st.subheader("📝 Key Insights")

if satisfaction < 60:
    st.warning("⚠️ Staff satisfaction is low. Consider reviewing workload and compensation.")
if profit_margin < 15:
    st.warning("⚠️ Profit margins are weak. Investigate operational costs and pricing.")
if error_rate > 5:
    st.warning("⚠️ High error rate detected. More staff training may be needed.")
if cust_satisfaction < 70:
    st.warning("⚠️ Customer satisfaction is dropping. Look into service quality improvements.")

st.success("✅ Dashboard generated successfully with the provided data.")
