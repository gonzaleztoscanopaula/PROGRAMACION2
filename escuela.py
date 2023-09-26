import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(host="localhost", user="root", port="3305", password="12345678", database="escuela")

# Función para cargar y mostrar información en el Treeview
def cargar_datos():
    tree.delete(*tree.get_children())  # Borrar datos existentes en el Treeview
    cursor = conexion.cursor()
    cursor.execute("SELECT Alumnos.IDALUMNO, Alumnos.NOMBRE, Alumnos.APELLIDO, Alumnos.DNI, Carreras.NOMBRE, EstadoAlumno.NOMBRE FROM Alumnos JOIN Carreras ON Alumnos.IDCARRERA = Carreras.IDCARRERA JOIN EstadoAlumno ON Alumnos.IDESTADOALUMNO = EstadoAlumno.IDESTADOALUMNO WHERE EstadoAlumno.NOMBRE = 'Regular'")
    for row in cursor.fetchall():
        # Convertir el nombre a mayúsculas y luego a minúsculas
        nombre = row[1].capitalize()
        apellido = row[2].upper()
        tree.insert("", "end", values=(row[0], nombre, apellido, row[3], row[4], row[5]))

# Función para mostrar todos los alumnos sin importar su estado
def ver_todos_los_alumnos():
    tree.delete(*tree.get_children())  # Borrar datos existentes en el Treeview
    cursor = conexion.cursor()
    cursor.execute("SELECT Alumnos.IDALUMNO, Alumnos.NOMBRE, Alumnos.APELLIDO, Alumnos.DNI, Carreras.NOMBRE, EstadoAlumno.NOMBRE FROM Alumnos JOIN Carreras ON Alumnos.IDCARRERA = Carreras.IDCARRERA JOIN EstadoAlumno ON Alumnos.IDESTADOALUMNO = EstadoAlumno.IDESTADOALUMNO")
    for row in cursor.fetchall():
        # Convertir el nombre a mayúsculas y luego a minúsculas
        nombre = row[1].capitalize()
        apellido = row[2].upper()
        tree.insert("", "end", values=(row[0], nombre, apellido, row[3], row[4], row[5]))

# Función para llenar el formulario con datos de la grilla
def llenar_formulario_desde_grilla(event):
    seleccion = tree.selection()
    if not seleccion:
        return
    
    

    item = tree.item(seleccion)
    id_alumno = item['values'][0]  # ID del alumno seleccionado

    cursor = conexion.cursor()
    cursor.execute("SELECT NOMBRE, APELLIDO, DNI, IDCARRERA, IDESTADOALUMNO FROM Alumnos WHERE IDALUMNO = %s", (id_alumno,))
    alumno = cursor.fetchone()

    nombre_entry.delete(0, tk.END)
    nombre_entry.insert(0, alumno[0].upper())  # Nombre del alumno en mayúsculas
    apellido_entry.delete(0, tk.END)
    apellido_entry.insert(0, alumno[1].upper())  # Apellido del alumno en mayúsculas
    dni_entry.delete(0, tk.END)
    dni_entry.insert(0, alumno[2])  # DNI del alumno

    carrera_id = alumno[3]  # ID de la carrera seleccionada
    estado_alumno_id = alumno[4]  # ID del estado seleccionado

    # Obtener el nombre de la carrera seleccionada
    carrera_nombre = obtener_nombre_carrera(carrera_id)
    
    # Obtener el nombre del estado seleccionado
    estado_alumno_nombre = obtener_nombre_estado(estado_alumno_id)

    carrera_combobox.set(carrera_nombre)  # Establecer la carrera seleccionada en el ComboBox
    estado_combobox.set(estado_alumno_nombre)  # Establecer el estado seleccionado en el ComboBox

    modificar_button.config(state=tk.NORMAL)
    global id_alumno_seleccionado
    id_alumno_seleccionado = id_alumno  # Almacenar el ID del alumno seleccionado

# Función para obtener el nombre de la carrera según su ID
def obtener_nombre_carrera(id_carrera):
    for carrera in carreras:
        if carrera[0] == id_carrera:
            return carrera[1]
    return ""

