import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QSizePolicy
)
from PySide6.QtGui import QFont, QPainter, QColor, QPen
from PySide6.QtCore import Qt, QRectF

# =========================
#  POTENCIÓMETRO VERTICAL
# =========================
class PotVerticalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Valor inicial, mínimo y máximo
        self.value = 100
        self.max_value = 400
        self.min_value = 1
        self.block_count = 27  # Número de bloques (barras)
        # Cambia el tamaño mínimo y máximo para ajustar el alto/anchura del potenciómetro
        self.setMinimumSize(110, 680)
        self.setMaximumWidth(160)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def paintEvent(self, event):
        # Dibuja el potenciómetro (barras de colores + marco)
        w, h = self.width(), self.height()
        margin = 16
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Porcentaje de llenado según valor
        percent = (self.value - self.min_value) / (self.max_value - self.min_value)
        filled_blocks = int(percent * self.block_count + 0.5)
        block_height = (h - 2*margin) / self.block_count
        block_width = w - 2*margin - 18

        # Dibuja cada bloque/barrra del potenciómetro
        for b in range(self.block_count):
            bx = margin + 9
            by = h - margin - (b + 1) * block_height + 4
            if b < filled_blocks:
                # Cambia color según zona del potenciómetro
                frac = (b + 1) / self.block_count
                if frac > 13/16:
                    color = QColor("#FF5757")  # rojo
                elif frac > 7/16:
                    color = QColor("#FFE662")  # amarillo
                else:
                    color = QColor("#4BFFB6")  # verde
                painter.setBrush(color)
            else:
                painter.setBrush(QColor(55, 55, 60))  # color de fondo de los bloques vacíos
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(QRectF(bx, by, block_width, block_height-7), 11, 11)

        # Marco exterior moderno
        painter.setPen(QPen(QColor(180, 200, 255), 4))
        painter.setBrush(Qt.NoBrush)
        rect = QRectF(margin, margin, w - 2*margin, h - 2*margin)
        painter.drawRoundedRect(rect, 29, 29)

        # Líneas divisorias y números de zona
        for i in range(1, 3):
            y = margin + (h - 2*margin) * i / 3
            painter.setPen(QPen(QColor(120,150,220), 2))
            painter.drawLine(margin, y, w - margin, y)
        font = QFont("Arial", 20, QFont.Bold)
        painter.setFont(font)
        for i, num in enumerate(['3', '2', '1']):
            y_num = margin + (h - 2*margin) * i / 3
            painter.setPen(QPen(QColor(130, 160, 210)))
            painter.drawText(QRectF(0, y_num, margin + 15, 46), Qt.AlignLeft | Qt.AlignTop, num)

        # Valor actual del potenciómetro, centrado en el bloque activo
        if filled_blocks > 0:
            block_centro = h - margin - (filled_blocks - 0.5) * block_height
            painter.setPen(QColor(220, 235, 255))
            painter.setFont(QFont("Arial", 23, QFont.Bold))
            painter.drawText(QRectF(0, block_centro-18, w, 36), Qt.AlignHCenter | Qt.AlignVCenter, str(self.value))

    # Permite actualizar el valor del potenciómetro con click o drag
    def mousePressEvent(self, event):
        self.update_value_from_y(event.position().y() if hasattr(event, "position") else event.y())
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.update_value_from_y(event.position().y() if hasattr(event, "position") else event.y())
    def update_value_from_y(self, y):
        margin = 16
        h = self.height()
        inner_h = h - 2 * margin
        rel_y = y - margin
        rel_y = max(0, min(inner_h, rel_y))
        percent = 1 - rel_y / inner_h
        value = int(round(self.min_value + percent * (self.max_value - self.min_value)))
        value = max(self.min_value, min(self.max_value, value))
        if value != self.value:
            self.value = value
            print(f"Potenciómetro: {self.value}")
            self.update()

