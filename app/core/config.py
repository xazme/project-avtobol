import os
import dotenv
from pydantic import BaseModel

dotenv.load_dotenv()


class DataFromEnv:
    """Loaded data from .env"""

    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT"))
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_URL: str = os.getenv("DB_URL")

    APP_HOST: str = os.getenv("APP_HOST")
    APP_PORT: int = int(os.getenv("APP_PORT"))

    MINIO_HOST: str = os.getenv("MINIO_HOST")
    MINIO_API_PORT: str = os.getenv("MINIO_API_PORT")
    MINIO_ACCESS_PATH: str = os.getenv("MINIO_ACCESS_KEY_PATH")
    MINIO_SECRET_PATH: str = os.getenv("MINIO_SECRET_KEY_PATH")

    ACCESS_PRIVATE_KEY_PATH: str = os.getenv("ACCESS_PRIVATE_KEY_PATH")
    ACCESS_PUBLIC_KEY_PATH: str = os.getenv("ACCESS_PUBLIC_KEY_PATH")

    REFRESH_PRIVATE_KEY_PATH: str = os.getenv("REFRESH_PRIVATE_KEY_PATH")
    REFRESH_PUBLIC_KEY_PATH: str = os.getenv("REFRESH_PUBLIC_KEY_PATH")
    ALGORITHM: str = os.getenv("ALGORITHM")


class DataBaseConnection:
    """DataBase data"""

    host: str = DataFromEnv.DB_HOST
    port: int = DataFromEnv.DB_PORT
    user: str = DataFromEnv.DB_USER
    password: str = DataFromEnv.DB_PASS
    name: str = DataFromEnv.DB_NAME

    db_url = DataFromEnv.DB_URL

    naming_convention: dict[str, str] = {
        "ix": "ix_%(table_name)s_%(column_0_name)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @classmethod
    def get_db_url(cls):
        return f"postgresql+asyncpg://{cls.user}:{cls.password}@{cls.host}:{cls.port}/{cls.name}"
        # return cls.db_url


class MinIO(BaseModel):

    @property
    def minio_access(self):
        with open(DataFromEnv.MINIO_ACCESS_PATH, "r") as file:
            access_key = file.read()
        return access_key

    @property
    def minio_secret(self):
        with open(DataFromEnv.MINIO_SECRET_PATH, "r") as file:
            secret_key = file.read()
        return secret_key

    @property
    def minio_url(self):
        return f"{DataFromEnv.MINIO_HOST}:{DataFromEnv.MINIO_API_PORT}"


class RunConfig(BaseModel):
    """Application data"""

    host: str = DataFromEnv.APP_HOST
    port: int = DataFromEnv.APP_PORT


class Auth(BaseModel):

    access_token_url: str = "/auth/sign-in"
    algorithm: str = DataFromEnv.ALGORITHM
    expire_minutes: int = 720
    expire_days: int = 7
    refresh_token_key: str = "refresh_token"

    @property
    def access_private_key(self):
        with open(DataFromEnv.ACCESS_PRIVATE_KEY_PATH, "r") as file:
            private_key = file.read()
        return private_key

    @property
    def access_public_key(self):
        with open(DataFromEnv.ACCESS_PUBLIC_KEY_PATH, "r") as file:
            public_key = file.read()
        return public_key

    @property
    def refresh_private_key(self):
        with open(DataFromEnv.REFRESH_PRIVATE_KEY_PATH, "r") as file:
            private_key = file.read()
        return private_key

    @property
    def refresh_public_key(self):
        with open(DataFromEnv.REFRESH_PUBLIC_KEY_PATH, "r") as file:
            public_key = file.read()
        return public_key


class ApiPrefix(BaseModel):
    """API prefixes"""

    main_prefix: str = "/api"
    user_prefix: str = "/user"
    car_brand_prefix: str = "/carbrand"
    car_series_prefix: str = "/carseries"
    product: str = "/product"
    car_part_prefix: str = "/carpart"
    token_prefix: str = "/token"
    disc_brand_prefix: str = "/discbrand"
    tire_brand_prefix: str = "/tirebrand"
    storage_prefix: str = "/storage"
    cart_prefix: str = "/cart"
    order_prefix: str = "/order"
    auth_prefix: str = "/auth"
    # etc


class Settings:
    """Main settings class"""

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    auth: Auth = Auth()
    db: DataBaseConnection = DataBaseConnection()
    minio: MinIO = MinIO()


settings = Settings()
