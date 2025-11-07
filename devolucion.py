from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem
import pyttsx3
from Facade import SistemaVentas

class AccessibleLineEdit(QtWidgets.QLineEdit):
    def __init__(self, texto_a_leer, lector_funcion, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.texto_a_leer = texto_a_leer
        self.leer_funcion = lector_funcion

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.leer_funcion(self.texto_a_leer)



class AccessibleButton(QtWidgets.QPushButton):
    def __init__(self, texto_a_leer, lector_funcion, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.texto_a_leer = texto_a_leer
        self.leer_funcion = lector_funcion

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.leer_funcion(self.texto_a_leer)



class Ui_Devolucion(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Devolución")
        self.setObjectName("Devolucion")
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI';
                background-color: #f0f2f5;
                font-size: 18px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                font-weight: bold;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 6px;
                background-color: white;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
        """)

        self.accesibilidad_activada = False
        self.engine = pyttsx3.init()
        self.facade = SistemaVentas()

        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        # Número de Ticket
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.lbNTicket = QtWidgets.QLabel("Número de Ticket:")
        self.horizontalLayout.addWidget(self.lbNTicket)

        self.txtNumTicket = AccessibleLineEdit("Campo número de ticket", self.leer)
        self.txtNumTicket.setValidator(QIntValidator(0, 999999))
        self.txtNumTicket.setMaxLength(6)
        self.txtNumTicket.setMinimumHeight(30)
        self.horizontalLayout.addWidget(self.txtNumTicket)

        self.btnBuscarT = AccessibleButton("Botón buscar ticket", self.leer)
        self.btnBuscarT.setText("Buscar")
        self.horizontalLayout.addWidget(self.btnBuscarT)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # Línea divisoria
        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)

        # Lista de productos
        self.ListaProductos = QtWidgets.QListWidget()
        self.verticalLayout.addWidget(self.ListaProductos)

        # Botones inferiores
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.btnDevolucion = AccessibleButton("Botón devolución", self.leer)
        self.btnDevolucion.setText("Devolución")
        self.btnSalir = AccessibleButton("Botón salir", self.leer)
        self.btnSalir.setText("Salir")
        self.btnAccesibilidad = QtWidgets.QPushButton("🔈 Accesibilidad (desactivado)")

        self.bottomLayout.addWidget(self.btnDevolucion)
        self.bottomLayout.addWidget(self.btnSalir)
        self.bottomLayout.addWidget(self.btnAccesibilidad)

        self.verticalLayout.addLayout(self.bottomLayout)

        # Conexiones
        self.btnSalir.clicked.connect(self.regresar_a_menu)
        self.btnBuscarT.clicked.connect(self.buscar_ticket)
        self.btnDevolucion.clicked.connect(self.devolver_productos)
        self.btnAccesibilidad.clicked.connect(self.toggle_accesibilidad)


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

    def regresar_a_menu(self):
        if hasattr(self, 'menu_trabajador_window'):
            self.menu_trabajador_window.show()
            self.close()

    def buscar_ticket(self):
        self.ListaProductos.clear()
        id_ticket = self.txtNumTicket.text().strip()

        if not id_ticket:
            QMessageBox.warning(self, "Campo vacío", "Ingresa un número de ticket.")
            self.leer("Por favor, ingresa un número de ticket.")
            return

        productos = self.facade.obtener_productos_de_ticket(int(id_ticket))

        if not productos:
            QMessageBox.information(self, "No encontrado", "No se encontraron productos para ese ticket.")
            self.leer("No se encontraron productos para ese ticket.")
            return

        self.leer(f"Se encontraron {len(productos)} productos.")
        for prod in productos:
            item_text = f"{prod['nombre']} - Vendido: {prod['cantidad']} - Precio: ${prod['precio_menudeo']:.2f}"
            item = QListWidgetItem(item_text)
            item.setData(QtCore.Qt.UserRole, {
                "id_producto": prod["id_producto"],
                "cantidad_vendida": prod["cantidad"]
            })
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.ListaProductos.addItem(item)

    def devolver_productos(self):
        id_ticket = self.txtNumTicket.text().strip()
        if not id_ticket:
            QMessageBox.warning(self, "Campo vacío", "Ingresa el número de ticket.")
            self.leer("Campo número de ticket vacío.")
            return

        devoluciones_realizadas = 0

        for i in range(self.ListaProductos.count()):
            item = self.ListaProductos.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                datos = item.data(QtCore.Qt.UserRole)
                id_producto = datos["id_producto"]

                cantidad, ok = QtWidgets.QInputDialog.getInt(
                    self,
                    "Cantidad a devolver",
                    f"¿Cuántas unidades de '{item.text()}' quieres devolver?",
                    1, 1, datos["cantidad_vendida"]
                )

                if ok:
                    success, msg = self.facade.procesar_devolucion(int(id_ticket), id_producto, cantidad)
                    if success:
                        devoluciones_realizadas += 1
                    else:
                        QMessageBox.warning(self, "Error al devolver", msg)
                        self.leer(f"No se pudo devolver {cantidad} unidades de {item.text()}")

        if devoluciones_realizadas > 0:
            QMessageBox.information(self, "Devolución completa", "Se procesaron las devoluciones.")
            self.leer("Se procesaron las devoluciones.")
            self.ListaProductos.clear()
            self.txtNumTicket.clear()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Devolucion = Ui_Devolucion()
    Devolucion.showMaximized()
    sys.exit(app.exec_())
