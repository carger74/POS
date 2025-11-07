from PyQt5 import QtCore, QtGui, QtWidgets
import pyttsx3
from Facade import SistemaVentas

class AccessibleLineEdit(QtWidgets.QLineEdit):
    def __init__(self, label_text, speak_func):
        super().__init__()
        self.label_text = label_text
        self.speak_func = speak_func

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.speak_func(self.label_text)

class AccessibleComboBox(QtWidgets.QComboBox):
    def __init__(self, label_text, speak_func):
        super().__init__()
        self.label_text = label_text
        self.speak_func = speak_func
        self.currentIndexChanged.connect(self.on_index_changed)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.speak_func(self.label_text)

    def on_index_changed(self, index):
        self.speak_func(f"{self.label_text}: {self.itemText(index)}")

class AccessibleButton(QtWidgets.QPushButton):
    def __init__(self, label_text, speak_func, text):
        super().__init__(text)
        self.label_text = label_text
        self.speak_func = speak_func

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.speak_func(self.label_text)

class Ui_Registro_Usuario(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro Usuario")
        self.accesibilidad_activada = False  # Accesibilidad desactivada por defecto
        self.engine = pyttsx3.init()
        self.facade = SistemaVentas()

        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI';
                background-color: #eef1f5;
                font-size: 16px;
            }
            QLabel {
                font-weight: bold;
                font-size: 18px;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                font-size: 16px;
                border-radius: 6px;
                border: 1px solid #ccc;
                background-color: white;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 12px;
                font-size: 16px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        self.layoutPrincipal = QtWidgets.QVBoxLayout(self)
        self.layoutPrincipal.setContentsMargins(40, 40, 40, 40)
        self.layoutPrincipal.setSpacing(20)

        self.lbusuario = QtWidgets.QLabel("Registro de usuario")
        self.lbusuario.setAlignment(QtCore.Qt.AlignCenter)
        self.lbusuario.setFont(QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold))
        self.layoutPrincipal.addWidget(self.lbusuario)

        self.formLayout = QtWidgets.QFormLayout()
        self.txNombre = AccessibleLineEdit("Nombre", self.leer)
        self.txtAp_p = AccessibleLineEdit("Apellido paterno", self.leer)
        self.txtAp_m = AccessibleLineEdit("Apellido materno", self.leer)
        self.cmbRol = AccessibleComboBox("Rol", self.leer)
        self.cmbRol.addItems(["trabajador", "gerente"])
        self.txtTelefono = AccessibleLineEdit("Teléfono", self.leer)
        self.txtEmail = AccessibleLineEdit("Correo electrónico", self.leer)

        self.formLayout.addRow("Nombre:", self.txNombre)
        self.formLayout.addRow("Apellido paterno:", self.txtAp_p)
        self.formLayout.addRow("Apellido materno:", self.txtAp_m)
        self.formLayout.addRow("Rol:", self.cmbRol)
        self.formLayout.addRow("Teléfono:", self.txtTelefono)
        self.formLayout.addRow("Email:", self.txtEmail)
        self.layoutPrincipal.addLayout(self.formLayout)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.btnAgregar = AccessibleButton("Agregar usuario", self.leer, "Agregar")
        self.btnRegresar = AccessibleButton("Regresar al menú", self.leer, "Regresar")
        self.btnAccesibilidad = QtWidgets.QPushButton("🔈 Accesibilidad (desactivado)")
        self.btnAccesibilidad.clicked.connect(self.toggle_accesibilidad)

        self.buttonLayout.addWidget(self.btnAgregar)
        self.buttonLayout.addWidget(self.btnRegresar)
        self.buttonLayout.addWidget(self.btnAccesibilidad)
        self.layoutPrincipal.addLayout(self.buttonLayout)

        self.btnAgregar.clicked.connect(self.registrar_usuario)
        self.btnRegresar.clicked.connect(self.regresar_a_menu)

    def leer(self, texto):
        if self.accesibilidad_activada:
            self.engine.stop()
            self.engine.say(texto)
            self.engine.runAndWait()

    def toggle_accesibilidad(self):
        self.accesibilidad_activada = not self.accesibilidad_activada
        estado = "activado" if self.accesibilidad_activada else "desactivado"
        self.btnAccesibilidad.setText(f"🔈 Accesibilidad ({estado})")
        self.leer(f"Modo accesibilidad {estado}")

    def registrar_usuario(self):
        nombre = self.txNombre.text().strip()
        ap_p = self.txtAp_p.text().strip()
        ap_m = self.txtAp_m.text().strip()
        rol = self.cmbRol.currentText()
        telefono = self.txtTelefono.text().strip()
        email = self.txtEmail.text().strip()

        if not all([nombre, ap_p, ap_m, rol, telefono, email]):
            QtWidgets.QMessageBox.warning(self, "Faltan campos", "Completa todos los campos")
            self.leer("Completa todos los campos")
            return

        resultado = self.facade.agregar_usuario(nombre, ap_p, ap_m, rol, email, telefono)
        if resultado:
            QtWidgets.QMessageBox.information(self, "Usuario creado",
                                              f" ID: {resultado['id']}\n Contraseña: {resultado['contrasena']}")
            self.leer("Usuario registrado correctamente")
            self.txNombre.clear()
            self.txtAp_p.clear()
            self.txtAp_m.clear()
            self.txtTelefono.clear()
            self.txtEmail.clear()
            self.cmbRol.setCurrentIndex(0)

    def regresar_a_menu(self):
        if hasattr(self, 'menu_admin_window'):
            self.menu_admin_window.show()
        self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = Ui_Registro_Usuario()
    win.showMaximized()
    sys.exit(app.exec_())
