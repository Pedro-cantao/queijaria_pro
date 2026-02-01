# src/backend/etl/transform.py
import os
import pandas as pd
from .utils import CLEAN_DIR, setup_logger

logger = setup_logger("etl.transform")

def normalize_produtos(df):
    if df is None:
        return None
    df = df.copy()
    df['produto_codigo'] = df['produto_codigo'].astype(str).str.strip()
    df['nome'] = df['nome'].astype(str).str.strip()
    df['unidade_base'] = df.get('unidade_base', 'UN')
    df = df.drop_duplicates(subset=['produto_codigo'])
    return df

def normalize_receitas(df):
    if df is None:
        return None
    df = df.copy()
    df['produto_codigo'] = df['produto_codigo'].astype(str).str.strip()
    df['descricao'] = df.get('descricao', df['produto_codigo'])
    df['rendimento_unidade'] = pd.to_numeric(df.get('rendimento_unidade', 1.0), errors='coerce').fillna(1.0)
    df = df.drop_duplicates(subset=['produto_codigo'])
    return df

def normalize_receita_itens(df):
    if df is None:
        return None
    df = df.copy()
    df['produto_codigo'] = df['produto_codigo'].astype(str).str.strip()
    df['item_codigo'] = df['item_codigo'].astype(str).str.strip()
    df['quantidade_por_unidade'] = pd.to_numeric(df['quantidade_por_unidade'], errors='coerce').fillna(0)
    df['unidade_medida'] = df.get('unidade_medida', '')
    df = df.drop_duplicates(subset=['produto_codigo','item_codigo'])
    return df

def normalize_ordens(df):
    if df is None:
        return None
    df = df.copy()
    for col in ['inicio_planejado','fim_planejado','inicio_real','fim_real']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    df['produto_codigo'] = df['produto_codigo'].astype(str).str.strip()
    df['unidades_planejadas'] = pd.to_numeric(df.get('unidades_planejadas',0), errors='coerce').fillna(0)
    df = df.drop_duplicates(subset=['numero_op'])
    return df

def save_clean(df, name):
    """
    Salva DataFrame em CLEAN_DIR com nome fornecido.
    """
    if df is None:
        logger.warning("Nenhum dataframe para salvar: %s", name)
        return None
    out = os.path.join(CLEAN_DIR, name)
    df.to_csv(out, index=False)
    logger.info("Salvo clean: %s (%d linhas)", out, len(df))
    return out
