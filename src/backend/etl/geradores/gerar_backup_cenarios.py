# src/backend/etl/geradores/gerar_backup_cenarios.py
import os
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("pt_BR")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def gerar_backup_cenarios(n_cenarios=100):
    """
    Combina dados de faltas, manutenção e ordens para criar cenários de stress.
    Saída: cenarios_backup.csv
    """
    ordens_path = os.path.join(DATA_DIR, "ordens_producao.csv")
    faltas_path = os.path.join(DATA_DIR, "faltas_estoque.csv")
    manut_path = os.path.join(DATA_DIR, "manutencao_eventos.csv")

    if not os.path.exists(ordens_path):
        raise FileNotFoundError("Gere ordens antes (ordens_producao.csv).")

    df_ord = pd.read_csv(ordens_path, parse_dates=["inicio_planejado","fim_planejado","inicio_real","fim_real"])
    df_faltas = pd.read_csv(faltas_path) if os.path.exists(faltas_path) else pd.DataFrame()
    df_manut = pd.read_csv(manut_path, parse_dates=["inicio","fim"]) if os.path.exists(manut_path) else pd.DataFrame()

    ordens = df_ord.to_dict(orient="records")
    cenarios = []

    for i in range(n_cenarios):
        op = random.choice(ordens)
        numero_op = op["numero_op"]
        # escolher se o cenário inclui falta, manutenção, atraso
        inclui_falta = (not df_faltas.empty) and (random.random() < 0.4)
        inclui_manut = (not df_manut.empty) and (random.random() < 0.3)
        atraso_min = random.choice([0, 30, 60, 120, 240])  # minutos
        impacto = {
            "numero_op": numero_op,
            "cenario_id": f"CEN{10000+i}",
            "inclui_falta": inclui_falta,
            "inclui_manut": inclui_manut,
            "atraso_minutos": atraso_min,
            "gravidade": random.choice(["baixa","media","alta"]),
            "descricao": ""
        }
        motivos = []
        if inclui_falta:
            # pegar uma falta relacionada se existir
            possiveis = df_faltas[df_faltas["numero_op"] == numero_op] if not df_faltas.empty else pd.DataFrame()
            if not possiveis.empty:
                sel = possiveis.sample(1).iloc[0]
                motivos.append(f"falta:{sel['item_codigo']}({sel['quantidade_em_falta']})")
            else:
                motivos.append("falta:insumo_generico")
        if inclui_manut:
            # pegar evento de manut aleatório
            if not df_manut.empty:
                sel = df_manut.sample(1).iloc[0]
                motivos.append(f"manut:{sel['maquina_codigo']} dur:{sel['duracao_horas']}h")
            else:
                motivos.append("manut:maquina_generica")
        if atraso_min > 0:
            motivos.append(f"atraso:{atraso_min}min")

        impacto["descricao"] = "; ".join(motivos) if motivos else "nenhum"
        cenarios.append(impacto)

    df = pd.DataFrame(cenarios)
    out_path = os.path.join(DATA_DIR, "cenarios_backup.csv")
    df.to_csv(out_path, index=False)
    print("Cenários de backup gerados em:", out_path)
    return out_path

if __name__ == "__main__":
    gerar_backup_cenarios(n_cenarios=120)
