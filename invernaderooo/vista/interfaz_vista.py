import tkinter as tk
from tkinter import ttk, messagebox

class Vista:
    def __init__(self, root):
        self.root = root
        self.root.title("Vivero vital")
        self.root.geometry("800x500")
        self.root.configure(bg="white")

        self.controlador = None
        self.marco_login = None
        self.marco_menu = None
        self.marco_agregar = None

        self.crear_interfaz_login()

    def set_controlador(self, controlador):
        self.controlador = controlador

    def crear_interfaz_login(self):
        self.marco_login = tk.Frame(self.root, bg="white")
        self.marco_login.pack(fill='both', expand=True)

        tk.Label(self.marco_login, text="Iniciar Sesión", font=("Helvetica", 18), bg="#FFFACD", fg="#FFA500", width=20).pack(pady=40)

        self.usuario_entry = tk.Entry(self.marco_login, bg="#f0f7da")
        self.usuario_entry.insert(0, "Admin")
        self.usuario_entry.pack(pady=5)

        self.contrasena_entry = tk.Entry(self.marco_login, show="●", bg="#f0f7da")
        self.contrasena_entry.insert(0, "12345678")
        self.contrasena_entry.pack(pady=5)

        tk.Button(self.marco_login, text="Confirmar", bg="#4CAF50", fg="white",command=self.verificar_login).pack(pady=10)

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()
        self.controlador.login(usuario, contrasena)

    def mostrar_error_login(self):
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def mostrar_menu_principal(self):
        self.marco_login.destroy()
        self.marco_menu = tk.Frame(self.root, bg="white")
        self.marco_menu.pack(fill='both', expand=True)

        boton_agregar = tk.Button(self.marco_menu, text="Registrar invernaderos", bg="#F5F5DC", command=self.mostrar_formulario)
        boton_agregar.pack(pady=10)

        self.lista_frame = tk.Frame(self.marco_menu, bg="white")
        self.lista_frame.pack(fill='both', expand=True)

        self.actualizar_lista_invernaderos()

    def mostrar_formulario(self):
        if self.marco_agregar:
            self.marco_agregar.destroy()

        self.marco_agregar = tk.Toplevel(self.root)
        self.marco_agregar.title("Registrar invernadero")
        self.marco_agregar.configure(bg="white")

        campos = [
            ("Nombre del invernadero", "nombre"),
            ("Capacidad de producción", "capacidad"),
            ("Superficie (m²)", "superficie"),
            ("Tipo de cultivo", "cultivo"),
            ("Fecha de creación (YYYY-MM-DD)", "fecha"),
            ("Responsable del invernadero", "responsable")
        ]
        self.entradas = {}
        for i, (texto, clave) in enumerate(campos):
            tk.Label(self.marco_agregar, text=texto, bg="white").grid(row=i, column=0, sticky="e", padx=10, pady=5)
            entrada = tk.Entry(self.marco_agregar, bg="#f0f7da")
            entrada.grid(row=i, column=1, padx=10, pady=5)
            self.entradas[clave] = entrada

        tk.Label(self.marco_agregar, text="Sistema de riego", bg="white").grid(row=len(campos), column=0, sticky="e", padx=10, pady=5)
        self.sistema_riego_var = tk.StringVar(value="Manual")
        opciones = ["Manual", "Automatizado", "Por goteo"]
        riego_menu = ttk.Combobox(self.marco_agregar, textvariable=self.sistema_riego_var, values=opciones, state="readonly")
        riego_menu.grid(row=len(campos), column=1, padx=10, pady=5)

        tk.Button(self.marco_agregar, text="Guardar", bg="green", fg="white",command=self.enviar_datos).grid(row=7, column=0, pady=15)
        tk.Button(self.marco_agregar, text="Cancelar", bg="red", fg="white",command=self.marco_agregar.destroy).grid(row=7, column=1, pady=15)

    def enviar_datos(self):
        try:
            datos = [
                self.entradas["nombre"].get(),
                self.entradas["capacidad"].get(),
                self.entradas["superficie"].get(),
                self.entradas["cultivo"].get(),
                self.entradas["fecha"].get(),
                self.entradas["responsable"].get(),
                self.sistema_riego_var.get()
            ]
            self.controlador.agregar_invernadero(datos)
            self.marco_agregar.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    def actualizar_lista_invernaderos(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        invernaderos = self.controlador.obtener_invernaderos()
        for i, inv in enumerate(invernaderos):
            texto = (
                f"{inv.nombre}\n"
                f"Capacidad: {inv.capacidad}\n"
                f"Superficie: {inv.superficie} m²\n"
                f"Tipo: {inv.tipo_cultivo}\n"
                f"Creación: {inv.fecha_creacion}\n"
                f"Responsable: {inv.responsable}\n"
                f"Riego: {inv.sistema_riego}"
            )
            tk.Label(self.lista_frame, text=texto, bg="#f0f7da", justify="left", relief="solid", bd=1,
                     padx=10, pady=5, width=40, anchor="w").grid(row=i // 2, column=i % 2, padx=10, pady=10)
    
    def seleccionar_item(self, event):
        item = self.tree.selection()
        if item:
            index = self.tree.index(item[0])
            invernadero = self.controlador.obtener_invernaderos()[index]
            self.entrada_nombre.delete(0, tk.END)
            self.entrada_nombre.insert(0, invernadero.nombre)

    def modificar_invernadero(self):
        item = self.tree.selection()
        if item:
            index = self.tree.index(item[0])
            datos = self.obtener_datos_formulario()
            if datos:
                self.controlador.modificar_invernadero(index, datos)
                self.limpiar_campos()

    def eliminar_invernadero(self):
        item = self.tree.selection()
        if item:
            index = self.tree.index(item[0])
            self.controlador.eliminar_invernadero(index)
            self.limpiar_campos()

