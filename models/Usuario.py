# usuario.py
from DatabaseConnection import DatabaseConnection

class Usuario:
    def __init__(self, rol):
        self.rol = rol

    @staticmethod
    def autenticar(id_usuario, contrasena):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT rol FROM Usuario
            WHERE id = ? AND contrasena = ?
        """, (id_usuario, contrasena))
        row = cursor.fetchone()
        if row:
            return Usuario(row["rol"])
        else:
            print("nada")
            return None
