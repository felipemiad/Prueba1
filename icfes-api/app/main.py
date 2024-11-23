from typing import Any

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from loguru import logger

from app.api import api_router
from app.config import settings, setup_app_logging

# Configurar logging lo antes posible
setup_app_logging(config=settings)

# Inicializar la aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,  # Nombre del proyecto
    openapi_url=f"{settings.API_V1_STR}/openapi.json"  # URL para la documentación OpenAPI
)

# Definir un router para la ruta raíz
root_router = APIRouter()

@root_router.get("/")
def index(request: Request) -> Any:
    """
    Respuesta básica en HTML para la raíz de la API.
    """
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Bienvenido a la API del ICFES</h1>"
        "<div>"
        "Documentación disponible: <a href='/docs'>aquí</a>"
        "</div>"
        "</body>"
        "</html>"
    )
    return HTMLResponse(content=body)

# Incluir el router de las rutas principales (API)
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

# Configurar CORS (Cross-Origin Resource Sharing)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    # Solo para depuración en desarrollo
    logger.warning("Ejecutando en modo desarrollo. No usar esta configuración en producción.")
    import uvicorn

    # Ejecutar el servidor con Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
