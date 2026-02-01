import os
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def gerar_capacidade():
    maquinas = [
        {"codigo":"L01","descricao":"Linha 1 - Mussarela","capacidade_hora":200},
        {"codigo":"L02","descricao":"Linha 2 - Queijo Prato","capacidade_hora":150},
        {"codigo":"L03","descricao":"Linha 3 - Queijo Minas","capacidade_hora":120}
    ]
    turnos = [
        {"nome":"Manha","inicio":"06:00:00","fim":"14:00:00"},
        {"nome":"Tarde","inicio":"14:00:00","fim":"22:00:00"},
        {"nome":"Noite","inicio":"22:00:00","fim":"06:00:00"}
    ]
    pd.DataFrame(maquinas).to_csv(os.path.join(DATA_DIR,"maquinas.csv"), index=False)
    pd.DataFrame(turnos).to_csv(os.path.join(DATA_DIR,"turnos.csv"), index=False)
    print("Maquinas e turnos gerados em:", DATA_DIR)

if __name__ == "__main__":
    gerar_capacidade()
