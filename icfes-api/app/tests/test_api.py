import math
import numpy as np
import pandas as pd
from fastapi.testclient import TestClient

def test_make_prediction(client: TestClient, test_data: pd.DataFrame) -> None:
    # Given
    payload = {
        "inputs": test_data.replace({np.nan: None}).to_dict(orient="records")
    }

    # When
    response = client.post(
        "http://localhost:8001/predict",
        json=payload,
    )

    # Then
    assert response.status_code == 200
    prediction_data = response.json()
    assert "predictions" in prediction_data
    assert prediction_data["errors"] is None
    assert len(prediction_data["predictions"]) > 0
    assert math.isclose(prediction_data["predictions"][0], 113422, rel_tol=100)
