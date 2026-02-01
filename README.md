# 🧀 Queijaria Pro

> Simulação de um sistema **PCP (Planejamento e Controle da Produção)** aplicado a uma queijaria industrial, com geração de dados sintéticos, ETL completo, banco de dados relacional e dashboard analítico.

---

## 📌 Visão Geral

O **Queijaria Pro** é um projeto voltado para **análise de dados industriais, automação e tomada de decisão** em ambientes de produção de laticínios.

O sistema simula operações reais de uma queijaria, incluindo:

- Produção
- Estoques
- Manutenção
- IoT
- Consumo energético
- Qualidade
- Falhas e restrições operacionais

Os dados são processados por um **pipeline ETL**, armazenados em **PostgreSQL** e consumidos via **Streamlit** ou **SQL** para análise de KPIs.

---

## 🎯 Objetivos do Projeto

- Simular:
  - Catálogo de produtos
  - Receitas (BOM)
  - Estoque e reservas
  - Ordens de produção (PCP)
  - Consumos de materiais
- Gerar eventos industriais:
  - Manutenções programadas e corretivas
  - Leituras IoT
  - Consumo energético
  - Rejeições de qualidade
- Automatizar:
  - Reserva de estoque
  - Identificação de faltas
- Disponibilizar:
  - KPIs operacionais
  - Views analíticas
  - Dashboard interativo

---

## 🗂️ Estrutura do Projeto

queijaria_pro/
├── data/
│ ├── raw/ # Backups brutos
│ └── clean/ # Dados tratados
│
├── docker/
│ └── postgres/
│ └── initdb/
│ └── ddl_pcp.sql # DDL inicial do banco
│
├── src/
│ ├── backend/
│ │ └── etl/
│ │ ├── geradores/ # Geração de dados sintéticos
│ │ │ ├── gerar_receitas.py
│ │ │ ├── gerar_estoque.py
│ │ │ ├── gerar_capacidade_turnos.py
│ │ │ ├── gerar_ordens_pcp.py
│ │ │ ├── gerar_logs_iot.py
│ │ │ ├── gerar_faltas_estoque.py
│ │ │ ├── gerar_eventos_manutencao.py
│ │ │ ├── gerar_consumo_energia.py
│ │ │ ├── gerar_rejeicoes_qualidade.py
│ │ │ └── gerar_backup_cenarios.py
│ │ │
│ │ ├── utils/
│ │ │ ├── init.py
│ │ │ └── core.py
│ │ │
│ │ ├── extract.py
│ │ ├── transform.py
│ │ ├── reserve_stock.py
│ │ ├── load.py
│ │ ├── etl.py
│ │ └── flows/
│ │ └── prefect_flow.py
│ │
│ └── frontend/
│ └── app.py # Dashboard Streamlit
│
├── scripts/
│ └── check_db.py # Verificação rápida do banco
│
├── requirements.txt
├── docker-compose.yml
└── README.md


---

## 🧠 Responsabilidades dos Módulos

| Módulo | Função |
|------|------|
| `geradores/` | Criação de CSVs sintéticos |
| `extract.py` | Backup dos dados brutos e leitura segura |
| `transform.py` | Validação, normalização e limpeza |
| `reserve_stock.py` | Reserva automática e detecção de faltas |
| `load.py` | Insert / Upsert idempotente no PostgreSQL |
| `etl.py` | Orquestração completa do ETL |
| `frontend/app.py` | Dashboard de KPIs em Streamlit |
| `scripts/check_db.py` | Diagnóstico rápido do banco |

---

## ⚙️ Pré-requisitos

- Python **3.10+**
- Docker e Docker Compose *(opcional)*
- Ambiente virtual Python (recomendado)

---

## 📦 Instalação

### 1️⃣ Criar ambiente virtual

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
