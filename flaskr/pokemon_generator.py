import pandas
import random
import json
from flaskr import pokemon

PokemonClass = pokemon.Pokemon

# The following arrays hold various information that impose further restrictions on Pokemon genders
genderless_pokemon = [
    "Arctovish", "Arctozolt", "Baltoy", "Beldum", "Bronzor", "Carbink", "Cryogonal", "Dhelmise", "Dracovish",
    "Dracozolt", "Falinks", "Golett", "Klink", "Lunatone", "Magnemite", "Minior", "Polteageist", "Porygon", "Rotom",
    "Solrock", "Staryu", "Unknown", "Voltorb"
]

female_only_pokemon = [
    "Nidoran F", "Illumise", "Happiny", "Kangaskhan", "Smoochum", "Miltank", "Petilil", "Vullaby", "Flabébé",
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
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
}


def get_gender(pokemon_object):
    """
    Determines the gender of a Pokemon.  Has a few checks for genderless, male-only, and female-only species.

    :param pokemon_object: The Pokemon to determine the gender of.
    :return: The Pokemon's gender.
    """

    pokemon_gender = "N"

    if pokemon_object["NAME"] not in genderless_pokemon:
        if pokemon_object["NAME"] in male_only_pokemon:
            pokemon_gender = "M"
        elif pokemon_object["NAME"] in female_only_pokemon:
            pokemon_gender = "F"
        else:
            random_number = random.randint(1, 2)

            if random_number == 1:
                pokemon_gender = "F"
            else:
                pokemon_gender = "M"

    return pokemon_gender


def get_ability(pokemon_object, hidden_ability_chance):
    """
    Determines the Pokemon's ability.

    :param pokemon_object: The Pokemon to generate an ability for.
    :param hidden_ability_chance: The chance for the Pokemon to have its hidden ability
    :return: A string with the Pokemon's chosen ability
    """
    abilities = pokemon_object["ABILITY"]

    # If hidden abilities are enabled and the Pokemon has hidden abilities, check to see if this one in particular gets
    # said hidden ability.  Existence of hidden ability is checked by comparing the Pokemon's hidden ability to itself;
    # if both values are identical, then a hidden ability exists.  If not, then it's NaN in the dataframe.
    if hidden_ability_chance > 0 and pokemon_object["ABILITY HIDDEN"] == pokemon_object["ABILITY HIDDEN"]:
        random_number = random.randint(1, 100)  # random_number determines whether the Pokemon will have an HA

        if hidden_ability_chance >= random_number:
            abilities = pokemon_object["ABILITY HIDDEN"]

    # Abilities are represented by a string in the data; this splits them, grabs a random one, and then returns it
    abilities = abilities.split(",")
    random_number = random.randint(0, len(abilities) - 1)

    pokemon_ability = abilities[random_number]

    return pokemon_ability


