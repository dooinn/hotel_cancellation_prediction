import streamlit as st
from daily_booking_status import app as daily_booking_status
from booking_analysis_report import app as booking_analysis_report
from booking_prediction import app as booking_prediction
from guest_segmentation_analysis import app as guest_segmentation_analysis

# Create a dictionary of pages
pages = {
    "Booking Status Dashboard": daily_booking_status,
    "Revenue & Occupancy Analysis" : booking_analysis_report,
    "Guest Segmentation Analysis" : guest_segmentation_analysis,
    "Booking Prediction": booking_prediction
}

# Radio button in the sidebar for navigation
page = st.sidebar.radio("Choose a page:", tuple(pages.keys()))

# Display the selected page with the content
pages[page]()
