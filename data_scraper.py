import requests
import pandas
from bs4 import BeautifulSoup
import json
import time

generations = ["II", "III", "IV", "V", "VI", "VII", "VII"]


def get_move_data():
    pokemon_list = pandas.read_csv("flaskr/data/pokemon.csv")
    egg_move_column_counter = 0
    regular_move_column_counter = 0
    egg_move_column_counter_increment = 0
    regular_move_column_counter_increment = 0
    egg_move_table_index = 7
    regular_move_table_index = 3

    for pokemon in pokemon_list.itertuples(index=False):
        pokemon_name = pokemon[3].capitalize()
        moves = {
            "II": {
                "egg_moves": [],
                "regular_moves": []
            },
            "III": {
                "egg_moves": [],
                "regular_moves": []
            },
            "IV": {
                "egg_moves": [],
                "regular_moves": []
            },
            "V": {
                "egg_moves": [],
                "regular_moves": []
            },
            "VI": {
                "egg_moves": [],
                "regular_moves": []
            },
            "VII": {
                "egg_moves": [],
                "regular_moves": []
            }
        }

        with open(f"flaskr/data/pokemon_moves/{pokemon_name}.json", "w+") as output_file:
            for generation in generations:
                try:
                    if generation == "II":
                        egg_move_column_counter = 2
                        regular_move_column_counter = 1
                        egg_move_column_counter_increment = 6
                        regular_move_column_counter_increment = 6
                        egg_move_table_index = 7
                        regular_move_table_index = 3

                    elif generation == "III" or generation == "IV":
                        egg_move_column_counter = 2
                        regular_move_column_counter = 1
                        egg_move_column_counter_increment = 9
                        regular_move_column_counter_increment = 9
                        egg_move_table_index = 7
                        regular_move_table_index = 3

                    elif generation == "V":
                        egg_move_column_counter = 2
                        regular_move_column_counter = 1
                        egg_move_column_counter_increment = 7
                        regular_move_column_counter_increment = 7
                        egg_move_table_index = 7
                        regular_move_table_index = 3

                    elif generation == "VI":
                        egg_move_column_counter = 1
                        regular_move_column_counter = 1
                        egg_move_column_counter_increment = 10
                        regular_move_column_counter_increment = 10
                        egg_move_table_index = 11
                        regular_move_table_index = 3

                    else:
                        egg_move_column_counter = 1
                        regular_move_column_counter = 2
                        egg_move_column_counter_increment = 7
                        regular_move_column_counter_increment = 8
                        egg_move_table_index = 11
                        regular_move_table_index = 3

                    data = requests.get(
                        f"https://bulbapedia.bulbagarden.net/wiki/{pokemon_name}_(Pok%C3%A9mon)/Generation_{generation}_learnset")

                    soup = BeautifulSoup(data.text, "html.parser")
                    tables = soup.find_all("table")

                    egg_move_table = tables[egg_move_table_index]
                    egg_move_columns = egg_move_table.find_all("td")

                    while egg_move_column_counter < len(egg_move_columns):
                        move = egg_move_columns[egg_move_column_counter].text

                        moves[generation]["egg_moves"].append(move.rstrip())
                        egg_move_column_counter += egg_move_column_counter_increment

                    regular_move_table = tables[regular_move_table_index]
                    regular_move_columns = regular_move_table.find_all("td")
                    regular_move_column_count = len(regular_move_table.find_all("th"))

                    if generation == "III" and regular_move_column_count > 9:
                        regular_move_column_counter = 2
                        regular_move_column_counter_increment = 10

                    if generation == "VI" and regular_move_column_count > 10:
                        regular_move_column_counter = 2
                        regular_move_column_counter_increment = 11

                    if generation == "VII" and regular_move_column_count < 8:
                        regular_move_column_counter = 1
                        regular_move_column_counter_increment = 7

                    while regular_move_column_counter < len(regular_move_columns):
                        move_level = regular_move_columns[regular_move_column_counter - 1].text

                        move_level_chars_to_remove = 2

                        if len(move_level) > 2 and "00" not in move_level:
                            move_level_chars_to_remove = int(len(move_level) / 2)

                            if generation == "VII":
                                move_level = move_level[1: -move_level_chars_to_remove]
                            else:
                                move_level = move_level[0: -move_level_chars_to_remove]

                        elif generation == "VII":
                            move_level = move_level[2:-2]

                        else:
                            move_level = move_level[0: -move_level_chars_to_remove]

                        move_name = regular_move_columns[regular_move_column_counter].text
                        move_name = move_name.rstrip()

                        move = {"Name": move_name, "Level": move_level}
                        moves[generation]["regular_moves"].append(move)
                        regular_move_column_counter += regular_move_column_counter_increment

                except Exception:
                    continue

            json.dump(moves, output_file)

        # time.sleep(60)

    print("Done")


def get_hatchable_pokemon():
    with open("C:/Users/clock/AppData/Roaming/JetBrains/PyCharmCE2020.3/scratches/scratch_3.json", "a+") as dataFile:
        base_url = "https://pokeapi.co/api/v2/evolution-chain/"
        counter = 237

        response = requests.get(base_url + str(counter))
        data = response.json()
        json.dump(data["chain"]["species"], dataFile)

        counter += 1

        while counter < 467:
            try:
                response = requests.get(base_url + str(counter))
                data = response.json()
                json.dump(data["chain"]["species"], dataFile)
                counter += 1
            except Exception:
                counter += 1
                continue


