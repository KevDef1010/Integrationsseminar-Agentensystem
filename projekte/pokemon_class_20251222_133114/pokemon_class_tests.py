# Tests fuer pokemon_class
import unittest

# Import der zu testenden Klasse
from pokemon_class_final import *

import unittest

class TestPokemon(unittest.TestCase):

    def setUp(self):
        self.pokemon = Pokemon("Bulbasaur", "Grass/Poison", 5, 45, ["Razer Leaf", "Vine Whip"])

    def test_init(self):
        self.assertEqual(self.pokemon.name, "Bulbasaur")
        self.assertEqual(self.pokemon.typ, "Grass/Poison")
        self.assertEqual(self.pokemon.level, 5)
        self.assertEqual(self.pokemon.max_hp, 45)
        self.assertEqual(self.pokemon.hp, 45)
        self.assertEqual(len(self.pokemon.attacks), 2)

    def test_take_damage(self):
        self.pokemon.take_damage(30)
        self.assertEqual(self.pokemon.hp, 15)
        self.pokemon.take_damage(46)
        self.assertTrue(self.pokemon.is_fainted())

    def test_heal(self):
        self.pokemon.take_damage(30)
        self.pokemon.heal(20)
        self.assertEqual(self.pokemon.hp, 35)
        self.pokemon.heal(46)
        self.assertEqual(self.pokemon.hp, 45)

    def test_is_fainted(self):
        self.assertFalse(self.pokemon.is_fainted())
        self.pokemon.take_damage(46)
        self.assertTrue(self.pokemon.is_fainted())

    def test_level_up(self):
        level, max_hp = self.pokemon.level_up()
        self.assertEqual(level, 6)
        self.assertEqual(max_hp, 50)
        self.assertEqual(self.pokemon.hp, 50)

if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()
