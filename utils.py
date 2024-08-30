# utils.py

class Par:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"
    
class NodoMapa:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None

class Mapa:
    def __init__(self):
        self.inicio = None

    def agregar(self, clave, valor):
        if not isinstance(clave, Par):
            raise TypeError("La clave debe ser una instancia de Par")
        nuevo_nodo = NodoMapa(clave, valor)
        if self.inicio is None:
            self.inicio = nuevo_nodo
        else:
            nodo_actual = self.inicio
            while nodo_actual.siguiente:
                nodo_actual = nodo_actual.siguiente
            nodo_actual.siguiente = nuevo_nodo

    def obtener(self, clave, valor_default=None):
        if not isinstance(clave, Par):
            raise TypeError("La clave debe ser una instancia de Par")
        nodo_actual = self.inicio
        while nodo_actual:
            if nodo_actual.clave == clave:
                return nodo_actual.valor
            nodo_actual = nodo_actual.siguiente
        return valor_default

    def contiene(self, clave):
        if not isinstance(clave, Par):
            raise TypeError("La clave debe ser una instancia de Par")
        nodo_actual = self.inicio
        while nodo_actual:
            if nodo_actual.clave == clave:
                return True
            nodo_actual = nodo_actual.siguiente
        return False

    def items(self):
        items = []
        nodo_actual = self.inicio
        while nodo_actual:
            items.append((nodo_actual.clave, nodo_actual.valor))
            nodo_actual = nodo_actual.siguiente
        return items




class Lista:
    def __init__(self):
        self._items = []

    def agregar(self, item):
        self._items.append(item)

    def obtener(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def items(self):
        return self._items