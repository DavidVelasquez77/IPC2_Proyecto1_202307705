class Par:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y

    def __hash__(self):
        prime = 31
        result = 1
        result = prime * result + self.x
        result = prime * result + self.y
        return result

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
        nodo_actual = self.inicio
        inicio_lista = NodoLista()
        actual_lista = inicio_lista
        while nodo_actual:
            nuevo_item = NodoLista()
            # Se evitan las tuplas. Se pueden crear nodos para la clave y el valor por separado, o cualquier otra estructura personalizada.
            clave_valor_nodo = NodoMapa(nodo_actual.clave, nodo_actual.valor)
            nuevo_item.valor = clave_valor_nodo
            actual_lista.siguiente = nuevo_item
            actual_lista = nuevo_item
            nodo_actual = nodo_actual.siguiente
        return Lista(inicio_lista.siguiente)

    def tamano(self):
        count = 0
        nodo_actual = self.inicio
        while nodo_actual:
            count += 1
            nodo_actual = nodo_actual.siguiente
        return count

class NodoLista:
    def __init__(self, valor=None):
        self.valor = valor
        self.siguiente = None

class Lista:
    def __init__(self, inicio=None):
        self.inicio = inicio

    def agregar(self, item):
        nuevo_nodo = NodoLista(item)
        if self.inicio is None:
            self.inicio = nuevo_nodo
        else:
            nodo_actual = self.inicio
            while nodo_actual.siguiente:
                nodo_actual = nodo_actual.siguiente
            nodo_actual.siguiente = nuevo_nodo

    def obtener(self, index):
        nodo_actual = self.inicio
        count = 0
        while nodo_actual:
            if count == index:
                return nodo_actual.valor
            nodo_actual = nodo_actual.siguiente
            count += 1
        raise IndexError("Índice fuera de rango")

    def __len__(self):
        count = 0
        nodo_actual = self.inicio
        while nodo_actual:
            count += 1
            nodo_actual = nodo_actual.siguiente
        return count

    def __iter__(self):
        self._current = self.inicio
        return self

    def __next__(self):
        if self._current is None:
            raise StopIteration
        else:
            valor = self._current.valor
            self._current = self._current.siguiente
            return valor

    def items(self):
        items_lista = Lista()
        nodo_actual = self.inicio
        while nodo_actual:
            items_lista.agregar(nodo_actual.valor)
            nodo_actual = nodo_actual.siguiente
        return items_lista
