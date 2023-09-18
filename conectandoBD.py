import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(host="localhost",port=3305, user="root", password="12345678", database="ESCUELA")

# Función para validar el DNI
def validar_dni(dni):
    # Aquí puedes agregar tu lógica de validación para el DNI
    # Por ejemplo, asegurarte de que sea un número válido y tenga la longitud adecuada
    # Devuelve True si es válido, False en caso contrario
    return True

# Función para cargar y mostrar información en el Treeview
def cargar_datos():
    tree.delete(*tree.get_children())  # Borrar datos existentes en el Treeview
    cursor = conexion.cursor()
    cursor.execute("SELECT Alumnos.NOMBRE, Alumnos.APELLIDO, Carreras.NOMBRE FROM Alumnos JOIN Carreras ON Alumnos.IDCARRERA = Carreras.IDCARRERA WHERE Alumnos.IDESTADOALUMNO = 1")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# Función para cargar los estados de alumno en el ComboBox
def cargar_estado_alumno():
    cursor = conexion.cursor()
    cursor.execute("SELECT IDESTADOALUMNO, DESCRIPCION FROM EstadoAlumno")
    estados = cursor.fetchall()
    estado_combobox['values'] = [row[1] for row in estados]
    return estados  # Devolver también la lista de estados con sus IDs

# Función para mostrar una ventana de alerta
def mostrar_alerta(mensaje):
    messagebox.showwarning("Alerta", mensaje)


# Función para guardar un nuevo registro de alumno
def guardar_alumno():
    nombre = nombre_entry.get().upper()
    apellido = apellido_entry.get().upper()
    dni = dni_entry.get()
    carrera_nombre = carrera_combobox.get()
    estado_alumno = estado_combobox.get()  # Obtener el estado del alumno desde el ComboBox


    if nombre and apellido and dni and carrera_nombre and estado_alumno:
        # Obtener el ID de la carrera seleccionada
        carreras = cargar_carreras()
        carrera_id = None
        for carrera in carreras:
            if carrera[1] == carrera_nombre:
                carrera_id = carrera[0]
                break
            

        cursor = conexion.cursor()
        # Insertar un nuevo registro en la tabla Alumnos con el ID de carrera y el estado del alumno
        cursor.execute("INSERT INTO Alumnos (NOMBRE, APELLIDO, DNI, IDCARRERA, IDESTADOALUMNO) VALUES (%s, %s, %s, %s, %s)", (nombre, apellido, dni, carrera_id, estado_alumno))
        conexion.commit()
        cargar_datos()  # Actualizar la vista
        # Limpiar los campos después de insertar
        nombre_entry.delete(0, tk.END)
        apellido_entry.delete(0, tk.END)
        dni_entry.delete(0, tk.END)
        carrera_combobox.set("")  # Limpiar la selección del ComboBox
        estado_combobox.set("")  # Limpiar la selección del ComboBox de estado
    else:
        mostrar_alerta("Los campos son obligatorios. Debe completarlos.")


# Función para cargar las carreras en el ComboBox
def cargar_carreras():
    cursor = conexion.cursor()
    cursor.execute("SELECT IDCARRERA, NOMBRE FROM Carreras ORDER BY NOMBRE")
    carreras = cursor.fetchall()
    carrera_combobox['values'] = [row[1] for row in carreras]
    return carreras  # Devolver también la lista de carreras con sus IDs

# Función para cargar datos de un registro seleccionado para edición
# Función para cargar datos de un registro seleccionado para edición
def cargar_registro_seleccionado():
    selected_item = tree.selection()[0]  # Obtener el ítem seleccionado en el Treeview
    values = tree.item(selected_item, 'values')  # Obtener los valores de las columnas
    # Autocompletar los campos con los valores seleccionados
    nombre_entry.delete(0, tk.END)
    nombre_entry.insert(0, values[0])
    apellido_entry.delete(0, tk.END)
    apellido_entry.insert(0, values[1])
    dni_entry.delete(0, tk.END)
    dni_entry.insert(0, "")  # Deja el campo DNI en blanco para que el usuario pueda editar
    carrera_combobox.set(values[2])  # Seleccionar la carrera
    # Cargar los estados de alumno en el ComboBox
    estados = cargar_estado_alumno()
    estado_id = None
    for estado in estados:
        if estado[1] == "REGULAR":
            estado_id = estado[0]
            break
    estado_combobox.set(estado_id)  # Seleccionar el estado "REGULAR"

