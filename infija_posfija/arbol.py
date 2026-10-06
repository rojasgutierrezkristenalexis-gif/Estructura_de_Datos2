"""
Módulo modelo del patrón MVC para expresiones matemáticas.

Contiene la lógica de negocio que permite representar una expresión
matemática infija como un árbol binario de expresión, obtener dicha
expresión en notación infija, prefija y posfija, y finalmente evaluarla
para calcular su resultado numérico.

Este módulo no depende de ninguna interfaz gráfica por lo que puede
reutilizarse de forma independiente.
"""

from __future__ import annotations

from typing import Optional, Union

# Operadores soportados por el modelo según su precedencia.
# A mayor valor de precedencia, mayor prioridad de la operación.
_PRECEDENCIA: dict = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
}

# Valor numérico que se puede almacenar dentro de un nodo hoja.
Numero = Union[int, float]


class Nodo:
    """Nodo de un árbol binario de expresión.

    Cada nodo almacena un dato, que puede ser un número (en el caso de
    una hoja) o un operador matemático (en el caso de un nodo interno).

    Attributes:
        dato: Valor almacenado en el nodo. Puede ser un número o uno
            de los operadores '+', '-', '*' o '/'.
        izquierda: Referencia al hijo izquierdo o None si no existe.
        derecha: Referencia al hijo derecho o None si no existe.
    """

    def __init__(self, dato: Union[Numero, str]) -> None:
        """Inicializa un nuevo nodo sin hijos.

        Args:
            dato: Valor que almacenará el nodo. Puede ser un número o
                un operador matemático.
        """
        self._dato = dato
        self._izquierda: Optional[Nodo] = None
        self._derecha: Optional[Nodo] = None

    @property
    def dato(self) -> Union[Numero, str]:
        """Obtiene el valor almacenado en el nodo.

        Returns:
            El dato del nodo.
        """
        return self._dato

    @property
    def izquierda(self) -> Optional["Nodo"]:
        """Obtiene el hijo izquierdo del nodo.

        Returns:
            Referencia al hijo izquierdo o None.
        """
        return self._izquierda

    @izquierda.setter
    def izquierda(self, nodo: Optional["Nodo"]) -> None:
        """Asigna el hijo izquierdo del nodo.

        Args:
            nodo: Nuevo hijo izquierdo o None para eliminarlo.
        """
        self._izquierda = nodo

    @property
    def derecha(self) -> Optional["Nodo"]:
        """Obtiene el hijo derecho del nodo.

        Returns:
            Referencia al hijo derecho o None.
        """
        return self._derecha

    @derecha.setter
    def derecha(self, nodo: Optional["Nodo"]) -> None:
        """Asigna el hijo derecho del nodo.

        Args:
            nodo: Nuevo hijo derecho o None para eliminarlo.
        """
        self._derecha = nodo

    @property
    def es_hoja(self) -> bool:
        """Indica si el nodo es una hoja (sin hijos).

        Returns:
            True si el nodo no tiene hijos, False en caso contrario.
        """
        return self._izquierda is None and self._derecha is None

    @property
    def es_operador(self) -> bool:
        """Indica si el dato del nodo es un operador matemático.

        Returns:
            True si el dato es '+', '-', '*' o '/'.
        """
        return self._dato in _PRECEDENCIA

    def __repr__(self) -> str:
        """Representación textual de depuración del nodo.

        Returns:
            Cadena con el dato del nodo.
        """
        return f"Nodo({self._dato!r})"


