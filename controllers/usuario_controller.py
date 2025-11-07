from models.usuario_registro import UsuarioRegistro

class UsuarioController:
    def registrar_usuario(self, nombre, ap_p, ap_m, rol, email, telefono):
        nuevo = UsuarioRegistro(nombre, ap_p, ap_m, rol, email, telefono)
        return nuevo.guardar()  # esto retorna el id y la contraseña

