from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from db_connection import *
from tkinter.messagebox import *
import re
from datetime import datetime

root = Tk()
root.geometry("1096x600")
root.resizable(False, False)
root.title("A Ver Si Ahorra!!!")


# Definir las Variables del Entorno Gráfico
var_tk_fecha = StringVar()
var_tk_categoria = StringVar()
var_tk_nombre_gasto = StringVar()
var_tk_importe = StringVar()
var_tk_descripcion = StringVar()
var_tk_gasto_total = DoubleVar()
var_tk_fecha_desde = StringVar()
var_tk_fecha_hasta = StringVar()

# Agregarle estilo
style = ttk.Style()

# Seleccionar un Theme
style.theme_use("clam")

# Configurar los colores del Treeview
style.configure(
    "Treeview",
    background="#C0C0C0",
    foreground="black",
    rowheight=25,
    fieldblackground="#C0C0C0",
)

# Cambiar color seleccionado
style.map("Treeview", background=[("selected", "#0044F7")])


# Crear un Treeview Frame para crear una Scrollbar
tree_frame = Frame(root)
tree_frame.pack(anchor=NW, padx=10, pady=10)

# Crear Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Crear el Treeview
my_tree = ttk.Treeview(
    tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended"
)
my_tree.pack()

# Configurar el Scrollbar
tree_scroll.config(command=my_tree.yview)

# Definir las Columnas
my_tree["columns"] = (
    "Id",
    "Categoria",
    "Nombre del Gasto",
    "Importe",
    "Fecha",
    "Descripcion",
)

# Formatear a las Columnas
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Id", anchor=W, width=30)
my_tree.column("Categoria", anchor=W, width=150)
my_tree.column("Nombre del Gasto", anchor=W, width=150)
my_tree.column("Importe", anchor=W, width=150)
my_tree.column("Fecha", anchor=W, width=150)
my_tree.column("Descripcion", anchor=W, width=150)

# Crear los Títulos (Headings)
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Id", text="Id", anchor=W)
my_tree.heading("Categoria", text="Categoría", anchor=W)
my_tree.heading("Nombre del Gasto", text="Nombre del Gasto", anchor=W)
my_tree.heading("Importe", text="Importe", anchor=W)
my_tree.heading("Fecha", text="Fecha", anchor=W)
my_tree.heading("Descripcion", text="Descripción", anchor=W)


# Crear etiquetas de filas alternadas en color
my_tree.tag_configure("registros_pares", background="white")
my_tree.tag_configure("registros_impares", background="lightblue")


# Crear una lista para el Menú de Opciones de las Categorías
menu_lista_opciones = [
    "Automotor",
    "Combustible",
    "Delivery",
    "Electrodomésticos",
    "Gastos Médicos",
    "Inmuebles",
    "Impuestos",
    "Limpieza",
    "Ropa",
    "Servicios",
    "Supermercado",
    "Varios",
    "Viáticos",
    "Vivienda",
]

menu_lista_ops2 = [
    "Automotor",
    "Combustible",
    "Delivery",
    "Electrodomésticos",
    "Gastos Médicos",
    "Inmuebles",
    "Impuestos",
    "Limpieza",
    "Ropa",
    "Servicios",
    "Supermercado",
    "Varios",
    "Viáticos",
    "Vivienda",
]


# Crear el label para cuando se apliquen los filtros de la consulta
filtro_aplicado_label = Label(
    root,
    text="¡Filtro aplicado!",
    fg="RED",
    font=("bold"),
)


def label_temporal_consulta():
    # Agrega un label temporal de que se cargó el registro existosamente.
    filtro_aplicado_label.place(x=820, y=50)


