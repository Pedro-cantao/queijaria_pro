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

def gerar_ordens(n_ordens=200):
    prod_path = os.path.join(DATA_DIR, "produtos.csv")
    rec_it_path = os.path.join(DATA_DIR, "receita_itens.csv")
    if not os.path.exists(prod_path) or not os.path.exists(rec_it_path):
        raise FileNotFoundError("Gere receitas antes de gerar ordens (executar gerar_receitas.py)")

    df_prod = pd.read_csv(prod_path)
    df_it = pd.read_csv(rec_it_path)

    ordens = []
    consumos = []
    maquinas = ["L01","L02","L03"]
    operadores = [fake.name() for _ in range(12)]

    for i in range(n_ordens):
        produto = df_prod.sample(1).iloc[0]
        produto_codigo = produto['produto_codigo']
        receita_itens = df_it[df_it['produto_codigo'] == produto_codigo]
        unidades = int(np.random.choice([5,10,20,50,100,200], p=[0.05,0.15,0.25,0.25,0.2,0.1]))
        inicio_planejado = datetime.now() - timedelta(days=random.randint(0,30), hours=random.randint(0,12))
        duracao_horas = max(0.5, unidades / 50)  # heurística simples
        fim_planejado = inicio_planejado + timedelta(hours=duracao_horas)
        inicio_real = inicio_planejado + timedelta(minutes=random.randint(-30,60))
        fim_real = fim_planejado + timedelta(minutes=random.randint(-60,120))
        status = random.choices(["finalizada","em_processo","descartada","planejada"], weights=[0.5,0.2,0.05,0.25])[0]
        if status == "finalizada" and fim_real < inicio_real:
            fim_real = inicio_real + timedelta(hours=duracao_horas)

        op_num = f"OP{10000 + i}"
        ordens.append({
            "numero_op": op_num,
            "produto_codigo": produto_codigo,
            "unidades_planejadas": unidades,
            "volume_planejado": round(unidades * 4.0,2),
            "inicio_planejado": inicio_planejado,
            "fim_planejado": fim_planejado,
            "inicio_real": inicio_real,
            "fim_real": fim_real,
            "operador": random.choice(operadores),
            "linha_equipamento": random.choice(maquinas),
            "status": status
        })

        # calcular consumo por item
        for _, it in receita_itens.iterrows():
            qpu = float(it['quantidade_por_unidade'])
            total = qpu * unidades
            custo_unit = round(random.uniform(0.05,5.0),4)
            consumos.append({
                "numero_op": op_num,
                "item_codigo": it['item_codigo'],
                "quantidade": round(total,6),
                "unidade_medida": it['unidade_medida'],
                "custo_unitario": custo_unit,
                "custo_total": round(total * custo_unit,2)
            })

    pd.DataFrame(ordens).to_csv(os.path.join(DATA_DIR,"ordens_producao.csv"), index=False)
    pd.DataFrame(consumos).to_csv(os.path.join(DATA_DIR,"insumos_consumo.csv"), index=False)
    print("Ordens e consumos gerados em:", DATA_DIR)

if __name__ == "__main__":
    gerar_ordens(n_ordens=200)
