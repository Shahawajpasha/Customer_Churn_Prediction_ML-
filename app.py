import streamlit as st
import pandas as pd
import pickle

model = pickle.load(open("churn_model.pkl", "rb"))

st.title("Customer Churn Prediction")
st.write("Predict whether a customer is likely to churn.")

st.sidebar.header("Enter Customer Information")

tenure = st.sidebar.slider("Tenure (months)", 0, 72, 12)
monthly_charges = st.sidebar.slider("Monthly Charges", 0, 150, 70)

contract = st.sidebar.selectbox(
    "Contract Type",
    ["Month-to-month", "One year", "Two year"]
)

internet_service = st.sidebar.selectbox(
    "Internet Service",
    ["DSL", "Fiber optic", "No"]
)

online_security = st.sidebar.selectbox(
    "Online Security",
    ["Yes", "No"]
)

tech_support = st.sidebar.selectbox(
    "Tech Support",
    ["Yes", "No"]
)

input_data = pd.DataFrame({
    "tenure": [tenure],
    "MonthlyCharges": [monthly_charges]
})

if st.button("Predict Churn"):

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0][1]

    st.subheader("Prediction Result")

    if prediction[0] == 1:
        st.error("⚠ Customer is likely to churn")
    else:
        st.success("✅ Customer is likely to stay")

    st.write(f"Churn Probability: {probability:.2f}")
