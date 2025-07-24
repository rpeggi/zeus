import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QSizePolicy
)
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QIcon, QPixmap
from PySide6.QtCore import Qt, QRectF, QSize

# ================================
#  CONFIGURACIÓN DE ICONOS
# ================================

# Si es True, usa PNGs en icons/xxx.png; si es False, usa emoji/texto Unicode
USE_ICONS = True

# Diccionario de rutas de iconos para cada botón
BTN_ICONS = {
    "luz_alta": "icons/luz_alta.png",     # Ruta para icono PNG de luz alta
    "luz_baja": "icons/luz_baja.png",     # Ruta para icono PNG de luz baja
    "int_izq": "icons/int_izq.png",       # Ruta para icono PNG intermitente izquierdo
    "int_der": "icons/int_der.png",       # Ruta para icono PNG intermitente derecho
    "bocina": "icons/bocina.png",         # Ruta para icono PNG bocina
    "stop": "icons/stop.png",             # Ruta para icono PNG stop
    "left": "icons/left.png",             # Ruta para icono PNG flecha izquierda
    "reverse": "icons/reverse.png",       # Ruta para icono PNG flecha reversa
    "forward": "icons/forward.png",       # Ruta para icono PNG flecha adelante
    "right": "icons/right.png",           # Ruta para icono PNG flecha derecha
    "mapa": "icons/mapa.png",             # Ruta para icono PNG de MAPA
}

# Diccionario de iconos Unicode/texto para cada botón (fallback si USE_ICONS es False)
BTN_UNICODE = {
    "luz_alta": "🔆",
    "luz_baja": "🔅",
    "int_izq": "⬅",
    "int_der": "➡",
    "bocina": "🔊",
    "stop": "✋",
    "left": "←",
    "reverse": "↓",
    "forward": "↑",
    "right": "→",
    "mapa": "MAPA",
}

# =============================================
#  CLASE DEL POTENCIÓMETRO VERTICAL
# =============================================
class PotVerticalWidget(QWidget):
    """Potenciómetro vertical visual tipo barra de bloques."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Valor actual, valor mínimo, valor máximo del potenciómetro
        self.value = 100
        self.max_value = 400
        self.min_value = 1
        self.block_count = 27  # Número de bloques o "niveles" visuales

        # Establece tamaño mínimo y máximo del widget (diseñado para 1024x600)
        self.setMinimumSize(90, 520)
        self.setMaximumWidth(110)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def paintEvent(self, event):
        """Dibuja el potenciómetro vertical."""
        w, h = self.width(), self.height()
        margin = 12  # Espaciado interno
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Calcula cuántos bloques están "llenados" según valor actual
        pct = (self.value - self.min_value) / (self.max_value - self.min_value)
        filled = int(pct * self.block_count + 0.5)
        block_h = (h - 2 * margin) / self.block_count
        block_w = w - 2 * margin - 14

        # Dibuja cada bloque (color según zona)
        for i in range(self.block_count):
            bx = margin + 7  # posición X
            by = h - margin - (i + 1) * block_h + 3  # posición Y (de abajo hacia arriba)
            if i < filled:
                frac = (i + 1) / self.block_count
                if frac > .75:
                    color = QColor("#FF5757")      # Zona roja (peligro)
                elif frac > .5:
                    color = QColor("#FFE662")      # Zona amarilla (media)
                else:
                    color = QColor("#4BFFB6")      # Zona verde (segura)
            else:
                color = QColor(50, 52, 60)         # Color de fondo (no lleno)
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            # Dibuja bloque redondeado
            painter.drawRoundedRect(QRectF(bx, by, block_w, block_h - 6), 9, 9)

        # Dibuja marco blanco exterior del potenciómetro
        painter.setPen(QPen(QColor(200, 210, 255), 3))
        painter.setBrush(Qt.NoBrush)
        rect = QRectF(margin, margin, w - 2 * margin, h - 2 * margin)
        painter.drawRoundedRect(rect, 24, 24)

        # Dibuja líneas divisorias (para zonas 1-2-3)
        for j in (1, 2):
            y = margin + (h - 2 * margin) * j / 3
            painter.setPen(QPen(QColor(150, 170, 230), 1.6))
            painter.drawLine(margin, y, w - margin, y)

        # Dibuja los números de las zonas ("3", "2", "1")
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        for idx, num in enumerate(['3', '2', '1']):
            y_text = margin + (h - 2 * margin) * idx / 3
            painter.setPen(QColor(150, 170, 230))
            painter.drawText(QRectF(0, y_text, margin + 10, 30), Qt.AlignLeft | Qt.AlignTop, num)

        # Dibuja el valor numérico actual dentro del bloque activo
        if filled:
            center_y = h - margin - (filled - .5) * block_h
            painter.setPen(QColor(235, 245, 255))
            painter.setFont(QFont("Arial", 19, QFont.Bold))
            painter.drawText(QRectF(0, center_y - 14, w, 28), Qt.AlignCenter, str(self.value))

    def mousePressEvent(self, e):
        """Cambia el valor del potenciómetro al hacer click."""
        self._update_value(e.position().y() if hasattr(e, 'position') else e.y())

    def mouseMoveEvent(self, e):
        """Permite arrastrar para cambiar el valor."""
        if e.buttons() & Qt.LeftButton:
            self._update_value(e.position().y() if hasattr(e, 'position') else e.y())

    def _update_value(self, y):
        """Actualiza self.value según la posición Y del mouse."""
        margin, h = 12, self.height()
        inner_h = h - 2 * margin
        rel = max(0, min(inner_h, y - margin))
        pct = 1 - rel / inner_h
        self.value = max(self.min_value, min(self.max_value, int(round(self.min_value + pct * (self.max_value - self.min_value)))))
        print(f"Potenciómetro: {self.value}")
        self.update()

# ============================================
#  FABRICANTES DE BOTONES MODERNOS
# ============================================

def modern_circle_btn(btn_name, slot, size=70, font_size=26, bg="#22252A", fg="#FFE662", border="#FFF"):
    """
    Devuelve un QPushButton circular moderno, con icono PNG o Unicode según USE_ICONS.
    - btn_name: clave de icono ("luz_alta", "bocina", etc)
    - slot: función a ejecutar al presionar el botón
    - size, font_size: tamaño de botón y fuente
    - bg, fg, border: colores de fondo, texto, borde
    """
    # El texto es "" si se usan iconos, o el texto unicode si no.
    btn = QPushButton("" if USE_ICONS else BTN_UNICODE[btn_name])
    btn.setFixedSize(size, size)
    btn.setFont(QFont("Arial", font_size, QFont.Bold))
    btn.setCursor(Qt.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton {{background:{bg};color:{fg};border:3px solid {border};border-radius:{size//2}px;}}
        QPushButton:hover {{background:#1a1c20;border:3px solid #00FFC3;color:#00FFC3;}}
        QPushButton:pressed {{background:#101114;border:3px solid #FF9066;color:#FF9066;}}
    """)
    # Si está activado el modo PNG, pone el icono correspondiente
    if USE_ICONS:
        btn.setIcon(QIcon(BTN_ICONS[btn_name]))
        btn.setIconSize(QSize(size-10, size-10))
    btn.clicked.connect(slot)
    btn.setObjectName(btn_name)
    return btn

