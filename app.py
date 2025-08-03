import streamlit as st
import spacy
import subprocess
import re

# --- Core Functions ---

@st.cache_resource
def download_spacy_model():
    """Checks if the spacy model is installed and downloads it if not."""
    try:
        spacy.load("en_core_web_sm")
    except OSError:
        # Don't show messages on the deployed app, just download
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])

def parse_miles_from_query(query, nlp_model):
    """
    Parses a text query to robustly find the number of miles.
    """
    # Use regular expressions to find numbers with commas
    query = query.replace(",", "")
    doc = nlp_model(query.lower())
    
    # Primary Method: Find a number token right before "mile" or "miles"
    for i, token in enumerate(doc):
        if token.text in ["mile", "miles"] and i > 0:
            prev_token = doc[i-1]
            if prev_token.like_num:
                try:
                    return int(float(prev_token.text))
                except ValueError:
                    continue
    
    # Fallback Method: Find the first number-like token in the text
    for token in doc:
        if token.like_num:
            try:
                return int(float(token.text))
            except ValueError:
                continue
            
    return 0 # Return 0 if no number is found

def calculate_costs(miles):
    """Performs the cost comparison calculation."""
    diesel_cost_per_mile = 0.58
    electric_cost_per_mile = 0.19
    total_diesel_cost = miles * diesel_cost_per_mile
    total_electric_cost = miles * electric_cost_per_mile
    savings = total_diesel_cost - total_electric_cost
    return total_diesel_cost, total_electric_cost, savings

# --- Main Application ---

# Run the download check first - this will only run on the Streamlit Cloud server
download_spacy_model()

# Load the NLP model once
@st.cache_resource
def load_nlp_model():
    return spacy.load("en_core_web_sm")

nlp = load_nlp_model()

# --- Page Configuration and Interface ---
st.set_page_config(page_title="Freight EV Cost Simulator", page_icon="⚡")
st.title("Diesel vs. Electric: Calculate Your Savings")

# Initialize session state for memory
if "results" not in st.session_state:
    st.session_state.results = None

# Get user input
haul_query = st.text_input(
    "Tell me about your haul...",
    placeholder="e.g., How much for a 1,200 mile trip?"
)

if st.button("Calculate My Savings"):
    if haul_query:
        miles_input = parse_miles_from_query(haul_query, nlp)
        if miles_input > 0:
            d_cost, e_cost, sav = calculate_costs(miles_input)
            st.session_state.results = {"diesel": d_cost, "electric": e_cost, "savings": sav}
        else:
            st.session_state.results = {"error": True}
    else:
        st.session_state.results = {"error": True}

# Display results from session state
if st.session_state.results:
    if "error" in st.session_state.results:
        st.error("Please describe your haul and include the number of miles.")
    else:
        results = st.session_state.results
        st.subheader("Estimated Trip Costs")
        col1, col2 = st.columns(2)
        col1.metric(label="Diesel Truck", value=f"${results['diesel']:,.2f}")
        col2.metric(label="Electric Truck", value=f"${results['electric']:,.2f}")

        st.subheader("Your Estimated Savings")
        st.success(f"You could save approximately ${results['savings']:,.2f} on this trip!")

st.caption("Your data is anonymized and used only to improve our calculations. We respect your privacy and are committed to ethical AI practices.")
