###################################################################################################
#  Imports: No need to modify these! (These provide us with add-ons; e.g. the time library allows #
#  us to make the game pause for a certain number of seconds.                                     #
#                                                                                                 #
#  Make sure to run the following in the terminal:                                                #
#    - pip install requests                                                                       #
#    - pip install urllib3                                                                        #
#    - pip install pytest                                                                         #
###################################################################################################
import json
import pygame
from pygame.locals import *
import pokeapi
import io
import math
import random
import requests
import time
from urllib.request import urlopen

pygame.init()

# Creating the game window
GAME_WIDTH = 500
GAME_HEIGHT = 500
SIZE = (GAME_WIDTH, GAME_HEIGHT)
game = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Pokemon Battle")

# COLORS
BLACK = (0, 0, 0)
GOLD = (218, 165, 32)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)


class Move:
    def __init__(self, url):
        # Gets the information about the provided move (from the url)
        req = requests.get(url)
        self.move_data = req.json()

        # Get the name, power, and type

        # Uncomment these if you want to see
        # json_object = json.dumps(self.move_data, indent=4)
        # with open("move_data.json", "w") as outfile:
        #     outfile.write(json_object)

        self.name = self.move_data["name"]
        self.power = self.move_data["power"]
        self.type = self.move_data["type"]["name"]


