# src/backend/etl/geradores/gerar_consumo_energia.py
import os
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("pt_BR")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def gerar_consumo_energia(n_registros=None):
    """
    Gera consumo de água (L), vapor (kg) e energia (kWh) por OP.
    Se n_registros for None, usa todas as ordens em ordens_producao.csv.
    Saída: consumo_energia.csv
    """
    ordens_path = os.path.join(DATA_DIR, "ordens_producao.csv")
    if not os.path.exists(ordens_path):
        raise FileNotFoundError("Gere ordens antes (ordens_producao.csv).")

    df_ord = pd.read_csv(ordens_path, parse_dates=["inicio_planejado","fim_planejado","inicio_real","fim_real"])
    if n_registros:
        df_ord = df_ord.sample(min(n_registros, len(df_ord)))
    rows = []
    for _, op in df_ord.iterrows():
        numero_op = op["numero_op"]
        unidades = float(op.get("unidades_planejadas") or 1)
        # heurísticas de consumo por unidade (ajustáveis)
        agua_por_unidade = random.uniform(5.0, 20.0)   # L por unidade
        vapor_por_unidade = random.uniform(0.5, 3.0)   # kg por unidade
        energia_por_unidade = random.uniform(0.2, 1.5) # kWh por unidade

        agua_total = round(agua_por_unidade * unidades, 3)
        vapor_total = round(vapor_por_unidade * unidades, 3)
        energia_total = round(energia_por_unidade * unidades, 3)

        custo_agua = round(agua_total * random.uniform(0.001, 0.005), 2)   # custo por L
        custo_vapor = round(vapor_total * random.uniform(0.02, 0.08), 2)  # custo por kg
        custo_energia = round(energia_total * random.uniform(0.2, 0.8), 2) # custo por kWh

        rows.append({
            "numero_op": numero_op,
            "unidades": unidades,
            "agua_L": agua_total,
            "vapor_kg": vapor_total,
            "energia_kWh": energia_total,
            "custo_agua": custo_agua,
            "custo_vapor": custo_vapor,
            "custo_energia": custo_energia,
            "custo_total": round(custo_agua + custo_vapor + custo_energia, 2)
        })

    df = pd.DataFrame(rows)
    out_path = os.path.join(DATA_DIR, "consumo_energia.csv")
    df.to_csv(out_path, index=False)
    print("Consumo de energia gerado em:", out_path)
    return out_path

if __name__ == "__main__":
    gerar_consumo_energia(n_registros=None)
