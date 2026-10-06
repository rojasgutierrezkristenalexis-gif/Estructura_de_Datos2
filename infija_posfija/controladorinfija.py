"""
Módulo controlador del patrón MVC para expresiones matemáticas.

El controlador actúa como intermediario entre la vista y el modelo:
recibe las acciones del usuario desde la vista, procesa la expresión
utilizando el modelo y actualiza la interfaz con los resultados.

No contiene lógica de negocio ni de presentación, únicamente orquesta
la comunicación entre ambos componentes.
"""

import os
import sys
import tkinter as tk

# Se agrega la carpeta raíz del proyecto a sys.path para permitir la
# importación del paquete infija_posfija tanto si el archivo se ejecuta
# como módulo (python -m ...) como si se ejecuta de forma directa.
_MARCA = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(_MARCA)
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)

from infija_posfija.arbol import ArbolBinario, operacion_valida
from infija_posfija.vistainfija import ArbolVista


class ArbolControlador:
    """Controlador que coordina el modelo y la vista.

    Se encarga de configurar los eventos de la interfaz (botón y tecla
    Enter) y de procesar la expresión cuando el usuario lo solicita.

    Attributes:
        modelo: Instancia del modelo ArbolBinario.
        vista: Instancia de la vista ArbolVista.
    """

    def __init__(self, modelo: ArbolBinario, vista: ArbolVista) -> None:
        """Inicializa el controlador y conecta los eventos de la vista.

        Args:
            modelo: Modelo que contiene la lógica de las expresiones.
            vista: Vista gráfica de la aplicación.
        """
        self.modelo = modelo
        self.vista = vista

        self._configurar_eventos()

    def _configurar_eventos(self) -> None:
        """Conecta las acciones del usuario con sus manejadores.

        El botón y la tecla Enter disparan el procesamiento de la
        expresión introducida en el campo de texto.
        """
        self.vista.btn_procesar.config(command=self.procesar_expresion)
        self.vista.entry_expresion.bind(
            "<Return>", lambda _evento: self.procesar_expresion()
        )

    def procesar_expresion(self) -> None:
        """Procesa la expresión introducida por el usuario.

        El flujo seguido es:
        1. Se lee y limpia la expresión del campo de texto.
        2. Se valida su estructura.
        3. Si es válida, se construye el árbol en el modelo.
        4. Se obtienen la notación posfija y el resultado.
        5. Se actualiza la vista y se dibuja el árbol.

        Si la expresión no es válida, se muestra un error sin
        interrumpir la ejecución de la aplicación.
        """
        expresion = self.vista.entry_expresion.get().strip()
        expresion = expresion.replace(" ", "")

        if not operacion_valida(expresion):
            self.vista.mostrar_error("La operación introducida no es válida.")
            return
        if not expresion:
            return

        try:
            # 1. Se construye el árbol dentro del modelo.
            self.modelo.construir(expresion)

            # 2. Se obtienen los resultados del modelo. La notación
            #    posfija se obtiene recorriendo el árbol en postorden.
            infija = self.modelo.infija(self.modelo.raiz)
            posfija = self.modelo.postorden(self.modelo.raiz)
            resultado = self.modelo.resultado(self.modelo.raiz)

            # 3. Se reflejan los resultados en la interfaz.
            self.vista.actualizar_datos(infija, posfija, resultado)
            self.vista.dibujar_arbol(self.modelo.raiz)
        except (ValueError, ZeroDivisionError) as error:
            self.vista.mostrar_error(str(error))


def iniciar_aplicacion() -> None:
    """Crea el modelo, la vista y el controlador e inicia la aplicación.

    Este es el punto de entrada de la aplicación MVC. Instancia los
    tres componentes y ejecuta el bucle principal de la interfaz.
    """
    modelo = ArbolBinario()
    vista = ArbolVista()
    ArbolControlador(modelo, vista)
    vista.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
