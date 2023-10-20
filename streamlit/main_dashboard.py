import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import time

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('city_hotel_dash.csv')
    df['arrival_date'] = pd.to_datetime(df['arrival_date'])
    return df

def app():
    df = load_data()
    st.title("Hotel Booking KPI Dashboard")
    st.write("Only the confirmed booking(=not canceled) results presented")




    # Convert Timestamp to native Python datetime.date
    min_date = df['arrival_date'].min().date()
    max_date = df['arrival_date'].max().date()

    # Initialize or reset session_state
    if not hasattr(st.session_state, 'selected_year'):
        st.session_state.selected_year = None

    # Create columns for buttons
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    # Place buttons in columns
    with filter_col1:
        if st.button('All'):
            st.session_state.selected_year = 'All'
    with filter_col2:
        if st.button('2015'):
            st.session_state.selected_year = '2015'
    with filter_col3:
        if st.button('2016'):
            st.session_state.selected_year = '2016'
    with filter_col4:
        if st.button('2017'):
            st.session_state.selected_year = '2017'

    # Dropdown to filter by specific date
    unique_dates = sorted(df['arrival_date'].dt.date.unique())
    selected_date = st.selectbox('Select a specific date', ['None'] + unique_dates)
    
    if selected_date != 'None':
        filtered_df = df[df['arrival_date'].dt.date == selected_date]
    else:
        # Set date range based on session state
        if st.session_state.selected_year == 'All':
            default_date_range = (min_date, max_date)
        elif st.session_state.selected_year == '2015':
            default_date_range = (datetime.date(2015, 1, 1), datetime.date(2015, 12, 31))
        elif st.session_state.selected_year == '2016':
            default_date_range = (datetime.date(2016, 1, 1), datetime.date(2016, 12, 31))
        elif st.session_state.selected_year == '2017':
            default_date_range = (datetime.date(2017, 1, 1), datetime.date(2017, 12, 31))
        else:
            default_date_range = (min_date, max_date)

        date_range = st.slider('Select Date Range for Analysis', min_date, max_date, default_date_range)

        filtered_df = df[(df['arrival_date'].dt.date >= date_range[0]) & (df['arrival_date'].dt.date <= date_range[1])]





    # KPIs
    col1, col2, col3, col4  = st.columns(4)

    # Function to wrap content with a border
    def bordered_content(content):
        return f"<div style='border: 2px solid; padding: 10px; border-radius: 5px;'>{content}</div>"

    # Total Booking Count
    with col1:
        st.subheader("Total Bookings")
        valid_booking = filtered_df.loc[filtered_df['is_canceled'] == 0]
        total_booking_count = len(valid_booking)
        st.markdown(bordered_content(total_booking_count), unsafe_allow_html=True)


    # Total Revenues
    with col2:
        st.subheader("Total Revenues")
        total_revenues = filtered_df.loc[filtered_df['is_canceled'] == 0, 'total_rate'].sum()
        st.markdown(bordered_content(f"${total_revenues:,.2f}"), unsafe_allow_html=True)

    # Average Nights per Booking
    with col3:
        st.subheader("Avg. Nights/Booking")
        valid_booking = filtered_df.loc[filtered_df['is_canceled'] == 0]
        avg_nights_per_booking = valid_booking['total_stay_nights'].mean()
        st.markdown(bordered_content(f"{avg_nights_per_booking:.2f}"), unsafe_allow_html=True)

    # Average Guests per Booking
    with col4:
        st.subheader("Avg. Guests/Booking")
        valid_booking = filtered_df.loc[filtered_df['is_canceled'] == 0]
        avg_guests_per_booking = valid_booking['total_guests'].mean()
        st.markdown(bordered_content(f"{avg_guests_per_booking:.2f}"), unsafe_allow_html=True)




    # Create columns for the plots
    plot1_col1, plot2_col2 = st.columns(2)

    # Time trend of bookings per month in the first column
    with plot1_col1:
        st.subheader("Time Trend of Bookings per Month")
        filtered_df['year_month'] = filtered_df['arrival_date'].dt.to_period('M').astype(str)

        # Filter only the rows where is_canceled = 0
        bookings_df = filtered_df[filtered_df['is_canceled'] == 0]
        bookings_per_month = bookings_df.groupby('year_month').size()

        fig_bookings = px.bar(bookings_per_month, x=bookings_per_month.index, y=bookings_per_month.values, 
                            labels={'year_month': 'Month', 'value': 'Number of Bookings'},
                            title='Time Trend of Bookings per Month')
        st.plotly_chart(fig_bookings)

    # Time trend of total revenues per month in the second column
    with plot2_col2:
        st.subheader("Time Trend of Total Revenues per Month")
        revenues_per_month = filtered_df[filtered_df['is_canceled'] == 0].groupby('year_month')['total_rate'].sum()
        fig_revenues = px.line(revenues_per_month, x=revenues_per_month.index, y=revenues_per_month.values,
                               labels={'year_month': 'Month', 'y': 'Total Revenues'},
                               title='Time Trend of Total Revenues per Month')
        st.plotly_chart(fig_revenues)

    
    
    plot2_col1, plot2_col2 = st.columns(2)

    # Filter only the rows where is_canceled = 0
    bookings_df = filtered_df[filtered_df['is_canceled'] == 0]

    with plot2_col1:
        st.subheader("Reserved Room Type")
        room_bookings = bookings_df['reserved_room_type'].value_counts()
        fig_room_type = px.bar(room_bookings, x=room_bookings.index, y=room_bookings.values,
                            labels={'reserved_room_type': 'Room Type', 'value': 'Number of Bookings'},
                            title='Reserved Room Type')
        st.plotly_chart(fig_room_type)

    with plot2_col2:
        st.subheader("Meal Type")
        meal_bookings = bookings_df['meal'].value_counts()
        fig_meal_type = px.bar(meal_bookings, x=meal_bookings.index, y=meal_bookings.values,
                            labels={'meal': 'Meal Type', 'value': 'Number of Bookings'},
                            title='Meal Type')
        st.plotly_chart(fig_meal_type)

    plot3_col1, plot3_col2, plot3_col3 = st.columns(3)

    with plot3_col1:
        st.subheader("Top 10 Countries with Most Bookings")
        country_bookings = bookings_df['country'].value_counts()
        top_countries = country_bookings.nlargest(10)
        fig_countries = px.bar(top_countries, x=top_countries.index, y=top_countries.values,
                            labels={'country': 'Country', 'value': 'Number of Bookings'},
                            title='Top 10 Countries with Most Bookings')
        st.plotly_chart(fig_countries)

    with plot3_col2:
        st.subheader("Bookings Count by Guest Group Type")
        guest_group_bookings = bookings_df['guest_group_type'].value_counts()
        fig_guest_group = px.bar(guest_group_bookings, x=guest_group_bookings.index, y=guest_group_bookings.values,
                                labels={'guest_group_type': 'Guest Group Type', 'value': 'Number of Bookings'},
                                title='Bookings Count by Guest Group Type')
        st.plotly_chart(fig_guest_group)

    with plot3_col3:
        st.subheader("Bookings Count by Deposit Type")
        deposit_type_bookings = bookings_df['deposit_type'].value_counts()
        fig_deposit_type = px.bar(deposit_type_bookings, x=deposit_type_bookings.index, y=deposit_type_bookings.values,
                                labels={'deposit_type': 'Deposit Type', 'value': 'Number of Bookings'},
                                title='Bookings Count by Deposit Type')
        st.plotly_chart(fig_deposit_type)

        
    # Define the columns to display
    columns_to_display = ['name','arrival_date', 'check_out_date','country', 'guest_group_type','total_guests', 'total_stay_nights', 'total_rate', 'reserved_room_type', 'is_canceled']

    # Get the name input from the user
    name_input = st.text_input("Filter by guest name:")

    # Filter the dataframe based on the name input
    if name_input:
        filtered_df = filtered_df[filtered_df['name'].str.contains(name_input, case=False, na=False)]

    # Display a table of booking info filtered by dates
    st.subheader("List of Bookings")
    st.write(filtered_df[columns_to_display])

    if __name__ == "__main__":
        st.write("Dashboard is active!")