def aplicar_filtro_tk():
    fecha_desde = var_tk_fecha_desde.get()
    fecha_hasta = var_tk_fecha_hasta.get()
    categoria = consulta_categoria_var.get()
    print(fecha_desde, fecha_hasta, categoria)
    if fecha_desde != "" and fecha_hasta != "" and categoria == "":
        resultado_consulta, total_gastos = filtrar_registros_db(
            fecha_desde, fecha_hasta, categoria
        )
        actualizar_treeview_filtros(resultado_consulta, total_gastos)
        label_temporal_consulta()
    elif fecha_desde == "" and fecha_hasta == "" and categoria != "":
        resultado_consulta, total_gastos = filtrar_registros_db(
            fecha_desde, fecha_hasta, categoria
        )
        actualizar_treeview_filtros(resultado_consulta, total_gastos)
        label_temporal_consulta()
    elif fecha_desde != "" and fecha_hasta != "" and categoria != "":
        resultado_consulta, total_gastos = filtrar_registros_db(
            fecha_desde, fecha_hasta, categoria
        )
        actualizar_treeview_filtros(resultado_consulta, total_gastos)
        label_temporal_consulta()
    else:
        showerror("ERROR", "Ambas fechas deben estan completas y/o la categoria.")


def remover_filtro_tk():
    consulta_fecha_desde.delete(0, END)
    consulta_fecha_hasta.delete(0, END)
    consulta_categoria_var.set(consulta_categoria_default)
    actualizar_treeview()
    filtro_aplicado_label.destroy()


# Crear el FRAME de Consulta y sus campos
consulta_frame = LabelFrame(root, text="", border=3)
consulta_frame.place(x=820, y=100)

consulta_x_label = Label(
    consulta_frame,
    text="Consultar por:",
    fg="#235CE0",
    font=("Helvetica", "12", "bold"),
)
consulta_x_label.grid(row=0, column=0, sticky=W, padx=1, pady=10)

consulta_categoria_label = Label(consulta_frame, text="Categoria: ")
consulta_categoria_label.grid(row=2, column=0, sticky=W)
consulta_categoria_default = ""
consulta_categoria_var = StringVar(value=consulta_categoria_default)
consulta_categoria = OptionMenu(
    consulta_frame, consulta_categoria_var, consulta_categoria_default, *menu_lista_ops2
)
consulta_categoria.grid(row=2, column=1, sticky=W)

consulta_fecha_label = Label(consulta_frame, text="Fecha Desde: ")
consulta_fecha_label.grid(row=3, column=0, sticky=W)

consulta_fecha_desde = DateEntry(
    consulta_frame, textvariable=var_tk_fecha_desde, date_pattern="dd-mm-y"
)
consulta_fecha_desde.grid(row=3, column=1, sticky=W)

consulta_fecha_label = Label(consulta_frame, text="Fecha hasta: ")
consulta_fecha_label.grid(row=4, column=0, sticky=W)
consulta_fecha_hasta = DateEntry(
    consulta_frame, textvariable=var_tk_fecha_hasta, date_pattern="dd-mm-y"
)
consulta_fecha_hasta.grid(row=4, column=1, sticky=W)

consulta_aplicar_filtro_button = Button(
    consulta_frame,
    text="Aplicar filtro",
    command=aplicar_filtro_tk,
    height=1,
    width=10,
)
consulta_aplicar_filtro_button.grid(row=1, column=0, sticky=W)

consulta_quitar_filtro_button = Button(
    consulta_frame, text="Remover filtro", command=remover_filtro_tk, height=1, width=10
)
consulta_quitar_filtro_button.grid(row=1, column=1, sticky=W)


# Crear el FRAME de TOTAL y sus campos (Labels)
total_frame = LabelFrame(root, text="", border=0)
total_frame.pack(side=TOP, anchor=NE, padx=330, pady=5)

total_gastos = Label(total_frame, text="TOTAL = $", font=("Helvetica", "12", "bold"))
total_gastos.grid(row=0, column=0, sticky=NW)
total_gastos_entry = Label(
    total_frame,
    textvariable=var_tk_gasto_total,
    font=("Helvetica", "12", "bold"),
)
total_gastos_entry.grid(row=0, column=1, sticky=NW)

