# Tests fuer battle_system
import unittest

# Import der zu testenden Klasse
from battle_system_final import *

from unittest import TestCase
from Pokemon import Attack, Pokemon, Battle

class TestPokemon(TestCase):
    def setUp(self):
        self.pikachu = Pokemon("Pikachu", "Electric", 50, 100, 100, [Attack("Thunder Shock", 10, "Electric")])
        self.bulbasaur = Pokemon("Bulbasaur", "Grass", 50, 80, 80, [Attack("Vine Whip", 5, "Grass")])
        self.battle = Battle(self.pikachu, self.bulbasaur)

    def test_init(self):
        self.assertEqual(self.pikachu.name, "Pikachu")
        self.assertEqual(self.pikachu.typ, "Electric")
        self.assertEqual(self.pikachu.level, 50)
        self.assertEqual(self.pikachu.hp, 100)
        self.assertEqual(self.pikachu.max_hp, 100)
        self.assertIn("Thunder Shock", self.pikachu.attacks)

    def test_take_damage(self):
        result = self.pikachu.take_damage(20)
        self.assertEqual(result, "Pikachu took 20 damage and has 80/100 HP left")
        result = self.pikachu.take_damage(90)
        self.assertEqual(result, "Pikachu fainted!")

    def test_heal(self):
        self.pikachu.hp = 10
        self.pikachu.heal(15)
        self.assertEqual(self.pikachu.hp, 25)
        self.assertLessEqual(self.pikachu.hp, 100)

    def test_is_fainted(self):
        self.assertTrue(self.pikachu.is_fainted())
        self.pikachu.heal(150)
        self.assertFalse(self.pikachu.is_fainted())

    def test_level_up(self):
        # Level up logic is not implemented, so this test will fail. Add level up functionality to the Pokemon class before running this test.
        self.pikachu.level += 5
        self.assertEqual(self.pikachu.max_hp, 120)
        self.assertGreater(self.pikachu.hp, 120)

    def test_execute_attack(self):
        result = self.battle.execute_attack(0, 0)
        self.assertEqual(result, "Bulbasaur used Grass attack!")
        self.bulbasaur.hp -= 15
        result = self.battle.execute_attack(0, 0)
        self.assertEqual(result, "Bulbasaur took 10 damage from the Thunder Shock and has 65/80 HP left")
        self.bulbasaur.hp -= 90
        result = self.battle.execute_attack(0, 0)
        self.assertEqual(result, "Bulbasaur fainted, Pikachu wins!")


if __name__ == '__main__':
    unittest.main()
