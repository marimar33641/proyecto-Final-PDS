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
        args = {
            'id': id_producto,
            'producto': producto,
            'maquina': maquina,
            'fecha': fecha,
            'hora': hora,
            'estado': estado,
        }
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




@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/pedidos')

def pedidos():
    return render_template('pedidos.html')

@app.route('/videos')

def videos():
    return render_template('videos.html')


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()