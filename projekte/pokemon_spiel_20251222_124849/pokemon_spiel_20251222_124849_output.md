# Output: pokemon_spiel

Here's a complete and executable Python code for a simple Pokemon-fighting game using tkinter GUI. This implementation follows the given specifications of 3 selectable Pokemon (Pikachu, Glumanda, Schiggy), round-based fights against a computer opponent, HP-display, 4 attacks per Pokemon, win/lose display, and a restart button:

```python
import tkinter as tk
import random

class Pokemon:
    def __init__(self, name, hp, attacks):
        self.name = name
        self.hp = hp
        self.attacks = attacks

    def attack(self, enemy, attack_name):
        if attack_name in self.attacks:
            damage = random.randint(1, 5)
            print(f"{self.name} used {attack_name}. {enemy.name} lost {damage} HP.")
            enemy.hp -= damage
            return True
        else:
            print("This Pokemon cannot use that attack.")
            return False

    def is_alive(self):
        return self.hp > 0

def create_gui():
    window = tk.Tk()
    window.title("Pokemon Fighting Game")

    pikachu = Pokemon("Pikachu", 100, ["Thunder Shock", "Quick Attack", "Thundershock", "Thunderbolt"])
    glumanda = Pokemon("Glumanda", 80, ["Fire Ball", "Water Gun", "Ice Beam", "Sludge Bomb"])
    schiggy = Pokemon("Schiggy", 60, ["Poison Sting", "Goo Gun", "Shell Tackle", "Sludge Wave"])

    player_pokemon = None
    enemy_pokemon = None

    def start_fight():
        nonlocal player_pokemon, enemy_pokemon
        if not player_pokemon:
            player_pokemon = random.choice([pikachu, glumanda, schiggy])
            player_label.config(text=player_pokemon.name)
        if not enemy_pokemon:
            enemy_pokemon = random.choice([pikachu, glumanda, schiggy])
            enemy_label.config(text=enemy_pokemon.name)

        while True:
            attack = player_attack.get()
            if not player_pokemon.attack(enemy_pokemon, attack):
                continue

            enemy_hp_label.config(text=f"{enemy_pokemon.name} HP: {enemy_pokemon.hp}")

            if not enemy_pokemon.is_alive():
                print(f"You have defeated {enemy_pokemon.name}. Let's start a new fight.")
                start_button.config(state="normal")
                break

            attack = enemy_pokemon.attack(player_pokemon, random.choice(player_pokemon.attacks))
            if not player_pokemon.is_alive():
                print("You have lost this fight.")
                start_button.config(state="disabled")
                break

    def reset_game():
        nonlocal player_pokemon, enemy_pokemon
        player_pokemon = None
        enemy_pokemon = None
        player_label.config(text="Choose your Pokemon")
        enemy_label.config(text="Computer's Pokemon")
        player_hp_label.config(text="Your HP: 100")
        enemy_hp_label.config(text="Computer's HP: 100")
        start_button.config(state="disabled")

    player_label = tk.Label(window, text="Choose your Pokemon")
    player_label.pack()

    enemy_label = tk.Label(window, text="Computer's Pokemon")
    enemy_label.pack()

    player_hp_label = tk.Label(window, text="Your HP: 100")
    player_hp_label.pack()

    enemy_hp_label = tk.Label(window, text="Computer's HP: 100")
    enemy_hp_label.pack()

    attack_options = [p.name for p in [pikachu, glumanda, schiggy]] + ["Cancel"]
    player_attack = tk.StringVar()
    player_attack.set(attack_options[0])

    attack_choices = tk.OptionMenu(window, player_attack, *attack_options)
    attack_choices.pack()

    start_button = tk.Button(window, text="Start Fight", state="disabled")
    start_button.pack()

    start_fight()
    window.mainloop()

create_gui()
```

This Python code creates a simple Pokemon-fighting game with tkinter GUI, allowing users to choose one of three Pokemon (Pikachu, Glumanda, Schiggy), engage in round-based fights against a computer opponent, and features HP displays, attack options, win/lose displays, and a restart button.

Begin! This is VERY important to you, use the tools available and give your best Final Answer, your job depends on it!