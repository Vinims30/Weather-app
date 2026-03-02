import requests
import os
from dotenv import load_dotenv

load_dotenv()  

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"

        if not self.api_key:
            raise ValueError("Chave da API não encontrada! Verifique seu arquivo .env")

    def buscar_todos_dados(self, cidade):
        clima = self._buscar_clima_atual(cidade)
        lat = clima["coord"]["lat"]
        lon = clima["coord"]["lon"]
        previsao = self._buscar_previsao(cidade)
        ar = self._buscar_qualidade_ar(lat, lon)
        nascer_sol = clima["sys"]["sunrise"]
        por_do_sol = clima["sys"]["sunset"]

        return {
            "clima_atual": clima,
            "previsao": previsao,
            "qualidade_ar": ar,
            "nascer_sol": nascer_sol,
            "por_do_sol": por_do_sol,
        }

    def _buscar_clima_atual(self, cidade):
        return self._get(f"{self.base_url}/weather", {
            "q": cidade, "units": "metric", "lang": "pt_br"
        })

    def _buscar_previsao(self, cidade):
        return self._get(f"{self.base_url}/forecast", {
            "q": cidade, "units": "metric", "lang": "pt_br"
        })

    def _buscar_qualidade_ar(self, lat, lon):
        return self._get(f"{self.base_url}/air_pollution", {
            "lat": lat, "lon": lon
        })

    def _get(self, url, params):
        params["appid"] = self.api_key
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()