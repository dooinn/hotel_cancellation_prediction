import streamlit as st
from daily_booking_status import app as daily_booking_status
from booking_analysis_report import app as booking_analysis_report
from booking_prediction import app as booking_prediction

# Create a dictionary of pages
pages = {
    "Daily Booking Status": daily_booking_status,
    "Monthly Analysis Report" : booking_analysis_report,
    "Booking Prediction": booking_prediction
}

# Radio button in the sidebar for navigation
page = st.sidebar.radio("Choose a page:", tuple(pages.keys()))

# Display the selected page with the content
pages[page]()
