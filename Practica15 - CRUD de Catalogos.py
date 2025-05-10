#Pedro Hernández Figueroa 22270495#

import flet as ft
import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "19270904",
    "database": "TiendaANAHI"
}

def get_connection():
    return mysql.connector.connect(**db_config)

def obtener_datos(tabla):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {tabla}")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return datos

def insertar_dato(tabla, datos):
    conn = get_connection()
    cursor = conn.cursor()
    columnas = ", ".join(datos.keys())
    valores = ", ".join(["%s"] * len(datos))
    sql = f"INSERT INTO {tabla} ({columnas}) VALUES ({valores})"
    cursor.execute(sql, list(datos.values()))
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_dato(tabla, id_columna, id_valor, datos):
    conn = get_connection()
    cursor = conn.cursor()
    asignaciones = ", ".join([f"{col}=%s" for col in datos.keys()])
    sql = f"UPDATE {tabla} SET {asignaciones} WHERE {id_columna}=%s"
    valores = list(datos.values()) + [id_valor]
    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_dato(tabla, id_columna, id_valor):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {tabla} WHERE {id_columna} = %s", (id_valor,))
    conn.commit()
    cursor.close()
    conn.close()

def view_categorias(page: ft.Page, container: ft.Container):
    nombre_input = ft.TextField(label="Nombre")
    descripcion_input = ft.TextField(label="Descripción")
    id_actualizando = ft.Ref[int]()
    
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )
    
    def agregar_actualizar_categoria(e):
        nuevo_dato = {
            "nombre": nombre_input.value,
            "descripcion": descripcion_input.value
        }
        if id_actualizando.current is not None:
            actualizar_dato("Categorias", "id_categoria", id_actualizando.current, nuevo_dato)
            id_actualizando.current = None
            agregar_btn.text = "Agregar"
        else:
            insertar_dato("Categorias", nuevo_dato)
        limpiar_campos()
        actualizar_tabla()
        
    def limpiar_campos():
        nombre_input.value = ""
        descripcion_input.value = ""
        id_actualizando.current = None
        container.update()
        
    def editar_categoria(item):
        nombre_input.value = item["nombre"]
        descripcion_input.value = item["descripcion"]
        id_actualizando.current = item["id_categoria"]
        agregar_btn.text = "Actualizar"
        container.update()
        
    def actualizar_tabla():
        tabla.rows.clear()
        datos = obtener_datos("Categorias")
        for item in datos:
            row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(item.get("nombre", "Sin datos"))),
                ft.DataCell(ft.Text(item.get("descripcion", "Sin datos"))),
                ft.DataCell(
                    ft.Row(controls=[
                        ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, i=item: editar_categoria(i)),
                        ft.IconButton(icon=ft.icons.DELETE, tooltip="Eliminar", on_click=lambda e, i=item: (eliminar_dato("Categorias", "id_categoria", i["id_categoria"]), actualizar_tabla()))
                    ])
                )
            ])
            tabla.rows.append(row)
        container.update()
    
    agregar_btn = ft.ElevatedButton(text="Agregar", on_click=agregar_actualizar_categoria)
    
    container.content = ft.Column([
        ft.Text("CRUD Categorías", size=24, weight=ft.FontWeight.BOLD),
        nombre_input,
        descripcion_input,
        agregar_btn,
        tabla
    ])
    actualizar_tabla()