# Función para obtener el nombre del estado según su ID
def obtener_nombre_estado(id_estado):
    for estado in estados:
        if estado[0] == id_estado:
            return estado[1]
    return ""

# Función para guardar cambios en el registro seleccionado
def guardar_cambios():
    nombre = nombre_entry.get().upper()
    apellido = apellido_entry.get().upper()
    dni = dni_entry.get()
    carrera_nombre = carrera_combobox.get()
    estado_alumno_nombre = estado_combobox.get()
    estado_alumno_id = None

    if not dni.isdigit() or len(dni) != 8:
        messagebox.showerror("Error", "El DNI debe contener exactamente 8 números.")
        return

    if nombre and apellido and dni and carrera_nombre and estado_alumno_nombre:
        # Verificar si el DNI ya existe en la misma carrera
        if not dni_disponible_en_carrera(dni, carrera_nombre):
            messagebox.showerror("Error", "El DNI ya existe en la misma carrera.")
            return

        carrera_id = obtener_id_carrera(carrera_nombre)
        
        # Obtener el ID del estado del alumno seleccionado
        for estado in estados:
            if estado[1] == estado_alumno_nombre:
                estado_alumno_id = estado[0]
                break

        cursor = conexion.cursor()
        cursor.execute("UPDATE Alumnos SET NOMBRE = %s, APELLIDO = %s, DNI = %s, IDCARRERA = %s, IDESTADOALUMNO = %s WHERE IDALUMNO = %s", (nombre, apellido, dni, carrera_id, estado_alumno_id, id_alumno_seleccionado))
        conexion.commit()
        cargar_datos()
        limpiar_formulario()
    else:
        mostrar_alerta("Los campos son obligatorios. Debe completarlos.")

# Función para verificar si el DNI ya existe en la misma carrera
def dni_disponible_en_carrera(dni, carrera_nombre):
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM Alumnos a JOIN Carreras c ON a.IDCARRERA = c.IDCARRERA WHERE a.DNI = %s AND c.NOMBRE = %s", (dni, carrera_nombre))
    count = cursor.fetchone()[0]
    return count == 0

# Función para obtener el ID de la carrera según su nombre
def obtener_id_carrera(nombre_carrera):
    for carrera in carreras:
        if carrera[1] == nombre_carrera:
            return carrera[0]
    return None

# Función para obtener el ID del estado según su nombre
def obtener_id_estado(nombre_estado):
    for estado in estados:
        if estado[1] == nombre_estado:
            return estado[0]
    return None

# Función para guardar un nuevo registro de alumno
def guardar_alumno():
    nombre = nombre_entry.get().upper()
    apellido = apellido_entry.get().upper()
    dni = dni_entry.get()
    carrera_nombre = carrera_combobox.get()
    estado_alumno_nombre = estado_combobox.get()
    estado_alumno_id = None

    if not dni.isdigit() or len(dni) != 8:
        messagebox.showerror("Error", "El DNI debe contener exactamente 8 números.")
        return

    if nombre and apellido and dni and carrera_nombre and estado_alumno_nombre:
        # Verificar si el DNI ya existe en la misma carrera
        if not dni_disponible_en_carrera(dni, carrera_nombre):
            messagebox.showerror("Error", "El DNI ya existe en la misma carrera.")
            return

        carrera_id = obtener_id_carrera(carrera_nombre)
        
        # Obtener el ID del estado del alumno seleccionado
        for estado in estados:
            if estado[1] == estado_alumno_nombre:
                estado_alumno_id = estado[0]
                break

        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Alumnos (NOMBRE, APELLIDO, DNI, IDCARRERA, IDESTADOALUMNO) VALUES (%s, %s, %s, %s, %s)", (nombre, apellido, dni, carrera_id, estado_alumno_id))
        conexion.commit()
        cargar_datos()
        limpiar_formulario()
    else:
        mostrar_alerta("Los campos son obligatorios. Debe completarlos.")

