import tkinter as tk
from tkinter import ttk
import mysql.connector

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3305,
    password="12345678",
    database="ALMACEN"
)

# Función para cargar y mostrar información en el Treeview
def cargar_datos():
    tree.delete(*tree.get_children()) # Borrar datos existentes en el Treeview
    cursor = conexion.cursor()
    cursor.execute("SELECT producto.nombre, categoria.nombre, marca.nombre FROM producto JOIN categoria ON producto.id_categoria = categoria.id JOIN marca ON producto.id_marca = marca.id")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# Crear ventana
root = tk.Tk()
root.title("Almacen de Productos La Nona")

# Cambiar el color de fondo de la ventana a un tono pastel (azul claro)
root.configure(bg="#add8e6")

# Configurar el estilo del Treeview
style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 12), background="#f5f5f5")  # Fondo en tono pastel
style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="#add8e6")  # Encabezados en tono pastel

# Crear Treeview para mostrar la información
tree = ttk.Treeview(root, columns=("Nombre", "Categoría", "Marca"), show="headings")
tree.heading("#1", text="Nombre")
tree.heading("#2", text="Categoría")
tree.heading("#3", text="Marca")
tree.column("#0", width=0, stretch=tk.NO)  # Ocultar la columna #0 que habitualmente muestra las primary key de los objetos
tree.pack(padx=10, pady=10)

# Estilo para el botón
style.configure("TButton", font=("Helvetica", 12, "bold"), foreground="white", background="#ff69b4")  # Botón en tono pastel

# Botón para cargar datos
cargar_button = ttk.Button(root, text="Cargar Datos", command=cargar_datos, style="TButton")
cargar_button.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()

# Cerrar la conexión a la base de datos al cerrar la aplicación
conexion.close()
