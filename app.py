import os
from flask import Flask, render_template, abort
from flask_flatpages import FlatPages

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config.update(
    FLATPAGES_ROOT=os.path.join(BASE_DIR, "content", "posts"),
    FLATPAGES_EXTENSION=".md",
    FLATPAGES_MARKDOWN_EXTENSIONS=["meta", "fenced_code", "tables"],
    FREEZER_DESTINATION=os.path.join(BASE_DIR, "docs"),
    FREEZER_BASE_URL="https://luciadiazs.github.io/entre_lineas/",
    APPLICATION_ROOT="/entre_lineas",
)

pages = FlatPages(app)

TEAM = [
    {"name": "Nicolle Soberón",   "role": "Integrante", "comision": None},
    {"name": "Connie Pérez",       "role": "Integrante", "comision": None},
    {"name": "Camila Marzal",      "role": "Integrante", "comision": None},
    {"name": "Samantha Calderón",  "role": "Integrante", "comision": None},
    {"name": "Ariana Alcedo",      "role": "Integrante", "comision": None},
    {"name": "Cielo Briceño",      "role": "Integrante", "comision": None},
    {"name": "Mayra Cárdenas",     "role": "Integrante", "comision": None},
    {"name": "Claudia Tejada",     "role": "Integrante", "comision": None},
    {"name": "Katherin Peña",      "role": "Integrante", "comision": None},
    {"name": "Daniela Pulido",     "role": "Integrante", "comision": None},
    {"name": "Lucía Díaz",         "role": "Integrante", "comision": None},
    {"name": "Aaron Vega",         "role": "Integrante", "comision": None},
    {"name": "Camila Lira",        "role": "Integrante", "comision": None},
]

CATEGORIAS = ["Todos", "Género", "Democracia", "Medio ambiente",
               "Pueblos indígenas", "Seguridad ciudadana", "DDHH"]


def get_posts(categoria=None):
    posts = [p for p in pages]
    if categoria and categoria != "Todos":
        posts = [p for p in posts if p.meta.get("categoria") == categoria]
    posts.sort(key=lambda p: p.meta.get("date", ""), reverse=True)
    return posts


@app.route("/")
def index():
    latest = get_posts()[:3]
    return render_template("index.html", posts=latest)


@app.route("/analisis/")
@app.route("/analisis/<categoria>/")
def analisis(categoria="Todos"):
    if categoria not in CATEGORIAS:
        abort(404)
    posts = get_posts(categoria)
    return render_template("analisis.html", posts=posts,
                           categorias=CATEGORIAS, categoria_actual=categoria)


@app.route("/analisis/post/<path:slug>/")
def post(slug):
    page = pages.get(slug)
    if page is None:
        abort(404)
    return render_template("post.html", post=page)


@app.route("/equipo/")
def equipo():
    return render_template("equipo.html", team=TEAM)


@app.route("/alertas/")
def alertas():
    return render_template("alertas.html")


if __name__ == "__main__":
    app.run(debug=True)
