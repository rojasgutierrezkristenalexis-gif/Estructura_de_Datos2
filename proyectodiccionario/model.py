from collections import deque


class Nodo:
    """Clase que representa un nodo en un árbol binario."""
    def __init__(self, palabra, traduccion):
        self._palabra = palabra
        self._traduccion = traduccion
        self._izq = None
        self._der = None

# Getters y Setters para Palabra (La clave del árbol)
    @property
    def palabra(self):
        return self._palabra

    @palabra.setter
    def palabra(self, nueva_palabra):
        self._palabra = nueva_palabra

    # Getters y Setters para Traducción (El valor asociado)
    @property
    def traduccion(self):
        return self._traduccion

    @traduccion.setter
    def traduccion(self, nueva_traduccion):
        self._traduccion = nueva_traduccion

    # Getters y Setters para los Hijos (Crucial para las rotaciones)
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

    def buscar_traduccion(self, palabra_buscada, nodo_actual=None):
        """Busca una palabra y retorna su traducción. Retorna None si no existe."""
        if nodo_actual is None:
            nodo_actual = self.raiz
        
        # Caso base: El árbol está vacío o llegamos al final sin encontrar nada
        if nodo_actual is None:
            return None
        
        # ¡Encontrado! Retornamos la traducción en lugar de True
        if nodo_actual.palabra == palabra_buscada.lower():
            return nodo_actual.traduccion
        
        # Navegación recursiva
        if palabra_buscada.lower() < nodo_actual.palabra:
            return self.buscar_traduccion(palabra_buscada, nodo_actual.izq)
        
        return self.buscar_traduccion(palabra_buscada, nodo_actual.der)
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
    def obtener_altura_total(self):
        return self._get_altura(self.raiz)
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
        if y is None or y.izq is None: # <--- EL SEGURO
            return y
        x = y.izq
        t2 = x.der
        x.der = y
        y.izq = t2
        return x

    def _rotar_izquierda(self, x):
        if x is None or x.der is None: # <--- EL SEGURO
            return x
        y = x.der
        t2 = y.izq
        y.izq = x
        x.der = t2
        return y

    # --- INSERCIÓN Y ELIMINACIÓN ---

    def insertar(self, palabra, traduccion):
        """Método público para insertar."""
        # Convertimos a minúsculas antes de entrar para mantener consistencia
        self.raiz = self._insertar_recursivo(self.raiz, palabra.lower(), traduccion)

    def _insertar_recursivo(self, nodo, palabra, traduccion):
        # 1. CASO BASE: Si llegamos a un espacio vacío, creamos el Nodo
        if not nodo:
            return Nodo(palabra, traduccion)

        # 2. BÚSQUEDA Y COLOCACIÓN
        if palabra < nodo.palabra:
            nodo.izq = self._insertar_recursivo(nodo.izq, palabra, traduccion)
        elif palabra > nodo.palabra:
            nodo.der = self._insertar_recursivo(nodo.der, palabra, traduccion)
        else:
            # Si la palabra ya existe, no hacemos nada más que retornar
            print(f"La palabra '{palabra}' ya existe en el diccionario.")
            return nodo

        # 3. BALANCEO (Ajustado a balance = der - izq)
        balance = self._get_balance(nodo)

        # --- CASO: EL ÁRBOL PESA A LA DERECHA (Balance > 1) ---
        if balance > 1:
            # Sub-caso: Derecha-Izquierda (DI) -> Rotación Doble
            if self._get_balance(nodo.der) < 0:
                nodo.der = self._rotar_derecha(nodo.der)
            # Caso Derecha-Derecha (DD) o después de la rotación derecha del hijo
            return self._rotar_izquierda(nodo)

        # --- CASO: EL ÁRBOL PESA A LA IZQUIERDA (Balance < -1) ---
        if balance < -1:
            # Sub-caso: Izquierda-Derecha (ID) -> Rotación Doble
            if self._get_balance(nodo.izq) > 0:
                nodo.izq = self._rotar_izquierda(nodo.izq)
            # Caso Izquierda-Izquierda (II) o después de la rotación izquierda del hijo
            return self._rotar_derecha(nodo)

        # Si el nodo está equilibrado (balance entre -1 y 1), lo retornamos normal
        return nodo
    def eliminar(self, palabra):
        """Método público para iniciar la eliminación."""
        if self.raiz:
            # Usamos lower() para que no importe si escriben con Mayúsculas
            self.raiz = self._eliminar_recursivo(self.raiz, palabra.lower())

    def _eliminar_recursivo(self, nodo, palabra):
        # 1. CASO BASE: Si no encontramos la palabra
        if nodo is None:
            return None

        # 2. BÚSQUEDA DEL NODO A ELIMINAR
        if palabra < nodo.palabra:
            nodo.izq = self._eliminar_recursivo(nodo.izq, palabra)
        elif palabra > nodo.palabra:
            nodo.der = self._eliminar_recursivo(nodo.der, palabra)
        else:
            # ¡ENCONTRADO!
            # Caso A: Nodo con un solo hijo o sin hijos (Hoja)
            if nodo.izq is None:
                return nodo.der
            elif nodo.der is None:
                return nodo.izq

            # Caso B: Nodo con dos hijos
            # Buscamos el sucesor (el más pequeño del lado derecho)
            sucesor = self._encontrar_minimo(nodo.der)
            
            # Reemplazamos los datos del nodo actual con los del sucesor
            nodo.palabra = sucesor.palabra
            nodo.traduccion = sucesor.traduccion
            
            # Eliminamos el sucesor de su posición original
            nodo.der = self._eliminar_recursivo(nodo.der, sucesor.palabra)

        # Si después de eliminar el árbol quedó vacío, retornamos None
        if nodo is None:
            return None

        # 3. BALANCEO (Igualito al de insertar)
        balance = self._get_balance(nodo)

        # --- CASO: EL ÁRBOL PESA A LA DERECHA (Balance > 1) ---
        if balance > 1:
            # Si el hijo derecho pesa a la izquierda, rotación doble (DI)
            if self._get_balance(nodo.der) < 0:
                nodo.der = self._rotar_derecha(nodo.der)
            return self._rotar_izquierda(nodo)

        # --- CASO: EL ÁRBOL PESA A LA IZQUIERDA (Balance < -1) ---
        if balance < -1:
            # Si el hijo izquierdo pesa a la derecha, rotación doble (ID)
            if self._get_balance(nodo.izq) > 0:
                nodo.izq = self._rotar_izquierda(nodo.izq)
            return self._rotar_derecha(nodo)

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
        res.append(f"{nodo_actual.palabra}: {nodo_actual.traduccion}")
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
