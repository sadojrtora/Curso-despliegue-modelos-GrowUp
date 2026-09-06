from contextlib import asynccontextmanager
# from typing import Literal 

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from Proyecto2.inferencia import pronosticar
from Proyecto2.schema import solicitudPronostico

bundle_name = "Proyecto2/modelo_demanda.joblib"

estado_servicio = {"bundle": None}

@asynccontextmanager
async def lifespan(app:FastAPI):
    estado_servicio["bundle"] = joblib.load(bundle_name)
    print("Bundle cargado correctamente ")
    yield
    estado_servicio["bundle"] = None

app = FastAPI(
    title = "API for Forecasting Demand",
    description = "This API allows you to predict the likelihood of future demand based on historical sales data.",
    version = "1.0.0",
    lifespan = lifespan
)

@app.get("/")
def status():
    return {
        "status": "Demand Forecasting API is running",
        "model_bundle": estado_servicio["bundle"] is not None,
    }

@app.post("/predict")
def predict(historial: solicitudPronostico):
    bundle = estado_servicio["bundle"]
    if bundle is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")

    store = historial.store
    item = historial.item
    horizonte = historial.horizonte
    registros = historial.historial

    historial = pd.DataFrame(
           { 
               "date" : pd.to_datetime([r.fecha for r in registros]),
               "store" : store,
               "item" : item,
               "sales" : [r.unidades for r in registros]
            }
        )
    bundle = estado_servicio["bundle"]
    pronostics = pronosticar(bundle, historial, horizonte)
    return {
        "store": store,
        "item": item,
        #"horizonte": horizonte,
        "pronosticos": pronostics
    }

