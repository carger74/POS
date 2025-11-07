from DatabaseConnection import DatabaseConnection

class Producto:
    observadores = []

    def __init__(self, cve_producto, nombre, precio_menudeo, precio_mayoreo, costo, stock):
        self.cve_producto = cve_producto
        self.nombre = nombre
        self.precio_menudeo = precio_menudeo
        self.precio_mayoreo = precio_mayoreo
        self.costo = costo
        self.stock = stock

    @classmethod
    def registrar_observador(cls, observador):
        cls.observadores.append(observador)

    def notificar_observadores(self):
        for obs in Producto.observadores:
            obs.notificar(self)

    def reducir_stock(self, cantidad):
        if cantidad > self.stock:
            raise ValueError(f"No hay suficiente stock para '{self.nombre}'. Quedan solo {self.stock} unidades.")

        self.stock -= cantidad

        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Inventario
            SET cantidad = ?
            WHERE cve_producto = ?
        """, (self.stock, self.cve_producto))
        conn.commit()

        if self.stock < 10:
            self.notificar_observadores()

    @classmethod
    def obtener_todos(cls):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.cve_producto, p.nombre, p.precio_menudeo, p.precio_mayoreo, p.costo, i.cantidad
            FROM Producto p
            JOIN Inventario i ON p.cve_producto = i.cve_producto
        """)
        productos = []
        for row in cursor.fetchall():
            productos.append(cls(
                row["cve_producto"],
                row["nombre"],
                row["precio_menudeo"],
                row["precio_mayoreo"],
                row["costo"],
                row["cantidad"]
            ))
        return productos

    @classmethod
    def obtener_por_id(cls, id_producto):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.cve_producto, p.nombre, p.precio_menudeo, p.precio_mayoreo, p.costo, i.cantidad
            FROM Producto p
            JOIN Inventario i ON p.cve_producto = i.cve_producto
            WHERE p.cve_producto = ?
        """, (id_producto,))
        row = cursor.fetchone()
        if row:
            return cls(
                row["cve_producto"],
                row["nombre"],
                row["precio_menudeo"],
                row["precio_mayoreo"],
                row["costo"],
                row["cantidad"]
            )
        return None

    def insertar_en_bd(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        # Insertar producto
        cursor.execute("""
            INSERT INTO Producto (nombre, precio_menudeo, precio_mayoreo, costo)
            VALUES (?, ?, ?, ?)
        """, (self.nombre, self.precio_menudeo, self.precio_mayoreo, self.costo))

        cve_producto = cursor.lastrowid

        # Insertar inventario
        cursor.execute("""
            INSERT INTO Inventario (cve_producto, cantidad)
            VALUES (?, ?)
        """, (cve_producto, self.stock))

        conn.commit()

    @staticmethod
    def eliminar_producto(cve_producto):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Inventario WHERE cve_producto = ?", (cve_producto,))
        cursor.execute("DELETE FROM Producto WHERE cve_producto = ?", (cve_producto,))
        conn.commit()
