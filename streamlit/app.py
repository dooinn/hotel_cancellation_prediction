import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    data = pd.read_csv('city_hotel_dash.csv')
    data['arrival_date'] = pd.to_datetime(data['arrival_date'])
    data['check_out_date'] = pd.to_datetime(data['check_out_date'])
    return data

def main():
    st.title("Hotel Booking Analysis")
    st.write("Welcome to the hotel booking analysis dashboard!")
    
    # Load data
    data = load_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")

    # Date range selector
    date_range = st.sidebar.date_input("Select Date Range", [data['arrival_date'].min(), data['arrival_date'].max()])
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

    # Multiple selectors
    selected_countries = st.sidebar.multiselect("Select Countries", data['country'].unique().tolist())
    selected_segments = st.sidebar.multiselect("Select Market Segments", data['market_segment'].unique().tolist())
    selected_canceled = st.sidebar.multiselect("Select Cancellation Status", [0, 1])
    selected_meal = st.sidebar.multiselect("Select Meal Type", data['meal'].unique().tolist())
    selected_repeated_guest = st.sidebar.multiselect("Select Repeated Guest", [0, 1])
    selected_room_type = st.sidebar.multiselect("Select Reserved Room Type", data['reserved_room_type'].unique().tolist())
    selected_deposit_type = st.sidebar.multiselect("Select Deposit Type", data['deposit_type'].unique().tolist())
    selected_guest_group = st.sidebar.multiselect("Select Guest Group Type", data['guest_group_type'].unique().tolist())
    selected_guest_origin = st.sidebar.multiselect("Select Guest Origin", data['guest_origin'].unique().tolist())
    
    # Sliders
    lead_time = st.sidebar.slider("Select Lead Time Range", int(data['lead_time'].min()), int(data['lead_time'].max()), (int(data['lead_time'].min()), int(data['lead_time'].max())))
    adr = st.sidebar.slider("Select ADR Range", float(data['adr'].min()), float(data['adr'].max()), (float(data['adr'].min()), float(data['adr'].max())))
    total_rate = st.sidebar.slider("Select Total Rate Range", float(data['total_rate'].min()), float(data['total_rate'].max()), (float(data['total_rate'].min()), float(data['total_rate'].max())))
    total_stay_nights = st.sidebar.slider("Select Total Stay Nights Range", int(data['total_stay_nights'].min()), int(data['total_stay_nights'].max()), (int(data['total_stay_nights'].min()), int(data['total_stay_nights'].max())))
    total_guests = st.sidebar.slider("Select Total Guests Range", int(data['total_guests'].min()), int(data['total_guests'].max()), (int(data['total_guests'].min()), int(data['total_guests'].max())))
    
    # Filter data based on selections
    filtered_data = data[
        (data['arrival_date'] >= start_date) & 
        (data['arrival_date'] <= end_date) & 
        (data['country'].isin(selected_countries) if selected_countries else True) &
        (data['market_segment'].isin(selected_segments) if selected_segments else True) &
        (data['is_canceled'].isin(selected_canceled) if selected_canceled else True) &
        (data['meal'].isin(selected_meal) if selected_meal else True) &
        (data['is_repeated_guest'].isin(selected_repeated_guest) if selected_repeated_guest else True) &
        (data['reserved_room_type'].isin(selected_room_type) if selected_room_type else True) &
        (data['deposit_type'].isin(selected_deposit_type) if selected_deposit_type else True) &
        (data['guest_group_type'].isin(selected_guest_group) if selected_guest_group else True) &
        (data['guest_origin'].isin(selected_guest_origin) if selected_guest_origin else True) &
        (data['lead_time'].between(lead_time[0], lead_time[1])) &
        (data['adr'].between(adr[0], adr[1])) &
        (data['total_rate'].between(total_rate[0], total_rate[1])) &
        (data['total_stay_nights'].between(total_stay_nights[0], total_stay_nights[1])) &
        (data['total_guests'].between(total_guests[0], total_guests[1]))
    ]
    
    
    
    st.write(filtered_data.head())
    
    
    
    
    
       # Revenue Analysis
    st.header("Revenue Analysis")
    
    # 1. Time series plot of revenue over time
    revenue_over_time = filtered_data.groupby('arrival_date')['total_rate'].sum().reset_index()
    fig1 = px.line(revenue_over_time, x='arrival_date', y='total_rate', title="Revenue Over Time")
    st.plotly_chart(fig1)

    # 2. Average daily rate (ADR) distribution
    fig2 = px.histogram(filtered_data, x='adr', nbins=50, title="Distribution of Average Daily Rate (ADR)")
    st.plotly_chart(fig2)

    # 3. Top countries by revenue
    countries_revenue = filtered_data.groupby('country')['total_rate'].sum().sort_values(ascending=False).reset_index().head(10)
    fig3 = px.bar(countries_revenue, x='country', y='total_rate', title="Top Countries by Revenue", labels={'total_rate': 'Revenue', 'country': 'Country'})
    st.plotly_chart(fig3)

if __name__ == "__main__":
    main()
