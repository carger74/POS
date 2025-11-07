from PyQt5.QtWidgets import QMessageBox

class AlertaStock:
    def notificar(self, producto):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("¡Stock Bajo!")
        msg.setText(f"⚠️ El producto '{producto.nombre}' tiene solo {producto.stock} unidades disponibles.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
