import numpy as np

def calculate_renovation_cost(square_feet, quality_level):
    """Calculate renovation costs based on square footage and quality level."""
    base_costs = {
        'basic': 30,
        'medium': 50,
        'luxury': 100
    }
    return square_feet * base_costs[quality_level]

def estimate_property_value(initial_value, renovation_cost, market_factor):
    """Estimate property value after renovation."""
    value_increase = renovation_cost * (1 + market_factor)
    return initial_value + value_increase

def calculate_roi(initial_investment, final_value, renovation_cost, holding_period):
    """Calculate ROI for the investment."""
    total_cost = initial_investment + renovation_cost
    profit = final_value - total_cost
    annual_roi = (profit / total_cost) * (12 / holding_period) * 100
    return profit, annual_roi

def generate_monthly_projection(initial_value, final_value, months):
    """Generate monthly value projections."""
    return np.linspace(initial_value, final_value, months)
