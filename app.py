from flask import Flask, request, redirect, flash, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = '123456'

# Configuración de la conexión a la base de datos MySQL
app.config['MYSQL_HOST'] = 'b3ye8bah7wwmpabuubvk-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'utwbhg2vtxhz5q4h'
app.config['MYSQL_PASSWORD'] = 'ivBWZBIuv6BwQfZoLBf4'
app.config['MYSQL_DB'] = 'b3ye8bah7wwmpabuubvk'

# Inicialización de la extensión MySQL
mysql = MySQL(app)
cors = CORS(app)

# Rutas
@app.route('/')
def hello():
    return jsonify({'message': 'Your Backend is working!'})

# Esta función maneja las solicitudes GET a la raíz de la aplicación.
# Retorna todos los productos en formato JSON.
@app.route('/products')
def index():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM Productos")
    if result_value > 0:
        products = cur.fetchall()
        return jsonify(products)
    return jsonify([])

# Esta función maneja las solicitudes GET a '/consul_usuario'.
# Retorna todos los proveedores en formato JSON.
@app.route('/consult_supplier')
def index_usuario():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM Proveedores")
    if result_value > 0:
        products = cur.fetchall()
        return jsonify(products)
    return jsonify([])

# Esta función maneja las solicitudes POST para agregar un nuevo producto.
# Recibe los detalles del producto en formato JSON y los inserta en la base de datos.
@app.route('/add_product', methods=['POST'])
def add_product():
    products_details = request.json
    nombre = products_details['nombre']
    descripcion = products_details['descripcion']
    precio = products_details['precio']
    stock = products_details['stock']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Productos(nombre, descripcion, precio, stock) VALUES(%s, %s, %s, %s)", (nombre, descripcion, precio, stock))
    mysql.connection.commit()
    cur.close()
    flash('Producto Agregado Satisfactoriamente')
    return jsonify({'message': 'Producto Agregado Satisfactoriamente'})

# Esta función maneja las solicitudes POST para agregar un nuevo proveedor.
# Recibe los detalles del proveedor en formato JSON y los inserta en la base de datos.
@app.route('/add_supplier', methods=['POST'])
def add_user():
    products_details = request.json
    nomb = products_details['nombre']
    contacto = products_details['contacto']
    telefono = products_details['telefono']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Proveedores(nombre, contacto, telefono) VALUES(%s, %s, %s)", (nomb, contacto, telefono))
    mysql.connection.commit()
    cur.close()
    flash('Proveedor Agregado Satisfactoriamente')
    return jsonify({'message': 'Proveedor Agregado Satisfactoriamente'})

# Esta función maneja las solicitudes GET y POST para editar un producto específico.
# Retorna los detalles del producto en formato JSON y actualiza los datos en la base de datos.
@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Productos WHERE id = %s", [id])
    product = cur.fetchone()
    if request.method == 'POST':
        products_details = request.json
        nombre = products_details['nombre']
        descripcion = products_details['descripcion']
        precio = products_details['precio']
        stock = products_details['stock']
        cur.execute("UPDATE Productos SET nombre = %s, descripcion = %s, precio = %s, stock= %s WHERE id = %s", (nombre, descripcion, precio, stock, id))
        mysql.connection.commit()
        cur.close()
        flash('Producto actualizado satisfactoriamente')
        return jsonify({'message': 'Producto actualizado satisfactoriamente'})
    return jsonify(product)

