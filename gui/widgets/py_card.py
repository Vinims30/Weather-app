from qt_core import *
import os

class PyCardTempo(QFrame):
    def __init__(self,dia,temp,icon_path,is_active = False):
        super().__init__()

        #Configuracoes Iniciais
        self.setObjectName("CardDeTempo")
        self.icon_path = icon_path
        self.icon_pixmap = None
        self.set_icon_pixmap()
        self.setFixedSize(90, 160)

        #Layout Interno
        self.layout_card = QVBoxLayout(self)
        self.layout_card.setContentsMargins(10, 15, 10, 15)
        self.layout_card.setSpacing(10)
        self.layout_card.setAlignment(Qt.AlignCenter)

        #Elementos: Dia
        self.label_dia = QLabel(dia)
        self.label_dia.setStyleSheet("font-weight: 500; font-size: 14px;background: transparent;")
        self.label_dia.setAlignment(Qt.AlignCenter)

        #Elementos: Icon
        self.label_icon = QLabel()
        self.label_icon.setFixedSize(50, 50)
        self.label_icon.setAlignment(Qt.AlignCenter)
        self.label_icon.setStyleSheet("background: transparent;")

        if self.icon_pixmap:
            # Redimensiona o pixmap para o tamanho do label com suavização
            scaled_icon = self.icon_pixmap.scaled(
                45, 45, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.label_icon.setPixmap(scaled_icon)

        #Elementos: Temperatura
        self.label_temp = QLabel(f"{temp}°")
        self.label_temp.setStyleSheet("font-weight: bold; font-size: 18px; background: transparent;")
        self.label_temp.setAlignment(Qt.AlignCenter)

        # Adicionando ao layout
        self.layout_card.addWidget(self.label_icon)
        self.layout_card.addWidget(self.label_dia)
        self.layout_card.addWidget(self.label_temp)

        self.atualizar_estilo(is_active)
    
    def set_icon_pixmap(self):
        #Carrega e prepara o ícone para evitar processamento no paintEvent
        if self.icon_path:
            # Caminho absoluto baseado no arquivo atual
            app_path = os.path.abspath(os.getcwd())
            folder = "gui/images/icons"
            full_path = os.path.normpath(os.path.join(app_path, folder, self.icon_path))
            
            if os.path.exists(full_path):
                self.icon_pixmap = QPixmap(full_path)
            else:
                print(f"Erro: Ícone não encontrado em {full_path}")
                self.icon_pixmap = None
        else:
            self.icon_pixmap = None


    def atualizar_estilo(self, is_active):
        bg_color = "#7DA2FF" if is_active else "white"
        text_color = "white" if is_active else "#5D99FF"
        
        self.setStyleSheet(f"""
            #CardDeTempo {{
                background-color: {bg_color};
                border-radius: 20px;
            }}
            QLabel {{ 
                color: {text_color}; 
            }}
        """)
    def atualizar_dados(self, dia, temp, icon_path):
        self.label_dia.setText(dia)
        self.label_temp.setText(f"{temp}°")
    
    # Atualiza o ícone
        self.icon_path = icon_path
        self.set_icon_pixmap()
    
        if self.icon_pixmap:
            scaled_icon = self.icon_pixmap.scaled(
                45, 45,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )   
            self.label_icon.setPixmap(scaled_icon)
        else:
            self.label_icon.clear()

