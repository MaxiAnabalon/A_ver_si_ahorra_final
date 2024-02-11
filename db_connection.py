import sqlite3


def connectar_base_db():
    connection_db = sqlite3.connect("a_ver_si_ahorra.db")
    return connection_db


def chequear_existencia_tabla_db():
    connection_db = connectar_base_db()
    cursor = connection_db.cursor()
    sql = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='gastos';"
    tabla_gastos = cursor.execute(sql).fetchall()
    # Si no existe crea la base.
    if tabla_gastos[0][0] != 1:
        crear_tabla_db()
    else:
        return connection_db


def crear_tabla_db():
    # Crea la tabla "gastos" si no existe.
    connection_db = connectar_base_db()
    cursor = connection_db.cursor()
    sql = "CREATE TABLE IF NOT EXISTS gastos(id integer NOT NULL PRIMARY KEY AUTOINCREMENT, categoria text, nombre_gasto text, importe real, fecha text, descripcion text)"
    cursor.execute(sql)
    connection_db.commit()
    connection_db.close()
    print("La tabla ha sido creada")


def eliminar_tabla_db():
    connection_db = connectar_base_db()
    cursor = connection_db.cursor()
    sql = "DROP TABLE gastos"
    cursor.execute(sql)
    connection_db.commit()
    connection_db.close()
    print("La tabla GASTOS ha sido eliminada")


def consultar_tabla_db():
    # Esta función trae todos los valores cargados en la base de datos ordenados descendentemente
    # Chequea primero si existe la tabla gastos. Si no, la crea.
    chequear_existencia_tabla_db()
    connection_db = connectar_base_db()
    cursor = connection_db.cursor()
    sql = "SELECT * from gastos ORDER BY id ASC"
    cursor.execute(sql)
    resultado_consulta = cursor.fetchall()
    connection_db.close()
    return resultado_consulta


def insertar_registro_db(*args):
    # Esta función inserta los registros indicados en el entorno gráfico.
    # Chequea primero si existe la tabla gastos. Si no, la crea.
    chequear_existencia_tabla_db()
    connection_db = connectar_base_db()
    cursor = connection_db.cursor()
    sql = "INSERT INTO gastos (fecha, categoria, nombre_gasto, importe, descripcion) VALUES (?, ?, ?, ?, ? );"
    cursor.execute(sql, args)
    connection_db.commit()
    connection_db.close()


def eliminar_registro_db(*args):
    # Esta función elimina los registros de la base, seleccionados en el entorno gráfico
    chequear_existencia_tabla_db()
    connection_db = connectar_base_db()
    cursor = connection_db.cursor()
    db_id = args
    sql = "DELETE from gastos where id = ?;"
    cursor.execute(sql, db_id)
    connection_db.commit()
    connection_db.close()


def modificar_registro_db(id, fecha, categoria, nombre_gasto, importe, descripcion):
    chequear_existencia_tabla_db()
    connection_db = connectar_base_db()
    cursor = connection_db.cursor()
    data = (fecha, categoria, nombre_gasto, importe, descripcion, id)
    sql = "UPDATE gastos SET fecha = ?, categoria = ?, nombre_gasto = ?, importe = ?, descripcion = ? WHERE id = ?;"
    cursor.execute(sql, data)
    connection_db.commit()
    connection_db.close()


def eliminar_todos_registros_db():
    # Esta función elimina todos los registros de la base, seleccionados en el entorno gráfico
    chequear_existencia_tabla_db()
    connection_db = connectar_base_db()
    cursor = connection_db.cursor()
    sql = "DELETE from gastos;"
    cursor.execute(sql)
    connection_db.commit()
    connection_db.close()


def filtrar_registros_db(fecha_desde, fecha_hasta, categoria):
    chequear_existencia_tabla_db()
    connection_db = connectar_base_db()
    cursor = connection_db.cursor()
    if fecha_desde == "" and fecha_hasta == "" and categoria != "":
        data = (categoria,)
        sql = "SELECT * from gastos WHERE categoria = ?;"
        cursor.execute(sql, data)
        resultado_consulta = cursor.fetchall()
        sql_total = "SELECT SUM(importe) FROM gastos WHERE categoria = ?;"
        cursor.execute(sql_total, data)
        total_gastos = cursor.fetchall()
        total_gastos = total_gastos[0][0]
        connection_db.close()
        return resultado_consulta, total_gastos
    elif fecha_desde != "" and fecha_hasta != "" and categoria == "":
        data = (fecha_desde, fecha_hasta)
        sql = "SELECT * from gastos WHERE fecha BETWEEN ? and ? ORDER BY fecha ASC;"
        cursor.execute(sql, data)
        resultado_consulta = cursor.fetchall()
        sql_total = "SELECT SUM(importe) FROM gastos WHERE fecha BETWEEN ? and ?;"
        cursor.execute(sql_total, data)
        total_gastos = cursor.fetchall()
        total_gastos = total_gastos[0][0]
        connection_db.close()
        return resultado_consulta, total_gastos
    else:
        data = (fecha_desde, fecha_hasta, categoria)
        sql = "SELECT * from gastos WHERE fecha BETWEEN ? and ? and categoria = ? ORDER BY fecha ASC;"
        cursor.execute(sql, data)
        resultado_consulta = cursor.fetchall()
        sql_total = "SELECT SUM(importe) FROM gastos WHERE fecha BETWEEN ? and ? and categoria = ?;"
        cursor.execute(sql_total, data)
        total_gastos = cursor.fetchall()
        total_gastos = total_gastos[0][0]
        connection_db.close()
        return resultado_consulta, total_gastos


def obtener_gastos_total_db():
    chequear_existencia_tabla_db()
    connection_db = connectar_base_db()
    cursor = connection_db.cursor()
    sql = "SELECT SUM(importe) FROM gastos;"
    cursor.execute(sql)
    total_gastos = cursor.fetchall()
    connection_db.close()
    total_gastos = total_gastos[0][0]
    if total_gastos == None:
        total_gastos = 0
    return total_gastos
