import streamlit as st
import numpy as np
import pickle

# Load trained model
with open("loan_model.pkl", "rb") as f:
    model = pickle.load(f)

# App title
st.title("💼 Loan Approval Prediction App")
st.markdown("Enter your information below to check if your loan will be approved.")

# User Inputs
gender = st.selectbox("Gender", ["Male", "Female"])
married = st.selectbox("Married", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
education = st.selectbox("Education", ["Graduate", "Not Graduate"])
self_employed = st.selectbox("Self Employed", ["Yes", "No"])
applicant_income = st.number_input("Applicant Income", min_value=0)
coapplicant_income = st.number_input("Coapplicant Income", min_value=0)
loan_amount = st.number_input("Loan Amount (in 1000)", min_value=0)
loan_term = st.number_input("Loan Term (in days)", min_value=0, value=360)
credit_history = st.selectbox("Credit History", ["Yes", "No"])
property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

# Encode inputs manually
gender = 1 if gender == "Male" else 0
married = 1 if married == "Yes" else 0
education = 1 if education == "Graduate" else 0
self_employed = 1 if self_employed == "Yes" else 0
credit_history = 1 if credit_history == "Yes" else 0
dependents = 3 if dependents == "3+" else int(dependents)

# One-hot encode property area
prop_urban = 1 if property_area == "Urban" else 0
prop_semiurban = 1 if property_area == "Semiurban" else 0
# If both are 0, it's Rural

# Feature order
input_features = np.array([
    gender, married, dependents, education, self_employed,
    applicant_income, coapplicant_income, loan_amount,
    loan_term, credit_history, prop_semiurban, prop_urban
]).reshape(1, -1)

# Predict on button click
if st.button("Predict Loan Approval"):
    result = model.predict(input_features)[0]
    if result == 1:
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Rejected")
