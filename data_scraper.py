import requests
import pandas
from bs4 import BeautifulSoup
import json
import time

generations = ["II", "III", "IV", "V", "VI", "VII", "VII"]


def get_move_data():
    pokemon_list = pandas.read_csv("./data/pokemon.csv")
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

        with open(f"./data/pokemon_moves/{pokemon_name}.json", "w+") as output_file:
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


if __name__ == '__main__':
    get_move_data()
