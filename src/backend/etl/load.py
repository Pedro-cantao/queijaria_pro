# src/backend/etl/load.py
import os
import logging
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# -------------------------------------------------------------------
# Configuração de logging
# -------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Carregar variáveis do .env
# -------------------------------------------------------------------
load_dotenv()
DB_URL = os.getenv(
    "DATABASE_URL"
)

# Criar engine de conexão
engine = create_engine(DB_URL, future=True)

# -------------------------------------------------------------------
# Diretório de dados
# -------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DATA_DIR = os.getenv("DATA_DIR", "/app/data")



# -------------------------------------------------------------------
# Funções auxiliares
# -------------------------------------------------------------------
def _read_csv_safe(name, parse_dates=None):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        logger.warning("%s não encontrado em %s", name, DATA_DIR)
        return None
    return pd.read_csv(path, parse_dates=parse_dates)


# -------------------------------------------------------------------
# Funções de carga
# -------------------------------------------------------------------
def load_produtos():
    df = _read_csv_safe("produtos.csv")
    if df is None:
        return
    with engine.begin() as conn:
        for _, r in df.iterrows():
            conn.execute(
                text(
                    """
                INSERT INTO produtos (produto_codigo, nome, unidade_base)
                VALUES (:codigo, :nome, :unidade)
                ON CONFLICT (produto_codigo) DO UPDATE
                  SET nome = EXCLUDED.nome, unidade_base = EXCLUDED.unidade_base
            """
                ),
                {
                    "codigo": str(r["produto_codigo"]).strip(),
                    "nome": str(r["nome"]).strip(),
                    "unidade": r.get("unidade_base", "UN"),
                },
            )
    logger.info("produtos carregados.")


def load_receitas_e_itens():
    df_rec = _read_csv_safe("receitas.csv")
    df_it = _read_csv_safe("receita_itens.csv")
    if df_rec is None or df_it is None:
        return
    with engine.begin() as conn:
        for _, rec in df_rec.iterrows():
            produto_codigo = str(rec["produto_codigo"]).strip()
            descricao = rec.get("descricao", produto_codigo)
            rendimento = float(rec.get("rendimento_unidade") or 1.0)
            prod = conn.execute(
                text("SELECT produto_id FROM produtos WHERE produto_codigo = :pc"),
                {"pc": produto_codigo},
            ).fetchone()
            if not prod:
                logger.warning(
                    "produto %s não cadastrado; pulando receita.", produto_codigo
                )
                continue
            produto_id = prod[0]
            existing = conn.execute(
                text("SELECT receita_id FROM receitas WHERE produto_id = :pid"),
                {"pid": produto_id},
            ).fetchone()
            if existing:
                receita_id = existing[0]
                conn.execute(
                    text(
                        "UPDATE receitas SET descricao = :d, rendimento_unidade = :r WHERE receita_id = :rid"
                    ),
                    {"d": descricao, "r": rendimento, "rid": receita_id},
                )
            else:
                receita_id = conn.execute(
                    text(
                        """
                    INSERT INTO receitas (produto_id, descricao, rendimento_unidade)
                    VALUES (:pid, :d, :r) RETURNING receita_id
                """
                    ),
                    {"pid": produto_id, "d": descricao, "r": rendimento},
                ).fetchone()[0]
            # remover itens antigos e inserir atuais
            conn.execute(
                text("DELETE FROM receita_itens WHERE receita_id = :rid"),
                {"rid": receita_id},
            )
            itens_prod = df_it[df_it["produto_codigo"] == produto_codigo]
            for _, it in itens_prod.iterrows():
                conn.execute(
                    text(
                        """
                    INSERT INTO receita_itens (receita_id, item_codigo, tipo_item, descricao_item,
                                               quantidade_por_unidade, unidade_medida, observacao)
                    VALUES (:rid, :ic, :ti, :di, :qpu, :um, :obs)
                """
                    ),
                    {
                        "rid": receita_id,
                        "ic": str(it.get("item_codigo")).strip(),
                        "ti": str(it.get("tipo_item") or "").strip(),
                        "di": str(it.get("descricao_item") or "").strip(),
                        "qpu": float(it.get("quantidade_por_unidade") or 0),
                        "um": str(it.get("unidade_medida") or "").strip(),
                        "obs": str(it.get("observacao") or ""),
                    },
                )
    logger.info("receitas e itens carregados.")


def load_estoque():
    df = _read_csv_safe("estoque.csv")
    if df is None:
        return
    with engine.begin() as conn:
        for _, r in df.iterrows():
            conn.execute(
                text(
                    """
                INSERT INTO estoque (item_codigo, tipo_item, lote, quantidade, unidade, localizacao, data_entrada)
                VALUES (:ic, :ti, :lote, :q, :un, :loc, now())
            """
                ),
                {
                    "ic": str(r.get("item_codigo")).strip(),
                    "ti": str(r.get("tipo_item") or "").strip(),
                    "lote": str(r.get("lote") or "").strip(),
                    "q": float(r.get("quantidade") or 0),
                    "un": str(r.get("unidade") or "").strip(),
                    "loc": str(r.get("localizacao") or ""),
                },
            )
    logger.info("estoque carregado.")


