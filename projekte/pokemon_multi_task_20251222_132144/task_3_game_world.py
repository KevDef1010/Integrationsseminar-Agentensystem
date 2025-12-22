# Spielwelt
# Generiert: 2025-12-22T13:22:36.393467

```python
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
```