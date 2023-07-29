from flask import Flask, current_app, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_mysqldb import MySQL

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