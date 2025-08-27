import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")

def get_air_quality(cidade):
    headers = {"X-API-Key": OPENAQ_API_KEY}
    url = f"https://api.openaq.org/v3/latest?city={cidade}"
    res = requests.get(url, headers=headers).json()

    air_data = []
    if "results" in res and res["results"]:
        for local in res["results"]:
            local_name = local['location']
            country = local['country']
            for pol in local["measurements"]:
                air_data.append({
                    "local": local_name,
                    "pais": country,
                    "parametro": pol["parameter"],
                    "valor": pol["value"],
                    "unidade": pol["unit"]
                })
    return air_data
