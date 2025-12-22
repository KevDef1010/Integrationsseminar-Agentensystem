# battle_system - Generiert durch Iterative Crew
# Iterationen: 3
# Tests bestanden: False


class Pokemon:
def \_\_init\_\_(self, name, typ, level, hp, max_hp, attacks):
self.name = name
self.typ = typ
self.level = level
self.hp = hp
self.max_hp = max_hp
self.attacks = attacks

def take_damage(self, amount):
self.hp -= amount
if self.hp <= 0:
return f"{self.name} fainted!"
else:
return f"{self.name} took {amount} damage and has {self.hp}/{self.max_hp} HP left"

def is_fainted(self):
return self.hp <= 0

class Attack:
def \_\_init\_\_(self, name, damage, typ):
self.name = name
self.damage = damage
self.typ = typ

def execute(self, pokemon):
if self.typ in pokemon.typ:
# same type attack
return f"{pokemon.name} took {self.damage} damage from the {self.name}"
else:
# different type attack
return f"{pokemon.name} is not very effective against {self.typ} attacks"

class Battle:
def \_\_init\_\_(self, pokemon1, pokemon2):
self.pokemon1 = pokemon1
self.pokemon2 = pokemon2
self.current_turn = 0

def execute_attack(self, attacker_index, attack_index):
if self.current_turn == 0:
attacker = self.pokemon1
opponent = self.pokemon2
else:
attacker = self.pokemon2
opponent = self.pokemon1

attack = attacker.attacks[attack_index]

if not opponent.is_fainted():
return f"{opponent.name} used {opponent.typ} attack!"
else:
return f"{opponent.name} is fainted, {attacker.name} wins!"

def get_winner(self):
if self.pokemon1.is_fainted():
return self.pokemon2
elif self.pokemon2.is_fainted():
return self.pokemon1
else:
return None

def switch_turn(self):
if self.current_turn == 0:
self.current_turn = 1
else:
self.current_turn = 0