def view_productos(page: ft.Page, container: ft.Container):
    nombre_input = ft.TextField(label="Nombre")
    descripcion_input = ft.TextField(label="Descripción")
    precio_input = ft.TextField(label="Precio", keyboard_type=ft.KeyboardType.NUMBER)
    stock_input = ft.TextField(label="Stock", keyboard_type=ft.KeyboardType.NUMBER)
    
    categorias_opciones = obtener_datos("Categorias")
    categoria_dropdown = ft.Dropdown(
        label="Categoría",
        options=[ft.dropdown.Option(str(cat["id_categoria"]), cat["nombre"]) for cat in categorias_opciones]
    )
    id_actualizando = ft.Ref[int]()
    
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Stock")),
            ft.DataColumn(ft.Text("Categoría")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )
    
    def agregar_actualizar_producto(e):
        nuevo_dato = {
            "nombre": nombre_input.value,
            "descripcion": descripcion_input.value,
            "precio": float(precio_input.value) if precio_input.value else 0,
            "stock": int(stock_input.value) if stock_input.value else 0,
            "id_categoria": int(categoria_dropdown.value) if categoria_dropdown.value else None
        }
        if id_actualizando.current is not None:
            actualizar_dato("Productos", "id_producto", id_actualizando.current, nuevo_dato)
            id_actualizando.current = None
            agregar_btn.text = "Agregar"
        else:
            insertar_dato("Productos", nuevo_dato)
        limpiar_campos()
        actualizar_tabla()
        
    def limpiar_campos():
        nombre_input.value = ""
        descripcion_input.value = ""
        precio_input.value = ""
        stock_input.value = ""
        categoria_dropdown.value = None
        id_actualizando.current = None
        container.update()
        
    def editar_producto(item):
        nombre_input.value = item["nombre"]
        descripcion_input.value = item["descripcion"]
        precio_input.value = str(item["precio"])
        stock_input.value = str(item["stock"])
        categoria_dropdown.value = str(item["id_categoria"])
        id_actualizando.current = item["id_producto"]
        agregar_btn.text = "Actualizar"
        container.update()
        
    def actualizar_tabla():
        tabla.rows.clear()
        datos = obtener_datos("Productos")
        for item in datos:
            row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(item.get("nombre", "Sin datos"))),
                ft.DataCell(ft.Text(item.get("descripcion", "Sin datos"))),
                ft.DataCell(ft.Text(f"${item.get('precio',0)}")),
                ft.DataCell(ft.Text(str(item.get("stock",0)))),
                ft.DataCell(ft.Text(
                    next((cat["nombre"] for cat in categorias_opciones if cat["id_categoria"] == item.get("id_categoria")), "Sin categoría")
                )),
                ft.DataCell(
                    ft.Row(controls=[
                        ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, i=item: editar_producto(i)),
                        ft.IconButton(icon=ft.icons.DELETE, tooltip="Eliminar", on_click=lambda e, i=item: (eliminar_dato("Productos", "id_producto", i["id_producto"]), actualizar_tabla()))
                    ])
                )
            ])
            tabla.rows.append(row)
        container.update()
    
    agregar_btn = ft.ElevatedButton(text="Agregar", on_click=agregar_actualizar_producto)
    
    container.content = ft.Column([
        ft.Text("CRUD Productos", size=24, weight=ft.FontWeight.BOLD),
        nombre_input,
        descripcion_input,
        precio_input,
        stock_input,
        categoria_dropdown,
        agregar_btn,
        tabla
    ])
    actualizar_tabla()

