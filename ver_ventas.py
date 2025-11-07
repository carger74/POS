from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItem, QStandardItemModel
import pyttsx3
import datetime

from PyQt5.QtWidgets import QMessageBox

from Facade import SistemaVentas

class Ui_VerVentas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ver Ventas")
        self.setObjectName("VerVentas")
        self.engine = pyttsx3.init()
        self.accesibilidad_activada = False

        # Estilo visual moderno
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', 'Arial';
                background-color: #f4f6f9;
                font-size: 16px;
            }
            QLabel {
                font-weight: bold;
            }
            QComboBox {
                padding: 10px;
                font-size: 18px;
            }
            QTableView {
                background: white;
                border-radius: 10px;
                font-size: 17px;
                border: 1px solid #ccc;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 20px;
                padding: 16px;
                margin-top: 20px;
                min-width: 300px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(40, 30, 40, 30)


        self.lbTitulo = QtWidgets.QLabel("Historial de Ventas")
        self.lbTitulo.setAlignment(QtCore.Qt.AlignCenter)
        self.lbTitulo.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        self.mainLayout.addWidget(self.lbTitulo)

        self.mainLayout.addWidget(self._crear_linea())


        self.lborderpor = QtWidgets.QLabel("Ordenar por:")
        self.cmbFecha = QtWidgets.QComboBox()
        self.cmbFecha.addItems(["Fecha", "Monto"])

        criterioLayout = QtWidgets.QHBoxLayout()
        criterioLayout.addWidget(self.lborderpor)
        criterioLayout.addWidget(self.cmbFecha)
        self.mainLayout.addLayout(criterioLayout)


        self.mainLayout.addWidget(self._crear_linea())
        self.tableVentas = QtWidgets.QTableView()
        self.mainLayout.addWidget(self.tableVentas)
        self.mainLayout.addWidget(self._crear_linea())


        botonesLayout = QtWidgets.QHBoxLayout()
        self.btnAccesibilidad = QtWidgets.QPushButton("🔈 Accesibilidad (desactivado)")
        self.btnRegresar = QtWidgets.QPushButton("Regresar")

        botonesLayout.addStretch()
        botonesLayout.addWidget(self.btnAccesibilidad)
        botonesLayout.addWidget(self.btnRegresar)
        botonesLayout.addStretch()
        self.mainLayout.addLayout(botonesLayout)


        self.facade = SistemaVentas()
        self.cmbFecha.currentIndexChanged.connect(self.cargar_ventas)
        self.btnRegresar.clicked.connect(self.regresar_a_menu)
        self.btnAccesibilidad.clicked.connect(self.toggle_accesibilidad)
        self.cmbFecha.highlighted.connect(lambda index: self.leer(f"Opción {self.cmbFecha.itemText(index)}"))

        self.cargar_ventas()

    def _crear_linea(self):
        linea = QtWidgets.QFrame()
        linea.setFrameShape(QtWidgets.QFrame.HLine)
        linea.setFrameShadow(QtWidgets.QFrame.Sunken)
        return linea

    def toggle_accesibilidad(self):
        self.accesibilidad_activada = not self.accesibilidad_activada
        estado = "activado" if self.accesibilidad_activada else "desactivado"
        self.btnAccesibilidad.setText(f"🔈 Accesibilidad ({estado})")
        self.leer(f"Modo accesibilidad {estado}")

    def leer(self, texto):
        if self.accesibilidad_activada:
            self.engine.stop()
            self.engine.say(texto)
            self.engine.runAndWait()

    def cargar_ventas(self):
        criterio = self.cmbFecha.currentText().lower()
        ventas = self.facade.obtener_ventas_ordenadas(criterio)

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ID Ticket", "Fecha", "Total", "Empleado"])

        for row in ventas:
            fecha = datetime.datetime.fromtimestamp(row["fecha_venta"]).strftime("%Y-%m-%d %H:%M")
            model.appendRow([
                QStandardItem(str(row["cve_venta"])),
                QStandardItem(fecha),
                QStandardItem(f"${row['total']:.2f}"),
                QStandardItem(row["empleado"])
            ])

        self.tableVentas.setModel(model)
        self.tableVentas.clicked.connect(self.mostrar_detalle_ticket)

        self.leer(f"{len(ventas)} ventas cargadas ordenadas por {criterio}")

    def regresar_a_menu(self):
        if hasattr(self, 'menu_admin_window'):
            self.menu_admin_window.show()
            self.close()

    def mostrar_detalle_ticket(self, index):
        fila = index.row()
        id_ticket = self.tableVentas.model().item(fila, 0).text()

        try:
            detalles = self.facade.obtener_detalles_ticket(int(id_ticket))
            if not detalles:
                QMessageBox.information(self, "Detalle vacío", "No hay productos asociados a este ticket.")
                return

            mensaje = f"Ticket #{id_ticket}:\n\n"
            for d in detalles:
                mensaje += f"• {d['nombre']} - {d['cantidad']} x ${d['precio']:.2f} = ${d['subtotal']:.2f}\n"
            total = sum([d["subtotal"] for d in detalles])
            mensaje += f"\nTotal: ${total:.2f}"

            QMessageBox.information(self, "Detalle de venta", mensaje)

            self.leer(f"Mostrando detalle del ticket {id_ticket}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el detalle: {e}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ui_VerVentas()
    ventana.showMaximized()
    sys.exit(app.exec_())
