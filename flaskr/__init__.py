from flask import Flask, url_for, render_template, request
from wtforms import Form, DecimalField, SelectField, validators


class GeneratorForm(Form):
    number_of_pokemon = DecimalField(label="number_to_generate",
                                     validators=[validators.NumberRange(min=1, max=100)])
    generation = SelectField(label="Generation", choices=["1", "2", "3", "4", "5", "6", "7", "8"])


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="Pokemon"
    )

    @app.route("/index")
    def index():
        generatorForm = GeneratorForm()
        return render_template("index.html", generatorForm=generatorForm)

    return app

