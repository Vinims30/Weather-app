from qt_core import *
from services.weather_service import WeatherService
import requests

class WeatherWorker(QThread):
    # Sinais emitidos de volta para a UI
    dados_prontos = Signal(dict)       # Emitido quando tudo deu certo
    erro_ocorrido = Signal(str)        # Emitido quando algo falhou

    def __init__(self, cidade):
        super().__init__()
        self.cidade = cidade
        self.service = WeatherService()

    def run(self):
        # Esse método roda em segundo plano — nunca trava a UI
        try:
            dados = self.service.buscar_todos_dados(self.cidade)
            self.dados_prontos.emit(dados)   # Avisa que terminou com sucesso
        except requests.exceptions.ConnectionError:
            self.erro_ocorrido.emit("Sem conexão com a internet.")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                self.erro_ocorrido.emit(f"Cidade '{self.cidade}' não encontrada.")
            else:
                self.erro_ocorrido.emit(f"Erro na API: {e}")
        except Exception as e:
            self.erro_ocorrido.emit(f"Erro inesperado: {e}")