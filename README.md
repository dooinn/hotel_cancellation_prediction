# Hotel Booking Cancellation Prediction

This is part of Ironhack's Final Project. In this endeavor, we aim to address a business challenge: how to maximize the revenue of a hotel. We employ machine learning classification models to predict booking cancellations, a critical factor impacting hotel revenue.


## Table of Contents

1. Introduction
2. Data
3. Methodology
4. Results
5. Conclusion


## 1. Introduction

- **Background**:


Hotel booking cancellations can have a significant impact on revenue and operations. Accurately predicting these cancellations can aid in better resource management, financial planning, and guest relations. Here are the specific reasons why predicting hotel booking cancellation is important.

**1. Revenue Optimization:**
Predicting cancellations allows hotels to better manage room inventory, potentially overbooking rooms to ensure maximum occupancy and implementing dynamic pricing.

**2. Operational Efficiency:**
Accurate cancellation predictions aid in resource allocation, such as staffing and procurement, ensuring that costs are minimized and resources aren't wasted on bookings that won't materialize.

**3. Guest Experience:**
By managing overbookings effectively through accurate predictions, hotels can minimize guest inconvenience, enhancing the overall guest experience.

**4. Strategic Marketing:**
Insights from cancellation trends can guide targeted marketing campaigns or loyalty programs to reduce future cancellations.

**5. Financial Forecasting:**
Understanding expected cancellations helps in more accurate financial planning and budgeting.

- **Goal**:

The primary objective of this project is to comprehend the booking behaviors of foreign guests at the City Hotel, which is considered the cash cow. Our aim is to implement a revenue optimization strategy by minimizing their cancellations. Thus, we seek to address the fundamental business question:

"What prompts foreign guests at the City Hotel to cancel their bookings?"

To tackle this, we endeavor to predict booking cancellations of foreign guests using machine learning algorithms. The classification models employed encompass Logistic Regression, Decision Trees, Random Forest, and XGBoost. Our aim is to contrast their performances and ascertain the most effective model, which will, in turn, guide future strategies for managing the hotel business.

## 2. Data
- **Source**: Hotel Booking Dataset on Kaggle
- **Description**:The dataset encompasses a range of hotel-related information, spanning booking status, guest details, and financial specifics. While the dataset includes both City and Resort hotels, to address our specific business question, we trained the data focusing on city hotel and foreign guests.
- **Cleaning and Preprocessing**:
    - **Handling Missing Values**: Addressed missing data using techniques like imputation or deletion.
    - **Outliers**: Detected and treated outliers to prevent skewed results.
    - **Feature Engineering**: Created new features to enhance the model's predictive power.
    - **Encoding**: Transformed categorical variables into a format suitable for machine learning using methods like one-hot or label encoding.
    - **Feature Selection**: Retained only the most influential features, optimizing both model performance and computational efficiency.


## 3. Methodology
- **EDA (Exploratory Data Analysis)**: We utilized Pandas and numpy for data manipulation, and crafted visualizations using Seaborn, Matplotlib, and Tableau Dashboards

[View Tableau Dashboard Here](https://public.tableau.com/app/profile/dooinn/viz/HotelBookingFinal/MarketSegmentation-Country)
![Dashboard - Main Dashboard](/img_assets/dashboard1.png)
![Dashboard - Market Segmentation](/img_assets/dashboard2.png)

- **Modelling**: For data modeling, we employed classification models, including Logistic Regression, Decision Trees, Random Forest, and Gradient Boosting (XGBoost). Each model was fine-tuned using hyperparameter optimization.

- **Evaluation**: To determine the most effective model for predicting cancellations, we assessed various metrics such as accuracy, precision, recall, F1-Score, and Area Under the Curve (AUC). Additionally, we examined potential overfitting and analyzed the confusion matrix.




## 4. Results

- **Findings**:
    - The cancellation rate for foreign guests shows exponential growth in Year 2 (30.50%) compared to Year 1 (18.77%).
    - For guest group types, couples and family groups reveal a notable increase in the cancellation rate in Year 2.
    - Regarding market segmentation, Online TA (Travel Agency) shows the highest increase in cancellation rate in Year 2.

The following slide deck provides more detailed information about the research.

[Business Case Study: Revenue Optimization Strategy for City Hotel](https://github.com/dooinn/hotel_cancellation_prediction/blob/main/City%20Hotel%20Revenue%20Opitmization%20Staregy%202017-2018.pdf)


- **Data Modelling Results**:
The following image is the XGBoost Classification Report and Feature Importances
![XGBoost Classification Report](/img_assets/class_report_feature_import.png)

    - After comparing the metrics of various algorithms (Logistic Regression, Decision Tree, Random Forest, XGBoost) in the context of hotel booking cancellations, the XGBoost model emerges as the best choice. It boasts the highest accuracy, F1-score for class 1 (cancellations), and AUC. Furthermore, its consistent performance on the test set indicates excellent generalization to new data.
    - In terms of the feature importance from XGBoost:
    1. Market segments hold significant influence in predicting cancellations, with online and offline travel agents, along with direct bookings, being the top contributors.
    2. Guest preferences and requirements, such as special requests and parking space needs, also considerably affect the predictions.
    3. Certain features, including specific meal and room types, demonstrate minimal influence on the prediction, suggesting they may be inconsequential for this specific prediction task.



## 5. Conclusion

Market segmentation is the primary feature we need to closely monitor when predicting cancellations. However, we still lack information that determines precisely why foreign guests cancel their bookings. We need to investigate in-depth the specific factors motivating cancellations via Online Travel Agencies like Booking.com. Additionally, we should explore each OTA's website, check our hotel's page, and analyze the features and reviews there to gain a better understanding of potential guest booking behaviors.



