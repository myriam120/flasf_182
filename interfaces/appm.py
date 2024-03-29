from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
#inicialización del servidor Flask
app = Flask(__name__)

#Configuracion de la conexion
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="COnsultorio"

app.secret_key='mysecretkey'
mysql= MySQL(app)

#Declaramos una ruta
#ruta Index http://localhost:5000
#ruta se compone de nombre y funcion
@app.route('/')
def index():
     return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    VRFC = request.form['txtRFC']
    VPass = request.form['txtPass']
    
    # Conectamos a la base de datos
    CS = mysql.connection.cursor()
    
    # Verificar las credenciales en la base de datos
    consulta = "SELECT RFC FROM admin WHERE RFC = %s AND contraseña = %s"
    CS.execute(consulta, (VRFC, VPass))
    resultado = CS.fetchone()
    Rol = "select Rol from admin where RFC = %s AND contraseña = %s"
    
    # Verificar si las credenciales son válidas
    if resultado is not None:
        # Las credenciales son válidas, redirigir al menú principal
        CS.execute(Rol, (VRFC, VPass))
        rol_resultado = CS.fetchone()

        if rol_resultado is not None and rol_resultado[0] == "Administrador":
            # El usuario es administrador, redirigir al menú de administrador
            return render_template('Menuadmin.html')
        else:
            # El usuario no es administrador, redirigir al menú principal
            return render_template('Menu.html')
    else:
        # Las credenciales son inválidas, redirigir a la página de inicio de sesión con un mensaje de error
        flash('RFC o contraseña incorrectos. Intente nuevamente.')
        return redirect(url_for('index'))


@app.route('/menu', methods=['GET'])
def menu():
    return render_template('Menu.html')

@app.route('/menuadmin', methods=['GET'])
def menuadmin():
    return render_template('Menuadmin.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        VRFC = request.form['txtRFC']
        VNom = request.form['txtNom']
        VAP = request.form['txtAP']
        VAM = request.form['txtAM']
        VCed = request.form['txtCed']
        VCorr = request.form['txtCorr']
        VRol = request.form['txtRol']
        VPass = request.form['txtPass']
        
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO admin (RFC, Nombre, Apellidopa, Apellidoma, Cedula, Correo, Rol, Contraseña) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (VRFC, VNom, VAP, VAM, VCed, VCorr, VRol, VPass))
        mysql.connection.commit()
        flash('Médico agregado correctamente')
        return redirect(url_for('admin'))

    return render_template('Admin.html')

@app.route('/regpaciente', methods=['GET', 'POST'])
def regpaciente():
    if request.method == 'POST':
        VMed = request.form['txtMd']  # Actualiza el nombre del atributo a txtMd
        VNom = request.form['txtNom']
        VAP = request.form['txtAP']
        VAM = request.form['txtAM']
        VNac = request.form['txtNac']
        VEnf = request.form['txtEnf']
        VAlr = request.form['txtAlg']
        VAnt = request.form['txtAnt']
        CS = mysql.connection.cursor()
        CS.execute(
            'INSERT INTO registro_paciente (Medico_id, Nombre, Apellidopa, Apellidoma, Fecha_Nacimiento, Enfermedades, Alergias, Antecedentes_familiares) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (VMed, VNom, VAP, VAM, VNac, VEnf, VAlr, VAnt))
        mysql.connection.commit()
        flash('Paciente registrado correctamente')
        return redirect(url_for('regpaciente'))

    CS = mysql.connection.cursor()
    CS.execute('SELECT ID, concat(Nombre, " ", Apellidopa, " ",Apellidoma) as Nombrec FROM admin')
    medicos = CS.fetchall()
    return render_template('RegPaciente.html', medicos=medicos)



@app.route('/ced', methods=['GET','POST'])
def ced():
    if request.method == 'POST':

        VPacID = request.form['txtID']
        VNom = request.form['txtDat']
        VPes = request.form['txtPes']
        VAP = request.form['txtAlt']
        VAM = request.form['txtTem']
        VNac = request.form['txtLPM']
        VEnf = request.form['txtOX']
        VED = request.form['txtED']
        VAlr = request.form['txtSint']
        VAnt = request.form['txtDig']
        VTrat = request.form['txtTrat']
            
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO exploracion_diagnostico (Id_paciente, Fecha, Peso, Altura, Temperatura, Latidos, Oxigeno, Edad, Sintomas, DX, Tratamiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (VPacID, VNom, VPes, VAP, VAM, VNac, VEnf, VED, VAlr, VAnt, VTrat))
        mysql.connection.commit()
        flash('Se ha registrado la consulta')
        return redirect(url_for('ced'))
    CS = mysql.connection.cursor()
    CS.execute('SELECT Id_paciente, concat(Nombre, " ", Apellidopa, " ",Apellidoma) as Nombrec FROM registro_paciente')
    pacientes = CS.fetchall()
    return render_template('Citas_Exp_Diagn.html', pacientes=pacientes)

@app.route('/citas')
def citas():
    return render_template('Citas.html')

@app.route('/cons_med')
def cons_med():
    return render_template('MEDICOS.html')

@app.route('/cons_pac')
def cons_pac():
    return render_template('PACIENTESS.html')

#Ejecucion de servidor
if __name__ =='__main__':
    app.run(port=5000,debug=True)


app = Flask(__name__)  
login_manager = LoginManager(app)
app.secret_key = “clave_secreta”

class Usuario(UserMixin):
    @login_manager.user_loader
    def load_user(usuario_id):
   #Buscar en BD y cargar atributos
     return Usuario.get(usuario_id)
 
    @login_manager.request_loader
    def load_user(request):
        if 'access_token' in request.cookies:
           #Decodificar el token
            decoded = jwt.decode(request.cookies['access_token'], current_app.config["SECRET_KEY"])
            #Cargar datos del usuario
            user = Usuario(decoded["email"],decoded["nombre"])
            #Devolver usuario 
            return user
            return None
        
usuario = Usuario(id =5, nombre ="Pedro" )
login_user(usuario)
logout_user()

	
Hola{{ current_user.nombre }}!
    {% if current_user.is_authenticated %}
        Hola{{ current_user.nombre }}!
    {% endif %}
    
{% if current_user.is_authenticated %}
                    <a href="{{ url_for('main.logout') }}">Logout</a>
{% else %}  
                   <a href="{{ url_for('main.login') }}">Login</a>
{% endif %}


@app.route('/usuario')
@login_required
def usuario():
    return render_template('usuario.html')

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Debe iniciar sesión para continuar.')
    return redirect(url_for('login'))