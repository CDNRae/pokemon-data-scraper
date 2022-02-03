import json
import requests

generations = ["II", "III", "IV", "V", "VI", "VII", "VII"]

# A list of Pokemon who cannot be legitimately obtained from an egg
non_obtainable_first_chains = ["articuno",
                               "zapdos",
                               "moltres",
                               "mewtwo",
                               "mew",
                               "unown",
                               "raikou",
                               "entei",
                               "suicune",
                               "raikou",
                               "lugia",
                               "ho-oh",
                               "celebi",
                               "regirock",
                               "regice",
                               "registeel",
                               "latias",
                               "latios",
                               "kyogre",
                               "groudon",
                               "rayquaza",
                               "jirachi",
                               "deoxys",
                               "uxie",
                               "mesprit",
                               "azelf",
                               "dialga",
                               "palkia",
                               "heatran",
                               "regigigas",
                               "giratina",
                               "cresselia",
                               "darkrai",
                               "shaymin",
                               "arceus",
                               "victini",
                               "cobalion",
                               "terrakion",
                               "virizion",
                               "tornadus",
                               "thundurus",
                               "reshiram",
                               "zekrom",
                               "landorus",
                               "kyurem",
                               "keldeo",
                               "meleotta",
                               "genesect",
                               "xerneas",
                               "ylvetal",
                               "zygarde",
                               "diancie",
                               "hoopa",
                               "volcanion",
                               "type: null",
                               "tapu koko",
                               "tapu lele",
                               "tapu bulu",
                               "tapu fini",
                               "cosmog",
                               "nihilego",
                               "buzzwole",
                               "pheromosa",
                               "xurkitree",
                               "celesteela",
                               "kartana",
                               "guzzlord",
                               "necrozma",
                               "magearna",
                               "marshadow",
                               "poiple",
                               "statakata",
                               "blacephalon",
                               "zeraora",
                               "meltan",
                               "dracozolt",
                               "arctozolt",
                               "arctovish",
                               "dracovish",
                               "zacian",
                               "zamazenta",
                               "eternatus",
                               "kubfu",
                               "zarude",
                               "regieleki",
                               "regidrago",
                               "glastrier",
                               "spectrier"
                               "calyrex",
                               "enamorus",
                               "ditto"
                               ]
alolan_variants = ["diglett-alola", "grimer-alola", "geodude-alola", "rattata-alola", "meowth-alola", "vulpix-alola",
                   "sandshrew-alola"]
galar_variants = ["zigzagoon-galar", "meowth-galar", "farfetchd-galar", "stunfisk-galar", "corsola-galar",
                  "yamask-galar", "ponyta-galar", "darumaka-galar", "slowpoke-galar"]


# Ripped from https://stackoverflow.com/questions/60978672/python-string-to-camelcase
def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0].capitalize() + ''.join(i.capitalize() for i in s[1:])


# Get a list of Pokemon that can be obtained from an egg, and their evolved forms (if any). The evolved forms will be
# used to determine the future typing of a Pokemon
def get_hatchable_pokemon():
    base_url = "https://pokeapi.co/api/v2/evolution-chain/"
    num_evo_chains = 0
    num_current_evo_chain = 1  # the evo chain IDs in PokeAPI start at 1
    list_of_pokemon = []
    output_file = open("data/egg_obtainable_pokemon.json", "w+")

    response = requests.get(base_url)
    data = response.json()

    num_evo_chains = data["count"]

    while num_current_evo_chain < num_evo_chains:
        response = requests.get(base_url + str(num_current_evo_chain))

        if response.status_code == 200:
            data = response.json()

            # Make sure that the Pokemon at the beginning of the chain can be obtained through an egg
            if (data["chain"]["species"]["name"]).lower() not in non_obtainable_first_chains:
                pokemon = {
                    "name": data["chain"]["species"]["name"],
                    "url": data["chain"]["species"]["url"],
                    "evolves_to": []
                }

                next_evo = data["chain"]["evolves_to"]

                # Check for the next line in the evo chain
                for evo in next_evo:
                    pokemon["evolves_to"].append(evo["species"]["name"])

                    if len(evo["evolves_to"]) > 0:
                        for next_next_evo in evo["evolves_to"]:
                            pokemon["evolves_to"].append(next_next_evo["species"]["name"])

                list_of_pokemon.append(pokemon)

        print(num_current_evo_chain)
        num_current_evo_chain += 1

    json.dump(list_of_pokemon, output_file)
    output_file.close()