# Crear el FRAME de DATA y sus campos (Label, Entry, OptionMenu y DateEntry)
data_frame = LabelFrame(root, text="")
data_frame.pack(anchor=W, fill="x", expand="yes", padx=10, pady=10)

nombre_gasto_label = Label(
    data_frame, text="Nombre del Gasto", font=("Helvetica", "11", "bold")
)
nombre_gasto_label.grid(row=0, column=0, padx=10, pady=10)
nombre_gasto_entry = Entry(data_frame, textvariable=var_tk_nombre_gasto, width=20)
nombre_gasto_entry.grid(row=0, column=1, padx=10, pady=10)

importe_label = Label(data_frame, text="Importe", font=("Helvetica", "11", "bold"))
importe_label.grid(row=0, column=2, padx=10, pady=10)
importe_entry = Entry(data_frame, textvariable=var_tk_importe, width=20)
importe_entry.grid(row=0, column=3, padx=10, pady=0)

categoria_label = Label(data_frame, text="Categoría", font=("Helvetica", "11", "bold"))
categoria_label.grid(row=0, column=4, padx=10, pady=10)
categoria_default = ""
categoria_var = StringVar(value=categoria_default)
categoria_entry = OptionMenu(data_frame, categoria_var, *menu_lista_opciones)
categoria_entry.grid(row=0, column=5, padx=10, pady=10)

fecha_label = Label(data_frame, text="Fecha", font=("Helvetica", "11", "bold"))
fecha_label.grid(row=1, column=0, padx=10, pady=10)
fecha_entry = DateEntry(
    data_frame, selectmode="day", textvariable=var_tk_fecha, date_pattern="dd-mm-y"
)
fecha_entry.grid(row=1, column=1, padx=10, pady=10)

descripcion_label = Label(
    data_frame, text="Descripción", font=("Helvetica", "11", "bold")
)
descripcion_label.grid(row=1, column=2, padx=10, pady=10)
descripcion_entry = Entry(data_frame, textvariable=var_tk_descripcion, width=20)
descripcion_entry.grid(row=1, column=3, padx=10, pady=10)

# Sección de funciones para los botones y llamas a la base de datos

# Actualiza el Treeview al iniciar el programa. Carga todos los registros que estén en la base de datos.
def actualizar_treeview_initial():
    count = 0
    # Esta función carga todo lo que está en la base de datos inicialmente.
    # Llamo a la funcion consulta_tabla() para obtener todos los valores cargados y lo asigno a la variable resultado_consulta
    resultado_consulta = consultar_tabla_db()
    # resultado_consulta devuelve los valores cargados en formato tupla. Las recorro para actualizar el tree (vista).
    # (2, 'Servicios', 'ABL', 2500.0, '03/02/22', 'ABL de casa')
    # (1, 'Automotor', 'Patente', 3000.0, '7/12/22', 'Fiat 1')
    for record in resultado_consulta:
        if count % 2 == 0:
            my_tree.insert(
                parent="",
                index="end",
                iid=count,
                text=record[0],  # ID
                values=(
                    record[0],  # ID
                    record[1],  # Categoria
                    record[2],  # Nombre de Gasto
                    record[3],  # Importe
                    record[4],  # Fecha
                    record[5],  # Descripcion
                ),
                tags=("registros_pares",),
            )
        else:
            my_tree.insert(
                parent="",
                index="end",
                iid=count,
                text=record[0],  # ID
                values=(
                    record[0],  # ID
                    record[1],  # Categoria
                    record[2],  # Nombre de Gasto
                    record[3],  # Importe
                    record[4],  # Fecha
                    record[5],  # Descripcion
                ),
                tags=("registros_impares",),
            )
        # Aumentar el contador
        count += 1

    gasto_total = obtener_gastos_total_db()
    var_tk_gasto_total.set(gasto_total)
    consulta_fecha_desde.delete(0, END)
    consulta_fecha_hasta.delete(0, END)
    limpiar_seleccion_tk()


