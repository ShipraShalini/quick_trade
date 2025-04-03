import os

ENV_LOCAL = "local"
ENV_PROD = "production"


class Settings:
    PROJECT_NAME: str = "QuikTrade"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", ENV_LOCAL)
    HOST: str = os.getenv("HOST", "localhost")
    PORT: str = os.getenv("PORT", "8000")
    VERSION: str = os.getenv("VERSION", "0.0")
    POSTGRES_PORT: str = os.getenv("DB_PORT", "5432")
    POSTGRES_HOST: str = os.getenv("DB_PASSWORD", "localhost")
    POSTGRES_USER: str = os.getenv("DB_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("DB_NAME", "tradedb")


settings = Settings()


DB_CONFIG: dict = {
    # We can have multiple connections and specify them for read or write.
    # Tortoise uses connection pool by default but we can update it if needed.
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
                "app.models.order",
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}
