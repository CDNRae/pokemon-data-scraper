from flask import Flask, url_for, render_template, request
from wtforms import Form, DecimalField, SelectField, validators
from . import pokemon_generator


class GeneratorForm(Form):
    number_of_pokemon = DecimalField(label="number_to_generate",
                                     validators=[validators.NumberRange(min=1, max=100)])
    generation = SelectField(label="Generation", choices=["I", "II", "III", "IV", "V", "VI", "VII", "VIII"])


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="Pokemon"
    )

    @app.route("/", methods=["GET", "POST"])
    def index():
        generatorForm = GeneratorForm()
        pokemon_data = ""
        number_to_generate = 1
        generation = 2
        egg_move_chance = 0
        hidden_ability_chance = 0
        shiny_chance = 0

        if request.method == "GET":
            return render_template("index.html", generatorForm=generatorForm, pokemon_data=pokemon_data)
        else:
            data = request.form

            if data["number_to_generate"] != "" and data["number_to_generate"] != "0":
                number_to_generate = int(data["number_to_generate"])

            if data["generation"] != "" and data["generation"] != "0":
                generation = int(data["generation"])

            if data["egg_move_chance"] != "" and data["egg_move_chance"] != "0":
                egg_move_chance = int(data["egg_move_chance"])

            if data["hidden_ability_chance"] != "" and data["hidden_ability_chance"] != "0":
                hidden_ability_chance = int(data["hidden_ability_chance"])

            if data["shiny_chance"] != "" and data["shiny_chance"] != "0":
                shiny_chance = int(data["shiny_chance"])

            pokemon_data = pokemon_generator.generate_pokemon(number_to_generate, generation, egg_move_chance, hidden_ability_chance, shiny_chance)
            return render_template("index.html", generatorForm=generatorForm, pokemon_data=pokemon_data)

    return app