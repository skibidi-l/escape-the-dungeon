import unittest
from game import Armor, Character, Consumable, PlayerCharacter, Attributes, Weapon

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
        health_potion = Consumable("Health Potion", "heal", 10)
        player.inventory.append(health_potion)
        player.use_item("Health Potion")
        self.assertEqual(player.current_health, 11)
        
        player.current_health = player.max_health - 5
        potion2 = Consumable("Health Potion", "heal", 10)
        player.inventory.append(potion2)
        player.use_item("Health Potion")
        self.assertEqual(player.current_health, player.max_health)
          # 10 + 10 from potion


    def test_player_equip_weapon(self):
        attr = Attributes(4, 4, 4)
        player = PlayerCharacter("herro there", "Mage", attr)
        weapon = Weapon("Sword", "1d8")
        player.equip_weapon(weapon)
        print(f"Equipped weapon: {player.equipments.weapon}")
        self.assertEqual(player.equipments.weapon.name, "Sword")

    def test_player_equip_armor(self):
        attr = Attributes(4, 4, 4)
        player = PlayerCharacter("herro there", "Mage", attr)
        armor = Armor("Chainmail", "chainmail")
        player.equip_armor(armor)
        print(f"Equipped armor: {player.equipments.armor}")
        self.assertEqual(player.equipments.armor.name, "Chainmail")

    def test_player_unequip_weapon(self):
        attr = Attributes(4, 4, 4)
        player = PlayerCharacter("herro there", "Mage", attr)
        weapon = Weapon("long bow", "1d8")
        player.equip(weapon)
        print(f"Equipped weapon before unequip: {player.equipments.weapon}")
        player.unequip_weapon()
        print(f"Equipped weapon after unequip: {player.equipments.weapon}")
        self.assertIsNone(player.equipments.weapon)

    def test_player_unequip_weapon_error_case(self):
        attr = Attributes(4, 4, 4)
        player = PlayerCharacter("herro there", "Mage", attr)
        print(f"Players inventor befor unequip attempt: {player.inventory}")
        weapon = Weapon("dagger", "1d4")
        player.unequip_weapon()
        print(f"Players inventory after unequip attempt: {player.inventory}")
        self.assertListEqual(player.inventory, [])

if __name__ == '__main__':
    unittest.main()