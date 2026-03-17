import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///spectertest.db"
    )


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///spectertest.db"
    )


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {
    "default": DevelopmentConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
