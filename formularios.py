from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired


class FileForm(FlaskForm):
    file = FileField(validators=[FileRequired()])
    submit = SubmitField("Enviar Arquivo")

