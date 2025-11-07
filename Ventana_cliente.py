from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from controllers.factura_controller import FacturaController
from pdf_generator import PDFGenerator
import pyttsx3
from DatabaseConnection import DatabaseConnection


class AccessibleLineEdit(QtWidgets.QLineEdit):
    def __init__(self, texto, lector_funcion, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.texto = texto
        self.leer_funcion = lector_funcion

    def focusInEvent(self, event):
        super().focusInEvent(event)
        if callable(self.leer_funcion):
            self.leer_funcion(self.texto)


class AccessibleComboBox(QtWidgets.QComboBox):
    def __init__(self, texto, lector_funcion, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.texto = texto
        self.leer_funcion = lector_funcion

    def focusInEvent(self, event):
        super().focusInEvent(event)
        if callable(self.leer_funcion):
            self.leer_funcion(self.texto)


class Ui_Facturacion(object):
    def setupUi(self, Facturacion):
        self.window = Facturacion
        self.engine = pyttsx3.init()
        self.accesibilidad_activa = False

        Facturacion.setObjectName("Facturacion")
        Facturacion.resize(950, 700)
        Facturacion.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e0f7fa, stop: 1 white);
                font-family: 'Segoe UI';
                font-size: 16px;
            }
            QLineEdit, QComboBox {
                padding: 6px; /* o incluso 4px */
                border: 2px solid #ccc;
                border-radius: 8px;
            }

            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 12px 20px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        self.verticalLayoutWidget = QtWidgets.QWidget(Facturacion)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)

        self.headerLayout = QtWidgets.QHBoxLayout()
        self.lblticket = QtWidgets.QLabel("Id del ticket:")
        self.txtid_ticket = AccessibleLineEdit("Campo para escribir el número de ticket", self.leer)
        self.btnBuscar = QtWidgets.QPushButton("Buscar")
        self.btnBuscar.clicked.connect(self.buscar_ticket)
        self.headerLayout.addWidget(self.lblticket)
        self.headerLayout.addWidget(self.txtid_ticket)
        self.headerLayout.addWidget(self.btnBuscar)
        self.verticalLayout.addLayout(self.headerLayout)

        self.tablaResumen = QtWidgets.QTableWidget()
        self.tablaResumen.setMinimumHeight(250)
        self.tablaResumen.setColumnCount(4)
        self.tablaResumen.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio Unitario", "Subtotal"])
        self.tablaResumen.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.verticalLayout.addWidget(self.tablaResumen)

        self.formLayout = QtWidgets.QFormLayout()
        self.txtNombre = AccessibleLineEdit("Nombre", self.leer)
        self.txtApellidoPat = AccessibleLineEdit("Apellido Paterno", self.leer)
        self.txtApellidoMat = AccessibleLineEdit("Apellido Materno", self.leer)
        self.txtRFC = AccessibleLineEdit("RFC", self.leer)
        self.txtCalle = AccessibleLineEdit("Calle", self.leer)
        self.spbExterior = QtWidgets.QSpinBox()
        self.spbInterior = QtWidgets.QSpinBox()
        self.txtCP = AccessibleLineEdit("Código Postal", self.leer)
        self.txtAlcaldia = AccessibleLineEdit("Alcaldía", self.leer)
        self.txtEmail = AccessibleLineEdit("Correo electrónico", self.leer)
        self.comboBox = AccessibleComboBox("Estado", self.leer)
        self.comboBox.addItems(["CDMX", "Edo. Mex"])
        self.cmbCFDI = AccessibleComboBox("Uso de CFDI", self.leer)
        self.cmbCFDI.addItems(["Adquisición de mercancías (G01)", "Gastos en general (G03)"])
        self.cmbRegimen = AccessibleComboBox("Régimen fiscal", self.leer)

        regimenes = [
            "601 - General de Ley Personas Morales",
            "603 - Personas Morales con Fines no Lucrativos",
            "605 - Sueldos y Salarios e Ingresos Asimilados a Salarios",
            "606 - Arrendamiento",
            "607 - Régimen de Enajenación o Adquisición de Bienes",
            "608 - Demás ingresos",
            "610 - Residentes en el Extranjero sin Establecimiento Permanente en México",
            "611 - Ingresos por Dividendos (socios y accionistas)",
            "612 - Personas Físicas con Actividades Empresariales y Profesionales",
            "614 - Ingresos por intereses",
            "615 - Régimen de los ingresos por obtención de premios",
            "616 - Sin obligaciones fiscales",
            "620 - Sociedades Cooperativas de Producción que optan por diferir sus ingresos",
            "621 - Incorporación Fiscal",
            "622 - Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras",
            "623 - Opcional para Grupos de Sociedades",
            "624 - Coordinados",
            "625 - Régimen de las Actividades Empresariales con ingresos a través de Plataformas Tecnológicas",
            "626 - Régimen Simplificado de Confianza (RESICO)"
        ]
        self.cmbRegimen.clear()
        self.cmbRegimen.addItems(regimenes)
        self.cmbRegimen.currentTextChanged.connect(lambda text: self.leer(text))

        campos = [
            ("Nombre", self.txtNombre),
            ("Apellido Paterno", self.txtApellidoPat),
            ("Apellido Materno", self.txtApellidoMat),
            ("RFC", self.txtRFC),
            ("Calle", self.txtCalle),
            ("Número Exterior", self.spbExterior),
            ("Número Interior", self.spbInterior),
            ("Estado", self.comboBox),
            ("Código Postal", self.txtCP),
            ("Alcaldía", self.txtAlcaldia),
            ("Uso CFDI", self.cmbCFDI),
            ("Régimen Fiscal", self.cmbRegimen),
            ("Correo Electrónico", self.txtEmail),
        ]

        for i, (etiqueta, campo) in enumerate(campos):
            self.formLayout.setWidget(i, QtWidgets.QFormLayout.LabelRole, QtWidgets.QLabel(etiqueta))
            self.formLayout.setWidget(i, QtWidgets.QFormLayout.FieldRole, campo)

        self.verticalLayout.addLayout(self.formLayout)

        # Botones en horizontal
        botonesLayout = QtWidgets.QHBoxLayout()
        self.btnFactura = QtWidgets.QPushButton("Generar Factura")
        self.btnFactura.clicked.connect(self.generar_factura)
        self.btnAccesibilidad = QtWidgets.QPushButton("Activar accesibilidad")
        self.btnAccesibilidad.setCheckable(True)
        self.btnAccesibilidad.toggled.connect(self.toggle_accesibilidad)
        botonesLayout.addWidget(self.btnFactura)
        botonesLayout.addWidget(self.btnAccesibilidad)
        self.verticalLayout.addLayout(botonesLayout)

        layout = QtWidgets.QVBoxLayout(Facturacion)
        layout.addWidget(self.verticalLayoutWidget)
        Facturacion.setLayout(layout)
        Facturacion.setWindowState(QtCore.Qt.WindowMaximized)

        self.controller = FacturaController()

    def leer(self, texto):
        if not self.accesibilidad_activa:
            return
        try:
            self.engine.say(texto)
            self.engine.runAndWait()
        except:
            self.engine = pyttsx3.init()
            self.engine.say(texto)
            self.engine.runAndWait()

    def toggle_accesibilidad(self, estado):
        self.accesibilidad_activa = estado
        if estado:
            self.btnAccesibilidad.setText("Desactivar accesibilidad")
            self.leer("Modo accesible activado")
        else:
            self.btnAccesibilidad.setText("Activar accesibilidad")
            self.leer("Modo accesible desactivado")

    def buscar_ticket(self):
        ticket = self.txtid_ticket.text().strip()
        if not ticket.isdigit():
            QMessageBox.warning(None, "Error", "Por favor, ingresa un número de ticket válido.")
            return

        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.nombre, dv.cantidad, dv.precio, (dv.cantidad * dv.precio) AS subtotal
            FROM Detalle_Venta dv
            JOIN Producto p ON dv.cve_inventario = p.cve_producto
            WHERE dv.cve_venta = ?
        """, (ticket,))
        rows = cursor.fetchall()

        if not rows:
            QMessageBox.warning(None, "No encontrado", "No se encontró ninguna venta con ese ticket.")
            self.tablaResumen.setRowCount(0)
            return

        self.tablaResumen.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tablaResumen.setItem(i, 0, QtWidgets.QTableWidgetItem(row["nombre"]))
            self.tablaResumen.setItem(i, 1, QtWidgets.QTableWidgetItem(str(row["cantidad"])))
            self.tablaResumen.setItem(i, 2, QtWidgets.QTableWidgetItem(f"${row['precio']:.2f}"))
            self.tablaResumen.setItem(i, 3, QtWidgets.QTableWidgetItem(f"${row['subtotal']:.2f}"))

    def generar_factura(self):
        try:
            datos_cliente = {
                'nombre': self.txtNombre.text().strip(),
                'ap_p': self.txtApellidoPat.text().strip(),
                'ap_m': self.txtApellidoMat.text().strip(),
                'rfc': self.txtRFC.text().strip(),
                'correo': self.txtEmail.text().strip(),
                'uso_cfdi': self.cmbCFDI.currentText(),
                'regimen': self.cmbRegimen.currentText(),
            }

            productos = []
            for i in range(self.tablaResumen.rowCount()):
                productos.append({
                    'nombre': self.tablaResumen.item(i, 0).text(),
                    'cantidad': int(self.tablaResumen.item(i, 1).text()),
                    'precio': float(self.tablaResumen.item(i, 2).text().replace('$', '')),
                    'subtotal': float(self.tablaResumen.item(i, 3).text().replace('$', '')),
                })

            total = self.obtener_total_tabla()
            cve_venta = int(self.txtid_ticket.text().strip())

            datos_db = {
                **datos_cliente,
                'calle': self.txtCalle.text().strip(),
                'num_ext': self.spbExterior.value(),
                'num_int': self.spbInterior.value(),
                'estado': self.comboBox.currentText(),
                'cp': self.txtCP.text().strip(),
                'alcaldia': self.txtAlcaldia.text().strip(),
                'cve_venta': cve_venta,
                'monto': total
            }

            factura_id = self.controller.generar_factura(datos_db)
            if factura_id:
                nombre_archivo = f"Factura_{factura_id}"
                pdf_gen = PDFGenerator()
                ruta_pdf = pdf_gen.generar_factura_pdf(datos_cliente, productos, total, nombre_archivo)
                pdf_gen.enviar_factura_por_correo(datos_cliente['correo'], ruta_pdf)
                self.limpiar_campos()
                QMessageBox.information(None, "Éxito", "Factura generada y enviada correctamente.")
            else:
                QMessageBox.warning(None, "Advertencia", "No se pudo generar la factura.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Ocurrió un error:\n{e}")

    def obtener_total_tabla(self):
        total = 0
        for i in range(self.tablaResumen.rowCount()):
            subtotal_str = self.tablaResumen.item(i, 3).text().replace("$", "").strip()
            total += float(subtotal_str)
        return total

    def limpiar_campos(self):
        self.txtid_ticket.clear()
        self.tablaResumen.setRowCount(0)
        self.txtNombre.clear()
        self.txtApellidoPat.clear()
        self.txtApellidoMat.clear()
        self.txtRFC.clear()
        self.txtCalle.clear()
        self.txtCP.clear()
        self.txtAlcaldia.clear()
        self.txtEmail.clear()
        self.spbExterior.setValue(0)
        self.spbInterior.setValue(0)
        self.comboBox.setCurrentIndex(0)
        self.cmbCFDI.setCurrentIndex(0)
        self.cmbRegimen.setCurrentIndex(0)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Facturacion = QtWidgets.QWidget()
    ui = Ui_Facturacion()
    ui.setupUi(Facturacion)
    Facturacion.showMaximized()
    sys.exit(app.exec_())
