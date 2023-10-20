import streamlit as st
from booking_analysis_report import app as booking_analysis_report
from booking_prediction import app as booking_prediction
from guest_segmentation_analysis import app as guest_segmentation_analysis
from main_dashboard import app as main_dashboard
from glossary import app as glossary

# Create a dictionary of pages
pages = {
    "Main Booking Dashboard" : main_dashboard,
    "Booking Analysis" : booking_analysis_report,
    "Guest Segmentation Analysis" : guest_segmentation_analysis,
    "Booking Prediction": booking_prediction,
    "Glossary": glossary
}

# Radio button in the sidebar for navigation
page = st.sidebar.radio("Choose a page:", tuple(pages.keys()))

# Display the selected page with the content
pages[page]()
