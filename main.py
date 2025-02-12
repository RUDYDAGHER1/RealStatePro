import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils import (
    calculate_renovation_cost,
    estimate_property_value,
    calculate_roi,
    generate_monthly_projection
)

# Page configuration
st.set_page_config(
    page_title="Real Estate Investment Simulator",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .stProgress .st-bo {
        background-color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("Real Estate Investment Simulator")
st.markdown("---")

# Sidebar for input parameters
with st.sidebar:
    st.header("Investment Parameters")
    
    initial_investment = st.number_input(
        "Initial Property Value ($)",
        min_value=50000,
        max_value=10000000,
        value=300000,
        step=10000,
        help="Enter the current property value"
    )
    
    square_feet = st.number_input(
        "Property Size (sq ft)",
        min_value=500,
        max_value=10000,
        value=1500,
        step=100
    )
    
    quality_level = st.selectbox(
        "Renovation Quality Level",
        options=['basic', 'medium', 'luxury'],
        help="Choose the quality level of renovations"
    )
    
    market_factor = st.slider(
        "Market Appreciation Factor",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Expected market value increase factor"
    )
    
    holding_period = st.slider(
        "Holding Period (months)",
        min_value=1,
        max_value=60,
        value=12,
        step=1
    )

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Renovation Budget")
    renovation_cost = calculate_renovation_cost(square_feet, quality_level)
    
    # Display renovation costs
    st.metric(
        label="Estimated Renovation Cost",
        value=f"${renovation_cost:,.2f}"
    )
    
    # Cost breakdown
    cost_per_sqft = renovation_cost / square_feet
    st.info(f"Cost per sq ft: ${cost_per_sqft:.2f}")

with col2:
    st.subheader("Property Value Estimation")
    final_value = estimate_property_value(
        initial_investment,
        renovation_cost,
        market_factor
    )
    
    # Display estimated final value
    st.metric(
        label="Estimated Final Value",
        value=f"${final_value:,.2f}",
        delta=f"${final_value - initial_investment:,.2f}"
    )

# ROI Analysis
st.markdown("---")
st.header("ROI Analysis")

profit, annual_roi = calculate_roi(
    initial_investment,
    final_value,
    renovation_cost,
    holding_period
)

col3, col4, col5 = st.columns(3)

with col3:
    st.metric(
        label="Total Profit",
        value=f"${profit:,.2f}"
    )

with col4:
    st.metric(
        label="Annual ROI",
        value=f"{annual_roi:.2f}%"
    )

with col5:
    st.metric(
        label="Total Investment Required",
        value=f"${initial_investment + renovation_cost:,.2f}"
    )

# Visualizations
st.markdown("---")
st.header("Investment Projections")

# Generate monthly projections
monthly_values = generate_monthly_projection(
    initial_investment,
    final_value,
    holding_period
)
months = list(range(1, holding_period + 1))

# Line chart for value progression
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=months,
    y=monthly_values,
    mode='lines+markers',
    name='Property Value',
    line=dict(color='#1f77b4', width=3)
))

fig1.update_layout(
    title="Projected Property Value Over Time",
    xaxis_title="Month",
    yaxis_title="Property Value ($)",
    hovermode='x',
    height=500
)

st.plotly_chart(fig1, use_container_width=True)

# Pie chart for cost breakdown
fig2 = px.pie(
    values=[initial_investment, renovation_cost],
    names=['Initial Investment', 'Renovation Cost'],
    title='Investment Breakdown'
)
fig2.update_traces(
    textposition='inside',
    textinfo='percent+label'
)

st.plotly_chart(fig2, use_container_width=True)

# Disclaimer
st.markdown("---")
st.caption(
    "Disclaimer: This is a simulation tool. Actual results may vary. "
    "Please consult with real estate professionals before making investment decisions."
)
