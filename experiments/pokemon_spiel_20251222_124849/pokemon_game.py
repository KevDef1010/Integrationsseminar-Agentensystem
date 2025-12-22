"""
Pokemon Kampfspiel - Generiert vom Multi-Agent CrewAI System
=============================================================
Waehle ein Pokemon und kaempfe gegen den Computer!
"""

import tkinter as tk
from tkinter import messagebox
import random


class Pokemon:
    """Ein Pokemon mit Name, HP und Attacken."""
    
    def __init__(self, name, max_hp, pokemon_type, attacks):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.pokemon_type = pokemon_type
        self.attacks = attacks  # Dict: {"Attackenname": Schaden}
    
    def is_alive(self):
        return self.hp > 0
    
    def reset(self):
        self.hp = self.max_hp


class PokemonGame:
    """Hauptklasse fuer das Pokemon-Kampfspiel."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pokemon Kampfspiel")
        self.root.geometry("500x400")
        self.root.configure(bg="#2c3e50")
        
        # Pokemon definieren
        self.all_pokemon = [
            Pokemon("Pikachu", 100, "Elektro", {
                "Donnerblitz": 25,
                "Ruckzuckhieb": 15,
                "Donnerschock": 20,
                "Eisenschweif": 18
            }),
            Pokemon("Glumanda", 90, "Feuer", {
                "Glut": 20,
                "Kratzer": 12,
                "Flammenwurf": 28,
                "Drachenwut": 22
            }),
            Pokemon("Schiggy", 110, "Wasser", {
                "Aquaknarre": 18,
                "Tackle": 12,
                "Blubbstrahl": 25,
                "Panzerschutz": 15
            })
        ]
        
        self.player_pokemon = None
        self.enemy_pokemon = None
        self.game_active = False
        
        self.create_selection_screen()
    
    def create_selection_screen(self):
        """Zeigt den Pokemon-Auswahlbildschirm."""
        # Alte Widgets entfernen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Titel
        title = tk.Label(
            self.root, 
            text="Waehle dein Pokemon!",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title.pack(pady=20)
        
        # Pokemon-Buttons
        button_frame = tk.Frame(self.root, bg="#2c3e50")
        button_frame.pack(pady=20)
        
        colors = {"Elektro": "#f1c40f", "Feuer": "#e74c3c", "Wasser": "#3498db"}
        
        for pokemon in self.all_pokemon:
            btn = tk.Button(
                button_frame,
                text=f"{pokemon.name}\n({pokemon.pokemon_type})\nHP: {pokemon.max_hp}",
                font=("Arial", 12),
                width=12,
                height=4,
                bg=colors.get(pokemon.pokemon_type, "gray"),
                command=lambda p=pokemon: self.select_pokemon(p)
            )
            btn.pack(side=tk.LEFT, padx=10)
    
    def select_pokemon(self, pokemon):
        """Spieler waehlt ein Pokemon."""
        self.player_pokemon = pokemon
        self.player_pokemon.reset()
        
        # Gegner zufaellig waehlen (nicht das gleiche)
        available = [p for p in self.all_pokemon if p != pokemon]
        self.enemy_pokemon = random.choice(available)
        self.enemy_pokemon.reset()
        
        self.game_active = True
        self.create_battle_screen()
    
    def create_battle_screen(self):
        """Zeigt den Kampfbildschirm."""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Gegner-Bereich (oben)
        enemy_frame = tk.Frame(self.root, bg="#34495e", pady=10)
        enemy_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.enemy_name_label = tk.Label(
            enemy_frame,
            text=f"Gegner: {self.enemy_pokemon.name}",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="white"
        )
        self.enemy_name_label.pack()
        
        # Gegner HP-Bar
        self.enemy_hp_frame = tk.Frame(enemy_frame, bg="#34495e")
        self.enemy_hp_frame.pack(pady=5)
        
        tk.Label(self.enemy_hp_frame, text="HP:", bg="#34495e", fg="white").pack(side=tk.LEFT)
        
        self.enemy_hp_bar = tk.Canvas(self.enemy_hp_frame, width=200, height=20, bg="gray")
        self.enemy_hp_bar.pack(side=tk.LEFT, padx=5)
        
        self.enemy_hp_label = tk.Label(
            self.enemy_hp_frame,
            text=f"{self.enemy_pokemon.hp}/{self.enemy_pokemon.max_hp}",
            bg="#34495e",
            fg="white"
        )
        self.enemy_hp_label.pack(side=tk.LEFT)
        
        # Kampf-Log
        self.log_frame = tk.Frame(self.root, bg="#2c3e50")
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log_text = tk.Text(
            self.log_frame,
            height=6,
            font=("Arial", 10),
            bg="#1a252f",
            fg="white",
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Spieler-Bereich (unten)
        player_frame = tk.Frame(self.root, bg="#34495e", pady=10)
        player_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.player_name_label = tk.Label(
            player_frame,
            text=f"Dein Pokemon: {self.player_pokemon.name}",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="white"
        )
        self.player_name_label.pack()
        
        # Spieler HP-Bar
        self.player_hp_frame = tk.Frame(player_frame, bg="#34495e")
        self.player_hp_frame.pack(pady=5)
        
        tk.Label(self.player_hp_frame, text="HP:", bg="#34495e", fg="white").pack(side=tk.LEFT)
        
        self.player_hp_bar = tk.Canvas(self.player_hp_frame, width=200, height=20, bg="gray")
        self.player_hp_bar.pack(side=tk.LEFT, padx=5)
        
        self.player_hp_label = tk.Label(
            self.player_hp_frame,
            text=f"{self.player_pokemon.hp}/{self.player_pokemon.max_hp}",
            bg="#34495e",
            fg="white"
        )
        self.player_hp_label.pack(side=tk.LEFT)
        
        # Attacken-Buttons
        attack_frame = tk.Frame(self.root, bg="#2c3e50")
        attack_frame.pack(pady=10)
        
        self.attack_buttons = []
        for i, (attack_name, damage) in enumerate(self.player_pokemon.attacks.items()):
            btn = tk.Button(
                attack_frame,
                text=f"{attack_name}\n({damage} Schaden)",
                font=("Arial", 9),
                width=14,
                height=2,
                command=lambda a=attack_name, d=damage: self.player_attack(a, d)
            )
            btn.grid(row=i//2, column=i%2, padx=5, pady=5)
            self.attack_buttons.append(btn)
        
        self.update_hp_bars()
        self.log_message(f"Kampf beginnt! {self.player_pokemon.name} vs {self.enemy_pokemon.name}!")
    
    def update_hp_bars(self):
        """Aktualisiert die HP-Anzeigen."""
        # Spieler HP
        player_percent = max(0, self.player_pokemon.hp / self.player_pokemon.max_hp)
        self.player_hp_bar.delete("all")
        color = "#2ecc71" if player_percent > 0.5 else "#f39c12" if player_percent > 0.2 else "#e74c3c"
        self.player_hp_bar.create_rectangle(0, 0, 200 * player_percent, 20, fill=color)
        self.player_hp_label.config(text=f"{max(0, self.player_pokemon.hp)}/{self.player_pokemon.max_hp}")
        
        # Gegner HP
        enemy_percent = max(0, self.enemy_pokemon.hp / self.enemy_pokemon.max_hp)
        self.enemy_hp_bar.delete("all")
        color = "#2ecc71" if enemy_percent > 0.5 else "#f39c12" if enemy_percent > 0.2 else "#e74c3c"
        self.enemy_hp_bar.create_rectangle(0, 0, 200 * enemy_percent, 20, fill=color)
        self.enemy_hp_label.config(text=f"{max(0, self.enemy_pokemon.hp)}/{self.enemy_pokemon.max_hp}")
    
    def log_message(self, message):
        """Fuegt eine Nachricht zum Kampf-Log hinzu."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def player_attack(self, attack_name, damage):
        """Spieler greift an."""
        if not self.game_active:
            return
        
        # Zufaellige Schadensvariation (+/- 20%)
        actual_damage = int(damage * random.uniform(0.8, 1.2))
        self.enemy_pokemon.hp -= actual_damage
        
        self.log_message(f"{self.player_pokemon.name} setzt {attack_name} ein! ({actual_damage} Schaden)")
        self.update_hp_bars()
        
        # Pruefen ob Gegner besiegt
        if not self.enemy_pokemon.is_alive():
            self.game_over(won=True)
            return
        
        # Gegner greift zurueck
        self.root.after(500, self.enemy_attack)
    
    def enemy_attack(self):
        """Gegner greift an."""
        if not self.game_active:
            return
        
        attack_name, damage = random.choice(list(self.enemy_pokemon.attacks.items()))
        actual_damage = int(damage * random.uniform(0.8, 1.2))
        self.player_pokemon.hp -= actual_damage
        
        self.log_message(f"{self.enemy_pokemon.name} setzt {attack_name} ein! ({actual_damage} Schaden)")
        self.update_hp_bars()
        
        # Pruefen ob Spieler besiegt
        if not self.player_pokemon.is_alive():
            self.game_over(won=False)
    
    def game_over(self, won):
        """Spiel beenden und Ergebnis zeigen."""
        self.game_active = False
        
        # Buttons deaktivieren
        for btn in self.attack_buttons:
            btn.config(state=tk.DISABLED)
        
        if won:
            self.log_message(f"\n🎉 GEWONNEN! {self.enemy_pokemon.name} wurde besiegt!")
            result_text = "Du hast gewonnen!"
            result_color = "#2ecc71"
        else:
            self.log_message(f"\n💀 VERLOREN! {self.player_pokemon.name} wurde besiegt!")
            result_text = "Du hast verloren!"
            result_color = "#e74c3c"
        
        # Ergebnis-Label
        result_label = tk.Label(
            self.root,
            text=result_text,
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg=result_color
        )
        result_label.pack(pady=5)
        
        # Neustart-Button
        restart_btn = tk.Button(
            self.root,
            text="Neues Spiel",
            font=("Arial", 12),
            command=self.create_selection_screen
        )
        restart_btn.pack(pady=5)
    
    def run(self):
        """Startet das Spiel."""
        self.root.mainloop()


if __name__ == "__main__":
    print("Pokemon Kampfspiel startet...")
    print("Waehle ein Pokemon und kaempfe!")
    game = PokemonGame()
    game.run()
