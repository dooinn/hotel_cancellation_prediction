import streamlit as st
import plotly.express as px
import pandas as pd


def app():
    
    st.title("Glossary")
    
    st.subheader("Meal")
    
    
    meal_content = """
- BB (Bed & Breakfast): This plan includes breakfast along with the room stay. No other meals are included.
- HB (Half Board): This plan includes breakfast and one other meal, usually dinner. It does not include any drinks.
- FB (Full Board): This plan includes all three main meals: breakfast, lunch, and dinner. Again, drinks might be extra.
- AI (All Inclusive): This plan includes all meals, snacks, and drinks. Some hotels might also include certain recreational activities in this package.
- SC or Undefined: Stands for Self Catering. No meals are included in the room rate. Guests are responsible for their own meals, either by cooking for themselves (if facilities are provided) or by eating out.
"""

    st.markdown(meal_content)
    
    
    st.subheader("Market Segment")
    
    
    market_segment_content = """
- Direct: Bookings made directly with the hotel, without any intermediaries.
- Corporate: Bookings made by corporate clients.
- Online TA: Bookings made through online travel agents like Expedia, Booking.com, etc.
- Offline TA/TO: Bookings made through offline travel agents or tour operators.
- Groups: Bookings associated with group travel.
- Complementary: Complimentary stays provided by the hotel.
- Aviation: Bookings related to airline crew stays.
- Transient: Individuals or families traveling, not as part of a group or business.
"""

    st.markdown(market_segment_content)
    
    
    
    
    

    
    