def view_proveedores(page: ft.Page, container: ft.Container):
    nombre_input = ft.TextField(label="Nombre")
    contacto_input = ft.TextField(label="Contacto")
    telefono_input = ft.TextField(label="Teléfono", keyboard_type=ft.KeyboardType.PHONE)
    email_input = ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL)
    direccion_input = ft.TextField(label="Dirección")
    id_actualizando = ft.Ref[int]()
    
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Contacto")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )
    
    def agregar_actualizar_proveedor(e):
        nuevo_dato = {
            "nombre": nombre_input.value,
            "contacto": contacto_input.value,
            "telefono": telefono_input.value,
            "email": email_input.value,
            "direccion": direccion_input.value
        }
        if id_actualizando.current is not None:
            actualizar_dato("Proveedores", "id_proveedor", id_actualizando.current, nuevo_dato)
            id_actualizando.current = None
            agregar_btn.text = "Agregar"
        else:
            insertar_dato("Proveedores", nuevo_dato)
        limpiar_campos()
        actualizar_tabla()
        
    def limpiar_campos():
        nombre_input.value = ""
        contacto_input.value = ""
        telefono_input.value = ""
        email_input.value = ""
        direccion_input.value = ""
        id_actualizando.current = None
        container.update()
        
    def editar_proveedor(item):
        nombre_input.value = item["nombre"]
        contacto_input.value = item["contacto"]
        telefono_input.value = item["telefono"]
        email_input.value = item["email"]
        direccion_input.value = item["direccion"]
        id_actualizando.current = item["id_proveedor"]
        agregar_btn.text = "Actualizar"
        container.update()
        
    def actualizar_tabla():
        tabla.rows.clear()
        datos = obtener_datos("Proveedores")
        for item in datos:
            row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(item.get("nombre", "Sin datos"))),
                ft.DataCell(ft.Text(item.get("contacto", "Sin datos"))),
                ft.DataCell(ft.Text(item.get("telefono", "Sin datos"))),
                ft.DataCell(ft.Text(item.get("email", "Sin datos"))),
                ft.DataCell(ft.Text(item.get("direccion", "Sin datos"))),
                ft.DataCell(
                    ft.Row(controls=[
                        ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, i=item: editar_proveedor(i)),
                        ft.IconButton(icon=ft.icons.DELETE, tooltip="Eliminar", on_click=lambda e, i=item: (eliminar_dato("Proveedores", "id_proveedor", i["id_proveedor"]), actualizar_tabla()))
                    ])
                )
            ])
            tabla.rows.append(row)
        container.update()
    
    agregar_btn = ft.ElevatedButton(text="Agregar", on_click=agregar_actualizar_proveedor)
    
    container.content = ft.Column([
        ft.Text("CRUD Proveedores", size=24, weight=ft.FontWeight.BOLD),
        nombre_input,
        contacto_input,
        telefono_input,
        email_input,
        direccion_input,
        agregar_btn,
        tabla
    ])
    actualizar_tabla()

def view_clientes(page: ft.Page, container: ft.Container):
    nombre_input = ft.TextField(label="Nombre")
    telefono_input = ft.TextField(label="Teléfono", keyboard_type=ft.KeyboardType.PHONE)
    email_input = ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL)
    direccion_input = ft.TextField(label="Dirección")
    id_actualizando = ft.Ref[int]()
    
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )
    
    def agregar_actualizar_cliente(e):
        nuevo_dato = {
            "nombre": nombre_input.value,
            "telefono": telefono_input.value,
            "email": email_input.value,
            "direccion": direccion_input.value
        }
        if id_actualizando.current is not None:
            actualizar_dato("Clientes", "id_cliente", id_actualizando.current, nuevo_dato)
            id_actualizando.current = None
            agregar_btn.text = "Agregar"
        else:
            insertar_dato("Clientes", nuevo_dato)
        limpiar_campos()
        actualizar_tabla()
        
    def limpiar_campos():
        nombre_input.value = ""
        telefono_input.value = ""
        email_input.value = ""
        direccion_input.value = ""
        id_actualizando.current = None
        container.update()
        
    def editar_cliente(item):
        nombre_input.value = item["nombre"]
        telefono_input.value = item["telefono"]
        email_input.value = item["email"]
        direccion_input.value = item["direccion"]
        id_actualizando.current = item["id_cliente"]
        agregar_btn.text = "Actualizar"
        container.update()
        
    def actualizar_tabla():
        tabla.rows.clear()
        datos = obtener_datos("Clientes")
        for item in datos:
            row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(item.get("nombre", "Sin datos"))),
                ft.DataCell(ft.Text(item.get("telefono", "Sin datos"))),
                ft.DataCell(ft.Text(item.get("email", "Sin datos"))),
                ft.DataCell(ft.Text(item.get("direccion", "Sin datos"))),
                ft.DataCell(
                    ft.Row(controls=[
                        ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, i=item: editar_cliente(i)),
                        ft.IconButton(icon=ft.icons.DELETE, tooltip="Eliminar", on_click=lambda e, i=item: (eliminar_dato("Clientes", "id_cliente", i["id_cliente"]), actualizar_tabla()))
                    ])
                )
            ])
            tabla.rows.append(row)
        container.update()
    
    agregar_btn = ft.ElevatedButton(text="Agregar", on_click=agregar_actualizar_cliente)
    
    container.content = ft.Column([
        ft.Text("CRUD Clientes", size=24, weight=ft.FontWeight.BOLD),
        nombre_input,
        telefono_input,
        email_input,
        direccion_input,
        agregar_btn,
        tabla
    ])
    actualizar_tabla()

