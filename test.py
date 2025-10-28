import unittest
from game import Character, consumable, PlayerCharacter, Attributes

class TestPlayerCharacter(unittest.TestCase):
    def test_create_new_player_character(self):
        attr = Attributes(5, 5, 5)
        player = PlayerCharacter("herro there", "Mage", attr)
        self.assertEqual(player.name, "herro there")
        self.assertEqual(player.character_class, "Mage")
        self.assertEqual(player.attributes.strength, 5)
        self.assertEqual(player.attributes.agility, 5)
        self.assertEqual(player.attributes.mind, 5)

    def test_player_use_health_potion(self):
        attr = Attributes(3, 5, 7)
        player = PlayerCharacter("herro there", "Mage", attr)
        print(f"max health: {player.max_health}")
        player.current_health = 1
        health_potion = consumable("Health Potion", "heal", 10)
        player.inventory.append(health_potion)
        player.use_item("Health Potion")
        self.assertEqual(player.current_health, 11)
        
        player.current_health = player.max_health - 5
        potion2 = consumable("Health Potion", "heal", 10)
        player.inventory.append(potion2)
        player.use_item("Health Potion")
        self.assertEqual(player.current_health, player.max_health)
          # 10 + 10 from potion


if __name__ == '__main__':
    unittest.main()