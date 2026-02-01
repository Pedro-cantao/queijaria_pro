
import os
import pandas as pd
import random
from faker import Faker

fake = Faker("pt_BR")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def gerar_faltas_estoque(n_cenarios=50, prob_falta_por_item=0.15):
    """
    Gera cenários de falta de insumo para ordens existentes.
    Requer arquivos: ordens_producao.csv e receita_itens.csv em data/.
    Saída: faltas_estoque.csv
    """
    ordens_path = os.path.join(DATA_DIR, "ordens_producao.csv")
    itens_path = os.path.join(DATA_DIR, "receita_itens.csv")
    estoque_path = os.path.join(DATA_DIR, "estoque.csv")

    if not os.path.exists(ordens_path) or not os.path.exists(itens_path):
        raise FileNotFoundError("Gere ordens e receitas antes (ordens_producao.csv, receita_itens.csv).")

    df_ord = pd.read_csv(ordens_path)
    df_it = pd.read_csv(itens_path)
    df_estoque = pd.read_csv(estoque_path) if os.path.exists(estoque_path) else pd.DataFrame(columns=["item_codigo","quantidade"])

    faltas = []
    sampled_ops = df_ord.sample(min(n_cenarios, len(df_ord))).to_dict(orient="records")

    for op in sampled_ops:
        numero_op = op["numero_op"]
        produto_codigo = op.get("produto_codigo")
        unidades = float(op.get("unidades_planejadas", 1))
        itens_receita = df_it[df_it["produto_codigo"] == produto_codigo]
        for _, it in itens_receita.iterrows():
            item = it["item_codigo"]
            qpu = float(it.get("quantidade_por_unidade") or 0)
            necessidade = qpu * unidades
            # probabilidade de faltar
            if random.random() < prob_falta_por_item:
                # calcular estoque disponível (soma por item)
                estoque_disp = 0.0
                if not df_estoque.empty:
                    estoque_disp = float(df_estoque[df_estoque["item_codigo"] == item]["quantidade"].sum() or 0.0)
                falta = max(0.0, necessidade - estoque_disp)
                faltas.append({
                    "numero_op": numero_op,
                    "item_codigo": item,
                    "necessidade": round(necessidade,6),
                    "estoque_disponivel": round(estoque_disp,6),
                    "quantidade_em_falta": round(falta,6),
                    "unidade_medida": it.get("unidade_medida",""),
                    "motivo": random.choice(["lead_time fornecedor","erro inventário","consumo inesperado","lote contaminado"])
                })

    df_faltas = pd.DataFrame(faltas)
    out_path = os.path.join(DATA_DIR, "faltas_estoque.csv")
    df_faltas.to_csv(out_path, index=False)
    print("Faltas geradas em:", out_path)
    return out_path

if __name__ == "__main__":
    gerar_faltas_estoque(n_cenarios=80, prob_falta_por_item=0.18)
