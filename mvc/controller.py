from model import modelo
from view import vista

class controlador:
    def __init__(self):
        self.modelo=modelo()
        self.vista=vista()
    def ejecutar(self):
        while True :
            n,p,c=self.vista.pedirproducto()
            if n.lower() == 'salir':break
            if p.lower() == 'salir':break
            if c.lower() == 'salir':break
            self.modelo.agregar(n,p,c)
            datos=self.modelo.producto()
            self.vista.mostrar(datos)
            