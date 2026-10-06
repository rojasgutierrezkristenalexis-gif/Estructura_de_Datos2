"""Módulo para la implementación de una estructura de datos Árbol AVL."""

from collections import deque
from typing import Any, Generator, List, Optional


class Nodo:
    """Representa un nodo dentro de un árbol AVL con encapsulamiento."""

    def __init__(self, valor: Any) -> None:
        self._valor: Any = valor
        self._izq: Optional["Nodo"] = None
        self._der: Optional["Nodo"] = None
        self._altura: int = 1

    # --- GETTERS Y SETTERS ---

    @property
    def valor(self) -> Any:
        return self._valor

    @valor.setter
    def valor(self, nuevo_valor: Any) -> None:
        self._valor = nuevo_valor

    @property
    def izq(self) -> Optional["Nodo"]:
        return self._izq

    @izq.setter
    def izq(self, nodo_izquierdo: Optional["Nodo"]) -> None:
        self._izq = nodo_izquierdo

    @property
    def der(self) -> Optional["Nodo"]:
        return self._der

    @der.setter
    def der(self, nodo_derecho: Optional["Nodo"]) -> None:
        self._der = nodo_derecho

    @property
    def altura(self) -> int:
        return self._altura

    @altura.setter
    def altura(self, nueva_altura: int) -> None:
        self._altura = nueva_altura


