import os
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker("pt_BR")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def gerar_receitas(n_produtos=5):
    produtos = []
    receitas = []
    itens = []

    # receita base: Mussarela 4kg (exemplo fiel ao que você forneceu)
    base_codigo = "PA0170003"
    base_nome = "QUEIJO MUSSARELA 4 KG"
    produtos.append({"produto_codigo": base_codigo, "nome": base_nome, "unidade_base": "UN"})
    receitas.append({"produto_codigo": base_codigo, "descricao": base_nome, "rendimento_unidade": 1.0})

    base_itens = [
        ("EM0020001","EM","SACOLA P/ QUEIJO MUSSARELA",0.250000,"UN"),
        ("EM0020018","EM","CAIXA PAPELAO QUEIJO MUSSARELA",0.041667,"UN"),
        ("EM0020024","EM","FILME STRETCH MANUAL 500MM",0.000121,"KG"),
        ("IN0010007","IN","SAL REFINADO IODADO 25 KG",0.026000,"KG"),
        ("MC0150272","MC","PALLETS DE MADEIRA",0.000833,"UN"),
        ("PI0170003","PI","QUEIJO MUSSARELA (INTER)",1.000000,"KG"),
        ("IN0010021","IN","FERMENTO QUEIJO MUSSARELA",0.001000,"EV"),
        ("IN0010024","IN","CLORETO DE CALCIO SOL 40 26KG",0.003500,"KG"),
        ("IN0010071","IN","COAGULANTE",0.000378,"LT"),
        ("MP0160004","MP","SORO DE LEITE FLUIDO",-2.833333,"LT"),
        ("MP0160009","MP","LEITE PADRONIZADO MUSSARELA",10.000000,"LT"),
        ("MP0160001","MP","LEITE CRU REFRIGERADO",10.120000,"LT"),
        ("MP0160010","MP","CREME DE LEITE",-0.083000,"KG")
    ]
    for it in base_itens:
        itens.append({
            "produto_codigo": base_codigo,
            "item_codigo": it[0],
            "tipo_item": it[1],
            "descricao_item": it[2],
            "quantidade_por_unidade": it[3],
            "unidade_medida": it[4],
            "observacao": ""
        })

    # gerar produtos sintéticos adicionais
    for i in range(n_produtos - 1):
        codigo = f"PA{1000000 + i}"
        nome = f"QUEIJO_TESTE_{i}"
        produtos.append({"produto_codigo": codigo, "nome": nome, "unidade_base": "UN"})
        receitas.append({"produto_codigo": codigo, "descricao": nome, "rendimento_unidade": 1.0})
        for j in range(3):
            item_code = f"IN{2000 + i*10 + j}"
            itens.append({
                "produto_codigo": codigo,
                "item_codigo": item_code,
                "tipo_item": "IN",
                "descricao_item": fake.word().upper(),
                "quantidade_por_unidade": round(np.random.uniform(0.001, 2.0),6),
                "unidade_medida": "KG",
                "observacao": ""
            })

    pd.DataFrame(produtos).to_csv(os.path.join(DATA_DIR, "produtos.csv"), index=False)
    pd.DataFrame(receitas).to_csv(os.path.join(DATA_DIR, "receitas.csv"), index=False)
    pd.DataFrame(itens).to_csv(os.path.join(DATA_DIR, "receita_itens.csv"), index=False)
    print("Receitas geradas em:", DATA_DIR)

if __name__ == "__main__":
    gerar_receitas(n_produtos=6)
