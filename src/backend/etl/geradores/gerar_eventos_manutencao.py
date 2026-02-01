
import os
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("pt_BR")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def gerar_eventos_manutencao(n_eventos=100, impacto_max_horas=8):
    """
    Gera eventos de manutenção com impacto em linhas/equipamentos.
    Saída: manutencao_eventos.csv
    """
    maquinas_path = os.path.join(DATA_DIR, "maquinas.csv")
    if os.path.exists(maquinas_path):
        df_maquinas = pd.read_csv(maquinas_path)
        maquinas = df_maquinas["codigo"].tolist()
    else:
        maquinas = ["L01","L02","L03"]

    eventos = []
    now = datetime.now()
    causas = ["preventiva","corretiva","falha elétrica","falha mecânica","ajuste de calibração","limpeza CIP"]
    tipos = ["preventiva","corretiva"]

    for i in range(n_eventos):
        maquina = random.choice(maquinas)
        inicio = now - timedelta(days=random.randint(0,30), hours=random.randint(0,23), minutes=random.randint(0,59))
        duracao = round(random.uniform(0.25, impacto_max_horas),2)  # horas
        fim = inicio + timedelta(hours=duracao)
        tipo = random.choices(tipos, weights=[0.6,0.4])[0]
        causa = random.choice(causas)
        impacto_ops = random.randint(0,5)  # quantas OP afetadas estimadas
        eventos.append({
            "evento_id": f"EV{10000+i}",
            "maquina_codigo": maquina,
            "tipo_manutencao": tipo,
            "causa": causa,
            "inicio": inicio,
            "fim": fim,
            "duracao_horas": round(duracao,2),
            "impacto_estimado_ops": impacto_ops,
            "descricao": fake.sentence(nb_words=8)
        })

    df_ev = pd.DataFrame(eventos)
    out_path = os.path.join(DATA_DIR, "manutencao_eventos.csv")
    df_ev.to_csv(out_path, index=False)
    print("Eventos de manutenção gerados em:", out_path)
    return out_path

if __name__ == "__main__":
    gerar_eventos_manutencao(n_eventos=120, impacto_max_horas=10)
