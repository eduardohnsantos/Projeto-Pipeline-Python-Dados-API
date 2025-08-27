import requests
import os
from dotenv import load_dotenv
from tabulate import tabulate
from extract_api2 import get_air_quality  # importa a função do outro script

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(cidade):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={OPENWEATHER_API_KEY}&lang=pt_br"
    res = requests.get(url).json()

    if "main" not in res:
        return {"erro": res.get("message", "Não foi possível obter os dados.")}

    return {
        "cidade": res["name"],
        "pais": res["sys"]["country"],
        "temperatura": f"{round(res['main']['temp'] - 273.15, 1)} °C",
        "sensacao_termica": f"{round(res['main']['feels_like'] - 273.15, 1)} °C",
        "temp_min": f"{round(res['main']['temp_min'] - 273.15, 1)} °C",
        "temp_max": f"{round(res['main']['temp_max'] - 273.15, 1)} °C",
        "humidade": f"{res['main']['humidity']}%",
        "pressao_atm": f"{res['main']['pressure']} hPa",
        "vento": f"{res['wind']['speed']} m/s",
        "descricao": res['weather'][0]['description'].capitalize()
    }

if __name__ == "__main__":
    cidade = input("Digite o nome da cidade: ")

    # Chama clima
    clima = get_weather(cidade)

    # Chama qualidade do ar
    qualidade_ar = get_air_quality(cidade)

    # --- Tabela do Clima ---
    print("\n--- Dados do Clima ---")
    if "erro" in clima:
        print("⚠️", clima["erro"])
    else:
        clima_table = [[k, v] for k, v in clima.items()]
        print(tabulate(clima_table, headers=["Parâmetro", "Valor"], tablefmt="grid"))

    # --- Tabela da Qualidade do Ar ---
    print("\n--- Qualidade do Ar ---")
    if not qualidade_ar:
        print("⚠️ Não há dados de qualidade do ar disponíveis.")
    else:
        ar_table = [
            [dado["parametro"], dado["valor"], dado["unidade"], dado["local"]]
            for dado in qualidade_ar
        ]
        print(tabulate(ar_table, headers=["Parâmetro", "Valor", "Unidade", "Local"], tablefmt="grid"))