# Gets a list of what egg-obtainable Pokemon are in each generation's Pokedex. It relies on the existence and proper
# population of flaskr/data/egg_obtainable_pokemon.json, which is done by the above function
def get_list_of_pokemon_in_gen_pokedex():
    list_of_pokemon_file = open("data/egg_obtainable_pokemon.json")
    list_of_pokemon_json = json.load(list_of_pokemon_file)
    list_of_pokemon = []
    list_of_pokemon_file.close()

    for pokemon in list_of_pokemon_json:
        list_of_pokemon.append(pokemon["name"])

    generation = 2

    with open("data/national_dex.json",
              "r") as national_dex_file:
        national_dex = (json.load(national_dex_file))["pokemon_entries"]

        list_of_pokemon_in_gen_dex = []

        while generation <= 8:
            national_dex_offset = 0
            national_dex_cap = 0
            gen_pokedex_filepath = "data/pokedex/"

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

            generation += 1


def create_pokemon_object(pokemon, has_url):
    # The refined pokemon object, to be stored as data
    refined_pokemon = {
        "name": "",
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
            "fire_red/leaf_green": [],
            "diamond/pearl": [],
            "platinum": [],
            "heart_gold/soul_silver": [],
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
            "gold/silver": [],
            "crystal": [],
            "ruby/sapphire": [],
            "emerald": [],
            "fire_red/leaf_green": [],
            "diamond/pearl": [],
            "platinum": [],
            "heart_gold/soul_silver": [],
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
    response = ""
    base_url = "https://pokeapi.co/api/v2/pokemon/"

    # Alolan and Galar variants have to be gotten via name instead of ID, hence the if-statement
    if has_url:
        refined_pokemon["name"] = pokemon["name"]
        split_url = pokemon["url"].split("/")
        response = requests.get(base_url + split_url[len(split_url) - 2])

    else:
        refined_pokemon["name"] = pokemon
        response = requests.get(base_url + pokemon)

    raw_pokemon_data = response.json()

    # Get typing
    for type in raw_pokemon_data["types"]:
        if type["slot"] == 1:
            refined_pokemon["primary_type"] = type["type"]["name"]
        else:
            refined_pokemon["secondary_type"] = type["type"]["name"]

    # Get abilities, hidden and regular. For hidden, it's only a string since Pokemon don't have more than one
    # possible hidden ability
    for ability in raw_pokemon_data["abilities"]:
        if ability["is_hidden"] is False:
            refined_pokemon["regular_abilities"].append(ability["ability"]["name"])
        else:
            refined_pokemon["hidden_ability"] = ability["ability"]["name"]

    # Get forms
    if len(raw_pokemon_data["forms"]) > 1:
        for form in raw_pokemon_data["forms"]:
            refined_pokemon["forms"].append(form["name"])

    # Get moves. This is mostly a mess of if/else checks
    for move in raw_pokemon_data["moves"]:
        # Sanitize move name for PKHeX
        move_name = to_camel_case(move["move"]["name"])

        for game_version in move["version_group_details"]:
            # Check for egg moves and TM moves
            if game_version["level_learned_at"] == 0 and game_version["move_learn_method"]["name"] == "egg":

                if game_version["version_group"]["name"] == "gold-silver":
                    refined_pokemon["egg_moves"]["gold/silver"].append(move_name)

                elif game_version["version_group"]["name"] == "crystal":
                    refined_pokemon["egg_moves"]["crystal"].append(move_name)

                elif game_version["version_group"]["name"] == "ruby-sapphire":
                    refined_pokemon["egg_moves"]["ruby/sapphire"].append(move_name)

                elif game_version["version_group"]["name"] == "emerald":
                    refined_pokemon["egg_moves"]["emerald"].append(move_name)

                elif game_version["version_group"]["name"] == "firered-leafgreen":
                    refined_pokemon["egg_moves"]["fire_red/leaf_green"].append(move_name)

                elif game_version["version_group"]["name"] == "diamond-pearl":
                    refined_pokemon["egg_moves"]["diamond/pearl"].append(move_name)

                elif game_version["version_group"]["name"] == "platinum":
                    refined_pokemon["egg_moves"]["platinum"].append(move_name)

                elif game_version["version_group"]["name"] == "heartgold-soulsilver":
                    refined_pokemon["egg_moves"]["heart_gold/soul_silver"].append(move_name)

                elif game_version["version_group"]["name"] == "black-white":
                    refined_pokemon["egg_moves"]["black/white"].append(move_name)

                elif game_version["version_group"]["name"] == "black2-white2":
                    refined_pokemon["egg_moves"]["black2/white2"].append(move_name)

                elif game_version["version_group"]["name"] == "x-y":
                    refined_pokemon["egg_moves"]["x/y"].append(move_name)

                elif game_version["version_group"]["name"] == "omega-ruby-alpha-sapphire":
                    refined_pokemon["egg_moves"]["omega_ruby/alpha_sapphire"].append(move_name)

                elif game_version["version_group"]["name"] == "sun-moon":
                    refined_pokemon["egg_moves"]["sun/moon"].append(move_name)

                elif game_version["version_group"]["name"] == "ultra-sun-ultra-moon":
                    refined_pokemon["egg_moves"]["ultra_sun/ultra_moon"].append(move_name)

                elif game_version["version_group"]["name"] == "ultra-sun-ultra-moon":
                    refined_pokemon["egg_moves"]["ultra_sun/ultra_moon"].append(move_name)

                    # Check for egg moves and TM moves
            elif game_version["level_learned_at"] == 1:

                if game_version["version_group"]["name"] == "gold-silver":
                    refined_pokemon["regular_moves"]["gold/silver"].append(move_name)

                elif game_version["version_group"]["name"] == "crystal":
                    refined_pokemon["regular_moves"]["crystal"].append(move_name)

                elif game_version["version_group"]["name"] == "ruby-sapphire":
                    refined_pokemon["regular_moves"]["ruby/sapphire"].append(move_name)

                elif game_version["version_group"]["name"] == "emerald":
                    refined_pokemon["regular_moves"]["emerald"].append(move_name)

                elif game_version["version_group"]["name"] == "firered-leafgreen":
                    refined_pokemon["regular_moves"]["fire_red/leaf_green"].append(move_name)

                elif game_version["version_group"]["name"] == "diamond-pearl":
                    refined_pokemon["regular_moves"]["diamond/pearl"].append(move_name)

                elif game_version["version_group"]["name"] == "platinum":
                    refined_pokemon["regular_moves"]["platinum"].append(move_name)

                elif game_version["version_group"]["name"] == "heartgold-soulsilver":
                    refined_pokemon["regular_moves"]["heart_gold/soul_silver"].append(move_name)

                elif game_version["version_group"]["name"] == "black-white":
                    refined_pokemon["regular_moves"]["black/white"].append(move_name)

                elif game_version["version_group"]["name"] == "black2-white2":
                    refined_pokemon["regular_moves"]["black2/white2"].append(move_name)

                elif game_version["version_group"]["name"] == "x-y":
                    refined_pokemon["regular_moves"]["x/y"].append(move_name)

                elif game_version["version_group"]["name"] == "omega-ruby-alpha-sapphire":
                    refined_pokemon["regular_moves"]["omega_ruby/alpha_sapphire"].append(move_name)

                elif game_version["version_group"]["name"] == "sun-moon":
                    refined_pokemon["regular_moves"]["sun/moon"].append(move_name)

                elif game_version["version_group"]["name"] == "ultra-sun-ultra-moon":
                    refined_pokemon["regular_moves"]["ultra_sun/ultra_moon"].append(move_name)

                elif game_version["version_group"]["name"] == "ultra-sun-ultra-moon":
                    refined_pokemon["regular_moves"]["ultra_sun/ultra_moon"].append(move_name)

    return refined_pokemon


def get_detailed_info_hatchable_pokemon():
    list_of_pokemon_file = open("data/egg_obtainable_pokemon.json")
    list_of_pokemon = json.load(list_of_pokemon_file)
    all_refined_pokemon = []

    for pokemon in list_of_pokemon:
        all_refined_pokemon.append(create_pokemon_object(pokemon, True))

    for pokemon in alolan_variants:
        all_refined_pokemon.append(create_pokemon_object(pokemon, False))

    for pokemon in galar_variants:
        all_refined_pokemon.append(create_pokemon_object(pokemon, False))

    list_of_pokemon_file.close()

    output_file = open("data/pokemon.json", "w+")
    json.dump(all_refined_pokemon, output_file)
    output_file.close()


if __name__ == '__main__':
    get_hatchable_pokemon()
    # get_list_of_pokemon_in_gen_pokedex()
    # get_detailed_info_hatchable_pokemon()
