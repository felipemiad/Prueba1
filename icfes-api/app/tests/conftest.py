from typing import Generator

import pandas as pd
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Fixture: Cargar el archivo de prueba (dataset de ejemplo)
@pytest.fixture(scope="module")
def test_data() -> pd.DataFrame:
    # Cambia "df_definitivo.csv" por el archivo de prueba que usarás
    return pd.read_csv("data/df_definitivo.csv")

# Fixture: Cliente de prueba para la API
@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as _client:
        yield _client
        app.dependency_overrides = {}

