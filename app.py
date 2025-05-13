from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

#creacion de base de datos y tabla 
def init_database():
    #se crea la base de datos en caso de que no exista 
    conn = sqlite3.connect("kardex.db")
    
    #nos sirve para hacer creacion de sentencias sql
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS personas(
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL, 
            fecha_nac TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
init_database()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/personas")
def personas():
    conn = sqlite3.connect("kardex.db")
    #permite manejar los registros como diccionarios
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM personas")
    personas = cursor.fetchall()
    return render_template("personas/index.html", personas = personas)

@app.route("/personas/create")
def create():
    return render_template('personas/create.html')

@app.route("/personas/create/save", methods = ['POST'])
def personas_save():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    fecha_nac = request.form['fecha_nac']
    
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO personas (nombre,telefono,fecha_nac) VALUES (?,?,?)",
    (nombre, telefono, fecha_nac))
    conn.commit()
    conn.close()
    return redirect('/personas')
   
#crear un repositorio "kardex2.0" 
#git init 
#git add.
#git commit -m"Primercommit"
#pegar git hub
#git remote -v
#git status 
#git push origin master 

#editar 
@app.route("/personas/edit/<int:id>")
def persona_edit(id):
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas WHERE id =?", (id,))
    persona = cursor.fetchone()
    conn.close()
    return render_template("personas/edit.html", persona=persona)

    
@app.route("/personas/update", methods=['POST'])
def personas_update():
    id = request.form['id']
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    fecha_nac = request.form['fecha_nac']
    
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE personas SET nombre =?, telefono=?, fecha_nac=? WHERE id =?", (nombre, telefono, fecha_nac,id))
    conn.commit()
    conn.close()
    return redirect("/personas")

#eleiminar registro
@app.route("/personas/delete/<int:id>")
def personas_delete(id):
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personas WHERE id =?", (id,))
    conn.commit()
    conn.close()
    return redirect('/personas')

if __name__=="__main__":
    app.run(debug=True)