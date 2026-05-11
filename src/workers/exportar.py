from pathlib import Path
from datetime import date
import pandas as pd

PASTA_SAIDA = Path(__file__).parent.parent.parent / "data" / "output"


def para_excel(df: pd.DataFrame, nome_base: str) -> Path:
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

    arquivo = PASTA_SAIDA / f"{nome_base}_{date.today().isoformat()}.xlsx"
    df.to_excel(arquivo, index=False, engine="openpyxl")
    print(f"  Exportado: {arquivo}")
    return arquivo