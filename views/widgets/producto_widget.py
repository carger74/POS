from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QSpinBox, QPushButton

class ProductoWidget(QGroupBox):
    def __init__(self, producto, callback_agregar):
        super().__init__(producto.nombre)
        self.producto = producto
        self.callback_agregar = callback_agregar

        layout = QVBoxLayout(self)

        self.lblPrecioMenudeo = QLabel(f"Menudeo: ${producto.precio_menudeo}")
        self.lblPrecioMayoreo = QLabel(f"Mayoreo: ${producto.precio_mayoreo}")
        self.spinCantidad = QSpinBox()
        self.spinCantidad.setRange(1, 999)
        self.btnAgregar = QPushButton("Agregar")

        layout.addWidget(self.lblPrecioMenudeo)
        layout.addWidget(self.lblPrecioMayoreo)
        layout.addWidget(QLabel("Cantidad:"))
        layout.addWidget(self.spinCantidad)
        layout.addWidget(self.btnAgregar)

        self.btnAgregar.clicked.connect(self.agregar_a_venta)

    def agregar_a_venta(self):
        cantidad = self.spinCantidad.value()
        precio = self.producto.precio_mayoreo if cantidad >= 10 else self.producto.precio_menudeo
        subtotal = cantidad * precio
        self.callback_agregar(self.producto, cantidad, precio, subtotal)
