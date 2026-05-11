import pandas as pd
from src.utils.http import get

TAMANHO_PAGINA = 100


def buscar_todos() -> pd.DataFrame:
    todos = []
    skip  = 0

    while True:
        dados = get(
            "/hr/v2/workers",
            params={"$top": TAMANHO_PAGINA, "$skip": skip},
        )
        pagina = dados.get("workers", [])
        if not pagina:
            break

        todos.extend(pagina)
        skip += TAMANHO_PAGINA
        print(f"  Carregados: {len(todos)} funcionários...")

    return pd.json_normalize(todos)


def buscar_por_matricula(matricula: str) -> dict | None:
    import requests as _req
    try:
        dados   = get(f"/hr/v2/workers/{matricula}")
        workers = dados.get("workers", [])
        return workers[0] if workers else None
    except _req.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            return None
        raise


def buscar_por_departamento(departamento: str) -> pd.DataFrame:
    dados = get(
        "/hr/v2/workers",
        params={"$filter": f"department eq '{departamento}'"},
    )
    return pd.json_normalize(dados.get("workers", []))