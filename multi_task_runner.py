"""
Multi-Task Experiment Runner
=============================
Teilt komplexe Aufgaben in mehrere Sub-Tasks auf, die von 
spezialisierten Agents bearbeitet werden.

Dies loest das Context-Window-Problem bei grossen Projekten.
"""

import os
import json
import time
import re
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

from crewai import Agent, Task, Crew, LLM

# Import aus experiment_runner
from experiment_runner import (
    ExperimentConfig, ExperimentTracer, ExperimentResult,
    get_system_info, estimate_tokens
)


# ============================================================
# POKEMON GAME TASK DEFINITIONS
# ============================================================

POKEMON_TASKS = {
    "task_1_data_models": {
        "name": "Datenmodelle",
        "description": """Schreibe Python-Klassen fuer ein Pokemon-Spiel.

SCHREIBE NUR DIESE KLASSEN (vollstaendig implementiert):

```python
import random

class Attack:
    '''Eine Attacke mit Name, Typ und Schaden.'''
    def __init__(self, name: str, typ: str, damage: int):
        self.name = name
        self.typ = typ
        self.damage = damage

class Pokemon:
    '''Ein Pokemon mit allen Attributen und Methoden.'''
    def __init__(self, name: str, typ: str, level: int, max_hp: int, attacks: list):
        self.name = name
        self.typ = typ
        self.level = level
        self.hp = max_hp
        self.max_hp = max_hp
        self.attacks = attacks
        self.xp = 0
    
    def take_damage(self, damage: int) -> int:
        '''Nimmt Schaden und gibt verbleibende HP zurueck.'''
        # Implementiere vollstaendig
        
    def attack(self, target, attack_index: int) -> int:
        '''Greift Ziel an mit Typen-Effektivitaet.'''
        # Feuer > Pflanze > Wasser > Feuer
        # Implementiere vollstaendig
        
    def gain_xp(self, amount: int) -> bool:
        '''Gibt XP und returned True bei Level-Up.'''
        # Level-Up bei xp >= level * 50
        # Bei Level-Up: +5 max_hp, +2 attack damage
        # Implementiere vollstaendig
    
    def is_fainted(self) -> bool:
        '''Returned True wenn HP <= 0.'''
        
    def heal(self, amount: int):
        '''Heilt Pokemon bis max_hp.'''

class Player:
    '''Der Spieler mit Team und Inventar.'''
    def __init__(self, name: str):
        self.name = name
        self.team: List[Pokemon] = []
        self.position = [200, 200]  # x, y auf Canvas
        self.money = 500
        self.pokeballs = 10
        self.badges = 0
    
    def add_pokemon(self, pokemon: Pokemon) -> bool:
        '''Fuegt Pokemon zum Team hinzu (max 6).'''
        
    def get_active_pokemon(self) -> Pokemon:
        '''Gibt erstes nicht-besiegtes Pokemon zurueck.'''
        
    def has_usable_pokemon(self) -> bool:
        '''Prueft ob noch kampffaehige Pokemon da sind.'''
        
    def move(self, dx: int, dy: int, world_width: int, world_height: int):
        '''Bewegt Spieler um dx, dy (mit Grenzen).'''

class Trainer:
    '''Ein NPC-Trainer mit Pokemon-Team.'''
    def __init__(self, name: str, team: List[Pokemon], position: tuple, reward: int):
        self.name = name
        self.team = team
        self.position = position
        self.reward = reward
        self.defeated = False

# Vordefinierte Pokemon und Attacken
def create_starter_pokemon():
    '''Erstellt die 3 Starter-Pokemon.'''
    # Chelast (Pflanze), Panflam (Feuer), Plinfa (Wasser)
    # Jedes mit 4 Attacken, Level 5
    
def create_wild_pokemon(zone: str) -> Pokemon:
    '''Erstellt zufaelliges wildes Pokemon basierend auf Zone.'''
    # zone: "route1" (Level 2-4), "route2" (Level 4-7)
```

REGELN:
1. Alle Methoden VOLLSTAENDIG implementieren
2. Keine Platzhalter oder pass
3. Typen-Effektivitaet: Feuer>Pflanze>Wasser>Feuer, 1.5x Schaden
4. Beginne mit: import random""",
        "expected_output": "Vollstaendige Python-Klassen Attack, Pokemon, Player, Trainer mit allen Methoden"
    },
    
    "task_2_battle_system": {
        "name": "Kampfsystem",
        "description": """Schreibe die Battle-Klasse fuer ein Pokemon-Kampfsystem mit tkinter.

VORAUSSETZUNG: Die Klassen Pokemon, Attack, Player existieren bereits.

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

REGELN:
1. Alle Methoden VOLLSTAENDIG implementieren
2. HP-Balken muessen sich visuell aendern
3. Kampf-Log zeigt alle Aktionen
4. Schoenes UI mit pack() oder grid()""",
        "expected_output": "Vollstaendige BattleSystem-Klasse mit UI und Kampflogik"
    },
    
    "task_3_game_world": {
        "name": "Spielwelt",
        "description": """Schreibe die GameWorld-Klasse fuer die Pokemon-Spielwelt mit tkinter.

```python
import tkinter as tk
import random

class GameWorld:
    '''Die Spielwelt mit Karte, Bewegung und Begegnungen.'''
    
    # Tile-Typen
    TILE_GRASS = 0      # Gruenes Gras (wilde Pokemon moeglich)
    TILE_PATH = 1       # Brauner Weg (sicher)
    TILE_WATER = 2      # Blaues Wasser (nicht begehbar)
    TILE_TOWN = 3       # Graue Stadt (sicher)
    
    TILE_SIZE = 32
    
    def __init__(self, master: tk.Tk, player, on_wild_encounter=None, on_trainer_encounter=None):
        self.master = master
        self.player = player
        self.on_wild_encounter = on_wild_encounter
        self.on_trainer_encounter = on_trainer_encounter
        
        self.world_frame = tk.Frame(master)
        
        # Karte: 15x12 Tiles = 480x384 Pixel
        self.map_width = 15
        self.map_height = 12
        
        # Erstelle die Karte (2D-Array)
        self.create_map()
        
        # Trainer auf der Karte
        self.trainers = self.create_trainers()
        
        # Canvas fuer die Welt
        self.canvas = tk.Canvas(
            self.world_frame, 
            width=self.map_width * self.TILE_SIZE,
            height=self.map_height * self.TILE_SIZE,
            bg='darkgreen'
        )
        self.canvas.pack()
        
        # HUD oben
        self.create_hud()
        
        # Tastatur-Bindings
        self.master.bind('<KeyPress>', self.on_key_press)
        
        # Spieler-Sprite
        self.player_sprite = None
        
    def create_map(self):
        '''Erstellt die Spielkarte.'''
        # Erstelle 2D-Array mit Tile-Typen
        # Links: Stadt (TILE_TOWN)
        # Mitte: Weg mit Gras drumherum (Route 1)
        # Rechts: Mehr Gras (Route 2)
        self.tiles = []
        # Implementiere die Karte
        
    def create_trainers(self) -> list:
        '''Erstellt NPC-Trainer auf der Karte.'''
        # 2-3 Trainer mit je 2-3 Pokemon
        
    def create_hud(self):
        '''Erstellt Heads-Up-Display.'''
        # Zeigt: Spielername, Geld, Pokeballs, Team-Status
        
    def draw_world(self):
        '''Zeichnet die komplette Welt.'''
        self.canvas.delete('all')
        # Zeichne alle Tiles
        # Zeichne Trainer
        # Zeichne Spieler
        
    def draw_tile(self, x: int, y: int, tile_type: int):
        '''Zeichnet ein einzelnes Tile.'''
        colors = {
            self.TILE_GRASS: '#228B22',   # Waldgruen
            self.TILE_PATH: '#8B4513',    # Braun
            self.TILE_WATER: '#1E90FF',   # Blau
            self.TILE_TOWN: '#808080'     # Grau
        }
        
    def on_key_press(self, event):
        '''Verarbeitet Tastendruecke.'''
        # WASD oder Pfeiltasten
        # Pruefe Kollision mit Wasser
        # Pruefe Trainer-Begegnung
        # Pruefe wilde Pokemon im Gras (25% Chance)
        
    def check_wild_encounter(self) -> bool:
        '''Prueft auf wilde Pokemon-Begegnung.'''
        # Nur im Gras, 25% Chance
        
    def check_trainer_encounter(self) -> Optional[Trainer]:
        '''Prueft auf Trainer-Begegnung.'''
        
    def get_zone(self) -> str:
        '''Gibt aktuelle Zone zurueck (route1, route2, town).'''
        
    def update_hud(self):
        '''Aktualisiert das HUD.'''
        
    def show(self):
        '''Zeigt die Spielwelt.'''
        self.world_frame.pack(fill='both', expand=True)
        self.draw_world()
        
    def hide(self):
        '''Versteckt die Spielwelt.'''
        self.world_frame.pack_forget()
```

REGELN:
1. Alle Methoden VOLLSTAENDIG implementieren  
2. Karte muss visuell ansprechend sein
3. Bewegung mit WASD oder Pfeiltasten
4. Kollisionserkennung funktioniert""",
        "expected_output": "Vollstaendige GameWorld-Klasse mit Karte, Bewegung und Begegnungen"
    },
    
    "task_4_main_game": {
        "name": "Hauptspiel",
        "description": """Schreibe die Game-Hauptklasse die alles zusammenfuegt.

VORAUSSETZUNG: Pokemon, Player, BattleSystem, GameWorld existieren.

```python
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
```

REGELN:
1. Alle Methoden VOLLSTAENDIG implementieren
2. Smooth Uebergaenge zwischen Screens
3. Speichern/Laden muss funktionieren
4. Sieg-Bedingung pruefen""",
        "expected_output": "Vollstaendige PokemonGame-Klasse als Haupteinstiegspunkt"
    }
}


