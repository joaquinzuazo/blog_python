import time
import requests
from flask import Flask, render_template, request, redirect, session, g, abort, Request, Blueprint

from orm import Post, User
from valid_register import valid_form
from routes_posts import routes


app = Flask(__name__)
app.secret_key = "senpai_key"

app.register_blueprint(routes)


@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        # si aca iriamos a buscar todos los datos del user, esta func tiene sentido
        g.user = session["username"]

@app.after_request
def after_request(response):
    return response


# ruta home para visualizar todos los posts y poder buscar por titulo 
@app.route('/')
def home():
    orm_posts = Post("blog.db")

    titulo_busqueda = request.args.get('search')
    if titulo_busqueda:
        posts = orm_posts.get_posts_by_title(title=titulo_busqueda)
        return render_template("home.html", posts=posts)
        
    posts = orm_posts.get_all_posts()
    return render_template("home.html", posts=posts)


# ruta estatica pag contacto
@app.route('/contacto')
def contacto():
    return render_template("contacto.html")


# ruta para login, get para obtener el form y post para procesar los datos de usuario
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        orm_user = User("blog.db")
        user_exist = orm_user.get_user_by_username(username=username)
        if user_exist and user_exist[0]['password'] == password:
            session['username'] = username
            return redirect('/perfil')

        return render_template("login.html", error="Usuario o contraseña incorrecta")


# ruta para registro, get para obtener el form y post para procesar los datos de usuario y guardarlos
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]


        orm_user = User("blog.db")

        # separando funciones para validar y poder testear individualmente partes del codigo.
        resultado, mensaje = valid_form(orm_user=orm_user, username=username, password=password)
        if not resultado:
            return render_template("register.html", error=mensaje)

        orm_user.create_user(username=username, password=password)

        return redirect('/login')


# ruta perfil, proximamente solo para usuarios con login
@app.route('/logout')
def logout():
    if not g.user:
        return render_template("login.html", error="Debe iniciar sesion")
    session.pop("username", None)
    return redirect('/')

# ruta perfil, proximamente solo para usuarios con login
@app.route('/perfil')
def perfil():
    # usando objeto session
    # username = session.get("username")
    # if not username:

    # usando objeto g, que es de contexto de request
    if not g.user:
        return redirect('/login')
    return render_template("perfil.html", username=g.user)


app.run(debug=True)