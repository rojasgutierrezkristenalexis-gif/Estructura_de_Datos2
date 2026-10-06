
class modelo:
    def __init__(self):
        self._catalogo=[]  
    def agregar(self,nombre,precio,categoria):
        producto_nuevo={'nombre':nombre,'precio':precio,
                        'categoria':categoria}
        
        self._catalogo.append(producto_nuevo)
    def producto(self):
        return self._catalogo