class ArbolBinario:
    """Árbol binario que representa una expresión matemática.

    La expresión se construye a partir de una cadena en notación
    infija. La estructura del árbol respeta la precedencia de los
    operadores y permite obtener la misma expresión en diferentes
    notaciones así como calcular su resultado.

    Attributes:
        raiz: Nodo que representa la raíz del árbol.
    """

    def __init__(self) -> None:
        """Inicializa un árbol binario vacío.

        La raíz comienza siendo None porque todavía no hay nodos.
        """
        self._raiz: Optional[Nodo] = None
        self._expresion_infija: str = ""

    @property
    def raiz(self) -> Optional[Nodo]:
        """Obtiene la raíz del árbol.

        Returns:
            Nodo raíz del árbol o None si está vacío.
        """
        return self._raiz

    @property
    def expresion_infija(self) -> str:
        """Obtiene la expresión infija original procesada.

        Returns:
            Cadena con la expresión en notación infija.
        """
        return self._expresion_infija

    def construir(self, expresion: str) -> None:
        """Construye el árbol a partir de una expresión infija.

        El proceso se realiza en dos etapas:

        1. La expresión infija se convierte a notación posfija con el
           algoritmo de Shunting-yard, una pila de operadores que
           respeta la precedencia y los paréntesis.
        2. A partir de la notación posfija se construye el árbol
           binario de expresión, donde los números son hojas y los
           operadores forman los nodos internos.

        Una vez construido el árbol, su notación posfija se obtiene
        recorriéndolo en :meth:`postorden`.

        Args:
            expresion: Expresión matemática en notación infija que
                puede incluir números enteros, decimales y operadores
                +, -, *, / así como paréntesis.

        Raises:
            ValueError: Si la expresión no es válida.
        """
        if not operacion_valida(expresion):
            raise ValueError("La operación introducida no es válida.")

        self._expresion_infija = expresion.strip()

        # Etapa 1: la expresión infija se convierte a posfija.
        posfija = _infija_a_posfija(_tokenizar(self._expresion_infija))

        # Etapa 2: se construye el árbol a partir de la posfija.
        self._raiz = _construir_arbol_desde_posfija(posfija)

    # ------------------------------------------------------------------
    # Recorridos del árbol que devuelven las notaciones en texto.
    # ------------------------------------------------------------------
    def prefija(self, nodo: Optional[Nodo]) -> str:
        """Obtiene la notación prefija del subárbol indicado.

        El recorrido sigue el orden: nodo actual, subárbol izquierdo
        y subárbol derecho.

        Args:
            nodo: Nodo del cual se obtiene la notación prefija.

        Returns:
            Cadena con la expresión en notación prefija.
        """
        if nodo is None:
            return ""
        return (
            str(nodo.dato)
            + self.prefija(nodo.izquierda)
            + self.prefija(nodo.derecha)
        )

    def infija(self, nodo: Optional[Nodo]) -> str:
        """Obtiene la notación infija del subárbol indicado.

        El recorrido sigue el orden: subárbol izquierdo, nodo actual
        y subárbol derecho.

        Args:
            nodo: Nodo del cual se obtiene la notación infija.

        Returns:
            Cadena con la expresión en notación infija.
        """
        if nodo is None:
            return ""
        if nodo.es_operador:
            # Se agregan paréntesis para conservar la precedencia.
            return (
                "("
                + self.infija(nodo.izquierda)
                + str(nodo.dato)
                + self.infija(nodo.derecha)
                + ")"
            )
        return str(nodo.dato)

    def postorden(self, nodo: Optional[Nodo]) -> str:
        """Recorre el árbol en postorden y devuelve la notación posfija.

        El recorrido postorden sigue el orden: subárbol izquierdo,
        subárbol derecho y, finalmente, el nodo actual. Como los
        operadores se visitan después que sus operandos, el resultado
        es la expresión en notación posfija (polaca inversa).

        Este es el método que convierte la expresión del árbol a
        notación posfija.

        Args:
            nodo: Nodo desde el cual comienza el recorrido.

        Returns:
            Cadena con la expresión en notación posfija.
        """
        if nodo is None:
            return ""
        return (
            self.postorden(nodo.izquierda)
            + self.postorden(nodo.derecha)
            + str(nodo.dato)
        )

    # ------------------------------------------------------------------
    # Evaluación del árbol.
    # ------------------------------------------------------------------
    def resultado(self, nodo: Optional[Nodo]) -> Optional[Numero]:
        """Evalúa el árbol y devuelve el resultado de la expresión.

        Los nodos hoja devuelven su valor numérico y los nodos
        operador combinan los resultados de sus hijos aplicando la
        operación correspondiente.

        Args:
            nodo: Nodo desde el cual se comienza la evaluación.

        Returns:
            Valor numérico del resultado o None si el nodo es None.

        Raises:
            ZeroDivisionError: Si se intenta dividir entre cero.
        """
        if nodo is None:
            return None

        if nodo.es_hoja:
            return nodo.dato  # type: ignore[return-value]

        izquierda = self.resultado(nodo.izquierda)
        derecha = self.resultado(nodo.derecha)

        if izquierda is None or derecha is None:
            raise ValueError("La expresión no contiene operandos suficientes.")

        if nodo.dato == "+":
            return izquierda + derecha
        if nodo.dato == "-":
            return izquierda - derecha
        if nodo.dato == "*":
            return izquierda * derecha
        if nodo.dato == "/":
            return izquierda / derecha

        raise ValueError(f"Operador no soportado: {nodo.dato!r}")


