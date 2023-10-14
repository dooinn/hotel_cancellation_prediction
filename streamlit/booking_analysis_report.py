import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def app():
# Load the data
    @st.cache_data  # This function will be cached
    def load_data():
        data = pd.read_csv('data.csv')
        data['year_month'] = data['arrival_date_year'].astype(str) + '-' + data['arrival_date_month']
        
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        data['arrival_date_month'] = pd.Categorical(data['arrival_date_month'], categories=month_order, ordered=True)
        
        data = data.sort_values(by=['arrival_date_year', 'arrival_date_month'])
        
        monthly_data = data.groupby('year_month').agg(total_bookings=('is_canceled', 'size'), cancellations=('is_canceled', 'sum')).reset_index()
        monthly_data['cancellation_rate'] = monthly_data['cancellations'] / monthly_data['total_bookings'] * 100  # expressed in percentage
        
        return monthly_data

    data = load_data()

    # Create a figure with secondary y-axis
    fig = go.Figure()

    # Add bar chart for booking count to the figure
    fig.add_trace(go.Bar(x=data['year_month'], y=data['total_bookings'], name='Booking Count'))

    # Add line chart for cancellation rate to the figure
    fig.add_trace(go.Scatter(x=data['year_month'], y=data['cancellation_rate'], name='Cancellation Rate (%)', yaxis='y2'))

    # Update layout to include secondary y-axis
    fig.update_layout(
        yaxis=dict(title='Booking Count'),
        yaxis2=dict(title='Cancellation Rate (%)', overlaying='y', side='right'),
        title='Monthly Booking Count vs Cancellation Rate',
        xaxis_title='Year-Month'
    )

    # Display the graph in Streamlit app
    st.plotly_chart(fig)
