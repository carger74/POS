from DatabaseConnection import DatabaseConnection
from datetime import datetime

class Devolucion:

    @staticmethod
    def registrar_devolucion(id_venta, id_producto, cantidad):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 🔍 Obtener precio del detalle de venta
        cursor.execute("""
            SELECT cantidad, precio
            FROM Detalle_Venta
            WHERE cve_venta = ? AND cve_inventario = ?
        """, (id_venta, id_producto))
        row = cursor.fetchone()

        if not row:
            raise Exception("El producto no pertenece a esta venta.")

        cantidad_actual = row["cantidad"]
        precio_unitario = row["precio"]

        if cantidad > cantidad_actual:
            raise Exception(f"No puedes devolver más de lo vendido (actual: {cantidad_actual})")

        monto = cantidad * precio_unitario  # 💰

        # 🧾 Insertar en tabla Devolucion
        cursor.execute("""
            INSERT INTO Devolucion (id_ticket, id_producto, cantidad_devuelta, fecha)
            VALUES (?, ?, ?, ?)
        """, (id_venta, id_producto, monto, fecha))

        # 🔁 Actualizar Inventario
        cursor.execute("""
            UPDATE Inventario
            SET cantidad = cantidad + ?
            WHERE cve_producto = ?
        """, (cantidad, id_producto))

        # 🔽 Actualizar cantidad en Detalle_Venta
        nueva_cantidad = cantidad_actual - cantidad
        if nueva_cantidad > 0:
            cursor.execute("""
                UPDATE Detalle_Venta
                SET cantidad = ?
                WHERE cve_venta = ? AND cve_inventario = ?
            """, (nueva_cantidad, id_venta, id_producto))
        else:
            # Si ya se devolvió todo ese producto, lo quitamos
            cursor.execute("""
                DELETE FROM Detalle_Venta
                WHERE cve_venta = ? AND cve_inventario = ?
            """, (id_venta, id_producto))

        # ⚰️ Si ya no quedan productos en la venta, eliminar venta completa
        cursor.execute("""
            SELECT COUNT(*) as productos_restantes
            FROM Detalle_Venta
            WHERE cve_venta = ?
        """, (id_venta,))
        if cursor.fetchone()["productos_restantes"] == 0:
            cursor.execute("DELETE FROM Venta WHERE cve_venta = ?", (id_venta,))
        else:
            cursor.execute("""
                UPDATE Venta
                SET total = total - ?
                WHERE cve_venta = ?
            """, (monto, id_venta))

        conn.commit()

    @staticmethod
    def eliminar_venta_completa(id_venta):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        # Recuperar productos vendidos
        cursor.execute("""
            SELECT cve_inventario, cantidad
            FROM Detalle_Venta
            WHERE cve_venta = ?
        """, (id_venta,))
        detalles = cursor.fetchall()

        for row in detalles:
            id_producto = row["cve_inventario"]
            cantidad = row["cantidad"]

            cursor.execute("""
                UPDATE Inventario
                SET cantidad = cantidad + ?
                WHERE cve_producto = ?
            """, (cantidad, id_producto))

        # Eliminar detalles y venta
        cursor.execute("DELETE FROM Detalle_Venta WHERE cve_venta = ?", (id_venta,))
        cursor.execute("DELETE FROM Venta WHERE cve_venta = ?", (id_venta,))
        conn.commit()

