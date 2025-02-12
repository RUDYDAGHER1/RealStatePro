import numpy as np

def calculate_furnishing_cost(square_feet, quality_level):
    """Calculate furnishing costs based on square footage and quality level."""
    base_costs_aed = {
        'basic': 100,    # AED per sq ft
        'medium': 200,
        'luxury': 400
    }
    return square_feet * base_costs_aed[quality_level]

def calculate_renovation_cost(square_feet, quality_level):
    """Calculate renovation costs based on square footage and quality level in AED."""
    base_costs_aed = {
        'basic': 110,    # AED per sq ft
        'medium': 183,    # ~50 USD to AED
        'luxury': 367    # ~100 USD to AED
    }
    return square_feet * base_costs_aed[quality_level]

def estimate_property_values(initial_value, renovation_cost, furnishing_cost, market_factor):
    """Estimate property values after renovation with different markup scenarios."""
    total_cost = renovation_cost + furnishing_cost
    value_increase = total_cost * (1 + market_factor)
    base_value = initial_value + value_increase

    return {
        'conservative': base_value * 1.15,  # +15%
        'moderate': base_value * 1.25,      # +25%
        'optimistic': base_value * 1.35     # +35%
    }

def calculate_roi_with_split(initial_investment, final_value, renovation_cost, furnishing_cost, holding_period):
    """Calculate ROI and profit split between investor and company."""
    total_cost = initial_investment + renovation_cost + furnishing_cost
    profit = final_value - total_cost

    # Split profit: 88% investor, 12% company
    investor_profit = profit * 0.88
    company_profit = profit * 0.12

    # Calculate annual ROI based on investor's portion
    annual_roi = (investor_profit / total_cost) * (12 / holding_period) * 100

    return {
        'total_profit': profit,
        'investor_profit': investor_profit,
        'company_profit': company_profit,
        'annual_roi': annual_roi
    }

def generate_monthly_projection(initial_value, final_value, months):
    """Generate monthly value projections."""
    return np.linspace(initial_value, final_value, months)