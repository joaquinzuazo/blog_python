from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {"autor":"Joaquin", "texto": "blabblablala"},
    {"autor":"Ines", "texto": "bsjadbajkdbdbd"},
    {"autor":"Nico", "texto": "bsjadbajkdbdbd"},
    {"autor":"Andres", "texto": "bsjadbajkdbdbd"},
    {"autor":"Maria", "texto": "bsjadbajkdbdbd"},
    {"autor":"Juan", "texto": "bsjadbajkdbdbd"},
]

# posts = []

@app.route('/')
def home():
    return render_template("home.html", nombre="Joaquin", posts=posts)

@app.route('/contacto')
def contacto():
    return render_template("contacto.html")

app.run(debug=True)