# --- CRUD Empleados ---
def view_empleados(page: ft.Page, container: ft.Container):
    nombre_input = ft.TextField(label="Nombre")
    cargo_input = ft.TextField(label="Cargo")
    telefono_input = ft.TextField(label="Teléfono", keyboard_type=ft.KeyboardType.PHONE)
    email_input = ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL)
    salario_input = ft.TextField(label="Salario", keyboard_type=ft.KeyboardType.NUMBER)
    fecha_input = ft.TextField(label="Fecha de Contratación", hint_text="AAAA-MM-DD")
    id_actualizando = ft.Ref[int]()
    
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Cargo")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Salario")),
            ft.DataColumn(ft.Text("Fecha de Contratación")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )
    
    def agregar_actualizar_empleado(e):
        nuevo_dato = {
            "nombre": nombre_input.value,
            "cargo": cargo_input.value,
            "telefono": telefono_input.value,
            "email": email_input.value,
            "salario": float(salario_input.value) if salario_input.value else 0,
            "fecha_contratacion": fecha_input.value
        }
        if id_actualizando.current is not None:
            actualizar_dato("Empleados", "id_empleado", id_actualizando.current, nuevo_dato)
            id_actualizando.current = None
            agregar_btn.text = "Agregar"
        else:
            insertar_dato("Empleados", nuevo_dato)
        limpiar_campos()
        actualizar_tabla()
        
    def limpiar_campos():
        nombre_input.value = ""
        cargo_input.value = ""
        telefono_input.value = ""
        email_input.value = ""
        salario_input.value = ""
        fecha_input.value = ""
        id_actualizando.current = None
        container.update()
        
    def editar_empleado(item):
        nombre_input.value = item["nombre"]
        cargo_input.value = item["cargo"]
        telefono_input.value = item["telefono"]
        email_input.value = item["email"]
        salario_input.value = str(item["salario"])
        fecha_input.value = item["fecha_contratacion"]
        id_actualizando.current = item["id_empleado"]
        agregar_btn.text = "Actualizar"
        container.update()
        
    def actualizar_tabla():
        tabla.rows.clear()
        datos = obtener_datos("Empleados")
        for item in datos:
            row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(item.get("nombre", "Sin datos"))),
                ft.DataCell(ft.Text(item.get("cargo", "Sin datos"))),
                ft.DataCell(ft.Text(item.get("telefono", "Sin datos"))),
                ft.DataCell(ft.Text(item.get("email", "Sin datos"))),
                ft.DataCell(ft.Text(f"${item.get('salario', 0)}")),
                ft.DataCell(ft.Text(item.get("fecha_contratacion", "Sin datos"))),
                ft.DataCell(
                    ft.Row(controls=[
                        ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, i=item: editar_empleado(i)),
                        ft.IconButton(icon=ft.icons.DELETE, tooltip="Eliminar", on_click=lambda e, i=item: (eliminar_dato("Empleados", "id_empleado", i["id_empleado"]), actualizar_tabla()))
                    ])
                )
            ])
            tabla.rows.append(row)
        container.update()
    
    agregar_btn = ft.ElevatedButton(text="Agregar", on_click=agregar_actualizar_empleado)
    
    container.content = ft.Column([
        ft.Text("CRUD Empleados", size=24, weight=ft.FontWeight.BOLD),
        nombre_input,
        cargo_input,
        telefono_input,
        email_input,
        salario_input,
        fecha_input,
        agregar_btn,
        tabla
    ])
    actualizar_tabla()

