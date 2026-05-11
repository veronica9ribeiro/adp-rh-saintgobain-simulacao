import time
import requests
from src.config import CONF

_token_cache = {
    "access_token": None,
    "expires_at": 0,
}


def _fetch_token() -> dict:
    response = requests.post(
        CONF.TOKEN_URL,
        data={
            "grant_type"   : "client_credentials",
            "client_id"    : CONF.CLIENT_ID,
            "client_secret": CONF.CLIENT_SECRET,
        },
    )
    response.raise_for_status()
    return response.json()


def _token_valido() -> bool:
    return (
        _token_cache["access_token"] is not None
        and time.time() < _token_cache["expires_at"] - 60
    )


def get_token() -> str:
    if not _token_valido():
        dados = _fetch_token()
        _token_cache["access_token"] = dados["access_token"]
        _token_cache["expires_at"]   = time.time() + dados["expires_in"]
    return _token_cache["access_token"]


def get_headers() -> dict:
    return {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type" : "application/json",
    }