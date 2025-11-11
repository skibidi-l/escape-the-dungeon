import random

armor_value = {
    "none": 0,
    "cloth armor": 1,
    "leather armor": 2,
    "chainmail armor": 3,
    "plate armor": 4,
    "dragon scale": 5,
}
class Item:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
    
class QuestItem(Item):
    def __init__(self, name):
        super().__init__(name)

class Consumable(Item):
    def __init__(self, name, effect, amount):
        super().__init__(name)
        self.effect = effect
        self.amount = amount

    def use(self, character):
        if self.effect == "heal":
            character.current_health += self.amount
            if character.current_health > character.max_health:
                character.current_health = character.max_health
            print(f"{character.name} used {self.amount} and healed 10 health points.")
        else:
            print(f"{self.name} has no effect.")
class Weapon(Item):
    def __init__(self, name, damage_dice):  
        super().__init__(name)
        self.damage = damage_dice
    def get_damage(self):   
        result = self.damage_dice.split('d')
        num_dice = int(result[0])
        sides = int(result[1])
        return roll_dice(sides_per_die=sides, number_of_dice=num_dice)

class Armor(Item):
    def __init__(self, name, type):
        super().__init__(name)
        self.type = type
        
    def get_defense(self):
        return armor_value[self.name]
    
class Equipment:
    def __init__(self, weapon, armor):
        self.weapon = weapon
        self.armor = armor

class Attributes:
    def __init__(self, strength, agility, mind):
        self.strength = strength
        self.agility = agility
        self.mind = mind

class Character:
    def __init__(self, name, character_class , attributes):
        self.name = name
        self.character_class = character_class
        self.max_health = attributes.strength * 5
        self.current_health = self.max_health
        self.attributes = attributes    
        self.equipments = Equipment(None,None)
        self.is_in_combat = False
    
    
    def equip_armor(self, armor):
        self.equipments.armor = armor

    def equip_weapon(self, weapon):
        self.equipments.weapon = weapon

    
    def get_armor_value(self):
        if self.equipments != None:
            return self.equipments.armor.get_defense()
        return 0
    
    def attack(self, target):
        damage = self.attributes.strength + roll_dice(sides_per_die=6)
        damage = damage - target.get_armor_value()
        target.current_health = target.current_health - damage
        return damage
    def dodge(self):
        dodge_chance = self.attributes.agility * 5
        if roll_dice(sides_per_die=100) <= dodge_chance:
            has_dodged = True
        else:
            has_dodged = False
        return has_dodged

    def show_stats(self):
        if self.is_in_combat == False:
            print("=======Character Stats=======")
            print(f"Name: {self.name}")
            print(f"Class: {self.character_class}")
            print(f"Health: {self.current_health}/{self.max_health}")
            print(f"Strength: {self.attributes.strength}")
            print(f"Agility: {self.attributes.agility}")
            print(f"Mind: {self.attributes.mind}")
        if self.equipments.weapon != None:
            print(f"Weapon: {self.equipments.weapon.name} (Damage: {self.equipments.weapon.damage})")
        else:
            print("Weapon: None")
        if self.equipments.armor != None:
            print(f"Armor: {self.equipments.armor.name} (Defense: {self.get_armor_value()})")
        else:
            print("Armor: None")

    def start_combat(self):
        self.is_in_combat = True

    def end_combat(self):
        self.is_in_combat = False
