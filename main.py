from flask import *
from config import app, db
from formularios import *
import os
import pandas as pd
from models import Course


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

        csv_file = "upload/udemy_courses_dataset.csv"
        df = pd.read_csv(csv_file)

        for i, row in df.iterrows():
            course = Course(
                course_title=row['course_title'],
                is_paid=row['is_paid'],
                price=row['price'],
                level=row['level'],
                content_duration=row['content_duration'],
                subject=row['subject']
            )
            db.session.add(course)
        db.session.commit()

        return render_template("/adicionar.html", attr=formulario)

    return render_template("/adicionar.html", attr=formulario)


if __name__ == "__main__":

    if not os.path.isdir("upload"):
        os.mkdir("upload")

    app.run(debug=True)
