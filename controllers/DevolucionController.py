from models.Devolucion import Devolucion
from DatabaseConnection import DatabaseConnection

class DevolucionController:
    def __init__(self):
        self.conn = DatabaseConnection().get_connection()

    def obtener_productos_de_ticket(self, id_ticket):
        cursor = self.conn.cursor()

        # 1. Traemos todos los productos vendidos en ese ticket
        cursor.execute("""
            SELECT 
                p.nombre,
                dv.cve_inventario as id_producto,
                dv.cantidad as cantidad_vendida,
                p.precio_menudeo
            FROM Detalle_Venta dv
            JOIN Producto p ON p.cve_producto = dv.cve_inventario
            WHERE dv.cve_venta = ?
        """, (id_ticket,))
        productos = cursor.fetchall()

        resultado = []

        for prod in productos:
            id_producto = prod["id_producto"]
            cantidad_vendida = prod["cantidad_vendida"]

            # 2. Verificamos cuántas unidades ya se devolvieron
            cursor.execute("""
                SELECT SUM(cantidad_devuelta / dv.precio) as cantidad_devueltas
                FROM Devolucion d
                JOIN Detalle_Venta dv ON d.id_ticket = dv.cve_venta AND d.id_producto = dv.cve_inventario
                WHERE d.id_ticket = ? AND d.id_producto = ?
            """, (id_ticket, id_producto))
            row = cursor.fetchone()
            ya_devuelto = row["cantidad_devueltas"] if row["cantidad_devueltas"] else 0

            # 3. Calculamos cuánto queda por devolver
            pendiente = cantidad_vendida - ya_devuelto

            # 4. Solo agregamos productos si aún hay algo por devolver
            if pendiente > 0:
                resultado.append({
                    "nombre": prod["nombre"],
                    "id_producto": id_producto,
                    "cantidad": int(pendiente),
                    "precio_menudeo": prod["precio_menudeo"]
                })

        return resultado

    def obtener_cantidad_devuelta(self, id_ticket, id_producto):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT SUM(cantidad_devuelta) as total
            FROM Devolucion
            WHERE id_ticket = ? AND id_producto = ?
        """, (id_ticket, id_producto))
        row = cursor.fetchone()
        return row["total"] if row["total"] else 0

    def registrar_devolucion(self, id_ticket, id_producto, cantidad):
        # Obtener cuánto se vendió originalmente
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT cantidad
            FROM Detalle_Venta
            WHERE cve_venta = ? AND cve_inventario = ?
        """, (id_ticket, id_producto))
        row = cursor.fetchone()
        if not row:
            raise Exception("El producto no pertenece a este ticket")

        cantidad_vendida = row["cantidad"]
        ya_devuelta = self.obtener_cantidad_devuelta(id_ticket, id_producto)

        if cantidad + ya_devuelta > cantidad_vendida:
            raise Exception(f"No puedes devolver más de lo que se vendió. Vendido: {cantidad_vendida}, ya devuelto: {ya_devuelta}")

        # Registrar la devolución en el modelo
        Devolucion.registrar_devolucion(id_ticket, id_producto, cantidad)