# ============================================================
# MULTI-TASK EXPERIMENT RUNNER
# ============================================================

def run_multi_task_experiment(
    experiment_name: str = "pokemon_multi_task",
    tasks: Dict[str, Dict] = None,
    models: Dict[str, str] = None,
    output_base_dir: str = "projekte"
) -> ExperimentResult:
    """
    Fuehrt ein Experiment mit mehreren spezialisierten Tasks durch.
    Jeder Task wird von einem eigenen Developer-Agent bearbeitet.
    Am Ende werden alle Code-Teile zu einer Datei zusammengefuegt.
    """
    
    if tasks is None:
        tasks = POKEMON_TASKS
    
    if models is None:
        models = {
            "developer": "codellama:13b",
            "integrator": "mistral:7b"
        }
    
    # Experiment Setup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    experiment_id = f"{experiment_name}_{timestamp}"
    output_dir = Path(output_base_dir) / experiment_id
    output_dir.mkdir(parents=True, exist_ok=True)
    
    config = ExperimentConfig(
        experiment_id=experiment_id,
        experiment_name=experiment_name,
        task_description="Pokemon RPG mit Multi-Task Architektur",
        models=models
    )
    
    tracer = ExperimentTracer(experiment_id, str(output_dir))
    tracer.start_experiment()
    
    print("=" * 70)
    print(f"🔬 MULTI-TASK EXPERIMENT: {experiment_name}")
    print(f"   ID: {experiment_id}")
    print(f"   Tasks: {len(tasks)}")
    print("=" * 70)
    
    # LLM fuer Developer
    developer_llm = LLM(
        model=f"ollama/{models['developer']}",
        base_url="http://localhost:11434"
    )
    
    code_outputs = {}
    experiment_start = time.time()
    
    try:
        # Jeden Task einzeln ausfuehren
        for task_id, task_config in tasks.items():
            print(f"\n{'='*50}")
            print(f"📝 Task: {task_config['name']}")
            print(f"{'='*50}")
            
            # Spezialisierter Developer fuer diesen Task
            developer = Agent(
                role=f"Python Developer - {task_config['name']}",
                goal="Schreibe VOLLSTAENDIGEN, AUSFUEHRBAREN Python-Code. Keine Platzhalter!",
                backstory=f"""Du bist ein Experte fuer {task_config['name']}.
                
KRITISCHE REGELN:
1. Schreibe NUR Python-Code, keine Erklaerungen
2. Jede Methode VOLLSTAENDIG implementieren
3. KEINE Platzhalter, KEIN 'pass', KEIN '...'
4. Code muss syntaktisch korrekt sein
5. Beginne direkt mit 'import' Statements""",
                llm=developer_llm,
                verbose=True
            )
            
            task = Task(
                description=task_config['description'],
                expected_output=task_config['expected_output'],
                agent=developer
            )
            
            crew = Crew(
                agents=[developer],
                tasks=[task],
                verbose=True
            )
            
            # Task tracken
            tracer.start_task(
                f"Developer-{task_config['name']}", 
                task_id, 
                models['developer']
            )
            
            task_start = time.time()
            result = crew.kickoff()
            task_duration = time.time() - task_start
            
            output_text = str(result)
            code_outputs[task_id] = output_text
            
            tracer.end_task(
                input_text=task_config['description'],
                output_text=output_text,
                success=True
            )
            
            # Speichere Teil-Output
            part_file = output_dir / f"{task_id}.py"
            with open(part_file, "w", encoding="utf-8") as f:
                f.write(f"# {task_config['name']}\n")
                f.write(f"# Generiert: {datetime.now().isoformat()}\n\n")
                f.write(output_text)
            
            print(f"✅ {task_config['name']} abgeschlossen ({task_duration:.1f}s)")
            print(f"   Output: {len(output_text)} Zeichen")
        
        # Code zusammenfuegen
        print(f"\n{'='*50}")
        print("🔧 Fuege Code zusammen...")
        print(f"{'='*50}")
        
        combined_code = combine_code_parts(code_outputs, output_dir)
        
        experiment_end = time.time()
        tracer.end_experiment()
        
        # Ergebnis speichern
        total_tokens = sum(m.estimated_output_tokens for m in tracer.agent_metrics)
        
        experiment_result = ExperimentResult(
            config=config,
            agent_metrics=tracer.agent_metrics,
            total_duration_seconds=round(experiment_end - experiment_start, 2),
            total_estimated_tokens=total_tokens,
            system_info=get_system_info(),
            crew_output=combined_code,
            individual_task_outputs=tracer.task_outputs,
            success=True
        )
        
        tracer.save_results(experiment_result)
        
        print(f"\n{'='*50}")
        print(f"✅ EXPERIMENT ABGESCHLOSSEN")
        print(f"   Dauer: {experiment_result.total_duration_seconds:.1f}s")
        print(f"   Tokens: {total_tokens}")
        print(f"   Output: {output_dir}")
        print(f"{'='*50}")
        
        return experiment_result
        
    except Exception as e:
        tracer.end_experiment()
        print(f"\n❌ FEHLER: {e}")
        raise


