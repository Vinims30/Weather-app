import sys
import os
import requests
from datetime import datetime
from collections import defaultdict

from qt_core import *
from gui.janelas.tela_principal.ui_tela_principal import UI_TelaPrincipal
from services.weather_worker import WeatherWorker


class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")

        self.ui = UI_TelaPrincipal()
        self.ui.setup_ui(self)

        self.worker = None  # Guarda referência ao worker ativo

        # Timer do relógio
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_tempo)
        self.timer.start(1000)
        self.atualizar_tempo()

        self.atualizar_icone_destaque("ensolarado.png")
        self.destacar_dia_atual()

        # Conecta a pesquisa
        self.ui.campo_pesquisa.returnPressed.connect(self.pesquisar_cidade)

        # Carrega cidade padrão ao iniciar
        self.iniciar_busca("São Paulo")

        self.show()

    # -------------------------------------------------------
    # PESQUISA
    # -------------------------------------------------------
    def pesquisar_cidade(self):
        cidade = self.ui.campo_pesquisa.text().strip()
        if cidade:
            self.iniciar_busca(cidade)

    def iniciar_busca(self, cidade):
        # Cancela worker anterior se ainda estiver rodando
        if self.worker and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()

        # Feedback visual enquanto carrega
        self.ui.label_cidade_hoje.setText("Carregando...")
        self.ui.label_temp_hoje.setText("--°")

        # Cria e inicia o worker em background
        self.worker = WeatherWorker(cidade)
        self.worker.dados_prontos.connect(self.atualizar_interface)
        self.worker.erro_ocorrido.connect(self.mostrar_erro)
        self.worker.start()

    # -------------------------------------------------------
    # ATUALIZAÇÃO DA INTERFACE
    # -------------------------------------------------------
    def atualizar_interface(self, dados):
        clima = dados["clima_atual"]
        previsao = dados["previsao"]
        ar = dados["qualidade_ar"]

        # Card principal
        self.ui.label_cidade_hoje.setText(clima["name"])
        self.ui.label_temp_hoje.setText(f'{round(clima["main"]["temp"])}°')
        self.ui.label_vento_hoje.setText(f'Vento: {round(clima["wind"]["speed"])} km/h')
        self.ui.label_humidade_hoje.setText(f'Hum: {clima["main"]["humidity"]}%')

        # Ícone do tempo
        icone_local = self.mapear_icone(clima["weather"][0]["icon"])
        self.atualizar_icone_destaque(icone_local)

        # Qualidade do ar
        aqi = ar["list"][0]["main"]["aqi"]
        textos_ar  = {1: "Boa", 2: "Regular", 3: "Moderada", 4: "Ruim", 5: "Péssima"}
        frases_ar  = {
            1: "Ótimo dia para caminhar!",
            2: "Relativamente seguro.",
            3: "Atenção para grupos sensíveis.",
            4: "Evite atividades ao ar livre.",
            5: "Permaneça em ambientes fechados.",
        }
        cores_ar = {
            1: "#115742", 2: "#7D6608", 3: "#784212",
            4: "#7B241C",  5: "#4A235A",
        }
        self.ui.label_qualidade_ar.setText(textos_ar.get(aqi, "N/A"))
        self.ui.label_qualidade_ar.setStyleSheet(
            f"color: {cores_ar.get(aqi, 'gray')}; font-weight: bold; font-size: 22px;"
        )
        self.ui.label_frase_ar.setText(frases_ar.get(aqi, ""))

        # Sunrise & Sunset
        nascer = datetime.fromtimestamp(dados["nascer_sol"]).strftime("%I:%M %p")
        por    = datetime.fromtimestamp(dados["por_do_sol"]).strftime("%I:%M %p")
        
        # Atualiza os labels do bloco sol
        labels_sol = self.ui.bloco_sol.findChildren(QLabel)
        for lbl in labels_sol:
            if "Nascer" in lbl.text():
                lbl.setText(f"☀️ Nascer: {nascer}")
            elif "Pôr" in lbl.text():
                lbl.setText(f"🌙 Pôr do Sol: {por}")

        # Cards da semana
        self.atualizar_cards_semana(previsao)

        # Gráfico de humidade
        self.atualizar_grafico(previsao)

        cidade_nome = clima["name"]
        self.ui.label_cidade_ar.setText(cidade_nome)
        self.ui.label_cidade_sol.setText(cidade_nome)
        self.ui.label_subtitulo_chuva.setText(cidade_nome)

    def atualizar_cards_semana(self, previsao):
        dias = defaultdict(list)
        for item in previsao["list"]:
            data = item["dt_txt"].split(" ")[0]
            dias[data].append(item)

        # weekday(): 0=Seg, 1=Ter, 2=Qua, 3=Qui, 4=Sex, 5=Sab, 6=Dom
        mapa_cards = {
            0: self.ui.card_seg,
            1: self.ui.card_ter,
            2: self.ui.card_qua,
            3: self.ui.card_qui,
            4: self.ui.card_sex,
            5: self.ui.card_sab,
            6: self.ui.card_dom,
        }
        nomes_pt = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]

        # 1. Reseta TODOS os cards primeiro
        for dia_idx, card in mapa_cards.items():
            card.atualizar_dados(nomes_pt[dia_idx], "--", "nublado.png")

        # 2. Preenche apenas os dias que a API retornou
        for data, itens in dias.items():
            item_dia = min(itens, key=lambda x: abs(
                datetime.strptime(x["dt_txt"], "%Y-%m-%d %H:%M:%S").hour - 12
            ))
            temp = round(item_dia["main"]["temp"])
            icone = self.mapear_icone(item_dia["weather"][0]["icon"])
            dia_semana = datetime.strptime(data, "%Y-%m-%d").weekday()

            card = mapa_cards.get(dia_semana)
            if card:
                card.atualizar_dados(nomes_pt[dia_semana], temp, icone)

        # 3. Reaplicar destaque do dia atual
        self.destacar_dia_atual()

    def atualizar_grafico(self, previsao):
        dias = defaultdict(list)
        for item in previsao["list"]:
            data = item["dt_txt"].split(" ")[0]
            dias[data].append(item["main"]["humidity"])

        # Lista de humidades médias por dia + lista de nomes dos dias
        humidades = []
        nomes_dias = []
        nomes_pt = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]

        for data, vals in list(dias.items())[:7]:
            humidades.append(round(sum(vals) / len(vals)))
            dia_semana = datetime.strptime(data, "%Y-%m-%d").weekday()  
            nomes_dias.append(nomes_pt[dia_semana])

    
        self.ui.grafico_chuva.days = nomes_dias
        self.ui.grafico_chuva.update_data(humidades)

    # -------------------------------------------------------
    # ERRO
    # -------------------------------------------------------
    def mostrar_erro(self, mensagem):
        self.ui.label_cidade_hoje.setText("Erro")
        self.ui.label_temp_hoje.setText("--°")

        msg = QMessageBox(self)
        msg.setWindowTitle("Erro ao buscar dados")
        msg.setText(mensagem)
        msg.setIcon(QMessageBox.Warning)
        msg.exec()

    # -------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------
    def mapear_icone(self, codigo_api):
        mapa = {
            # Céu limpo
            "01d": "ensolarado.png",
            "01n": "ensolarado.png",

            # Poucas nuvens
            "02d": "nublado.png",
            "02n": "nublado.png",

            # Nuvens dispersas
            "03d": "nublado.png",
            "03n": "nublado.png",

            # Nublado fechado
            "04d": "nublado.png",
            "04n": "nublado.png",

            # Chuva leve/garoa
            "09d": "chovendo.png",
            "09n": "chovendo.png",

            # Chuva moderada
            "10d": "chovendo.png",
            "10n": "chovendo.png",

            # Trovoada
            "11d": "trovoada.png",
            "11n": "trovoada.png",

            # Neve 
            "13d": "nevando.png",
            "13n": "nevando.png",

            # Névoa/neblina/fumaça
            "50d": "nublado.png",
        "   50n": "nublado.png",
    }
        return mapa.get(codigo_api, "nublado.png")
    
    def atualizar_tempo(self):
        agora = QDateTime.currentDateTime()
        hora_atual = agora.time().hour()
        local = QLocale(QLocale.Portuguese, QLocale.Brazil)

        self.ui.label_horario.setText(agora.toString("hh:mm AP"))

        # ← Correção: monta a string manualmente para evitar duplicação
        dia_num = agora.date().day()
        mes_nome = local.toString(agora.date(), "MMMM")  # só o nome do mês
        self.ui.label_dia_mes_hoje.setText(f"Hoje, {dia_num} de {mes_nome}")

        data_texto = local.toString(agora, "dddd, d 'de' MMMM, yyyy").capitalize()
        self.ui.label_data.setText(data_texto)

        if 5 <= hora_atual < 12:
            saudacao = "Bom Dia!"
        elif 12 <= hora_atual < 18:
            saudacao = "Boa Tarde!"
        else:
            saudacao = "Boa Noite!"
        self.ui.label_saudacao.setText(saudacao)

    def atualizar_icone_destaque(self, nome_icone):
        app_path = os.path.abspath(os.getcwd())
        full_path = os.path.normpath(
            os.path.join(app_path, "gui/images/icons", nome_icone)
        )
        if os.path.exists(full_path):
            pixmap = QPixmap(full_path).scaled(
                110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.ui.label_icon_hoje.setPixmap(pixmap)
            self.ui.label_icon_hoje.setAlignment(Qt.AlignCenter)

    def destacar_dia_atual(self):
        dia_semana = QDate.currentDate().dayOfWeek()
        mapa_cards = {
            1: self.ui.card_seg, 2: self.ui.card_ter, 3: self.ui.card_qua,
            4: self.ui.card_qui, 5: self.ui.card_sex, 6: self.ui.card_sab,
            7: self.ui.card_dom
        }
        for card in mapa_cards.values():
            card.atualizar_estilo(False)
        card_hoje = mapa_cards.get(dia_semana)
        if card_hoje:
            card_hoje.atualizar_estilo(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela = TelaPrincipal()
    sys.exit(app.exec())