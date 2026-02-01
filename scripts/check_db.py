# scripts/check_db.py
import os
import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://admin:admin@localhost:5432/queijaria")
engine = create_engine(DB_URL, future=True)

QUERIES = {
    "produtos_count": "SELECT count(*) AS cnt FROM produtos;",
    "receitas_count": "SELECT count(*) AS cnt FROM receitas;",
    "itens_receita_count": "SELECT count(*) AS cnt FROM receita_itens;",
    "estoque_count": "SELECT count(*) AS cnt FROM estoque;",
    "ordens_count": "SELECT count(*) AS cnt FROM ordens_producao;",
    "consumos_count": "SELECT count(*) AS cnt FROM insumos_consumo;",
    "v_cumprimento_sample": "SELECT * FROM v_kpi_cumprimento_plano LIMIT 5;",
    "v_leadtime_sample": "SELECT * FROM v_kpi_leadtime_produto LIMIT 5;",
    "v_capacidade_sample": "SELECT * FROM v_kpi_capacidade_utilizada LIMIT 5;",
    "v_necessidade_insumos_sample": "SELECT * FROM v_necessidade_insumos_por_op LIMIT 10;"
}

def run_checks():
    print("Conectando em:", DB_URL)
    with engine.connect() as conn:
        for name, q in QUERIES.items():
            try:
                df = pd.read_sql(text(q), conn)
                print(f"\n--- {name} ---")
                print(df)
            except Exception as e:
                print(f"\n[ERROR] {name}: {e}")

if __name__ == "__main__":
    run_checks()