def chequear_variables_tk():
    fecha = var_tk_fecha.get()
    categoria = categoria_var.get()
    nombre_gasto = var_tk_nombre_gasto.get()
    importe = var_tk_importe.get()
    descripcion = var_tk_descripcion.get()

    reg_alfanum = "^[A-Za-záéíóú,0-9,\s]*$"  # regex, validar ingreso alfanumérico.
    if not re.match(reg_alfanum, nombre_gasto) or (nombre_gasto == ""):
        showerror(
            "ERROR", "Gastos no debe estar vacío, debe tener solo letras y números."
        )
    elif fecha == "":
        showerror("ERROR", "Seleccione una Fecha")
    elif categoria == "":
        showerror("ERROR", "Seleccione una Categoria")
    else:
        try:
            importe = int(importe)
            return fecha, categoria, nombre_gasto, importe, descripcion
        except ValueError:
            try:
                importe = float(importe)
                return fecha, categoria, nombre_gasto, importe, descripcion
            except ValueError:
                showerror("ERROR", "Importe debe ser números enteros o decimales")
    # else:
    #     return fecha, categoria, nombre_gasto, importe, descripcion, my_tree


def label_temporal_ingreso_tk():
    # Agrega un label temporal de que se cargó el registro existosamente.
    ingreso_registro_label = Label(
        root,
        text="¡Registro ingresado exitosomente!",
        width=50,
        fg="GREEN",
        font=("bold"),
    )
    ingreso_registro_label.place(x=40, y=295)
    ingreso_registro_label.after(1500, lambda: ingreso_registro_label.destroy())


def agregar_registro_tk():
    # Agrega un registro nuevo.
    # Primero llama a la función para chequear si las variables son correctas.
    (fecha, categoria, nombre_gasto, importe, descripcion) = chequear_variables_tk()
    insertar_registro_db(fecha, categoria, nombre_gasto, importe, descripcion)
    # Llamo a la función para actualizar el entorno gráfico con la nueva alta hecha.
    actualizar_treeview()
    label_temporal_ingreso_tk()  # "Registro ha sido ingresado exitosamente."
    limpiar_seleccion_tk()


def actualizar_treeview():
    # Actualiza el Treeview (Entorno gráfico) ante un evento de alta/modificación.
    count = 0
    # Elimino los registros de la pantalla para cargarlos de nuevo
    records = my_tree.get_children()
    for element in records:
        my_tree.delete(element)

    # Cargo de nuevo los elementos en la pantalla.
    # Llamo a la funcion consulta_tabla() para obtener todos los valores cargados en la DB y lo asigno a la variable resultado_consulta
    resultado_consulta = consultar_tabla_db()
    # resultado_consulta devuelve los valores cargados en formato tupla. Las recorro para actualizar el tree (vista).
    for record in resultado_consulta:
        if count % 2 == 0:
            my_tree.insert(
                parent="",
                index="end",
                iid=count,
                text=record[0],  # ID
                values=(
                    record[0],  # ID
                    record[1],  # Categoria
                    record[2],  # Nombre de Gasto
                    record[3],  # Importe
                    record[4],  # Fecha
                    record[5],  # Descripcion
                ),
                tags=("registros_pares",),
            )
        else:
            my_tree.insert(
                parent="",
                index="end",
                iid=count,
                text=record[0],  # ID
                values=(
                    record[0],  # ID
                    record[1],  # Categoria
                    record[2],  # Nombre de Gasto
                    record[3],  # Importe
                    record[4],  # Fecha
                    record[5],  # Descripcion
                ),
                tags=("registros_impares",),
            )
        # Aumentar el contador
        count += 1
    gasto_total = obtener_gastos_total_db()
    var_tk_gasto_total.set(gasto_total)


