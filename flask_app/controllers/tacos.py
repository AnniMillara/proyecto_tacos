# CONTROLADOR DE TACOS
from flask_app import app
from flask import (
    render_template,
    redirect,
    request,
    url_for
)
from flask_app.models.taco import Taco
from flask_app.models.restaurante import Restaurante

# INICIO
@app.route("/")
def index():
    """
    Muestra el formulario para crear un taco.
    También recupera todos los restaurantes para que
    el usuario pueda seleccionar uno.
    """

    todos_restaurantes = Restaurante.get_all()
    return render_template(
        "index.html",
        todos_restaurantes=todos_restaurantes
    )

# CREATE
# Crear taco
@app.route("/crear",methods=["POST"])
def crear():
    """
    Recibe el formulario y crea un taco.
    """
    datos = {
        "tortilla": request.form["tortilla"].strip(),
        "guiso": request.form["guiso"].strip(),
        "salsa": request.form["salsa"].strip(),
        "restaurante_id": request.form["restaurante_id"]
        }
    Taco.save(datos)
    return redirect(url_for("tacos"))

# READ
# Listar tacos
@app.route("/tacos")
def tacos():
    """
    Recupera todos los tacos
    y los envía a la vista.
    """
    todos_los_tacos = Taco.get_all()
    return render_template(
        "resultados.html",
        todos_tacos=todos_los_tacos
    )

# READ
# Restaurantes + Tacos
@app.route("/restaurantes/<int:id>")
def restaurante(id):
    """
    Muestra un restaurante junto con
    todos sus tacos relacionados.
    """
    datos = {"id": id}

    restaurante = Restaurante.get_restaurante_y_tacos(datos)
    if restaurante is None:
        return (
            "Restaurante no encontrado", 404
        )
    return render_template(
        "restaurante.html",
        restaurante=restaurante
    )

#Listado de restaurantes
@app.route("/restaurantes")
def restaurantes():
    """
    Muestra todos los restaurantes.
    """
    todos_restaurantes = Restaurante.get_all()
    return render_template(
        "restaurantes.html",
        restaurantes=todos_restaurantes
    )

# READ
# Ver detalle
@app.route("/mostrar/<int:taco_id>")
def detalle(taco_id):
    """
    Recupera un taco específico.
    """
    datos = {"id": taco_id}
    taco = Taco.get_one(datos)
    
    if taco is None:
        return (
            "Taco no encontrado",
            404
        )
    return render_template("detalle.html", taco=taco)

# UPDATE
# Mostrar formulario
@app.route("/editar/<int:taco_id>")
def editar(taco_id):
    """
    Recupera un taco y muestra
    el formulario de edición.
    """
    datos = {"id": taco_id}
    taco = Taco.get_one(datos)
    
    if taco is None:
        return (
            "Taco no encontrado",
            404
        )
    return render_template( "editar.html", taco=taco )

# UPDATE
# Procesar información
@app.route("/actualizar/<int:taco_id>", methods=["POST"])
def actualizar(taco_id):
    """
    Actualiza la información del taco.
    """
    datos = {
        "id": taco_id,
        "tortilla": request.form["tortilla"],
        "guiso": request.form["guiso"],
        "salsa": request.form["salsa"],
        "salsa": request.form["salsa"]
    }
    
    Taco.update(datos)
    return redirect(
        url_for(
            "detalle",
            taco_id=taco_id
        )
    )

# DELETE
# Eliminar taco
@app.route("/borrar/<int:taco_id>")
def borrar(taco_id):
    """
    Elimina un taco.
    """
    datos = {"id": taco_id}
    Taco.delete(datos)
    return redirect(url_for("tacos"))