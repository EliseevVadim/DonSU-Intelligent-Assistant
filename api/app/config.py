import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    VECTOR_DB_NAME: str
    ASSISTANT_DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    EMBEDDINGS_MODEL_NAME: str
    GENERATOR_MODEL_NAME: str
    COLLECTION_NAME: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        extra='allow'
    )


settings = Settings()


def get_knowledge_base_connection_string():
    return (f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}"
            f":{settings.DB_PORT}/{settings.VECTOR_DB_NAME}")


def get_assistant_db_connection_string():
    return (f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}"
            f":{settings.DB_PORT}/{settings.ASSISTANT_DB_NAME}")


def get_auth_encoding():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


def get_embeddings_model_name():
    return settings.EMBEDDINGS_MODEL_NAME


def get_generator_model_name():
    return settings.GENERATOR_MODEL_NAME


def get_collection_name():
    return settings.COLLECTION_NAME


def get_google_client_id():
    return settings.GOOGLE_CLIENT_ID


def get_google_client_secret():
    return settings.GOOGLE_CLIENT_SECRET
