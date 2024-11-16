import streamlit as st
import sys
import pandas as pd
sys.path.insert(0, '/Users/tanishqgoyal/Desktop/Ideathon/Ideathon_submission')
from functions.Intrinsic_value import calculate_intrinsic_value  # Import your calculation function
from functions.chatbot import chat_interface  # Import the chatbot component

# Set the page configuration
st.set_page_config(
    page_title="Company Overview",
    page_icon=":chart_with_upwards_trend:",
    layout="centered"
)
intrinsic_value = 0
# Check if a company has been selected
if "selected_company" not in st.session_state:
    st.error("No company selected. Please go back to the Home Page and select a company.")
else:
    selected_company = st.session_state.selected_company

    # Display the header and selected company name
    st.title("Company Overview")
    st.write(f"### Analysis for: **{selected_company}**")

    try:
            # Call the function and get the intrinsic value
        intrinsic_value = calculate_intrinsic_value(selected_company)
            # Display the intrinsic value in a formatted way
        st.success(f"Intrinsic Value per Share for {selected_company}: **${intrinsic_value:.2f}**")
    except Exception as e:
            # Handle any errors and display an error message
        st.error(f"An error occurred: {str(e)}")
    # Example: Display a placeholder for future data or insights

   # Include the chatbot component with page-specific context
    #chatbot_component(f"I already calculated the intrinsic value for this company. which is {intrinsic_value} What else would you like to know?",)
    #st.info("Stay tuned! Detailed company insights and visualizations will appear here.")
    chat_interface()
