import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
from utils import extraer_numero_id
import styles as st


class AgenciaEspacialApp:
    def __init__(self, root, db_manager):
        self.root = root
        self.db = db_manager

        self.root.title(st.WINDOW_TITLE)
        self.root.geometry(st.WINDOW_SIZE)
        self.root.resizable(*st.WINDOW_RESIZABLE)

        # conectar a la base de datos al iniciar
        exito, err = self.db.conectar()
        if not exito:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos:\n{err}")

        # construir la interfaz gráfica
        self.crear_widgets()

        self.root.protocol("WM_DELETE_WINDOW", self.al_cerrar)

        self.mostrar_agencias()

    def crear_widgets(self):
        frame_form = tk.LabelFrame(
            self.root, 
            text="Detalles de la Agencia Espacial", 
            **st.FRAME_INNER_PADDING
        )
        frame_form.pack(fill="x", **st.FRAME_OUTER_PADDING)

        tk.Label(frame_form, text="ID Único:").grid(row=0, column=0, sticky="w", **st.LABEL_GRID_PADDING)
        self.entry_id = tk.Entry(frame_form, width=st.ENTRY_WIDTH)
        self.entry_id.grid(row=0, column=1, **st.ENTRY_GRID_PADDING)

        tk.Label(frame_form, text="Nombre Agencia:").grid(row=1, column=0, sticky="w", **st.LABEL_GRID_PADDING)
        self.entry_nombre = tk.Entry(frame_form, width=st.ENTRY_WIDTH)
        self.entry_nombre.grid(row=1, column=1, **st.ENTRY_GRID_PADDING)

        tk.Label(frame_form, text="País de Origen:").grid(row=2, column=0, sticky="w", **st.LABEL_GRID_PADDING)
        self.entry_pais = tk.Entry(frame_form, width=st.ENTRY_WIDTH)
        self.entry_pais.grid(row=2, column=1, **st.ENTRY_GRID_PADDING)

        tk.Label(frame_form, text="Fecha Creación (AAAA-MM-DD):").grid(row=3, column=0, sticky="w", **st.LABEL_GRID_PADDING)
        self.entry_fecha = tk.Entry(frame_form, width=st.ENTRY_WIDTH)
        self.entry_fecha.grid(row=3, column=1, **st.ENTRY_GRID_PADDING)

        # botones para el CRUD
        frame_botones = tk.Frame(self.root, **st.FRAME_BOTONES_PADDING)
        frame_botones.pack()

        self.btn_agregar = tk.Button(
            frame_botones, text="Agregar Agencia", command=self.agregar_agencia, width=st.BUTTON_WIDTH
        )
        self.btn_agregar.grid(row=0, column=0, **st.BUTTON_GRID_PADDING)

        self.btn_mostrar = tk.Button(
            frame_botones, text="Mostrar Agencias", command=self.mostrar_agencias, width=st.BUTTON_WIDTH
        )
        self.btn_mostrar.grid(row=0, column=1, **st.BUTTON_GRID_PADDING)

        self.btn_actualizar = tk.Button(
            frame_botones, text="Actualizar Agencia", command=self.actualizar_agencia, width=st.BUTTON_WIDTH
        )
        self.btn_actualizar.grid(row=1, column=0, **st.BUTTON_GRID_PADDING)

        self.btn_borrar = tk.Button(
            frame_botones, text="Borrar Agencia", command=self.borrar_agencia, width=st.BUTTON_WIDTH
        )
        self.btn_borrar.grid(row=1, column=1, **st.BUTTON_GRID_PADDING)

        # lista de las agencias
        frame_lista = tk.LabelFrame(
            self.root, 
            text="Agencias Espaciales Almacenadas", 
            **st.FRAME_INNER_PADDING
        )
        frame_lista.pack(fill="both", expand=True, **st.FRAME_OUTER_PADDING)

        self.lista_agencias = tk.Listbox(
            frame_lista, selectmode=tk.SINGLE, width=st.LISTBOX_WIDTH, height=st.LISTBOX_HEIGHT
        )
        self.lista_agencias.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=self.lista_agencias.yview)
        scrollbar.pack(side="right", fill="y")
        self.lista_agencias.config(yscrollcommand=scrollbar.set)

        self.lista_agencias.bind('<<ListboxSelect>>', self.cargar_datos_seleccionados)

    def agregar_agencia(self):
        agencia_id = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        pais = self.entry_pais.get().strip()
        fecha = self.entry_fecha.get().strip()

        if not agencia_id or not nombre or not pais or not fecha:
            messagebox.showwarning("Campos Incompletos", "Por favor complete todos los campos requeridos.")
            return

        try:
            self.db.agregar_agencia(int(agencia_id), nombre, pais, fecha)
            messagebox.showinfo("Éxito", f"Agencia '{nombre}' agregada correctamente.")
            self.mostrar_agencias()
            self.limpiar_campos()
        except Error as e:
            messagebox.showerror("Error SQL", f"Error al insertar en la base de datos:\n{str(e)}")
        except ValueError:
            messagebox.showerror("Error de Formato", "El ID debe ser un número entero válido.")

    def mostrar_agencias(self):
        try:
            self.lista_agencias.delete(0, tk.END)
            agencias = self.db.obtener_agencias()

            for agencia in agencias:
                item_text = f"ID: {agencia[0]}, Nombre: {agencia[1]}, País: {agencia[2]}, Fecha: {agencia[3]}"
                self.lista_agencias.insert(tk.END, item_text)
        except Error as e:
            messagebox.showerror("Error SQL", f"Error al recuperar los datos:\n{str(e)}")

    def cargar_datos_seleccionados(self, event):
        seleccion = self.lista_agencias.curselection()
        if seleccion:
            item_seleccionado = self.lista_agencias.get(seleccion[0])
            agencia_id = extraer_numero_id(item_seleccionado)

            if agencia_id:
                try:
                    datos = self.db.obtener_agencia_por_id(agencia_id)
                    if datos:
                        self.entry_id.delete(0, tk.END)
                        self.entry_id.insert(0, str(datos[0]))
                        self.entry_nombre.delete(0, tk.END)
                        self.entry_nombre.insert(0, datos[1])
                        self.entry_pais.delete(0, tk.END)
                        self.entry_pais.insert(0, datos[2])
                        self.entry_fecha.delete(0, tk.END)
                        self.entry_fecha.insert(0, str(datos[3]))
                except Error as e:
                    messagebox.showerror("Error SQL", f"Error al consultar el registro:\n{str(e)}")

    def actualizar_agencia(self):
        agencia_id = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        pais = self.entry_pais.get().strip()
        fecha = self.entry_fecha.get().strip()

        if not agencia_id or not nombre or not pais or not fecha:
            messagebox.showwarning("Advertencia", "Seleccione un registro y asegúrese de completar todos los campos.")
            return

        try:
            self.db.actualizar_agencia(int(agencia_id), nombre, pais, fecha)
            messagebox.showinfo("Éxito", f"Agencia con ID {agencia_id} actualizada correctamente.")
            self.mostrar_agencias()
            self.limpiar_campos()
        except Error as e:
            messagebox.showerror("Error SQL", f"Error al actualizar el registro:\n{str(e)}")

    def borrar_agencia(self):
        seleccion = self.lista_agencias.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una agencia de la lista para proceder a borrar.")
            return

        item_seleccionado = self.lista_agencias.get(seleccion[0])
        agencia_id = extraer_numero_id(item_seleccionado)

        if agencia_id:
            confirmacion = messagebox.askyesno(
                "Confirmación de Borrado",
                f"¿Está seguro de que desea eliminar la agencia con ID {agencia_id}?\nEsta acción no se puede deshacer."
            )

            if confirmacion:
                try:
                    self.db.borrar_agencia(agencia_id)
                    messagebox.showinfo("Éxito", f"Agencia con ID {agencia_id} borrada correctamente.")
                    self.mostrar_agencias()
                    self.limpiar_campos()
                except Error as e:
                    messagebox.showerror("Error SQL", f"Error al eliminar el registro:\n{str(e)}")

    def limpiar_campos(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_pais.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)

    def al_cerrar(self):
        self.db.cerrar()
        self.root.destroy()
