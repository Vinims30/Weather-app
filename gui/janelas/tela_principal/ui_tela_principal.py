from qt_core import *
from gui.widgets.py_card import PyCardTempo
from gui.widgets.grafico import PyRainfallChart

class UI_TelaPrincipal(object):
    def setup_ui(self, parent):
        # Parametros Iniciais
        # //////////////////////////////////////////////////////
        parent.resize(1200, 750)
        parent.setMinimumSize(1100, 650)

        # Frame Central
        self.frame_central = QFrame()
        self.frame_central.setStyleSheet("background-color: #F0F4FF")

        # Main Layout
        self.layout_principal = QHBoxLayout(self.frame_central)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

    
        # 1. CONTEÚDO PRINCIPAL (Centro)
        # //////////////////////////////////////////////////////
        self.area_principal = QFrame()
        self.layout_area_principal = QVBoxLayout(self.area_principal)
        self.layout_area_principal.setContentsMargins(40, 30, 40, 30)
        self.layout_area_principal.setSpacing(10)

        # Cabeçalho 
        self.label_horario = QLabel("")
        self.label_horario.setStyleSheet("font-size: 45px; font-weight: bold; color: #5D99FF; background: transparent;")
        self.label_data = QLabel("")
        self.label_data.setStyleSheet("font-size: 14px; color: #88A0C0; font-weight: bold; background: transparent;")
        self.label_saudacao = QLabel("")
        self.label_saudacao.setStyleSheet("font-size: 26px; font-weight: 600; color: #5D99FF; margin-top: 10px; background: transparent;")

        self.layout_area_principal.addWidget(self.label_horario)
        self.layout_area_principal.addWidget(self.label_data)
        self.layout_area_principal.addWidget(self.label_saudacao)

        # Cards Semanais 
        self.container_cards = QWidget()
        self.layout_cards_semanais = QHBoxLayout(self.container_cards)
        self.layout_cards_semanais.setContentsMargins(0, 20, 0, 20)
        self.layout_cards_semanais.setSpacing(15)

        self.card_dom = PyCardTempo(dia="Dom", temp=28, icon_path="ensolarado.png")
        self.card_seg = PyCardTempo(dia="Seg", temp=17, icon_path="chovendo.png")
        self.card_ter = PyCardTempo(dia="Ter", temp=20, icon_path="nublado.png")
        self.card_qua = PyCardTempo(dia="Qua", temp=29, icon_path="trovoada.png")
        self.card_qui = PyCardTempo(dia="Qui", temp=22, icon_path="nublado.png")
        self.card_sex = PyCardTempo(dia="Sex", temp=17, icon_path="chovendo.png")
        self.card_sab = PyCardTempo(dia="Sab", temp=25, icon_path="ensolarado.png")

        for card in [self.card_dom, self.card_seg, self.card_ter, self.card_qua, self.card_qui, self.card_sex, self.card_sab]:
            self.layout_cards_semanais.addWidget(card)
        self.layout_cards_semanais.addStretch()

        self.layout_area_principal.addWidget(self.container_cards)

        # GRID DE DETALHES
        self.container_grid_detalhes = QWidget()
        self.layout_grid_detalhes = QGridLayout(self.container_grid_detalhes)
        self.layout_grid_detalhes.setSpacing(20)
        self.layout_grid_detalhes.setContentsMargins(0, 0, 0, 0)

        # Bloco Ar
        self.bloco_ar = self.criar_bloco_estilizado("Qualidade do Ar", "")
        self.label_cidade_ar = self.bloco_ar.findChildren(QLabel)[1]
        ar_content = QVBoxLayout()
        self.label_qualidade_ar = QLabel("Boa")
        self.label_qualidade_ar.setStyleSheet("color: #115742; font-weight: bold; font-size: 22px;")
        self.label_frase_ar = QLabel("Um ótimo dia para caminhar!")
        self.label_frase_ar.setStyleSheet("color: gray; font-size: 11px;")
        ar_content.addWidget(self.label_qualidade_ar)
        ar_content.addWidget(self.label_frase_ar)
        self.bloco_ar.layout().addLayout(ar_content, 1, 0, 1, 2)

        # Bloco Sol
        self.bloco_sol = self.criar_bloco_estilizado("Sunrise & Sunset", "")
        self.label_cidade_sol = self.bloco_sol.findChildren(QLabel)[1]
        sol_content = QVBoxLayout()
        self.label_nascer_sol = QLabel("☀️ Nascer: 05:40 AM")   # ← guardar referência
        self.label_por_sol = QLabel("🌙 Pôr do Sol: 18:32 PM")  # ← guardar referência
        sol_content.addWidget(self.label_nascer_sol)
        sol_content.addWidget(self.label_por_sol)
        self.bloco_sol.layout().addLayout(sol_content, 1, 0, 1, 2)

        # Bloco Chuva
        self.bloco_chuva = self.criar_bloco_estilizado("Umidade Semanal (%)", "")
        self.label_subtitulo_chuva = self.bloco_chuva.findChildren(QLabel)[1]
        self.grafico_chuva = PyRainfallChart()
        self.bloco_chuva.layout().addWidget(self.grafico_chuva, 1, 0, 1, 2)

        self.layout_grid_detalhes.addWidget(self.bloco_ar, 0, 0)
        self.layout_grid_detalhes.addWidget(self.bloco_sol, 0, 1)
        self.layout_grid_detalhes.addWidget(self.bloco_chuva, 1, 0, 1, 2)

        self.layout_area_principal.addWidget(self.container_grid_detalhes)
        self.layout_area_principal.addStretch()


        # 2. BARRA LATERAL DIREITA
        # //////////////////////////////////////////////////////
        self.barra_lateral_direita = QFrame()
        self.barra_lateral_direita.setFixedWidth(350)

        self.barra_lateral_direita.setStyleSheet("""
            QFrame {
                background-color: #F8FAFF; 
                border-left: 1px solid #E0E8F5;
                border-right: none;
                border-top: none;
                border-bottom: none;
            }
        """)
        
        self.layout_barra_lateral_direita = QVBoxLayout(self.barra_lateral_direita)
        self.layout_barra_lateral_direita.setContentsMargins(25, 30, 25, 30)
        self.layout_barra_lateral_direita.setSpacing(20)

        # Campo de Pesquisa
        self.campo_pesquisa = QLineEdit()
        self.campo_pesquisa.setPlaceholderText("Pesquisar...")
        self.campo_pesquisa.setFixedHeight(45)
        self.campo_pesquisa.setStyleSheet("""
            QLineEdit {
                background-color: white; 
                border: 1px solid #E0E8F5; 
                border-radius: 15px; 
                padding-left: 15px;
                color: #5D99FF;
            }
        """)
        self.layout_barra_lateral_direita.addWidget(self.campo_pesquisa)

        # CARD HOJE
        self.card_hoje = QFrame()
        self.card_hoje.setFixedHeight(450)
        self.card_hoje.setObjectName("CardHoje")
        
        self.card_hoje.setStyleSheet("""
            #CardHoje { 
                background-color: #7DA2FF; 
                border-radius: 30px; 
                border: none;
            }
            QLabel { 
                color: white; 
                border: none;
                background: transparent;
            }
        """)
        
        self.layout_card_hoje = QVBoxLayout(self.card_hoje)
        self.layout_card_hoje.setContentsMargins(30, 40, 30, 30)
        self.layout_card_hoje.setSpacing(0)
        
        # Alinhamento do Nome da Cidade e Data
        self.label_cidade_hoje = QLabel("São Paulo")
        self.label_cidade_hoje.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 2px;")
        self.label_cidade_hoje.setAlignment(Qt.AlignCenter)
        
        self.label_dia_mes_hoje = QLabel("Hoje, 1 de março") 
        self.label_dia_mes_hoje.setStyleSheet("font-size: 14px; color: rgba(255, 255, 255, 0.8);")
        self.label_dia_mes_hoje.setAlignment(Qt.AlignCenter)
        
        # Ícone do Tempo
        self.label_icon_hoje = QLabel()
        self.label_icon_hoje.setAlignment(Qt.AlignCenter)
        
        # Temperatura
        self.label_temp_hoje = QLabel("25°")
        self.label_temp_hoje.setStyleSheet("font-size: 85px; font-weight: bold; margin-bottom: 10px;")
        self.label_temp_hoje.setAlignment(Qt.AlignCenter)

        # INFORMAÇÕES EXTRAS (Vento e Humidade)
        # Usamos um QFrame apenas para organizar, com fundo transparente para não criar a caixa branca
        self.container_extras_hoje = QFrame()
        self.container_extras_hoje.setStyleSheet("background: transparent; border: none;")
        self.layout_extras = QHBoxLayout(self.container_extras_hoje)
        self.layout_extras.setContentsMargins(0, 10, 0, 0)

        # Criando labels com cores sólidas para garantir visibilidade
        self.label_vento_hoje = QLabel("Vento: 15 km/h")
        self.label_vento_hoje.setStyleSheet("font-size: 13px; font-weight: 500; color: white;")
        
        self.label_humidade_hoje = QLabel("Hum: 62%")
        self.label_humidade_hoje.setStyleSheet("font-size: 13px; font-weight: 500; color: white;")

        self.layout_extras.addWidget(self.label_vento_hoje)
        self.layout_extras.addStretch()
        self.layout_extras.addWidget(self.label_humidade_hoje)

        # Adicionando tudo ao layout do card na ordem correta
        self.layout_card_hoje.addWidget(self.label_cidade_hoje)
        self.layout_card_hoje.addWidget(self.label_dia_mes_hoje)
        self.layout_card_hoje.addStretch()
        self.layout_card_hoje.addWidget(self.label_icon_hoje)
        self.layout_card_hoje.addStretch()
        self.layout_card_hoje.addWidget(self.label_temp_hoje)
        self.layout_card_hoje.addWidget(self.container_extras_hoje)
        
        self.layout_barra_lateral_direita.addWidget(self.card_hoje)
        self.layout_barra_lateral_direita.addStretch()

        # Adicionando tudo ao layout principal com proporções (Stretch)
        self.layout_principal.addWidget(self.area_principal, stretch=3)
        self.layout_principal.addWidget(self.barra_lateral_direita, stretch=1)

        parent.setCentralWidget(self.frame_central)

    def criar_bloco_estilizado(self, titulo, subtitulo):
        bloco = QFrame()
        bloco.setStyleSheet("background-color: white; border-radius: 20px;")
        layout = QGridLayout(bloco)
        layout.setContentsMargins(20, 15, 20, 15)
        
        t = QLabel(titulo)
        t.setStyleSheet("color: #2D3748; font-weight: bold; font-size: 13px; background: transparent;")
        s = QLabel(subtitulo)
        s.setStyleSheet("color: #A0AEC0; font-size: 11px; background: transparent;")
        
        layout.addWidget(t, 0, 0, Qt.AlignLeft)
        layout.addWidget(s, 0, 1, Qt.AlignRight)
        return bloco