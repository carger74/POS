from DatabaseConnection import DatabaseConnection

class UsuarioRegistro:
    def __init__(self, nombre, ap_p, ap_m, rol, email, telefono):
        self.nombre = nombre
        self.ap_p = ap_p
        self.ap_m = ap_m
        self.rol = rol
        self.email = email
        self.telefono = telefono

    def guardar(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Usuario (nombre, ap_p, ap_m, rol, email, telefono)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.nombre, self.ap_p, self.ap_m, self.rol, self.email, self.telefono))
        conn.commit()

        # Recuperar el id generado automáticamente
        cursor.execute("""
            SELECT id, contrasena
            FROM Usuario
            ORDER BY cve_usuario DESC
            LIMIT 1
        """)
        return cursor.fetchone()  # devuelve un diccionario con id y contrasena



