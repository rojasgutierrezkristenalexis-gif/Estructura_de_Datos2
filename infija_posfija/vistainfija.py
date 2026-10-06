"""
Módulo vista del patrón MVC para expresiones matemáticas.

Contiene la interfaz gráfica construida con Tkinter que permite al
usuario introducir una expresión infija, visualizar la expresión en
notación posfija, el resultado de la operación y el árbol binario de
expresión de forma gráfica.

La vista solo se encarga de mostrar información y delegar las acciones
del usuario al controlador, por lo que no contiene lógica de negocio.
"""

import tkinter as tk
from tkinter import messagebox

from infija_posfija.arbol import Nodo


class ArbolVista(tk.Tk):
    """Ventana principal de la aplicación (vista MVC).

    Hereda de Tk y por tanto es la ventana raíz de la interfaz.
    Se limita a construir los controles, mostrar resultados y
    notificar errores.

    Attributes:
        entry_expresion: Campo de texto donde se escribe la expresión.
        btn_procesar: Botón que dispara el procesamiento.
        lbl_posfija: Etiqueta que muestra la notación posfija.
        lbl_resultado: Etiqueta que muestra el resultado.
        canvas: Lienzo donde se dibuja el árbol.
    """

    def __init__(self) -> None:
        """Inicializa la ventana y construye todos sus controles."""
        super().__init__()
        self.title("Conversor de Expresión Infija a Posfija (MVC)")
        self.geometry("900x650")
        self.configure(bg="#f8f9fa")

        self._crear_interfaz()

    # ------------------------------------------------------------------
    # Construcción de la interfaz.
    # ------------------------------------------------------------------
    def _crear_interfaz(self) -> None:
        """Crea los distintos paneles de la ventana.

        La interfaz se organiza en tres zonas: un panel superior con
        los controles de entrada, un panel de resultados y un lienzo
        para el árbol.
        """
        self._crear_panel_entrada()
        self._crear_panel_resultados()
        self._crear_canvas()

    def _crear_panel_entrada(self) -> None:
        """Construye el panel superior con los controles de entrada.

        Incluye un campo de texto, un botón para procesar la expresión
        y una etiqueta con las instrucciones de uso.
        """
        panel = tk.Frame(
            self, bg="#ffffff", pady=10, padx=10, bd=1, relief=tk.RAISED
        )
        panel.pack(side=tk.TOP, fill=tk.X)

        etiqueta = tk.Label(
            panel,
            text="Expresión infija:",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
        )
        etiqueta.pack(side=tk.LEFT, padx=5)

        self.entry_expresion = tk.Entry(panel, font=("Arial", 12), width=22)
        self.entry_expresion.insert(0, "5+3*2")
        self.entry_expresion.pack(side=tk.LEFT, padx=5)

        self.btn_procesar = tk.Button(
            panel,
            text="Procesar",
            bg="#0d6efd",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
        )
        self.btn_procesar.pack(side=tk.LEFT, padx=5)

        instrucciones = tk.Label(
            panel,
            text="Soporta +, -, * y / además de paréntesis.",
            font=("Arial", 9),
            fg="#6c757d",
            bg="#ffffff",
        )
        instrucciones.pack(side=tk.LEFT, padx=20)

    def _crear_panel_resultados(self) -> None:
        """Construye el panel que muestra los resultados.

        Muestra tres etiquetas con la notación infija, la notación
        posfija y el resultado de la operación.
        """
        panel = tk.Frame(self, bg="#f8f9fa", pady=5)
        panel.pack(side=tk.TOP, fill=tk.X, padx=15)

        self.lbl_infija = tk.Label(
            panel,
            text="Notación Infija: -",
            font=("Arial", 10),
            bg="#f8f9fa",
            anchor="w",
        )
        self.lbl_infija.pack(fill=tk.X, pady=1)

        self.lbl_posfija = tk.Label(
            panel,
            text="Notación Posfija: -",
            font=("Arial", 11, "bold"),
            fg="#0d6efd",
            bg="#f8f9fa",
            anchor="w",
        )
        self.lbl_posfija.pack(fill=tk.X, pady=1)

        self.lbl_resultado = tk.Label(
            panel,
            text="Resultado: -",
            font=("Arial", 13, "bold"),
            fg="#198754",
            bg="#f8f9fa",
            anchor="w",
        )
        self.lbl_resultado.pack(fill=tk.X, pady=1)

    def _crear_canvas(self) -> None:
        """Construye el lienzo donde se dibujará el árbol."""
        self.canvas = tk.Canvas(self, bg="#ffffff")
        self.canvas.pack(
            side=tk.TOP, fill=tk.BOTH, expand=True, padx=15, pady=10
        )

    # ------------------------------------------------------------------
    # Métodos públicos utilizados por el controlador.
    # ------------------------------------------------------------------
    def mostrar_error(self, mensaje: str) -> None:
        """Muestra un cuadro de diálogo con un mensaje de error.

        Args:
            mensaje: Texto que se mostrará en el cuadro de error.
        """
        messagebox.showerror("Error de Entrada", mensaje)

    def actualizar_datos(self, infija: str, posfija: str, resultado) -> None:
        """Actualiza las etiquetas con los resultados del modelo.

        Args:
            infija: Expresión en notación infija.
            posfija: Expresión en notación posfija.
            resultado: Valor numérico resultante de la operación.
        """
        self.lbl_infija.config(text=f"Notación Infija: {infija}")
        self.lbl_posfija.config(text=f"Notación Posfija: {posfija}")
        self.lbl_resultado.config(text=f"Resultado: {resultado}")

    # ------------------------------------------------------------------
    # Dibujo del árbol.
    # ------------------------------------------------------------------
    def dibujar_arbol(self, raiz: Nodo) -> None:
        """Dibuja el árbol de expresión completo en el lienzo.

        Args:
            raiz: Nodo raíz del árbol a dibujar.
        """
        self.canvas.delete("all")
        if raiz is None:
            return

        ancho = self.canvas.winfo_width()
        if ancho <= 1:
            ancho = 800

        self._dibujar_nodo(raiz, x=ancho // 2, y=40, desplazamiento=ancho // 4)

    def _dibujar_nodo(
        self, nodo: Nodo, x: int, y: int, desplazamiento: int
    ) -> None:
        """Dibuja un nodo y, de forma recursiva, sus hijos.

        Args:
            nodo: Nodo que se desea dibujar.
            x: Coordenada horizontal del centro del nodo.
            y: Coordenada vertical del centro del nodo.
            desplazamiento: Separación horizontal entre el nodo y sus
                hijos.
        """
        radio = 20

        if nodo.izquierda is not None:
            x_hijo, y_hijo = x - desplazamiento, y + 60
            self.canvas.create_line(
                x, y, x_hijo, y_hijo, width=2, fill="#6c757d"
            )
            self._dibujar_nodo(
                nodo.izquierda, x_hijo, y_hijo, desplazamiento // 2
            )

        if nodo.derecha is not None:
            x_hijo, y_hijo = x + desplazamiento, y + 60
            self.canvas.create_line(
                x, y, x_hijo, y_hijo, width=2, fill="#6c757d"
            )
            self._dibujar_nodo(
                nodo.derecha, x_hijo, y_hijo, desplazamiento // 2
            )

        # Los números se pintan de color verde y los operadores de azul.
        if nodo.es_operador:
            color_relleno = "#e3f2fd"
            color_borde = "#0d6efd"
        else:
            color_relleno = "#e8f5e9"
            color_borde = "#198754"

        self.canvas.create_oval(
            x - radio,
            y - radio,
            x + radio,
            y + radio,
            fill=color_relleno,
            outline=color_borde,
            width=2,
        )
        self.canvas.create_text(
            x, y, text=str(nodo.dato), font=("Arial", 11, "bold")
        )
