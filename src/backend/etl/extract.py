# src/backend/etl/extract.py
import os
import shutil
import pandas as pd
from .utils import DATA_DIR, RAW_DIR, timestamped_filename, setup_logger

logger = setup_logger("etl.extract")

# arquivos esperados (ajuste se necessário)
EXPECTED = [
    "produtos.csv",
    "receitas.csv",
    "receita_itens.csv",
    "estoque.csv",
    "maquinas.csv",
    "turnos.csv",
    "ordens_producao.csv",
    "insumos_consumo.csv",
    "faltas_estoque.csv",
    "manutencao_eventos.csv",
    "iot_readings.csv",
    "consumo_energia.csv",
    "rejeicoes_qualidade.csv",
    "cenarios_backup.csv"
]

def backup_raw():
    """
    Copia arquivos existentes de DATA_DIR para RAW_DIR com timestamp.
    Retorna lista de caminhos copiados.
    """
    copiados = []
    for fname in EXPECTED:
        src = os.path.join(DATA_DIR, fname)
        if os.path.exists(src):
            dst_name = timestamped_filename(fname.replace(".csv",""))
            dst = os.path.join(RAW_DIR, dst_name)
            shutil.copy2(src, dst)
            copiados.append(dst)
            logger.info("Backup raw: %s -> %s", src, dst)
        else:
            logger.debug("Arquivo não encontrado (ignorado): %s", src)
    return copiados

def read_csv_safe(fname, parse_dates=None):
    """
    Lê CSV de DATA_DIR com tratamento de erro.
    Retorna DataFrame ou None.
    """
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        logger.warning("Arquivo não encontrado: %s", path)
        return None
    try:
        df = pd.read_csv(path, parse_dates=parse_dates)
        logger.info("Lido: %s (%d linhas)", fname, len(df))
        return df
    except Exception as e:
        logger.error("Erro ao ler %s: %s", fname, e)
        raise
