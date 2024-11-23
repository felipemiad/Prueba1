from typing import Any, List, Optional
from pydantic import BaseModel

# Esquema para los resultados de predicción
class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[float]]  # Lista de predicciones numéricas (PUNT_GLOBAL)

# Esquema para los inputs múltiples
class MultipleDataInputs(BaseModel):
    inputs: List[dict]  # Lista de diccionarios con los datos de entrada

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "FAMI_ESTRATOVIVIENDA": 3,
                        "FAMI_PERSONASHOGAR": 4,
                        "FAMI_TIENEINTERNET": 1,
                        "ESTU_HORASSEMANATRABAJA": 10,
                        "FAMI_COMECARNEPESCADOHUEVO": 2,
                        "COLE_NATURALEZA": "Privado",
                        "ESTU_DEPTO_RESIDE": "Bogotá",
                        "COLE_JORNADA": "Mañana",
                        "COLE_GENERO": "Mixto",
                    }
                ]
            }
        }
