from flask import Flask, render_template, request, redirect
from wtforms import Form, DecimalField, SelectField, SelectMultipleField, BooleanField, validators
from flaskr import pokemon_generator


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="Pokemon"
    )

    @app.route('/', defaults={'path': ''})
    def returnToIndex(path):
        return redirect("/index")

    @app.route('/index', methods=["GET", "POST"])
    def index():
        pokemon_data = ""

        type_restrictions = []
        type_restrictions_final_evo_only = True
        type_restrictions_first_and_final_evo = True

        user_data = {
            "number_to_generate": 1,
            "generation": 2,
            "egg_move_chance": 0,
            "hidden_ability_chance": 0,
            "shiny_chance": 0
        }

        if request.method == "GET":
            return render_template("index.html", pokemon_data=pokemon_data)
        else:
            data = request.form

            if data["number_to_generate"] != "" and data["number_to_generate"] != "0":
                user_data["number_to_generate"] = int(data["number_to_generate"])

            if data["generation"] != "" and data["generation"] != "0":
                user_data["generation"] = int(data["generation"])

            if data["egg_move_chance"] != "" and data["egg_move_chance"] != "0":
                user_data["egg_move_chance"] = int(data["egg_move_chance"])

            if data["hidden_ability_chance"] != "" and data["hidden_ability_chance"] != "0":
                user_data["hidden_ability_chance"] = int(data["hidden_ability_chance"])

            if data["shiny_chance"] != "" and data["shiny_chance"] != "0":
                user_data["shiny_chance"] = int(data["shiny_chance"])

            pokemon_data = pokemon_generator.generate_pokemon(user_data["number_to_generate"], user_data["generation"], user_data["egg_move_chance"],
                                                              user_data["hidden_ability_chance"], user_data["shiny_chance"], types=[],
                                                              consider_final_evo_type_only=True,
                                                              consider_first_and_final_evo_type=True)

            return render_template("index.html", user_data=user_data, pokemon_data=pokemon_data)

    return app


if __name__ == '__main__':
    create_app()
