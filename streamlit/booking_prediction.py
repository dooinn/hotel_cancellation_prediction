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
    deposit_type_Non_Refund = st.selectbox('Is Deposit Type Non Refund?', options=[0, 1])
    market_segment_Online_TA = st.selectbox('Is Market Segment Online TA', options=[0, 1])
    
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
    'lead_time': 0,
    'arrival_date_year': 2016,
    'arrival_date_month': 8,
    'arrival_date_week_number': 33,
    'arrival_date_day_of_month': 20,
    'stays_in_weekend_nights': 0,
    'stays_in_week_nights': 2,
    'adults': 2,
    'children': 0.0,
    'babies': 0,
    'is_repeated_guest': 0,
    'previous_bookings_not_canceled': 0,
    'booking_changes': 0,
    'days_in_waiting_list': 0,
    'adr': 0.0,
    'meal_FB': 0,
    'meal_HB': 0,
    'meal_SC': 0,
    'market_segment_Complementary': 0,
    'market_segment_Corporate': 0,
    'market_segment_Direct': 0,
    'market_segment_Groups': 0,
    'market_segment_Offline TA/TO': 0,
    'market_segment_Undefined': 0,
    'distribution_channel_Direct': 0,
    'distribution_channel_GDS': 0,
    'distribution_channel_TA/TO': 1,
    'distribution_channel_Undefined': 0,
    'reserved_room_type_B': 0,
    'reserved_room_type_C': 0,
    'reserved_room_type_D': 0,
    'reserved_room_type_E': 0,
    'reserved_room_type_F': 0,
    'reserved_room_type_G': 0,
    'reserved_room_type_P': 0,
    'deposit_type_Refundable': 0,
    'customer_type_Group': 0,
    'customer_type_Transient': 1,
    'customer_type_Transient-Party': 0
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
        prediction_proba = model.predict_proba(user_input)[0][1]  # Get the probability of class 1 (cancellation)
        
        st.write(f"Probability of cancellation: {prediction_proba * 100:.2f}%")
        
        if prediction[0] == 1:
            st.write("The booking is likely to be cancelled.")
        else:
            st.write("The booking is likely to be not cancelled.")

# Run the app
if __name__ == "__main__":
    app()
