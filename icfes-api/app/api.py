import json
from typing import Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger
from app.schemas import HealthResponse, PredictionResults, MultipleDataInputs

api_router = APIRouter()

# Ruta para verificar que la API se esté ejecutando correctamente
@api_router.get("/health", response_model=HealthResponse, status_code=200)
def health() -> dict:
    """
    Verifica que la API y el modelo están funcionando correctamente.
    """
    health = HealthResponse(
        status="ok",  # Estado de la API
        uptime=0.0    # Placeholder; puedes calcular el tiempo de uptime si lo necesitas
    )

    return health.dict()


# Ruta para realizar las predicciones
@api_router.post("/predict", response_model=PredictionResults, status_code=200)
async def predict(input_data: MultipleDataInputs) -> Any:
    """
    Predicción usando el modelo de ICFES.
    """

    # Convertir los datos de entrada a un DataFrame
    input_df = pd.DataFrame(jsonable_encoder(input_data.inputs))

    logger.info(f"Realizando predicción con entradas: {input_data.inputs}")

    try:
        # Cargar el modelo y realizar predicción
        from model_abandono.predictor import ModelPredictor  # Importa el predictor del modelo
        predictor = ModelPredictor()
        predictions = predictor.predict(input_df.values.tolist())  # Predice con los datos

        # Construir la respuesta
        results = {
            "errors": None,
            "version": "1.0.0",
            "predictions": predictions,
        }

        logger.info(f"Resultados de predicción: {results.get('predictions')}")
        return results

    except Exception as e:
        logger.error(f"Error durante la predicción: {e}")
        raise HTTPException(status_code=400, detail="Error al realizar la predicción")