def view_usuarios(page: ft.Page, container: ft.Container):
    nombre_usuario_input = ft.TextField(label="Nombre de Usuario")
    contrasena_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
    empleados_opciones = obtener_datos("Empleados")
    empleado_dropdown = ft.Dropdown(
        label="Empleado Asociado",
        options=[ft.dropdown.Option(str(emp["id_empleado"]), emp["nombre"]) for emp in empleados_opciones]
    )
    rol_dropdown = ft.Dropdown(
        label="Rol",
        options=[
            ft.dropdown.Option("Administrador"),
            ft.dropdown.Option("Cajero"),
            ft.dropdown.Option("Almacén")
        ]
    )
    id_actualizando = ft.Ref[int]()
    
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre de Usuario")),
            ft.DataColumn(ft.Text("Empleado Asociado")),
            ft.DataColumn(ft.Text("Rol")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )
    
    def agregar_actualizar_usuario(e):
        nuevo_dato = {
            "nombre_usuario": nombre_usuario_input.value,
            "contrasena": contrasena_input.value,
            "id_empleado": int(empleado_dropdown.value) if empleado_dropdown.value else None,
            "rol": rol_dropdown.value
        }
        if id_actualizando.current is not None:
            actualizar_dato("Usuarios", "id_usuario", id_actualizando.current, nuevo_dato)
            id_actualizando.current = None
            agregar_btn.text = "Agregar"
        else:
            insertar_dato("Usuarios", nuevo_dato)
        limpiar_campos()
        actualizar_tabla()
        
    def limpiar_campos():
        nombre_usuario_input.value = ""
        contrasena_input.value = ""
        empleado_dropdown.value = None
        rol_dropdown.value = None
        id_actualizando.current = None
        container.update()
        
    def editar_usuario(item):
        nombre_usuario_input.value = item["nombre_usuario"]
        contrasena_input.value = item["contrasena"]
        empleado_dropdown.value = str(item["id_empleado"])
        rol_dropdown.value = item["rol"]
        id_actualizando.current = item["id_usuario"]
        agregar_btn.text = "Actualizar"
        container.update()
        
    def actualizar_tabla():
        tabla.rows.clear()
        datos = obtener_datos("Usuarios")
        for item in datos:
            row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(item.get("nombre_usuario", "Sin datos"))),
                ft.DataCell(ft.Text(
                    next((emp["nombre"] for emp in empleados_opciones if emp["id_empleado"] == item.get("id_empleado")), "Sin empleado asociado")
                )),
                ft.DataCell(ft.Text(item.get("rol", "Sin rol"))),
                ft.DataCell(
                    ft.Row(controls=[
                        ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, i=item: editar_usuario(i)),
                        ft.IconButton(icon=ft.icons.DELETE, tooltip="Eliminar", on_click=lambda e, i=item: (eliminar_dato("Usuarios", "id_usuario", i["id_usuario"]), actualizar_tabla()))
                    ])
                )
            ])
            tabla.rows.append(row)
        container.update()
    
    agregar_btn = ft.ElevatedButton(text="Agregar", on_click=agregar_actualizar_usuario)
    
    container.content = ft.Column([
        ft.Text("CRUD Usuarios", size=24, weight=ft.FontWeight.BOLD),
        nombre_usuario_input,
        contrasena_input,
        empleado_dropdown,
        rol_dropdown,
        agregar_btn,
        tabla
    ])
    actualizar_tabla()