# ----------------------------------------------------------------------
# Funciones auxiliares del modelo (lógica de validación y tokenización).
# ----------------------------------------------------------------------
def es_operador(caracter: str) -> bool:
    """Comprueba si un símbolo es un operador matemático.

    Args:
        caracter: Símbolo que se desea comprobar.

    Returns:
        True si el símbolo es '+', '-', '*' o '/'.
    """
    return caracter in _PRECEDENCIA


def _precedencia(operador: str) -> int:
    """Obtiene la precedencia de un operador.

    Args:
        operador: Operador del cual se desea conocer la precedencia.

    Returns:
        Valor entero de precedencia. Los operadores * y / tienen
        valor 2 mientras que + y - tienen valor 1.
    """
    return _PRECEDENCIA.get(operador, 0)


def es_numero(token: str) -> bool:
    """Comprueba si un token representa un número.

    Se aceptan números enteros y decimales, incluyendo el punto
    decimal.

    Args:
        token: Símbolo que se desea comprobar.

    Returns:
        True si el token es un número, False en caso contrario.
    """
    try:
        float(token)
        return True
    except (TypeError, ValueError):
        return False


def _convertir_numero(token: str) -> Numero:
    """Convierte un token en su valor numérico.

    Args:
        token: Cadena que representa un número.

    Returns:
        Valor entero si el número no tiene parte decimal, o valor
        flotante en caso contrario.
    """
    valor = float(token)
    if valor.is_integer():
        return int(valor)
    return valor


def _infija_a_posfija(tokens) -> list[str]:
    """Convierte una lista de tokens infijos a notación posfija.

    Se utiliza el algoritmo de Shunting-yard con una pila de
    operadores. La precedencia de los operadores y los paréntesis se
    respetan durante el proceso.

    Args:
        tokens: Lista de tokens que componen la expresión infija.

    Returns:
        Lista de tokens de la misma expresión en notación posfija.
    """
    pila: list[str] = []
    posfija: list[str] = []

    for simbolo in tokens:
        if es_numero(simbolo):
            # Los números pasan directamente a la salida.
            posfija.append(simbolo)
        elif simbolo == "(":
            pila.append(simbolo)
        elif simbolo == ")":
            # Se desapilan operadores hasta encontrar el paréntesis.
            while pila and pila[-1] != "(":
                posfija.append(pila.pop())
            if pila:
                pila.pop()  # Se elimina el paréntesis de apertura.
        elif es_operador(simbolo):
            # Se desapilan operadores de mayor o igual precedencia.
            while (
                pila
                and pila[-1] != "("
                and _precedencia(pila[-1]) >= _precedencia(simbolo)
            ):
                posfija.append(pila.pop())
            pila.append(simbolo)

    # Se vacían los operadores que quedaron en la pila.
    while pila:
        posfija.append(pila.pop())

    return posfija


