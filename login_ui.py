from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import (
    QMessageBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QGraphicsOpacityEffect
)
import pyttsx3
from models.Usuario import Usuario
from menu_admin_ui import Ui_Menu
from menu_trabajador_ui import Ui_Menu_trabajador
from menu_gerente_ui import Ui_Menu_gerente

class AccessibleLineEdit(QtWidgets.QLineEdit):
    def __init__(self, mensaje, lector_funcion, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mensaje_accesible = mensaje
        self.leer_funcion = lector_funcion

    def focusInEvent(self, event):
        super().focusInEvent(event)
        if callable(self.leer_funcion):
            self.leer_funcion(self.mensaje_accesible)


class Ui_Log_in(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.setMinimumSize(600, 400)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Accesibilidad
        self.accesibilidad_activa = False
        self.engine = pyttsx3.init()

        # Fondo y estilo visual
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #d0eaff, stop: 1 white
                );
            }

            QLabel {
                color: #333;
                font-weight: bold;
                font-size: 35px;
            }

            QLineEdit {
                padding: 20px;
                border: 2px solid #ccc;
                border-radius: 12px;
                font-size: 26px;
                background: white;
                min-height: 55px;
            }

            QLineEdit:focus {
                border: 2px solid #5dade2;
                background: #f8fcff;
            }

            QPushButton {
                background-color: #2e86de;
                color: white;
                padding: 22px 40px;
                border-radius: 16px;
                font-weight: bold;
                font-size: 26px;
                min-height: 80px;
                min-width: 280px;
            }

            QPushButton:hover {
                background-color: #2168af;
            }
        """)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(50, 40, 50, 40)
        self.layout.addStretch()

        # Título
        self.Anuncio = QLabel("Abarrotes \"tienda\"")
        self.Anuncio.setFont(QtGui.QFont("Arial", 30, QtGui.QFont.Bold))
        self.Anuncio.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.Anuncio)

        # Usuario
        user_layout = QHBoxLayout()
        self.Lb_Usuario = QLabel("Usuario:")
        self.Lb_Usuario.setFont(QtGui.QFont("Arial", 22))
        self.text_usuario = QLineEdit()
        self.text_usuario = AccessibleLineEdit("Campo usuario", self.leer)
        self.text_usuario.setFont(QtGui.QFont("Arial", 22))
        self.text_usuario.setPlaceholderText("Escriba su usuario")
        user_layout.addWidget(self.Lb_Usuario)
        user_layout.addWidget(self.text_usuario)
        self.layout.addLayout(user_layout)

        # Contraseña
        pass_layout = QHBoxLayout()
        self.Lb_constrasena = QLabel("Contraseña:")
        self.Lb_constrasena.setFont(QtGui.QFont("Arial", 22))
        self.text_contrasena = QLineEdit()
        self.text_contrasena = AccessibleLineEdit("Campo contraseña", self.leer)
        self.text_contrasena.setFont(QtGui.QFont("Arial", 22))
        self.text_contrasena.setPlaceholderText("Escriba su contraseña")
        self.text_contrasena.setEchoMode(QtWidgets.QLineEdit.Password)
        self.text_contrasena.returnPressed.connect(self.validar_usuario)
        pass_layout.addWidget(self.Lb_constrasena)
        pass_layout.addWidget(self.text_contrasena)
        self.layout.addLayout(pass_layout)

        # Botón Entrar
        self.BtnEntrar = QPushButton("Entrar")
        self.BtnEntrar.setFont(QtGui.QFont("Arial", 26, QtGui.QFont.Bold))
        self.BtnEntrar.clicked.connect(self.validar_usuario)
        self.layout.addWidget(self.BtnEntrar, alignment=QtCore.Qt.AlignCenter)

        # Botón de accesibilidad
        self.btn_accesibilidad = QPushButton("Activar accesibilidad")
        self.btn_accesibilidad.setFont(QtGui.QFont("Arial", 16))
        self.btn_accesibilidad.setCheckable(True)
        self.btn_accesibilidad.setStyleSheet("QPushButton:checked { background-color: #117a65; }")
        self.btn_accesibilidad.toggled.connect(self.toggle_accesibilidad)
        self.layout.addWidget(self.btn_accesibilidad, alignment=QtCore.Qt.AlignCenter)

        self.layout.addStretch()

        # Reloj en esquina inferior derecha con fondo flotante
        self.lbReloj = QLabel("00/00/0000 00:00:00")
        self.lbReloj.setFont(QtGui.QFont("Arial", 22, QtGui.QFont.Bold))
        self.lbReloj.setStyleSheet("""
            QLabel {
                background-color: white;
                padding: 8px 16px;
                border-radius: 10px;
                border: 1px solid #ccc;
                color: #000;
            }
        """)
        self.lbReloj.setAlignment(QtCore.Qt.AlignRight)

        clock_layout = QHBoxLayout()
        clock_layout.addStretch()
        clock_layout.addWidget(self.lbReloj)
        self.layout.addLayout(clock_layout)

        self.iniciar_reloj()

    def toggle_accesibilidad(self, activado):
        self.accesibilidad_activa = activado
        if activado:
            self.btn_accesibilidad.setText("Desactivar accesibilidad")
            self.leer("Modo accesible activado. Ingrese su usuario y contraseña y presione Entrar.")
        else:
            self.btn_accesibilidad.setText("Activar accesibilidad")
            self.leer("Modo accesible desactivado.")

    def leer(self, texto):
        if not self.accesibilidad_activa:
            return
        try:
            self.engine.say(texto)
            self.engine.runAndWait()
        except Exception:
            # Reiniciar el motor de voz si se bloquea o cierra inesperadamente
            try:
                self.engine.stop()
            except:
                pass
            self.engine = pyttsx3.init()
            self.engine.say(texto)
            try:
                self.engine.runAndWait()
            except:
                pass

    def crear_focus_handler(self, mensaje):
        def handler(event):
            self.leer(mensaje)
            QtWidgets.QLineEdit.focusInEvent(event.sender(), event)
        return handler

    def iniciar_reloj(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_reloj)
        self.timer.start(1000)

    def actualizar_reloj(self):
        ahora = QtCore.QDateTime.currentDateTime()
        self.lbReloj.setText(ahora.toString("dd/MM/yyyy hh:mm:ss"))

    def validar_usuario(self):
        id_text = self.text_usuario.text()
        pass_text = self.text_contrasena.text()
        usuario = Usuario.autenticar(id_text, pass_text)

        self.text_usuario.clear()
        self.text_contrasena.clear()

        if usuario is not None:
            self.leer(f"Bienvenido {usuario.rol}")

            if usuario.rol == "trabajador":
                self.menu_trabajador_widget = QtWidgets.QWidget()
                self.menu_trabajador_ui = Ui_Menu_trabajador()
                self.menu_trabajador_ui.setupUi(self.menu_trabajador_widget)
                self.menu_trabajador_ui.login_window = self.window()
                self.menu_trabajador_widget.showMaximized()
                self.window().hide()

            elif usuario.rol == "gerente":
                self.menu_gerente_widget = QtWidgets.QWidget()
                self.menu_gerente_ui = Ui_Menu_gerente()
                self.menu_gerente_ui.setupUi(self.menu_gerente_widget)
                self.menu_gerente_ui.login_window = self.window()
                self.menu_gerente_widget.showMaximized()
                self.window().hide()

            elif usuario.rol == "admin":
                self.menu_admin_widget = QtWidgets.QWidget()
                self.menu_ui = Ui_Menu()
                self.menu_ui.setupUi(self.menu_admin_widget)
                self.menu_ui.login_window = self.window()
                self.menu_admin_widget.showMaximized()
                self.window().hide()
            else:
                msg = f"Rol desconocido: {usuario.rol}"
                QMessageBox.warning(None, "Error", msg)
                self.leer(msg)
        else:
            msg = "Usuario o contraseña incorrectos"
            QMessageBox.warning(None, "Error", msg)
            self.leer(msg)

    def mostrar_con_transicion(self, siguiente_widget):
        efecto_actual = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(efecto_actual)
        fade_out = QPropertyAnimation(efecto_actual, b"opacity")
        fade_out.setDuration(400)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.InOutQuad)

        efecto_siguiente = QGraphicsOpacityEffect(siguiente_widget)
        siguiente_widget.setGraphicsEffect(efecto_siguiente)
        efecto_siguiente.setOpacity(0.0)

        fade_in = QPropertyAnimation(efecto_siguiente, b"opacity")
        fade_in.setDuration(500)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.InOutQuad)

        def mostrar_nueva():
            siguiente_widget.showMaximized()
            fade_in.start()
            self.close()

        fade_out.finished.connect(mostrar_nueva)
        fade_out.start()


# MAIN
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ui_Log_in()
    ventana.showMaximized()
    sys.exit(app.exec_())
