import tkinter as tk
from tkinter import scrolledtext

personas = ["Nombre", "Edad", "Ciudad", "Profesión", "Cedula"]
diccionario1 = {"Nombre": "Hector", "Edad": 45, "Ciudad": "San Martin", "Profesión": "comerciante", "Cedula": "17357505"}
diccionario2 = {"Nombre": "Maria", "Edad": 25, "Ciudad": "Bogota", "Profesión": "abogada", "Cedula": "40188527"}
diccionario3 = {"Nombre": "Juan", "Edad": 40, "Ciudad": "Villavicencio", "Profesión": "medico", "Cedula": "480809"}
diccionario4 = {"Nombre": "Ana", "Edad": 35, "Ciudad": "Granada", "Profesión": "Meretriz", "Cedula": "40188345"}

lista_diccionarios = [diccionario1, diccionario2, diccionario3, diccionario4]

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Visor de Personas")
ventana.geometry("400x300")

# Área de texto con scroll para mostrar los datos
txt_area = scrolledtext.ScrolledText(ventana, width=40, height=15)
txt_area.pack(padx=10, pady=10)

# Lógica de impresión dentro de la ventana
for d in lista_diccionarios:
    for p in personas:
        linea = f"{p} : {d[p]}\n"
        txt_area.insert(tk.END, linea)
    txt_area.insert(tk.END, "-" * 30 + "\n")

ventana.mainloop()
