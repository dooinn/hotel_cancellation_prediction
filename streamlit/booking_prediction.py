import streamlit as st
import pickle
import pandas as pd

# Load the model outside of the function to avoid reloading it every time the function runs
with open('xgboost_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Define the function to get user inputs

def get_user_input():
    # Numerical Input
    previous_cancellations = st.slider('Previous Cancellations', min_value=0, max_value=10, value=0)
    required_car_parking_spaces = st.slider('Required Car Parking Spaces', min_value=0, max_value=5, value=0)
    total_of_special_requests = st.slider('Total of Special Requests', min_value=0, max_value=5, value=0)
    
    # Categorical Input
    deposit_type_Non_Refund = st.selectbox('Deposit Type Non Refund', options=[0, 1])
    market_segment_Online_TA = st.selectbox('Market Segment Online TA', options=[0, 1])
    
    # User data
    user_data = {
        'previous_cancellations': previous_cancellations,
        'required_car_parking_spaces': required_car_parking_spaces,
        'total_of_special_requests': total_of_special_requests,
        'deposit_type_Non_Refund': deposit_type_Non_Refund,  # Assuming one-hot encoded
        'market_segment_Online_TA': market_segment_Online_TA,  # Assuming one-hot encoded
    }
    
    # Dummy data for the other features
    dummy_data = {
        'hotel': 'City Hotel',
        'lead_time': 100,  
        'arrival_date_year': 2016,  
        'arrival_date_month': 'January',
        'arrival_date_week_number': 1,
        'arrival_date_day_of_month': 1,
        'stays_in_weekend_nights': 1,
        'stays_in_week_nights': 2,
        'adults': 2,
        'children': 0,
        'babies': 0,
        'meal': 'BB',
        'country': 'PRT',
        'market_segment': 'Direct',
        'distribution_channel': 'Direct',
        'is_repeated_guest': 0,
        'previous_bookings_not_canceled': 0,
        'reserved_room_type': 'A',
        'assigned_room_type': 'A',
        'booking_changes': 0,
        'deposit_type': 'No Deposit',
        'agent': 9.0,  # or other typical value
        'days_in_waiting_list': 0,
        'customer_type': 'Transient',
        'adr': 100.0,  # or other typical value
        'reservation_status': 'Check-Out',
        'reservation_status_date': '2017-04-01'
    }

    # Exclude the features used in user input to avoid duplication
    unused_features = [feat for feat in dummy_data.keys() if feat not in user_data.keys()]
    dummy_data = {feat: dummy_data[feat] for feat in unused_features}
    
    # Merge user data and dummy data
    user_data.update(dummy_data)
    
    return pd.DataFrame([user_data])


# Define the main behavior of the streamlit app
def app():
    st.write("# Hotel Booking Cancellation Prediction")
    user_input = get_user_input()

    # Predict and display the result
    if st.button('Predict'):
        prediction = model.predict(user_input)
        
        if prediction[0] == 1:
            st.write("The booking is likely to be cancelled.")
        else:
            st.write("The booking is likely to be not cancelled.")

# Run the app
if __name__ == "__main__":
    app()
