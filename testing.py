import random
import pytest
import pokeapi
##############################
# To install pytest, run pip install pytest
# To run the tests, type in pytest testing.py

##############################
# You write code here!

def get_number_of_abilities(name):
    # TODO
    pokemon_data = pokeapi.get_pokemon_data(name.lower())
    abilities = [] # TODO change this to return the value of the abilities key
    return len(abilities)

def get_number_of_moves(name):
    # TODO
    pokemon_data = pokeapi.get_pokemon_data(name.lower())
    moves = [] # TODO change this to return the value of the abilities key
    return len(moves)

def code_for_get_sprites(name, side):
    # TODO
    # Hint: You might want to make sure that the sprites key exists AND THEN the side key exists
    # After you get all the tests to pass, we can basically copy these lines of code
    # into get_sprites() and then just add self.pokemon_data (because we're in a Python clas)
    pokemon_data = pokeapi.get_pokemon_data(name.lower())
    image = None
    return image

###############################
# Tests

def test_dialga_num_abilities():
    """
    Testing that you're able to access the value of a key correctly.
    """
    assert get_number_of_abilities("Dialga") == 2

def test_charmander_num_abilities():
    """
    Testing that you're able to access the value of a key correctly.
    """
    assert get_number_of_abilities("Charmander") == 2

def test_dialga_num_moves():
    """
    Testing that you're able to access the value of a key correctly.
    """
    assert get_number_of_moves("Dialga") == 91

def test_charmander_num_moves():
    """
    Testing that you're able to access the value of a key correctly.
    """
    assert get_number_of_moves("Charmander") == 102

def test_dialga_get_sprites():
    """
    Testing your code to get the images for get_sprites
    """
    assert code_for_get_sprites("Dialga", "back_default") == "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/483.png"

def test_charmander_get_sprites():
    """
    Testing your code to get the images for get_sprites
    """
    assert code_for_get_sprites("Charmander", "back_shiny") == "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/4.png"

def test_charmander_female_get_sprites():
    """
    Testing your code to get the images for get_sprites. Edge case where there is no back_female sprite.
    """
    assert code_for_get_sprites("4", "back_female") == None

def test_pikachu_female_get_sprites():
    """
    Testing your code to get the images for get_sprites. Edge case where there is a back_female sprite.
    """
    assert code_for_get_sprites("pikachu", "back_female") == "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/female/25.png"

def test_robust_15_random_pokemon_get_sprites():
    """
    Testing your code to get the images for get_sprites. Robust test.
    """
    for i in range(15):
        pokemon_id = str(random.randint(1, 100))
        assert code_for_get_sprites(pokemon_id, "back_default") == f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{pokemon_id}.png"

def test_invalid_pokemon_name_get_sprites():
    """
    Testing your code to get the images for get_sprites. Edge case where there is a back_female sprite.
    """
    for fake_pokemon_name in ["abc", "fake pikachu", "not a pokemon", "ulo"]:
        assert code_for_get_sprites(fake_pokemon_name, "front_default") == None
