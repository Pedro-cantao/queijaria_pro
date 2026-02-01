# src/backend/etl/etl.py
#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

# imports relativos dentro do pacote
from .utils import setup_logger, PROJECT_ROOT
from .extract import backup_raw, read_csv_safe
from .transform import (
    normalize_produtos, normalize_receitas, normalize_receita_itens,
    normalize_ordens, save_clean
)
from .reserve_stock import reservar_para_ordens

logger = setup_logger("etl.main", log_file=os.path.join(PROJECT_ROOT, "etl_run.log"))

def call_loader():
    """
    Chama o loader como módulo para manter contexto de pacote.
    Assumimos que src/backend/etl/load.py tem um main() ou é executável como módulo.
    """
    logger.info("Executando loader (inserção no banco)...")
    # executa como módulo do pacote para evitar problemas de import relativo
    cmd = [sys.executable, "-m", "src.backend.etl.load"]
    res = subprocess.run(cmd)
    if res.returncode != 0:
        logger.error("Loader retornou código %s", res.returncode)
        raise RuntimeError("Loader falhou")
    logger.info("Loader finalizado com sucesso.")

def run_etl():
    logger.info("=== Iniciando ETL ===")
    # 1) backup raw
    backup_raw()

    # 2) extract (leitura dos CSVs)
    df_prod = read_csv_safe("produtos.csv")
    df_rec = read_csv_safe("receitas.csv")
    df_it = read_csv_safe("receita_itens.csv")
    df_ord = read_csv_safe("ordens_producao.csv", parse_dates=["inicio_planejado","fim_planejado","inicio_real","fim_real"])
    df_estoque = read_csv_safe("estoque.csv")

    # 3) transform
    prod_clean = normalize_produtos(df_prod)
    rec_clean = normalize_receitas(df_rec)
    it_clean = normalize_receita_itens(df_it)
    ord_clean = normalize_ordens(df_ord)

    # 4) salvar clean
    save_clean(prod_clean, "produtos_clean.csv")
    save_clean(rec_clean, "receitas_clean.csv")
    save_clean(it_clean, "receita_itens_clean.csv")
    save_clean(ord_clean, "ordens_producao_clean.csv")

    # 5) reservar estoque (idempotente)
    ok = reservar_para_ordens(max_ops=None)
    if not ok:
        logger.warning("Reserva de estoque reportou erro; verifique logs e relatório de faltas.")

    # 6) load (inserir no banco)
    call_loader()

    logger.info("=== ETL finalizado ===")

if __name__ == "__main__":
    # rodar como módulo do pacote é recomendado:
    # python -m src.backend.etl.etl
    run_etl()