# Función para guardar cambios en un registro existente
def guardar_cambios():
    selected_item = tree.selection()[0]  # Obtener el ítem seleccionado en el Treeview
    values = tree.item(selected_item, 'values')  # Obtener los valores de las columnas
    nombre = nombre_entry.get().upper()
    apellido = apellido_entry.get().upper()
    dni = dni_entry.get()
    carrera_nombre = carrera_combobox.get()
    estado_id = estado_combobox.get()

    if nombre and apellido and validar_dni(dni) and carrera_nombre and estado_id:
        # Obtener el ID de la carrera seleccionada
        carreras = cargar_carreras()
        carrera_id = None
        for carrera in carreras:
            if carrera[1] == carrera_nombre:
                carrera_id = carrera[0]
                break

        cursor = conexion.cursor()
        # Actualizar el registro existente en la tabla Alumnos con los nuevos valores
        cursor.execute("UPDATE Alumnos SET NOMBRE=%s, APELLIDO=%s, DNI=%s, IDCARRERA=%s, IDESTADOALUMNO=%s WHERE NOMBRE=%s AND APELLIDO=%s", (nombre, apellido, dni, carrera_id, estado_id, values[0], values[1]))
        conexion.commit()
        cargar_datos()  # Actualizar la vista
        # Limpiar los campos después de insertar
        nombre_entry.delete(0, tk.END)
        apellido_entry.delete(0, tk.END)
        dni_entry.delete(0, tk.END)
        carrera_combobox.set("")  # Limpiar la selección del ComboBox
        estado_combobox.set("")  # Limpiar la selección del ComboBox de estado
    else:
        mostrar_alerta("Los campos son obligatorios. Debe completarlos correctamente.")

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
carrera_combobox = ttk.Combobox(formulario_frame, state="readonly")  # Configurar el ComboBox como de solo lectura
carrera_combobox.grid(row=4, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

# Combo box para el estado de alumno
estado_label = tk.Label(formulario_frame, text="Estado Alumno:")
estado_label.grid(row=5, column=0)
estado_combobox = ttk.Combobox(formulario_frame, state="readonly")  # Configurar el ComboBox como de solo lectura
estado_combobox.grid(row=5, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="ew")

# Cargar las carreras al inicio de la aplicación
cargar_carreras()

# Botón para guardar un nuevo registro de alumno
guardar_button = tk.Button(formulario_frame, text="Guardar", command=guardar_alumno)
guardar_button.grid(row=6, columnspan=2, pady=10, sticky="ew")

# Botón para cargar datos
cargar_button = tk.Button(root, text="Cargar Datos", command=cargar_datos)
cargar_button.pack(pady=5)

# Botón para modificar un registro existente
modificar_button = tk.Button(root, text="Modificar", command=cargar_registro_seleccionado)
modificar_button.pack(pady=5)

# Botón para guardar cambios en un registro existente
guardar_cambios_button = tk.Button(root, text="Guardar Cambios", command=guardar_cambios)
guardar_cambios_button.pack(pady=5)

# Crear Treeview para mostrar la información
tree = ttk.Treeview(root, columns=("Nombre", "Apellido", "Carrera"))
tree.heading("#1", text="Nombre")
tree.heading("#2", text="Apellido")
tree.heading("#3", text="Carrera")
tree.column("#0", width=0, stretch=tk.NO)  # Ocultar la columna #0 que habitualmente muestra las primary key de los objetos
tree.pack(padx=10, pady=10)

# Ejecutar la aplicación
root.mainloop()

# Cerrar la conexión a la base de datos al cerrar la aplicación
conexion.close()