def get_list_of_pokemon_in_gen_pokedex():
    list_of_pokemon_file = open("C:/Users/clock/AppData/Roaming/JetBrains/PyCharmCE2020.3/scratches/scratch_3.json")
    list_of_pokemon_json = (json.load(list_of_pokemon_file))["list_of_pokemon"]
    list_of_pokemon = []
    list_of_pokemon_file.close()

    for pokemon in list_of_pokemon_json:
        list_of_pokemon.append(pokemon["name"])

    generation = 2

    with open("C:/Users/clock/AppData/Roaming/JetBrains/PyCharmCE2020.3/scratches/scratch_1.json",
              "r") as national_dex_file:
        national_dex = (json.load(national_dex_file))["pokemon_entries"]

        list_of_pokemon_in_gen_dex = []

        while generation <= 8:
            national_dex_offset = 0
            national_dex_cap = 0
            gen_pokedex_filepath = "C:/Users/clock/PycharmProjects/pokemon_egg_generator/flaskr/data/pokedex/"

            if generation == 2:
                national_dex_offset = 0
                national_dex_cap = 251
                gen_pokedex_filepath += "gen_2.json"

            elif generation == 3:
                national_dex_offset = 251
                national_dex_cap = 386
                gen_pokedex_filepath += "gen_3.json"

            elif generation == 4:
                national_dex_offset = 386
                national_dex_cap = 493
                gen_pokedex_filepath += "gen_4.json"

            elif generation == 5:
                national_dex_offset = 493
                national_dex_cap = 649
                gen_pokedex_filepath += "gen_5.json"

            elif generation == 6:
                national_dex_offset = 649
                national_dex_cap = 721
                gen_pokedex_filepath += "gen_6.json"

            elif generation == 7:
                national_dex_offset = 721
                national_dex_cap = 809
                gen_pokedex_filepath += "gen_7.json"

            elif generation == 8:
                national_dex_offset = 809
                national_dex_cap = 898
                gen_pokedex_filepath += "gen_8.json"
                
            while national_dex_offset < national_dex_cap:
                pokemon_name = national_dex[national_dex_offset]["pokemon_species"]["name"]

                if pokemon_name in list_of_pokemon:
                    list_of_pokemon_in_gen_dex.append(pokemon_name)

                national_dex_offset += 1

            gen_pokedex = open(gen_pokedex_filepath, "w")
            json.dump(list_of_pokemon_in_gen_dex, gen_pokedex)

            print(list_of_pokemon_in_gen_dex)
            generation += 1
            
            
def get_detailed_info_hatchable_pokemon():
    list_of_pokemon_file = open("C:/Users/clock/AppData/Roaming/JetBrains/PyCharmCE2020.3/scratches/scratch_3.json")
    list_of_pokemon = json.load(list_of_pokemon_file)

    for pokemon in list_of_pokemon["list_of_pokemon"]:

        # The refined pokemon object, to be stored as data
        refined_pokemon = {
            "name": pokemon["name"],
            "primary_type": "",
            "secondary_type": "",
            "regular_abilities": [],
            "hidden_ability": "",
            "forms": [],
            "regular_moves": {
                "gold/silver": [],
                "crystal": [],
                "ruby/sapphire": [],
                "emerald": [],
                "diamond/pearl": [],
                "platinum": [],
                "black/white": [],
                "black_2/white_2": [],
                "x/y": [],
                "omega_ruby/alpha_sapphire": [],
                "sun/moon": [],
                "ultra_sun/ultra_moon": [],
                "sword/shield": [],
                "brilliant_diamond/shining_pearl": []
            },
            "egg_moves": {
                "crystal": [],
                "ruby/sapphire": [],
                "emerald": [],
                "diamond/pearl": [],
                "platinum": [],
                "black/white": [],
                "black_2/white_2": [],
                "x/y": [],
                "omega_ruby/alpha_sapphire": [],
                "sun/moon": [],
                "ultra_sun/ultra_moon": [],
                "sword/shield": [],
                "brilliant_diamond/shining_pearl": []
            }
        }
        species_url = pokemon["url"].split("/")
        pokemon_url = "https://pokeapi.co/api/v2/pokemon/" + species_url[len(species_url) - 2]

        response = requests.get(pokemon["url"])
        raw_pokemon_data = response.json()

        # Get typing
        for type in raw_pokemon_data["types"]:
            if type["slot"] == 1:
                refined_pokemon["primary_type"] = type["type"]["name"]
            else:
                refined_pokemon["secondary_type"] = type["type"]["name"]

        # Get abilities, hidden and regular
        for ability in raw_pokemon_data["abilities"]:
            if ability["is_hidden"] is False:
                refined_pokemon["regular_abilities"].append(ability["ability"]["name"])
            else:
                refined_pokemon["hidden_ability"].append(ability["ability"]["name"])



if __name__ == '__main__':
    # get_hatchable_pokemon()
    # get_list_of_pokemon_in_gen_pokedex()
    get_detailed_info_hatchable_pokemon()