# Función para limpiar el formulario
def limpiar_formulario():
    nombre_entry.delete(0, tk.END)
    apellido_entry.delete(0, tk.END)
    dni_entry.delete(0, tk.END)
    carrera_combobox.set("")
    estado_combobox.set("")
    modificar_button.config(state=tk.DISABLED)

# Función para cargar carreras desde la base de datos y cargarlas en el ComboBox
def cargar_carreras():
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT IDCARRERA, NOMBRE FROM Carreras ORDER BY NOMBRE")
        carreras = cursor.fetchall()
        # Obtener solo los nombres de las carreras
        nombres_carreras = [row[1] for row in carreras]
        carrera_combobox['values'] = nombres_carreras
        return carreras  # Devolver también la lista completa de carreras con sus IDs
    except Exception as e:
        mostrar_alerta(f"Error al cargar carreras: {str(e)}")
        return []

# Función para cargar estados de alumnos desde la base de datos y cargarlos en el ComboBox
def cargar_estados_alumno():
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT IDESTADOALUMNO, NOMBRE FROM EstadoAlumno ORDER BY NOMBRE")
        estados = cursor.fetchall()
        # Obtener solo los nombres de los estados
        nombres_estados = [row[1] for row in estados]
        estado_combobox['values'] = nombres_estados
        return estados  # Devolver también la lista completa de estados con sus IDs
    except Exception as e:
        mostrar_alerta(f"Error al cargar estados de alumno: {str(e)}")
        return []

# Función para mostrar una ventana de alerta
def mostrar_alerta(mensaje):
    messagebox.showwarning("Alerta", mensaje)

# Función para cambiar el estado del alumno a "libre"
def cambiar_estado_alumno():
    seleccion = tree.selection()
    if not seleccion:
        return

    confirmacion = messagebox.askyesno("Confirmar cambio de estado", "¿Está seguro de eliminar este registro?")
    if not confirmacion:
        return

    item = tree.item(seleccion)
    id_alumno = item['values'][0]

    cursor = conexion.cursor()
    cursor.execute("UPDATE Alumnos SET IDESTADOALUMNO = 2 WHERE IDALUMNO = %s", (id_alumno,))
    conexion.commit()
    
    # Eliminar el elemento seleccionado del Treeview
    tree.delete(seleccion)

# Crear ventana
root = tk.Tk()
root.title("Consulta de Alumnos")

# Crear un frame con un borde visible para el formulario de inscripción
formulario_frame = tk.Frame(root, bd=2, relief=tk.SOLID)
formulario_frame.pack(padx=10, pady=10)

# Título del formulario
titulo_label = tk.Label(formulario_frame, text="Formulario Inscripción", font=("Helvetica", 14))
titulo_label.grid(row=0, column=0, columnspan=2, pady=10)

# Campos de entrada para nombre, apellido y DNI con el mismo ancho que el ComboBox
nombre_label = tk.Label(formulario_frame, text="Nombre:")
nombre_label.grid(row=1, column=0)
nombre_entry = tk.Entry(formulario_frame)
nombre_entry.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

apellido_label = tk.Label(formulario_frame, text="Apellido:")
apellido_label.grid(row=2, column=0)
apellido_entry = tk.Entry(formulario_frame)
apellido_entry.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