def actualizar_treeview_filtros(resultado_consulta, total_gastos):
    # Actualiza el Treeview (Entorno gráfico) ante un evento de filtro.
    count = 0
    # Elimino los registros de la pantalla para cargarlos de nuevo
    records = my_tree.get_children()
    for element in records:
        my_tree.delete(element)

    # resultado_consulta devuelve los valores cargados en formato tupla. Las recorro para actualizar el tree (vista).
    # (2, 'Servicios', 'ABL', 2500.0, '03/02/22', 'ABL de casa')
    # (1, 'Automotor', 'Patente', 3000.0, '7/12/22', 'Fiat 1')
    for record in resultado_consulta:
        if count % 2 == 0:
            my_tree.insert(
                parent="",
                index="end",
                iid=count,
                text=record[0],  # ID
                values=(
                    record[0],  # ID
                    record[1],  # Categoria
                    record[2],  # Nombre de Gasto
                    record[3],  # Importe
                    record[4],  # Fecha
                    record[5],  # Descripcion
                ),
                tags=("registros_pares",),
            )
        else:
            my_tree.insert(
                parent="",
                index="end",
                iid=count,
                text=record[0],  # ID
                values=(
                    record[0],  # ID
                    record[1],  # Categoria
                    record[2],  # Nombre de Gasto
                    record[3],  # Importe
                    record[4],  # Fecha
                    record[5],  # Descripcion
                ),
                tags=("registros_impares",),
            )
        # Aumentar el contador
        count += 1
    var_tk_gasto_total.set(total_gastos)


# Botón Eliminar Registro
def eliminar_registro_tk():
    # Obtengo desde el entorno grafico (tree) el valor seleccionado a eliminar.
    valor_seleccionado = my_tree.selection()
    valor_seleccionado_item = my_tree.item(valor_seleccionado)
    # {'text': 3, 'image': '', 'values': ['Automotor', 'Patente', '3000.0', '7/12/22', 'Fiat 1'], 'open': 0, 'tags': ''}
    db_id = valor_seleccionado_item["text"]
    # Llamo a la función de DB para eliminar el registro pasandole le id.
    eliminar_registro_db(db_id)
    # Elimino el valor desde el entorno gráfico.
    my_tree.delete(valor_seleccionado)
    gasto_total = obtener_gastos_total_db()
    var_tk_gasto_total.set(gasto_total)
    actualizar_treeview()


def eliminar_todos_registros_tk():
    # Elimino todos los registros de la base de datos.
    eliminar_todos_registros_db()
    # Elimino todos los registros del entorno gráfico.
    items = my_tree.get_children()
    for item in items:
        my_tree.delete(item)
    gasto_total = obtener_gastos_total_db()
    var_tk_gasto_total.set(gasto_total)


def eliminar_tabla_tk():
    eliminar_tabla_db()
    items = my_tree.get_children()
    for item in items:
        my_tree.delete(item)
    gasto_total = obtener_gastos_total_db()
    var_tk_gasto_total.set(gasto_total)


def label_temporal_modificacion_tk():
    # Agrega un label temporal de que se cargó el registro existosamente.
    modificar_registro_label = Label(
        root,
        text="¡Registro actualizado exitosomente!",
        width=50,
        fg="GREEN",
        font=("bold"),
    )
    modificar_registro_label.place(x=40, y=295)
    modificar_registro_label.after(1500, lambda: modificar_registro_label.destroy())


def actualizar_registro_tk():
    # Botón Modificar registro.
    # FUNCIÓN: Modifica un registro existente.
    (fecha, categoria, nombre_gasto, importe, descripcion) = chequear_variables_tk()
    id = seleccionar_registro_tk()
    modificar_registro_db(id, fecha, categoria, nombre_gasto, importe, descripcion)
    # Llamo a la función para actualizar el entorno gráfico con la nueva alta hecha.
    actualizar_treeview()
    limpiar_seleccion_tk()
    label_temporal_modificacion_tk()


