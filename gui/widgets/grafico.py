from qt_core import *

class PyRainfallChart(QWidget):
    def __init__(self, data=None, days=None):
        super().__init__()
        # Dados iniciais
        self.data = data if data else [40, 60, 30, 80, 50, 90, 20, 55, 70, 45, 35, 65]
        self.days = days if days else ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
        self.setMinimumHeight(120)

    def update_data(self, new_data):
        """Método para a API injetar novos dados de chuva"""
        self.data = new_data
        self.update() # Força o repaint do widget

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height() - 20 
        padding = 10
        bar_spacing = 8
        
        # Cálculo da largura das barras proporcional ao widget
        bar_width = (width - (2 * padding) - (len(self.data) * bar_spacing)) / len(self.data)
        max_val = max(self.data) if max(self.data) > 0 else 1

        for i, val in enumerate(self.data):
            # Calcular altura da barra
            bar_height = (val / max_val) * (height - 20)
            x = padding + i * (bar_width + bar_spacing)
            y = height - bar_height
            
            # Desenhar Barra
            path = QPainterPath()
            rect = QRectF(x, y, bar_width, bar_height)
            path.addRoundedRect(rect, 5, 5) # Bordas arredondadas nas barras
            
            painter.fillPath(path, QColor("#5D99FF"))
            
            # Desenhar Legenda (Meses/Dias)
            painter.setPen(QColor("#A0AEC0"))
            painter.setFont(QFont("Segoe UI", 8))
            painter.drawText(QRectF(x, height + 2, bar_width, 15), Qt.AlignCenter, self.days[i])