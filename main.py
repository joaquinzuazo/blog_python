import sqlite3
from flask import Flask, render_template, request, redirect, url_for

from orm import Post, User

app = Flask(__name__)

# def get_db_connection():
#     conn = sqlite3.connect('blog.db')
#     # cursor = conn.cursor()
#     conn.row_factory = sqlite3.Row
#     return conn

# Falsa db de posts
# posts = [
#     {"id": 1, "autor":"Joaquin", "titulo":"Python", "texto": "blabblablala"},
#     {"id": 2, "autor":"Ines", "titulo":"Java", "texto": "bsjadbajkdbdbd"},
#     {"id": 3, "autor":"Nico", "titulo":"JS", "texto": "bsjadbajkdbdbd"},
#     {"id": 4, "autor":"Andres", "titulo":"Go", "texto": "bsjadbajkdbdbd"},
#     {"id": 5, "autor":"Maria", "titulo":"TS", "texto": "bsjadbajkdbdbd"},
#     {"id": 6, "autor":"Juan", "titulo":"Java", "texto": "bsjadbajkdbdbd"}
# ]

# falsa db de users
# users = [
#     {"id": 1, "username": "jzuazo", "password":"123456"},
#     {"id": 2, "username": "iness", "password":"123456"},
# ]


# ruta home para visualizar todos los posts y poder buscar por titulo 
@app.route('/')
def home():
    # funciona con la db en variable
    # busqueda = request.args.get('search')
    # if busqueda:
    #     list_post = []
    #     for post in posts:
    #         if busqueda.lower() in post['titulo'].lower():
    #             list_post.append(post)
    #     return render_template("home.html", posts=list_post)
    # else:
    #     return render_template("home.html", posts=posts)
    
    # funciona con db sqlite:
    # conn = get_db_connection()

    # con ORM propio:
    orm_posts = Post("blog.db")

    titulo_busqueda = request.args.get('search')
    if titulo_busqueda:
        # posts = conn.execute("SELECT * FROM posts WHERE posts.titulo LIKE ?", (f"%{busqueda}%",)).fetchall() 
        # conn.close()
        posts = orm_posts.get_posts_by_title(title=titulo_busqueda)
        return render_template("home.html", posts=posts)
        
    # posts = conn.execute("SELECT * FROM posts").fetchall()
    # conn.close()
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
        # con base de datos falsa:
        # for user in users:
        #     if user['username'] == request.form["username"] and user['password'] == request.form["password"]:
        #         return redirect('/perfil')

        # con sqlite
        username = request.form["username"]
        password = request.form["password"]

        # con sql:
        # conn = get_db_connection()
        # query = conn.execute("SELECT * FROM users WHERE users.username == ?", (username,))
        # user_exist = query.fetchone()
        # conn.close()

        # con orm:
        orm_user = User("blog.db")
        user_exist = orm_user.get_user_by_username(username=username)
        if user_exist and user_exist[0]['password'] == password:
            return redirect('/perfil')

        return render_template("login.html", error="Usuario o contraseña incorrecta")


# ruta para registro, get para obtener el form y post para procesar los datos de usuario y guardarlos
# solo en memoria
# @app.route('/register', methods=["GET", "POST"])
# def register():
#     if request.method == "GET":
#         return render_template("register.html")
#     elif request.method == "POST":
#             user_exist = list(filter(lambda user: user['username'] == request.form["username"], users))
#             if user_exist:
#                 return render_template("register.html", error="El username ya existe")
#             new_id = users[-1]["id"] + 1
#             new_user = {"id": new_id, "username": request.form["username"], "password":  request.form["password"]}
#             users.append(new_user)
#             return "ok"


# ruta para registro, get para obtener el form y post para procesar los datos de usuario y guardarlos
# en bd
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if not username or not password:
            return render_template("register.html", error="El username y el password son obligatorios")
        
        if len(password) < 5:
            return render_template("register.html", error="La password debe contener mas de 5 caracteres")
        
        # con sql
        # conn = get_db_connection()
        # query = conn.execute("SELECT * FROM users WHERE users.username == ?", (username,))
        # user_exist = query.fetchone()

        # con orm
        orm_user = User("blog.db")
        user_exist = orm_user.get_user_by_username(username=username)
        if user_exist:
            return render_template("register.html", error="El username ya existe")

        # con sql:
        # conn.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
        # conn.commit()
        # conn.close()

        # con orm primera forma:
        orm_user.create_user(username=username, password=password)

        # con orm segunda forma:
        # orm_user.insert("INSERT INTO users (username, password) VALUES (?,?)",  (username, password))
        return redirect('/login')


# ruta perfil, proximamente solo para usuarios con login
@app.route('/perfil')
def perfil():
    return render_template("perfil.html")


# ruta para crear post, get para visualizar form y post para procesarlo
@app.route('/post', methods=["GET", "POST"])
def create_post():
    # con try except capturo los errores que puedan ocurrir tanto en la ruta, como los lanzados desde las clases y metodos utilizados dentro.
    try:
        if request.method == "GET":
            return render_template("create_post.html")
        elif request.method == "POST":
            autor = request.form["autor"]
            titulo = request.form["titulo"]
            contenido = request.form["contenido"]
            if autor and titulo and contenido:
                # con slq
                # conn = get_db_connection()
                # conn.execute("INSERT INTO posts (autor, titulo, contenido) VALUES (?,?,?)", (autor, titulo, contenido))
                # conn.commit()
                # conn.close()

                # con orm
                orm_posts = Post("blog.db")
                orm_posts.create_post(autor=autor, titulo=titulo, contenido=contenido)
                return redirect('/')
            else:
                return render_template("create_post.html", error="Todos los campos del post son obligatorios")
    except Exception as e:
        return render_template("create_post.html", error="En este momento, no podemos procesar la solicitud, intente nuevamente")


# ruta para visualizar un post por id
@app.route('/post/<id>')
def post_id(id):
    # for post in posts:
    #     if post["id"] == id:
    #         return render_template("post.html", post=post)
    # return 'ok'
    
    # con sql:
    # conn = get_db_connection()
    # query = conn.execute("SELECT * FROM posts WHERE posts.id == ?", id)
    # post = query.fetchone()
    # conn.close()

    # con orm propio:
    orm_posts = Post("blog.db")
    post = orm_posts.get_posts_by_id(id=id)

    if post:
        return render_template("post.html", post=post[0])
    return redirect('/')




# ruta para probar parametros dinamicos por url y ademas hacer el cast directo en url
# @app.route('/otros/calculadora/<int:numa>/<int:numb>')
# def calculadora(numa, numb):
#     suma = numa+numb
#     return render_template("calcu.html", resultado=suma)


# ruta para probar el cast de tipo path
# @app.route('/otros/<path:url>')
# def path_url(url):
#     print(url)
#     list_post = []
#     return render_template("home.html", posts=list_post)


# ruta ejemplo de redirect y url_for
# @app.route('/algo/<algo>')
# def algo(algo):
#     if algo.isnumeric():
#         # return redirect(url_for('busqueda_post', id=algo))
#         return redirect(f'/post/{algo}')
#     else:
#         return render_template("home.html", posts=posts)

app.run(debug=True)