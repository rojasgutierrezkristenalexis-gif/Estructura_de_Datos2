class Nodo:
    def __init__(self, id_usuario, nombre):
        self.id_usuario = id_usuario  # Este será nuestro dato para ordenar
        self.nombre = nombre          # Este es un dato extra
        self.izq = None               # Referencia al hijo izquierdo
        self.der = None               # Referencia al hijo derecho

# Probemos que funciona creando un nodo manualmente
raiz = Nodo(10, "Juan")
print(f"Nodo creado: ID {raiz.id_usuario}, Nombre: {raiz.nombre}")
def mostrar_ordenado(nodo):
    if nodo is not None:
        mostrar_ordenado(nodo.izq) # Primero va a lo más pequeño (izquierda)
        print(f"ID: {nodo.id_usuario} - Nombre: {nodo.nombre}") # Imprime el actual
        mostrar_ordenado(nodo.der) # Luego va a los mayores (derecha)

# Probemos todo junto
raiz = None
raiz = insertar(raiz, 100, "Director")
raiz = insertar(raiz, 50, "Gerente")
raiz = insertar(raiz, 150, "Socio")

print("--- Contenido del Árbol Ordenado ---")
mostrar_ordenado(raiz)
#segundo commit