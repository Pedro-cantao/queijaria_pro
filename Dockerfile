 # Dockerfile
FROM python:3.12-slim

# Evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
ARG APP_USER=appuser
ARG APP_HOME=/app
RUN useradd --create-home --shell /bin/bash $APP_USER
WORKDIR $APP_HOME

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Ajustar permissões
RUN chown -R $APP_USER:$APP_USER $APP_HOME
USER $APP_USER

# Variável para apontar para pasta de dados (montada via volume)
ENV DATA_DIR=/app/data

# Porta padrão para Streamlit (frontend)
EXPOSE 8501

# Comando padrão (pode ser sobrescrito no docker-compose)
CMD ["python", "src/backend/etl/load.py"]