class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name: str, level: int, x: int, y: int):
        """
        Initializing the pokemon class
        """
        pygame.sprite.Sprite.__init__(self)
        # Let's use these parameter names

        # Set the name, level, x, and y coordinates of the Pokemon from the
        # parameters passed into the __init__ function.
        self.name = None
        self.level = 0
        self.x = 0
        self.y = 0
        self.name = name
        self.level = level
        self.x = x
        self.y = y

        # Set the initial number of potions that the Pokemon starts out with
        self.num_potions = 0
        self.num_potions = 3

        # Set the pokemon_data
        self.pokemon_data = None
        self.pokemon_data = pokeapi.get_pokemon_data(name.lower())

        # Set the stats/health points about the pokemon
        self.current_hp = 0
        self.max_hp = 0
        self.attack = 0
        self.defense = 0
        self.speed = 0

        # Hint: Get access to all the stats from the pokemon_data
        stats = self.pokemon_data.get("stats")
        for stat in stats:
            if stat["stat"]["name"] == "hp":
                self.current_hp = stat["base_stat"] + self.level
                self.max_hp = stat["base_stat"] + self.level
            elif stat["stat"]["name"] == "attack":
                self.attack = stat["base_stat"]
            elif stat["stat"]["name"] == "defense":
                self.defense = stat["base_stat"]
            elif stat["stat"]["name"] == "speed":
                self.speed = stat["base_stat"]

        # Set the types that this pokemon can have
        # Hint: Get access to all the types from the pokemon_data
        self.types = []
        for i in range(len(self.pokemon_data["types"])):
            type = self.pokemon_data["types"][i]
            type_name = type["type"]["name"]
            self.types.append(type_name)

        # Size of the pokemon
        self.size = 150

        # Set the default sprite of the pokemon to be
        # the front facing sprite ("front_default")
        # - Hint: use the set_sprite() function
        self.set_sprite("front_default")

    def set_sprite(self, sprite_choice):
        """
        Choose the sprite to display for the pokemon.

        Side specifies the type for the sprite. We only allow the following options:
        - "back_default"
        - "back_female"
        - "back_shiny"
        - "back_shiny_female"
        - "front_default"
        - "front_female"
        - "front_shiny"
        - "front_shiny_female"

        WARNING: Not all pokemon have female sprites, so double check.
        """
        # Safety check to make sure we only use a valid sprite choice
        allowed_sprites = {"back_default", "back_female", "back_shiny", "back_shiny_female", "front_default", "front_female", "front_shiny", "front_shiny_female"}
        assert sprite_choice in allowed_sprites, f"Make sure to use a valid sprite choice in set_sprite()!\n{sprite_choice} is not valid!\nValid options are: {allowed_sprites}"

        # TODO Get the sprite choice's URL from the pokemon_data
        print("TODO get the sprite image! (delete this message and the return once you do)")
        image = "TODO"
        return # delete this line once start this section

        # This makes it so Pygame can use the image and then display it!
        image_stream = urlopen(image).read()
        image_file = io.BytesIO(image_stream)
        self.image = pygame.image.load(image_file).convert_alpha()

        # Scales the image accordingly
        scale = self.size / self.image.get_width()
        new_width = self.image.get_width() * scale
        new_height = self.image.get_height() * scale
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

    def draw(self, alpha=255):
        """
        Draws the pokemon based on the sprite image you set.

        Note: Alpha here ranges from 0 to 255 to represent the
        transparency. 0 being invisible and 255 being visible.
        https://www.pygame.org/docs/ref/color.html
        """
        sprite = self.image.copy()
        rgba_color_value = (255, 255, 255, alpha)
        sprite.fill(rgba_color_value, None, BLEND_RGBA_MULT)
        game.blit(sprite, (self.x, self.y))

    def get_rect(self):
        """
        Get the rectangular area of the Surface.
        https://www.pygame.org/docs/ref/surface.html#pygame.Surface.get_rect
        """
        return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def set_moves(self):
        """
        Set the moves of the pokemon. Provided code, no need to add anything here!
        """
        self.moves = []

        # go through all moves from the api
        for i in range(len(self.pokemon_data["moves"])):
            # get move from different game versions
            versions = self.pokemon_data["moves"][i]["version_group_details"]
            for j in range(len(versions)):
                version = versions[j]

                # only use moves from red-blue version
                if version["version_group"]["name"] != "red-blue":
                    continue

                # only get moves that can be learned from levlling up
                learn_method = version["move_learn_method"]["name"]
                if learn_method != "level-up":
                    continue

                # add the move to the options if the pokemon has a high enough level
                level_learned = version["level_learned_at"]
                if self.level >= level_learned:
                    move = Move(self.pokemon_data["moves"][i]["move"]["url"])

                    # only include attack moves
                    if move.power is not None:
                        self.moves.append(move)

    def draw_hp(self):
        """
        Draws the healthbar for each pokemon. Provided code :)
        """
        bar_scale = 200 // self.max_hp

        # Draw the red part
        for i in range(self.max_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(game, RED, bar)

        # Draw the green part (current hp)
        for i in range(self.current_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(game, GREEN, bar)

        # Text for HP
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(
            f"{self.name} HP: {self.current_hp} / {self.max_hp}", True, BLACK
        )
        text_rect = text.get_rect()
        text_rect.x = self.hp_x
        text_rect.y = self.hp_y + 30
        game.blit(text, text_rect)

    def use_potion(self):
        """
        Called when player uses a potion.
        Check if there are any potions left, if the player
        has potions left, then add 30 hp (make sure not to go
        over the max hp!)

        Then decrease the number of potions left
        """
        print("Implement the function to use_potion()")
        pass

    def perform_attack(self, other_pokemon, move):
        display_message(f"TODO list the move that the pokemon made!")

        # Calculate the damage
        damage = (2 * self.level + 10) / 250 * self.attack / other_pokemon.defense * move.power

        # Same type attack bonus
        # If the pokemon has the same type as the type of the move, then
        # let's increase the damage done (e.g. double damage *= 2)

        # Critical hit
        # TODO make it so there's a chance (you can determine the percentage)
        # that the damage will be doubled

        # Round down the damage to a whole number
        damage = math.floor(damage)
        # Make it so the other pokemon takes damage.
        other_pokemon.take_damage(damage)

    def take_damage(self, damage_amount: int):
        """
        Make it so the pokemon takes the specified damage.
        Decrease the current_hp (self.current_hp)
        """
        # Subtract the damage_amount from the current_hp
        # Make sure that the hp doesn't go below 0!
        print("TODO: Implement take_damage()!")
        pass

def display_message(message: str):
    # drawing box with border
    pygame.draw.rect(game, WHITE, (10, 350, 480, 140))
    pygame.draw.rect(game, BLACK, (10, 350, 480, 140), 3)

    # display the message
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect()
    text_rect.x = 30
    text_rect.y = 410
    game.blit(text, text_rect)
    pygame.display.update()


def create_button(width, height, x, y, text_center_x, text_center_y, button_text):
    mouse_cursor = pygame.mouse.get_pos()

    button = Rect(x, y, width, height)

    # highlight the button the mouse is pointing to
    if button.collidepoint(mouse_cursor):
        pygame.draw.rect(game, GOLD, button)
    else:
        pygame.draw.rect(game, WHITE, button)

    # adding button_text to the button
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render(f"{button_text}", True, BLACK)
    text_rect = text.get_rect(center=(text_center_x, text_center_y))
    game.blit(text, text_rect)
    return button

# Starter pokemon
player_pokemon = None  # leave this as None
rival_pokemon = None  # leave this as None

# level of the pokemon
level = 30

# Choose up to 6 pokemon that they player can choose
# e.g. pikachu = Pokemon("Pikachu", level, x_coord, y_coord)
bulbasaur = Pokemon("Bulbasaur", level, 25, 150)
charmander = Pokemon("Charmander", level, 175, 150)
squirtle = Pokemon("Squirtle", level, 325, 150)
pikachu = Pokemon("Pikachu", level, 25, 0)

# Then put the pokemon variables in this list
starter_pokemon = []
# e.g. starter_pokemon = [pokemon1, pokemon2, pokemon3]
starter_pokemon = [bulbasaur, charmander, squirtle, pikachu]

# Pygame event loop
game_status = "select pokemon"
move_buttons = []

while game_status != "quit":
    for event in pygame.event.get():
        if event.type == QUIT:
            game_status = "quit"

        # If a key is pressed
        if event.type == KEYDOWN:
            print(f"{event.key} was pressed!")

        # If the mouse button is pressed
        if event.type == MOUSEBUTTONDOWN:
            mouse_cursor = pygame.mouse.get_pos()
            print(f"mouse pressed at {mouse_cursor}!")

            # Selecting Your Pokemon:
            if game_status == "select pokemon":
                pass

            # Player turn: check if the player
            # selected the fight or use potion button
            elif game_status == "player turn":
                # Check if fight button was clicked, if so make it the player's move

                # Check if the potion button was clicked
                if potion_button.collidepoint(mouse_cursor):
                    # Force the player to attack if there are no more potions -> player move
                    # If the player does have potions, then have them use the potion and make it the opponents turn
                    pass
            # Player move: or selecting an attack move
            elif game_status == "player move":
                pass

    # Displaying the pokemon select screen
    if game_status == "select pokemon":
        game.fill(WHITE)

        # Draw the starter pokemon (hint pokemon_variable.draw())

        # Draw box around the pokemon
        # - Get the position of the mouse
        # - Go through all of the starter pokemon (hint the list we made might be useful!)
        #   - if the position of the mouse is in the pokemon's box (hint: we can use collidepoint()),
        #     then let's draw an outline around the pokemon

        # Use display_message to share a select a pokemon message
        display_message("Select a pokemon!")

    # Displaying the prebattle screen
    if game_status == "prebattle":
        game.fill(WHITE)
        # Draw the player and rival pokemon
        # TODO

        # Set the moves of the player and rival pokemon
        # (hint, call the set_moves() function!)
        # TODO

        # Reposition the pokemon/ make them larger for battle!
        # player_pokemon.x = -50
        # player_pokemon.y = 100
        # rival_pokemon.x = 250
        # rival_pokemon.y = -50
        # player_pokemon.size = 300
        # rival_pokemon.size = 300

        # Consider changing the image (set_sprite) so the rival pokemon
        # faces forward and our pokemon faces them (backwards)

        display_message(f"Prebattle, add a custom message!")
        pygame.display.update()

    # The start of the battle
    if game_status == "start battle":
        # Either make it so the pokemon appear (instantly or via animation!)
        pass

        # Draw the health point bars
        pygame.display.update()

    # Battle!
    if game_status == "battle":
        game.fill(WHITE)
        # Draw the pokemon and the health bars (draw_hp)
        display_message(f"Battle!")
        pygame.display.update()

        # Determine who goes first
        # - can do this pased on who has the greater speed, level, or randomly!
        # if the opponent goes first, then set game_status = "opponent turn"
        # if we (the player) goes first, then set game_status = "player turn"

    # Our opponents turn
    if game_status == "opponent turn":
        game.fill(WHITE)
        player_pokemon.draw()
        rival_pokemon.draw()
        player_pokemon.draw_hp()
        rival_pokemon.draw_hp()
        display_message(f"Rival's turn!")
        pygame.display.update()

    # Our turn!
    if game_status == "player turn":
        game.fill(WHITE)

        # Create the potion and fight buttons
        # TODO
        pygame.draw.rect(game, BLACK, (10, 350, 480, 140), 3)
        pygame.display.update()

    if game_status == "player move":
        game.fill(WHITE)

        move_buttons = []
        # Create a button for each move

        # Draw a black border
        pygame.draw.rect(game, BLACK, (10, 350, 480, 140), 3)
        pygame.display.update()

    if game_status == "opponent turn":
        game.fill(WHITE)

        # Check if the rival pokemon was defeated
        pygame.display.update()
        time.sleep(2)

    # When one of the pokemon are defeated, we'll have them "faint"
    if game_status == "fainted":
        # Set the game_status to gameover
        pass

    if game_status == "gameover":
        display_message("TODO ask the user if they want to play again")

    pygame.display.update()

pygame.quit()