# Esta función maneja las solicitudes GET y POST para editar un proveedor específico.
# Retorna los detalles del proveedor en formato JSON y actualiza los datos en la base de datos.
@app.route('/edit_supplier/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Proveedores WHERE id = %s", [id])
    product = cur.fetchone()
    if request.method == 'POST':
        products_details = request.json
        nomb = products_details['nombre']
        contacto = products_details['contacto']
        telefono = products_details['telefono']
        
        cur.execute("UPDATE Proveedores SET nombre = %s, contacto = %s, telefono= %s WHERE id = %s", (nomb, contacto, telefono, id))
        mysql.connection.commit()
        cur.close()
        flash('Proveedor actualizado satisfactoriamente')
        return jsonify({'message': 'Proveedor actualizado satisfactoriamente'})
    return jsonify(product)

# Esta función maneja las solicitudes POST para eliminar un producto específico.
# Elimina el producto correspondiente de la base de datos.
@app.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Productos WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Producto eliminado satisfactoriamente')
    return jsonify({'message': 'Producto eliminado satisfactoriamente'})

# Esta función maneja las solicitudes POST para eliminar un proveedor específico.
# Elimina el proveedor correspondiente de la base de datos.
@app.route('/delete_supplier/<int:id>', methods=['POST'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Proveedores WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Proveedor eliminado satisfactoriamente')
    return jsonify({'message': 'Proveedor eliminado satisfactoriamente'})

# Esta función maneja las solicitudes GET a '/compras'.
# Retorna todos los detalles de las compras en formato JSON.
@app.route('/compras')
def compras():
    cur = mysql.connection.cursor()
    cur.execute("SELECT c.id, p.nombre as nombre_producto, u.nombre as proveedor_nombre, c.fecha, c.cantidad "
                "FROM Compras c "
                "JOIN Productos p ON c.id_producto = p.id "
                "JOIN Proveedores u ON c.id_proveedor = u.id")
    compras1 = cur.fetchall()

    cur.execute("SELECT id, nombre FROM Productos")
    producto1 = cur.fetchall()

    cur.execute("SELECT id, nombre as nomb FROM Proveedores")
    usuarios1 = cur.fetchall()

    cur.close()
    return jsonify({'compras': compras1, 'productos': producto1, 'usuarios': usuarios1})

# Esta función maneja las solicitudes POST para agregar una nueva compra.
# Recibe los detalles de la compra en formato JSON y los inserta en la base de datos.
@app.route('/compras_agregar', methods=['POST'])
def agregar_compras():
    compra_details = request.json
    id_producto = compra_details['id_producto']
    id_proveedor = compra_details['id_proveedor']
    fecha = compra_details['fecha']
    cantidad = compra_details['cantidad']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Compras (id_producto, id_proveedor, fecha, cantidad) VALUES (%s, %s, %s, %s)",
                (id_producto, id_proveedor, fecha, cantidad))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Compra agregada satisfactoriamente'})

# Esta función maneja las solicitudes GET y POST para editar una compra específica.
# Retorna los detalles de la compra en formato JSON y actualiza los datos en la base de datos.
@app.route('/edit_compra/<int:id>', methods=['GET', 'POST'])
def edit_compra(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Compras WHERE id = %s", [id])
    compra = cur.fetchone()

    cur.execute("SELECT id, nombre FROM Productos")
    product1 = cur.fetchall()

    cur.execute("SELECT id, nombre as nomb FROM Proveedores")
    usuarios1 = cur.fetchall()

    if request.method == 'POST':
        compra_details = request.json
        id_producto = compra_details['id_producto']
        id_proveedor = compra_details['id_proveedor']
        fecha = compra_details['fecha']
        cantidad = compra_details['cantidad']
        
        cur.execute("UPDATE Compras SET id_producto = %s, id_proveedor = %s, fecha = %s, cantidad = %s WHERE id = %s", 
                    (id_producto, id_proveedor, fecha, cantidad, id))
        
        mysql.connection.commit()

        cur.close()
        flash('Compra actualizada satisfactoriamente')
        return jsonify({'message': 'Compra actualizada satisfactoriamente'})
    return jsonify({'compra': compra, 'productos': product1, 'usuarios': usuarios1})

# Esta función maneja las solicitudes POST para eliminar una compra específica.
# Elimina la compra correspondiente de la base de datos.
@app.route('/delete_compra/<int:id>', methods=['POST'])
def delete_compra(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Compras WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Compra eliminada satisfactoriamente')
    return jsonify({'message': 'Compra eliminada satisfactoriamente'})

if __name__ == '__main__':
    app.run(debug=True)