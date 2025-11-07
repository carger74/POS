from models.venta import Venta

class GananciaController:
    def __init__(self):
        self.modelo = Venta

    def obtener_productos_mas_vendidos(self, anio, mes_inicio, mes_fin):
        return self.modelo.productos_mas_vendidos(anio, mes_inicio, mes_fin)

    def obtener_ganancias_por_mes(self, ano, mes):

        return self.modelo.obtener_ganancias_por_mes(ano,mes)

    def obtener_ganancia_neta(self, anio, mes_inicio, mes_fin):
        return self.modelo.obtener_ganancias_por_rango(anio, mes_inicio, mes_fin)

