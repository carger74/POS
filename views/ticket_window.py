from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
from datetime import datetime

class TicketWindow(QDialog):
    def __init__(self, cliente, metodo_pago, productos_seleccionados, total, cve_venta, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ticket de Venta")
        self.resize(500, 500)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"Ticket ID: {cve_venta}"))
        layout.addWidget(QLabel(f"Cliente: {cliente}"))
        layout.addWidget(QLabel(f"Método de pago: {metodo_pago}"))
        layout.addWidget(QLabel(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))

        tabla = QTableWidget(len(productos_seleccionados), 4)
        tabla.setHorizontalHeaderLabels(["Producto", "Precio Unitario", "Cantidad", "Subtotal"])
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, (producto, cantidad, precio, subtotal) in enumerate(productos_seleccionados):
            tabla.setItem(i, 0, QTableWidgetItem(producto.nombre))
            tabla.setItem(i, 1, QTableWidgetItem(f"${precio:.2f}"))
            tabla.setItem(i, 2, QTableWidgetItem(str(cantidad)))
            tabla.setItem(i, 3, QTableWidgetItem(f"${subtotal:.2f}"))

        layout.addWidget(tabla)
        layout.addWidget(QLabel(f"Monto total: ${total:.2f}"))

        cerrar_btn = QPushButton("Cerrar")
        cerrar_btn.clicked.connect(self.accept)
        layout.addWidget(cerrar_btn)
