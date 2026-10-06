import tkinter as tk
from tkinter import messagebox
class vista:
    def __init__(self,funcion_mandada,funcion_eliminar,funcion_traducir):
        self.mensaje_controlador=funcion_mandada
        self.mensaje_eliminar=funcion_eliminar
        self.mensaje_traduccion=funcion_traducir
        self.root=tk.Tk()
        self.root.title("diccionario ingles-español")
        self.root.geometry("500x500")
        self.label_palabra=tk.Label(self.root,text='palabra')
        self.label_palabra.pack(pady=5)
        self.palabra=tk.Entry(self.root)
        self.palabra.pack(pady=20)
        self.label_traduccion=tk.Label(self.root,text='traduccion')
        self.label_traduccion.pack(pady=10)
        self.traduccion=tk.Entry(self.root)
        self.traduccion.pack(pady=10)
        self.resultado_texto = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.resultado_texto.pack(pady=20)
        self.palabra.bind("<Return>",self.agregar_valor)
        self.traduccion.bind("<Return>",self.agregar_valor)
        self.caja_visual=tk.Listbox(self.root , width=30 , height=10 )
        self.caja_visual.pack(pady=10)
        self.btn_eliminar = tk.Button(self.root, text="Eliminar Palabra", command=self.click_eliminar, bg="#ff4444", fg="white")
        self.btn_eliminar.pack(pady=5)
        self.btn_buscar = tk.Button(self.root, text="🔍 Buscar", command=self.mostrar_traduccion, bg="#44aaff", fg="white")
        self.btn_buscar.pack(pady=5)
    def agregar_valor(self,event=None):
        nueva_palabra=self.palabra.get()
        traduccion=self.traduccion.get()
        self.mensaje_controlador(nueva_palabra,traduccion)
        self.palabra.delete(0,tk.END)
        self.traduccion.delete(0,tk.END)
    def actualizar_ventana(self,lista):
        self.caja_visual.delete(0,tk.END)
        for e in lista :
            self.caja_visual.insert(tk.END, f" Nodo: {e}")
    def click_eliminar(self):
        palabra_a_borrar = self.palabra.get() # O el item seleccionado
        if palabra_a_borrar:
            self.mensaje_eliminar(palabra_a_borrar)
            self.palabra.delete(0, 'end') # Limpiamos el campo
    def mostrar_traduccion(self):
        palabra_a_traducir=self.palabra.get()
        if palabra_a_traducir :
            self.mensaje_traduccion(palabra_a_traducir)
            self.palabra.delete(0, 'end') # Limpiamos el campo
    def mostrar_resultado_en_pantalla(self, traduccion):
        # Esta función la llama el controlador cuando ya tiene la respuesta
        if traduccion and traduccion != "No encontrado":
            self.resultado_texto.config(text=f"Traducción: {traduccion}", fg="green")
        else:
            self.resultado_texto.config(text="❌ Palabra no encontrada", fg="red")
    def ejecutar(self):
        self.root.mainloop()
        