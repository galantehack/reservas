import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Crear la base de datos y la tabla de reservas si no existen
def crear_tabla():
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        celular TEXT,
                        fecha TEXT,
                        hora TEXT,
                        servicio TEXT, 
                        empleado TEXT,
                        comentarios TEXT,
                        estado TEXT DEFAULT 'Activo')''')
    conn.commit()
    conn.close()

# Llamamos a la función para crear la tabla en la base de datos al iniciar la aplicación
crear_tabla()

# Ruta principal (Inicio)
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/vista")
def vista():
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM reservas''' )
    lista = cursor.fetchall()               
    
    conn.close()
    
    return render_template("vista.html", lista=lista)

# Ruta para enviar una nueva reserva
@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    # Obtener los datos del formulario
    nombre = request.form['nombre']
    celular = request.form['celular']
    fecha = request.form['fecha']
    hora = request.form['hora']
    servicio = request.form['servicio']
    empleado = request.form['empleado']
    comentarios = request.form['comentarios']
    
    # Insertar los datos de la reserva en la base de datos
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO reservas (nombre, celular, fecha, hora, servicio, empleado, comentarios) 
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (nombre, celular, fecha, hora, servicio, empleado, comentarios))
    conn.commit()
    conn.close()

    # Redirigir a la página de inicio
    return redirect(url_for('inicio'))

# Ruta para marcar una reserva como completada
@app.route('/completar_reserva/<int:reserva_id>', methods=['POST'])
def completar_reserva(reserva_id):
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE reservas SET estado = 'Completada' WHERE id = ?''', (reserva_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('vista'))

# Ruta para cancelar una reserva
@app.route('/cancelar_reserva/<int:reserva_id>', methods=['POST'])
def cancelar_reserva(reserva_id):
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE reservas SET estado = 'Cancelada' WHERE id = ?''', (reserva_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('vista'))

if __name__ == "__main__":
    app.run(debug=True)
