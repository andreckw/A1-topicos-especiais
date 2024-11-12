from flask import *
from config import app
from formularios import *
import os


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("/index.html")


@app.route("/adicionar", methods=["POST", "GET"])
def adicionar():
    formulario = FileForm()

    if formulario.validate_on_submit():
        f = formulario.file.data
        filename = f"upload/{f.filename}"
        f.save(filename)

        return render_template("/adicionar.html", attr=formulario)

    return render_template("/adicionar.html", attr=formulario)


if __name__ == "__main__":

    if not os.path.isdir("upload"):
        os.mkdir("upload")

    app.run(debug=True)
