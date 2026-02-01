from sqlalchemy import create_engine

# String de conexão usando pg8000
DATABASE_URL = "postgresql+pg8000://admin:admin@localhost:5432/queijaria"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute("SELECT version();")
        print("Conexão OK:", result.fetchone())
except Exception as e:
    print("Erro de conexão:", repr(e))
