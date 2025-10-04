import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Cridge Pharmacy KPI Dashboard", layout="wide")

st.title("💊 Cridge Pharmacy KPI Dashboard")
st.write("Enter KPI data below to calculate metrics and generate visualizations.")

# ---------------------------
# Sidebar for User Input
# ---------------------------
st.sidebar.header("📊 Input KPI Data")

# ---- Operations ----
st.sidebar.subheader("Operations KPIs")
fulfillment_time = st.sidebar.number_input("Avg Prescription Fulfillment Time (min)", 5, 60, 15)
error_rate = st.sidebar.number_input("Error Rate (%)", 0.0, 10.0, 1.5, step=0.1)
daily_workload = st.sidebar.slider("Avg Prescriptions per Day", 50, 1000, 250)

# ---- Financial ----
st.sidebar.subheader("Financial KPIs")
revenue_per_rx = st.sidebar.number_input("Revenue per Prescription ($)", 0.0, 500.0, 85.0, step=1.0)
profit_margin = st.sidebar.number_input("Profit Margin (%)", 0.0, 100.0, 20.0, step=0.5)
total_revenue = st.sidebar.number_input("Monthly Total Revenue ($)", 0.0, 1000000.0, 50000.0, step=1000.0)

# ---- Staff ----
st.sidebar.subheader("Staff KPIs")
turnover_rate = st.sidebar.number_input("Turnover Rate (%)", 0.0, 100.0, 15.0, step=0.5)
overtime_hours = st.sidebar.number_input("Avg Overtime Hours / Staff / Month", 0.0, 100.0, 10.0, step=1.0)
training_hours = st.sidebar.number_input("Avg Training Hours / Staff / Month", 0.0, 100.0, 5.0, step=1.0)
staff_satisfaction = st.sidebar.slider("Staff Satisfaction (1-10)", 1, 10, 6)

# ---- Customers ----
st.sidebar.subheader("Customer KPIs")
repeat_patients = st.sidebar.number_input("Repeat Patient Rate (%)", 0.0, 100.0, 65.0, step=1.0)
cust_satisfaction = st.sidebar.slider("Customer Satisfaction (1-10)", 1, 10, 7)
complaints = st.sidebar.number_input("Complaints per 100 Prescriptions", 0.0, 50.0, 5.0, step=1.0)

# ---------------------------
# Layout with Columns
# ---------------------------
tab1, tab2, tab3, tab4 = st.tabs(["⚙️ Operations", "💰 Financial", "👩 Staff", "🙋 Customers"])

# ---- Operations Tab ----
with tab1:
    st.subheader("Operations Metrics")
    ops_df = pd.DataFrame({
        "Metric": ["Fulfillment Time (min)", "Error Rate (%)", "Daily Workload"],
        "Value": [fulfillment_time, error_rate, daily_workload]
    })

    fig_ops = px.bar(ops_df, x="Metric", y="Value", color="Metric",
                     title="Operations KPIs", text="Value")
    st.plotly_chart(fig_ops, use_container_width=True)

# ---- Financial Tab ----
with tab2:
    st.subheader("Financial Metrics")
    fin_df = pd.DataFrame({
        "Metric": ["Revenue per Rx", "Profit Margin (%)", "Total Revenue ($)"],
        "Value": [revenue_per_rx, profit_margin, total_revenue]
    })

    fig_fin = px.bar(fin_df, x="Metric", y="Value", color="Metric",
                     title="Financial KPIs", text="Value")
    st.plotly_chart(fig_fin, use_container_width=True)

# ---- Staff Tab ----
with tab3:
    st.subheader("Staff Metrics")

    staff_df = pd.DataFrame({
        "Metric": ["Turnover Rate (%)", "Overtime Hours", "Training Hours"],
        "Value": [turnover_rate, overtime_hours, training_hours]
    })
    fig_staff = px.bar(staff_df, x="Metric", y="Value", color="Metric",
                       title="Staff KPIs", text="Value")
    st.plotly_chart(fig_staff, use_container_width=True)

    # Gauge for staff satisfaction
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=staff_satisfaction,
        title={'text': "Staff Satisfaction"},
        gauge={'axis': {'range': [0, 10]},
               'bar': {'color': "green"},
               'steps': [
                   {'range': [0, 4], 'color': "red"},
                   {'range': [4, 7], 'color': "yellow"},
                   {'range': [7, 10], 'color': "lightgreen"}
               ]}
    ))
    st.plotly_chart(gauge, use_container_width=True)

# ---- Customers Tab ----
with tab4:
    st.subheader("Customer Metrics")
    cust_df = pd.DataFrame({
        "Metric": ["Repeat Patients (%)", "Customer Satisfaction (1-10)", "Complaints per 100 Rx"],
        "Value": [repeat_patients, cust_satisfaction, complaints]
    })

    fig_cust = px.bar(cust_df, x="Metric", y="Value", color="Metric",
                      title="Customer KPIs", text="Value")
    st.plotly_chart(fig_cust, use_container_width=True)

# ---------------------------
# Summary
# ---------------------------
st.markdown("---")
st.subheader("📌 KPI Summary Report")
st.write(f"""
- **Operations:** Fulfillment time is {fulfillment_time} mins, error rate {error_rate}%, workload {daily_workload} prescriptions/day.  
- **Financial:** Revenue per Rx ${revenue_per_rx}, Profit Margin {profit_margin}%, Total Revenue ${total_revenue}.  
- **Staff:** Turnover {turnover_rate}%, Overtime {overtime_hours} hrs/month, Training {training_hours} hrs, Satisfaction {staff_satisfaction}/10.  
- **Customers:** {repeat_patients}% repeat patients, Satisfaction {cust_satisfaction}/10, {complaints} complaints/100 Rx.  
""")
