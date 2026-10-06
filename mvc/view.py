class vista:
    def pedirproducto(self):
        nombre=input ('nuevo producto ......\n')
        precio=input  ('precio \n')
        categoria=input('categoria \n')
        return nombre,precio,categoria
    def mostrar(self,lista):
        print('la lista es ',lista)