import streamlit as st
import plotly.express as px
import pandas as pd


def load_data():
    data = pd.read_csv('city_hotel_dash.csv')
    return data

def app():
    st.title("Hotel Booking Analysis")
    st.write("Welcome to the hotel booking analysis dashboard!")
    
    # Load data
    data = load_data()
    
    # Display data (for initial testing)
    st.write(data.head())

if __name__ == "__main__":
    app()