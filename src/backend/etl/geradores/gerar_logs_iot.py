# src/backend/etl/geradores/gerar_logs_iot.py
import os
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker("pt_BR")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def gerar_logs_iot(n_ops=50, pontos_por_op=120, freq_minutos=1):
    """
    Gera leituras de sensores (temp, pH, vazao) por OP.
    Requer ordens_producao.csv para amostrar OP reais.
    Saída: iot_readings.csv
    """
    ordens_path = os.path.join(DATA_DIR, "ordens_producao.csv")
    if not os.path.exists(ordens_path):
        raise FileNotFoundError("Gere ordens antes (ordens_producao.csv).")

    df_ord = pd.read_csv(ordens_path, parse_dates=["inicio_planejado","fim_planejado","inicio_real","fim_real"])
    sampled = df_ord.sample(min(n_ops, len(df_ord))).to_dict(orient="records")

    rows = []
    sensor_types = [
        ("temp_pasteurizacao","C"),
        ("ph_coagulacao","pH"),
        ("vazao_leite","L/min")
    ]

    for op in sampled:
        numero_op = op["numero_op"]
        # define janela: se existir inicio_real/fim_real usa, senão usa inicio_planejado/fim_planejado
        start = pd.to_datetime(op.get("inicio_real") or op.get("inicio_planejado") or datetime.now())
        end = pd.to_datetime(op.get("fim_real") or op.get("fim_planejado") or (start + timedelta(hours=1)))
        total_minutes = int((end - start).total_seconds() / 60)
        if total_minutes <= 0:
            total_minutes = max(1, pontos_por_op)
            end = start + timedelta(minutes=total_minutes)
        step = max(1, int(total_minutes / pontos_por_op))

        timestamps = [start + timedelta(minutes=i) for i in range(0, total_minutes+1, step)]
        for ts in timestamps:
            # gerar leituras por sensor
            temp = round(np.random.normal(loc=72.0, scale=1.5),2)  # exemplo pasteurização em C
            ph = round(np.random.normal(loc=6.6, scale=0.05),2)
            vazao = round(abs(np.random.normal(loc=120.0, scale=20.0)),2)
            rows.append({
                "numero_op": numero_op,
                "ts": ts,
                "sensor": "temp_pasteurizacao",
                "unit": "C",
                "value": temp
            })
            rows.append({
                "numero_op": numero_op,
                "ts": ts,
                "sensor": "ph_coagulacao",
                "unit": "pH",
                "value": ph
            })
            rows.append({
                "numero_op": numero_op,
                "ts": ts,
                "sensor": "vazao_leite",
                "unit": "L/min",
                "value": vazao
            })

    df = pd.DataFrame(rows)
    out_path = os.path.join(DATA_DIR, "iot_readings.csv")
    df.to_csv(out_path, index=False)
    print("Logs IoT gerados em:", out_path)
    return out_path

if __name__ == "__main__":
    gerar_logs_iot(n_ops=60, pontos_por_op=100, freq_minutos=1)
