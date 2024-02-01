from flask import Flask, render_template, request, redirect

from orm import Post, User

app = Flask(__name__)

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
        
        if not username or not password:
            return render_template("register.html", error="El username y el password son obligatorios")
        
        if len(password) < 5:
            return render_template("register.html", error="La password debe contener mas de 5 caracteres")

        orm_user = User("blog.db")
        user_exist = orm_user.get_user_by_username(username=username)
        if user_exist:
            return render_template("register.html", error="El username ya existe")
        orm_user.create_user(username=username, password=password)

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
    orm_posts = Post("blog.db")
    post = orm_posts.get_posts_by_id(id=id)

    if post:
        return render_template("post.html", post=post[0])
    return redirect('/')

app.run(debug=True)