def modern_square_btn(btn_name, slot, size=120, font_size=60, border="#FFF"):
    """
    Igual que el anterior, pero cuadrado. Útil para flechas de dirección.
    """
    btn = QPushButton("" if USE_ICONS else BTN_UNICODE[btn_name])
    btn.setFixedSize(size, size)
    btn.setFont(QFont("Arial", font_size, QFont.Bold))
    btn.setCursor(Qt.PointingHandCursor)
    btn.setStyleSheet(f"""
        QPushButton {{background:#1B1D22;color:#fff;border:3px solid {border};border-radius:20px;}}
        QPushButton:hover {{background:#202228;color:#00FFC3;border:3px solid #00FFC3;}}
        QPushButton:pressed {{background:#131518;color:#FFE662;border:3px solid #FFE662;}}
    """)
    if USE_ICONS:
        btn.setIcon(QIcon(BTN_ICONS[btn_name]))
        btn.setIconSize(QSize(size-14, size-14))
    btn.clicked.connect(slot)
    btn.setObjectName(btn_name)
    return btn

def modern_map_btn(slot):
    """
    Botón MAPA. Si USE_ICONS es True, pone PNG, si no pone texto "MAPA".
    """
    btn = QPushButton("" if USE_ICONS else BTN_UNICODE["mapa"])
    btn.setFixedSize(190, 90)
    btn.setFont(QFont("Arial", 30, QFont.Bold))
    btn.setStyleSheet("""
        QPushButton {background:#23242a;color:#63C5FA;border:3px solid #63C5FA;border-radius:20px;letter-spacing:2px;}
        QPushButton:hover {background:#181a1e;border:3px solid #00FFC3;color:#00FFC3;}
        QPushButton:pressed {background:#111216;border:3px solid #FFE662;color:#FFE662;}
    """)
    if USE_ICONS:
        btn.setIcon(QIcon(BTN_ICONS["mapa"]))
        btn.setIconSize(QSize(170, 70))
    btn.clicked.connect(slot)
    btn.setObjectName("MAPA")
    return btn

