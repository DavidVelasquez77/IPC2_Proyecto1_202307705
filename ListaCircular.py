from Nodo import Nodo

class ListaCircular:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def agregar(self, nombre, n, m, datos=None):
        """Agrega una nueva matriz (Nodo) a la lista circular."""
        nuevo_nodo = Nodo(nombre, n, m, datos)
        if self.primero is None:
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
            self.ultimo.siguiente = self.primero  # Mantiene la lista circular
        else:
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo
            self.ultimo.siguiente = self.primero  # Mantiene la circularidad

    def mostrar_todas(self):
        """Muestra todas las matrices en la lista circular."""
        if self.primero is None:
            print("La lista está vacía.")
            return

        actual = self.primero
        while True:
            print(f"Matriz: {actual.nombre} ({actual.n}x{actual.m})")
            actual.mostrar_matriz()
            actual = actual.siguiente
            if actual == self.primero:
                break

    def buscar(self, nombre):
        """Busca una matriz por nombre y la devuelve si existe."""
        if self.primero is None:
            return None

        actual = self.primero
        while True:
            if actual.nombre == nombre:
                return actual  # Retorna el nodo si encuentra la matriz
            actual = actual.siguiente
            if actual == self.primero:
                break
        return None

    def eliminar(self, nombre):
        """Elimina una matriz de la lista circular por nombre."""
        if self.primero is None:
            return False  # Lista vacía, no se puede eliminar nada

        actual = self.primero
        anterior = None
        while True:
            if actual.nombre == nombre:
                if anterior is None:  # Si es el primer nodo
                    if self.primero == self.ultimo:  # Solo un nodo en la lista
                        self.primero = None
                        self.ultimo = None
                    else:
                        self.primero = self.primero.siguiente
                        self.ultimo.siguiente = self.primero
                else:
                    anterior.siguiente = actual.siguiente
                    if actual == self.ultimo:
                        self.ultimo = anterior
                        self.ultimo.siguiente = self.primero
                return True  # Nodo eliminado
            anterior = actual
            actual = actual.siguiente
            if actual == self.primero:
                break
        return False  # No se encontró el nodo
