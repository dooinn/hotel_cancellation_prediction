import streamlit as st
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
import pandas as pd

# Loading data functions
@st.cache_data
def load_raw_data():
    data = pd.read_csv('city_hotel.csv')
    data['arrival_date'] = pd.to_datetime(data['arrival_date_year'].astype(str) + '-' + 
                                          data['arrival_date_month'] + '-' + 
                                          data['arrival_date_day_of_month'].astype(str))
    return data

@st.cache_data
def load_monthly_data(data):
    data['year_month'] = data['arrival_date_year'].astype(str) + '-' + data['arrival_date_month']
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    data['arrival_date_month'] = pd.Categorical(data['arrival_date_month'], categories=month_order, ordered=True)
    data = data.sort_values(by=['arrival_date_year', 'arrival_date_month'])
    monthly_data = data.groupby('year_month').agg(total_bookings=('is_canceled', 'size'), cancellations=('is_canceled', 'sum')).reset_index()
    monthly_data['cancellation_rate'] = monthly_data['cancellations'] / monthly_data['total_bookings'] * 100  # expressed in percentage
    return monthly_data

# Calculation functions
def calculate_annual_occupancy(data):
    daily_occupancy = data.groupby('arrival_date').size().reset_index(name='number_of_bookings')
    daily_occupancy['occupancy_rate'] = (daily_occupancy['number_of_bookings'] / 449) * 100
    date_ranges = [("2015-07-01", "2016-07-01"), ("2016-07-01", "2017-07-01")]
    annual_occupancy_rates = {f"{start_date} to {end_date}": daily_occupancy[(daily_occupancy['arrival_date'] >= start_date) & 
                                          (daily_occupancy['arrival_date'] < end_date)]['occupancy_rate'].mean() 
                             for start_date, end_date in date_ranges}
    return annual_occupancy_rates

def calculate_monthly_occupancy(data):
    monthly_occupancy = data.groupby(data['arrival_date'].dt.to_period("M")).size().reset_index(name='number_of_bookings')
    monthly_occupancy['occupancy_rate'] = (monthly_occupancy['number_of_bookings'] / 449) * 100
    monthly_occupancy.columns = ['Month-Year', 'Number of Bookings', 'Average Occupancy Rate (%)']
    monthly_occupancy['Month-Year'] = monthly_occupancy['Month-Year'].dt.strftime('%B %Y')
    return monthly_occupancy

def create_occupancy_heatmap(data):
    data['month'] = data['arrival_date'].dt.month_name()
    data['day_of_week'] = data['arrival_date'].dt.day_name()
    data['occupancy_rate'] = (1 / 449) * 100  # Since each row represents a booking, the occupancy for each row is 1/449
    avg_occupancy = data.groupby(['month', 'day_of_week'])['occupancy_rate'].mean().unstack().reset_index()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    avg_occupancy['month'] = pd.Categorical(avg_occupancy['month'], categories=month_order, ordered=True)
    avg_occupancy = avg_occupancy.sort_values('month').set_index('month')[day_order]
    fig = go.Figure(data=go.Heatmap(z=avg_occupancy.values, x=avg_occupancy.columns, y=avg_occupancy.index, colorscale="Viridis", showscale=True))
    fig.update_layout(title="Average Occupancy Rate by Month and Day of Week", xaxis_title="Day of Week", yaxis_title="Month")
    return fig

def display_booking_cancellation_trend(monthly_data):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly_data['year_month'], y=monthly_data['total_bookings'], name='Booking Count'))
    fig.add_trace(go.Scatter(x=monthly_data['year_month'], y=monthly_data['cancellation_rate'], name='Cancellation Rate (%)', yaxis='y2'))
    fig.update_layout(yaxis=dict(title='Booking Count'), yaxis2=dict(title='Cancellation Rate (%)', overlaying='y', side='right'), title='Monthly Booking Count vs Cancellation Rate', xaxis_title='Year-Month')
    st.plotly_chart(fig)

def app():
    raw_data = load_raw_data()
    monthly_data = load_monthly_data(raw_data)
    
    st.header("Revenue Trend")
    raw_data['total_revenue'] = raw_data['adr'] * (raw_data['stays_in_weekend_nights'] + raw_data['stays_in_week_nights'])
    revenue_trend = raw_data.groupby('arrival_date')['total_revenue'].sum().reset_index()
    fig_revenue_trend = px.line(revenue_trend, x='arrival_date', y='total_revenue', title='Revenue Over Time')
    st.plotly_chart(fig_revenue_trend)
    
    st.header("Annual Occupancy Rates")
    annual_rates = calculate_annual_occupancy(raw_data)
    for period, rate in annual_rates.items():
        st.write(f"{period}: {rate:.2f}%")
    
    st.header("Occupancy Rate Trend")
    daily_occupancy = raw_data.groupby('arrival_date').size().reset_index(name='number_of_bookings')
    daily_occupancy['occupancy_rate'] = (daily_occupancy['number_of_bookings'] / 449) * 100
    fig_occupancy_trend = px.line(daily_occupancy, x='arrival_date', y='occupancy_rate', title='Occupancy Rate Over Time')
    st.plotly_chart(fig_occupancy_trend)
    
    st.header("Average Monthly Occupancy Rate")
    monthly_rates = calculate_monthly_occupancy(raw_data)
    st.table(monthly_rates)
    
    st.header("Average Occupancy Rate Heatmap")
    avg_occupancy_heatmap = create_occupancy_heatmap(raw_data)
    st.plotly_chart(avg_occupancy_heatmap)
    
    st.header("Booking & Cancellation Trend")
    display_booking_cancellation_trend(monthly_data)
