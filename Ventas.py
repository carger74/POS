from PyQt5 import QtCore, QtGui, QtWidgets
from models.producto import Producto
from views.widgets.producto_widget import ProductoWidget
from Facade import SistemaVentas
from PyQt5.QtWidgets import QMessageBox
from views.ticket_window import TicketWindow
import pyttsx3

class Ui_Ventana_ventas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.total = 0
        self.productos_seleccionados = []
        self.engine = pyttsx3.init()
        self.accesibilidad_activada = False

        self.setObjectName("Ventana_ventas")
        self.setWindowTitle("Punto de Venta")
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI';
                font-size: 16px;
                background-color: #f0f2f5;
            }
            QLineEdit, QTableWidget, QTableWidgetItem, QCheckBox {
                font-size: 16px;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
                background-color: #007bff;
                color: white;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.lblBuscarProducto = QtWidgets.QLabel("Buscar producto:")
        self.horizontalLayout.addWidget(self.lblBuscarProducto)

        self.txtproducto = QtWidgets.QLineEdit()
        self.txtproducto.setMinimumHeight(30)
        self.txtproducto.focusInEvent = self.wrap_focus_in(self.txtproducto.focusInEvent, "Buscar producto")
        self.horizontalLayout.addWidget(self.txtproducto)

        self.btnBuscar = QtWidgets.QPushButton("Buscar")
        self.btnBuscar.clicked.connect(self.buscar_producto)
        self.horizontalLayout.addWidget(self.btnBuscar)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line_2 = QtWidgets.QFrame()
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_2)

        self.ScrollContenedor = QtWidgets.QScrollArea()
        self.ScrollContenedor.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.ScrollContenedor.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_5 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.ScrollContenedor)

        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)

        self.tablaTicket = QtWidgets.QTableWidget()
        self.tablaTicket.setColumnCount(5)
        self.tablaTicket.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio", "Subtotal", "Acción"])
        self.tablaTicket.horizontalHeader().setStretchLastSection(True)
        self.tablaTicket.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalLayout.addWidget(self.tablaTicket)

        self.formLayout_2 = QtWidgets.QFormLayout()

        self.lbMonto = QtWidgets.QLabel("Monto:")
        self.lbMontoTotal = QtWidgets.QLabel("$0.00")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbMonto)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lbMontoTotal)

        self.label = QtWidgets.QLabel("Nombre del cliente:")
        self.txtNombreCliente = QtWidgets.QLineEdit()
        self.txtNombreCliente.setMinimumHeight(30)
        self.txtNombreCliente.focusInEvent = self.wrap_focus_in(self.txtNombreCliente.focusInEvent, "Nombre del cliente")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtNombreCliente)

        self.label_2 = QtWidgets.QLabel("Método de pago:")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.checkEfectivo = QtWidgets.QCheckBox("Efectivo")
        self.checkEfectivo.focusInEvent = self.wrap_focus_in(self.checkEfectivo.focusInEvent, "Pago en efectivo")
        self.CheckTarjeta = QtWidgets.QCheckBox("Tarjeta")
        self.CheckTarjeta.focusInEvent = self.wrap_focus_in(self.CheckTarjeta.focusInEvent, "Pago con tarjeta")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.checkEfectivo)
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.CheckTarjeta)

        self.btnTerminar = QtWidgets.QPushButton("Finalizar")
        self.btnTerminar.clicked.connect(self.finalizar_venta)
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.btnTerminar)

        self.btnSalir = QtWidgets.QPushButton("Salir")
        self.btnSalir.clicked.connect(self.regresar_a_menu)
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.btnSalir)

        self.btnAccesibilidad = QtWidgets.QPushButton("🔈 Accesibilidad (desactivado)")
        self.btnAccesibilidad.clicked.connect(self.toggle_accesibilidad)
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.btnAccesibilidad)

        self.verticalLayout.addLayout(self.formLayout_2)

        self.CheckTarjeta.toggled.connect(self.exclusivo_tarjeta)
        self.checkEfectivo.toggled.connect(self.exclusivo_efectivo)

        self.facade = SistemaVentas()

        QtCore.QMetaObject.connectSlotsByName(self)
        self.cargar_productos_en_malla()

    def wrap_focus_in(self, old_event, text):
        def new_event(event):
            self.leer(text)
            return old_event(event)
        return new_event

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

    def exclusivo_tarjeta(self, estado):
        if estado:
            self.checkEfectivo.setChecked(False)

    def exclusivo_efectivo(self, estado):
        if estado:
            self.CheckTarjeta.setChecked(False)

    def cargar_productos_en_malla(self):
        productos = Producto.obtener_todos()
        fila, columna = 0, 0
        for prod in productos:
            widget = ProductoWidget(prod, self.agregar_al_total)
            self.gridLayout_5.addWidget(widget, fila, columna)
            columna += 1
            if columna == 3:
                columna = 0
                fila += 1

    def agregar_al_total(self, producto, cantidad, precio, subtotal):
        self.total += subtotal
        self.lbMontoTotal.setText(f"${self.total:.2f}")
        self.productos_seleccionados.append((producto, cantidad, precio, subtotal))
        self.actualizar_tabla_ticket()

    def finalizar_venta(self):
        if not self.productos_seleccionados:
            QMessageBox.warning(None, "Sin productos", "No hay productos en la venta.")
            return

        id_usuario = 10
        ok, total, cve_venta = self.facade.realizar_venta(self.productos_seleccionados, id_usuario)

        if ok:
            cliente = self.txtNombreCliente.text().strip() or "No especificado"
            metodo = "Efectivo" if self.checkEfectivo.isChecked() else "Tarjeta" if self.CheckTarjeta.isChecked() else "No especificado"
            ticket = TicketWindow(cliente, metodo, self.productos_seleccionados, total, cve_venta)
            ticket.exec_()

            self.lbMontoTotal.setText("$0.00")
            self.total = 0
            self.productos_seleccionados.clear()
            self.txtNombreCliente.clear()
            self.tablaTicket.setRowCount(0)
            self.checkEfectivo.setChecked(False)
            self.CheckTarjeta.setChecked(False)
        else:
            QMessageBox.critical(None, "Error en la venta", f"Ocurrió un error:\n{total}")

    def buscar_producto(self):
        texto = self.txtproducto.text().strip().lower()
        while self.gridLayout_5.count():
            widget = self.gridLayout_5.takeAt(0).widget()
            if widget:
                widget.setParent(None)

        productos = Producto.obtener_todos()
        fila, columna = 0, 0
        for prod in productos:
            if texto in prod.nombre.lower():
                widget = ProductoWidget(prod, self.agregar_al_total)
                self.gridLayout_5.addWidget(widget, fila, columna)
                columna += 1
                if columna == 3:
                    columna = 0
                    fila += 1

    def actualizar_tabla_ticket(self):
        self.tablaTicket.setRowCount(len(self.productos_seleccionados))
        for i, (producto, cantidad, precio, subtotal) in enumerate(self.productos_seleccionados):
            self.tablaTicket.setItem(i, 0, QtWidgets.QTableWidgetItem(producto.nombre))
            self.tablaTicket.setItem(i, 1, QtWidgets.QTableWidgetItem(str(cantidad)))
            self.tablaTicket.setItem(i, 2, QtWidgets.QTableWidgetItem(f"${precio:.2f}"))
            self.tablaTicket.setItem(i, 3, QtWidgets.QTableWidgetItem(f"${subtotal:.2f}"))
            btnEliminar = QtWidgets.QPushButton("❌")
            btnEliminar.clicked.connect(lambda _, index=i: self.eliminar_producto(index))
            self.tablaTicket.setCellWidget(i, 4, btnEliminar)

    def eliminar_producto(self, index):
        producto = self.productos_seleccionados[index]
        self.total -= producto[3]
        del self.productos_seleccionados[index]
        self.lbMontoTotal.setText(f"${self.total:.2f}")
        self.actualizar_tabla_ticket()

    def regresar_a_menu(self):
        if hasattr(self, 'menu_trabajador_window'):
            self.menu_trabajador_window.show()
            self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ui_Ventana_ventas()
    ventana.showMaximized()
    sys.exit(app.exec_())
