import logging
import sys
from types import FrameType
from typing import List, cast

from loguru import logger
from pydantic import AnyHttpUrl, BaseSettings

# Nivel del logger
class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO  # Los niveles de logging se definen como enteros

# Configuración general de la API
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"  # Prefijo de las rutas de la API

    # Meta
    logging: LoggingSettings = LoggingSettings()

    # BACKEND_CORS_ORIGINS permite definir orígenes permitidos para solicitudes CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # Para desarrollo local
        "http://localhost:8000",
        "https://localhost:3000",
        "https://localhost:8000",
    ]

    # Nombre del proyecto (actualizado para el ICFES)
    PROJECT_NAME: str = "ICFES API"

    class Config:
        case_sensitive = True  # Hacer las configuraciones sensibles a mayúsculas/minúsculas

# Intercepción de mensajes de loggers
# Permite integrar loguru con logging estándar de Python
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Obtener el nivel correspondiente de Loguru si existe
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Encontrar la función desde donde se originó el mensaje de log
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )

# Configuración de loggers usando uvicorn
def setup_app_logging(config: Settings) -> None:
    """Configura el logging personalizado para la aplicación."""
    LOGGERS = ("uvicorn.asgi", "uvicorn.access")
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=config.logging.LOGGING_LEVEL)]

    logger.configure(
        handlers=[{"sink": sys.stderr, "level": config.logging.LOGGING_LEVEL}]
    )


# Instancia de configuración
settings = Settings()
