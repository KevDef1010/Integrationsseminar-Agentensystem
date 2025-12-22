# Kampfsystem
# Generiert: 2025-12-22T13:22:18.367714

```python
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
```