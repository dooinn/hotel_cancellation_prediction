import streamlit as st
import plotly.express as px
import pandas as pd

# Constants
TOTAL_ROOMS = 449
ROOMS_BY_TYPE = {
    "A": 319, "D": 91, "F": 15, "E": 12, 
    "B": 8, "G": 4, "C": 0, "P": 0
}

@st.cache_data
def load_data():
    """Load the dataset"""
    return pd.read_csv('city_hotel.csv')

def transform_data(df):
    """Transforms the dataset by adding arrival_date column"""
    df['arrival_date'] = pd.to_datetime(df['arrival_date_year'].astype(str) + '-' + 
                                        df['arrival_date_month'] + '-' + 
                                        df['arrival_date_day_of_month'].astype(str))
    return df

def calculate_kpis(data_on_date, total_rooms):
    """Calculate KPIs for the given data on the selected date"""
    # Calculate based on cancellation status
    total_bookings_count = len(data_on_date[data_on_date['is_canceled'] == 0])
    total_cancellation_count = len(data_on_date) - total_bookings_count
    
    # Derive other metrics
    occupancy_rate = (total_bookings_count / total_rooms) * 100
    cancellation_rate = (total_cancellation_count / len(data_on_date)) * 100
    total_available_room_count = total_rooms - total_bookings_count
    
    return occupancy_rate, total_bookings_count, total_cancellation_count, cancellation_rate, total_available_room_count

def calculate_rooms_per_type(data_on_date):
    """Calculate rooms per type for the given data on the selected date"""
    # Count booked rooms per type where 'is_canceled' is 0
    booked_rooms_per_type = data_on_date[data_on_date['is_canceled'] == 0].groupby('reserved_room_type').size()
    
    # Calculate available rooms per type
    available_rooms_per_type = {room_type: ROOMS_BY_TYPE[room_type] - booked_rooms_per_type.get(room_type, 0)
                                for room_type in ROOMS_BY_TYPE.keys()}
    
    return pd.DataFrame({
        'Room Type': list(ROOMS_BY_TYPE.keys()),
        'Booked': [booked_rooms_per_type.get(rt, 0) for rt in ROOMS_BY_TYPE.keys()],
        'Available': [available_rooms_per_type[rt] for rt in ROOMS_BY_TYPE.keys()]
    })
    
def display_kpis(occupancy_rate, total_bookings_count, total_cancellation_count, cancellation_rate, total_available_room_count):
    """Display the KPIs on the Streamlit dashboard"""
    cols = st.columns(5)

    with cols[0]:
        st.metric("Occupancy Rate", f"{occupancy_rate:.2f}%")
    with cols[1]:
        st.metric("Total Bookings Count", total_bookings_count)
    with cols[2]:
        st.metric("Total Cancellation Count", total_cancellation_count)
    with cols[3]:
        st.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")
    with cols[4]:
        st.metric("Total Available Room Count", total_available_room_count)

def display_charts(total_booked_rooms, total_cancellation_count, data_on_date):
    """Display the charts on the Streamlit dashboard"""
    chart_cols = st.columns(3)

    with chart_cols[0]:
        occupancy_data = {
            'Status': ['Occupied', 'Available'],
            'Rooms': [total_booked_rooms, TOTAL_ROOMS - total_booked_rooms]
        }
        occupancy_fig = px.pie(occupancy_data, names='Status', values='Rooms', title='Occupancy Rate')
        st.plotly_chart(occupancy_fig)

    with chart_cols[1]:
        cancellation_data = {
            'Status': ['Cancelled', 'Not Cancelled'],
            'Bookings': [total_cancellation_count, total_booked_rooms]
        }
        cancellation_fig = px.pie(cancellation_data, names='Status', values='Bookings', title='Cancellation Rate')
        st.plotly_chart(cancellation_fig)

    with chart_cols[2]:
        rooms_df = calculate_rooms_per_type(data_on_date)
        fig = px.bar(rooms_df, 
                     x='Room Type', 
                     y=['Available', 'Booked'],
                     title='Available and Booked Rooms per Room Type',
                     labels={'value': 'Room Count', 'variable': 'Status'},
                     height=400)
        st.plotly_chart(fig)

def display_booking_list(data_on_date):
    """Display the booking list on the Streamlit dashboard"""
    filtered_data = data_on_date[data_on_date['is_canceled'] == 0]
    guest_info = filtered_data[['country', 'adults', 'children', 'babies', 'reserved_room_type', 'adr', 'reservation_status']]
    
    st.header("Booking List")
    st.table(guest_info)

def app():
    # Load and transform data
    df = transform_data(load_data())
    
    # Header
    st.header("Booking Status Dashboard")

    # Date Filter
    selected_date = st.date_input("Select a Date", min_value=df['arrival_date'].min(), 
                                  value=df['arrival_date'].max(), 
                                  max_value=df['arrival_date'].max())
    
    # Filter the data for the selected date
    data_on_date = df[df['arrival_date'] == pd.to_datetime(selected_date)]
    
    # Calculate and display KPIs
    kpis = calculate_kpis(data_on_date, TOTAL_ROOMS)
    display_kpis(*kpis)
    
    # Display charts
    display_charts(kpis[1], kpis[2], data_on_date)
    
    # Display booking list
    display_booking_list(data_on_date)

# If the script is executed, run the app
if __name__ == "__main__":
    app()