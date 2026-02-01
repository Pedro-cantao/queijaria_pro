import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# -------------------------------------------------------------------
# Configuração inicial da página
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Queijaria Pro - Dashboard PCP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------
# Conexão com banco
# -------------------------------------------------------------------
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)

engine = get_engine()

# -------------------------------------------------------------------
# Funções auxiliares
# -------------------------------------------------------------------
def load_table(table_name: str) -> pd.DataFrame:
    """Tenta carregar uma tabela do banco, retorna DataFrame vazio se falhar."""
    try:
        with engine.connect() as conn:
            return pd.read_sql(text(f"SELECT * FROM {table_name}"), conn)
    except Exception as e:
        st.warning(f"Erro ao carregar tabela '{table_name}': {e}")
        return pd.DataFrame()

def kpi_card(title, value, delta=None, help_text=None):
    """Renderiza um KPI estilizado em card."""
    st.metric(label=title, value=value, delta=delta, help=help_text)

# -------------------------------------------------------------------
# Inicializa DataFrames (evita variáveis não definidas)
# -------------------------------------------------------------------
ordens_df = pd.DataFrame()
estoque_df = pd.DataFrame()
faltas_df = pd.DataFrame()
consumo_df = pd.DataFrame()
qualidade_df = pd.DataFrame()

# -------------------------------------------------------------------
# Layout principal
# -------------------------------------------------------------------
st.title("🧀 Queijaria Pro - Dashboard PCP")
st.markdown("### Painel de indicadores e dados de produção")

# KPIs principais
ordens_df = load_table("ordens_pcp")
estoque_df = load_table("estoque")
faltas_df = load_table("faltas_reserva")
consumo_df = load_table("consumo_energia")
qualidade_df = load_table("rejeicoes_qualidade")

if not ordens_df.empty or not faltas_df.empty or not qualidade_df.empty:
    col1, col2, col3, col4 = st.columns(4)

    total_ordens = len(ordens_df) if not ordens_df.empty else 0
    concluidas = (
        ordens_df[ordens_df["status"] == "concluida"].shape[0]
        if not ordens_df.empty else 0
    )
    total_faltas = len(faltas_df) if not faltas_df.empty else 0
    taxa_rejeicao = (
        qualidade_df["rejeitado"].mean() * 100
        if not qualidade_df.empty else 0
    )

    with col1:
        kpi_card("Total de Ordens", total_ordens)
    with col2:
        kpi_card("Ordens Concluídas", concluidas,
                 delta=f"{(concluidas/total_ordens):.0%}" if total_ordens > 0 else None)
    with col3:
        kpi_card("Faltas de Estoque", total_faltas)
    with col4:
        kpi_card("Taxa de Rejeição", f"{taxa_rejeicao:.1f}%")

# -------------------------------------------------------------------
# Seções detalhadas com visualização
# -------------------------------------------------------------------
if not estoque_df.empty:
    st.subheader("📦 Estoque")
    st.dataframe(estoque_df, use_container_width=True)

if not ordens_df.empty:
    st.subheader("📝 Ordens de Produção")
    st.dataframe(ordens_df, use_container_width=True)
    st.bar_chart(ordens_df["status"].value_counts())

if not faltas_df.empty:
    st.subheader("⚠️ Faltas de Estoque")
    st.dataframe(faltas_df, use_container_width=True)

if not consumo_df.empty:
    st.subheader("💡 Consumo de Energia")
    consumo_df["data"] = pd.to_datetime(consumo_df["data"])
    consumo_df = consumo_df.sort_values("data")
    st.line_chart(consumo_df.set_index("data")["kwh"])

if not qualidade_df.empty:
    st.subheader("🔍 Qualidade")
    st.dataframe(qualidade_df, use_container_width=True)

# -------------------------------------------------------------------
# Rodapé
# -------------------------------------------------------------------
st.markdown("---")
st.caption("Queijaria Pro • Simulação PCP • Dashboard Streamlit")
