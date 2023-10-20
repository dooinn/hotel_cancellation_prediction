import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

st. set_page_config(layout="wide")
# Load data
@st.cache_data
def load_data():
    return pd.read_csv("city_hotel_dash.csv")  # Adjust path as needed

def app():
    
    data = load_data()

    # Relabel is_canceled
    data['is_canceled'] = data['is_canceled'].replace({0: 'Not Cancelled', 1: 'Cancelled'})

    # Create a column combining year and month for easier grouping
    data['year_month'] = data['arrival_date_year'].astype(str) + "-" + data['arrival_date_month']

    # Streamlit header
    st.title("Booking & Cancellation Analysis")

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        # Extra stacked bar chart for bookings count in each month
        st.subheader("Monthly Booking")
        fig, ax = plt.subplots(figsize=(12, 6))
        monthly_counts = data.groupby(['year_month', 'is_canceled']).size().unstack().fillna(0)
        monthly_counts.plot(kind='bar', stacked=True, colormap="tab20c", ax=ax)
        # Calculate and annotate with cancellation rate
        total_bookings = monthly_counts.sum(axis=1)
        cancelled_bookings = monthly_counts['Cancelled']
        cancellation_rate = (cancelled_bookings / total_bookings) * 100
        for i, rate in enumerate(cancellation_rate):
            ax.text(i, total_bookings.iloc[i] + 20, f"{rate:.2f}%", ha='center')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        content = """
- The booking trends exhibit seasonality. Bookings peak from spring to autumn, indicating these as the high seasons, while winter represents the low season.
- The cancellation rate remains relatively consistent, with an average rate hovering between 30% to 40%.
"""
        st.markdown(content)

 

    with row1_col2:
        st.subheader("Meal")
        counts = data.groupby(['meal', 'is_canceled']).size().unstack().fillna(0)
        total = counts.sum(axis=1)
        cancellation_rate = (counts['Cancelled'] / total) * 100
        fig, ax = plt.subplots(figsize=(12, 6))
        counts.plot(kind='bar', stacked=True, colormap="tab20c", ax=ax)
        for i, rate in enumerate(cancellation_rate):
            ax.text(i, total.iloc[i] + 20, f"{rate:.2f}%", ha='center')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        content = """
- BB (Bed and Breakfast) is the most commonly chosen meal plan by guests.
- SC (Self Catering) ranks as the second most popular choice. This option allows guests the flexibility to either dine out or prepare their own meals, often perceived as the most economical choice during their stay.
- HB (Half Board) isn't as favored as SC. It includes breakfast and one additional meal, either lunch or dinner.
- FB (Full Board) encompasses all three meals: breakfast, lunch, and dinner, provided by the hotel. While it's the priciest meal plan, it's noteworthy that its cancellation rate stands at a staggering 79.55%. This rate is significantly higher than other meal plans, which range from 37% to 42%. It's plausible that guests who initially opt for FB might later reconsider to experience local restaurants or simply change their dining preferences.
"""
        st.markdown(content)
    


    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.subheader("Country")
        top_countries = data['country'].value_counts().index[:10]
        data_filtered = data[data['country'].isin(top_countries)]
        counts = data_filtered.groupby(['country', 'is_canceled']).size().unstack().fillna(0)
        total = counts.sum(axis=1)
        cancellation_rate = (counts['Cancelled'] / total) * 100
        fig, ax = plt.subplots(figsize=(12, 6))
        counts.plot(kind='bar', stacked=True, colormap="tab20c", ax=ax)
        for i, rate in enumerate(cancellation_rate):
            ax.text(i, total.iloc[i] + 20, f"{rate:.2f}%", ha='center')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        
    with row2_col2:
        st.subheader("Local vs Foreign guests bookings")
        data['guest_origin'] = data['country'].apply(lambda x: 'Local' if x == 'PRT' else 'Foreign')
        # top_countries = data['country'].value_counts().index[:10]
        # data_filtered = data[data['country'].isin(top_countries)]
        counts = data.groupby(['guest_origin', 'is_canceled']).size().unstack().fillna(0)
        total = counts.sum(axis=1)
        cancellation_rate = (counts['Cancelled'] / total) * 100
        fig, ax = plt.subplots(figsize=(12, 6))
        counts.plot(kind='bar', stacked=True, colormap="tab20c", ax=ax)
        for i, rate in enumerate(cancellation_rate):
            ax.text(i, total.iloc[i] + 20, f"{rate:.2f}%", ha='center')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
    content = """
- Given the hotel's location in Lisbon, it's unsurprising that the majority of guests hail from Portugal.
- Interestingly, the combined number of international guests surpasses that of local visitors, suggesting that the hotel is primarily frequented by foreign travelers.
- Guests from countries in close proximity to Portugal, especially from Europe, tend to dominate the booking statistics compared to those from farther afield.
- On the topic of cancellations, local guests exhibit a markedly higher rate than their international counterparts. This might be attributed to the fact that foreign guests typically book with more conviction, possibly due to the effort and planning involved in international travel.
- It's worth considering that these international visitors could be significant contributors to the hotel's revenue stream.
"""
    st.markdown(content)
    
    
    
    


    row3_col1, row3_col2 = st.columns(2)
    
    with row3_col1:
        st.subheader("Reserved Room Type")
        counts = data.groupby(['reserved_room_type', 'is_canceled']).size().unstack().fillna(0)
        total = counts.sum(axis=1)
        cancellation_rate = (counts['Cancelled'] / total) * 100
        fig, ax = plt.subplots(figsize=(12, 6))
        counts.plot(kind='bar', stacked=True, colormap="tab20c", ax=ax)
        for i, rate in enumerate(cancellation_rate):
            ax.text(i, total.iloc[i] + 20, f"{rate:.2f}%", ha='center')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
    

    with row3_col2:
        st.subheader("ADR distribution by Room Type")
        unique_room_types = data['reserved_room_type'].unique()
        colors = sns.color_palette("husl", len(unique_room_types))
        fig, ax = plt.subplots(figsize=(20, 10))

        for idx, room_type in enumerate(unique_room_types):
            subset = data[data['reserved_room_type'] == room_type]
            median_adr = subset['adr'].median()
            label = f"{room_type} (Median: ${median_adr:.2f})"
            sns.kdeplot(subset['adr'], label=label, color=colors[idx], shade=True, ax=ax)

        ax.set_title('Distribution of ADR for Each Reserved Room Type')
        ax.set_xlabel('Average Daily Rate (ADR)')
        ax.set_ylabel('Density')
        ax.legend(title='Reserved Room Type')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        st.pyplot(fig)
    
    row4_col1, row4_col2 = st.columns(2)
    
    with row4_col1:
        st.subheader("Deposit Type")
        counts = data.groupby(['deposit_type', 'is_canceled']).size().unstack().fillna(0)
        total = counts.sum(axis=1)
        cancellation_rate = (counts['Cancelled'] / total) * 100
        fig, ax = plt.subplots(figsize=(12, 6))
        counts.plot(kind='bar', stacked=True, colormap="tab20c", ax=ax)
        for i, rate in enumerate(cancellation_rate):
            ax.text(i, total.iloc[i] + 20, f"{rate:.2f}%", ha='center')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
    with row4_col2:        
        st.subheader("Market Segment")
        counts = data.groupby(['market_segment', 'is_canceled']).size().unstack().fillna(0)
        total = counts.sum(axis=1)
        cancellation_rate = (counts['Cancelled'] / total) * 100
        fig, ax = plt.subplots(figsize=(12, 6))
        counts.plot(kind='bar', stacked=True, colormap="tab20c", ax=ax)
        for i, rate in enumerate(cancellation_rate):
            ax.text(i, total.iloc[i] + 20, f"{rate:.2f}%", ha='center')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        

    
    row5_col1, row5_col2 = st.columns(2)
    with row5_col1:
        st.subheader("Guest Group Type")
        counts = data.groupby(['guest_group_type', 'is_canceled']).size().unstack().fillna(0)
        total = counts.sum(axis=1)
        cancellation_rate = (counts['Cancelled'] / total) * 100
        fig, ax = plt.subplots(figsize=(12, 6))
        counts.plot(kind='bar', stacked=True, colormap="tab20c", ax=ax)
        for i, rate in enumerate(cancellation_rate):
            ax.text(i, total.iloc[i] + 20, f"{rate:.2f}%", ha='center')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    


    # Create a temporary numeric version of the 'is_canceled' column for calculations
    data['is_canceled_numeric'] = data['is_canceled'].replace({'Not Cancelled': 0, 'Cancelled': 1})


    row6_col1, row6_col2, row6_col3  = st.columns(3)
    with row6_col1:
        st.subheader("Lead Time")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(x='is_canceled', y='lead_time', data=data, ax=ax, palette="tab20c")
        ax.set_title(f"Box plot of Lead Time vs. Cancellation Status")
        st.pyplot(fig)
    
    with row6_col2:
        st.subheader("ADR")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(x='is_canceled', y='adr', data=data, ax=ax, palette="tab20c")
        ax.set_title(f"Box plot of ADR vs. Cancellation Status")
        st.pyplot(fig)
    
    with row6_col3:   
        st.subheader("Total Stay Nights")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(x='is_canceled', y='total_stay_nights', data=data, ax=ax, palette="tab20c")
        ax.set_title(f"Box plot of Stay Nights vs. Cancellation Status")
        st.pyplot(fig)
    
    
    
    row7_col1, row7_col2, row7_col3, row7_4, row7_5  = st.columns(5)
    with row7_col1:
        st.subheader("Repeated Guest")
        fig, ax = plt.subplots(figsize=(12, 6))
        means = data.groupby('is_repeated_guest')['is_canceled_numeric'].mean()
        means.plot(kind='bar', ax=ax, color='lightblue')
        ax.set_title(f"Mean Cancellation Rate by Repated Guest")
        ax.set_ylabel("Mean Cancellation Rate")
        for j, rate in enumerate(means):
            ax.text(j, rate + 0.02, f"{rate:.2f}", ha='center')
        st.pyplot(fig)
    
    with row7_col2:
        st.subheader("Previous Cancellation")
        fig, ax = plt.subplots(figsize=(12, 6))
        means = data.groupby('previous_cancellations')['is_canceled_numeric'].mean()
        means.plot(kind='bar', ax=ax, color='lightblue')
        ax.set_title(f"Mean Cancellation Rate by Previous Cancellation")
        ax.set_ylabel("Mean Cancellation Rate")
        for j, rate in enumerate(means):
            ax.text(j, rate + 0.02, f"{rate:.2f}", ha='center')
        st.pyplot(fig)
    
    with row7_col3:
        st.subheader("Booking Changes")
        fig, ax = plt.subplots(figsize=(12, 6))
        means = data.groupby('booking_changes')['is_canceled_numeric'].mean()
        means.plot(kind='bar', ax=ax, color='lightblue')
        ax.set_title(f"Mean Cancellation Rate by Booking Changes")
        ax.set_ylabel("Mean Cancellation Rate")
        for j, rate in enumerate(means):
            ax.text(j, rate + 0.02, f"{rate:.2f}", ha='center')
        st.pyplot(fig)
    
    with row7_4:
        st.subheader("Car Parking Request")
        fig, ax = plt.subplots(figsize=(12, 6))
        means = data.groupby('required_car_parking_spaces')['is_canceled_numeric'].mean()
        means.plot(kind='bar', ax=ax, color='lightblue')
        ax.set_title(f"Mean Cancellation Rate by Car Parking Spaces Request")
        ax.set_ylabel("Mean Cancellation Rate")
        for j, rate in enumerate(means):
            ax.text(j, rate + 0.02, f"{rate:.2f}", ha='center')
        st.pyplot(fig)
        
    with row7_5:
        st.subheader("Special Request")
        fig, ax = plt.subplots(figsize=(12, 6))
        means = data.groupby('total_of_special_requests')['is_canceled_numeric'].mean()
        means.plot(kind='bar', ax=ax, color='lightblue')
        ax.set_title(f"Mean Cancellation Rate by Special Requests")
        ax.set_ylabel("Mean Cancellation Rate")
        for j, rate in enumerate(means):
            ax.text(j, rate + 0.02, f"{rate:.2f}", ha='center')
        st.pyplot(fig)
        

    

   
