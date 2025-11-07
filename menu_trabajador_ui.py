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


class Ui_Menu_trabajador(object):
    def setupUi(self, Menu_trabajador):
        Menu_trabajador.setObjectName("Menu_trabajador")
        Menu_trabajador.resize(800, 600)
        self.window = Menu_trabajador


        self.accesibilidad_activa = False
        self.engine = pyttsx3.init()


        Menu_trabajador.setStyleSheet("""
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
            QLabel {
                color: #333;
                font-size: 28px;
                font-weight: bold;
            }
        """)

        self.verticalLayout = QtWidgets.QVBoxLayout(Menu_trabajador)
        self.verticalLayout.setContentsMargins(100, 40, 100, 40)
        self.verticalLayout.setSpacing(30)

        self.verticalLayout.addStretch(2)


        self.lb_anuncio = QtWidgets.QLabel("Abarrotera \"tienda\"")
        self.lb_anuncio.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.lb_anuncio)


        self.btnRegistrarVenta = AccessibleButton("Registrar Venta", self.leer)
        self.btnRegistrarVenta.setMinimumSize(350, 90)
        self.btnRegistrarVenta.setMaximumSize(600, 150)
        self.btnRegistrarVenta.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnRegistrarVenta.clicked.connect(self.abrirVenta)
        self.verticalLayout.addWidget(self.btnRegistrarVenta, alignment=QtCore.Qt.AlignHCenter)


        self.btnHacerDevolucion = AccessibleButton("Hacer Devolución", self.leer)
        self.btnHacerDevolucion.setMinimumSize(350, 90)
        self.btnHacerDevolucion.setMaximumSize(600, 150)
        self.btnHacerDevolucion.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnHacerDevolucion.clicked.connect(self.abrirDevolucion)
        self.verticalLayout.addWidget(self.btnHacerDevolucion, alignment=QtCore.Qt.AlignHCenter)

        self.verticalLayout.addStretch(1)


        self.btnAccesibilidad = AccessibleButton("Activar accesibilidad", self.leer)
        self.btnAccesibilidad.setCheckable(True)
        self.btnAccesibilidad.setStyleSheet("""
            QPushButton:checked {
                background-color: #117a65;
            }
        """)
        self.btnAccesibilidad.setMinimumSize(250, 60)
        self.btnAccesibilidad.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnAccesibilidad.toggled.connect(self.toggle_accesibilidad)
        self.verticalLayout.addWidget(self.btnAccesibilidad, alignment=QtCore.Qt.AlignHCenter)


        self.btnCerrarSesion = AccessibleButton("Cerrar", self.leer)
        self.btnCerrarSesion.setMinimumSize(250, 60)
        self.btnCerrarSesion.setMaximumSize(400, 100)
        self.btnCerrarSesion.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnCerrarSesion.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.btnCerrarSesion.clicked.connect(self.regresar_login)
        self.verticalLayout.addWidget(self.btnCerrarSesion, alignment=QtCore.Qt.AlignHCenter)

        self.verticalLayout.addStretch(1)
        QtCore.QMetaObject.connectSlotsByName(Menu_trabajador)

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

    def abrirVenta(self):
        from Ventas import Ui_Ventana_ventas
        self.ventas_window = Ui_Ventana_ventas()
        self.ventas_window.menu_trabajador_window = self.verticalLayout.parentWidget()
        self.ventas_window.show()  # Ya se abre maximizada desde el constructor
        self.verticalLayout.parentWidget().hide()

    def abrirDevolucion(self):
        from devolucion import Ui_Devolucion
        self.devolucion_window = Ui_Devolucion()  # ← ya es QWidget
        self.devolucion_window.menu_trabajador_window = self.verticalLayout.parentWidget()
        self.devolucion_window.showMaximized()
        self.verticalLayout.parentWidget().hide()

    def regresar_login(self):
        if self.accesibilidad_activa is True: # o False, según estado anterior
            self.leer("Cerrando sesión.")
        self.engine = pyttsx3.init()
        QtCore.QTimer.singleShot(800, self._cerrar_ventana)

    def _cerrar_ventana(self):
        self.login_window.show()
        self.window.close()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Menu_trabajador = QtWidgets.QWidget()
    ui = Ui_Menu_trabajador()
    ui.setupUi(Menu_trabajador)
    Menu_trabajador.showMaximized()
    sys.exit(app.exec_())
