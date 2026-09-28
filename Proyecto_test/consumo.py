import requests


url = "http://127.0.0.1:8000"

status_response = requests.get(f"{url}/", timeout=10)
status_response.raise_for_status()
print("API status:", status_response.json())

loan_application = {
    "Gender": "Male",
    "Married": "Yes",
    "Dependents": "1",
    "Education": "Graduate",
    "Self_Employed": "No",
    "ApplicantIncome": 4583,
    "CoapplicantIncome": 1508,
    "LoanAmount": 128,
    "Loan_Amount_Term": 360,
    "Credit_History": 1,
    "Property_Area": "Rural",
}

prediction_response = requests.post(
    f"{url}/predict",
    json=loan_application,
    timeout=10,
)
prediction_response.raise_for_status()
print("Loan prediction:", prediction_response.json())