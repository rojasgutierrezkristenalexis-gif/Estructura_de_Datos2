class Nodo:
    def __init__(self, id_usuario, nombre):
        self.id_usuario = id_usuario  # Este será nuestro dato para ordenar
        self.nombre = nombre          # Este es un dato extra
        self.izq = None               # Referencia al hijo izquierdo
        self.der = None               # Referencia al hijo derecho

# Probemos que funciona creando un nodo manualmente
raiz = Nodo(10, "Juan")
print(f"Nodo creado: ID {raiz.id_usuario}, Nombre: {raiz.nombre}")