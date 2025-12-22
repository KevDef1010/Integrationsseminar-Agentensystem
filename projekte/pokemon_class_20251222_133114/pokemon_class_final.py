# pokemon_class - Generiert durch Iterative Crew
# Iterationen: 1
# Tests bestanden: True

class Pokemon:
    def __init__(self, name, typ, level, max_hp, attacks):
        self.name = name
        self.typ = typ
        self.level = level
        self.max_hp = max_hp
        self.hp = max_hp
        self.attacks = attacks
    
    def take_damage(self, amount):
        self.hp -= amount
        return self.hp
    
    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        return self.hp
    
    def is_fainted(self):
        return self.hp <= 0
    
    def level_up(self):
        self.level += 1
        self.max_hp += 5
        self.heal(self.max_hp)
        return (self.level, self.max_hp)