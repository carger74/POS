from controllers.producto_controller import ProductoController
from controllers.venta_controller import VentaController
from observers.AlertaStock import AlertaStock
from models.producto import Producto
from controllers.DevolucionController import DevolucionController
from controllers.usuario_controller import UsuarioController
from controllers.ganacia_controller import GananciaController

Producto.registrar_observador(AlertaStock())

class SistemaVentas:
    def __init__(self):
        self.producto_controller = ProductoController()
        self.venta_controller = VentaController()
        self.devolucion_controller = DevolucionController()
        self.usuario_controller = UsuarioController()
        self.ganancia_controller = GananciaController()




    def listar_productos(self):
        return self.producto_controller.obtener_productos_disponibles()

    def agregar_producto_a_venta(self, id_producto, cantidad):
        return self.producto_controller.obtener_producto_por_id(id_producto)

    def descontar_stock(self, id_producto, cantidad):
        return self.producto_controller.reducir_stock_producto(id_producto, cantidad)

    def realizar_venta(self, productos_seleccionados, id_usuario):
        return self.venta_controller.registrar_venta(productos_seleccionados, id_usuario)

    def obtener_productos_de_ticket(self, id_ticket):
        return self.devolucion_controller.obtener_productos_de_ticket(id_ticket)

    def procesar_devolucion(self, id_ticket, id_producto, cantidad):
        try:
            self.devolucion_controller.registrar_devolucion(id_ticket, id_producto, cantidad)
            return True, "Devolución registrada correctamente."
        except Exception as e:
            return False, str(e)

    def agregar_usuario(self, nombre, ap_p, ap_m, rol, email, telefono):
        return self.usuario_controller.registrar_usuario(nombre, ap_p, ap_m, rol, email, telefono)

    def agregar_producto(self, nombre, costo, mayoreo, menudeo, stock):
        return self.producto_controller.agregar_producto(nombre, costo, mayoreo, menudeo, stock)

    def obtener_inventario(self):
        return self.producto_controller.obtener_productos_disponibles()

    def actualizar_stock(self, cve_producto, nueva_cantidad):
        return self.producto_controller.actualizar_stock(cve_producto, nueva_cantidad)

    def actualizar_precio_o_costo(self, cve_producto, campo, valor):
        return self.producto_controller.actualizar_precio_o_costo(cve_producto, campo, valor)

    def obtener_ventas_ordenadas(self, criterio="fecha"):
        return self.venta_controller.obtener_ventas_ordenadas(criterio)

    def obtener_productos_mas_vendidos(self, anio, mes_inicio, mes_fin):
        return self.ganancia_controller.obtener_productos_mas_vendidos(anio, mes_inicio, mes_fin)

    def obtener_ganancia_neta(self, anio, mes_inicio, mes_fin):
        return self.ganancia_controller.obtener_ganancia_neta(anio, mes_inicio, mes_fin)

    def eliminar_producto(self, cve_producto):
        self.producto_controller.eliminar_producto(cve_producto)

    def obtener_detalles_ticket(self, id_venta):
        return self.venta_controller.obtener_detalles_de_venta(id_venta)





