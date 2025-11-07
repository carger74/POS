from DatabaseConnection import DatabaseConnection

class Venta:
    @staticmethod
    def insertar(fecha_venta, total, cve_usuario):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Venta (fecha_venta, total, cve_usuario)
            VALUES (?, ?, ?)
        """, (fecha_venta, total, cve_usuario))
        return cursor.lastrowid

    @staticmethod
    def insertar_detalle(cve_venta, cve_inventario, cantidad, precio):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Detalle_Venta (cve_venta, cve_inventario, cantidad, precio)
            VALUES (?, ?, ?, ?)
        """, (cve_venta, cve_inventario, cantidad, precio))

    def obtener_ventas(orden="fecha"):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        query = """
               SELECT v.cve_venta, v.fecha_venta, v.total, u.nombre || ' ' || u.ap_p AS empleado
               FROM Venta v
               JOIN Usuario u ON v.cve_usuario = u.cve_usuario
           """
        if orden == "monto":
            query += " ORDER BY v.total DESC"
        else:
            query += " ORDER BY v.fecha_venta DESC"

        cursor.execute(query)
        return cursor.fetchall()

    def obtener_ganancias_por_mes(anio, mes):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(dv.precio * dv.cantidad) AS ingresos, 
                   SUM(p.costo * dv.cantidad) AS costos
            FROM Venta v
            JOIN Detalle_Venta dv ON v.cve_venta = dv.cve_venta
            JOIN Producto p ON p.cve_producto = dv.cve_inventario
            WHERE strftime('%Y', datetime(v.fecha_venta, 'unixepoch')) = ?
              AND strftime('%m', datetime(v.fecha_venta, 'unixepoch')) = ?
        """, (str(anio), f"{mes:02d}"))

        row = cursor.fetchone()
        ingresos = row["ingresos"] or 0
        costos = row["costos"] or 0
        ganancia = ingresos - costos

        return {
            "ingresos": ingresos,
            "costos": costos,
            "ganancia": ganancia
        }

    @staticmethod
    def productos_mas_vendidos(anio, mes_inicio, mes_fin):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.nombre, SUM(dv.cantidad) as cantidad
            FROM Venta v
            JOIN Detalle_Venta dv ON v.cve_venta = dv.cve_venta
            JOIN Producto p ON p.cve_producto = dv.cve_inventario
            WHERE strftime('%Y', datetime(v.fecha_venta, 'unixepoch')) = ?
              AND CAST(strftime('%m', datetime(v.fecha_venta, 'unixepoch')) AS INTEGER) BETWEEN ? AND ?
            GROUP BY p.nombre
            ORDER BY cantidad DESC
            LIMIT 10
        """, (str(anio), mes_inicio, mes_fin))

        return cursor.fetchall()

    @staticmethod
    def obtener_ganancias_por_rango(anio, mes_inicio, mes_fin):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT strftime('%m', datetime(v.fecha_venta, 'unixepoch')) as mes,
                   SUM(dv.precio * dv.cantidad) AS ingresos,
                   SUM(p.costo * dv.cantidad) AS costos
            FROM Venta v
            JOIN Detalle_Venta dv ON v.cve_venta = dv.cve_venta
            JOIN Producto p ON p.cve_producto = dv.cve_inventario
            WHERE strftime('%Y', datetime(v.fecha_venta, 'unixepoch')) = ?
              AND CAST(strftime('%m', datetime(v.fecha_venta, 'unixepoch')) AS INTEGER) BETWEEN ? AND ?
            GROUP BY mes
            ORDER BY mes
        """, (str(anio), mes_inicio, mes_fin))

        rows = cursor.fetchall()
        return [{"mes": int(row["mes"]), "ganancia": (row["ingresos"] or 0) - (row["costos"] or 0)} for row in rows]

    @staticmethod
    def obtener_detalles_de_venta(id_venta):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.nombre, dv.cantidad, dv.precio, (dv.cantidad * dv.precio) AS subtotal
            FROM Detalle_Venta dv
            JOIN Inventario i ON dv.cve_inventario = i.cve_inventario
            JOIN Producto p ON i.cve_producto = p.cve_producto
            WHERE dv.cve_venta = ?
        """, (id_venta,))
        return cursor.fetchall()
