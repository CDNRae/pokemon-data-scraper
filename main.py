import pandas
import random
import json
from enum import Enum
from pokemon import Pokemon as pokemonClass

# The following arrays hold various information that impose further restrictions on Pokemon genders
genderless_pokemon = [
    "Arctovish", "Arctozolt", "Baltoy", "Beldum", "Bronzor", "Carbink", "Cryogonal", "Dhelmise", "Dracovish",
    "Dracozolt", "Falinks", "Golett", "Klink", "Lunatone", "Magnemite", "Minior", "Polteageist", "Porygon", "Rotom",
    "Solrock", "Staryu", "Unknown", "Voltorb"
]

female_only_pokemon = [
    "Nidoran F", "Illumise", "Happiny", "Kangaskhan", "Smoochum", "Miltank", "Petilil", "Vullaby", "Flabebe",
    "Bounsweet", "Hatenna", "Milcrey"
]

male_only_pokemon = [
    "Tyrogue", "Tauros", "Throh", "Sawk", "Rufflet", "Impidimp"
]

# List of possible Pokemon natures
natures = [
    "Hardy", "Lonely", "Adamant", "Naughty", "Brave", "Bold", "Docile", "Impish", "Lax", "Relaxed", "Modest", "Mild",
    "Bashful", "Rash", "Quiet", "Calm", "Gentle", "Careful", "Quirky", "Sassy", "Timid", "Hasty", "Jolly", "Naive",
    "Serious"
]

generations = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
    8: "VIII"
}


def get_gender(pokemon):
    """
    Determines the gender of a Pokemon.  Has a few checks for genderless, male-only, and female-only species.

    :param pokemon: The Pokemon to determine the gender of.
    :return: The Pokemon's gender.
    """

    pokemon_gender = "N"
    
    if pokemon["NAME"] not in genderless_pokemon:
        if pokemon["NAME"] in male_only_pokemon:
            pokemon_gender = "M"
        elif pokemon["NAME"] in female_only_pokemon:
            pokemon_gender = "F"
        else:
            random_number = random.randint(1, 2)

            if random_number == 1:
                pokemon_gender = "F"
            else:
                pokemon_gender = "M"
                
    return pokemon_gender


def get_ability(pokemon, hidden_ability_chance):
    """
    Determines the Pokemon's ability.

    :param pokemon: The Pokemon to generate an ability for.
    :param hidden_ability_chance: The chance for the Pokemon to have its hidden ability
    :return: A string with the Pokemon's chosen ability
    """
    abilities = pokemon["ABILITY"]

    # If hidden abilities are enabled and the Pokemon has hidden abilities, check to see if this one in particular gets
    # said hidden ability.  Existence of hidden ability is checked by comparing the Pokemon's hidden ability to itself;
    # if both values are identical, then a hidden ability exists.  If not, then it's NaN in the dataframe.
    if hidden_ability_chance > 0 and pokemon["ABILITY HIDDEN"] == pokemon["ABILITY HIDDEN"]:
        random_number = random.randint(1, 100)  # random_number determines whether the Pokemon will have an HA

        if hidden_ability_chance >= random_number:
            abilities = pokemon["ABILITY HIDDEN"]

    # Abilities are represented by a string in the data; this splits them, grabs a random one, and then returns it
    abilities = abilities.split(",")
    random_number = random.randint(0, len(abilities) - 1)

    pokemon_ability = abilities[random_number]

    return pokemon_ability


def get_moves(pokemon, generation, egg_move_chance):
    """
    Cleans up a given move by capitalizing it and removing dahses, and in the case of egg moves, determines if the
    Pokemon should get the move.

    :param move: The move to be assessed
    :param move_details_dataframe: A dataframe containing info on Pokemon moves.  See pokemon_moves_details.csv.
    :param egg_move_chance: The chance, determined by a user, for a Pokemon to have an egg move.
    :return: A string containing the name of the move, or nothing
    """
    species = pokemon.Species.capitalize()
    generation_numeral = generations[generation]
    all_moves = {}
    moves_for_pokemon = []
    egg_moves = []
    regular_moves = []
    egg_move_length = 0
    regular_move_length = 0
    counter = 0

    print(species)
    with open(f"./data/pokemon_moves/{species}.json", "r") as moves_file:
        all_moves = json.load(moves_file)

    valid_moves = all_moves[generation_numeral]
    egg_moves = valid_moves["egg_moves"]
    regular_moves = valid_moves["regular_moves"]

    egg_move_length = len(egg_moves)
    regular_move_length = len(regular_moves)

    total_moves = egg_move_length + regular_move_length
    
    if total_moves <= 4:
        if egg_move_length > 0:
            while len(moves_for_pokemon) < 4 and counter < egg_move_length:
                move = clean_move(egg_moves[counter])
                moves_for_pokemon.append(move)
                counter += 1

        counter = 0

        while len(moves_for_pokemon) < 4 and counter < regular_move_length:
            move = regular_moves[counter]

            if int(move["Level"]) > 1:
                break
            else:
                moves_for_pokemon.append(move["Name"])

            counter += 1
    else:
        counter = 0

        while len(moves_for_pokemon) < 4 and counter < 50:
            will_have_egg_move = random.randint(1, 100)

            if egg_move_length > 0 and will_have_egg_move <= egg_move_chance:
                move_index = random.randint(0, egg_move_length - 1)
                move = clean_move(egg_moves[move_index])

                if move not in moves_for_pokemon:
                    moves_for_pokemon.append(move)
            else:
                move_index = random.randint(0, regular_move_length - 1)
                move = regular_moves[move_index]
                moveName = clean_move(move["Name"])

                if move["Level"] != "N/A" and move["Level"] != "Evo." and int(move["Level"]) == 1 and moveName not in moves_for_pokemon:
                    moves_for_pokemon.append(moveName)

                counter += 1

    pokemon.MoveOne = moves_for_pokemon[0]

    if len(moves_for_pokemon) > 1:
        pokemon.MoveTwo = moves_for_pokemon[1]

    if len(moves_for_pokemon) > 2:
        pokemon.MoveThree = moves_for_pokemon[2]

    if len(moves_for_pokemon) > 3:
        pokemon.MoveFour = moves_for_pokemon[3]


