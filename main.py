from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Falsa db de posts
posts = [
    {"id": 1, "autor":"Joaquin", "titulo":"Python", "texto": "blabblablala"},
    {"id": 2, "autor":"Ines", "titulo":"Java", "texto": "bsjadbajkdbdbd"},
    {"id": 3, "autor":"Nico", "titulo":"JS", "texto": "bsjadbajkdbdbd"},
    {"id": 4, "autor":"Andres", "titulo":"Go", "texto": "bsjadbajkdbdbd"},
    {"id": 5, "autor":"Maria", "titulo":"TS", "texto": "bsjadbajkdbdbd"},
    {"id": 6, "autor":"Juan", "titulo":"Java", "texto": "bsjadbajkdbdbd"},
    {"id": 7, "autor":"Juan", "titulo":"Java", "texto": "bsjadbajkdbdbd"},
    {"id": 8, "autor":"Juan", "titulo":"Java", "texto": "bsjadbajkdbdbd"},
    {"id": 9, "autor":"Juan", "titulo":"Java", "texto": "bsjadbajkdbdbd"},
    {"id": 10, "autor":"Juan", "titulo":"Java", "texto": "bsjadbajkdbdbd"},
    {"id": 11, "autor":"Juan", "titulo":"Java", "texto": "bsjadbajkdbdbd"},
    {"id": 12, "autor":"Juan", "titulo":"Java", "texto": "bsjadbajkdbdbd"},
    {"id": 13, "autor":"Juan", "titulo":"Java", "texto": "bsjadbajkdbdbd"},

]

# falsa db de users
users = [
    {"username": "jzuazo", "password":"123456"},
    {"username": "iness", "password":"123456"},
]

# posts = []

# ruta home para visualizar todos los posts y poder buscar por titulo
@app.route('/')
def home():
    busqueda = request.args.get('search')
    if busqueda:
        list_post = []
        for post in posts:
            if busqueda.lower() in post['titulo'].lower():
                list_post.append(post)
        return render_template("home.html", posts=list_post)
    else:
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
        for user in users:
            if user['username'] == request.form["username"] and user['password'] == request.form["password"]:
                return redirect('/perfil')
        else:
            return render_template("login.html", error="Usuario o contraseña incorrecta")

# ruta perfil, proximamente solo para usuarios con login
@app.route('/perfil')
def perfil():
    return render_template("perfil.html")

# ruta para crear post, get para visualizar form y post para procesarlo
@app.route('/post', methods=["GET", "POST"])
def post():
    pass

# ruta para visualizar un post por id
@app.route('/post/<int:id>')
def post_id(id):
    for post in posts:
        if post["id"] == id:
            return render_template("post.html", post=post)
    return 'ok'

# ruta para probar el cast de tipo path
@app.route('/otros/<path:url>')
def path_url(url):
    print(url)
    list_post = []
    return render_template("home.html", posts=list_post)

# ruta para probar parametros dinamicos por url y ademas hacer el cast directo en url
@app.route('/otros/calculadora/<int:numa>/<int:numb>')
def calculadora(numa, numb):
    suma = numa+numb
    return render_template("calcu.html", resultado=suma)

# ruta ejemplo de redirect y url_for
# @app.route('/algo/<algo>')
# def algo(algo):
#     if algo.isnumeric():
#         # return redirect(url_for('busqueda_post', id=algo))
#         return redirect(f'/post/{algo}')
#     else:
#         return render_template("home.html", posts=posts)

app.run(debug=True)