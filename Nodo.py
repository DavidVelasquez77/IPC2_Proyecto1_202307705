class Nodo:
    def __init__(self, nombre, n, m, datos=None):
        self.nombre = nombre  # Nombre de la matriz
        self.n = n  # Número de filas
        self.m = m  # Número de columnas
        self.datos = datos if datos is not None else {}  # Diccionario para almacenar los valores en la matriz
        self.siguiente = None  # Puntero al siguiente nodo en la lista circular

    def obtener_dato(self, x, y):
        """Devuelve el valor almacenado en la posición (x, y) de la matriz."""
        return self.datos.get((x, y), 0)  # Devuelve 0 si no se encuentra la clave (x, y)
    
    def establecer_dato(self, x, y, valor):
        """Establece el valor en la posición (x, y) de la matriz."""
        self.datos[(x, y)] = valor

    def mostrar_matriz(self):
        """Muestra la matriz completa en formato tabular."""
        for i in range(1, self.n + 1):
            fila = []
            for j in range(1, self.m + 1):
                fila.append(str(self.obtener_dato(i, j)))
            print(" | ".join(fila))
        print()  # Línea en blanco al final de la matriz
