from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Facade import SistemaVentas

class Ui_RGanancia(object):
    def setupUi(self, RGanancia):
        RGanancia.setObjectName("RGanancia")
        RGanancia.setWindowTitle("Reporte de Ganancias")
        self.ventana = RGanancia

        RGanancia.setStyleSheet("""
            QWidget {
                background-color: #f0f4f7;
                font-family: 'Segoe UI';
                font-size: 23px;
            }
            QLabel {
                color: #333;
                font-weight: bold;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QComboBox {
                padding: 6px;
                border-radius: 6px;
                background-color: white;
            }
        """)

        fuente_grande = QtGui.QFont("Segoe UI", 14)

        self.layoutCentral = QtWidgets.QVBoxLayout(RGanancia)
        self.layoutCentral.setContentsMargins(20, 20, 20, 20)


        self.lbTitulo = QtWidgets.QLabel("Reporte de Ganancias")
        self.lbTitulo.setAlignment(QtCore.Qt.AlignCenter)
        self.lbTitulo.setFont(QtGui.QFont("Segoe UI", 28, QtGui.QFont.Bold))
        self.layoutCentral.addWidget(self.lbTitulo)
        self.layoutCentral.addWidget(self._crear_linea())


        self.layoutControles = QtWidgets.QHBoxLayout()
        self.layoutControles.setSpacing(15)

        labelInicio = QtWidgets.QLabel("Mes inicio:")
        labelInicio.setFont(fuente_grande)
        self.layoutControles.addWidget(labelInicio)

        self.cmbMesInicio = QtWidgets.QComboBox()
        self.cmbMesInicio.setFont(fuente_grande)
        self.meses_texto = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.cmbMesInicio.addItems(self.meses_texto)
        self.layoutControles.addWidget(self.cmbMesInicio)

        labelFin = QtWidgets.QLabel("Mes fin:")
        labelFin.setFont(fuente_grande)
        self.layoutControles.addWidget(labelFin)

        self.cmbMesFin = QtWidgets.QComboBox()
        self.cmbMesFin.setFont(fuente_grande)
        self.cmbMesFin.addItems(self.meses_texto)
        self.layoutControles.addWidget(self.cmbMesFin)

        labelAnio = QtWidgets.QLabel("Año:")
        labelAnio.setFont(fuente_grande)
        self.layoutControles.addWidget(labelAnio)

        self.cmbAnio = QtWidgets.QComboBox()
        self.cmbAnio.setFont(fuente_grande)
        self.cmbAnio.addItems(["2025", "2026"])
        self.layoutControles.addWidget(self.cmbAnio)

        self.btnActualizar = QtWidgets.QPushButton("Actualizar")
        self.btnActualizar.setFont(fuente_grande)
        self.layoutControles.addWidget(self.btnActualizar)

        self.layoutCentral.addLayout(self.layoutControles)
        self.layoutCentral.addWidget(self._crear_linea())


        self.layoutGraficas = QtWidgets.QHBoxLayout()

        self.widgetGraficoLinea = QtWidgets.QWidget()
        self.widgetGraficoLinea.setLayout(QtWidgets.QVBoxLayout())
        self.widgetGraficoLinea.layout().setContentsMargins(0, 0, 0, 0)
        self.layoutGraficas.addWidget(self.widgetGraficoLinea)

        self.widgetGraficoPastel = QtWidgets.QWidget()
        self.widgetGraficoPastel.setLayout(QtWidgets.QVBoxLayout())
        self.widgetGraficoPastel.layout().setContentsMargins(0, 0, 0, 0)
        self.layoutGraficas.addWidget(self.widgetGraficoPastel)

        self.layoutCentral.addLayout(self.layoutGraficas)
        self.layoutCentral.addWidget(self._crear_linea())

        self.btnRegresar = QtWidgets.QPushButton("Regresar")
        self.btnRegresar.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Bold))
        self.btnRegresar.setMinimumSize(QtCore.QSize(900, 70))
        self.btnRegresar.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 20px;
                padding: 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)


        layout_boton = QtWidgets.QHBoxLayout()
        layout_boton.addStretch()
        layout_boton.addWidget(self.btnRegresar)
        layout_boton.addStretch()
        self.layoutCentral.addLayout(layout_boton)

        self.facade = SistemaVentas()
        self.btnActualizar.clicked.connect(self.actualizar_graficos)
        self.btnRegresar.clicked.connect(self.regresar_a_menu)

    def _crear_linea(self):
        linea = QtWidgets.QFrame()
        linea.setFrameShape(QtWidgets.QFrame.HLine)
        linea.setFrameShadow(QtWidgets.QFrame.Sunken)
        return linea

    def actualizar_graficos(self):
        try:
            anio = int(self.cmbAnio.currentText())
            mes_inicio = self.cmbMesInicio.currentIndex() + 1
            mes_fin = self.cmbMesFin.currentIndex() + 1

            productos = self.facade.obtener_productos_mas_vendidos(anio, mes_inicio, mes_fin)
            ganancia_mensual = self.facade.obtener_ganancia_neta(anio, mes_inicio, mes_fin)

            self.limpiar_graficos()

            if productos:
                nombres = [p["nombre"] for p in productos]
                cantidades = [p["cantidad"] for p in productos]
                fig1 = Figure(figsize=(6, 5))
                ax1 = fig1.add_subplot(111)
                ax1.pie(cantidades, labels=nombres, autopct="%1.1f%%", startangle=140, textprops={'fontsize': 14})
                ax1.set_title("Productos más vendidos", fontsize=16)
                canvas1 = FigureCanvas(fig1)
                self.widgetGraficoPastel.layout().addWidget(canvas1)

            if ganancia_mensual:
                meses = [self.meses_texto[int(item["mes"]) - 1] for item in ganancia_mensual]
                ganancias = [item["ganancia"] for item in ganancia_mensual]
                fig2 = Figure(figsize=(6, 5))
                ax2 = fig2.add_subplot(111)
                ax2.bar(meses, ganancias, color="#4CAF50")
                ax2.set_title("Ganancia neta mensual", fontsize=16)
                ax2.set_xlabel("Mes", fontsize=14)
                ax2.set_ylabel("Ganancia", fontsize=14)
                ax2.tick_params(axis='x', labelsize=12)
                ax2.tick_params(axis='y', labelsize=12)
                canvas2 = FigureCanvas(fig2)
                self.widgetGraficoLinea.layout().addWidget(canvas2)

        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Ocurrió un error:\n{e}")

    def limpiar_graficos(self):
        for widget in [self.widgetGraficoPastel, self.widgetGraficoLinea]:
            layout = widget.layout()
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

    def regresar_a_menu(self):
        if hasattr(self, 'menu_admin_window'):
            self.menu_admin_window.show()
            self.ventana.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RGanancia = QtWidgets.QWidget()
    ui = Ui_RGanancia()
    ui.setupUi(RGanancia)
    RGanancia.showMaximized()
    sys.exit(app.exec_())