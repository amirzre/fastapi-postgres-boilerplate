import uvicorn

from core.config import EnvironmentType, config

if __name__ == "__main__":
    uvicorn.run(
        app="core.server:app",
        reload=True if config.ENVIRONMENT != EnvironmentType.PRODUCTION else False,
        workers=config.WORKERS,
    )