def get_moves(pokemon_object, generation, egg_move_chance):
    """
    Cleans up a given move by capitalizing it and removing dahses, and in the case of egg moves, determines if the
    Pokemon should get the move.

    :param pokemon_object: The object containing info for the Pokemon being created
    :param generation: The generation the Pokemon is being created for.
    :param egg_move_chance: The chance, determined by a user, for a Pokemon to have an egg move.
    """
    all_moves = {}
    moves_for_pokemon = []
    egg_moves = []
    regular_moves = []
    egg_move_length = 0
    regular_move_length = 0
    counter = 0

    species = pokemon_object.Species.capitalize()
    generation_numeral = generations[generation]

    # Get the Pokemon's moveset data
    with open(f"flaskr/data/pokemon_moves/{species}.json", "r") as moves_file:
        all_moves = json.load(moves_file)

    # Split up the moveset into egg moves and regular moves, targeting the generation the Pokemon is being created for
    egg_moves = all_moves[generation_numeral]["egg_moves"]
    regular_moves = all_moves[generation_numeral]["regular_moves"]

    # Get the number of egg moves and regular moves, and the total
    egg_move_length = len(egg_moves)
    regular_move_length = len(regular_moves)
    total_moves = egg_move_length + regular_move_length

    # If the Pokemon can know less than four moves, there's no point in randomizing
    if total_moves <= 4:
        if egg_move_length > 0:
            while len(moves_for_pokemon) < 4 and counter < egg_move_length:
                move = clean_move(egg_moves[counter])
                moves_for_pokemon.append(move)
                counter += 1

        counter = 0

        while len(moves_for_pokemon) < 4 and counter < regular_move_length:
            move = regular_moves[counter]

            # Since moves are ordered by when a Pokemon learns them, the loop is broken purposefully once the level of
            # of the incoming moves exceeds 1
            if int(move["Level"]) > 1:
                break
            else:
                moves_for_pokemon.append(move["Name"])

            counter += 1
    else:
        counter = 0

        while len(moves_for_pokemon) < 4 and counter < 50:
            will_have_egg_move = random.randint(1, 100)

            # See if the Pokemon will have an egg move.  If it will, grab a random one from the list and add it to the
            # moveset
            if egg_move_length > 0 and will_have_egg_move <= egg_move_chance:
                move_index = random.randint(0, egg_move_length - 1)
                move = clean_move(egg_moves[move_index])

                if move not in moves_for_pokemon:
                    moves_for_pokemon.append(move)
            # Randomly select a regular move that the Pokemon learns at level 1.  Some checks are in place to handle odd
            # case where level is assigned as N/A, Evo., etc.
            else:
                move_index = random.randint(0, regular_move_length - 1)
                move = regular_moves[move_index]
                moveName = clean_move(move["Name"])

                if move["Level"] != "N/A" and move["Level"] != "Evo." and int(
                        move["Level"]) == 1 and moveName not in moves_for_pokemon:
                    moves_for_pokemon.append(moveName)

                counter += 1

    # Add the moves to the pokemon object
    if len(moves_for_pokemon) > 0:
        pokemon_object.MoveOne = moves_for_pokemon[0]

    if len(moves_for_pokemon) > 1:
        pokemon_object.MoveTwo = moves_for_pokemon[1]

    if len(moves_for_pokemon) > 2:
        pokemon_object.MoveThree = moves_for_pokemon[2]

    if len(moves_for_pokemon) > 3:
        pokemon_object.MoveFour = moves_for_pokemon[3]


def clean_move(move_name):
    """
    Remove special characters, trailing whitespace, and certain strings from the moves

    :param move_name: The cleaned move name
    :return:
    """
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
    """
    Generates a series of Pokemon in JSON format, which are written to the output_file

    :param number_to_generate: Number of Pokemon to generate
    :param generation:  The generation of games the Pokemon are from
    :param egg_move_chance: The chance of a Pokemon having an egg move
    :param hidden_ability_chance: The chance of a Pokemon having its hidden ability
    :param shiny_chance: The chance of a Pokemon being shiny
    :return:
    """
    # Setting up the output file, data, randomizer, etc.
    output_string = "["
    loop_counter = 0
    random.seed()

    # Get Pokemon from the specified generation
    pokemon_list = pandas.read_csv("flaskr/data/pokemon.csv")
    pokemon_list = pokemon_list[pokemon_list.GENERATION <= generation]

    # Hidden abilities can only be had from Gen V onward; if it's earlier, we set hidden_ability_chance to 0 regardless
    # of what the user picked
    if hidden_ability_chance > 0 and generation < 5:
        hidden_ability_chance = 0

    while loop_counter < number_to_generate:
        # random_number is used for the random number generation.  Currently represents the Pokemon that will be picked.
        # Re-seeding it every time.
        random_number = random.randint(0, len(pokemon_list.index) - 1)

        # Instantiate the Pokemon object that will hold all the data about the Pokemon
        pokemon_object = PokemonClass()

        # Get the Pokemon's species, set it on the object, along with its level
        pokemon = pokemon_list.iloc[random_number]
        pokemon_object.Species = pokemon["NAME"]
        pokemon_object.Level = 1

        # Get gender
        pokemon_object.Gender = get_gender(pokemon)

        # If the Pokemon can be shiny, make a check to see whether the one being generated will be shiny
        pokemon_object.isShiny = "false"

        if shiny_chance > 0:
            random_number = random.randint(1, 100)

            if shiny_chance >= random_number:
                pokemon_object.isShiny = "true"

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

        # Convert Pokemon object to a dict, and use it to dump a JSON string to the output_file
        output_string = output_string + pokemon_object.pokemon_as_dict().__str__()
        output_string = output_string + ","

        loop_counter += 1

    output_string = output_string + "]"
    return output_string


if __name__ == '__main__':
    # Number of pokemon to generate, generation, % chance of egg moves, % chance of hidden abilities, % chance of shiny
    print(generate_pokemon(10, 7, 50, 50, 100))
