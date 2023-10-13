import streamlit as st
import plotly.express as px
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')
    df['arrival_date'] = pd.to_datetime(df['arrival_date_year'].astype(str) + '-' + 
                                        df['arrival_date_month'] + '-' + 
                                        df['arrival_date_day_of_month'].astype(str))
    return df




# Calculate KPIs
def calculate_kpis(df, selected_date, total_rooms):
    # Filter the data for the selected date
    data_on_date = df[df['arrival_date'] == pd.to_datetime(selected_date)]
    
    # 1. Occupancy Rate
    total_booked_rooms = data_on_date[data_on_date['is_canceled'] == 0]['adults'].sum()
    occupancy_rate = (total_booked_rooms / total_rooms) * 100
    
    # 2. Total Bookings Count
    total_bookings_count = len(data_on_date[data_on_date['is_canceled'] == 0])
    
    # 3. Total Cancellation Count
    total_cancellation_count = len(data_on_date[data_on_date['is_canceled'] == 1])
    
    # 4. Cancellation Rate
    cancellation_rate = (total_cancellation_count / len(data_on_date)) * 100
    
    # 5. Total Available Room Count
    total_available_room_count = total_rooms - total_booked_rooms
    
    return occupancy_rate, total_bookings_count, total_cancellation_count, cancellation_rate, total_available_room_count



# Calculate available and booked rooms per room type
def calculate_rooms_per_type(data_on_date, rooms_by_type):
    # Calculate booked rooms per type
    booked_rooms_per_type = data_on_date[data_on_date['is_canceled'] == 0].groupby('reserved_room_type')['adults'].sum()
    
    # Calculate available rooms per type
    available_rooms_per_type = {room_type: rooms_by_type[room_type] - booked_rooms_per_type.get(room_type, 0)
                                for room_type in rooms_by_type.keys()}
    
    return pd.DataFrame({
        'Room Type': list(rooms_by_type.keys()),
        'Booked': [booked_rooms_per_type.get(rt, 0) for rt in rooms_by_type.keys()],
        'Available': [available_rooms_per_type[rt] for rt in rooms_by_type.keys()]
    })



# Load data
df = load_data()

# Sidebar
st.sidebar.header("Filters")
selected_date = st.sidebar.date_input("Select a Date", min_value=df['arrival_date'].min(), 
                                      value=df['arrival_date'].min(), 
                                      max_value=df['arrival_date'].max())

# Filter the data for the selected date
data_on_date = df[df['arrival_date'] == pd.to_datetime(selected_date)]



# KPIs
st.header("Key Performance Indicators")
occupancy_rate, total_bookings_count, total_cancellation_count, cancellation_rate, total_available_room_count = calculate_kpis(df, selected_date, total_rooms=449)

# Display KPIs
st.metric("Occupancy Rate", f"{occupancy_rate:.2f}%")
st.metric("Total Bookings Count", total_bookings_count)
st.metric("Total Cancellation Count", total_cancellation_count)
st.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")
st.metric("Total Available Room Count", total_available_room_count)

# Room type details as provided in a previous message
rooms_by_type = {
    "A": 319,
    "D": 91,
    "F": 15,
    "E": 12,
    "B": 8,
    "G": 4,
    "C": 0,
    "P": 0
}

# Calculate rooms per type for the selected date
rooms_df = calculate_rooms_per_type(data_on_date, rooms_by_type)

# Create a bar chart
fig = px.bar(rooms_df, 
             x='Room Type', 
             y=['Available', 'Booked'],
             title='Available and Booked Rooms per Room Type',
             labels={'value': 'Room Count', 'variable': 'Status'},
             color_discrete_map={'Available': 'blue', 'Booked': 'gray'},
             height=400)

# Display bar chart in Streamlit app
st.plotly_chart(fig)