class ArbolAVL:
    """Estructura de datos Árbol AVL (Auto-balanceado) con nombres expresivos."""

    def __init__(self) -> None:
        self.raiz: Optional[Nodo] = None

    # --- MÉTODOS DE ESTADO Y UTILIDAD ---

    def _obtener_altura_nodo(self, nodo_objetivo: Optional[Nodo]) -> int:
        """Obtiene la altura de un nodo de forma segura en $O(1)$."""
        return nodo_objetivo.altura if nodo_objetivo else 0

    def _obtener_factor_balance(self, nodo_objetivo: Optional[Nodo]) -> int:
        """Calcula el factor de equilibrio (FB = Altura_Derecha - Altura_Izquierda)."""
        if not nodo_objetivo:
            return 0
        altura_derecha = self._obtener_altura_nodo(nodo_objetivo.der)
        altura_izquierda = self._obtener_altura_nodo(nodo_objetivo.izq)
        return altura_derecha - altura_izquierda

    def _actualizar_altura(self, nodo_objetivo: Nodo) -> None:
        """Recalcula la altura del nodo basado en sus subárboles en $O(1)$."""
        altura_izquierda = self._obtener_altura_nodo(nodo_objetivo.izq)
        altura_derecha = self._obtener_altura_nodo(nodo_objetivo.der)
        nodo_objetivo.altura = 1 + max(altura_izquierda, altura_derecha)

    def altura(self) -> int:
        """Devuelve la altura total del árbol desde la raíz."""
        return self._obtener_altura_nodo(self.raiz)

    def es_vacio(self) -> bool:
        """Verifica si el árbol no tiene raíz asignada."""
        return self.raiz is None

    def es_hoja(self, nodo_evaluado: Optional[Nodo]) -> bool:
        """Verifica si un nodo no posee ningún hijo."""
        if nodo_evaluado is None:
            return False
        return nodo_evaluado.izq is None and nodo_evaluado.der is None

    def cantidad(self, nodo_actual: Optional[Nodo] = None) -> int:
        """Cuenta recursivamente el total de nodos almacenados."""
        if nodo_actual is None:
            return 0
        return (
            1
            + self.cantidad(nodo_actual.izq)
            + self.cantidad(nodo_actual.der)
        )

    def buscar(self, valor_buscado: Any) -> bool:
        """Busca si un valor existe en el árbol de forma iterativa $O(\\log N)$."""
        nodo_actual = self.raiz
        while nodo_actual:
            if valor_buscado == nodo_actual.valor:
                return True
            if valor_buscado < nodo_actual.valor:
                nodo_actual = nodo_actual.izq
            else:
                nodo_actual = nodo_actual.der
        return False

    def obtener_sucesor(self, valor_referencia: Any) -> Optional[Any]:
        """Encuentra el valor que sigue inmediatamente (In-Order) al valor dado."""
        nodo_actual = self.raiz
        nodo_sucesor = None

        while nodo_actual:
            if valor_referencia < nodo_actual.valor:
                nodo_sucesor = nodo_actual
                nodo_actual = nodo_actual.izq
            elif valor_referencia > nodo_actual.valor:
                nodo_actual = nodo_actual.der
            else:
                if nodo_actual.der:
                    return self._encontrar_minimo(nodo_actual.der).valor
                break

        return nodo_sucesor.valor if nodo_sucesor else None

    def _encontrar_minimo(self, nodo_inicial: Nodo) -> Nodo:
        """Encuentra el nodo con la clave mínima en un subárbol."""
        nodo_actual = nodo_inicial
        while nodo_actual.izq:
            nodo_actual = nodo_actual.izq
        return nodo_actual

    # --- LÓGICA DE ROTACIONES Y BALANCEO ---

    def _rotar_derecha(self, nodo_desbalanceado: Nodo) -> Nodo:
        """Ejecuta una rotación simple a la derecha (Caso Izquierda-Izquierda)."""
        nueva_raiz_subarbol = nodo_desbalanceado.izq
        subarbol_intermedio = nueva_raiz_subarbol.der

        # Reorganización de punteros
        nueva_raiz_subarbol.der = nodo_desbalanceado
        nodo_desbalanceado.izq = subarbol_intermedio

        # Actualización de alturas en orden de abajo hacia arriba
        self._actualizar_altura(nodo_desbalanceado)
        self._actualizar_altura(nueva_raiz_subarbol)

        return nueva_raiz_subarbol

    def _rotar_izquierda(self, nodo_desbalanceado: Nodo) -> Nodo:
        """Ejecuta una rotación simple a la izquierda (Caso Derecha-Derecha)."""
        nueva_raiz_subarbol = nodo_desbalanceado.der
        subarbol_intermedio = nueva_raiz_subarbol.izq

        # Reorganización de punteros
        nueva_raiz_subarbol.izq = nodo_desbalanceado
        nodo_desbalanceado.der = subarbol_intermedio

        # Actualización de alturas en orden de abajo hacia arriba
        self._actualizar_altura(nodo_desbalanceado)
        self._actualizar_altura(nueva_raiz_subarbol)

        return nueva_raiz_subarbol

    # --- INSERCIÓN Y ELIMINACIÓN ---

    def insertar(self, valor_nuevo: Any) -> None:
        """Inserta un valor manteniendo la propiedad del árbol AVL."""
        self.raiz = self._insertar_recursivo(self.raiz, valor_nuevo)

    def _insertar_recursivo(self, nodo_actual: Optional[Nodo], valor_nuevo: Any) -> Nodo:
        if not nodo_actual:
            return Nodo(valor_nuevo)

        if valor_nuevo < nodo_actual.valor:
            nodo_actual.izq = self._insertar_recursivo(nodo_actual.izq, valor_nuevo)
        elif valor_nuevo > nodo_actual.valor:
            nodo_actual.der = self._insertar_recursivo(nodo_actual.der, valor_nuevo)
        else:
            print(f"El valor {valor_nuevo} ya existe en el árbol. Operación omitida.")
            return nodo_actual

        self._actualizar_altura(nodo_actual)
        factor_balance = self._obtener_factor_balance(nodo_actual)

        # Caso Izquierda-Izquierda (II)
        if factor_balance < -1 and valor_nuevo < nodo_actual.izq.valor:
            return self._rotar_derecha(nodo_actual)

        # Caso Derecha-Derecha (DD)
        if factor_balance > 1 and valor_nuevo > nodo_actual.der.valor:
            return self._rotar_izquierda(nodo_actual)

        # Caso Izquierda-Derecha (ID)
        if factor_balance < -1 and valor_nuevo > nodo_actual.izq.valor:
            nodo_actual.izq = self._rotar_izquierda(nodo_actual.izq)
            return self._rotar_derecha(nodo_actual)

        # Caso Derecha-Izquierda (DI)
        if factor_balance > 1 and valor_nuevo < nodo_actual.der.valor:
            nodo_actual.der = self._rotar_derecha(nodo_actual.der)
            return self._rotar_izquierda(nodo_actual)

        return nodo_actual

    def eliminar(self, valor_a_eliminar: Any) -> None:
        """Elimina un valor del árbol y re-balancea la estructura."""
        if self.raiz:
            self.raiz = self._eliminar_recursivo(self.raiz, valor_a_eliminar)

    def _eliminar_recursivo(
        self, nodo_actual: Optional[Nodo], valor_a_eliminar: Any
    ) -> Optional[Nodo]:
        if nodo_actual is None:
            return None

        if valor_a_eliminar < nodo_actual.valor:
            nodo_actual.izq = self._eliminar_recursivo(nodo_actual.izq, valor_a_eliminar)
        elif valor_a_eliminar > nodo_actual.valor:
            nodo_actual.der = self._eliminar_recursivo(nodo_actual.der, valor_a_eliminar)
        else:
            # Caso 1 y 2: Sin hijos o con un solo hijo
            if nodo_actual.izq is None:
                return nodo_actual.der
            if nodo_actual.der is None:
                return nodo_actual.izq

            # Caso 3: Dos hijos (Reemplazar con el sucesor in-order)
            nodo_sucesor = self._encontrar_minimo(nodo_actual.der)
            nodo_actual.valor = nodo_sucesor.valor
            nodo_actual.der = self._eliminar_recursivo(
                nodo_actual.der, nodo_sucesor.valor
            )

        self._actualizar_altura(nodo_actual)
        factor_balance = self._obtener_factor_balance(nodo_actual)

        # Re-balanceo post-eliminación
        if factor_balance < -1 and self._obtener_factor_balance(nodo_actual.izq) <= 0:
            return self._rotar_derecha(nodo_actual)

        if factor_balance < -1 and self._obtener_factor_balance(nodo_actual.izq) > 0:
            nodo_actual.izq = self._rotar_izquierda(nodo_actual.izq)
            return self._rotar_derecha(nodo_actual)

        if factor_balance > 1 and self._obtener_factor_balance(nodo_actual.der) >= 0:
            return self._rotar_izquierda(nodo_actual)

        if factor_balance > 1 and self._obtener_factor_balance(nodo_actual.der) < 0:
            nodo_actual.der = self._rotar_derecha(nodo_actual.der)
            return self._rotar_izquierda(nodo_actual)

        return nodo_actual

    # --- RECORRIDOS ---

    def amplitud(self) -> List[Any]:
        """Recorrido por niveles (BFS)."""
        if self.raiz is None:
            return []

        valores_recorridos = []
        cola_nodos = deque([self.raiz])

        while cola_nodos:
            nodo_visita = cola_nodos.popleft()
            valores_recorridos.append(nodo_visita.valor)

            if nodo_visita.izq:
                cola_nodos.append(nodo_visita.izq)
            if nodo_visita.der:
                cola_nodos.append(nodo_visita.der)

        return valores_recorridos

    def pre_orden(self, nodo_actual: Optional[Nodo] = None, es_nodo_raiz: bool = True) -> List[Any]:
        """Recorrido Pre-Orden (Raíz -> Izquierda -> Derecha)."""
        if es_nodo_raiz:
            nodo_actual = self.raiz

        if nodo_actual is None:
            return []

        resultado_acumulado = [nodo_actual.valor]
        resultado_acumulado.extend(self.pre_orden(nodo_actual.izq, False))
        resultado_acumulado.extend(self.pre_orden(nodo_actual.der, False))
        return resultado_acumulado

    def in_orden(self, nodo_actual: Optional[Nodo] = None, es_nodo_raiz: bool = True) -> List[Any]:
        """Recorrido In-Orden (Izquierda -> Raíz -> Derecha)."""
        if es_nodo_raiz:
            nodo_actual = self.raiz

        if nodo_actual is None:
            return []

        resultado_acumulado = self.in_orden(nodo_actual.izq, False)
        resultado_acumulado.append(nodo_actual.valor)
        resultado_acumulado.extend(self.in_orden(nodo_actual.der, False))
        return resultado_acumulado

    def post_orden(self, nodo_actual: Optional[Nodo] = None, es_nodo_raiz: bool = True) -> List[Any]:
        """Recorrido Post-Orden (Izquierda -> Derecha -> Raíz)."""
        if es_nodo_raiz:
            nodo_actual = self.raiz

        if nodo_actual is None:
            return []

        resultado_acumulado = self.post_orden(nodo_actual.izq, False)
        resultado_acumulado.extend(self.post_orden(nodo_actual.der, False))
        resultado_acumulado.append(nodo_actual.valor)
        return resultado_acumulado


# --- PRUEBA DE FUNCIONALIDAD ---
if __name__ == "__main__":
    mi_avl = ArbolAVL()
    elementos_prueba = [10, 20, 30, 40, 50, 25]

    for elemento in elementos_prueba:
        mi_avl.insertar(elemento)

    print(f"Altura del árbol tras inserciones: {mi_avl.altura()}")
    mi_avl.eliminar(20)

    print(f"Recorrido Amplitud (Balanceado): {mi_avl.amplitud()}")
    print(f"Recorrido InOrden (Ordenado):   {mi_avl.in_orden()}")