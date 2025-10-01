# streamlit_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------
# Sample KPI Data
# -------------------------------
days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

# Operations
prescription_fulfillment_time = [28, 30, 32, 29, 27, 31, 33]
error_rate = [0.8, 1.2, 0.9, 0.5, 0.7, 1.0, 1.1]
daily_workload_per_staff = [45, 50, 47, 49, 46, 52, 51]

# Financials
revenue_per_prescription = [15, 16, 15.5, 14, 16.5, 17, 16]
profit_margin = [0.25, 0.22, 0.24, 0.26, 0.23, 0.27, 0.25]
total_revenue = [1500, 1600, 1550, 1400, 1650, 1700, 1600]

# Staff
turnover_rate = 0.12
overtime_hours = 8
training_hours = 5
staff_satisfaction = 4.2

# Customers
repeat_patient_rate = 0.82
customer_satisfaction = 4.1
complaints_per_100 = 0.8

# -------------------------------
# Streamlit Layout
# -------------------------------
st.set_page_config(page_title="Cridge Pharmacy KPI Dashboard", layout="wide")
st.title("Cridge Pharmacy KPI Dashboard")
st.markdown("Monitoring Operations, Financials, Staff, and Customer KPIs")

# -------------------------------
# Operations KPIs
# -------------------------------
st.subheader("Operations KPIs")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(x=days, y=prescription_fulfillment_time, markers=True,
                   labels={'x':'Day','y':'Minutes'}, title="Prescription Fulfillment Time (min)")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(x=days, y=error_rate, labels={'x':'Day','y':'Error Rate (%)'},
                  title="Prescription Error Rate (%)", color=error_rate, color_continuous_scale='Reds')
    st.plotly_chart(fig2, use_container_width=True)

# Daily Workload Heatmap
st.subheader("Daily Workload per Staff")
workload_matrix = np.array([daily_workload_per_staff])
fig3 = px.imshow(workload_matrix, text_auto=True, color_continuous_scale='YlGnBu',
                 labels=dict(x="Day", y="Staff", color="Prescriptions"),
                 x=days, y=["Staff 1"])
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# Financial KPIs
# -------------------------------
st.subheader("Financial KPIs")
fig4 = go.Figure()
fig4.add_trace(go.Bar(x=days, y=total_revenue, name='Total Revenue ($)', marker_color='skyblue'))
fig4.add_trace(go.Scatter(x=days, y=profit_margin, name='Profit Margin', marker_color='orange', mode='lines+markers', yaxis='y2'))

# Create second y-axis
fig4.update_layout(
    title="Revenue & Profit Margin",
    yaxis=dict(title='Revenue ($)'),
    yaxis2=dict(title='Profit Margin (%)', overlaying='y', side='right'),
    legend=dict(x=0.1, y=1.1)
)
st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# Staff KPIs
# -------------------------------
st.subheader("Staff KPIs")
col3, col4 = st.columns(2)

with col3:
    staff_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=staff_satisfaction,
        domain={'x':[0,1],'y':[0,1]},
        title={'text':'Staff Satisfaction (out of 5)'},
        gauge={'axis':{'range':[0,5]},
               'bar':{'color':'green'}}
    ))
    st.plotly_chart(staff_fig, use_container_width=True)

with col4:
    staff_data = pd.DataFrame({
        "KPI":["Turnover Rate","Overtime Hours","Training Hours"],
        "Value":[turnover_rate*100, overtime_hours, training_hours]
    })
    fig5 = px.bar(staff_data, x="KPI", y="Value", color="Value", text="Value",
                  labels={'Value':'Value'}, title="Other Staff KPIs")
    st.plotly_chart(fig5, use_container_width=True)

# -------------------------------
# Customer KPIs
# -------------------------------
st.subheader("Customer KPIs")
customer_data = pd.DataFrame({
    "KPI":["Repeat Patient Rate","Customer Satisfaction","Complaints per 100 Prescriptions"],
    "Value":[repeat_patient_rate*100, customer_satisfaction*20, complaints_per_100*100]  # scaled for visualization
})
fig6 = px.bar(customer_data, x="KPI", y="Value", color="Value", text="Value",
              labels={'Value':'Percentage / Score'}, title="Customer KPIs")
st.plotly_chart(fig6, use_container_width=True)
