import csv
import os
from datetime import datetime
from extract_api1 import get_weather
from extract_api2 import get_air_quality

# Entrada da cidade
cidade = input("Digite o nome da cidade: ")

# Buscar dados
weather = get_weather(cidade)
air_quality = get_air_quality(cidade)

# Data e hora da coleta
coleta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Cabeçalho base
cabecalho_base = [
    "Data_Coleta", "Cidade", "Local OpenAQ", "País OpenAQ",
    "Temperatura (°C)", "Sensação térmica (°C)", "Temp mínima (°C)", "Temp máxima (°C)",
    "Umidade (%)", "Pressão atmosférica (hPa)", "Descrição clima"
]

# Dados base
dados_base = [
    coleta,
    cidade,
    "N/A", "N/A",  # Local e País padrão
    weather["temperatura"], weather["sensacao_termica"], weather["temp_min"],
    weather["temp_max"], weather["humidade"], weather["pressao_atm"], weather["descricao"]
]

# Cabeçalho e dados extras da qualidade do ar
cabecalho_extra = []
dados_extra = []
if air_quality:
    for aq in air_quality:
        parametro = aq["parametro"].replace(" ", "_").replace("/", "_")
        cabecalho_extra.extend([f"{parametro} Valor", f"{parametro} Unidade"])
        dados_extra.extend([aq["valor"], aq["unidade"]])
else:
    cabecalho_extra.extend(["Parâmetro", "Valor", "Unidade"])
    dados_extra.extend(["N/A", "N/A", "N/A"])

# Cabeçalho final e dados finais
cabecalho_final = cabecalho_base + cabecalho_extra
dados_linha = dados_base + dados_extra

# Nome do arquivo CSV
arquivo_csv = "clima_qualidade_ar.csv"
arquivo_existe = os.path.isfile(arquivo_csv)

# Salvar incrementalmente
with open(arquivo_csv, mode="a", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    if not arquivo_existe:
        writer.writerow(cabecalho_final)  # escreve cabeçalho apenas na primeira vez
    writer.writerow(dados_linha)

print(f"✅ Dados salvos/atualizados em {arquivo_csv}")
