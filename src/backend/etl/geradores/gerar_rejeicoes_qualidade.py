# src/backend/etl/geradores/gerar_rejeicoes_qualidade.py
import os
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("pt_BR")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def gerar_rejeicoes_qualidade(n_amostras=500, taxa_rejeicao_base=0.05):
    """
    Gera amostras de controle de qualidade com resultados e marca rejeição.
    Saída: rejeicoes_qualidade.csv
    """
    ordens_path = os.path.join(DATA_DIR, "ordens_producao.csv")
    if not os.path.exists(ordens_path):
        raise FileNotFoundError("Gere ordens antes (ordens_producao.csv).")

    df_ord = pd.read_csv(ordens_path, parse_dates=["inicio_planejado","fim_planejado","inicio_real","fim_real"])
    ordens = df_ord["numero_op"].tolist()
    parametros = [
        ("pH", 6.5, 6.9, 0.05),
        ("umidade", 45.0, 55.0, 2.0),
        ("gordura_ges", 20.0, 30.0, 1.5),
        ("ccs", 10000, 50000, 5000)  # contagem de células somáticas
    ]

    rows = []
    for i in range(n_amostras):
        numero_op = random.choice(ordens)
        ts = datetime.now() - timedelta(days=random.randint(0,30), minutes=random.randint(0,1440))
        sample_id = f"QA{int(datetime.timestamp(ts))}{i}"
        results = {}
        rejeitado = False
        motivos = []
        for p, low, high, sigma in parametros:
            if isinstance(low, int) and isinstance(high, int):
                val = int(random.gauss((low+high)/2, sigma))
            else:
                val = round(random.gauss((low+high)/2, sigma), 3)
            results[p] = val
            # regra simples de rejeição: fora do intervalo +/- tolerância
            if p == "pH":
                if val < low or val > high:
                    rejeitado = True
                    motivos.append(f"{p} fora de faixa")
            elif p == "ccs":
                if val > high:
                    rejeitado = True
                    motivos.append(f"{p} alto")
            else:
                if val < low or val > high:
                    rejeitado = True
                    motivos.append(f"{p} fora de faixa")

        # probabilidade adicional de rejeição aleatória
        if random.random() < taxa_rejeicao_base:
            rejeitado = True
            motivos.append("amostra aleatória falha")

        rows.append({
            "sample_id": sample_id,
            "numero_op": numero_op,
            "ts": ts,
            "pH": results["pH"],
            "umidade": results["umidade"],
            "gordura_ges": results["gordura_ges"],
            "ccs": results["ccs"],
            "rejeitado": rejeitado,
            "motivo_rejeicao": "; ".join(motivos) if motivos else ""
        })

    df = pd.DataFrame(rows)
    out_path = os.path.join(DATA_DIR, "rejeicoes_qualidade.csv")
    df.to_csv(out_path, index=False)
    print("Rejeições de qualidade geradas em:", out_path)
    return out_path

if __name__ == "__main__":
    gerar_rejeicoes_qualidade(n_amostras=600, taxa_rejeicao_base=0.04)
