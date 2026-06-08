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

AREAS = [
    {
        "nombre": "Coordinación General",
        "miembros": [
            {"name": "Nicolle Soberón", "foto": "nicolle-soberon.jpg"},
            {"name": "Connie Pérez",    "foto": "connie-perez.jpg"},
        ],
    },
    {
        "nombre": "Análisis",
        "miembros": [
            {"name": "Daniela Pulido",    "foto": "daniela-pulido.jpg"},
            {"name": "Lucía Díaz",        "foto": "lucia-diaz.jpg"},
            {"name": "Samantha Calderón", "foto": "samantha-calderon.jpg"},
            {"name": "Cielo Briceño",     "foto": "cielo-briceno.jpg"},
            {"name": "Ariana Alcedo",     "foto": "ariana-alcedo.jpg"},
        ],
    },
    {
        "nombre": "Seguimiento",
        "miembros": [
            {"name": "Katherin Peña", "foto": "katherin-pena.jpg"},
        ],
    },
    {
        "nombre": "Medios",
        "miembros": [
            {"name": "Mayra Cárdenas", "foto": "mayra-cardenas.jpg"},
            {"name": "Claudia Tejada", "foto": "claudia-tejada.jpg"},
        ],
    },
    {
        "nombre": "Programación",
        "miembros": [
            {"name": "Lucía Díaz", "foto": "lucia-diaz.jpg"},
        ],
    },
    {
        "nombre": "Relaciones Interinstitucionales y Economía",
        "miembros": [
            {"name": "Aaron Vega",    "foto": "aaron-vega.jpg"},
            {"name": "Camila Marzal", "foto": "camila-marzal.jpg"},
        ],
    },
]

TEAM = [m for area in AREAS for m in area["miembros"]]

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
    return render_template("equipo.html", areas=AREAS)


@app.route("/nosotros/")
def nosotros():
    return render_template("nosotros.html")


@app.route("/alertas/")
def alertas():
    return render_template("alertas.html")


if __name__ == "__main__":
    app.run(debug=True)