def view_ventas(page: ft.Page, container: ft.Container):

    cliente_opciones = obtener_datos("Clientes")
    empleado_opciones = obtener_datos("Empleados")
    cliente_dropdown = ft.Dropdown(
        label="Cliente",
        options=[ft.dropdown.Option(str(cli["id_cliente"]), cli["nombre"]) for cli in cliente_opciones]
    )
    empleado_dropdown = ft.Dropdown(
        label="Empleado",
        options=[ft.dropdown.Option(str(emp["id_empleado"]), emp["nombre"]) for emp in empleado_opciones]
    )
    total_input = ft.TextField(label="Total", keyboard_type=ft.KeyboardType.NUMBER)
    id_actualizando = ft.Ref[int]()

    producto_opciones = obtener_datos("Productos")
    producto_dropdown = ft.Dropdown(
        label="Producto",
        options=[ft.dropdown.Option(str(prod["id_producto"]), prod["nombre"]) for prod in producto_opciones]
    )
    cantidad_input = ft.TextField(label="Cantidad", keyboard_type=ft.KeyboardType.NUMBER)
    precio_unitario_input = ft.TextField(label="Precio Unitario", keyboard_type=ft.KeyboardType.NUMBER)
    subtotal_input = ft.TextField(label="Subtotal", keyboard_type=ft.KeyboardType.NUMBER)
    
    tabla_ventas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Empleado")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )
    tabla_detalles = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Precio Unitario")),
            ft.DataColumn(ft.Text("Subtotal")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )
    
    def agregar_actualizar_venta(e):
        nuevo_dato = {
            "id_cliente": int(cliente_dropdown.value) if cliente_dropdown.value else None,
            "id_empleado": int(empleado_dropdown.value) if empleado_dropdown.value else None,
            "total": float(total_input.value) if total_input.value else 0
        }
        if id_actualizando.current is not None:
            actualizar_dato("Ventas", "id_venta", id_actualizando.current, nuevo_dato)
            id_actualizando.current = None
            agregar_btn.text = "Agregar Venta"
        else:
            insertar_dato("Ventas", nuevo_dato)
        limpiar_campos_venta()
        actualizar_tabla_ventas()
        
    def agregar_detalle(e):
        nuevo_detalle = {
            "id_venta": id_actualizando.current,
            "id_producto": int(producto_dropdown.value) if producto_dropdown.value else None,
            "cantidad": int(cantidad_input.value) if cantidad_input.value else 0,
            "precio_unitario": float(precio_unitario_input.value) if precio_unitario_input.value else 0,
            "subtotal": float(subtotal_input.value) if subtotal_input.value else 0
        }
        insertar_dato("Detalles_Venta", nuevo_detalle)
        actualizar_tabla_detalles()
        
    def limpiar_campos_venta():
        cliente_dropdown.value = None
        empleado_dropdown.value = None
        total_input.value = ""
        id_actualizando.current = None
        container.update()
        
    def limpiar_campos_detalles():
        producto_dropdown.value = None
        cantidad_input.value = ""
        precio_unitario_input.value = ""
        subtotal_input.value = ""
        container.update()
        
    def editar_venta(item):
        cliente_dropdown.value = str(item["id_cliente"])
        empleado_dropdown.value = str(item["id_empleado"])
        total_input.value = str(item["total"])
        id_actualizando.current = item["id_venta"]
        agregar_btn.text = "Actualizar Venta"
        actualizar_tabla_detalles()  
        container.update()
        
    def actualizar_tabla_ventas():
        tabla_ventas.rows.clear()
        datos = obtener_datos("Ventas")
        for item in datos:
            row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(
                    next((cli["nombre"] for cli in cliente_opciones if cli["id_cliente"] == item.get("id_cliente")), "Sin Cliente")
                )),
                ft.DataCell(ft.Text(
                    next((emp["nombre"] for emp in empleado_opciones if emp["id_empleado"] == item.get("id_empleado")), "Sin Empleado")
                )),
                ft.DataCell(ft.Text(f"${item.get('total', 0)}")),
                ft.DataCell(
                    ft.Row(controls=[
                        ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar Venta", on_click=lambda e, i=item: editar_venta(i)),
                        ft.IconButton(icon=ft.icons.DELETE, tooltip="Eliminar Venta", on_click=lambda e, i=item: (eliminar_dato("Ventas", "id_venta", i["id_venta"]), actualizar_tabla_ventas()))
                    ])
                )
            ])
            tabla_ventas.rows.append(row)
        container.update()
        
    def actualizar_tabla_detalles():
        if id_actualizando.current is None:
            return
        tabla_detalles.rows.clear()
        datos_detalles = obtener_datos("Detalles_Venta")
        for detalle in datos_detalles:
            if detalle.get("id_venta") == id_actualizando.current:
                row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(
                        next((prod["nombre"] for prod in producto_opciones if prod["id_producto"] == detalle.get("id_producto")), "Sin Producto")
                    )),
                    ft.DataCell(ft.Text(str(detalle.get("cantidad", 0)))),
                    ft.DataCell(ft.Text(f"${detalle.get('precio_unitario', 0)}")),
                    ft.DataCell(ft.Text(f"${detalle.get('subtotal', 0)}")),
                    ft.DataCell(
                        ft.IconButton(icon=ft.icons.DELETE, tooltip="Eliminar Detalle", on_click=lambda e, i=detalle: (eliminar_dato("Detalles_Venta", "id_detalle", i["id_detalle"]), actualizar_tabla_detalles()))
                    )
                ])
                tabla_detalles.rows.append(row)
        container.update()
    
    agregar_btn = ft.ElevatedButton(text="Agregar Venta", on_click=agregar_actualizar_venta)
    content = ft.Column([
        ft.Text("CRUD Ventas", size=24, weight=ft.FontWeight.BOLD),
        cliente_dropdown,
        empleado_dropdown,
        total_input,
        agregar_btn,
        tabla_ventas,
        ft.Text("Detalles de Venta", size=24, weight=ft.FontWeight.BOLD),
        producto_dropdown,
        cantidad_input,
        precio_unitario_input,
        subtotal_input,
        ft.ElevatedButton(text="Agregar Detalle", on_click=agregar_detalle),
        tabla_detalles
    ])
    container.content = content
    actualizar_tabla_ventas()

