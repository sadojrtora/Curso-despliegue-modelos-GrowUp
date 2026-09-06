## Funcion para pronosticar ventas futuras
import pandas as pd
import numpy as np

# Se pueden traer todas las funciones de features.py, pero solo se necesita crear_features para pronosticar
from Proyecto2.features import crear_features 

def pronosticar(bundle, historial, horizonte=14):
    """
    bundle    : dict con modelo, columnas y configuracion
    historial : DataFrame con columnas date, store, item, sales (al menos 28 filas, sin huecos)
    horizonte : cantidad de dias a pronosticar
    devuelve  : lista de dicts {fecha, prediccion}
    """
    # Extraer del bundle el modelo, el orden de variables y el historial minimo.
    modelo, columnas = bundle["modelo"], bundle["columnas"]
    minimo = bundle["min_historial"]

    # Ordenar y normalizar las fechas del historial recibido.
    h = historial.copy()
    h["date"] = pd.to_datetime(h["date"])
    h = h.sort_values("date").reset_index(drop=True)

    # Verificar que existen suficientes observaciones y que no faltan dias.
    if len(h) < minimo:
        raise ValueError(f"Se requieren al menos {minimo} dias de historia, se recibieron {len(h)}")
    if h.date.diff().dropna().ne(pd.Timedelta(days=1)).any():
        raise ValueError("El historial tiene fechas faltantes o desordenadas")

    # Identificar la serie que se continuara pronosticando.
    store, item = int(h.store.iloc[-1]), int(h.item.iloc[-1])
    resultado = []

    # Repetir la prediccion para cada dia del horizonte solicitado.
    for _ in range(horizonte):
        siguiente = h.date.iloc[-1] + pd.Timedelta(days=1)
        h = pd.concat(
            [h, pd.DataFrame([{"date": siguiente, "store": store, "item": item, "sales": np.nan}])],
            ignore_index=True,
        )

        # Crear las variables del nuevo dia usando el mismo proceso del entrenamiento.
        fila = crear_features(h).iloc[[-1]]
        pred = max(0.0, float(modelo.predict(fila[columnas])[0]))

        # Usar la prediccion como historia para poder calcular el siguiente dia.
        h.loc[h.index[-1], "sales"] = pred
        resultado.append({"fecha": siguiente.date().isoformat(), "prediccion": round(pred, 2)})

    return resultado