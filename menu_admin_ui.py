from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
import pyttsx3


class AccessibleButton(QtWidgets.QPushButton):
    def __init__(self, texto, lector_funcion, *args, **kwargs):
        super().__init__(texto, *args, **kwargs)
        self.texto = texto
        self.leer_funcion = lector_funcion

    def focusInEvent(self, event):
        super().focusInEvent(event)
        if callable(self.leer_funcion):
            self.leer_funcion(self.texto)


class Ui_Menu(object):
    def setupUi(self, Menu):
        self.window = Menu
        self.accesibilidad_activa = False
        self.engine = pyttsx3.init()

        Menu.setObjectName("Menu")
        Menu.setWindowTitle("Menú del Administrador")
        Menu.resize(800, 600)

        # 🎨 Estilo moderno
        Menu.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e0f7fa, stop: 1 white
                );
                font-family: 'Segoe UI';
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 20px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton#btnRegresar {
                background-color: #dc3545;
            }
            QPushButton#btnRegresar:hover {
                background-color: #c82333;
            }
            QLabel {
                color: #333;
                font-size: 28px;
                font-weight: bold;
            }
        """)

        self.verticalLayout = QtWidgets.QVBoxLayout(Menu)
        self.verticalLayout.setContentsMargins(100, 40, 100, 40)
        self.verticalLayout.setSpacing(20)

        self.verticalLayout.addStretch(1)

        self.label = QtWidgets.QLabel("Abarrotes \"tienda\"")
        self.label.setMinimumSize(350, 80)
        self.label.setMaximumSize(600, 120)
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignHCenter)

        def crear_boton(nombre, objName=""):
            boton = AccessibleButton(nombre, self.leer)
            boton.setMinimumSize(350, 80)
            boton.setMaximumSize(600, 120)
            font = QtGui.QFont()
            font.setPointSize(18)
            boton.setFont(font)
            if objName:
                boton.setObjectName(objName)
            self.verticalLayout.addWidget(boton, alignment=QtCore.Qt.AlignHCenter)
            return boton

        self.btnGanancias = crear_boton("Reporte Ganancias")
        self.btnVentas = crear_boton("Ver Ventas")
        self.btnInventario = crear_boton("Inventario")
        self.btnUsuarios = crear_boton("Agregar Usuario")
        self.btnRegresar = crear_boton("Regresar", objName="btnRegresar")

        self.btnAccesibilidad = AccessibleButton("Activar accesibilidad", self.leer)
        self.btnAccesibilidad.setCheckable(True)
        self.btnAccesibilidad.setMinimumSize(250, 60)
        self.btnAccesibilidad.setFont(QtGui.QFont("Arial", 16))
        self.btnAccesibilidad.setStyleSheet("""
            QPushButton:checked {
                background-color: #117a65;
            }
        """)
        self.btnAccesibilidad.toggled.connect(self.toggle_accesibilidad)
        self.verticalLayout.addWidget(self.btnAccesibilidad, alignment=QtCore.Qt.AlignHCenter)

        self.verticalLayout.addStretch(2)

        QtCore.QMetaObject.connectSlotsByName(Menu)

        self.btnGanancias.clicked.connect(self.abrir_ganancias)
        self.btnVentas.clicked.connect(self.abrir_ventas)
        self.btnInventario.clicked.connect(self.abrir_inventario)
        self.btnUsuarios.clicked.connect(self.abrir_usuarios)
        self.btnRegresar.clicked.connect(self.regresar_login)

    def leer(self, texto):
        if not self.accesibilidad_activa:
            return
        try:
            self.engine.say(texto)
            self.engine.runAndWait()
        except Exception:
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

    def toggle_accesibilidad(self, estado):
        self.accesibilidad_activa = estado
        if estado:
            self.btnAccesibilidad.setText("Desactivar accesibilidad")
            self.leer("Modo accesible activado")
        else:
            self.btnAccesibilidad.setText("Activar accesibilidad")
            self.leer("Modo accesible desactivado")

    def abrir_ganancias(self):
        from reporteganacia import Ui_RGanancia
        self.ganancia_window = QtWidgets.QWidget()
        self.ganancia_ui = Ui_RGanancia()
        self.ganancia_ui.setupUi(self.ganancia_window)
        self.ganancia_ui.menu_admin_window = self.window
        self.ganancia_window.showMaximized()
        self.window.hide()

    def abrir_ventas(self):
        from ver_ventas import Ui_VerVentas
        self.venta_window = Ui_VerVentas()
        self.venta_window.menu_admin_window = self.verticalLayout.parentWidget()
        self.venta_window.showMaximized()
        self.verticalLayout.parentWidget().hide()

    def abrir_inventario(self):
        from inventario import Ui_Inventario
        self.inventario_window = Ui_Inventario()
        self.inventario_window.menu_admin_window = self.verticalLayout.parentWidget()
        self.inventario_window.showMaximized()
        self.verticalLayout.parentWidget().hide()

    def abrir_usuarios(self):
        from Registro_usuario import Ui_Registro_Usuario
        self.usuario_window = Ui_Registro_Usuario()
        self.usuario_window.menu_admin_window = self.window
        self.usuario_window.showMaximized()
        self.window.hide()

    def regresar_login(self):
        if self.accesibilidad_activa is True:
            self.leer("Cerrando sesión.")
        self.engine = pyttsx3.init()
        QtCore.QTimer.singleShot(800, self._cerrar_ventana)

    def _cerrar_ventana(self):
        self.login_window.show()
        self.window.close()

# MAIN
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Menu = QtWidgets.QWidget()
    ui = Ui_Menu()
    ui.setupUi(Menu)
    Menu.showMaximized()
    sys.exit(app.exec_())
