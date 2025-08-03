# ==============================================================================
# FINAL APPLICATION CODE (app.py)
# ==============================================================================
import streamlit as st

# --- Page Configuration (Sets the title and icon for the browser tab) ---
st.set_page_config(
    page_title="Freight EV Cost Simulator",
    page_icon="⚡",
    layout="centered"
)

# --- Calculation Logic (A simple function to do the math) ---
def calculate_costs(miles):
    """
    Performs a simple cost comparison calculation.
    These values are industry averages we can refine later.
    """
    # Cost per mile assumptions
    diesel_cost_per_mile = 0.58  # ($3.78/gal / 6.5 MPG)
    electric_cost_per_mile = 0.19 # (1.5 kWh/mile * $0.12/kWh)

    # Calculate total costs
    total_diesel_cost = miles * diesel_cost_per_mile
    total_electric_cost = miles * electric_cost_per_mile
    savings = total_diesel_cost - total_electric_cost

    return total_diesel_cost, total_electric_cost, savings

# --- Main App Interface (The visual part of the app) ---
st.title("Diesel vs. Electric: Calculate Your Savings")

# Use a text input for the user to enter the miles
# We will use a simple number input for now to ensure it works reliably
miles_input = st.number_input(
    "Enter the total miles for the haul:",
    min_value=0,
    step=50,
    help="Type the number of miles for your trip."
)

# When the user clicks the button, we run the calculation
if st.button("Calculate My Savings"):
    if miles_input > 0:
        # Run the calculation function with the user's input
        diesel_cost, electric_cost, savings = calculate_costs(miles_input)

        # Display the results in a clear format
        st.subheader("Estimated Trip Costs")
        col1, col2 = st.columns(2)
        col1.metric(label="Diesel Truck", value=f"${diesel_cost:,.2f}")
        col2.metric(label="Electric Truck", value=f"${electric_cost:,.2f}")

        st.subheader("Your Estimated Savings")
        st.success(f"You could save approximately ${savings:,.2f} on this trip!")
    else:
        # Show an error if the user didn't enter any miles
        st.error("Please enter a number of miles greater than zero.")

# --- Footer with our Ethical Commitment ---
st.caption("Your data is anonymized and used only to improve our calculations. We respect your privacy.")
