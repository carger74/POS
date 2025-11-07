from models.producto import Producto
from DatabaseConnection import DatabaseConnection


class ProductoController:
    def __init__(self):
        pass

    def obtener_productos_disponibles(self):
        """Obtiene todos los productos con su cantidad actual"""
        return Producto.obtener_todos()

    def obtener_producto_por_id(self, id_producto):
        return Producto.obtener_por_id(id_producto)

    def reducir_stock_producto(self, id_producto, cantidad):
        producto = Producto.obtener_por_id(id_producto)
        if producto:
            producto.reducir_stock(cantidad)
            return True
        return False

    def agregar_producto(self, nombre, costo, mayoreo, menudeo, stock):
        nuevo = Producto(None, nombre, menudeo, mayoreo, costo, stock)
        nuevo.insertar_en_bd()
        return True

    def actualizar_stock(self, cve_producto, nueva_cantidad):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Inventario SET cantidad = ? WHERE cve_producto = ?
        """, (nueva_cantidad, cve_producto))
        conn.commit()

    def actualizar_precio_o_costo(self, cve_producto, campo, valor):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        query = f"UPDATE Producto SET {campo} = ? WHERE cve_producto = ?"
        cursor.execute(query, (valor, cve_producto))
        conn.commit()

    def eliminar_producto(self, cve_producto):
        Producto.eliminar_producto(cve_producto)