class PlayerCharacter(Character):
    def __init__(self, name, character_class, attributes):
        super().__init__(name, character_class, attributes)
        self.gold = 0
        self.inventory = []

    def unequip(self, item):
        if isinstance(item, Weapon):
            self.equipments.weapon = None
            self.inventory.append(item)
            print(f"You have unequipped the weapon: {item.name}")
        elif isinstance(item, Armor):
            self.equipments.armor = None
            self.inventory.append(item)
            print(f"You have unequipped the armor: {item.name}")
        else:
            print(f"You cannot unequip the item: {item.name}")

    def equip(self, item_name):
        for index, item in enumerate(self.inventory):
            if item.name.lower() == item_name:
                if isinstance(item, Weapon):
                    self.unequip(self.equipments.weapon)
                    del self.inventory[index]
                    self.equip_weapon(item)
                    print(f"you have equiped the weapon: {item.name}")
                elif isinstance(item, Armor):
                    self.unequip(self.equipments.armor)
                    del self.inventory[index]
                    print(f"you have equiped the armor: {item.name}")
                else:
                    print(f"you cannot equip the item: {item.name}, it is neither a weapon nor armor")

                break

    def is_in_inventory(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name:
                return True
        return False

    def use_item(self, item_name):
        for index, item in enumerate (self.inventory):
            if item.name.lower() == item_name.lower():
                if isinstance(item, Consumable):
                    print(f"Using item: {item.name}")
                    item.use(self)
                del self.inventory[index]
                break



class NonPlayerCharacter(Character):
    def __init__(self, name, character_class, attributes):
        super().__init__(name, character_class, attributes)

def roll_dice( sides_per_die, number_of_dice=1):
    total = 0
    for _ in range(number_of_dice):
        total += random.randint(1, sides_per_die)
    return total

def loot_roll(loot_list):
    number_of_loot_items = roll_dice(sides_per_die=3)
    looted_items = []
    for _ in range(number_of_loot_items):
        loot_item = random.choice(loot_list)
        looted_items.append(loot_item)
    return looted_items

def encounter(player, monster):
    print(f"You have encountered a {monster.name}!")
    player.start_combat()
    
    print(f"welcome to the dungeon dungeoneer, to test your might, you will have to duel...a good ole {monster.name}!")
    print(f"You have encountered a {monster.name}!")   
    print(f"⚠️ The {monster.name} attacks you!⚠️")

    loot_list = [
        Armor("cloth armor", "cloth armor"),
        Weapon("sword", "1d6"),
        Weapon("dagger", "1d4"),
        Weapon("staff", "1d4"),
        Weapon("mace", "1d6"),
        Weapon("axe", "1d6")
    ]

    print(loot_list)
    loot_list = [Armor("cloth armor", "cloth armor"),Armor("leather armor", "leather armor"),Armor("chainmail armor", "chainmail armor"),Armor("plate armor", "plate armor"),Armor("dragon scale", "dragon scale"),Weapon("sword", "1d6"),Weapon("dagger", "1d4"),Weapon("staff", "1d4"),Weapon("mace", "1d6"),Weapon("axe", "1d6")]
    while True:
        if player.current_health <= 0:
            break
        action = input("Choose action: attack / dodge / spell: ").lower()
        has_dodged = False
        
        if action == 'attack':
            damage = player.attack(monster)
            print(f"You swing your weapon and deal {damage} damage!")

            print(f"the Monster's health is {monster.current_health}")

        elif action == "dodge":
            has_dodged = player.dodge()
            if has_dodged:
                print("ya dodged the attack, well played...")
            else:
                print("ya tried to dodge but had a skill issue,lul")
        elif action == "spell":
            if player.attributes.mind>=6:
                print("ya cast a powerful fireball")
                monster.current_health = 0
                print("well done ")
            else:
                print("ya fail to cast the spell.")
        else:
            print("dumdass dont smash your keyboard!!!")
        if monster.current_health <= 0:
            print(f"congrats,your SOOOO good, well this is only thy beginning, you have slain a {monster.name}!")
            print("you may earn these items:")
            for loot in loot_list:
                print(loot)
            print("LET'S GO GAMBLINGGG!!! picking your rewards...")
            number_of_loot_items = roll_dice
            looted_items = loot_roll(loot_list)
            loot_gold = roll_dice(number_of_dice=5, sides_per_die=4)
            print(f"you found {looted_items} and {loot_gold} gold from the {monster.name}, u RICH now")
            player.inventory.extend(looted_items)
            player.gold += loot_gold
            break
        else:
            if not has_dodged:
                hit = monster.attack(player)
                print(f"The {monster.name} brandishes a knife, hitting a mighty swing dealing {hit} your player health depleted to {player.current_health}")

    player.end_combat()