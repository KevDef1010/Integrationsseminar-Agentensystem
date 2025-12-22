# Output: pokemon_multi_task

"""
Pokemon Abenteuer - Ein Pokemon-Diamant inspiriertes RPG
=========================================================
Generiert durch Multi-Agent System
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
from typing import List, Optional



# ============================================================
# TASK_1_DATA_MODELS
# ============================================================

import random

class Attack:
    def __init__(self, name: str, typ: str, damage: int):
        self.name = name
        self.typ = typ
        self.damage = damage

class Pokemon:
    def __init__(self, name: str, typ: str, level: int, max_hp: int, attacks: list):
        self.name = name
        self.typ = typ
        self.level = level
        self.hp = max_hp
        self.max_hp = max_hp
        self.attacks = attacks
        self.xp = 0
    
    def take_damage(self, damage: int) -> int:
        self.hp -= damage
        return self.hp
    
    def attack(self, target, attack_index: int):
        attack = self.attacks[attack_index]
        
        if attack.typ == 'Feuer':
            if target.typ == 'Pflanze':
                damage *= 1.5
        elif attack.typ == 'Wasser':
            if target.typ == 'Feuer':
                damage *= 1.5
        
        return self.take_damage(damage)
    
    def gain_xp(self, amount: int):
        self.xp += amount
        while self.xp >= self.level * 50:
            self.level_up()
            self.max_hp += 5
            self.attacks[0].damage += 2
        
    def level_up(self):
        self.level += 1
    
    def is_fainted(self) -> bool:
        return self.hp <= 0
    
    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)

class Player:
    def __init__(self, name: str):
        self.name = name
        self.team: List[Pokemon] = []
        self.position = [200, 200] # x, y auf Canvas
        self.money = 500
        self.pokeballs = 10
        self.badges = 0
    
    def add_pokemon(self, pokemon: Pokemon) -> bool:
        if len(self.team) < 6:
            self.team.append(pokemon)
            return True
        else:
            return False
    
    def get_active_pokemon(self) -> Pokemon:
        for pokemon in self.team:
            if not pokemon.is_fainted():
                return pokemon
        return None
    
    def has_usable_pokemon(self) -> bool:
        for pokemon in self.team:
            if not pokemon.is_fainted():
                return True
        return False
    
    def move(self, dx: int, dy: int, world_width: int, world_height: int):
        self.position[0] += dx
        self.position[1] += dy
        
        if self.position[0] > world_width:
            self.position[0] = world_width - 1
        elif self.position[0] < 0:
            self.position[0] = 0
            
        if self.position[1] > world_height:
            self.position[1] = world_height - 1
        elif self.position[1] < 0:
            self.position[1] = 0
        
        return self.position
    
class Trainer:
    def __init__(self, name: str, team: List[Pokemon], position: tuple, reward: int):
        self.name = name
        self.team = team
        self.position = position
        self.reward = reward
        self.defeated = False


# ============================================================
# TASK_2_BATTLE_SYSTEM
# ============================================================

import tkinter as tk
from tkinter import messagebox
import random

class BattleSystem:
    '''Rundenbasiertes Pokemon-Kampfsystem.'''
    
    def __init__(self, master: tk.Tk, player, enemy_pokemon, 
                 is_trainer_battle: bool = False, trainer_name: str = None,
                 on_battle_end=None):
        self.master = master
        self.player = player
        self.player_pokemon = player.get_active_pokemon()
        self.enemy_pokemon = enemy_pokemon
        self.is_trainer_battle = is_trainer_battle
        self.trainer_name = trainer_name
        self.on_battle_end = on_battle_end  # Callback wenn Kampf endet
        
        self.battle_frame = tk.Frame(master, bg='lightgray')
        self.create_battle_ui()
        
    def create_battle_ui(self):
        '''Erstellt das Kampf-UI.'''
        # Oben: Gegner-Pokemon mit HP-Balken
        # Mitte: Kampf-Log (Text-Widget)
        # Unten links: Eigenes Pokemon mit HP-Balken
        # Unten rechts: 4 Attacken-Buttons + Flucht-Button + Pokeball-Button
        
    def create_hp_bar(self, parent, pokemon, is_enemy: bool) -> tk.Frame:
        '''Erstellt HP-Anzeige mit farbigem Balken.'''
        # Gruen > 50%, Gelb > 20%, Rot <= 20%
        
    def update_hp_bars(self):
        '''Aktualisiert beide HP-Balken.'''
        
    def player_attack(self, attack_index: int):
        '''Spieler greift an, dann Gegner.'''
        # 1. Spieler-Attacke ausfuehren
        # 2. Schaden berechnen mit Typen-Effektivitaet
        # 3. HP-Balken updaten
        # 4. Pruefen ob Gegner besiegt
        # 5. Wenn nicht: Gegner greift an
        # 6. Pruefen ob eigenes Pokemon besiegt
        
    def enemy_turn(self):
        '''Gegner waehlt zufaellige Attacke.'''
        
    def try_catch(self):
        '''Versucht wildes Pokemon zu fangen.'''
        # Nur bei wilden Pokemon
        # Fangchance: (1 - hp/max_hp) * 0.4 + 0.1
        # Bei Erfolg: Pokemon zum Team hinzufuegen
        
    def try_flee(self):
        '''Versucht zu fliehen.'''
        # 60% Chance bei wilden Pokemon
        # 0% bei Trainer-Kaempfen
        
    def end_battle(self, victory: bool):
        '''Beendet den Kampf und gibt XP/Geld.'''
        # Bei Sieg: XP = gegner_level * 15
        # Bei Trainer-Sieg: Geld = trainer.reward
        
    def show(self):
        '''Zeigt Battle-Frame an.'''
        self.battle_frame.pack(fill='both', expand=True)
        
    def hide(self):
        '''Versteckt Battle-Frame.'''
        self.battle_frame.pack_forget()


# ============================================================
# TASK_3_GAME_WORLD
# ============================================================

import tkinter as tk
import random

class GameWorld:
    '''The game world with map, movement, and encounters.'''
    
    # Tile types
    TILE_GRASS = 0      # Green grass (wild pokemon possible)
    TILE_PATH = 1       # Brown path (safe)
    TILE_WATER = 2      # Blue water (not passable)
    TILE_TOWN = 3       # Grey town (safe)
    
    TILE_SIZE = 32
    
    def __init__(self, master: tk.Tk, player, on_wild_encounter=None, on_trainer_encounter=None):
        self.master = master
        self.player = player
        self.on_wild_encounter = on_wild_encounter
        self.on_trainer_encounter = on_trainer_encounter
        
        self.world_frame = tk.Frame(master)
        
        # Map: 15x12 tiles = 480x384 pixels
        self.map_width = 15
        self.map_height = 12
        
        # Create the map (2D array)
        self.create_map()
        
        # Trainers on the map
        self.trainers = self.create_trainers()
        
        # Canvas for the world
        self.canvas = tk.Canvas(
            self.world_frame, 
            width=self.map_width * self.TILE_SIZE,
            height=self.map_height * self.TILE_SIZE,
            bg='darkgreen'
        )
        self.canvas.pack()
        
        # HUD above
        self.create_hud()
        
        # Keyboard bindings
        self.master.bind('<KeyPress>', self.on_key_press)
        
        # Player sprite
        self.player_sprite = None
        
    def create_map(self):
        '''Creates the game map.'''
        # Create 2D array with tile types
        # Left: Town (TILE_TOWN)
        # Middle: Path with grass around it (Route 1)
        # Right: More grass (Route 2)
        
    def create_trainers(self) -> list:
        '''Creates NPC trainers on the map.'''
        # 2-3 trainers with 2-3 pokemon each
        return []
    
    def create_hud(self):
        '''Creates Heads-Up-Display.'''
        # Shows: Player name, money, pokeballs, team status
        
    def draw_world(self):
        '''Draws the entire world.'''
        self.canvas.delete('all')
        # Draw all tiles
        # Draw trainers
        # Draw player
        
    def draw_tile(self, x: int, y: int, tile_type: int):
        '''Draws a single tile.'''
        colors = {
            self.TILE_GRASS: '#228B22',   # Forest green
            self.TILE_PATH: '#8B4513',    # Brown
            self.TILE_WATER: '#1E90FF',   # Blue
            self.TILE_TOWN: '#808080'     # Grey
        }
        
    def on_key_press(self, event):
        '''Processes keyboard input.'''
        key = event.keysym
        if key == 'w':   # Up
            self.player.move('up')
        elif key == 's':   # Down
            self.player.move('down')
        elif key == 'a':   # Left
            self.player.move('left')
        elif key == 'd':   # Right
            self.player.move('right')
        
    def check_wild_encounter(self) -> bool:
        '''Checks for wild pokemon encounter.'''
        # Only in grass, 25% chance
        return random.random() < 0.25
    
    def check_trainer_encounter(self) -> Optional[Trainer]:
        '''Checks for trainer encounter.'''
        # TODO: Implement
        return None
    
    def get_zone(self) -> str:
        '''Gets the current zone (route1, route2, town).'''
        # TODO: Implement
        return 'town'
        
    def update_hud(self):
        '''Updates the HUD.'''
        # TODO: Implement
        
    def show(self):
        '''Shows the game world.'''
        self.world_frame.pack(fill='both', expand=True)
        self.draw_world()
        
    def hide(self):
        '''Hides the game world.'''
        self.world_frame.pack_forget()


# ============================================================
# TASK_4_MAIN_GAME
# ============================================================

import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class PokemonGame:
    '''Hauptklasse die alle Komponenten verbindet.'''
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pokemon Abenteuer")
        self.root.geometry("520x450")
        self.root.resizable(False, False)
        
        self.player = None
        self.game_world = None
        self.battle_system = None
        self.current_screen = "title"  # title, starter, world, battle
        
        self.show_title_screen()
        
    def show_title_screen(self):
        '''Zeigt den Titelbildschirm.'''
        self.clear_screen()
        
        title_frame = tk.Frame(self.root, bg='#FF0000')
        title_frame.pack(fill='both', expand=True)
        
        # ASCII-Art oder grosser Titel
        tk.Label(title_frame, text="⚡ POKEMON ⚡", 
                font=('Arial', 32, 'bold'), bg='#FF0000', fg='yellow').pack(pady=50)
        tk.Label(title_frame, text="ABENTEUER", 
                font=('Arial', 24), bg='#FF0000', fg='white').pack()
        
        tk.Button(title_frame, text="Neues Spiel", font=('Arial', 16),
                 command=self.start_new_game, width=15).pack(pady=30)
        tk.Button(title_frame, text="Spiel Laden", font=('Arial', 16),
                 command=self.load_game, width=15).pack(pady=10)
                 
    def start_new_game(self):
        '''Startet ein neues Spiel.'''
        name = simpledialog.askstring("Name", "Wie heisst du, Trainer?")
        if not name:
            name = "Ash"
        self.player = Player(name)
        self.show_starter_selection()
        
    def show_starter_selection(self):
        '''Zeigt Starter-Pokemon Auswahl.'''
        self.clear_screen()
        # Professor-Text
        # 3 Buttons fuer Chelast, Panflam, Plinfa
        # Mit Bild/Beschreibung fuer jedes
        
    def select_starter(self, starter_name: str):
        '''Waehlt Starter-Pokemon.'''
        starters = create_starter_pokemon()
        # Finde gewaehltes Pokemon
        # Fuege zum Team hinzu
        self.start_adventure()
        
    def start_adventure(self):
        '''Startet das eigentliche Spiel.'''
        self.current_screen = "world"
        self.game_world = GameWorld(
            self.root, 
            self.player,
            on_wild_encounter=self.start_wild_battle,
            on_trainer_encounter=self.start_trainer_battle
        )
        self.game_world.show()
        
    def start_wild_battle(self, wild_pokemon):
        '''Startet Kampf gegen wildes Pokemon.'''
        self.current_screen = "battle"
        self.game_world.hide()
        self.battle_system = BattleSystem(
            self.root, self.player, wild_pokemon,
            is_trainer_battle=False,
            on_battle_end=self.end_battle
        )
        self.battle_system.show()
        
    def start_trainer_battle(self, trainer):
        '''Startet Trainer-Kampf.'''
        # Zeige Trainer-Intro
        # Starte Kampf gegen erstes Trainer-Pokemon
        
    def end_battle(self, victory: bool, was_trainer: bool = False):
        '''Beendet Kampf und kehrt zur Welt zurueck.'''
        self.battle_system.hide()
        self.current_screen = "world"
        self.game_world.show()
        self.game_world.update_hud()
        
        # Pruefe ob alle Trainer besiegt
        self.check_victory()
        
    def check_victory(self):
        '''Prueft ob Spiel gewonnen.'''
        # Alle Trainer besiegt = Sieg
        
    def save_game(self):
        '''Speichert Spielstand als JSON.'''
        
    def load_game(self):
        '''Laedt Spielstand aus JSON.'''
        
    def clear_screen(self):
        '''Entfernt alle Widgets.'''
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def run(self):
        '''Startet das Spiel.'''
        self.root.mainloop()

if __name__ == "__main__":
    game = PokemonGame()
    game.run()
