from flask import render_template, request, redirect, g, Blueprint
from orm import Post


routes = Blueprint('posts', __name__, template_folder='templates', url_prefix="/posts")


# ruta para crear post, get para visualizar form y post para procesarlo
@routes.route('/crear', methods=["GET", "POST"])
def create_post():
    # con try except capturo los errores que puedan ocurrir tanto en la ruta, como los lanzados desde las clases y metodos utilizados dentro.
    try:
        if request.method == "GET":
            # username = session.get("username")
            if not g.user:
                return render_template("login.html", error="Debe iniciar sesion")
            return render_template("create_post.html")
        elif request.method == "POST":
            # username = session.get("username")
            if not g.user:
                return render_template("login.html", error="Debe iniciar sesion")
            
            autor = g.user
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
@routes.route('/<id>')
def post_id(id):
    orm_posts = Post("blog.db")
    post = orm_posts.get_posts_by_id(id=id)

    if post:
        return render_template("post.html", post=post[0])
    return redirect('/')