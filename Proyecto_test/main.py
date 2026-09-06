from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

bundle_name = Path(__file__).with_name("loan_approval_model.pkl")
estado_servicio = {"bundle": None}


@asynccontextmanager
async def lifespan(app: FastAPI):
    estado_servicio["bundle"] = joblib.load(bundle_name)
    print(f"Modelo cargado correctamente desde {bundle_name}")
    yield
    estado_servicio["bundle"] = None


app = FastAPI(
    title="Loan Approval Prediction API",
    description="API para predecir la aprobación de solicitudes de préstamo.",
    version="1.0.0",
    lifespan=lifespan,
)


class LoanApplication(BaseModel):
    Gender: str = Field(..., description="Male or Female")
    Married: str = Field(..., description="Yes or No")
    Dependents: str = Field(..., description="0, 1, 2 or 3+")
    Education: str = Field(..., description="Graduate or Not Graduate")
    Self_Employed: str = Field(..., description="Yes or No")
    ApplicantIncome: float = Field(..., ge=0)
    CoapplicantIncome: float = Field(..., ge=0)
    LoanAmount: float = Field(..., ge=0)
    Loan_Amount_Term: float = Field(..., gt=0)
    Credit_History: float = Field(..., ge=0, le=1) # ge = greater than or equal to number defined, le = less than or equal to number defined
    Property_Area: str = Field(..., description="Urban, Semiurban or Rural")


class LoanPrediction(BaseModel):
    loan_status_prediction: int
    approval_probability: float
    decision: str


@app.get("/")
def status():
    return {
        "status": "Loan Approval API is running",
        "model_bundle": estado_servicio["bundle"] is not None,
    }


@app.post("/predict", response_model = LoanPrediction)
def predict(application: LoanApplication):
    bundle = estado_servicio["bundle"]
    if bundle is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")

    input_data = pd.DataFrame([application.model_dump()])[bundle["columns"]]
    pipeline = bundle["pipeline"]
    prediction = int(pipeline.predict(input_data)[0])
    probability = float(pipeline.predict_proba(input_data)[0][1])

    return LoanPrediction(
        loan_status_prediction= prediction,
        approval_probability= round(probability, 4),
        decision="Approved" if prediction == 1 else "Rejected",
    )