def combine_code_parts(code_outputs: Dict[str, str], output_dir: Path) -> str:
    """
    Kombiniert die einzelnen Code-Teile zu einer ausfuehrbaren Datei.
    """
    
    # Extrahiere Python-Code aus den Outputs
    def extract_code(text: str) -> str:
        """Extrahiert Code aus Markdown-Bloecken oder Text."""
        # Suche nach ```python ... ``` Bloecken
        code_blocks = re.findall(r'```python\n(.*?)```', text, re.DOTALL)
        if code_blocks:
            return '\n\n'.join(code_blocks)
        
        # Suche nach ``` ... ``` Bloecken
        code_blocks = re.findall(r'```\n(.*?)```', text, re.DOTALL)
        if code_blocks:
            return '\n\n'.join(code_blocks)
        
        # Nehme den gesamten Text
        return text
    
    parts = []
    
    # Header
    parts.append('''"""
Pokemon Abenteuer - Ein Pokemon-Diamant inspiriertes RPG
=========================================================
Generiert durch Multi-Agent System
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
from typing import List, Optional

''')
    
    # Fuege jeden Code-Teil hinzu
    for task_id in sorted(code_outputs.keys()):
        code = extract_code(code_outputs[task_id])
        parts.append(f"\n# {'='*60}")
        parts.append(f"# {task_id.upper()}")
        parts.append(f"# {'='*60}\n")
        parts.append(code)
    
    combined = '\n'.join(parts)
    
    # Speichere kombinierte Datei
    game_file = output_dir / "pokemon_adventure.py"
    with open(game_file, "w", encoding="utf-8") as f:
        f.write(combined)
    
    print(f"📦 Kombinierter Code: {game_file}")
    print(f"   Zeilen: {combined.count(chr(10))}")
    
    return combined


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║         MULTI-TASK EXPERIMENT RUNNER - Pokemon RPG                   ║
╠══════════════════════════════════════════════════════════════════════╣
║  Teilt das Pokemon-Spiel in 4 spezialisierte Tasks auf:              ║
║  1. Datenmodelle (Pokemon, Attack, Player, Trainer)                  ║
║  2. Kampfsystem (BattleSystem mit UI)                                ║
║  3. Spielwelt (GameWorld mit Karte und Bewegung)                     ║
║  4. Hauptspiel (Game-Klasse die alles verbindet)                     ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    print("Starte Multi-Task Experiment...")
    print("Dies kann 3-5 Minuten dauern.\n")
    
    result = run_multi_task_experiment()
    
    print(f"\n🎮 Spiel testen mit: python {result.config.experiment_id}/pokemon_adventure.py")
