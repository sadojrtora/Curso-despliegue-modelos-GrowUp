from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException

from schema import LoanApplication, LoanPrediction


BUNDLE_PATH = Path(__file__).with_name("loan_approval_model.pkl")
service_state = {"bundle": None}


@asynccontextmanager
async def lifespan(app: FastAPI):
    service_state["bundle"] = joblib.load(BUNDLE_PATH)
    print(f"Loan approval model loaded from {BUNDLE_PATH.name}")
    yield
    service_state["bundle"] = None


app = FastAPI(
    title="Loan Approval Prediction API",
    description="Predicts the approval outcome of a loan application.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def status():
    bundle = service_state["bundle"]
    return {
        "status": "Loan approval prediction API is running",
        "model_loaded": bundle is not None,
        "model": bundle["metadata"].get("model") if bundle is not None else None,
    }


@app.post("/predict", response_model=LoanPrediction)
def predict(application: LoanApplication) -> LoanPrediction:
    bundle = service_state["bundle"]
    if bundle is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    row = application.model_dump()
    input_data = {
        column: row[column] if row[column] is not None else np.nan
        for column in bundle["columns"]
    }
    application_df = pd.DataFrame([input_data], columns=bundle["columns"])
    pipeline = bundle["pipeline"]

    prediction = int(pipeline.predict(application_df)[0])
    classes = list(pipeline.classes_)
    approval_index = classes.index(1)
    approval_probability = float(
        pipeline.predict_proba(application_df)[0, approval_index]
    )

    return LoanPrediction(
        loan_status="Y" if prediction == 1 else "N",
        approval_probability=round(approval_probability, 4),
    )