def clean_move(move_name):
    move_to_return = move_name

    move_to_return = move_to_return.replace("*", "")
    move_to_return = move_to_return.replace("‡", "")
    move_to_return = move_to_return.replace("†", "")
    move_to_return = move_to_return.replace("HGSS", "")
    move_to_return = move_to_return.replace("GS", "")
    move_to_return = move_to_return.replace("ORAS", "")
    move_to_return = move_to_return.replace("USUM", "")
    move_to_return = move_to_return.replace("SM", "")
    move_to_return = move_to_return.strip()

    return move_to_return


def generate_pokemon(number_to_generate, generation, egg_move_chance, hidden_ability_chance, shiny_chance):
    # Setting up the output file, data, randomizer, etc.
    output_file = open("./output/output_file.json", "w+")
    output_file.write("[")
    generated_pokemon = []
    loop_counter = 0
    random.seed()

    pokemon_list = pandas.read_csv("./data/pokemon.csv")

    # Dropping Pokemon outside of the generation specified
    pokemon_list = pokemon_list[pokemon_list.GENERATION <= generation]

    # Hidden abilities can only be had from Gen V onward; if it's earlier, we set hidden_ability_chance to 0 regardless
    # of what the user picked
    if hidden_ability_chance > 0 and generation < 5:
        hidden_ability_chance = 0

    while loop_counter < number_to_generate:
        # random_number is used for the random number generation.  Currently represents the Pokemon that will be picked.
        # Re-seeding it every time.
        random_number = random.randint(0, len(pokemon_list.index) - 1)

        pokemon_object = pokemonClass()
        pokemon = pokemon_list.iloc[random_number]
        pokemon_gender = ""
        pokemon_ability = ""
        pokemon_is_shiny = ""
        pokemon_nature = ""
        pokemon_ivs = []
        pokemon_moves = []

        pokemon_object.Species = pokemon["NAME"]
        pokemon_object.Level = 1

        # Get gender
        pokemon_object.Gender = get_gender(pokemon)

        # If the Pokemon can be shiny, make a check to see whether the one being generated will be shiny
        pokemon_object.isShiny = False

        if shiny_chance > 0:
            random_number = random.randint(1, 100)

            if shiny_chance >= random_number:
                pokemon_object.isShiny = True

        # Simple step to determine the Pokemon's nature.
        random_number = random.randint(0, 24)
        pokemon_object.Nature = natures[random_number]

        # Get ability
        pokemon_object.Ability = get_ability(pokemon, hidden_ability_chance)

        # Next, IVs are determined by randomly generating numbers between 1 and 31.
        random_number = random.randint(1, 31)
        pokemon_object.HP = random_number

        random_number = random.randint(1, 31)
        pokemon_object.Atk = random_number

        random_number = random.randint(1, 31)
        pokemon_object.Def = random_number

        random_number = random.randint(1, 31)
        pokemon_object.SpA = random_number

        random_number = random.randint(1, 31)
        pokemon_object.SpD = random_number

        random_number = random.randint(1, 31)
        pokemon_object.Spe = random_number

        # Get moves
        get_moves(pokemon_object, generation, egg_move_chance)

        json.dump(pokemon_object.pokemon_as_dict(), output_file)
        output_file.write(",\n")

        loop_counter += 1

    output_file.write("]")
    output_file.close()


if __name__ == '__main__':
    # Number of pokemon to generate, generation, % chance of egg moves, % chance of hidden abilities, % chance of shiny
    generate_pokemon(10, 7, 50, 50, 100)