def seleccionar_registro_tk():
    # Botón Seleccionar Registro.
    # FUNCIÓN: Selecciona un registro ya cargado.
    fecha_entry.delete(0, END)
    categoria_var.set(categoria_default)
    nombre_gasto_entry.delete(0, END)
    importe_entry.delete(0, END)
    descripcion_entry.delete(0, END)
    # Tomar lo seleccionado
    seleccionado = my_tree.focus()
    # Tomar los valores de lo seleccionado
    try:
        valores = my_tree.item(seleccionado, "values")
        id = valores[0]
        # Mostrar los valores en los campos de entrada
        fecha_entry.insert(0, valores[4])
        nombre_gasto_entry.insert(0, valores[2])
        importe_entry.insert(0, valores[3])
        descripcion_entry.insert(0, valores[5])
        categoria_var.set(valores[1])
        return id
    except:
        showerror("ERROR", "Por favor, seleccione un registro")


def limpiar_seleccion_tk():
    # Botón Limpiar cuadros de entrada
    # FUNCIÓN: Borra todas las opciones ingresadas de los campos entry en Registros
    fecha_entry.delete(0, END)
    nombre_gasto_entry.delete(0, END)
    importe_entry.delete(0, END)
    descripcion_entry.delete(0, END)
    categoria_var.set(categoria_default)


# Agregar Botones en un nuevo Frame llamado: botones_frame
botones_frame = LabelFrame(
    root, text="ACCIONES", font=("Helvetica", "11", "bold"), foreground="#235CE0"
)
botones_frame.pack(anchor=W, fill="x", expand="yes", padx=10)


boton_agregar_registro = Button(
    botones_frame,
    text="Agregar Registro",
    command=lambda: agregar_registro_tk(),
    height=1,
    width=18,
)
boton_agregar_registro.grid(row=0, column=0, padx=10, pady=5)

boton_eliminar_registro = Button(
    botones_frame,
    text="Eliminar Registro",
    command=eliminar_registro_tk,
    height=1,
    width=18,
)
boton_eliminar_registro.grid(row=0, column=1, padx=10, pady=5)

boton_seleccionar_registro = Button(
    botones_frame,
    text="Seleccionar Registro",
    command=seleccionar_registro_tk,
    height=1,
    width=18,
)
boton_seleccionar_registro.grid(row=1, column=0, padx=10, pady=5)

boton_actualizar_registro = Button(
    botones_frame,
    text="Actualizar Registro",
    height=1,
    width=18,
    command=actualizar_registro_tk,
)
boton_actualizar_registro.grid(row=1, column=1, padx=10, pady=5)

boton_eliminar_todos = Button(
    botones_frame,
    text="Eliminar Registros\n(Todo)",
    command=eliminar_todos_registros_tk,
    height=2,
    width=18,
)
boton_eliminar_todos.grid(row=0, column=2, padx=10, pady=5)

boton_eliminar_tabla = Button(
    botones_frame,
    text="Eliminar Tabla",
    foreground="RED",
    font=("bold"),
    command=eliminar_tabla_tk,
    height=1,
    width=18,
)
boton_eliminar_tabla.grid(row=1, column=6, padx=10, pady=5)

boton_limpiar_seleccion = Button(
    botones_frame,
    text="Limpiar Seleccion",
    command=limpiar_seleccion_tk,
    height=1,
    width=18,
)
boton_limpiar_seleccion.grid(row=1, column=2, padx=10, pady=5)

# Enlazar el Treeview con la selección de registros
# my_tree.bind("<ButtonRelease-1>", seleccionar_registro)
# Lo que hace esto es cada vez que seleccionamos un registro, lo pone directamente en los cuadros de entry. Hay que pasarle argumentos a la fucion seleccionar registro para que lo haga.

# Función que llama a consultar toda la tabla en la DB y actualiza el tree ni bien se ejecuta el programa.
actualizar_treeview_initial()


root.mainloop()
