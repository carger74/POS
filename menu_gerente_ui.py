from PyQt5 import QtCore, QtGui, QtWidgets
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


class Ui_Menu_gerente(object):
    def setupUi(self, Menu_gerente):
        Menu_gerente.setObjectName("Menu_gerente")
        Menu_gerente.setWindowTitle("Menú del Gerente")
        Menu_gerente.resize(900, 600)
        self.window = Menu_gerente  # Almacenar referencia directa

        # Accesibilidad
        self.accesibilidad_activa = False
        self.engine = pyttsx3.init()

        # 🎨 Estilo con fondo y botones modernos
        Menu_gerente.setStyleSheet("""
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

        self.verticalLayout = QtWidgets.QVBoxLayout(Menu_gerente)
        self.verticalLayout.setContentsMargins(100, 40, 100, 40)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignHCenter)

        self.verticalLayout.addStretch(1)

        self.label = QtWidgets.QLabel(Menu_gerente)
        self.label.setMinimumSize(QtCore.QSize(350, 80))
        self.label.setMaximumSize(QtCore.QSize(600, 120))
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        def crear_boton_accesible(nombre, lector_funcion, objName=""):
            boton = AccessibleButton(nombre, lector_funcion)
            boton.setMinimumSize(QtCore.QSize(350, 80))
            boton.setMaximumSize(QtCore.QSize(550, 120))
            font = QtGui.QFont()
            font.setPointSize(18)
            boton.setFont(font)
            if objName:
                boton.setObjectName(objName)
            self.verticalLayout.addWidget(boton, alignment=QtCore.Qt.AlignHCenter)
            return boton

        # Botones funcionales
        self.btnVentas = crear_boton_accesible("Ver Ventas", self.leer)
        self.btnInventario = crear_boton_accesible("Inventario", self.leer)
        self.btnRegresar = crear_boton_accesible("Regresar", self.leer, objName="btnRegresar")

        # Botón accesibilidad
        self.btnAccesibilidad = AccessibleButton("Activar accesibilidad", self.leer)
        self.btnAccesibilidad.setFont(QtGui.QFont("Arial", 16))
        self.btnAccesibilidad.setCheckable(True)
        self.btnAccesibilidad.setMinimumSize(250, 60)
        self.btnAccesibilidad.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnAccesibilidad.setStyleSheet("""
            QPushButton:checked {
                background-color: #117a65;
            }
        """)
        self.btnAccesibilidad.toggled.connect(self.toggle_accesibilidad)
        self.verticalLayout.addWidget(self.btnAccesibilidad, alignment=QtCore.Qt.AlignHCenter)

        self.verticalLayout.addStretch(2)

        self.retranslateUi(Menu_gerente)
        QtCore.QMetaObject.connectSlotsByName(Menu_gerente)

        self.btnVentas.clicked.connect(self.abrir_ventas)
        self.btnInventario.clicked.connect(self.abrir_inventario)
        self.btnRegresar.clicked.connect(self.regresar_login)

    def retranslateUi(self, Menu_gerente):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Menu_gerente", "Abarrotes \"tienda\""))

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

    def toggle_accesibilidad(self, estado):
        self.accesibilidad_activa = estado
        if estado:
            self.btnAccesibilidad.setText("Desactivar accesibilidad")
            self.leer("Modo accesible activado")
        else:
            self.btnAccesibilidad.setText("Activar accesibilidad")
            self.leer("Modo accesible desactivado")

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

    def regresar_login(self):
        if self.accesibilidad_activa is True:  # o False, según estado anterior
            self.leer("Cerrando sesión.")
        self.engine = pyttsx3.init()
        QtCore.QTimer.singleShot(800, self._cerrar_ventana)


    def _cerrar_ventana(self):
        self.login_window.show()
        self.window.close()

# Ejecución independiente

