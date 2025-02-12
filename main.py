import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils import (
    calculate_renovation_cost,
    calculate_furnishing_cost,
    estimate_property_values,
    calculate_roi_with_split,
    generate_monthly_projection
)

# Page configuration
st.set_page_config(
    page_title="Real Estate Investment Simulator - UAE",
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
st.title("Real Estate Investment Simulator - UAE")
st.markdown("---")

# Sidebar for input parameters
with st.sidebar:
    st.header("Investment Parameters")

    initial_investment = st.number_input(
        "Initial Property Value (AED)",
        min_value=200_000,
        max_value=50_000_000,
        value=1_000_000,
        step=100_000,
        help="Enter the current property value in AED"
    )

    square_feet = st.number_input(
        "Property Size (sq ft)",
        min_value=500,
        max_value=10000,
        value=1500,
        step=100
    )

    quality_level = st.selectbox(
        "Quality Level",
        options=['basic', 'medium', 'luxury'],
        help="Choose the quality level for renovation and furnishing"
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
    st.subheader("Cost Breakdown")
    renovation_cost = calculate_renovation_cost(square_feet, quality_level)
    furnishing_cost = calculate_furnishing_cost(square_feet, quality_level)

    # Display costs
    st.metric(
        label="Renovation Cost",
        value=f"AED {renovation_cost:,.2f}"
    )
    st.metric(
        label="Furnishing Cost",
        value=f"AED {furnishing_cost:,.2f}"
    )

    # Cost per sqft
    total_cost_per_sqft = (renovation_cost + furnishing_cost) / square_feet
    st.info(f"Total Cost per sq ft: AED {total_cost_per_sqft:.2f}")

with col2:
    st.subheader("Estimated Sale Prices")
    property_values = estimate_property_values(
        initial_investment,
        renovation_cost,
        furnishing_cost,
        market_factor
    )

    # Display different price estimates
    for scenario, value in property_values.items():
        st.metric(
            label=f"{scenario.title()} Estimate (+{15 if scenario == 'conservative' else 25 if scenario == 'moderate' else 35}%)",
            value=f"AED {value:,.2f}",
            delta=f"AED {value - initial_investment:,.2f}"
        )

# ROI Analysis
st.markdown("---")
st.header("Investment Analysis")

# Calculate ROI for moderate scenario
roi_data = calculate_roi_with_split(
    initial_investment,
    property_values['moderate'],
    renovation_cost,
    furnishing_cost,
    holding_period
)

col3, col4, col5 = st.columns(3)

with col3:
    st.metric(
        label="Investor's Profit (88%)",
        value=f"AED {roi_data['investor_profit']:,.2f}"
    )

with col4:
    st.metric(
        label="Company's Profit (12%)",
        value=f"AED {roi_data['company_profit']:,.2f}"
    )

with col5:
    st.metric(
        label="Annual ROI",
        value=f"{roi_data['annual_roi']:.2f}%"
    )

# Total Investment Required
st.metric(
    label="Total Investment Required",
    value=f"AED {initial_investment + renovation_cost + furnishing_cost:,.2f}"
)

# Visualizations
st.markdown("---")
st.header("Investment Projections")

# Generate monthly projections (using moderate scenario)
monthly_values = generate_monthly_projection(
    initial_investment,
    property_values['moderate'],
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
    yaxis_title="Property Value (AED)",
    hovermode='x',
    height=500
)

st.plotly_chart(fig1, use_container_width=True)

# Pie chart for cost breakdown
costs_data = pd.DataFrame({
    'Category': ['Initial Investment', 'Renovation Cost', 'Furnishing Cost'],
    'Amount': [initial_investment, renovation_cost, furnishing_cost]
})

fig2 = px.pie(
    costs_data,
    values='Amount',
    names='Category',
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