from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Configura la conexión a SQL Server usando pyodbc
def conectar_sql_server():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=ALEXIS;'
            'DATABASE=TEST;'  # Reemplaza con el nombre de tu base de datos
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        return str(e)

# Ruta para obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    conn = conectar_sql_server()
    if isinstance(conn, str):
        return jsonify({'error': conn})
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, email FROM Usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    lista_usuarios = [{'id': row[0], 'nombre': row[1], 'email': row[2]} for row in usuarios]
    return jsonify(lista_usuarios)

# Ruta para obtener un usuario por ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    conn = conectar_sql_server()
    if isinstance(conn, str):
        return jsonify({'error': conn})
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, email FROM Usuarios WHERE id = ?', id)
    usuario = cursor.fetchone()
    conn.close()
    if usuario:
        return jsonify({'id': usuario[0], 'nombre': usuario[1], 'email': usuario[2]})
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

# Ruta para crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    nuevo_usuario = request.get_json()
    nombre = nuevo_usuario.get('nombre')
    email = nuevo_usuario.get('email')
    conn = conectar_sql_server()
    if isinstance(conn, str):
        return jsonify({'error': conn})
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Usuarios (nombre, email) VALUES (?, ?)', (nombre, email))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Usuario creado exitosamente'}), 201

# Ruta para actualizar un usuario existente
@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario_actualizado = request.get_json()
    nombre = usuario_actualizado.get('nombre')
    email = usuario_actualizado.get('email')
    conn = conectar_sql_server()
    if isinstance(conn, str):
        return jsonify({'error': conn})
    cursor = conn.cursor()
    cursor.execute('UPDATE Usuarios SET nombre = ?, email = ? WHERE id = ?', (nombre, email, id))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Usuario actualizado exitosamente'})

# Ruta para eliminar un usuario
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    conn = conectar_sql_server()
    if isinstance(conn, str):
        return jsonify({'error': conn})
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Usuarios WHERE id = ?', id)
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Usuario eliminado exitosamente'})

if __name__ == '__main__':
    app.run(debug=True)
