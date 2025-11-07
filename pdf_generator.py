from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os


class PDFGenerator:
    def generar_factura_pdf(self, datos_cliente, productos, total, nombre_archivo):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Factura Electrónica", ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        pdf.cell(0, 10, "Datos del Cliente:", ln=True)
        pdf.set_font("Arial", "", 11)

        pdf.cell(0, 8, f"Nombre: {datos_cliente['nombre']} {datos_cliente['ap_p']} {datos_cliente['ap_m']}", ln=True)
        pdf.cell(0, 8, f"RFC: {datos_cliente['rfc']}", ln=True)
        pdf.cell(0, 8, f"Correo: {datos_cliente['correo']}", ln=True)
        pdf.cell(0, 8, f"Uso CFDI: {datos_cliente['uso_cfdi']}", ln=True)
        pdf.cell(0, 8, f"Régimen Fiscal: {datos_cliente['regimen']}", ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Resumen de productos:", ln=True)
        pdf.set_font("Arial", "", 11)

        pdf.cell(60, 8, "Producto", 1)
        pdf.cell(30, 8, "Cantidad", 1)
        pdf.cell(40, 8, "Precio Unitario", 1)
        pdf.cell(40, 8, "Subtotal", 1)
        pdf.ln()

        for p in productos:
            pdf.cell(60, 8, p['nombre'], 1)
            pdf.cell(30, 8, str(p['cantidad']), 1)
            pdf.cell(40, 8, f"${p['precio']:.2f}", 1)
            pdf.cell(40, 8, f"${p['subtotal']:.2f}", 1)
            pdf.ln()

        pdf.set_font("Arial", "B", 12)
        pdf.cell(130, 10, "Total", 1)
        pdf.cell(40, 10, f"${total:.2f}", 1)

        ruta_archivo = os.path.join(os.getcwd(), f"{nombre_archivo}.pdf")
        pdf.output(ruta_archivo)

        return ruta_archivo

    def enviar_factura_por_correo(self, correo_destino, ruta_pdf):
        remitente = "careboss1@gmail.com"
        password = "zcpo xccq wskq gqrd"  # Usa una contraseña de app de Gmail



        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = correo_destino
        mensaje['Subject'] = "Factura generada - Punto de Venta"

        cuerpo = MIMEText("Adjunto a este correo encontrará su factura solicitada. ¡Gracias por su compra!", 'plain')
        mensaje.attach(cuerpo)

        with open(ruta_pdf, "rb") as f:
            archivo_pdf = MIMEApplication(f.read(), _subtype="pdf")
            archivo_pdf.add_header('Content-Disposition', 'attachment', filename=os.path.basename(ruta_pdf))
            mensaje.attach(archivo_pdf)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, password)
            servidor.send_message(mensaje)

        return True