def _construir_arbol_desde_posfija(posfija: list[str]) -> Optional[Nodo]:
    """Construye el árbol de expresión a partir de la notación posfija.

    Se recorre la expresión posfija y se utiliza una pila de nodos:
    cuando aparece un número se apila una hoja y cuando aparece un
    operador se desapilan dos nodos que pasan a ser sus hijos, y el
    nodo del operador se vuelve a apilar.

    Args:
        posfija: Lista de símbolos en notación posfija.

    Returns:
        Nodo raíz del árbol construido o None si la lista está vacía.

    Raises:
        ValueError: Si la expresión no contiene operandos suficientes.
    """
    pila: list[Nodo] = []

    for simbolo in posfija:
        if es_numero(simbolo):
            # Las hojas del árbol son los números.
            pila.append(Nodo(_convertir_numero(simbolo)))
            continue

        # Un operador necesita dos operandos para formarse.
        if len(pila) < 2:
            raise ValueError("Expresión mal formada (faltan operandos).")

        derecha = pila.pop()
        izquierda = pila.pop()

        operador = Nodo(simbolo)
        operador.izquierda = izquierda
        operador.derecha = derecha
        pila.append(operador)

    return pila[-1] if pila else None


def _tokenizar(expresion: str) -> list[str]:
    """Divide una expresión infija en símbolos (tokens).

    Los números pueden tener varias cifras y punto decimal. Cualquier
    otro carácter (operadores o paréntesis) se convierte en su propio
    token.

    Args:
        expresion: Expresión matemática en notación infija.

    Returns:
        Lista de tokens que componen la expresión.
    """
    tokens: list[str] = []
    numero_actual = ""

    for caracter in expresion:
        if caracter.isdigit() or caracter == ".":
            numero_actual += caracter
        else:
            if numero_actual:
                tokens.append(numero_actual)
                numero_actual = ""
            if caracter != " ":
                tokens.append(caracter)

    if numero_actual:
        tokens.append(numero_actual)

    return tokens


def es_valido(expresion: str) -> bool:
    """Comprueba que la expresión use únicamente caracteres válidos.

    Se permiten dígitos, el punto decimal y los operadores +, -, *
    y / así como paréntesis de apertura y cierre.

    Args:
        expresion: Expresión que se desea validar.

    Returns:
        True si todos los caracteres son válidos, False en caso
        contrario.
    """
    if not expresion.strip():
        return False

    for caracter in expresion:
        if caracter == " ":
            continue
        if (
            caracter.isdigit()
            or caracter == "."
            or es_operador(caracter)
            or caracter == "("
            or caracter == ")"
        ):
            continue
        return False

    return True


def operacion_valida(expresion: str) -> bool:
    """Comprueba que la estructura de la expresión sea correcta.

    Además de verificar los caracteres permitidos, se comprueba que:
    - La expresión no comience ni termine con un operador.
    - No existan dos operadores consecutivos.
    - Los paréntesis estén balanceados.
    - Cada paréntesis de apertura vaya seguido de un operando y cada
      paréntesis de cierre, precedido de un operando.

    Args:
        expresion: Expresión matemática que se desea validar.

    Returns:
        True si la expresión tiene una estructura válida.
    """
    if not es_valido(expresion):
        return False

    expresion = expresion.strip()

    # Una operación no puede comenzar ni terminar con un operador.
    if not expresion:
        return False
    if es_operador(expresion[0]) or es_operador(expresion[-1]):
        return False

    tokens = _tokenizar(expresion)

    # Se recuerda el símbolo anterior para detectar secuencias
    # inválidas de operadores u operandos.
    anterior = ""

    for token in tokens:
        # Dos operadores consecutivos son inválidos. Ejemplo: "5+*2".
        if es_operador(token) and es_operador(anterior):
            return False
        # Un operador nunca puede seguir a un paréntesis de apertura.
        # Ejemplo: "(+5)".
        if es_operador(token) and anterior == "(":
            return False
        # Un operador nunca puede preceder a un paréntesis de cierre.
        # Ejemplo: "(5+)".
        if token == ")" and es_operador(anterior):
            return False
        anterior = token

    # Se verifica el balanceo de los paréntesis.
    balance = 0
    for token in tokens:
        if token == "(":
            balance += 1
        elif token == ")":
            balance -= 1
            if balance < 0:
                return False

    return balance == 0
