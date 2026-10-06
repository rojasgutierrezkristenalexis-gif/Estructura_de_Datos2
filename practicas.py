from clasearbol import ArbolAVL
if __name__ == '__main__': 
    arbolito=ArbolAVL()
    for i in range(5):
        dato=input(' inserta dato en arbol ')
        arbolito.insertar(dato)
    print(arbolito.InOrden())

    