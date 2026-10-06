class NodoArbolB:
    def __init__(self, t, es_hoja=True):
        self._t = t
        self._es_hoja = es_hoja
        self._claves = []
        self._hijos = []

    # --- Propiedad: t (Grado mínimo - Solo lectura) ---
    @property
    def t(self):
        return self._t

    # --- Propiedad: es_hoja ---
    @property
    def es_hoja(self):
        return self._es_hoja

    @es_hoja.setter
    def es_hoja(self, valor):
        if isinstance(valor, bool):
            self._es_hoja = valor
        else:
            raise ValueError("es_hoja debe ser booleano.")

    # --- Propiedad: claves ---
    @property
    def claves(self):
        return self._claves

    @claves.setter
    def claves(self, lista):
        if isinstance(lista, list):
            self._claves = lista
        else:
            raise TypeError("Las claves deben ser una lista.")

    # --- Propiedad: hijos ---
    @property
    def hijos(self):
        return self._hijos

    @hijos.setter
    def hijos(self, lista):
        if isinstance(lista, list):
            self._hijos = lista
        else:
            raise TypeError("Los hijos deben ser una lista.")


class ArbolB:
    def __init__(self, t):
        self._t = t
        self.raiz = NodoArbolB(t)

    def buscar(self, k, nodo=None):
        if nodo is None:
            nodo = self.raiz
        
        i = 0
        while i < len(nodo.claves) and k > nodo.claves[i]:
            i += 1
        
        if i < len(nodo.claves) and k == nodo.claves[i]:
            return True
        
        if nodo.es_hoja:
            return False
        
        return self.buscar(k, nodo.hijos[i])

    def insertar(self, k):
        raiz = self.raiz
        # Si la raíz está llena, el árbol crece hacia arriba
        if len(raiz.claves) == (2 * self._t) - 1:
            nueva_raiz = NodoArbolB(self._t, False)
            self.raiz = nueva_raiz
            # La antigua raíz se vuelve hija de la nueva
            nueva_raiz.hijos.insert(0, raiz)
            self._dividir_hijo(nueva_raiz, 0)
            self._insertar_no_lleno(nueva_raiz, k)
        else:
            self._insertar_no_lleno(raiz, k)

    def _dividir_hijo(self, x, i):
        t = self._t
        y = x.hijos[i]
        z = NodoArbolB(t, y.es_hoja)
        
        # El nodo z toma las t-1 claves más grandes de y
        # El valor medio sube al padre x
        x.claves.insert(i, y.claves[t - 1])
        x.hijos.insert(i + 1, z)
        
        z.claves = y.claves[t : (2 * t) - 1]
        y.claves = y.claves[0 : t - 1]
        
        # Si no es hoja, también repartimos los hijos
        if not y.es_hoja:
            z.hijos = y.hijos[t : 2 * t]
            y.hijos = y.hijos[0 : t]

    def _insertar_no_lleno(self, x, k):
        i = len(x.claves) - 1
        
        if x.es_hoja:
            # Insertar en la lista de claves manteniendo el orden
            x.claves.append(None)
            while i >= 0 and k < x.claves[i]:
                x.claves[i + 1] = x.claves[i]
                i -= 1
            x.claves[i + 1] = k
        else:
            # Buscar el hijo adecuado para descender
            while i >= 0 and k < x.claves[i]:
                i -= 1
            i += 1
            
            # Si el hijo está lleno, hay que dividirlo antes de bajar
            if len(x.hijos[i].claves) == (2 * self._t) - 1:
                self._dividir_hijo(x, i)
                if k > x.claves[i]:
                    i += 1
            self._insertar_no_lleno(x.hijos[i], k)

    def imprimir_arbol(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz
        
        print(f"Nivel {nivel} {nodo.claves}")
        
        if not nodo.es_hoja:
            for hijo in nodo.hijos:
                self.imprimir_arbol(hijo, nivel + 1)


# --- Bloque de ejecución ---
if __name__ == "__main__":
    # Creamos un árbol de grado 2 (máximo 3 claves y 4 hijos por nodo)
    # Es pequeño para poder ver las divisiones rápido
    bt = ArbolB(t=2)

    valores = [10, 20, 5, 6, 12, 30, 7, 17, 3, 25]
    
    print("--- Insertando valores ---")
    for v in valores:
        bt.insertar(v)
    
    print("\n--- Estructura final del árbol ---")
    bt.imprimir_arbol()

    print("\n--- Pruebas de búsqueda ---")
    print(f"¿Existe el 17?: {bt.buscar(17)}")
    print(f"¿Existe el 100?: {bt.buscar(100)}")