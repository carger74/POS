from models.factura import FacturaModel

class FacturaController:
    def __init__(self):
        self.modelo = FacturaModel

    def generar_factura(self, datos):
        estado_id = FacturaModel.insertar_estado(datos['estado'])
        cp_id = FacturaModel.insertar_cp(datos['cp'], estado_id)
        alcaldia_id = FacturaModel.insertar_alcaldia(datos['alcaldia'], cp_id)
        direccion_id = FacturaModel.insertar_direccion(alcaldia_id, datos['calle'], datos['num_ext'], datos['num_int'])
        cliente_id = FacturaModel.insertar_datos_cliente(
            datos['nombre'], datos['ap_p'], datos['ap_m'], datos['rfc'], direccion_id
        )
        factura_id = FacturaModel.insertar_factura(
            datos['cve_venta'], cliente_id, datos['monto'], datos['uso_cfdi'], datos['correo'], datos['regimen']
        )

        return factura_id