def main(page: ft.Page):
    page.title = "Tienda ANAHÍ - CRUD"
    page.horizontal_alignment = "stretch"

    content_container = ft.Container(expand=True)

    def switch_view(view_name: str):
        if view_name == "categorias":
            view_categorias(page, content_container)
        elif view_name == "productos":
            view_productos(page, content_container)
        elif view_name == "proveedores":
            view_proveedores(page, content_container)
        elif view_name == "clientes":
            view_clientes(page, content_container)
        elif view_name == "empleados":
            view_empleados(page, content_container)
        elif view_name == "usuarios":
            view_usuarios(page, content_container)
        elif view_name == "ventas":
            view_ventas(page, content_container)
        page.update()

    vistas = ["categorias", "productos", "proveedores", "clientes", "empleados", "usuarios", "ventas"]
    
    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.CATEGORY, label="Categorías"),
            ft.NavigationRailDestination(icon=ft.icons.SHOP, label="Productos"),
            ft.NavigationRailDestination(icon=ft.icons.SUPERVISOR_ACCOUNT, label="Proveedores"),
            ft.NavigationRailDestination(icon=ft.icons.PEOPLE, label="Clientes"),
            ft.NavigationRailDestination(icon=ft.icons.PERSON, label="Empleados"),
            ft.NavigationRailDestination(icon=ft.icons.ACCOUNT_CIRCLE, label="Usuarios"),
            ft.NavigationRailDestination(icon=ft.icons.RECEIPT, label="Ventas")
        ],
        on_change=lambda e: switch_view(vistas[e.control.selected_index])
    )

    layout = ft.Row(
        controls=[
            nav_rail,
            content_container
        ],
        expand=True
    )
    
    page.add(layout)

    switch_view("categorias")

ft.app(target=main)