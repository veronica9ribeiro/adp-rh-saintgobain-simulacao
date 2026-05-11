import os
from dotenv import load_dotenv

load_dotenv()


def _require(var: str) -> str:
    value = os.getenv(var)
    if not value:
        raise EnvironmentError(
            f"Variável '{var}' não encontrada. Verifique seu .env."
        )
    return value


class Config:
    CLIENT_ID     = _require("ADP_CLIENT_ID")
    CLIENT_SECRET = _require("ADP_CLIENT_SECRET")
    TOKEN_URL     = _require("ADP_TOKEN_URL")
    BASE_URL      = _require("ADP_BASE_URL")


CONF = Config()