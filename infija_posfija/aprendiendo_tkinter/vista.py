import tkinter as tk
from tkinter import messagebox

if __name__ == '__main__' :
    ventana=tk.Tk()
    ventana.title("arbol binario")
    ventana.geometry("400x400")
    ventana.minsize(350,150)
    ventana.grid_columnconfigure(0,weight=1)
    ventana.grid_rowconfigure(0,weight=1)
    label1=tk.Label(ventana,text='funcion Infija')
    label1.grid(column=0,row=0,padx=5,pady=5,sticky="nw")
    entrada=tk.Entry(ventana)
    ventana.grid_columnconfigure(1,weight=1)
    ventana.grid_rowconfigure(1,weight=1)
    entrada.grid(column=1,row=0,sticky="nw")
    boton=tk.Button( command='')
    boton.grid(column=1 ,row=1 ,padx=5, pady=5 ,sticky="nw")
    
    
    
    
    
    ventana.mainloop()