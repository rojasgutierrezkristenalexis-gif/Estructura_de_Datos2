from view import vista
from model import ArbolAVL

class Controlador:
    def __init__(self):
        self.vista=vista(funcion_mandada=self.logica_de_guardado,
                        funcion_eliminar=self.borrar_palabra,
                        funcion_traducir=self.buscar_traduccion)
        self.arbol=ArbolAVL()
    def logica_de_guardado(self, palabra, traduccion):
        # Esta es la función que la Vista va a ejecutar "por nosotros"
        print(f"--- Controlador: Recibí '{palabra}', validando... ---")
        print(f"--- Controlador: Recibí '{traduccion}', validando... ---")
        if palabra.strip() and traduccion.strip() :
            self.arbol.insertar(palabra,traduccion)
            lista_in=self.arbol.InOrden() 
            print(self.arbol.obtener_altura_total())
            self.vista.actualizar_ventana(lista_in)
        else:
            print("Error: No puedes enviar algo vacío.")
    def borrar_palabra(self, palabra):
        if not palabra:
            return
    
    # 1. Borramos del árbol
        self.arbol.eliminar(palabra)
    
    # 2. Obtenemos la lista actualizada (In-Orden)
        nueva_lista = self.arbol.InOrden() 
    
    # 3. Mandamos la lista a la vista para que refresque la pantalla
        self.vista.actualizar_ventana(nueva_lista)
    def buscar_traduccion(self, palabra):
        traducido=self.arbol.buscar_traduccion(palabra)
        self.vista.mostrar_resultado_en_pantalla(traducido)
    def ejecutar(self):
        self.vista.ejecutar()