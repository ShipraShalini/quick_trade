import os


class Settings:
    PROJECT_NAME: str = "QuikTrade"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")
    HOST: str = os.getenv("HOST", "localhost")
    PORT: str = os.getenv("PORT", "8000")
    VERSION: str = os.getenv("VERSION", "0.0")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tradedb")


settings = Settings()


DB_CONFIG: dict = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": settings.POSTGRES_HOST,
                "port": settings.POSTGRES_PORT,
                "user": settings.POSTGRES_USER,
                "password": settings.POSTGRES_PASSWORD,
                "database": settings.POSTGRES_DB,
                "max_inactive_connection_lifetime": 120,
            },
        },

    },
    "apps": {
        "models": {
            "models": [
                # "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}
