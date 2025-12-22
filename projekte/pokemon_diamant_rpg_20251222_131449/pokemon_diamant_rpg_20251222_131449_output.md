# Output: pokemon_diamant_rpg

Here's the complete documentation in Markdown format for the provided code:

---

# Pokemon Abenteuer Game Technical Documentation

## Classes and Interfaces

### Pokemon

#### Attributes

* `name` (str): The name of the Pokemon.
* `typ` (str): The type of the Pokemon.
* `level` (int): The level of the Pokemon.
* `hp` (int): The current hit points of the Pokemon.
* `max_hp` (int): The maximum hit points of the Pokemon.
* `attacks` (list): A list containing the attacks of the Pokemon.
* `xp` (int): Experience points accumulated by the Pokemon.

#### Methods

* `attack(enemy)`: Attacks an enemy with the first attack in the `attacks` list.
* `level_up()`: Increases the level of the Pokemon if it gains enough experience.
* `gain_xp(amount)`: Adds the given amount of experience points to the Pokemon.

### Attack

#### Attributes

* `name` (str): The name of the attack.
* `typ` (str): The type of the attack.
* `damage` (int): The damage caused by the attack.

#### Methods

* Not defined in provided code.

### Player

#### Attributes

* `name` (str): The name of the player.
* `team` (Team): The team owned by the player, containing their Pokemon.
* `position` (tuple): The current position of the player on the game map.
* `money` (int): The amount of money possessed by the player.
* `pokeballs` (int): The number of Pokeballs available to the player.

#### Methods

* `move(x, y)`: Moves the player's position to the given coordinates.
* `throw_pokeball(pokemon)`: Throws a Pokeball at a wild Pokemon in an attempt to capture it.

### GameWorld

#### Attributes

* `canvas` (tkinter.Canvas): The canvas used for displaying the game world.
* `tiles` (list): A 3x3 grid representing the tiles on the game map.
* `npcs` (list): A list of Non-Player Characters present in the game world.
* `wild_pokemon_zones` (dict): A dictionary mapping coordinates to Boolean values, indicating whether a given tile contains wild Pokémon.

#### Methods

* `spawn_wild_pokemon(position)`: Spawns a random wild Pokémon at the specified position if it's within a wild Pokémon zone.
* `is_safe_zone(position)`: Checks whether the given tile is safe to land on, such as grass.

### Battle

#### Attributes

* `player_pokemon` (Pokemon): The player's currently selected Pokemon in battle.
* `enemy_pokemon` (Pokemon): The enemy Pokémon encountered during the current battle.
* `is_trainer_battle` (bool): A flag indicating whether the battle is against a trainer or wild Pokémon.

#### Methods

* `start_battle()`: Starts the battle between the player and the enemy Pokemon.
* `attack_phase()`: Allows the player to attack the enemy Pokemon with their selected Pokemon's attacks.
* `flee_phase()`: Attempts to flee from the battle if the player chooses to do so.
* `swap_pokemon()`: Swaps the player's current Pokemon with another one in their team if the new Pokemon has a higher level than the enemy Pokémon.

### Game

#### Attributes

* `canvas` (tkinter.Canvas): The canvas used for displaying the game world.
* `tiles` (list): A 3x3 grid representing the tiles on the game map.
* `npcs` (list): A list of Non-Player Characters present in the game world.
* `wild_pokemon_zones` (dict): A dictionary mapping coordinates to Boolean values, indicating whether a given tile contains wild Pokémon.

#### Methods

* `start()`: Initializes the game, including spawning the player's starting Pokémon and setting up the game loop.

### Team

#### Attributes

* `name` (str): The name of the team.
* `pokemons` (list): A list containing the Pokemon on the team.

#### Methods

* Not defined in provided code.

## Example Usage

Here's an example usage of the provided code, demonstrating how the classes are connected:

```python
# Initialize the game world and create a new game instance
root = tk.Tk()
canvas = tk.Canvas(root, width=640, height=480)
tiles = [
    ["Grass", "Grass", "Water"],
    ["Water", "Fire", "Electric"],
    ["Grass", "Poison", "Rock"]
]
npcs = []
wild_pokemon_zones = {}
game_world = GameWorld(canvas, tiles, npcs, wild_pokemon_zones)
game = Game(canvas, tiles, npcs, wild_pokemon_zones)

# Start the game
game.start()
```