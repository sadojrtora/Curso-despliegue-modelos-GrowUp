from contextlib import asynccontextmanager
from typing import Literal 

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

bundle_name = "model_e_cardiaca_v1.pkl"

estado_servicio = {"bundle": None}

@asynccontextmanager
async def lifespan(app:FastAPI):
    estado_servicio["bundle"] = joblib.load(bundle_name)
    print("Bundle cargado correctamente ")
    yield
    estado_servicio["bundle"] = None

app = FastAPI(
    title = "API for Predicting Heart Disease",
    description = "This API allows you to predict the likelihood of coronary heart disease (chd) based on various health parameters.",
    version = "1.0.0",
    lifespan = lifespan
)

'''
Context data:
sbp: presión arterial sistólica, entero.
Tabaco: consumo acumulado de tabaco, decimal.
ldl: colesterol LDL, decimal.
Adiposidad: nivel de adiposidad, decimal.
Familia: antecedentes familiares; solo acepta "Presente" o "Ausente".
Tipo: comportamiento tipo A, entero.
Obesidad: nivel de obesidad, decimal.
Alcohol: consumo actual de alcohol, decimal.
Edad: edad del paciente, entero.",
'''

class PacienteInput(BaseModel):

    sbp: int = Field(...,description="Presión arterial sistólica"),
    Tabaco: float = Field(...,description="Tabaco acumulado (kg)")

    ldl: float = Field(...,description="Colesterol LDL")

    Adiposidad: float = Field(...,description="Adiposidad")

    Familia: Literal['Presente',

                     'Ausente'] = Field(

                         ...,description="Antecendentes familiares de enfermedad cardíaca")

    Tipo: int = Field(...,description="Comportamiento tipo-A")

    Obesidad: float = Field(...,description="Obesidad")

    Alcohol:float = Field(...,description="Consumo actual de alcohol")

    Edad:int = Field(...,description="Edad")

class PacienteOutput(BaseModel):

    chd_prediction: int
    probability: float
    risk: str

@app.get("/")
def status():
    return {
        "status": "Coronary Disease API 'is running",
        "model_bundle": estado_servicio["bundle"] is not None      
    }

@app.post("/predict", response_model = PacienteOutput)
def predecir(paciente: PacienteInput):
# Validar el modelo
    bundle = estado_servicio["bundle"] 
    if bundle is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")

    row = paciente.model_dump()

    row["Familia"] = bundle["mapping_familia"][row["Familia"]]
    X_new = pd.DataFrame([row])[bundle["columns"]]
    prediction = bundle["pipeline"].predict(X_new)[0]
    probability = bundle["pipeline"].predict_proba(X_new)[0][1]

    # Return outputs
    return PacienteOutput(
        chd_prediction=int(prediction),
        probability= round(float(probability),4),
        risk="High" if probability > 0.7 else "Low"
    )