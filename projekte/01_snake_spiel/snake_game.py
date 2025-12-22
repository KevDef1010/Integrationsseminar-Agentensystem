"""
Snake Spiel - Generiert vom Multi-Agent CrewAI System
======================================================
Steuerung: Pfeiltasten
Neustart: Leertaste oder R-Taste
Beenden: ESC oder Fenster schliessen
"""

import tkinter as tk
from random import randint


class SnakeGame:
    """Hauptklasse für das Snake-Spiel mit tkinter GUI."""
    
    def __init__(self):
        # Spielkonstanten
        self.CANVAS_WIDTH = 600
        self.CANVAS_HEIGHT = 400
        self.CELL_SIZE = 20
        self.GAME_SPEED = 150  # Millisekunden zwischen Updates
        
        # Tkinter Fenster erstellen
        self.root = tk.Tk()
        self.root.title("🐍 Snake Spiel - CrewAI Generated")
        self.root.resizable(False, False)
        
        # Score Label
        self.score_var = tk.StringVar()
        self.score_var.set("Punkte: 0")
        self.score_label = tk.Label(
            self.root, 
            textvariable=self.score_var, 
            font=("Arial", 16, "bold"),
            bg="black",
            fg="lime"
        )
        self.score_label.pack(fill=tk.X)
        
        # Canvas erstellen
        self.canvas = tk.Canvas(
            self.root,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Info Label
        self.info_label = tk.Label(
            self.root,
            text="Pfeiltasten: Steuern | Leertaste/R: Neustart | ESC: Beenden",
            font=("Arial", 10),
            bg="gray20",
            fg="white"
        )
        self.info_label.pack(fill=tk.X)
        
        # Tastatur-Bindings
        self.root.bind("<Up>", lambda e: self.change_direction("up"))
        self.root.bind("<Down>", lambda e: self.change_direction("down"))
        self.root.bind("<Left>", lambda e: self.change_direction("left"))
        self.root.bind("<Right>", lambda e: self.change_direction("right"))
        self.root.bind("<space>", lambda e: self.restart_game())
        self.root.bind("<r>", lambda e: self.restart_game())
        self.root.bind("<R>", lambda e: self.restart_game())
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        # Spiel initialisieren
        self.init_game()
        
    def init_game(self):
        """Initialisiert oder resettet das Spiel."""
        # Snake startet in der Mitte
        start_x = self.CANVAS_WIDTH // 2
        start_y = self.CANVAS_HEIGHT // 2
        
        # Snake als Liste von [x, y] Koordinaten
        self.snake = [
            [start_x, start_y],
            [start_x - self.CELL_SIZE, start_y],
            [start_x - 2 * self.CELL_SIZE, start_y]
        ]
        
        self.direction = "right"
        self.next_direction = "right"
        self.score = 0
        self.game_over = False
        self.score_var.set(f"Punkte: {self.score}")
        
        # Essen platzieren
        self.spawn_food()
        
        # Spielschleife starten
        self.game_loop()
    
    def spawn_food(self):
        """Platziert Essen an zufälliger Position."""
        while True:
            x = randint(0, (self.CANVAS_WIDTH - self.CELL_SIZE) // self.CELL_SIZE) * self.CELL_SIZE
            y = randint(0, (self.CANVAS_HEIGHT - self.CELL_SIZE) // self.CELL_SIZE) * self.CELL_SIZE
            self.food = [x, y]
            
            # Sicherstellen, dass Essen nicht auf Snake spawnt
            if self.food not in self.snake:
                break
    
    def change_direction(self, new_direction):
        """Ändert die Bewegungsrichtung der Snake."""
        # Verhindere 180-Grad-Wendungen
        opposites = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left"
        }
        
        if new_direction != opposites.get(self.direction):
            self.next_direction = new_direction
    
    def move_snake(self):
        """Bewegt die Snake in die aktuelle Richtung."""
        self.direction = self.next_direction
        
        # Neue Kopfposition berechnen
        head = self.snake[0].copy()
        
        if self.direction == "up":
            head[1] -= self.CELL_SIZE
        elif self.direction == "down":
            head[1] += self.CELL_SIZE
        elif self.direction == "left":
            head[0] -= self.CELL_SIZE
        elif self.direction == "right":
            head[0] += self.CELL_SIZE
        
        # Neuen Kopf vorne anfügen
        self.snake.insert(0, head)
        
        # Prüfen ob Essen gefressen
        if head == self.food:
            self.score += 10
            self.score_var.set(f"Punkte: {self.score}")
            self.spawn_food()
        else:
            # Schwanz entfernen wenn kein Essen
            self.snake.pop()
    
    def check_collision(self):
        """Prüft auf Kollisionen mit Wänden oder sich selbst."""
        head = self.snake[0]
        
        # Wandkollision
        if (head[0] < 0 or head[0] >= self.CANVAS_WIDTH or
            head[1] < 0 or head[1] >= self.CANVAS_HEIGHT):
            return True
        
        # Selbstkollision
        if head in self.snake[1:]:
            return True
        
        return False
    
    def draw(self):
        """Zeichnet das Spielfeld, Snake und Essen."""
        self.canvas.delete("all")
        
        # Gitter zeichnen (optional, für bessere Übersicht)
        for i in range(0, self.CANVAS_WIDTH, self.CELL_SIZE):
            self.canvas.create_line(i, 0, i, self.CANVAS_HEIGHT, fill="gray20")
        for i in range(0, self.CANVAS_HEIGHT, self.CELL_SIZE):
            self.canvas.create_line(0, i, self.CANVAS_WIDTH, i, fill="gray20")
        
        # Snake zeichnen
        for i, segment in enumerate(self.snake):
            # Kopf ist heller
            color = "lime" if i == 0 else "green"
            self.canvas.create_rectangle(
                segment[0], segment[1],
                segment[0] + self.CELL_SIZE, segment[1] + self.CELL_SIZE,
                fill=color,
                outline="darkgreen"
            )
        
        # Essen zeichnen
        self.canvas.create_oval(
            self.food[0] + 2, self.food[1] + 2,
            self.food[0] + self.CELL_SIZE - 2, self.food[1] + self.CELL_SIZE - 2,
            fill="red",
            outline="darkred"
        )
    
    def show_game_over(self):
        """Zeigt Game Over Bildschirm."""
        self.canvas.create_rectangle(
            self.CANVAS_WIDTH // 4, self.CANVAS_HEIGHT // 3,
            3 * self.CANVAS_WIDTH // 4, 2 * self.CANVAS_HEIGHT // 3,
            fill="gray20",
            outline="white"
        )
        self.canvas.create_text(
            self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 - 20,
            text="GAME OVER",
            font=("Arial", 24, "bold"),
            fill="red"
        )
        self.canvas.create_text(
            self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 + 10,
            text=f"Endstand: {self.score} Punkte",
            font=("Arial", 14),
            fill="white"
        )
        self.canvas.create_text(
            self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2 + 40,
            text="Leertaste drücken zum Neustarten",
            font=("Arial", 12),
            fill="yellow"
        )
    
    def restart_game(self):
        """Startet das Spiel neu."""
        if self.game_over:
            self.init_game()
    
    def game_loop(self):
        """Hauptspielschleife."""
        if not self.game_over:
            self.move_snake()
            
            if self.check_collision():
                self.game_over = True
                self.draw()
                self.show_game_over()
            else:
                self.draw()
                self.root.after(self.GAME_SPEED, self.game_loop)
    
    def run(self):
        """Startet das Spiel."""
        self.root.mainloop()


if __name__ == "__main__":
    print("🐍 Snake Spiel startet...")
    print("Steuerung: Pfeiltasten")
    print("Neustart: Leertaste oder R")
    print("Beenden: ESC oder Fenster schliessen")
    print("-" * 40)
    
    game = SnakeGame()
    game.run()
