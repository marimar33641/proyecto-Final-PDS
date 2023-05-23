from flask import Flask, render_template, request, url_for, redirect, flash
from config import config
from flask_mysqldb import MySQL
from models.ModelUser import ModelUser
from models.entities.User import User

app = Flask(__name__)
db = MySQL(app)
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        #print(request.form['username'])
        #print(request.form['password'])
        user = User(0,request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('home'))
            else:
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/reservas', methods =['GET', 'POST'])

def reserva():
    if request.method == 'POST':
        id_producto = request.form['id']
        producto = request.form['producto']
        maquina = request.form['maquina']
        fecha = request.form['fecha']
        hora = request.form['hora']
        estado = request.form['estado']
        # Crea un cursor para ejecutar consultas SQL
        cur = db.connection.cursor()
        # Define la consulta SQL para insertar los datos en la base de datos
        query = "INSERT INTO ventas (id_producto, producto, maquina, fecha, hora, estado) VALUES (%s, %s, %s, %s, %s, %s)"
        # Ejecuta la consulta SQL con los valores de los inputs del formulario
        cur.execute(query, (id_producto, producto, maquina, fecha, hora, estado))
        # Guarda los cambios en la base de datos
        db.connection.commit()
        # Cierra el cursor
        cur.close()
        return render_template('reservas.html')
    return render_template('reservas.html')


@app.route('/pedidos')

def pedidos():
    # Crea un cursor para ejecutar consultas SQL
    cur = db.connection.cursor()
    # Define la consulta SQL para obtener los datos de la tabla 'ventas'
    query = "SELECT id_producto, producto, maquina, fecha, hora, estado FROM ventas"
    # Ejecuta la consulta SQL
    cur.execute(query)
    # Obtiene todos los resultados de la consulta
    data = cur.fetchall()
    # Cierra el cursor
    cur.close()
    return render_template('pedidos.html', data=data)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/editar/<id_producto>')
def editar_pedido(id_producto):
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM ventas WHERE id_producto = %s', (id_producto,))
    data = cur.fetchall()
    print(data[0])
    return render_template('editar_pedido.html', id_producto=id_producto, data=data)

@app.route('/cargar/<id_producto>', methods = ['POST'])
def cargar(id_producto):
    if request.method == 'POST':
        producto = request.form['producto']
        maquina = request.form['maquina']
        fecha = request.form['fecha']
        hora = request.form['hora']
        estado = request.form['estado']
        cur = db.connection.cursor()
        cur.execute("""
            UPDATE ventas
            SET producto = %s,
                maquina = %s,
                fecha = %s,
                hora = %s,
                estado = %s
            WHERE id_producto = %s
        """, (producto, maquina, fecha, hora, estado, id_producto))
        db.connection.commit()
        flash("Pedido actualizado")
        return redirect(url_for('pedidos'))


@app.route('/borrar/<string:id_producto>')
def borrarPedido(id_producto):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM ventas Where id_producto ={0}'.format(id_producto))
    db.connection.commit()
    flash('Pedido removido')
    return redirect(url_for('pedidos'))


@app.route('/videos')

def videos():
    return render_template('videos.html')

@app.route('/localizacion')

def localizacion():
    return render_template('localizacion.html')



if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()