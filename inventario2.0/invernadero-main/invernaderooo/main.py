import tkinter as tk
from modelo.modelo import Modelo
from vista.interfaz_vista import Vista
from controlador.controlador import Controlador

if __name__ == '__main__':
    root = tk.Tk()
    modelo = Modelo()
    vista = Vista(root)
    app = Controlador(modelo, vista)
    root.mainloop()
