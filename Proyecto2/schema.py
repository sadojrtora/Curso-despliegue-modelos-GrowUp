from pydantic import BaseModel, Field
from datetime import date

class registroHistorico(BaseModel):
    fecha: date
    unidades: int = Field(ge = 0, description="Number of units sold on the given date (No puede ser negativo)")

class solicitudPronostico(BaseModel):
    store: int = Field(ge = 1, le = 10, description="ID of the store from 1 to 10")
    item: int = Field(ge = 1, le = 50, description="ID of the item from 1 to 50")
    historial: list[registroHistorico] = Field(min_length=28, max_length=365, description="Historical sales data for the item in the store (between 28 and 365 days)")
    horizonte : int = Field(default=14, ge=1, le=28, description="Number of days to forecast (between 1 and 28 days)")
                                        
