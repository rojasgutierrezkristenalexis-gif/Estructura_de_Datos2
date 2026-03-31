from collections import deque

class Nodo:
    """Clase que representa un nodo en un árbol binario."""
    def __init__(self, valor):
        self._valor = valor  # El número que lleva en el pecho
        self._izq = None     # Mano izquierda (vacía al empezar)
        self._der = None     # Mano derecha (vacía al empezar)

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


class ArbolBinario:
    """Estructura de Datos Abstracta para un Árbol Binario."""
    def __init__(self):
        self.raiz = None
 #insertar de manera navegacion tarea
    def esvacio(self):
        return not self.raiz
    def insertarnavegacion(self, valor):
    # 1. Preparación
         nuevo = Nodo(valor)
    
    # Caso especial: Si el árbol está vacío
         #if not self.raiz:
         if self.esvacio():
           self.raiz = nuevo
           return

    # 2. Navegación (Búsqueda del lugar)
         actual = self.raiz
         padre = None

         while actual:
            padre = actual  # Guardamos el rastro del último nodo visitado

        # --- VALIDACIÓN DE REPETIDOS ---
            if valor == actual.valor:
             print(f"El valor {valor} ya existe. Operación omitida.")
             return  # Sale de la función COMPLETAMENTE
        # -------------------------------

        # Decidimos hacia dónde bajar
            if valor < actual.valor:
                actual = actual.izq
            else:
                actual = actual.der

    # 3. Conexión (Fuera del bucle while, cuando actual es None)
         if valor < padre.valor:
            padre.izq = nuevo
         else:
            padre.der = nuevo
    #hacer trace
    def insertar(self, valor):
        """Inserta un valor respetando la propiedad de búsqueda."""
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(valor, self.raiz)

    def PreOrden(self, nodo_actual=None, inicial=True):
        """Raíz -> Izquierda -> Derecha"""
        if inicial: nodo_actual = self.raiz
        if nodo_actual is None: return []
        
        res = [nodo_actual.valor]
        res += self.PreOrden(nodo_actual.izq, False)
        res += self.PreOrden(nodo_actual.der, False)
        return res
    def InOrden(self, nodo_actual=None, inicial=True):
        """Izquierda -> Raíz -> Derecha (Muestra los datos ordenados)"""
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
    def _insertar_recursivo(self, valor, nodo_actual):
        if valor < nodo_actual.valor:
            if nodo_actual.izq is None:
                nodo_actual.izq = Nodo(valor)
            else:
                self._insertar_recursivo(valor, nodo_actual.izq)
        else:
            if nodo_actual.der is None:
                nodo_actual.der = Nodo(valor)
            else:
                self._insertar_recursivo(valor, nodo_actual.der)

    def buscar(self, valor, nodo_actual = None):
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

    def es_hoja(self, nodo):
        """Verifica si un nodo no tiene hijos."""
        return nodo.izq is None and nodo.der is None

    def altura(self, nodo_actual):
        """Calcula la altura (camino más largo a una hoja)."""
        if nodo_actual is None:
            return -1
        return 1 + max(self.altura(nodo_actual.izq), self.altura(nodo_actual.der))

    def cantidad(self, nodo_actual):
        """Cuenta el total de nodos en el árbol."""
        if nodo_actual is None:
            return 0
        return 1 + self.cantidad(nodo_actual.izq) + self.cantidad(nodo_actual.der)

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

# --- PRUEBA DE FUNCIONAMIENTO ---
arbol = ArbolBinario()
valores = [50, 30, 70, 20, 40, 60, 80]
for v in valores:
    arbol.insertarnavegacion(v)

print(f"Recorrido en Amplitud: {arbol.amplitud()}")
print(f"Total de nodos: {arbol.cantidad(arbol.raiz)}")
print(f"Altura del árbol: {arbol.altura(arbol.raiz)}")
print(f"¿Existe el 60?: {arbol.buscar(60)}")
print(f"PreOrden:  {arbol.PreOrden()}")
print(f"InOrden:   {arbol.InOrden()}")  # Debería salir ordenado: 20, 30, 40...
print(f"PostOrden: {arbol.PostOrden()}")