def load_capacidade_turnos():
    dfm = _read_csv_safe("maquinas.csv")
    dft = _read_csv_safe("turnos.csv")
    with engine.begin() as conn:
        if dfm is not None:
            for _, r in dfm.iterrows():
                conn.execute(
                    text(
                        """
                    INSERT INTO capacidade_maquina (codigo, descricao, capacidade_hora)
                    VALUES (:c, :d, :cap)
                    ON CONFLICT (codigo) DO UPDATE
                      SET descricao = EXCLUDED.descricao, capacidade_hora = EXCLUDED.capacidade_hora
                """
                    ),
                    {
                        "c": str(r.get("codigo")).strip(),
                        "d": str(r.get("descricao") or ""),
                        "cap": float(r.get("capacidade_hora") or 0),
                    },
                )
        if dft is not None:
            for _, r in dft.iterrows():
                conn.execute(
                    text(
                        """
                    INSERT INTO turnos (nome, inicio, fim)
                    VALUES (:n, :i, :f)
                    ON CONFLICT (nome) DO UPDATE
                      SET inicio = EXCLUDED.inicio, fim = EXCLUDED.fim
                """
                    ),
                    {
                        "n": str(r.get("nome")).strip(),
                        "i": str(r.get("inicio")),
                        "f": str(r.get("fim")),
                    },
                )
    logger.info("capacidade e turnos carregados.")


def load_ordens_e_consumos():
    df_op = _read_csv_safe(
        "ordens_producao.csv",
        parse_dates=["inicio_planejado", "fim_planejado", "inicio_real", "fim_real"],
    )
    df_cons = _read_csv_safe("insumos_consumo.csv")
    if df_op is None:
        return
    with engine.begin() as conn:
        for _, r in df_op.iterrows():
            produto_codigo = str(r.get("produto_codigo")).strip()
            prod = conn.execute(
                text("SELECT produto_id FROM produtos WHERE produto_codigo = :pc"),
                {"pc": produto_codigo},
            ).fetchone()
            if not prod:
                logger.warning(
                    "produto %s não cadastrado; pulando OP %s",
                    produto_codigo,
                    r.get("numero_op"),
                )
                continue
            produto_id = prod[0]
            rec = conn.execute(
                text("SELECT receita_id FROM receitas WHERE produto_id = :pid"),
                {"pid": produto_id},
            ).fetchone()
            receita_id = rec[0] if rec else None
            conn.execute(
                text(
                    """
                INSERT INTO ordens_producao
                (numero_op, produto_id, receita_id, unidades_planejadas, volume_planejado,
                 inicio_planejado, fim_planejado, inicio_real, fim_real, operador, linha_equipamento, status)
                VALUES (:num, :pid, :rid, :up, :vol, :ip, :fp, :ir, :fr, :op, :linha, :status)
                ON CONFLICT (numero_op) DO UPDATE SET
                  produto_id = EXCLUDED.produto_id,
                  receita_id = EXCLUDED.receita_id,
                  unidades_planejadas = EXCLUDED.unidades_planejadas,
                  volume_planejado = EXCLUDED.volume_planejado,
                  inicio_planejado = EXCLUDED.inicio_planejado,
                  fim_planejado = EXCLUDED.fim_planejado,
                  inicio_real = EXCLUDED.inicio_real,
                  fim_real = EXCLUDED.fim_real,
                  operador = EXCLUDED.operador,
                  linha_equipamento = EXCLUDED.linha_equipamento,
                  status = EXCLUDED.status
            """
                ),
                {
                    "num": str(r.get("numero_op")),
                    "pid": produto_id,
                    "rid": receita_id,
                    "up": float(r.get("unidades_planejadas") or 0),
                    "vol": float(r.get("volume_planejado") or 0),
                    "ip": r.get("inicio_planejado"),
                    "fp": r.get("fim_planejado"),
                    "ir": r.get("inicio_real"),
                    "fr": r.get("fim_real"),
                    "op": str(r.get("operador") or ""),
                    "linha": str(r.get("linha_equipamento") or ""),
                    "status": str(r.get("status") or ""),
                },
            )
        if df_cons is not None:
            for _, c in df_cons.iterrows():
                numero_op = str(c.get("numero_op"))
                op = conn.execute(
                    text("SELECT op_id FROM ordens_producao WHERE numero_op = :num"),
                    {"num": numero_op},
                ).fetchone()
                if not op:
                    continue
                op_id = op[0]
                conn.execute(
                    text(
                        """
                    INSERT INTO insumos_consumo (op_id, item_codigo, quantidade, unidade_medida, custo_unitario, custo_total)
                    VALUES (:opid, :ic, :q, :um, :cu, :ct)
                """
                    ),
                    {
                        "opid": op_id,
                        "ic": str(c.get("item_codigo")),
                        "q": float(c.get("quantidade") or 0),
                        "um": str(c.get("unidade_medida") or ""),
                        "cu": float(c.get("custo_unitario") or 0),
                        "ct": float(c.get("custo_total") or 0),
                    },
                )
    logger.info("ordens e consumos carregados.")


def main():
    try:
        load_produtos()
        load_receitas_e_itens()
        load_estoque()
        load_capacidade_turnos()
        load_ordens_e_consumos()
        logger.info("Carga completa.")
    except SQLAlchemyError as e:
        logger.error("Erro ao carregar dados: %s", e)
        raise


if __name__ == "__main__":
    main()
