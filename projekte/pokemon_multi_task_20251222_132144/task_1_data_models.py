# Datenmodelle
# Generiert: 2025-12-22T13:22:04.829916

```python
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
```