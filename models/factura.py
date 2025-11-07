from DatabaseConnection import DatabaseConnection

class FacturaModel:
    @staticmethod
    def registrar_factura(datos):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        # Insertar estado
        cursor.execute("INSERT INTO estado (estado) VALUES (?)", (datos["estado"],))
        cve_estado = cursor.lastrowid

        # Insertar CP
        cursor.execute("INSERT INTO codigo_postal (CP, cve_estado) VALUES (?, ?)", (datos["cp"], cve_estado))
        cve_cp = cursor.lastrowid

        # Insertar alcaldía
        cursor.execute("INSERT INTO alcaldia (alcaldia, cve_cp) VALUES (?, ?)", (datos["alcaldia"], cve_cp))
        cve_alcaldia = cursor.lastrowid

        # Insertar dirección
        cursor.execute("""
            INSERT INTO direccion_facturacion (calle, numero_ext, numero_int, cve_alcaldia)
            VALUES (?, ?, ?, ?)
        """, (datos["calle"], datos["num_ext"], datos["num_int"], cve_alcaldia))
        cve_dir = cursor.lastrowid

        # Insertar datos del cliente
        cursor.execute("""
            INSERT INTO datos_factura_cliente (nombre, ap_p, ap_m, RFC, cve_dir_fact)
            VALUES (?, ?, ?, ?, ?)
        """, (datos["nombre"], datos["ap_p"], datos["ap_m"], datos["rfc"], cve_dir))
        cve_datos_cliente = cursor.lastrowid

        # Insertar factura
        cursor.execute("""
            INSERT INTO Factura (cve_venta, cve_dat_fact_cliente, monto, uso_CFDI, correo, razon)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (datos["id_ticket"], cve_datos_cliente, datos["monto"],
              datos["uso_cfdi"], datos["correo"], datos["regimen_fiscal"]))

        conn.commit()
        return True
    @staticmethod
    def insertar_estado(nombre):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO estado (estado) VALUES (?)", (nombre,))
        conn.commit()

        return cursor.lastrowid

    @staticmethod
    def insertar_cp(cp, cve_estado):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO codigo_postal (CP, cve_estado) VALUES (?, ?)", (cp, cve_estado))
        conn.commit()

        return cursor.lastrowid

    @staticmethod
    def insertar_alcaldia(nombre, cve_cp):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alcaldia (alcaldia, cve_cp) VALUES (?, ?)", (nombre, cve_cp))
        conn.commit()

        return cursor.lastrowid

    @staticmethod
    def insertar_direccion(cve_alcaldia, calle, num_ext, num_int):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO direccion_facturacion (cve_alcaldia, calle, numero_ext, numero_int)
            VALUES (?, ?, ?, ?)
        """, (cve_alcaldia, calle, num_ext, num_int))
        conn.commit()

        return cursor.lastrowid

    @staticmethod
    def insertar_datos_cliente(nombre, ap_p, ap_m, rfc, cve_dir):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO datos_factura_cliente (nombre, ap_p, ap_m, RFC, cve_dir_fact)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, ap_p, ap_m, rfc, cve_dir))
        conn.commit()

        return cursor.lastrowid

    @staticmethod
    def insertar_factura(cve_venta, cve_cliente, monto, uso_cfdi, correo, razon_social):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Factura (cve_venta, cve_dat_fact_cliente, monto, uso_CFDI, correo, razon)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cve_venta, cve_cliente, monto, uso_cfdi, correo, razon_social))
        conn.commit()
        return cursor.lastrowid