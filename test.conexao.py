import psycopg2

# Digite manualmente a senha sem copiar de outro lugar
senha = "Edja271529@@"  # digite exatamente aqui

conn = psycopg2.connect(
    host="localhost",
    dbname="clima_tempo",
    user="postgres",
    password=senha,
    port=5432
)
print("✅ Conexão OK!")
conn.close()
