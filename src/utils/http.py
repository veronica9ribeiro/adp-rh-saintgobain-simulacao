import time
import requests
from src.auth.token import get_headers
from src.config import CONF

MAX_RETRIES    = 3
RETRY_WAIT_SEG = 2


def _url(path: str) -> str:
    return f"{CONF.BASE_URL}{path}"


def get(path: str, params: dict = None) -> dict:
    for tentativa in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(
                _url(path),
                headers=get_headers(),
                params=params,
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json()

        except requests.HTTPError as e:
            status = e.response.status_code if e.response else None
            if status == 401:
                raise
            if tentativa < MAX_RETRIES and status and status >= 500:
                print(f"  [aviso] Tentativa {tentativa} falhou ({status}). Aguardando {RETRY_WAIT_SEG}s...")
                time.sleep(RETRY_WAIT_SEG)
                continue
            raise


def post(path: str, payload: dict) -> dict:
    resp = requests.post(
        _url(path),
        headers=get_headers(),
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()