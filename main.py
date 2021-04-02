import pandas
import random

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


def get_gender(pokemon):
    """
    Determines the gender of a Pokemon.  Has a few checks for genderless, male-only, and female-only species.

    :param pokemon: The Pokemon to determine the gender of.
    :return: The Pokemon's gender.
    """

    pokemon_gender = ""
    
    if pokemon["NAME"] not in genderless_pokemon:
        if pokemon["NAME"] in male_only_pokemon:
            pokemon_gender = "(M)"
        elif pokemon["NAME"] in female_only_pokemon:
            pokemon_gender = "(F)"
        else:
            random_number = random.randint(1, 2)

            if random_number == 1:
                pokemon_gender = "(F)"
            else:
                pokemon_gender = "(M)"
                
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


def get_move(move, move_details_dataframe, egg_move_chance):
    """
    Cleans up a given move by capitalizing it and removing dahses, and in the case of egg moves, determines if the
    Pokemon should get the move.

    :param move: The move to be assessed
    :param move_details_dataframe: A dataframe containing info on Pokemon moves.  See pokemon_moves_details.csv.
    :param egg_move_chance: The chance, determined by a user, for a Pokemon to have an egg move.
    :return: A string containing the name of the move, or nothing
    """
    move_to_return = ""

    # If the method a move is learned == 1, then it's a regular move and we don't need any extra checks
    if move["pokemon_move_method_id"] == 1:
        move_details = move_details_dataframe[move_details_dataframe["id"] == move["move_id"]]
        move_to_return = move_details["identifier"].item()

    # If it's an egg move, we may or may not add it, depending on the chance for the Pokemon to have egg move
    else:
        random_number = random.randint(1, 100)

        if egg_move_chance >= random_number:
            move_details = move_details_dataframe[move_details_dataframe["id"] == move["move_id"]]
            move_to_return = move_details["identifier"].item()

    # Cleaning up the moves so they can be imported properly
    if move_to_return != "mud-slap":
        move_to_return = move_to_return.replace("-", " ")

    move_to_return = move_to_return.title()

    return move_to_return


def generate_pokemon(number_to_generate, generation, egg_move_chance, hidden_ability_chance, shiny_chance):
    # Setting up the output file, data, randomizer, etc.
    output_file = open("./output/output_file.txt", "w+")
    loop_counter = 0

    pokemon_list = pandas.read_csv("./data/pokemon.csv")
    pokemon_known_moves = pandas.read_csv("./data/pokemon_moves.csv")
    pokemon_move_details = pandas.read_csv("./data/pokemon_moves_details.csv")

    # Dropping Pokemon outside of the generation specified
    pokemon_list = pokemon_list[pokemon_list.GENERATION <= generation]

    # Hidden abilities can only be had from Gen V onward; if it's earlier, we set hidden_ability_chance to 0 regardless
    # of what the user picked
    hidden_ability_chance = 0

    while loop_counter < number_to_generate:
        # random_number is used for the random number generation.  Currently represents the Pokemon that will be picked.
        # Re-seeding it every time.
        random.seed()
        random_number = random.randint(0, len(pokemon_list.index) - 1)

        pokemon = pokemon_list.iloc[random_number]
        pokemon_gender = ""
        pokemon_ability = ""
        pokemon_is_shiny = ""
        pokemon_nature = ""
        pokemon_ivs = []
        pokemon_moves = []

        # Get gender
        pokemon_gender = get_gender(pokemon)

        # If the Pokemon can be shiny, make a check to see whether the one being generated will be shiny
        if shiny_chance > 0:
            random_number = random.randint(1, 100)

            if shiny_chance >= random_number:
                pokemon_is_shiny = "Shiny: Yes\n"

        # Simple step to determine the Pokemon's nature.
        random_number = random.randint(0, 24)
        pokemon_nature = natures[random_number]

        # Get ability
        pokemon_ability = get_ability(pokemon, hidden_ability_chance)

        # Next, IVs are determined by randomly generating numbers between 1 and 31.
        while len(pokemon_ivs) < 6:
            random_number = random.randint(1, 31)
            pokemon_ivs.append(random_number)

        # Set up the Pokemon's moves -- drop all moves that the Pokemon can't know by level 1, or moves
        # that are taught through anything other than level up, and optionally, egg moves
        move_loop_counter = 0
        moves_for_pokemon = pokemon_known_moves[pokemon_known_moves["pokemon_id"] == pokemon["NUMBER"]]
        moves_for_pokemon = moves_for_pokemon[moves_for_pokemon["level"] < 2]

        if egg_move_chance == 0:
            moves_for_pokemon = moves_for_pokemon[moves_for_pokemon["pokemon_move_method_id"] == 1]

        # If the Pokemon can only know 4 or fewer moves, there's no need to run it through a loop to randomly choose
        if len(moves_for_pokemon) < 4:
            for move in moves_for_pokemon:
                move_to_add = get_move(move, pokemon_move_details, egg_move_chance)

                if move_to_add not in pokemon_moves:
                    pokemon_moves.append(move_to_add)
        else:
            while move_loop_counter < len(moves_for_pokemon.index) - 1 and len(pokemon_moves) < 4:
                random_number = random.randint(0, len(moves_for_pokemon.index) - 1)
                move = moves_for_pokemon.iloc[random_number]

                move_to_add = get_move(move, pokemon_move_details, egg_move_chance)

                if move_to_add not in pokemon_moves:
                    pokemon_moves.append(move_to_add)

                move_loop_counter += 1

        loop_counter += 1

        pokemon_moves_as_string = ""

        for move in pokemon_moves:
            if move != "":
                pokemon_moves_as_string = pokemon_moves_as_string + f"- {move}\n"

        output_file.write(f"{pokemon['NAME']} {pokemon_gender}\n"
                          f"Ability: {pokemon_ability}\n"
                          f"Level: 1\n"
                          f"{pokemon_is_shiny}"
                          f"{pokemon_nature} Nature\n"
                          f"IVs: {pokemon_ivs[0]} HP / {pokemon_ivs[1]} Atk / {pokemon_ivs[2]} Def / {pokemon_ivs[3]} SpA / {pokemon_ivs[4]} SpD / {pokemon_ivs[5]} Spe\n"
                          f"{pokemon_moves_as_string}\n"
                          )

    output_file.close()


if __name__ == '__main__':
    # Number of pokemon to generate, generation, % chance of egg moves, % chance of hidden abilities, % chance of shiny
    generate_pokemon(30, 6, 50, 50, 5)
