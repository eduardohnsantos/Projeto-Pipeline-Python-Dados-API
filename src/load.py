import csv
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# --- Caminho do .env na raiz do projeto ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT_DIR, ".env")

# Carrega o .env com encoding UTF-8
if not os.path.exists(ENV_PATH):
    raise FileNotFoundError(f".env não encontrado em {ENV_PATH}")
load_dotenv(dotenv_path=ENV_PATH, encoding="utf-8")

# --- Variáveis de conexão ---
DB_HOST = os.getenv("DB_HOST").strip()
DB_NAME = os.getenv("DB_NAME").strip()
DB_USER = os.getenv("DB_USER").strip()
DB_PASS = os.getenv("DB_PASS").strip()
DB_PORT = int(os.getenv("DB_PORT", 5432))

# --- Arquivo CSV e tabela ---
ARQUIVO_CSV = os.path.join(os.path.dirname(__file__), "clima_qualidade_ar.csv")
TABELA = "clima_qualidade_ar"

# --- Conexão com PostgreSQL ---
conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    port=DB_PORT
)
cur = conn.cursor()


# --- Inserir dados do CSV incrementalmente ---
with open(ARQUIVO_CSV, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Adiciona timestamp da coleta
        row["data_coleta"] = datetime.now()

        # Colunas e valores
        cols = ', '.join([f'"{col}"' for col in row.keys()])
        vals = ', '.join([f"%({col})s" for col in row.keys()])

        # INSERT incremental (evita duplicatas)
        insert_query = f"""
        INSERT INTO {TABELA} ({cols})
        VALUES ({vals})
        ON CONFLICT (cidade, data_coleta) DO NOTHING;
        """
        cur.execute(insert_query, row)

conn.commit()
cur.close()
conn.close()

print(f"✅ Dados carregados incrementalmente para a tabela {TABELA}")
