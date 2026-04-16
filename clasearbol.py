from collections import deque


class Nodo:
    """Clase que representa un nodo en un árbol binario."""
    def __init__(self, valor):
        self._valor = valor
        self._izq = None
        self._der = None

    # Getters y Setters (Encapsulamiento)
    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, nuevo_valor):
        self._valor = nuevo_valor

    @property
    def izq(self):
        return self._izq

    @izq.setter
    def izq(self, nodo):
        self._izq = nodo

    @property
    def der(self):
        return self._der

    @der.setter
    def der(self, nodo):
        self._der = nodo


class ArbolAVL:
    """
    Estructura de Datos AVL.
    Mantiene todas las funciones originales e integra el auto-equilibrio.
    """
    def __init__(self):
        self.raiz = None

    # --- MÉTODOS DE ESTADO Y UTILIDAD ---

    def esvacio(self):
        """Verifica si el árbol no tiene raíz."""
        return not self.raiz

    def es_hoja(self, nodo):
        """Verifica si un nodo no tiene hijos."""
        if nodo is None:
            return False
        return nodo.izq is None and nodo.der is None

    def cantidad(self, nodo_actual):
        """Cuenta el total de nodos en el árbol."""
        if nodo_actual is None:
            return 0
        return 1 + self.cantidad(nodo_actual.izq) + self.cantidad(nodo_actual.der)

    def buscar(self, valor, nodo_actual=None):
        """Busca un valor en el árbol. Retorna True si existe."""
        if nodo_actual is None:
            nodo_actual = self.raiz
        if nodo_actual is None:
            return False
        if nodo_actual.valor == valor:
            return True
        if valor < nodo_actual.valor:
            return self.buscar(valor, nodo_actual.izq)
        return self.buscar(valor, nodo_actual.der)

    def obtener_sucesor(self, valor):
        """Encuentra el valor que sigue lógicamente (In-Order) al valor dado."""
        actual = self.raiz
        sucesor = None
        while actual:
            if valor < actual.valor:
                sucesor = actual
                actual = actual.izq
            elif valor > actual.valor:
                actual = actual.der
            else:
                if actual.der:
                    return self._encontrar_minimo(actual.der).valor
                break
        return sucesor.valor if sucesor else None

    def _encontrar_minimo(self, nodo):
        """Auxiliar para encontrar el nodo con el valor más pequeño."""
        actual = nodo
        while actual and actual.izq is not None:
            actual = actual.izq
        return actual

    # --- LÓGICA DE BALANCEO (AVL) ---

    def _get_altura(self, nodo):
        """Calcula la altura dinámicamente."""
        if nodo is None:
            return -1
        return 1 + max(self._get_altura(nodo.izq), self._get_altura(nodo.der))

    def _get_balance(self, nodo):
        """Calcula el factor de equilibrio (FE)."""
        if not nodo:
            return 0
        return self._get_altura(nodo.der) - self._get_altura(nodo.izq)

    def _rotar_derecha(self, y):
        """Rotación Simple Derecha (Caso Izquierda-Izquierda)."""
        x = y.izq
        t2 = x.der
        x.der = y
        y.izq = t2
        return x

    def _rotar_izquierda(self, x):
        """Rotación Simple Izquierda (Caso Derecha-Derecha)."""
        y = x.der
        t2 = y.izq
        y.izq = x
        x.der = t2
        return y

    # --- INSERCIÓN Y ELIMINACIÓN ---

    def insertar(self, valor):
        """Inserta un valor respetando la propiedad de búsqueda y balanceo."""
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        if not nodo:
            return Nodo(valor)

        if valor < nodo.valor:
            nodo.izq = self._insertar_recursivo(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._insertar_recursivo(nodo.der, valor)
        else:
            print(f"El valor {valor} ya existe. Operación omitida.")
            return nodo

        # Balanceo post-inserción
        balance = self._get_balance(nodo)

        # Caso II (Izquierda-Izquierda)
        if balance < -1 and valor < nodo.izq.valor:
            return self._rotar_derecha(nodo)
        # Caso DD (Derecha-Derecha)
        if balance > 1 and valor > nodo.der.valor:
            return self._rotar_izquierda(nodo)
        # Caso ID (Izquierda-Derecha)
        if balance < -1 and valor > nodo.izq.valor:
            nodo.izq = self._rotar_izquierda(nodo.izq)
            return self._rotar_derecha(nodo)
        # Caso DI (Derecha-Izquierda)
        if balance > 1 and valor < nodo.der.valor:
            nodo.der = self._rotar_derecha(nodo.der)
            return self._rotar_izquierda(nodo)

        return nodo

    def eliminar(self, valor):
        """Método público para iniciar la eliminación con balanceo."""
        if self.raiz:
            self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo, valor):
        if nodo is None:
            return None

        if valor < nodo.valor:
            nodo.izq = self._eliminar_recursivo(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._eliminar_recursivo(nodo.der, valor)
        else:
            # Caso 1 y 2: Hoja o un solo hijo
            if nodo.izq is None:
                return nodo.der
            elif nodo.der is None:
                return nodo.izq

            # Caso 3: Dos hijos
            sucesor = self._encontrar_minimo(nodo.der)
            nodo.valor = sucesor.valor
            nodo.der = self._eliminar_recursivo(nodo.der, sucesor.valor)

        # Balanceo post-eliminación
        balance = self._get_balance(nodo)
        if balance < -1 and self._get_balance(nodo.izq) <= 0:
            return self._rotar_derecha(nodo)
        if balance < -1 and self._get_balance(nodo.izq) > 0:
            nodo.izq = self._rotar_izquierda(nodo.izq)
            return self._rotar_derecha(nodo)
        if balance > 1 and self._get_balance(nodo.der) >= 0:
            return self._rotar_izquierda(nodo)
        if balance > 1 and self._get_balance(nodo.der) < 0:
            nodo.der = self._rotar_derecha(nodo.der)
            return self._rotar_izquierda(nodo)

        return nodo

    # --- RECORRIDOS ---

    def amplitud(self):
        """Recorrido por niveles (BFS)."""
        if self.raiz is None:
            return []
        resultado = []
        cola = deque([self.raiz])
        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.valor)
            if nodo.izq:
                cola.append(nodo.izq)
            if nodo.der:
                cola.append(nodo.der)
        return resultado

    def PreOrden(self, nodo_actual=None, inicial=True):
        """Raíz -> Izquierda -> Derecha"""
        if inicial: nodo_actual = self.raiz
        if nodo_actual is None: return []
        res = [nodo_actual.valor]
        res += self.PreOrden(nodo_actual.izq, False)
        res += self.PreOrden(nodo_actual.der, False)
        return res

    def InOrden(self, nodo_actual=None, inicial=True):
        """Izquierda -> Raíz -> Derecha"""
        if inicial: nodo_actual = self.raiz
        if nodo_actual is None: return []
        res = self.InOrden(nodo_actual.izq, False)
        res.append(nodo_actual.valor)
        res += self.InOrden(nodo_actual.der, False)
        return res

    def PostOrden(self, nodo_actual=None, inicial=True):
        """Izquierda -> Derecha -> Raíz"""
        if inicial: nodo_actual = self.raiz
        if nodo_actual is None: return []
        res = self.PostOrden(nodo_actual.izq, False)
        res += self.PostOrden(nodo_actual.der, False)
        res.append(nodo_actual.valor)
        return res
# --- Prueba de Fuego (Carga desbalanceada) ---
mi_avl = ArbolAVL()
# Insertamos valores que en un BST normal crearían una línea recta (desbalance total)
elementos = [10, 20, 30, 40, 50, 25]
for e in elementos:
    mi_avl.insertar(e)

print(f"Recorrido Amplitud (Balanceado): {mi_avl.amplitud()}")
print(f"Recorrido InOrden (Ordenado):   {mi_avl.InOrden()}")