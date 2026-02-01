import pandas as pd
import random
from faker import Faker
from datetime import datetime

fake = Faker("pt_BR")

def gerar_dados_queijaria(n_linhas=10000, caminho_saida="dados_queijaria_vaca.csv"):
    fornecedores = [f"F{str(i).zfill(3)}" for i in range(1, 21)]
    tanques = [f"T{str(i).zfill(2)}" for i in range(1, 6)]

    registros = []
    for _ in range(n_linhas):
        fornecedor = random.choice(fornecedores)
        tipo_leite = "Vaca"
        coleta = fake.date_time_this_year()
        volume = round(random.uniform(200, 5000), 2)
        temp = round(random.uniform(3, 8), 1)
        densidade = round(random.uniform(1.028, 1.034), 3)
        ph = round(random.uniform(6.5, 6.9), 2)
        acidez = random.randint(14, 20)
        gordura = round(random.uniform(3.0, 5.5), 2)
        proteina = round(random.uniform(2.8, 4.0), 2)
        lactose = round(random.uniform(4.4, 5.2), 2)
        ccs = random.randint(100000, 500000)
        cbt = random.randint(20000, 200000)
        antibiotico = random.choice(["Sim", "Não"])
        rejeicao = "" if antibiotico == "Não" else "Antibiótico detectado"
        preco = round(random.uniform(2.0, 3.0), 2)
        custo_total = round(volume * preco, 2)
        tanque = random.choice(tanques)

        registros.append([
            fornecedor, tipo_leite, coleta.strftime("%Y-%m-%d %H:%M:%S"), volume, temp, densidade, ph, acidez,
            gordura, proteina, lactose, ccs, cbt, antibiotico, rejeicao,
            preco, custo_total, tanque
        ])

    colunas = [
        "Fornecedor", "TipoLeite", "DataHoraColeta", "Volume(L)", "TempRecepcao(°C)",
        "Densidade", "pH", "AcidezDornic(°D)", "Gordura(%)", "Proteina(%)",
        "Lactose(%)", "CCS", "CBT", "Antibiotico", "Rejeicao",
        "PrecoPorLitro", "CustoTotal", "TanqueDestino"
    ]

    df = pd.DataFrame(registros, columns=colunas)
    df.to_csv(caminho_saida, index=False)
    print(f"✅ Arquivo gerado com sucesso: {caminho_saida}")

if __name__ == "__main__":
    gerar_dados_queijaria()
