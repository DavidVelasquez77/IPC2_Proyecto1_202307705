# Nodo.py
from utils import Par 

class Nodo:
    def __init__(self, nombre, n, m, datos):
        self.nombre = nombre
        self.n = n
        self.m = m
        self.datos = datos  # datos debe ser una instancia de Mapa
        self.siguiente = None

    def obtener_dato(self, x, y):
        return self.datos.obtener(Par(x, y), 0)  # Usar Par como clave

    def establecer_dato(self, x, y, valor):
        self.datos.agregar(Par(x, y), valor)  # Usar Par como clave

    def mostrar_matriz(self):
        """Muestra la matriz completa en formato tabular."""
        for i in range(1, self.n + 1):
            fila = ""
            for j in range(1, self.m + 1):
                valor = str(self.obtener_dato(i, j))
                if j > 1:
                    fila += " | "
                fila += valor
            print(fila)
        print()  # Línea en blanco al final de la matriz