# ============================================
#  CLASE PRINCIPAL DE LA VENTANA
# ============================================
class MainWindow(QWidget):
    """Ventana principal, panel de controles moderno."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel 1024×600 – Modern UI")
        self.setStyleSheet("background-color:#18191d;")
        self.resize(1024, 600)   # tamaño de ventana (ajustado a 1024x600)
        self._init_ui()

    # ---------- Slots de los botones ----------
    # Cada función se llama al presionar su botón y solo imprime el nombre del botón.
    def luz_alta(self):         print("LUZ ALTA presionada")
    def luz_baja(self):         print("LUZ BAJA presionada")
    def int_izq(self):          print("INTERMITENTE IZQ presionado")
    def int_der(self):          print("INTERMITENTE DER presionado")
    def mapa(self):             print("MAPA presionado")
    def bocina(self):           print("BOCINA presionada")
    def stop(self):             print("STOP presionado")
    def left(self):             print("LEFT presionado")
    def reverse(self):          print("REVERSE presionado")
    def forward(self):          print("FORWARD presionado")
    def right(self):            print("RIGHT presionado")

    def _init_ui(self):
        """
        Construye toda la interfaz visual y la disposición de botones, cámaras y potenciómetro.
        """
        main_h = QHBoxLayout(self)               # Layout principal: horizontal
        main_h.setContentsMargins(20, 15, 20, 15)
        main_h.setSpacing(0)

        center_v = QVBoxLayout()                 # Panel central (vertical)
        center_v.setSpacing(18)

        # ---- FILA DE CÁMARAS ----
        cam_row = QHBoxLayout(); cam_row.setSpacing(36)
        for cam in ("FC", "RC"):   # Para cada cámara (frontal y trasera)
            box = QVBoxLayout()
            lbl = QLabel(cam)
            lbl.setFont(QFont("Arial", 16, QFont.Bold))
            lbl.setStyleSheet("color:#fff;padding-bottom:4px;")
            img = QLabel("CÁMARA")
            img.setAlignment(Qt.AlignCenter)
            img.setFixedSize(300, 140)
            img.setStyleSheet("border:3px solid #63C5FA;background:#23242a;border-radius:18px;color:#6c7c92;font:700 26px 'Arial';")
            # Para usar imagen real de cámara: descomentar siguiente línea (y poner el PNG en icons/)
            # img.setPixmap(QPixmap(f"icons/cam_{cam.lower()}.png").scaled(300, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            # img.setText("")   # Elimina el texto "CÁMARA"
            box.addWidget(lbl)
            box.addWidget(img)
            cam_row.addLayout(box)
        center_v.addLayout(cam_row)

        # ---- FILA DE CONTROLES CIRCULARES + MAPA ----
        ctrl_row = QHBoxLayout(); ctrl_row.setSpacing(10)
        # Añade los 4 botones y el botón MAPA, usando la función moderna
        ctrl_row.addWidget(modern_circle_btn("luz_alta", self.luz_alta, size=70, font_size=28))
        ctrl_row.addWidget(modern_circle_btn("luz_baja", self.luz_baja, size=70, font_size=28))
        ctrl_row.addWidget(modern_circle_btn("int_izq", self.int_izq, fg="#63C5FA", size=70, font_size=28))
        ctrl_row.addWidget(modern_circle_btn("int_der", self.int_der, fg="#63C5FA", size=70, font_size=28))
        ctrl_row.addWidget(modern_map_btn(self.mapa))
        center_v.addLayout(ctrl_row)

        # ---- FILA DE BOCINA Y STOP ----
        bs_row = QHBoxLayout(); bs_row.setSpacing(50)
        bs_row.addStretch(1)
        bs_row.addWidget(modern_circle_btn("bocina", self.bocina, fg="#63C5FA", size=70, font_size=28))
        bs_row.addWidget(modern_circle_btn("stop", self.stop, fg="#FFE662", size=70, font_size=28))
        bs_row.addStretch(1)
        center_v.addLayout(bs_row)

        # ---- FILA DE FLECHAS GRANDES ----
        arrow_row = QHBoxLayout(); arrow_row.setSpacing(46)
        # Añade los 4 botones de dirección (flechas), cuadrados y grandes
        for name, slot in [("left",self.left),("reverse",self.reverse),("forward",self.forward),("right",self.right)]:
            arrow_row.addWidget(modern_square_btn(name, slot, size=120, font_size=60))
        center_v.addLayout(arrow_row)

        # ---- FILA DE LABELS DE FLECHAS ----
        label_row = QHBoxLayout(); label_row.setSpacing(arrow_row.spacing())
        for text in ["LEFT","REVERSE","FORWARD","RIGHT"]:
            lab = QLabel(text)
            lab.setFixedWidth(120)
            lab.setAlignment(Qt.AlignCenter)
            lab.setFont(QFont("Arial", 16, QFont.Bold))
            lab.setStyleSheet("color:#fff;")
            label_row.addWidget(lab)
        center_v.addLayout(label_row)

        # Añade todo el panel central al layout principal (lado izquierdo)
        main_h.addLayout(center_v, stretch=5)

        # ---- POTENCIÓMETRO ----
        pot_v = QVBoxLayout(); pot_v.addStretch(1)
        pot = PotVerticalWidget()
        pot.setMinimumHeight(540)
        pot_v.addWidget(pot, alignment=Qt.AlignVCenter)
        pot_v.addStretch(1)
        # Añade el potenciómetro al layout principal (lado derecho)
        main_h.addLayout(pot_v, stretch=1)

# ============================
#  EJECUCIÓN DE LA APP
# ============================
if __name__ == "__main__":
    # Crea y lanza la aplicación PySide6
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
