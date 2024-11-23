from fastapi import APIRouter
from app.schemas import PredictionResults, MultipleDataInputs

api_router = APIRouter()

# Ruta de salud
@api_router.get("/health", response_model=PredictionResults, status_code=200)
def health():
    return {"status": "ok"}

# Ruta de predicción temporal (sin modelo)
@api_router.post("/predict", response_model=PredictionResults, status_code=200)
async def predict(input_data: MultipleDataInputs):
    """
    Ruta temporal para verificar que la API funciona sin el modelo.
    """
    # Simulación de respuesta
    return {
        "errors": None,
        "version": "1.0.0",
        "predictions": [0.0 for _ in input_data.inputs]  # Devuelve una lista de ceros
    }
