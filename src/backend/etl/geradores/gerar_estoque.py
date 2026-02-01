import os
import pandas as pd
import random
from faker import Faker

fake = Faker("pt_BR")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def gerar_estoque(n_itens=50):
    rows = []
    tipos = ["IN","EM","MP","PI","MC"]
    unidades = ["KG","LT","UN","EV"]
    locais = ["ALMOX1","ALMOX2","CAMARA1","CAMARA2"]
    for i in range(n_itens):
        codigo = f"IT{1000+i}"
        tipo = random.choice(tipos)
        lote = f"L{fake.bothify(text='??-#####')}"
        quantidade = round(random.uniform(5, 5000),6)
        unidade = random.choice(unidades)
        local = random.choice(locais)
        rows.append({
            "item_codigo": codigo,
            "tipo_item": tipo,
            "lote": lote,
            "quantidade": quantidade,
            "unidade": unidade,
            "localizacao": local
        })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA_DIR, "estoque.csv"), index=False)
    print("Estoque gerado em:", DATA_DIR)

if __name__ == "__main__":
    gerar_estoque(n_itens=80)
