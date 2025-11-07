from models.venta import Venta
from datetime import datetime

class VentaController:
    def __init__(self):
        pass

    def registrar_venta(self, productos_seleccionados, id_usuario):

        try:
            total = sum(subtotal for _, _, _, subtotal in productos_seleccionados)
            fecha = int(datetime.now().timestamp())


            cve_venta = Venta.insertar(fecha, total, id_usuario)

            for producto, cantidad, precio, subtotal in productos_seleccionados:

                Venta.insertar_detalle(cve_venta, producto.cve_producto, cantidad, precio)

                try:
                    producto.reducir_stock(cantidad)
                except ValueError as e:
                    raise Exception(f"Error con '{producto.nombre}': {e}")

            return True, total, cve_venta
        except Exception as e:
            return False, str(e), None


    def obtener_ventas_ordenadas(self, criterio="fecha"):
        return Venta.obtener_ventas(criterio)

    @staticmethod
    def obtener_detalles_de_venta(id_venta):
        return Venta.obtener_detalles_de_venta(id_venta)