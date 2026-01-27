import unittest
from game import Armor, Character, Consumable, PlayerCharacter, Attributes, Weapon, NonPlayerCharacter, Spell, Skill, HealthPotion
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
        health_potion = HealthPotion("Small Health Potion", 10)
        player.inventory.append(health_potion)
        player.use_item("Small Health Potion")
        self.assertEqual(player.current_health, 11)
        
        player.current_health = player.max_health - 5
        potion2 = HealthPotion("Medium Health Potion", 20)
        player.inventory.append(potion2)
        player.use_item("Medium Health Potion")
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
    def test_mage_encounter(self):
        attr = Attributes(3, 4, 8)
        player = PlayerCharacter("herro there", "Mage", attr)
        player.equip_armor(Armor("cloth armor","cloth"))
        player.equip_weapon(Weapon("wooden staff","1d6"))
        fireball_spell = Spell("Fireball", "1d6", 120)

        player.learn_spell(fireball_spell)
        print(f"Player Spells: {[spell.name for spell in player.spells if spell is not None]}")

        goblin_monster = NonPlayerCharacter("Goblin","Beast", Attributes(3, 4, 8))
        goblin_monster.equip_armor(Armor("leather armor","leather"))
        goblin_monster.equip_weapon(Weapon("club","1d6"))

        while goblin_monster.current_health > 0 and player.current_health > 0:
            player.cast_spell("Fireball", goblin_monster)
            if goblin_monster.current_health <= 0:
                break

            hit = goblin_monster.attack(player)
            print(f"{goblin_monster.name} and hits for {hit} damage.")

        if goblin_monster.current_health <= 0:
            print("goblin defeated!")
        else:
            print("player defeated!")

    def test_skill_use(self):
        attr = Attributes(4, 8, 2)
        player = PlayerCharacter("herro there", "Rogue", attr)

        backstab_skill = Skill("Backstab", "3d6", 200)
        player.learn_skill(backstab_skill)
        self.assertEqual(player.skills[0].name, "Backstab")

        goblin_monster = NonPlayerCharacter("Goblin","Beast", Attributes(3, 4, 8))
        goblin_monster.equip_armor(Armor("leather armor","leather"))
        goblin_monster.equip_weapon(Weapon("club","1d6"))

        while goblin_monster.current_health > 0 and player.current_health > 0:
            player.use_skill("Backstab", goblin_monster)
            if goblin_monster.current_health <= 0:
                break

            hit = goblin_monster.attack(player)
            print(f"{goblin_monster.name} and hits for {hit} damage.")


if __name__ == '__main__':
    unittest.main()