# ==========================================
#  BOTONES MODERNOS (CIRCULARES Y CUADRADOS)
# ==========================================
def modern_circle_btn(icon, name, slot, bg="#23242A", fg="#FFE662", border="#FFF", size=90, font_size=38):
    """
    Crea un botón circular moderno.
    icon: Puede ser un caracter unicode o el path de una imagen (ver comentario abajo).
    name: nombre interno del botón.
    slot: función a ejecutar cuando se presiona.
    bg, fg, border: colores de fondo, texto y borde.
    size, font_size: tamaño.
    Para usar una imagen en vez de icono:
        - Cambia el texto por '', usa btn.setIcon(QIcon('ruta/a/tu/imagen.png'))
        - Ajusta btn.setIconSize(QSize(size-10, size-10))
    """
    btn = QPushButton(icon)
    btn.setFixedSize(size, size)
    btn.setFont(QFont("Arial", font_size, QFont.Bold))
    btn.setCursor(Qt.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton {{
            background: {bg};
            color: {fg};
            border: 4px solid {border};
            border-radius: {size//2}px;
        }}
        QPushButton:hover {{
            background: #1a1a1e;
            color: #00FFC3;
            border: 4px solid #00FFC3;
        }}
        QPushButton:pressed {{
            background: #101115;
            color: #ff5757;
            border: 4px solid #ff5757;
        }}
    """)
    btn.clicked.connect(slot)
    btn.setObjectName(name)
    # --------- Para IMÁGENES en vez de icono: descomentar las siguientes líneas --------
    # from PySide6.QtGui import QIcon, QPixmap
    # btn.setText("")
    # btn.setIcon(QIcon(QPixmap("ruta/imagen.png")))
    # btn.setIconSize(QSize(size-10, size-10))
    return btn

def modern_square_btn(icon, name, slot, border="#FFF", size=160, font_size=78):
    """
    Crea un botón cuadrado moderno.
    icon: caracter unicode o path de imagen (ver comentario).
    Para poner imagen, ver ejemplo arriba.
    """
    btn = QPushButton(icon)
    btn.setFixedSize(size, size)
    btn.setFont(QFont("Arial", font_size, QFont.Bold))
    btn.setCursor(Qt.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton {{
            background: #191B1E;
            color: #fff;
            border: 4px solid {border};
            border-radius: 34px;
        }}
        QPushButton:hover {{
            background: #181a1e;
            color: #00FFC3;
            border: 4px solid #00FFC3;
        }}
        QPushButton:pressed {{
            background: #15181c;
            color: #ffe662;
            border: 4px solid #ffe662;
        }}
    """)
    btn.clicked.connect(slot)
    btn.setObjectName(name)
    # --- Para imagen, usa btn.setIcon(QIcon('ruta/imagen.png')) y btn.setText("") ---
    return btn

def modern_map_label(slot):
    """
    Botón MAPA grande y moderno. 
    Para imagen, cambia el texto por '' y usa setIcon igual que arriba.
    """
    btn = QPushButton("MAPA")
    btn.setFixedSize(260, 120)
    btn.setFont(QFont("Arial", 42, QFont.Bold))
    btn.setStyleSheet("""
        QPushButton {
            background: #23242a;
            color: #63C5FA;
            border: 4px solid #63C5FA;
            border-radius: 30px;
            letter-spacing: 2px;
        }
        QPushButton:hover {
            background: #181a1e;
            color: #fff;
            border: 4px solid #00FFC3;
        }
        QPushButton:pressed {
            background: #15181c;
            color: #ffe662;
            border: 4px solid #ffe662;
        }
    """)
    btn.clicked.connect(slot)
    btn.setObjectName("MAPA")
    # -- Para imagen, btn.setText(""); btn.setIcon(QIcon('ruta/imagen.png')); etc. --
    return btn

# ================
#   VENTANA PRINCIPAL
# ================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layout clásico, estilo moderno")
        self.setStyleSheet("background-color: #18191d;")
        self.resize(1366, 900)
        self.setup_ui()

    # ------ Funciones de cada botón ------
    def luz_alta(self): print("Botón LUZ ALTA presionado")
    def luz_baja(self): print("Botón LUZ BAJA presionado")
    def intermitente_izq(self): print("Botón INTERMITENTE IZQUIERDA presionado")
    def intermitente_der(self): print("Botón INTERMITENTE DERECHA presionado")
    def mapa(self): print("Botón MAPA presionado")
    def bocina(self): print("Botón BOCINA presionado")
    def stop(self): print("Botón STOP presionado")
    def left(self): print("Botón LEFT presionado")
    def reverse(self): print("Botón REVERSE presionado")
    def forward(self): print("Botón FORWARD presionado")
    def right(self): print("Botón RIGHT presionado")

    def setup_ui(self):
        # Layout horizontal principal: panel central y potenciómetro a la derecha
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(38, 24, 38, 24)
        main_layout.setSpacing(0)

        center_panel = QVBoxLayout()
        center_panel.setSpacing(24)

        # -------------------
        # Cámaras, bien alineadas
        cam_row = QHBoxLayout()
        cam_row.setSpacing(56)
        for label in ["FC", "RC"]:
            cam_box = QVBoxLayout()
            cam_lbl = QLabel(label)
            cam_lbl.setFont(QFont("Arial", 20, QFont.Bold))
            cam_lbl.setStyleSheet("color: #fff; padding-bottom: 7px;")
            cam_lbl.setAlignment(Qt.AlignLeft)
            img_placeholder = QLabel("CÁMARA")
            img_placeholder.setAlignment(Qt.AlignCenter)
            img_placeholder.setFixedSize(470, 210)
            img_placeholder.setStyleSheet("""
                border: 4px solid #63C5FA;
                background: #23242a;
                border-radius: 26px;
                color: #6c7c92;
                font: 700 44px 'Arial';
            """)
            # --- Para usar una imagen en vez de texto, usa:
            # img_placeholder.setPixmap(QPixmap("ruta/imagen.jpg").scaled(470, 210, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            cam_box.addWidget(cam_lbl)
            cam_box.addWidget(img_placeholder)
            cam_row.addLayout(cam_box)
        center_panel.addLayout(cam_row)

        # -------------------
        # Controles circulares (luces, intermitentes) y MAPA (más juntos y MAPA grande)
        ctrl_row = QHBoxLayout()
        ctrl_row.setSpacing(14)
        ctrl_row.addWidget(modern_circle_btn("🔆", "luz_alta", self.luz_alta, fg="#FFE662", size=100, font_size=44))
        ctrl_row.addWidget(modern_circle_btn("🔅", "luz_baja", self.luz_baja, fg="#FF9066", size=100, font_size=44))
        ctrl_row.addWidget(modern_circle_btn("⬅", "intermitente_izq", self.intermitente_izq, fg="#63C5FA", size=100, font_size=44))
        ctrl_row.addWidget(modern_circle_btn("➡", "intermitente_der", self.intermitente_der, fg="#63C5FA", size=100, font_size=44))
        ctrl_row.addWidget(modern_map_label(self.mapa))
        center_panel.addLayout(ctrl_row)

        # -------------------
        # Bocina y stop (centrados debajo)
        mid_ctrls = QHBoxLayout()
        mid_ctrls.setSpacing(75)
        mid_ctrls.addStretch(1)
        mid_ctrls.addWidget(modern_circle_btn("🔊", "bocina", self.bocina, fg="#63C5FA", size=100, font_size=44))
        mid_ctrls.addWidget(modern_circle_btn("✋", "stop", self.stop, fg="#FFE662", size=100, font_size=44))
        mid_ctrls.addStretch(1)
        center_panel.addLayout(mid_ctrls)

        # -------------------
        # Flechas de dirección grandes y etiquetas alineadas
        arrow_row = QHBoxLayout()
        arrow_row.setSpacing(80)
        arrow_btns = [
            ("←", "left", self.left),
            ("↓", "reverse", self.reverse),
            ("↑", "forward", self.forward),
            ("→", "right", self.right)
        ]
        for icon, name, slot in arrow_btns:
            arrow_row.addWidget(modern_square_btn(icon, name, slot, size=170, font_size=88))
        center_panel.addLayout(arrow_row)

        # Etiquetas alineadas bajo cada flecha
        label_row = QHBoxLayout()
        label_row.setSpacing(arrow_row.spacing())
        label_font = QFont("Arial", 27, QFont.Bold)
        for text in ["LEFT", "REVERSE", "FORWARD", "RIGHT"]:
            lbl = QLabel(text)
            lbl.setFont(label_font)
            lbl.setStyleSheet("color: #fff; letter-spacing: 2px;")
            lbl.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            lbl.setFixedWidth(170)
            label_row.addWidget(lbl)
        center_panel.addLayout(label_row)

        # Agrega el panel central al layout principal
        main_layout.addLayout(center_panel, stretch=6)

        # Potenciómetro vertical moderno alineado a la derecha
        pot_layout = QVBoxLayout()
        pot_layout.setContentsMargins(0, 0, 0, 0)
        pot_layout.addStretch(1)
        potentiometer = PotVerticalWidget()
        potentiometer.setMinimumHeight(810)
        pot_layout.addWidget(potentiometer, alignment=Qt.AlignVCenter)
        pot_layout.addStretch(1)
        main_layout.addLayout(pot_layout, stretch=1)

        self.setLayout(main_layout)

# =========
# MAIN
# =========
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
