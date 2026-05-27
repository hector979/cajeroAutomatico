from tkinter import Tk, ttk
from tkinter import messagebox
if __name__ == "__main__":
    root = Tk()
    root.title("Mi Aplicacion")
    root.geometry("400x100")

    frm = ttk.Frame(root, padding=10)
    frm.grid()

    lbl = ttk.Label(frm, text="Ventana Python mia de prueba")
    lbl.grid(column=0, row=0)

    # Crear un botón utilizando ttk

    btn = ttk.Button(frm, text="Salir", command=root.destroy)
    btn.grid(column=1, row=10)

    btn_info = ttk.Button(frm, text="Informacion", 
                          command=lambda: messagebox.showinfo("Informacion", "Esta es una ventana de información"))
    btn_info.grid(column=1, row=0)

    escribir = ttk.Entry(frm, width=40, font=("Arial", 12))
    escribir.grid(column=0, row=1, columnspan=3, padx=5, pady=35)
    escribir.focus() #cursor automatico en el campo entry

    #definir funcion de saludo con validacion

def mostrar_info():
    lbl_saludo.config(text="Esta es una ventana con información")

def saludar():
    nombre = entrada_nombre.get()
    lbl_saludo.config(text=f"Bienvenido, {nombre}")

def limpiar():
    entrada_nombre.delete(0, 'end')
    lbl_saludo.config(text="Ventana Python")

if _name_ == "_main_":
    root = Tk()
    root.title("Mi aplicación")
    root.geometry("400x200")

    frm = ttk.Frame(root, padding=10)
    frm.grid()

    # Texto principal
    lbl_saludo = ttk.Label(frm, text="Ventana Python")
    lbl_saludo.grid(column=0, row=0, columnspan=3)

    # Solicitar nombre
    lbl_nombre = ttk.Label(frm, text="Ingrese su nombre:")
    lbl_nombre.grid(column=0, row=1)

    # Cuadro de texto
    entrada_nombre = ttk.Entry(frm, width=25)
    entrada_nombre.grid(column=1, row=1)

    # Botón saludar
    btn_saludar = ttk.Button(frm, text="Saludar", command=saludar)
    btn_saludar.grid(column=0, row=2)

    # Botón información
    btn_info = ttk.Button(frm, text="Información", command=mostrar_info)
    btn_info.grid(column=1, row=2)

    # Botón limpiar
    btn_limpiar = ttk.Button(frm, text="Limpiar", command=limpiar)
    btn_limpiar.grid(column=2, row=2)

    root.mainloop()
