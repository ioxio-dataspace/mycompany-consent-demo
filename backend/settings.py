import os
from typing import List, Literal

from pydantic import AnyHttpUrl, BaseModel, BaseSettings, SecretStr


class FrontendSettings(BaseModel):
    path_prefix: str
    auth_error_page: str = "/auth-error"


def _is_local_env(env: str) -> bool:
    return env in {"development", "unittest"}


class Settings(BaseSettings):
    PROJECT_NAME: str = "MyCompany consent demo"
    GOOGLE_PROJECT_NAME: str = "dli-demos"
    DB_COLLECTION_PREFIX: str = "mycompany"
    ENV: str = "development"
    BASE_URL: AnyHttpUrl = "http://localhost:3000"
    NEXUS_BASE_DOMAIN: str = "sandbox.digitalliving.fi"

    CONSENT_PROVIDER_URL = "https://consent.sandbox.digitalliving.fi"

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "DEBUG"

    COOKIE_SECURE: bool = not _is_local_env(os.environ.get("ENV", ENV))

    LE_API_URL: AnyHttpUrl = "http://192.168.99.100:31000"
    LE_APP_TOKEN: str = "ey..."
    PRODUCT_GATEWAY_URL: AnyHttpUrl = "https://gateway.sandbox.digitalliving.fi"

    OPENID_CONNECT_ISSUER: AnyHttpUrl = "https://login.sandbox.digitalliving.fi"
    OPENID_CONNECT_CLIENT_ID: str
    OPENID_CONNECT_CLIENT_SECRET: SecretStr
    OPENID_CONNECT_ACR_VALUES: str = "fake-auth"
    OPENID_CONNECT_SCOPES: str = "openid"
    OPENID_CONNECT_INCLUDE_ID_TOKEN_HINT_IN_LOGOUT: bool = True

    AUTH_VALID_RETURN_PATH_PREFIXES: set = {
        "/my-company",
        "/accountant",
    }

    FRONTEND_APPS: List[FrontendSettings] = [
        FrontendSettings(path_prefix="/my-company"),
        FrontendSettings(path_prefix="/accountant"),
    ]

    def is_local_env(self):
        return _is_local_env(self.ENV)

    class Config:
        env_file = ".env"


conf = Settings()
