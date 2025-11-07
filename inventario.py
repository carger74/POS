from PyQt5 import QtCore, QtGui, QtWidgets
import pyttsx3
from Facade import SistemaVentas
from PyQt5.QtWidgets import QMessageBox

class Ui_Inventario(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario")
        self.accesibilidad_activada = False
        self.engine = pyttsx3.init()
        self.facade = SistemaVentas()

        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI';
                background-color: #f0f2f5;
                font-size: 18px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 14px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                font-weight: bold;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                padding: 6px;
                border-radius: 6px;
                border: 1px solid #ccc;
                background: white;
            }
        """)

        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.tablInventario = QtWidgets.QTableWidget()
        self.tablInventario.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tablInventario.setColumnCount(6)
        self.tablInventario.setHorizontalHeaderLabels(["Producto", "Costo", "Mayoreo", "Menudeo", "Stock", "Eliminar"])
        self.tablInventario.horizontalHeader().setStretchLastSection(True)
        self.tablInventario.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.mainLayout.addWidget(self.tablInventario)

        self.formGroup = QtWidgets.QGroupBox("Agregar producto")
        self.formLayout = QtWidgets.QFormLayout(self.formGroup)

        self.txtnombre = QtWidgets.QLineEdit()
        self.spnCosto = QtWidgets.QDoubleSpinBox()
        self.spnCosto.setMaximum(99999.99)
        self.spnMayoreo = QtWidgets.QDoubleSpinBox()
        self.spnMayoreo.setMaximum(99999.99)
        self.spnMenudeo = QtWidgets.QDoubleSpinBox()
        self.spnMenudeo.setMaximum(99999.99)
        self.spnCantidad = QtWidgets.QSpinBox()

        self.formLayout.addRow("Nombre:", self.txtnombre)
        self.formLayout.addRow("Costo:", self.spnCosto)
        self.formLayout.addRow("Mayoreo:", self.spnMayoreo)
        self.formLayout.addRow("Menudeo:", self.spnMenudeo)
        self.formLayout.addRow("Cantidad:", self.spnCantidad)

        self.btnAgregar = QtWidgets.QPushButton("Agregar")
        self.btnRegresar = QtWidgets.QPushButton("Regresar")
        self.btnAccesibilidad = QtWidgets.QPushButton("🔈 Accesibilidad (desactivado)")

        self.btnAgregar.clicked.connect(self.agregar_producto)
        self.btnRegresar.clicked.connect(self.regresar_a_menu)
        self.btnAccesibilidad.clicked.connect(self.toggle_accesibilidad)

        btnsLayout = QtWidgets.QHBoxLayout()
        btnsLayout.addWidget(self.btnRegresar)
        btnsLayout.addWidget(self.btnAccesibilidad)

        self.formLayout.addRow(self.btnAgregar)
        self.formLayout.addRow(btnsLayout)

        self.mainLayout.addWidget(self.formGroup)

        self.cargar_tabla_inventario()

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

    def cargar_tabla_inventario(self):
        self.tablInventario.setRowCount(0)
        productos = self.facade.obtener_inventario()

        for i, prod in enumerate(productos):
            self.tablInventario.insertRow(i)
            self.tablInventario.setItem(i, 0, QtWidgets.QTableWidgetItem(prod.nombre))

            def crear_spinbox(valor, campo):
                spin = QtWidgets.QDoubleSpinBox() if campo != "stock" else QtWidgets.QSpinBox()
                spin.setMaximum(999999.99 if campo != "stock" else 99999)
                spin.setValue(valor)
                spin.setProperty("cve_producto", prod.cve_producto)
                spin.editingFinished.connect(lambda s=spin: self.actualizar_valor(s, campo))
                return spin

            self.tablInventario.setCellWidget(i, 1, crear_spinbox(prod.costo, "costo"))
            self.tablInventario.setCellWidget(i, 2, crear_spinbox(prod.precio_mayoreo, "precio_mayoreo"))
            self.tablInventario.setCellWidget(i, 3, crear_spinbox(prod.precio_menudeo, "precio_menudeo"))
            self.tablInventario.setCellWidget(i, 4, crear_spinbox(prod.stock, "stock"))

            # Botón eliminar
            btnEliminar = QtWidgets.QPushButton("❌")
            btnEliminar.setProperty("cve_producto", prod.cve_producto)
            btnEliminar.clicked.connect(self.confirmar_eliminacion)
            self.tablInventario.setCellWidget(i, 5, btnEliminar)

    def confirmar_eliminacion(self):
        boton = self.sender()
        cve_producto = boton.property("cve_producto")
        reply = QMessageBox.question(self, "Confirmar", "¿Seguro que deseas eliminar este producto?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.facade.eliminar_producto(cve_producto)
            QMessageBox.information(self, "Eliminado", "Producto eliminado correctamente.")
            self.cargar_tabla_inventario()

    def actualizar_valor(self, spinbox, campo):
        cve_producto = spinbox.property("cve_producto")
        valor = spinbox.value()
        try:
            if campo == "stock":
                self.facade.actualizar_stock(cve_producto, valor)
            else:
                self.facade.actualizar_precio_o_costo(cve_producto, campo, valor)
            QMessageBox.information(None, "Éxito", f"{campo.capitalize()} actualizado: {valor:.2f}")
            self.leer(f"{campo} actualizado a {valor}")
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))

    def agregar_producto(self):
        nombre = self.txtnombre.text().strip()
        costo = self.spnCosto.value()
        mayoreo = self.spnMayoreo.value()
        menudeo = self.spnMenudeo.value()
        cantidad = self.spnCantidad.value()

        if not nombre or costo <= 0 or mayoreo <= 0 or menudeo <= 0 or cantidad <= 0:
            QMessageBox.warning(None, "Campos inválidos", "Llena todos los campos con valores válidos.")
            return

        ok = self.facade.agregar_producto(nombre, costo, mayoreo, menudeo, cantidad)
        if ok:
            QMessageBox.information(None, "Agregado", "Producto agregado correctamente.")
            self.leer(f"{nombre} agregado al inventario")
            self.txtnombre.clear()
            self.spnCosto.setValue(0)
            self.spnMayoreo.setValue(0)
            self.spnMenudeo.setValue(0)
            self.spnCantidad.setValue(0)
            self.cargar_tabla_inventario()

    def regresar_a_menu(self):
        if hasattr(self, 'menu_admin_window'):
            self.menu_admin_window.show()
            self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ui_Inventario()
    ventana.showMaximized()
    sys.exit(app.exec_())