dni_label = tk.Label(formulario_frame, text="DNI:")
dni_label.grid(row=3, column=0)
dni_entry = tk.Entry(formulario_frame)
dni_entry.grid(row=3, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

# Combo box para la carrera
carrera_label = tk.Label(formulario_frame, text="Carrera:")
carrera_label.grid(row=4, column=0)
carrera_combobox = ttk.Combobox(formulario_frame, state="readonly")
carrera_combobox.grid(row=4, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

# Combo box para el estado del alumno
estado_label = tk.Label(formulario_frame, text="Estado del Alumno:")
estado_label.grid(row=5, column=0)
estado_combobox = ttk.Combobox(formulario_frame, state="readonly")
estado_combobox.grid(row=5, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

# Cargar las carreras y estados al inicio de la aplicación y obtener la lista de carreras y estados con sus IDs
carreras = cargar_carreras()
estados = cargar_estados_alumno()

# Botón para guardar un nuevo registro de alumno
guardar_button = tk.Button(formulario_frame, text="Guardar", command=guardar_alumno)
guardar_button.grid(row=6, columnspan=2, pady=10, sticky="ew")

# Botón para limpiar el formulario
limpiar_button = tk.Button(formulario_frame, text="Limpiar", command=limpiar_formulario)
limpiar_button.grid(row=10, columnspan=2, pady=10, sticky="ew")

# Botón para ver la lista de todos los alumnos
ver_todos_button = tk.Button(formulario_frame, text="Ver Todos los Alumnos", command=ver_todos_los_alumnos)
ver_todos_button.grid(row=11, columnspan=2, pady=10, sticky="ew")


# Crear Treeview para mostrar la información
tree = ttk.Treeview(root, columns=("ID", "Nombre", "Apellido", "DNI", "Carrera", "Estado"))
tree.heading("#2", text="Nombre")
tree.heading("#3", text="Apellido")
tree.heading("#4", text="DNI")
tree.heading("#5", text="Carrera")
tree.heading("#6", text="Estado")
tree.column("#1", width=0, stretch=tk.NO)  # Ocultar la columna #1 que muestra el ID
tree.column("#0", width=0, stretch=tk.NO)  # Ocultar la columna #0 que habitualmente muestra las primary key de los objetos
tree.pack(padx=10, pady=10)

# Botón para cargar datos
cargar_button = tk.Button(formulario_frame, text="Cargar Datos", command=cargar_datos)
cargar_button.grid(row=7, columnspan=2, pady=10, sticky="ew")

# Habilitar la selección de elementos en el Treeview
tree.bind("<ButtonRelease-1>", llenar_formulario_desde_grilla)

# Botón para guardar cambios
modificar_button = tk.Button(formulario_frame, text="Modificar", command=guardar_cambios, state=tk.DISABLED)
modificar_button.grid(row=8, columnspan=2, pady=10, sticky="ew")

# Botón para cambiar el estado del alumno a "libre"
cambiar_estado_button = tk.Button(formulario_frame, text="Eliminar", command=cambiar_estado_alumno)
cambiar_estado_button.grid(row=9, columnspan=2, pady=10, sticky="ew")

def llenar_formulario_desde_grilla(event):
    seleccion = tree.selection()
    if not seleccion:
        return

    item = tree.item(seleccion)
    id_alumno = item['values'][0]  # ID del alumno seleccionado

    cursor = conexion.cursor()
    cursor.execute("SELECT NOMBRE, APELLIDO, DNI, IDCARRERA, IDESTADOALUMNO FROM Alumnos WHERE IDALUMNO = %s", (id_alumno,))
    alumno = cursor.fetchone()

    nombre_entry.delete(0, tk.END)
    nombre_entry.insert(0, alumno[0])  # Nombre del alumno (en mayúsculas o minúsculas según esté almacenado)
    apellido_entry.delete(0, tk.END)
    apellido_entry.insert(0, alumno[1].upper())  # Apellido del alumno en mayúsculas
    dni_entry.delete(0, tk.END)
    dni_entry.insert(0, alumno[2])  # DNI del alumno

    carrera_id = alumno[3]  # ID de la carrera seleccionada
    estado_alumno_id = alumno[4]  # ID del estado seleccionado

    # Obtener el nombre de la carrera seleccionada
    carrera_nombre = obtener_nombre_carrera(carrera_id)
    
    # Obtener el nombre del estado seleccionado
    estado_alumno_nombre = obtener_nombre_estado(estado_alumno_id)

    carrera_combobox.set(carrera_nombre)  # Establecer la carrera seleccionada en el ComboBox
    estado_combobox.set(estado_alumno_nombre)  # Establecer el estado seleccionado en el ComboBox

    modificar_button.config(state=tk.NORMAL)
    global id_alumno_seleccionado
    id_alumno_seleccionado = id_alumno  # Almacenar el ID del alumno seleccionado


# Ejecutar la aplicación
root.mainloop()

# Cerrar la conexión a la base de datos al cerrar la aplicación
conexion.close()
