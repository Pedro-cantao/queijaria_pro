Queijaria Pro README
Visão geral
Queijaria Pro é um projeto de simulação de um sistema PCP (Planejamento e Controle da Produção) para uma queijaria. Gera dados sintéticos, transforma e carrega em PostgreSQL, simula cenários operacionais (faltas, manutenção, IoT, consumo energético, rejeições) e expõe KPIs via frontend (Streamlit) ou consultas SQL.

Objetivos

Simular catálogo de produtos, receitas (BOM), estoque, ordens de produção e consumos.

Gerar eventos de manutenção, leituras IoT, consumo energético e amostras de qualidade.

Reservar automaticamente estoque para ordens e reportar faltas.

Disponibilizar views de KPI para análise e dashboard.

Estrutura do projeto
Código
queijaria_pro/
├── data/
│   ├── raw/
│   └── clean/
├── docker/postgres/initdb/ddl_pcp.sql
├── src/backend/etl/
│   ├── geradores/
│   │   ├── gerar_receitas.py
│   │   ├── gerar_estoque.py
│   │   ├── gerar_capacidade_turnos.py
│   │   ├── gerar_ordens_pcp.py
│   │   ├── gerar_dados.py
│   │   ├── gerar_logs_iot.py
│   │   ├── gerar_faltas_estoque.py
│   │   ├── gerar_eventos_manutencao.py
│   │   ├── gerar_consumo_energia.py
│   │   ├── gerar_rejeicoes_qualidade.py
│   │   └── gerar_backup_cenarios.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── core.py
│   ├── extract.py
│   ├── transform.py
│   ├── reserve_stock.py
│   ├── load.py
│   ├── etl.py
│   └── flows/
│       └── prefect_flow.py
├── src/frontend/app.py
├── scripts/check_db.py
├── requirements.txt
├── docker-compose.yml
└── README.md
Principais responsabilidades

geradores/: criar CSVs sintéticos em data/.

extract.py: backup raw e leitura segura.

transform.py: validação e normalização; grava em data/clean/.

reserve_stock.py: reserva automática e relatório de faltas.

load.py: inserção/upsert idempotente no Postgres.

etl.py: orquestrador (backup → extract → transform → reserve → load).

frontend/app.py: dashboard Streamlit com KPIs.

scripts/check_db.py: verificação rápida do banco.

Pré requisitos e instalação
Requisitos

Python 3.10+

Docker e Docker Compose (opcional)

Ambiente virtual recomendado

Instalação

bash
python -m venv venv
# Unix
source venv/bin/activate
# Windows PowerShell
# venv\Scripts\Activate.ps1

pip install -r requirements.txt
Variáveis de ambiente

DATABASE_URL (exemplo):
postgresql+psycopg2://admin:admin@localhost:5432/queijaria

Use .env para desenvolvimento se desejar.

Como rodar
1. Gerar dados

bash
python src/backend/etl/geradores/gerar_receitas.py
python src/backend/etl/geradores/gerar_estoque.py
python src/backend/etl/geradores/gerar_capacidade_turnos.py
python src/backend/etl/geradores/gerar_ordens_pcp.py
# geradores opcionais
python src/backend/etl/geradores/gerar_logs_iot.py
python src/backend/etl/geradores/gerar_faltas_estoque.py
python src/backend/etl/geradores/gerar_eventos_manutencao.py
python src/backend/etl/geradores/gerar_consumo_energia.py
python src/backend/etl/geradores/gerar_rejeicoes_qualidade.py
python src/backend/etl/geradores/gerar_backup_cenarios.py
2. Subir Postgres com Docker Compose (opcional)

bash
docker-compose up --build -d
Observação: scripts em docker/postgres/initdb/ executam apenas na primeira inicialização do volume.

3. Executar ETL

bash
# recomendado (garante imports relativos)
python -m src.backend.etl.etl
4. Verificar banco

bash
export DATABASE_URL="postgresql+psycopg2://admin:admin@localhost:5432/queijaria"
python scripts/check_db.py
5. Rodar frontend

bash
streamlit run src/frontend/app.py
Acesse http://localhost:8501.

Troubleshooting e próximos passos
Problemas comuns

ModuleNotFoundError utils: verifique src/backend/etl/utils/__init__.py e rode o ETL como módulo (python -m src.backend.etl.etl) ou ajuste PYTHONPATH=src.

DDL não executado no container: remova o volume Postgres se precisar reexecutar os scripts de init.

Permissões/CRLF: em Windows, converta arquivos SQL para LF se houver erro.

Relatórios e artefatos

Backups brutos: data/raw/ (timestamp).

Arquivos limpos: data/clean/.

Relatório de faltas de reserva: data/faltas_reserva_report.csv.

Melhorias sugeridas

Integrar Alembic para migrações de schema.

Agendar ETL com Prefect ou cron em container etl_runner.

Persistir séries temporais em TimescaleDB/InfluxDB para dados IoT.

Adicionar testes com pytest e CI.

Comandos úteis resumidos
bash
# ativar venv e instalar
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# gerar dados
python src/backend/etl/geradores/gerar_receitas.py

# rodar ETL
python -m src.backend.etl.etl

# checar DB
python scripts/check_db.py

# rodar frontend
streamlit run src/frontend/app.py