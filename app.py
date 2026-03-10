import streamlit as st
import pandas as pd
import pickle

# Load trained model
model = pickle.load(open("churn_model.pkl", "rb"))

st.title("Customer Churn Prediction")
st.write("Predict whether a telecom customer is likely to churn.")

st.sidebar.header("Enter Customer Information")

# ---------- USER INPUTS ----------

gender = st.sidebar.selectbox("Gender", ["Female", "Male"])
senior = st.sidebar.selectbox("Senior Citizen", [0, 1])
partner = st.sidebar.selectbox("Partner", ["Yes", "No"])
dependents = st.sidebar.selectbox("Dependents", ["Yes", "No"])
tenure = st.sidebar.slider("Tenure (months)", 0, 72, 12)

phone_service = st.sidebar.selectbox("Phone Service", ["Yes", "No"])
multiple_lines = st.sidebar.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])

internet_service = st.sidebar.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

online_security = st.sidebar.selectbox("Online Security", ["Yes", "No", "No internet service"])
online_backup = st.sidebar.selectbox("Online Backup", ["Yes", "No", "No internet service"])
device_protection = st.sidebar.selectbox("Device Protection", ["Yes", "No", "No internet service"])
tech_support = st.sidebar.selectbox("Tech Support", ["Yes", "No", "No internet service"])

streaming_tv = st.sidebar.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
streaming_movies = st.sidebar.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

contract = st.sidebar.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
paperless = st.sidebar.selectbox("Paperless Billing", ["Yes", "No"])

payment_method = st.sidebar.selectbox(
    "Payment Method",
    ["Electronic check","Mailed check","Bank transfer (automatic)","Credit card (automatic)"]
)

monthly_charges = st.sidebar.slider("Monthly Charges", 0, 150, 70)

# ---------- ENCODING ----------

yes_no_map = {"Yes":1,"No":0}

gender_map = {"Female":0,"Male":1}

multiple_lines_map = {"No":0,"Yes":1,"No phone service":2}

internet_map = {"DSL":0,"Fiber optic":1,"No":2}

security_map = {"No":0,"Yes":1,"No internet service":2}

contract_map = {"Month-to-month":0,"One year":1,"Two year":2}

payment_map = {
    "Electronic check":0,
    "Mailed check":1,
    "Bank transfer (automatic)":2,
    "Credit card (automatic)":3
}

# ---------- FEATURE ENGINEERING ----------

total_charges = tenure * monthly_charges
total_spend = tenure * monthly_charges

# ---------- CREATE DATAFRAME ----------

input_data = pd.DataFrame({
'gender':[gender_map[gender]],
'SeniorCitizen':[senior],
'Partner':[yes_no_map[partner]],
'Dependents':[yes_no_map[dependents]],
'tenure':[tenure],
'PhoneService':[yes_no_map[phone_service]],
'MultipleLines':[multiple_lines_map[multiple_lines]],
'InternetService':[internet_map[internet_service]],
'OnlineSecurity':[security_map[online_security]],
'OnlineBackup':[security_map[online_backup]],
'DeviceProtection':[security_map[device_protection]],
'TechSupport':[security_map[tech_support]],
'StreamingTV':[security_map[streaming_tv]],
'StreamingMovies':[security_map[streaming_movies]],
'Contract':[contract_map[contract]],
'PaperlessBilling':[yes_no_map[paperless]],
'PaymentMethod':[payment_map[payment_method]],
'MonthlyCharges':[monthly_charges],
'TotalCharges':[total_charges],
'TotalSpend':[total_spend]
})

# ---------- PREDICTION ----------

if st.button("Predict Churn"):

    model_features = model.get_booster().feature_names
    input_data = input_data[model_features]

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0][1]

    st.subheader("Prediction Result")

    if prediction[0] == 1:
        st.error("⚠ Customer is likely to churn")
    else:
        st.success("✅ Customer is likely to stay")

    st.write(f"Churn Probability: {probability:.2f}")
