from flask import Flask, url_for, render_template, request
from wtforms import Form, DecimalField, SelectField, validators


class GeneratorForm(Form):
    number_of_pokemon = DecimalField(label="number_to_generate",
                                     validators=[validators.NumberRange(min=1, max=100)])
    generation = SelectField(label="Generation", choices=["I", "II", "III", "IV", "V", "VI", "VII", "VIII"])


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="Pokemon"
    )

    @app.route("/index", methods=["GET", "POST"])
    def index():
        generatorForm = GeneratorForm()

        if request.method == "GET":
            return render_template("index.html", generatorForm=generatorForm)
        else:
            data = request.form
            print(data)
            return render_template("index.html", generatorForm=generatorForm)

    return app

